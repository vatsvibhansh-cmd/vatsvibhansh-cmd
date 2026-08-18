import os
import numpy as np
from PIL import Image, ImageOps, ImageFilter, ImageEnhance

def process_image(img_path):
    img = Image.open(img_path).convert('RGB')
    width, height = img.size
    
    # Head and shoulders crop: top 10% to 90%, center horizontal
    crop_aspect = 300 / 340
    img_aspect = width / height
    
    if img_aspect > crop_aspect:
        new_width = int(height * crop_aspect)
        left = (width - new_width) // 2
        img = img.crop((left, 0, left + new_width, height))
    else:
        new_height = int(width / crop_aspect)
        top = int((height - new_height) * 0.1) # keep face near top
        img = img.crop((0, top, width, top + new_height))
        
    img = img.resize((300, 340), Image.Resampling.LANCZOS)
    
    # Pre-processing as per spec:
    # autocontrast(cutoff=1) + UnsharpMask(radius=3, percent=140) + Contrast 1.3x
    gray = ImageOps.autocontrast(img.convert('L'), cutoff=1)
    gray = gray.filter(ImageFilter.UnsharpMask(radius=3, percent=140))
    enhancer = ImageEnhance.Contrast(gray)
    gray = enhancer.enhance(1.3)
    
    img_np = np.array(gray, dtype=np.float32)
    
    # Simple background segmentation mask for dark mode
    # Color distance check on original RGB image
    rgb_np = np.array(img, dtype=np.float32)
    # Background in photo is night sky / background elements (dark top, illuminated background)
    # Face & shirt have clear skin tones and dark jacket
    # Let's create foreground mask where face/hair/body is located
    h, w = img_np.shape
    mask = np.ones((h, w), dtype=bool)
    
    # Hard-clear border noise
    mask[0:15, :] = False
    
    return img_np, mask

def floyd_steinberg_dither_serpentine(arr, mask=None, invert=False):
    h, w = arr.shape
    img = arr.copy()
    output = np.zeros((h, w), dtype=np.uint8)
    
    for y in range(h):
        # Serpentine order: even rows L->R, odd rows R->L
        x_range = range(w) if y % 2 == 0 else range(w - 1, -1, -1)
        direction = 1 if y % 2 == 0 else -1
        
        for x in x_range:
            old_val = img[y, x]
            if mask is not None and not mask[y, x]:
                new_val = 255 if not invert else 0
            else:
                new_val = 255 if old_val > 128 else 0
                
            output[y, x] = new_val
            err = old_val - new_val
            
            # Error distribution (Floyd-Steinberg)
            # (x + dir, y): 7/16
            # (x - dir, y + 1): 3/16
            # (x, y + 1): 5/16
            # (x + dir, y + 1): 1/16
            if 0 <= x + direction < w:
                img[y, x + direction] += err * (7.0 / 16.0)
            if y + 1 < h:
                if 0 <= x - direction < w:
                    img[y + 1, x - direction] += err * (3.0 / 16.0)
                img[y + 1, x] += err * (5.0 / 16.0)
                if 0 <= x + direction < w:
                    img[y + 1, x + direction] += err * (1.0 / 16.0)
                    
    return output

def dither_to_svg_paths(dither_matrix, scale_x=1.2, scale_y=1.2, offset_x=45, offset_y=95, draw_white=False):
    # Converts 2D binary matrix into horizontal run-length SVG path strings
    h, w = dither_matrix.shape
    path_runs = []
    
    target_val = 255 if draw_white else 0
    
    for y in range(h):
        in_run = False
        start_x = 0
        for x in range(w):
            val = dither_matrix[y, x]
            is_match = (val == target_val)
            
            if is_match and not in_run:
                in_run = True
                start_x = x
            elif not is_match and in_run:
                in_run = False
                run_length = x - start_x
                px = offset_x + start_x * scale_x
                py = offset_y + y * scale_y
                pw = run_length * scale_x
                path_runs.append(f"M {px:.1f} {py:.1f} h {pw:.1f}")
                
        if in_run:
            run_length = w - start_x
            px = offset_x + start_x * scale_x
            py = offset_y + y * scale_y
            pw = run_length * scale_x
            path_runs.append(f"M {px:.1f} {py:.1f} h {pw:.1f}")
            
    return " ".join(path_runs)

img_path = r"C:\Users\Vibhansh Vats\.gemini\antigravity-ide\brain\91a6552c-a66b-4da4-a6d8-de676ebfd8c1\.user_uploaded\media_1787081387643.jpg"
gray_arr, mask = process_image(img_path)

# Invert gray for dark mode so lit areas have high density / white dots
dark_dither = floyd_steinberg_dither_serpentine(255 - gray_arr, mask=mask, invert=True)
light_dither = floyd_steinberg_dither_serpentine(gray_arr, mask=None, invert=False)

dark_path = dither_to_svg_paths(dark_dither, scale_x=1.2, scale_y=1.2, offset_x=36, offset_y=100, draw_white=True)
light_path = dither_to_svg_paths(light_dither, scale_x=1.2, scale_y=1.2, offset_x=36, offset_y=100, draw_white=False)

print(f"Dark path runs length: {len(dark_path)}")
print(f"Light path runs length: {len(light_path)}")

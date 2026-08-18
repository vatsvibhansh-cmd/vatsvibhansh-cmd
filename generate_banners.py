import os
import numpy as np
from PIL import Image, ImageOps, ImageFilter, ImageEnhance

def process_portrait_paths(img_path):
    img = Image.open(img_path).convert('RGB')
    width, height = img.size
    
    # Head and shoulders crop: top 5% to 85%, center horizontal
    crop_aspect = 300 / 340
    img_aspect = width / height
    
    if img_aspect > crop_aspect:
        new_width = int(height * crop_aspect)
        left = (width - new_width) // 2
        img = img.crop((left, 0, left + new_width, height))
    else:
        new_height = int(width / crop_aspect)
        top = int((height - new_height) * 0.05)
        img = img.crop((0, top, width, top + new_height))
        
    img = img.resize((300, 340), Image.Resampling.LANCZOS)
    
    # Contrast 1.3x only, with autocontrast(cutoff=1) + UnsharpMask(radius=3, percent=140)
    gray = ImageOps.autocontrast(img.convert('L'), cutoff=1)
    gray = gray.filter(ImageFilter.UnsharpMask(radius=3, percent=140))
    enhancer = ImageEnhance.Contrast(gray)
    gray = enhancer.enhance(1.3)
    
    img_np = np.array(gray, dtype=np.float32)
    
    # Background thresholding / segmentation for dark mode
    # Create mask for dark mode subject background removal
    h, w = img_np.shape
    mask = np.ones((h, w), dtype=bool)
    
    # Perform 1-bit Floyd-Steinberg dithering in serpentine order
    def dither(arr, invert=False):
        data = arr.copy()
        out = np.zeros((h, w), dtype=np.uint8)
        for y in range(h):
            x_range = range(w) if y % 2 == 0 else range(w - 1, -1, -1)
            direction = 1 if y % 2 == 0 else -1
            for x in x_range:
                old_v = data[y, x]
                new_v = 255 if old_v > 128 else 0
                out[y, x] = new_v
                err = old_v - new_v
                if 0 <= x + direction < w:
                    data[y, x + direction] += err * (7.0 / 16.0)
                if y + 1 < h:
                    if 0 <= x - direction < w:
                        data[y + 1, x - direction] += err * (3.0 / 16.0)
                    data[y + 1, x] += err * (5.0 / 16.0)
                    if 0 <= x + direction < w:
                        data[y + 1, x + direction] += err * (1.0 / 16.0)
        return out

    # Dark mode dither (dots draw lit subject)
    dark_matrix = dither(255 - gray_arr)
    # Light mode dither (dots draw dark parts)
    light_matrix = dither(gray_arr)

    def to_path(matrix, scale_x=1.16, scale_y=1.16, offset_x=55, offset_y=112, draw_white=True):
        path_runs = []
        target = 255 if draw_white else 0
        for y in range(h):
            in_run = False
            start_x = 0
            for x in range(w):
                is_match = (matrix[y, x] == target)
                if is_match and not in_run:
                    in_run = True
                    start_x = x
                elif not is_match and in_run:
                    in_run = False
                    run_len = x - start_x
                    px = offset_x + start_x * scale_x
                    py = offset_y + y * scale_y
                    pw = run_len * scale_x
                    path_runs.append(f"M {px:.1f} {py:.1f} h {pw:.1f}")
            if in_run:
                run_len = w - start_x
                px = offset_x + start_x * scale_x
                py = offset_y + y * scale_y
                pw = run_len * scale_x
                path_runs.append(f"M {px:.1f} {py:.1f} h {pw:.1f}")
        return " ".join(path_runs)

    dark_path = to_path(dark_matrix, draw_white=True)
    light_path = to_path(light_matrix, draw_white=False)
    
    return dark_path, light_path

img_path = r"C:\Users\Vibhansh Vats\.gemini\antigravity-ide\brain\91a6552c-a66b-4da4-a6d8-de676ebfd8c1\.user_uploaded\media_1787081387643.jpg"

# Global array calculation for helper
img_tmp = Image.open(img_path).convert('RGB')
w_t, h_t = img_tmp.size
crop_aspect = 300 / 340
img_aspect = w_t / h_t
if img_aspect > crop_aspect:
    new_w = int(h_t * crop_aspect)
    left = (w_t - new_w) // 2
    img_tmp = img_tmp.crop((left, 0, left + new_w, h_t))
else:
    new_h = int(w_t / crop_aspect)
    top = int((h_t - new_h) * 0.05)
    img_tmp = img_tmp.crop((0, top, w_t, top + new_h))
img_tmp = img_tmp.resize((300, 340), Image.Resampling.LANCZOS)
gray_arr = np.array(ImageEnhance.Contrast(ImageOps.autocontrast(img_tmp.convert('L'), cutoff=1).filter(ImageFilter.UnsharpMask(radius=3, percent=140))).enhance(1.3), dtype=np.float32)

dark_portrait_path, light_portrait_path = process_portrait_paths(img_path)

def generate_banner(is_dark=True):
    bg_color = '#0A101F' if is_dark else '#FAFAFA'
    term_bg = '#0D1527' if is_dark else '#FFFFFF'
    border_color = '#1E293B' if is_dark else '#CBD5E1'
    chrome_color = '#22D3EE' if is_dark else '#0891B2'
    label_color = '#94A3B8' if is_dark else '#64748B'
    val_color = '#F8FAFC' if is_dark else '#0F172A'
    accent_color = '#10B981' if is_dark else '#059669'
    purple_accent = '#A78BFA' if is_dark else '#7C3AED'
    dot_leader_color = '#1E293B' if is_dark else '#E2E8F0'
    panel_bg = '#070D18' if is_dark else '#F1F5F9'
    
    portrait_path = dark_portrait_path if is_dark else light_portrait_path
    
    rows = [
        ('Subject', 'Vibhansh Vats', val_color),
        ('Role', 'Data Scientist & ML Engineer', purple_accent),
        ('Origin', 'India', val_color),
        ('Education', 'Computer Science & Data Analytics', val_color),
        ('Status', 'Training Models + Analyzing Data + Shipping AI', accent_color),
        ('ToolChain', 'Python · PyTorch · Scikit-Learn · SQL · Jupyter', chrome_color),
        ('Core.Lang', 'Python · SQL · R · C++ · Julia', val_color),
        ('Core.ML', 'PyTorch · TensorFlow · Scikit-Learn · XGBoost', purple_accent),
        ('Core.Data', 'Pandas · NumPy · SciPy · Apache Spark', val_color),
        ('Core.Viz', 'Matplotlib · Seaborn · Plotly · Tableau', chrome_color),
        ('Grid.Mail', 'vatsvibhansh@gmail.com', val_color),
        ('Grid.Portfolio', 'github.com/vatsvibhansh-cmd', val_color),
        ('Grid.LinkedIn', 'linkedin.com/in/vibhansh-vats-729935279', chrome_color),
        ('Grid.GitHub', 'github.com/vatsvibhansh-cmd', purple_accent),
    ]

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1180 610" width="1180" height="610">
  <defs>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;500;600;700&amp;display=swap');
      .mono {{ font-family: 'Fira Code', monospace; }}
      .pulse {{ animation: pulse 2s infinite; }}
      .portrait-dots {{ shape-rendering: crispEdges; stroke: {purple_accent}; stroke-width: 1.15; fill: none; }}
      @keyframes pulse {{
        0%, 100% {{ opacity: 1; }}
        50% {{ opacity: 0.3; }}
      }}
    </style>
  </defs>

  <!-- Terminal Container Background -->
  <rect x="0" y="0" width="1180" height="610" rx="12" fill="{bg_color}"/>
  <rect x="2" y="2" width="1176" height="606" rx="10" fill="{term_bg}" stroke="{border_color}" stroke-width="2"/>

  <!-- Titlebar -->
  <rect x="2" y="2" width="1176" height="42" rx="10" fill="{panel_bg}"/>
  <circle cx="24" cy="23" r="6" fill="#EF4444"/>
  <circle cx="44" cy="23" r="6" fill="#F59E0B"/>
  <circle cx="64" cy="23" r="6" fill="#10B981"/>
  <text x="590" y="27" text-anchor="middle" fill="{label_color}" font-size="13" class="mono" font-weight="500">profile.sh --live</text>

  <!-- LEFT PANEL: VISUAL.MAP (Floyd-Steinberg Dithered Portrait of Vibhansh Vats) -->
  <g transform="translate(24, 60)">
    <rect x="0" y="0" width="420" height="524" rx="8" fill="{panel_bg}" stroke="{border_color}" stroke-width="1.5"/>
    
    <!-- Panel Header -->
    <text x="20" y="32" fill="{chrome_color}" font-size="13" class="mono" font-weight="700">VISUAL.MAP</text>
    <rect x="115" y="18" width="165" height="20" rx="10" fill="{purple_accent}20"/>
    <text x="197" y="32" text-anchor="middle" fill="{purple_accent}" font-size="11" class="mono" font-weight="600">PORTRAIT.DITHER_1BIT</text>

    <!-- Portrait Canvas Frame -->
    <rect x="16" y="48" width="388" height="400" rx="6" fill="{bg_color}" stroke="{border_color}" stroke-width="1"/>

    <!-- Dithered Vector Portrait Run-Length Path -->
    <path d="{portrait_path}" class="portrait-dots"/>

    <!-- Overlay Corner HUD Brackets -->
    <path d="M 22 60 L 22 75 M 22 60 L 37 60" stroke="{chrome_color}" stroke-width="1.5" fill="none"/>
    <path d="M 398 60 L 398 75 M 398 60 L 383 60" stroke="{chrome_color}" stroke-width="1.5" fill="none"/>
    <path d="M 22 436 L 22 421 M 22 436 L 37 436" stroke="{chrome_color}" stroke-width="1.5" fill="none"/>
    <path d="M 398 436 L 398 421 M 398 436 L 383 436" stroke="{chrome_color}" stroke-width="1.5" fill="none"/>

    <!-- Bottom Metrics Bar inside Left Panel -->
    <rect x="16" y="460" width="388" height="48" rx="6" fill="{bg_color}" stroke="{border_color}" stroke-width="1"/>
    <text x="30" y="480" fill="{label_color}" font-size="11" class="mono">PIPELINE: Floyd-Steinberg 300x340</text>
    <text x="30" y="496" fill="{chrome_color}" font-size="11" class="mono">DENSITY: 1-Bit Dither · CrispEdges</text>
    <rect x="300" y="472" width="90" height="24" rx="12" fill="{accent_color}20" stroke="{accent_color}" stroke-width="1"/>
    <text x="345" y="488" text-anchor="middle" fill="{accent_color}" font-size="11" class="mono" font-weight="700">VERIFIED</text>
  </g>

  <!-- RIGHT PANEL: SYSTEM.INFO Readout -->
  <g transform="translate(470, 60)">
    <text x="0" y="32" fill="{chrome_color}" font-size="14" class="mono" font-weight="700">SYSTEM.INFO</text>
    
    <circle cx="125" cy="27" r="5" fill="{accent_color}" class="pulse"/>
    <text x="136" y="31" fill="{accent_color}" font-size="12" class="mono" font-weight="700">LIVE</text>

    <rect x="520" y="10" width="166" height="28" rx="14" fill="{panel_bg}" stroke="{chrome_color}" stroke-width="1.5"/>
    <text x="603" y="29" text-anchor="middle" fill="{chrome_color}" font-size="13" class="mono" font-weight="600">@vatsvibhansh-cmd</text>

    <line x1="0" y1="48" x2="686" y2="48" stroke="{border_color}" stroke-width="1"/>
'''

    y_start = 80
    row_gap = 33

    for i, (label, val, color) in enumerate(rows):
        y = y_start + i * row_gap
        label_w = len(label) * 9.5 + 15
        val_w = len(val) * 8.5 + 15
        x1 = label_w
        x2 = 686 - val_w
        
        svg += f'''    <text x="0" y="{y}" fill="{label_color}" font-size="14" class="mono" font-weight="500">{label}</text>
    <line x1="{x1:.1f}" y1="{y-4}" x2="{x2:.1f}" y2="{y-4}" stroke="{dot_leader_color}" stroke-width="1.5" stroke-dasharray="2 4"/>
    <text x="686" y="{y}" text-anchor="end" fill="{color}" font-size="14" class="mono" font-weight="600" textLength="{len(val)*9.2:.1f}" lengthAdjust="spacingAndGlyphs">{val}</text>
'''

    svg += f'''  </g>
</svg>'''
    return svg

out_dir = r'C:\Users\Vibhansh Vats\.gemini\antigravity-ide\scratch\vatsvibhansh-cmd'
with open(os.path.join(out_dir, 'dark.svg'), 'w', encoding='utf-8') as f:
    f.write(generate_banner(True))

with open(os.path.join(out_dir, 'light.svg'), 'w', encoding='utf-8') as f:
    f.write(generate_banner(False))

print('SUCCESS_PORTRAIT_BANNER_GENERATED')

import os

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
      .glow {{ filter: drop-shadow(0px 0px 6px {purple_accent}80); }}
      .flow-line {{ stroke-dasharray: 8 8; animation: dash 20s linear infinite; }}
      @keyframes pulse {{
        0%, 100% {{ opacity: 1; }}
        50% {{ opacity: 0.3; }}
      }}
      @keyframes dash {{
        to {{ stroke-dashoffset: -1000; }}
      }}
    </style>
    <linearGradient id="panelGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{purple_accent}" stop-opacity="0.15"/>
      <stop offset="100%" stop-color="{chrome_color}" stop-opacity="0.05"/>
    </linearGradient>
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

  <!-- LEFT PANEL: VISUAL.MAP (Data Science & ML Matrix Topology) -->
  <g transform="translate(24, 60)">
    <rect x="0" y="0" width="420" height="524" rx="8" fill="{panel_bg}" stroke="{border_color}" stroke-width="1.5"/>
    
    <!-- Panel Header -->
    <text x="20" y="32" fill="{chrome_color}" font-size="13" class="mono" font-weight="700">VISUAL.MAP</text>
    <rect x="115" y="18" width="160" height="20" rx="10" fill="{purple_accent}20"/>
    <text x="195" y="32" text-anchor="middle" fill="{purple_accent}" font-size="11" class="mono" font-weight="600">DS.NEURAL_MATRIX</text>

    <!-- Visual Canvas Area -->
    <rect x="16" y="48" width="388" height="400" rx="6" fill="{bg_color}" stroke="{border_color}" stroke-width="1"/>
    
    <!-- Matrix Grid Lines -->
    <path d="M 16 128 L 404 128 M 16 208 L 404 208 M 16 288 L 404 288 M 16 368 L 404 368" stroke="{dot_leader_color}" stroke-width="1" stroke-dasharray="4 4"/>
    <path d="M 93 48 L 93 448 M 170 48 L 170 448 M 247 48 L 247 448 M 324 48 L 324 448" stroke="{dot_leader_color}" stroke-width="1" stroke-dasharray="4 4"/>

    <!-- Neural Network Graph & Data Nodes -->
    <path d="M 65 140 Q 150 90 210 180 T 350 120" fill="none" stroke="{purple_accent}" stroke-width="2" class="flow-line" opacity="0.8"/>
    <path d="M 65 240 Q 140 320 220 220 T 350 310" fill="none" stroke="{chrome_color}" stroke-width="2" class="flow-line" opacity="0.8"/>
    <path d="M 65 340 Q 180 200 240 340 T 350 220" fill="none" stroke="{accent_color}" stroke-width="2" class="flow-line" opacity="0.7"/>

    <!-- Scatter Plot / Dither Cluster Points -->
    <g class="glow">
      <circle cx="65" cy="140" r="7" fill="{purple_accent}"/>
      <circle cx="65" cy="240" r="7" fill="{chrome_color}"/>
      <circle cx="65" cy="340" r="7" fill="{accent_color}"/>
      
      <circle cx="170" cy="100" r="6" fill="{chrome_color}"/>
      <circle cx="170" cy="200" r="6" fill="{purple_accent}"/>
      <circle cx="170" cy="300" r="6" fill="{accent_color}"/>
      <circle cx="170" cy="390" r="6" fill="{chrome_color}"/>

      <circle cx="260" cy="130" r="6" fill="{accent_color}"/>
      <circle cx="260" cy="230" r="6" fill="{chrome_color}"/>
      <circle cx="260" cy="330" r="6" fill="{purple_accent}"/>

      <circle cx="350" cy="120" r="8" fill="{purple_accent}"/>
      <circle cx="350" cy="220" r="8" fill="{accent_color}"/>
      <circle cx="350" cy="310" r="8" fill="{chrome_color}"/>
    </g>

    <!-- Data Stream Particles -->
    <circle cx="115" cy="115" r="3" fill="{purple_accent}" class="pulse"/>
    <circle cx="215" cy="165" r="3" fill="{chrome_color}" class="pulse"/>
    <circle cx="305" cy="175" r="3" fill="{accent_color}" class="pulse"/>
    <circle cx="120" cy="275" r="3" fill="{accent_color}" class="pulse"/>

    <!-- Training Loss Curve overlay -->
    <path d="M 26 430 C 100 420 150 380 220 370 C 300 360 350 355 394 352 L 394 440 L 26 440 Z" fill="url(#panelGrad)" opacity="0.6"/>
    <path d="M 26 430 C 100 420 150 380 220 370 C 300 360 350 355 394 352" fill="none" stroke="{accent_color}" stroke-width="2"/>
    <text x="35" y="420" fill="{accent_color}" font-size="10" class="mono" font-weight="600">loss: 0.0031</text>
    <text x="310" y="370" fill="{purple_accent}" font-size="10" class="mono" font-weight="600">acc: 99.4%</text>

    <!-- Bottom Metrics Bar inside Left Panel -->
    <rect x="16" y="460" width="388" height="48" rx="6" fill="{bg_color}" stroke="{border_color}" stroke-width="1"/>
    <text x="30" y="480" fill="{label_color}" font-size="11" class="mono">MODEL: Transformer / GNN</text>
    <text x="30" y="496" fill="{chrome_color}" font-size="11" class="mono">PARAMS: 17.4M · EPOCH: 500</text>
    <rect x="300" y="472" width="90" height="24" rx="12" fill="{accent_color}20" stroke="{accent_color}" stroke-width="1"/>
    <text x="345" y="488" text-anchor="middle" fill="{accent_color}" font-size="11" class="mono" font-weight="700">OPTIMAL</text>
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

print('SUCCESS')

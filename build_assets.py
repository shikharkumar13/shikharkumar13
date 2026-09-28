"""Generates the self-hosted SVG visuals for the GitHub profile README.

Run:  python3 build_assets.py   -> writes assets/*.svg
Every visual that sits on a page background has a light and a dark file,
switched in the README with <picture> + prefers-color-scheme.
"""
from pathlib import Path

OUT = Path(__file__).parent / "assets"
OUT.mkdir(exist_ok=True)

FONT = "-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,monospace"

THEMES = {
    "light": dict(card="#ffffff", border="#d0d7de", text="#1f2328", muted="#59636e",
                  track="#e6e9ef", a1="#4f46e5", a2="#0d9488", a3="#7c3aed"),
    "dark":  dict(card="#161b22", border="#30363d", text="#e6edf3", muted="#9198a1",
                  track="#262c36", a1="#818cf8", a2="#2dd4bf", a3="#a78bfa"),
}


# --------------------------------------------------------------------------
# 1. Header banner (one file: its own coloured background works on both themes)
# --------------------------------------------------------------------------
def banner() -> str:
    # small neural-net motif on the right
    layers = [(870, [95, 145, 195, 245]), (980, [70, 120, 170, 220, 270]), (1090, [120, 170, 220])]
    edges, nodes = [], []
    k = 0
    for (x1, ys1), (x2, ys2) in zip(layers, layers[1:]):
        for y1 in ys1:
            for y2 in ys2:
                k += 1
                edges.append(
                    f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" class="edge" '
                    f'style="animation-delay:{(k % 7) * 0.35:.2f}s"/>')
    k = 0
    for x, ys in layers:
        for y in ys:
            k += 1
            nodes.append(f'<circle cx="{x}" cy="{y}" r="8" class="node" '
                         f'style="animation-delay:{(k % 5) * 0.4:.1f}s"/>')

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 340" width="1200" height="340" role="img" aria-label="Shikhar, Data Scientist: Machine Learning, MLOps and Generative AI">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#312e81">
        <animate attributeName="stop-color" values="#312e81;#4c1d95;#134e4a;#312e81" dur="14s" repeatCount="indefinite"/>
      </stop>
      <stop offset="55%" stop-color="#4f46e5">
        <animate attributeName="stop-color" values="#4f46e5;#7c3aed;#0f766e;#4f46e5" dur="14s" repeatCount="indefinite"/>
      </stop>
      <stop offset="100%" stop-color="#0d9488">
        <animate attributeName="stop-color" values="#0d9488;#4f46e5;#7c3aed;#0d9488" dur="14s" repeatCount="indefinite"/>
      </stop>
    </linearGradient>
    <pattern id="dots" width="26" height="26" patternUnits="userSpaceOnUse">
      <circle cx="2" cy="2" r="1.4" fill="#ffffff" opacity=".10"/>
    </pattern>
    <clipPath id="round"><rect width="1200" height="340" rx="22"/></clipPath>
  </defs>
  <style>
    .edge {{ stroke:#ffffff; stroke-width:1.3; opacity:.14; animation:pulse 3.2s ease-in-out infinite; }}
    .node {{ fill:#ffffff; animation:glow 2.6s ease-in-out infinite; }}
    .fade {{ animation:rise .9s ease-out both; }}
    @keyframes pulse {{ 0%,100% {{ opacity:.10 }} 50% {{ opacity:.45 }} }}
    @keyframes glow  {{ 0%,100% {{ opacity:.55 }} 50% {{ opacity:1 }} }}
    @keyframes rise  {{ from {{ opacity:0; transform:translateY(10px) }} to {{ opacity:1; transform:none }} }}
    @media (prefers-reduced-motion: reduce) {{ * {{ animation:none !important }} }}
  </style>
  <g clip-path="url(#round)">
    <rect width="1200" height="340" fill="url(#bg)"/>
    <rect width="1200" height="340" fill="url(#dots)"/>
    <g>{''.join(edges)}</g>
    <g>{''.join(nodes)}</g>
  </g>
  <g font-family="{FONT}" fill="#ffffff">
    <text x="70" y="92" font-size="22" font-family="{MONO}" opacity=".85" class="fade">~/shikharkumar13 $ whoami</text>
    <text x="68" y="168" font-size="72" font-weight="800" letter-spacing="-1" class="fade" style="animation-delay:.15s">Shikhar</text>
    <text x="70" y="218" font-size="34" font-weight="700" class="fade" style="animation-delay:.3s">Data Scientist</text>
    <text x="70" y="262" font-size="21" opacity=".88" class="fade" style="animation-delay:.45s">Machine Learning  ·  MLOps  ·  Generative AI   |   Taught 20,000+ professionals</text>
  </g>
</svg>
'''


# --------------------------------------------------------------------------
# 2. "How I build ML systems" pipeline
# --------------------------------------------------------------------------
STAGES = [
    ("01", "Version data", "pandas · SQL · DVC"),
    ("02", "Feature pipelines", "scikit-learn"),
    ("03", "Train &amp; track", "LightGBM · MLflow"),
    ("04", "Serve", "FastAPI · Docker"),
    ("05", "Monitor", "drift · CI/CD"),
]


def pipeline(t: dict) -> str:
    W, bw, bh, top = 1000, 168, 96, 30
    xs = [100 + i * 200 for i in range(5)]
    cy = top + bh / 2
    boxes, arrows = [], []
    for i, (x, (num, title, tools)) in enumerate(zip(xs, STAGES)):
        col = [t["a1"], t["a3"], t["a1"], t["a2"], t["a2"]][i]
        boxes.append(f'''
    <g class="stage" style="animation-delay:{i * 0.12:.2f}s">
      <rect x="{x - bw / 2}" y="{top}" width="{bw}" height="{bh}" rx="12" fill="{t["card"]}" stroke="{t["border"]}"/>
      <rect x="{x - bw / 2}" y="{top}" width="{bw}" height="5" rx="2.5" fill="{col}"/>
      <text x="{x - bw / 2 + 16}" y="{top + 30}" font-family="{MONO}" font-size="13" font-weight="700" fill="{col}">{num}</text>
      <text x="{x - bw / 2 + 16}" y="{top + 56}" font-size="17" font-weight="700" fill="{t["text"]}">{title}</text>
      <text x="{x - bw / 2 + 16}" y="{top + 80}" font-size="13.5" fill="{t["muted"]}">{tools}</text>
    </g>''')
    for x in xs[:-1]:
        arrows.append(f'<line x1="{x + bw / 2 + 4}" y1="{cy}" x2="{x + 200 - bw / 2 - 8}" y2="{cy}" class="flow" marker-end="url(#ah)"/>')
    # feedback loop: monitor -> ingest
    yb = top + bh
    loop = (f'<path d="M {xs[4]} {yb + 4} V {yb + 52} Q {xs[4]} {yb + 62} {xs[4] - 10} {yb + 62} '
            f'H {xs[0] + 10} Q {xs[0]} {yb + 62} {xs[0]} {yb + 52} V {yb + 10}" class="flow loop" marker-end="url(#ah2)"/>')
    label_w = 270
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} 212" width="{W}" height="212" role="img" aria-label="ML system lifecycle: ingest, features, train, serve, monitor, retrain">
  <defs>
    <marker id="ah" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="{t["muted"]}"/></marker>
    <marker id="ah2" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="{t["a2"]}"/></marker>
  </defs>
  <style>
    .flow {{ stroke:{t["muted"]}; stroke-width:2; fill:none; stroke-dasharray:6 5; animation:dash 1.4s linear infinite; }}
    .loop {{ stroke:{t["a2"]}; }}
    .stage {{ animation:rise .6s ease-out both; }}
    @keyframes dash {{ to {{ stroke-dashoffset:-22 }} }}
    @keyframes rise {{ from {{ opacity:0; transform:translateY(8px) }} to {{ opacity:1; transform:none }} }}
    @media (prefers-reduced-motion: reduce) {{ * {{ animation:none !important }} }}
  </style>
  <g font-family="{FONT}">
    {''.join(arrows)}
    {loop}
    {''.join(boxes)}
    <rect x="{W / 2 - label_w / 2}" y="{yb + 50}" width="{label_w}" height="24" rx="12" fill="{t["card"]}" stroke="{t["a2"]}"/>
    <text x="{W / 2}" y="{yb + 67}" text-anchor="middle" font-size="13" font-weight="600" fill="{t["a2"]}">retrain with Prefect when data drifts</text>
  </g>
</svg>
'''


# --------------------------------------------------------------------------
# 3. Learning path across the teaching repos
# --------------------------------------------------------------------------
PATH = [
    ("Python", "20 chapters"),
    ("Statistics", "13 articles"),
    ("Feature Eng.", "10 notebooks"),
    ("ML Algorithms", "hands-on"),
    ("MLOps", "13 articles"),
    ("Generative AI", "42-article path"),
]


def learning_path(t: dict) -> str:
    W = 1000
    xs = [85 + i * 166 for i in range(len(PATH))]
    y = 58
    dots = []
    for i, (x, (name, sub)) in enumerate(zip(xs, PATH)):
        dots.append(f'''
    <g class="step" style="animation-delay:{i * 0.15:.2f}s">
      <circle cx="{x}" cy="{y}" r="21" fill="{t["card"]}" stroke="url(#g)" stroke-width="3"/>
      <text x="{x}" y="{y + 5}" text-anchor="middle" font-family="{MONO}" font-size="14" font-weight="700" fill="{t["text"]}">{i + 1}</text>
      <text x="{x}" y="{y + 50}" text-anchor="middle" font-size="16" font-weight="700" fill="{t["text"]}">{name}</text>
      <text x="{x}" y="{y + 72}" text-anchor="middle" font-size="13.5" fill="{t["muted"]}">{sub}</text>
    </g>''')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} 150" width="{W}" height="150" role="img" aria-label="Learning path: Python, Statistics, Feature Engineering, ML Algorithms, MLOps, Generative AI">
  <defs>
    <linearGradient id="g" gradientUnits="userSpaceOnUse" x1="{xs[0]}" y1="0" x2="{xs[-1]}" y2="0">
      <stop offset="0" stop-color="{t["a1"]}"/><stop offset=".5" stop-color="{t["a3"]}"/><stop offset="1" stop-color="{t["a2"]}"/>
    </linearGradient>
  </defs>
  <style>
    .run {{ stroke:url(#g); stroke-width:4; stroke-dasharray:14 10; animation:dash 1.6s linear infinite; }}
    .step {{ animation:rise .6s ease-out both; }}
    @keyframes dash {{ to {{ stroke-dashoffset:-48 }} }}
    @keyframes rise {{ from {{ opacity:0; transform:translateY(8px) }} to {{ opacity:1; transform:none }} }}
    @media (prefers-reduced-motion: reduce) {{ * {{ animation:none !important }} }}
  </style>
  <g font-family="{FONT}">
    <line x1="{xs[0]}" y1="{y}" x2="{xs[-1]}" y2="{y}" stroke="{t["track"]}" stroke-width="4" stroke-linecap="round"/>
    <line x1="{xs[0]}" y1="{y}" x2="{xs[-1]}" y2="{y}" class="run"/>
    {''.join(dots)}
  </g>
</svg>
'''


if __name__ == "__main__":
    (OUT / "banner.svg").write_text(banner())
    for name, t in THEMES.items():
        (OUT / f"ml-pipeline-{name}.svg").write_text(pipeline(t))
        (OUT / f"learning-path-{name}.svg").write_text(learning_path(t))
    for f in sorted(OUT.glob("*.svg")):
        print(f.name, f.stat().st_size, "bytes")

"""Self-contained diagrams. Host image tools and three.js are optional extras."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from rms.data import tech_tree
from rms.gates import current_phase
from rms.physics import V


def scene_card_svg(state: dict[str, Any], payload: dict[str, Any]) -> str:
    language = state.get("language", "zh")
    phase = payload.get("phase") or current_phase(state)
    title = state.get("program", "Real Mars Shot")
    year = f"{state['clock']['year']}-{state['clock']['month']:02d}"
    lines = payload.get("summary_lines") or []
    body = lines[1] if len(lines) > 1 else phase
    action = payload.get("action") or "brief"
    # Geometric plate, not a fake photograph. Labels stay short so missing CJK fonts still leave the drawing.
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="960" height="540" viewBox="0 0 960 540" id="scene-card">
  <rect width="960" height="540" fill="#12151c"/>
  <circle cx="760" cy="150" r="70" fill="#c4553a"/>
  <circle cx="730" cy="120" r="18" fill="#8d3a2c"/>
  <rect x="80" y="300" width="220" height="70" rx="8" fill="#2c3340" stroke="#d7c4a3"/>
  <rect x="100" y="250" width="80" height="50" fill="#3d4c5c"/>
  <polygon points="150,250 190,210 230,250" fill="#d7c4a3"/>
  <rect x="360" y="330" width="16" height="80" fill="#888"/>
  <polygon points="352,330 384,330 368,250" fill="#eee"/>
  <text x="48" y="56" fill="#f3efe6" font-family="Georgia, serif" font-size="28">{_xml(title)}</text>
  <text x="48" y="92" fill="#d7c4a3" font-family="sans-serif" font-size="16">{_xml(year)} · {_xml(phase)} · {_xml(str(action))}</text>
  <text x="48" y="470" fill="#c9d2df" font-family="sans-serif" font-size="14">{_xml(body)[:110]}</text>
  <text x="48" y="500" fill="#8ea0b5" font-family="sans-serif" font-size="12">{_xml(language)} · real mars shot</text>
</svg>
'''


def deltav_mermaid() -> str:
    return """flowchart LR
  earth["Earth surface ~9.4 km/s to LEO (estimate, with losses)"] --> leo["LEO"]
  leo -->|"TLI ~3.15 km/s"| tli["Trans-lunar"]
  tli -->|"LOI ~0.9"| llo["Low lunar orbit"]
  llo -->|"descent ~1.9, no atmosphere"| moon["Lunar surface"]
  leo -->|"TMI ~3.6 km/s min-energy"| tmi["Trans-Mars"]
  tmi -->|"aerocapture + ~0.6 terminal (estimate)"| mars["Mars surface"]
  note["DRA 5.0 aggregate: Moon ~9.5 km/s LEO to surface and back; Mars 12-14 km/s"]
"""


def techtree_mermaid() -> str:
    lines = ["flowchart TD"]
    for tech_id, row in tech_tree().items():
        label = row["en"].replace('"', "'")
        lines.append(f'  {tech_id}["{label}"]')
        for prereq in row["prereq"]:
            lines.append(f"  {prereq} --> {tech_id}")
    return "\n".join(lines) + "\n"


def habitat_svg() -> str:
    scale = V("radiation", "shield_scale_g_cm2")
    buried = V("radiation", "buried_habitat_extra_g_cm2")
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="880" height="420" viewBox="0 0 880 420" id="habitat-section">
  <rect width="880" height="420" fill="#1b140f"/>
  <rect x="40" y="40" width="800" height="120" fill="#6b4b32"/>
  <text x="60" y="78" fill="#f3efe6" font-family="sans-serif" font-size="16">regolith overburden, extra shielding about {buried:.0f} g/cm2 (estimate)</text>
  <text x="60" y="104" fill="#e7d7c3" font-family="sans-serif" font-size="13">transmission model 1 / (1 + extra / {scale:.0f}). Not HZETRN. extra = 0 reproduces MSL/RAD.</text>
  <rect x="160" y="180" width="560" height="150" rx="70" fill="#243044" stroke="#d7c4a3" stroke-width="3"/>
  <text x="250" y="250" fill="#f3efe6" font-family="sans-serif" font-size="16">pressure vessel · 98% water loop · crops need kilowatts of light per person-area</text>
  <rect x="200" y="300" width="80" height="16" fill="#88c0d0"/>
  <text x="290" y="314" fill="#88c0d0" font-family="sans-serif" font-size="12">storm shelter, about 20 g/cm2 extra water/poly (estimate)</text>
</svg>
'''


def architecture_mermaid() -> str:
    return """flowchart TD
  subgraph earth [Earth first]
    analog["Analogs: cold, heat, vacuum, closed air"]
    labs["ECLSS 93% then 98%, Sabatier, crop lab"]
  end
  subgraph machines [Machines]
    robots["Robotic landers and relays"]
    isru["ISRU pilots"]
  end
  subgraph moon [Moon]
    ice["South-pole ice, LCROSS-class resource"]
    crewMoon["Short crew sorties after analogs"]
  end
  subgraph life [Biology]
    sim["Simulant grow-out, perchlorates included"]
    farm["Greenhouses, not open-air sprinkling"]
  end
  subgraph mars [Mars windows ~26 months]
    cargo["Cargo and dust-storm survival"]
    pilot["Oxygen pilot, far past MOXIE grams"]
    crew["Crew conjunction, then a dependent outpost"]
  end
  seed["Ember: 5 years local surplus and a real archive"]
  analog --> labs --> robots --> ice --> crewMoon --> sim --> farm --> cargo --> pilot --> crew --> seed
"""


def orbit_svg() -> str:
    # Heliocentric sketch. 1 AU = 160 px. Mars a = 1.5237 AU. Transfer ellipse a = (1+1.5237)/2.
    au = 160.0
    earth_r = 1.0 * au
    mars_a = V("bodies", "mars", "semi_major_axis_au") * au
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="880" height="640" viewBox="0 0 880 640" id="orbit-svg">
  <rect width="880" height="640" fill="#0c1020"/>
  <circle cx="440" cy="320" r="18" fill="#e6c36a"/>
  <ellipse cx="440" cy="320" rx="{earth_r:.1f}" ry="{earth_r:.1f}" fill="none" stroke="#6eb5ff" stroke-width="2"/>
  <ellipse cx="440" cy="320" rx="{mars_a:.1f}" ry="{mars_a * 0.97:.1f}" fill="none" stroke="#d36b4f" stroke-width="2"/>
  <ellipse cx="440" cy="300" rx="{(earth_r + mars_a) / 2:.1f}" ry="{(earth_r + mars_a) / 2 * 0.72:.1f}" fill="none" stroke="#f3efe6" stroke-dasharray="6 6"/>
  <circle cx="{440 + earth_r:.1f}" cy="320" r="6" fill="#6eb5ff"/>
  <circle cx="{440 + mars_a:.1f}" cy="320" r="7" fill="#d36b4f"/>
  <text x="24" y="36" fill="#f3efe6" font-family="sans-serif" font-size="16">Hohmann-class sketch, not a porkchop. Synodic period 779.94 days.</text>
  <text x="24" y="60" fill="#c9d2df" font-family="sans-serif" font-size="13">Earth orbit 1 AU. Mars semi-major axis 1.5237 AU (NSSDC). Dashed curve is the transfer ellipse.</text>
</svg>
'''


def orbit_html(title: str = "Real Mars Shot transfer") -> str:
    svg = orbit_svg()
    payload = {
        "earth_au": 1.0,
        "mars_au": V("bodies", "mars", "semi_major_axis_au"),
        "synodic_days": V("bodies", "mars", "synodic_days"),
    }
    data = json.dumps(payload)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <title>{_xml(title)}</title>
  <style>
    body {{ margin: 0; background: #0c1020; color: #f3efe6; font-family: sans-serif; }}
    #fallback-canvas {{ width: 100%; height: 70vh; display: block; }}
    #three-root {{ width: 100%; height: 70vh; display: none; }}
    p {{ margin: 12px 16px; max-width: 70ch; line-height: 1.45; }}
  </style>
</head>
<body>
  <p>Optional three.js view of a Hohmann-class Earth–Mars transfer. If the network cannot load three.js, the canvas below is the diagram. Windows are {payload['synodic_days']} days apart. This is not a trajectory design tool.</p>
  <div id="three-root"></div>
  <canvas id="fallback-canvas" width="960" height="640"></canvas>
  <script>
    const DATA = {data};
    const canvas = document.getElementById('fallback-canvas');
    const ctx = canvas.getContext('2d');
    function draw2d() {{
      const w = canvas.width, h = canvas.height;
      ctx.fillStyle = '#0c1020';
      ctx.fillRect(0, 0, w, h);
      const cx = w / 2, cy = h / 2 + 10;
      const au = 150;
      ctx.strokeStyle = '#6eb5ff';
      ctx.beginPath(); ctx.arc(cx, cy, DATA.earth_au * au, 0, Math.PI * 2); ctx.stroke();
      ctx.strokeStyle = '#d36b4f';
      ctx.beginPath(); ctx.ellipse(cx, cy, DATA.mars_au * au, DATA.mars_au * au * 0.97, 0, 0, Math.PI * 2); ctx.stroke();
      ctx.setLineDash([6, 6]); ctx.strokeStyle = '#f3efe6';
      const a = (DATA.earth_au + DATA.mars_au) / 2 * au;
      ctx.beginPath(); ctx.ellipse(cx, cy - 16, a, a * 0.72, 0, 0, Math.PI * 2); ctx.stroke();
      ctx.setLineDash([]);
      ctx.fillStyle = '#e6c36a'; ctx.beginPath(); ctx.arc(cx, cy, 10, 0, Math.PI * 2); ctx.fill();
      ctx.fillStyle = '#6eb5ff'; ctx.beginPath(); ctx.arc(cx + DATA.earth_au * au, cy, 6, 0, Math.PI * 2); ctx.fill();
      ctx.fillStyle = '#d36b4f'; ctx.beginPath(); ctx.arc(cx + DATA.mars_au * au, cy, 7, 0, Math.PI * 2); ctx.fill();
    }}
    draw2d();
  </script>
  <script type="module">
    try {{
      const THREE = await import('https://unpkg.com/three@0.160.0/build/three.module.js');
      const root = document.getElementById('three-root');
      root.style.display = 'block';
      const renderer = new THREE.WebGLRenderer({{ antialias: true }});
      renderer.setSize(root.clientWidth || 960, 480);
      root.appendChild(renderer.domElement);
      const scene = new THREE.Scene();
      const camera = new THREE.PerspectiveCamera(45, 960/480, 0.1, 100);
      camera.position.set(0, 6, 8);
      camera.lookAt(0, 0, 0);
      scene.add(new THREE.AmbientLight(0xffffff, 0.8));
      const sun = new THREE.Mesh(new THREE.SphereGeometry(0.25, 24, 24), new THREE.MeshBasicMaterial({{ color: 0xe6c36a }}));
      scene.add(sun);
      function ring(radius, color) {{
        const geo = new THREE.BufferGeometry();
        const pts = [];
        for (let i = 0; i <= 128; i++) {{
          const t = i / 128 * Math.PI * 2;
          pts.push(new THREE.Vector3(Math.cos(t) * radius, 0, Math.sin(t) * radius));
        }}
        geo.setFromPoints(pts);
        scene.add(new THREE.Line(geo, new THREE.LineBasicMaterial({{ color }})));
      }}
      ring(DATA.earth_au * 2.2, 0x6eb5ff);
      ring(DATA.mars_au * 2.2, 0xd36b4f);
      const earth = new THREE.Mesh(new THREE.SphereGeometry(0.12, 16, 16), new THREE.MeshBasicMaterial({{ color: 0x6eb5ff }}));
      earth.position.set(DATA.earth_au * 2.2, 0, 0);
      const mars = new THREE.Mesh(new THREE.SphereGeometry(0.1, 16, 16), new THREE.MeshBasicMaterial({{ color: 0xd36b4f }}));
      mars.position.set(DATA.mars_au * 2.2, 0, 0);
      scene.add(earth); scene.add(mars);
      renderer.render(scene, camera);
      document.getElementById('fallback-canvas').style.display = 'none';
    }} catch (err) {{
      console.warn('three.js unavailable', err);
    }}
  </script>
  <template id="static-svg">{svg}</template>
</body>
</html>
"""


def _xml(text: str) -> str:
    return (
        str(text)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def write(path: Path, text: str) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return str(path)

#!/usr/bin/env python3
"""Render geometry-derived PNG views and an offline orbit viewer for a mesh.

Requires numpy, trimesh, matplotlib and Pillow. Preview sampling and normalization
only affect the displayed copy; this program never rewrites the source mesh.
"""

from __future__ import annotations

import argparse
import html
import json
import math
import os
from pathlib import Path
import tempfile

import numpy as np
import trimesh


CLAY = np.array([0.72, 0.65, 0.55])
DEFAULT_COLOR = np.array([174, 184, 194, 255], dtype=float)


def _face_colors(mesh, selected):
    """Approximate each triangle's appearance by averaging its vertex samples."""
    visual = mesh.visual
    kind = getattr(visual, "kind", None)
    try:
        if kind == "texture":
            colors = np.asarray(visual.to_color().vertex_colors, dtype=float)
            rgba = colors[np.asarray(mesh.faces)[selected]].mean(axis=1)
            description = "texture sampled at vertices, averaged per triangle"
        elif kind == "vertex":
            colors = np.asarray(visual.vertex_colors, dtype=float)
            rgba = colors[np.asarray(mesh.faces)[selected]].mean(axis=1)
            description = "vertex colors averaged per triangle"
        elif kind == "face":
            rgba = np.asarray(visual.face_colors, dtype=float)[selected]
            description = "face colors"
        else:
            rgba = np.tile(DEFAULT_COLOR, (len(selected), 1))
            description = "neutral color (source has no appearance)"
    except (AttributeError, IndexError, TypeError, ValueError):
        rgba = np.tile(DEFAULT_COLOR, (len(selected), 1))
        description = "neutral color (source appearance could not be sampled)"
    if rgba.ndim != 2 or rgba.shape[1] not in (3, 4) or not np.isfinite(rgba).all():
        raise ValueError("mesh contains invalid appearance values")
    rgb = np.clip(rgba[:, :3] / 255.0, 0.0, 1.0)
    if rgba.shape[1] == 4:
        alpha = np.clip(rgba[:, 3:4] / 255.0, 0.0, 1.0)
        rgb = rgb * alpha + (1.0 - alpha) * 0.96
    return rgb, description


def prepare_scene(scene, max_triangles=20000):
    """Validate all source geometry, retain scene transforms, sample for display."""
    if not isinstance(max_triangles, int) or max_triangles <= 0:
        raise ValueError("max_triangles must be a positive integer")
    if isinstance(scene, trimesh.Trimesh):
        scene = trimesh.Scene(scene)
    instances = []
    bounds = []
    total = 0
    for node in scene.graph.nodes_geometry:
        transform, geometry_name = scene.graph[node]
        mesh = scene.geometry[geometry_name]
        if not isinstance(mesh, trimesh.Trimesh):
            continue
        vertices = np.asarray(mesh.vertices)
        faces = np.asarray(mesh.faces)
        if vertices.ndim != 2 or vertices.shape[1] != 3 or not np.isfinite(vertices).all():
            raise ValueError("mesh contains NaN, infinite or invalid vertex coordinates")
        if faces.ndim != 2 or faces.shape[1] != 3:
            raise ValueError("mesh must contain triangular faces")
        if len(faces) == 0:
            continue
        if faces.min() < 0 or faces.max() >= len(vertices):
            raise ValueError("mesh contains an invalid face index")
        if not np.isfinite(transform).all():
            raise ValueError("scene contains an invalid transform")
        world = trimesh.transform_points(vertices, transform)
        if not np.isfinite(world).all():
            raise ValueError("transformed mesh contains non-finite coordinates")
        bounds.extend((world.min(axis=0), world.max(axis=0)))
        instances.append((mesh, world, total))
        total += len(faces)
    if not instances:
        raise ValueError("input contains no triangle mesh")
    bounds = np.asarray(bounds)
    lower, upper = bounds.min(axis=0), bounds.max(axis=0)
    center = lower / 2.0 + upper / 2.0
    radius = float(np.linalg.norm((upper - lower) / 2.0))
    if not math.isfinite(radius) or radius <= 0:
        raise ValueError("mesh has no finite spatial extent")
    count = min(total, max_triangles)
    chosen = np.linspace(0, total - 1, count, dtype=np.int64)
    triangles, colors, appearances = [], [], set()
    for mesh, world, offset in instances:
        selected = chosen[(chosen >= offset) & (chosen < offset + len(mesh.faces))] - offset
        if not len(selected):
            continue
        triangles.append((world[np.asarray(mesh.faces)[selected]] - center) / radius)
        color, appearance = _face_colors(mesh, selected)
        colors.append(color)
        appearances.add(appearance)
    triangles = np.concatenate(triangles)
    if not np.isfinite(triangles).all():
        raise ValueError("normalized mesh contains non-finite coordinates")
    return {
        "triangles": triangles,
        "colors": np.concatenate(colors),
        "source_triangles": total,
        "preview_triangles": count,
        "sampled": count < total,
        "appearance": sorted(appearances),
        "bounds": [lower.tolist(), upper.tolist()],
    }


def view_specs(up_axis="z"):
    up_index = "xyz".index(up_axis)
    horizontal = [axis for axis in range(3) if axis != up_index]
    result = []
    for axis, sign in ((horizontal[1], 1), (horizontal[0], 1), (horizontal[0], -1), (horizontal[1], -1)):
        eye = np.zeros(3)
        eye[axis] = sign
        result.append((f"From {'+' if sign > 0 else '-'}{'XYZ'[axis]}", eye))
    result.append(("From +X +Y +Z (3/4)", np.ones(3)))
    return result


def camera_basis(eye, up_axis="z"):
    eye = np.asarray(eye, dtype=float)
    eye = eye / np.linalg.norm(eye)
    up = np.eye(3)["xyz".index(up_axis)]
    right = np.cross(up, eye)
    right /= np.linalg.norm(right)
    up = np.cross(eye, right)
    return right, up, eye


def _normals(triangles):
    normal = np.cross(triangles[:, 1] - triangles[:, 0], triangles[:, 2] - triangles[:, 0])
    lengths = np.linalg.norm(normal, axis=1)
    return normal / np.maximum(lengths[:, None], 1e-15)


def render_contact_sheet(preview, output, up_axis="z"):
    # Keep font/config writes in a writable temporary directory on locked-down Macs.
    with tempfile.TemporaryDirectory(prefix="u1-preview-mpl-") as cache:
        previous = os.environ.get("MPLCONFIGDIR")
        os.environ["MPLCONFIGDIR"] = cache
        try:
            import matplotlib
            matplotlib.use("Agg", force=True)
            from matplotlib import pyplot as plt
            from matplotlib.collections import PolyCollection

            triangles = preview["triangles"]
            normals = _normals(triangles)
            fig, axes = plt.subplots(2, 5, figsize=(16, 7), facecolor="#f5f5f3")
            for column, (label, eye) in enumerate(view_specs(up_axis)):
                right, up, eye = camera_basis(eye, up_axis)
                projected = np.stack((triangles @ right, triangles @ up), axis=-1)
                order = np.argsort((triangles @ eye).mean(axis=1), kind="stable")
                light = eye + up * 0.7 - right * 0.4
                light /= np.linalg.norm(light)
                shade = 0.32 + 0.68 * np.abs(normals @ light)
                for row in range(2):
                    ax = axes[row, column]
                    base = preview["colors"] if row == 0 else np.tile(CLAY, (len(triangles), 1))
                    facecolors = np.clip(base * shade[:, None], 0, 1)
                    collection = PolyCollection(
                        projected[order], facecolors=facecolors[order], edgecolors="none",
                        antialiased=False, closed=True,
                    )
                    ax.add_collection(collection)
                    ax.set(xlim=(-1.04, 1.04), ylim=(-1.04, 1.04), aspect="equal")
                    ax.set_axis_off()
                    ax.set_title(label, fontsize=10, pad=8)
            axes[0, 0].text(-0.03, 0.5, "Approx. appearance", rotation=90, va="center", ha="right", transform=axes[0, 0].transAxes)
            axes[1, 0].text(-0.03, 0.5, "Clay geometry", rotation=90, va="center", ha="right", transform=axes[1, 0].transAxes)
            note = sampling_note(preview)
            fig.suptitle(f"Actual mesh views · {up_axis.upper()} up · orthographic", fontsize=16, y=0.98)
            fig.text(0.5, 0.035, note, ha="center", fontsize=9)
            fig.text(0.5, 0.012, "Colors are per-triangle approximations; clay shows geometry. Camera labels do not assume the subject's front.", ha="center", fontsize=8)
            fig.subplots_adjust(left=0.045, right=0.99, top=0.9, bottom=0.09, wspace=0.06, hspace=0.2)
            fig.savefig(output, dpi=130, facecolor=fig.get_facecolor())
            plt.close(fig)
        finally:
            if previous is None:
                os.environ.pop("MPLCONFIGDIR", None)
            else:
                os.environ["MPLCONFIGDIR"] = previous


def sampling_note(preview):
    if preview["sampled"]:
        return (f"Preview samples {preview['preview_triangles']:,} of {preview['source_triangles']:,} triangles; "
                "sampling can show holes or miss details. Source file unchanged.")
    return f"All {preview['source_triangles']:,} source triangles displayed. Source file unchanged."


VIEWER = r'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>__TITLE__ — mesh preview</title>
<style>
:root{color-scheme:light;font:15px system-ui,sans-serif;color:#253136;background:#f5f5f3}body{max-width:1100px;margin:24px auto;padding:0 18px}h1{font-size:22px;margin-bottom:8px}p{line-height:1.5;margin:8px 0}button{font:inherit;border:1px solid #9ba4a6;border-radius:6px;background:white;padding:7px 12px;cursor:pointer}button[aria-pressed=true]{background:#263f49;color:white}nav{display:flex;flex-wrap:wrap;gap:8px;margin:14px 0}canvas{display:block;width:100%;height:min(66vh,680px);min-height:280px;background:#eeeeeb;border:1px solid #d8dcda;border-radius:8px;touch-action:none;cursor:grab}canvas:active{cursor:grabbing}small{color:#526166}#mode{font-weight:600}
</style></head><body>
<h1>__TITLE__</h1>
<p>Actual mesh geometry · <strong>__UP__ up</strong> · offline viewer</p>
<p>__NOTE__</p><p><small>__APPEARANCE__</small></p>
<nav aria-label="Display mode"><button id="color" aria-pressed="true">Approx. appearance</button><button id="clay" aria-pressed="false">Clay geometry</button><button id="reset">Reset view</button></nav>
<nav id="views" aria-label="Camera direction"></nav>
<canvas id="viewer" tabindex="0" aria-label="Interactive mesh preview. Drag or use arrow keys to rotate. Scroll or use plus and minus to zoom."></canvas>
<p id="mode">Approximate source appearance</p>
<p>Drag to orbit · scroll to zoom · arrow keys rotate · + / − zoom. Camera labels give the viewing position relative to the source axes; the subject's front is not inferred.</p>
<small>Orthographic, depth-sorted triangle preview. Texture is sampled at vertices and averaged per triangle; transparency is composited. This is a visual inspection aid, not a printability check.</small>
<script id="mesh-data" type="application/json">__DATA__</script>
<script>
'use strict';
const data=JSON.parse(document.getElementById('mesh-data').textContent);
const canvas=document.getElementById('viewer'), ctx=canvas.getContext('2d');
const U=data.upAxis, H=[0,1,2].filter(i=>i!==U), t=data.triangles, colors=data.colors;
const dot=(a,b)=>a[0]*b[0]+a[1]*b[1]+a[2]*b[2];
const cross=(a,b)=>[a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]];
const norm=a=>{const n=Math.hypot(...a)||1;return a.map(v=>v/n)};
const normals=t.map(f=>norm(cross(f[1].map((v,i)=>v-f[0][i]),f[2].map((v,i)=>v-f[0][i]))));
let az=Math.PI/3, el=0.4, zoom=1, clay=false, drag=null, pending=false;
function schedule(){if(!pending){pending=true;requestAnimationFrame(()=>{pending=false;draw()})}}
function draw(){
 const dpr=Math.min(window.devicePixelRatio||1,2), w=canvas.clientWidth,h=canvas.clientHeight;
 if(canvas.width!==Math.round(w*dpr)||canvas.height!==Math.round(h*dpr)){canvas.width=Math.round(w*dpr);canvas.height=Math.round(h*dpr)}
 ctx.setTransform(dpr,0,0,dpr,0,0);ctx.clearRect(0,0,w,h);
 const eye=[0,0,0], up0=[0,0,0];up0[U]=1;
 eye[H[0]]=Math.cos(el)*Math.cos(az);eye[H[1]]=Math.cos(el)*Math.sin(az);eye[U]=Math.sin(el);
 const right=norm(cross(up0,eye)),up=cross(eye,right),light=norm(eye.map((v,i)=>v+0.7*up[i]-0.4*right[i]));
 const scale=Math.min(w,h)*0.44*zoom;
 const faces=t.map((f,i)=>({i,z:(dot(f[0],eye)+dot(f[1],eye)+dot(f[2],eye))/3})).sort((a,b)=>a.z-b.z);
 for(const {i} of faces){
  const f=t[i], shade=0.32+0.68*Math.abs(dot(normals[i],light)), c=clay?[0.72,0.65,0.55]:colors[i];
  ctx.fillStyle=`rgb(${c.map(v=>Math.round(Math.min(1,Math.max(0,v*shade))*255)).join(',')})`;
  ctx.beginPath();f.forEach((p,j)=>{const x=w/2+dot(p,right)*scale,y=h/2-dot(p,up)*scale;j?ctx.lineTo(x,y):ctx.moveTo(x,y)});ctx.closePath();ctx.fill();
 }
}
function setMode(value){clay=value;document.getElementById('color').setAttribute('aria-pressed',String(!clay));document.getElementById('clay').setAttribute('aria-pressed',String(clay));document.getElementById('mode').textContent=clay?'Clay geometry':'Approximate source appearance';schedule()}
document.getElementById('color').onclick=()=>setMode(false);document.getElementById('clay').onclick=()=>setMode(true);
document.getElementById('reset').onclick=()=>{az=Math.PI/3;el=0.4;zoom=1;schedule()};
for(const view of data.views){const button=document.createElement('button');button.textContent=view.label;button.onclick=()=>{const e=norm(view.eye);az=Math.atan2(e[H[1]],e[H[0]]);el=Math.asin(e[U]);schedule()};document.getElementById('views').append(button)}
canvas.addEventListener('pointerdown',e=>{drag=[e.clientX,e.clientY];canvas.setPointerCapture(e.pointerId);canvas.focus()});
canvas.addEventListener('pointermove',e=>{if(!drag)return;az-=(e.clientX-drag[0])*0.009;el=Math.max(-1.5,Math.min(1.5,el+(e.clientY-drag[1])*0.009));drag=[e.clientX,e.clientY];schedule()});
canvas.addEventListener('pointerup',()=>{drag=null});canvas.addEventListener('pointercancel',()=>{drag=null});
canvas.addEventListener('wheel',e=>{e.preventDefault();zoom=Math.max(0.25,Math.min(6,zoom*Math.exp(-e.deltaY*0.001)));schedule()},{passive:false});
canvas.addEventListener('keydown',e=>{let handled=true;if(e.key==='ArrowLeft')az-=0.12;else if(e.key==='ArrowRight')az+=0.12;else if(e.key==='ArrowUp')el=Math.min(1.5,el+0.12);else if(e.key==='ArrowDown')el=Math.max(-1.5,el-0.12);else if(e.key==='+'||e.key==='=')zoom=Math.min(6,zoom*1.1);else if(e.key==='-')zoom=Math.max(0.25,zoom/1.1);else handled=false;if(handled){e.preventDefault();schedule()}});
window.addEventListener('resize',schedule);schedule();
</script></body></html>'''


def write_viewer(preview, output, source_name, up_axis="z"):
    data = {
        "triangles": np.round(preview["triangles"], 7).tolist(),
        "colors": np.round(preview["colors"], 5).tolist(),
        "upAxis": "xyz".index(up_axis),
        "sourceTriangles": preview["source_triangles"],
        "previewTriangles": preview["preview_triangles"],
        "sampled": preview["sampled"],
        "views": [{"label": label, "eye": eye.tolist()} for label, eye in view_specs(up_axis)],
    }
    payload = json.dumps(data, separators=(",", ":"), allow_nan=False).replace("<", "\\u003c")
    values = {
        "TITLE": html.escape(source_name), "UP": up_axis.upper(),
        "NOTE": html.escape(sampling_note(preview)),
        "APPEARANCE": html.escape("Appearance: " + "; ".join(preview["appearance"])),
        "DATA": payload,
    }
    document = VIEWER
    # DATA is inserted last so geometry payload cannot be interpreted as a template.
    for key, value in values.items():
        document = document.replace(f"__{key}__", value)
    Path(output).write_text(document, encoding="utf-8")


def generate_preview(source, output_dir, max_triangles=20000, up_axis="z"):
    source, output_dir = Path(source), Path(output_dir)
    if source.suffix.lower() not in {".glb", ".obj", ".stl"}:
        raise ValueError("input must be GLB, OBJ or STL")
    if up_axis not in {"x", "y", "z"}:
        raise ValueError("up_axis must be x, y or z")
    scene = trimesh.load(source, force="scene", process=False)
    preview = prepare_scene(scene, max_triangles)
    output_dir.mkdir(parents=True, exist_ok=True)
    png, viewer = output_dir / "views.png", output_dir / "viewer.html"
    if source.resolve() in {png.resolve(), viewer.resolve()}:
        raise ValueError("preview output must not overwrite the source")
    render_contact_sheet(preview, png, up_axis)
    write_viewer(preview, viewer, source.name, up_axis)
    return {key: value for key, value in preview.items() if key not in {"triangles", "colors"}} | {
        "views": str(png.resolve()), "viewer": str(viewer.resolve()), "up_axis": up_axis,
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--up-axis", choices=("x", "y", "z"), default="z", help="explicit source up axis; default z; never inferred")
    parser.add_argument("--max-triangles", type=int, default=20000, help="display-only triangle sampling limit (default 20000); source is never modified")
    args = parser.parse_args(argv)
    if args.max_triangles <= 0:
        parser.error("--max-triangles must be positive")
    try:
        report = generate_preview(args.input, args.output_dir, args.max_triangles, args.up_axis)
    except (OSError, ValueError, ImportError) as exc:
        parser.exit(2, f"ERROR: {exc}\n")
    print(json.dumps(report, indent=2, allow_nan=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

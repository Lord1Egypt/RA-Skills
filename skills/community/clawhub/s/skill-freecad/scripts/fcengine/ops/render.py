"""Headless PNG rendering for visual checks.

A small orthographic rasteriser: tessellate, z-buffer, Lambert shading, then
model edges drawn on top. It uses only numpy (bundled with FreeCAD) and
zlib, so it needs no GUI, OpenGL or extra packages.
"""

from __future__ import annotations

import struct
import zlib
from typing import Any, Dict, List, Tuple

from .. import errors, geometry, workspace
from ..document import Context, role, visible_objects
from ..errors import SkillError

# view -> (direction from the model towards the camera, screen-up vector)
VIEWS = {
    "iso": ((1, -1, 1), (0, 0, 1)),
    "front": ((0, -1, 0), (0, 0, 1)),
    "back": ((0, 1, 0), (0, 0, 1)),
    "right": ((1, 0, 0), (0, 0, 1)),
    "left": ((-1, 0, 0), (0, 0, 1)),
    "top": ((0, 0, 1), (0, 1, 0)),
    "bottom": ((0, 0, -1), (0, -1, 0)),
}
BG = (255, 255, 255)
BASE = (0.62, 0.70, 0.82)
EDGE = (40, 40, 40)
AXIS_COLORS = ((220, 40, 40), (30, 160, 60), (40, 80, 230))  # X red, Y green, Z blue


def _basis(np: Any, view: str) -> Any:
    to_cam, up = (np.array(v, float) for v in VIEWS[view])
    to_cam /= np.linalg.norm(to_cam)
    right = np.cross(up, to_cam)
    if np.linalg.norm(right) < 1e-9:
        right = np.array([1.0, 0, 0])
    right /= np.linalg.norm(right)
    true_up = np.cross(to_cam, right)
    return np.vstack([right, true_up, to_cam])  # rows: screen x, screen y, depth (towards camera)


def _raster(
    np: Any,
    pts: Any,
    tris: Any,
    normals: Any,
    edges: List[Any],
    R: Any,
    scale: float,
    size: int,
    light: Any,
    deflection: float,
    base_rgb: Any = None,
    vertex_rgb: Any = None,
    vertex_normals: Any = None,
    material_colors: bool = False,
) -> Any:
    img = np.empty((size, size, 3), np.uint8)
    img[:] = BG
    zbuf = np.full((size, size), -np.inf)
    P = pts @ R.T
    center = (P[:, :2].min(0) + P[:, :2].max(0)) / 2
    sx = (P[:, 0] - center[0]) * scale + size / 2
    sy = size / 2 - (P[:, 1] - center[1]) * scale
    sz = P[:, 2]
    shade = 0.30 + 0.70 * np.abs(normals @ light)
    vshade = None if vertex_normals is None else 0.30 + 0.70 * np.abs(vertex_normals @ light)  # smooth (Gouraud)
    if base_rgb is None:
        colors = (np.outer(shade, BASE) * 255).clip(0, 255).astype(np.uint8)
    else:  # per-triangle colours (e.g. a stress map), still shaded
        colors = (shade[:, None] * (0.35 + 0.65 * base_rgb) * 255).clip(0, 255).astype(np.uint8)
    for t in range(len(tris)):
        i, j, k = tris[t]
        x0, x1, x2 = sx[i], sx[j], sx[k]
        y0, y1, y2 = sy[i], sy[j], sy[k]
        area = (x1 - x0) * (y2 - y0) - (x2 - x0) * (y1 - y0)
        if abs(area) < 1e-12:
            continue
        xmin, xmax = max(int(min(x0, x1, x2)), 0), min(int(max(x0, x1, x2)) + 1, size - 1)
        ymin, ymax = max(int(min(y0, y1, y2)), 0), min(int(max(y0, y1, y2)) + 1, size - 1)
        if xmin > xmax or ymin > ymax:
            continue
        gx, gy = np.meshgrid(np.arange(xmin, xmax + 1) + 0.5, np.arange(ymin, ymax + 1) + 0.5)
        w0 = ((x1 - gx) * (y2 - gy) - (x2 - gx) * (y1 - gy)) / area
        w1 = ((x2 - gx) * (y0 - gy) - (x0 - gx) * (y2 - gy)) / area
        w2 = 1 - w0 - w1
        inside = (w0 >= -1e-6) & (w1 >= -1e-6) & (w2 >= -1e-6)
        if not inside.any():
            continue
        z = w0 * sz[i] + w1 * sz[j] + w2 * sz[k]
        sub = zbuf[ymin : ymax + 1, xmin : xmax + 1]
        upd = inside & (z > sub)
        sub[upd] = z[upd]
        if vertex_rgb is None and (vshade is None or base_rgb is not None):
            img[ymin : ymax + 1, xmin : xmax + 1][upd] = colors[t]
        elif vertex_rgb is None:  # smooth shading of the base colour
            sh = w0 * vshade[i] + w1 * vshade[j] + w2 * vshade[k]
            col = (sh[..., None] * BASE * 255).clip(0, 255).astype(np.uint8)
            img[ymin : ymax + 1, xmin : xmax + 1][upd] = col[upd]
        else:  # Gouraud: interpolate vertex colours (a stress field, or part materials)
            col = w0[..., None] * vertex_rgb[i] + w1[..., None] * vertex_rgb[j] + w2[..., None] * vertex_rgb[k]
            sh = shade[t] if vshade is None else (w0 * vshade[i] + w1 * vshade[j] + w2 * vshade[k])[..., None]
            # Material colours keep their hue, lifted slightly so black rubber still shows its shape.
            col = (
                (sh * ((0.12 + 0.88 * col) if material_colors else (0.35 + 0.65 * col)) * 255)
                .clip(0, 255)
                .astype(np.uint8)
            )
            img[ymin : ymax + 1, xmin : xmax + 1][upd] = col[upd]
    # Edges, depth-tested with a small bias so visible edges win over their faces.
    depth_span = float(sz.max() - sz.min()) if len(sz) else 1.0
    # The tessellation can lie up to `deflection` in front of the true surface,
    # which hides edges on curved/tangent faces (dashed lines) unless the bias covers it.
    bias = max(0.004 * max(depth_span, 1e-6), 3 * deflection) + 1e-6
    for poly in edges:
        Q = poly @ R.T
        ex = (Q[:, 0] - center[0]) * scale + size / 2
        ey = size / 2 - (Q[:, 1] - center[1]) * scale
        ez = Q[:, 2]
        for a in range(len(Q) - 1):
            n = int(max(abs(ex[a + 1] - ex[a]), abs(ey[a + 1] - ey[a]))) + 2
            ts = np.linspace(0, 1, n)
            xs = (ex[a] + (ex[a + 1] - ex[a]) * ts).astype(int)
            ys = (ey[a] + (ey[a + 1] - ey[a]) * ts).astype(int)
            zs = ez[a] + (ez[a + 1] - ez[a]) * ts
            ok = (xs >= 0) & (xs < size) & (ys >= 0) & (ys < size)
            xs, ys, zs = xs[ok], ys[ok], zs[ok]
            vis = zs >= zbuf[ys, xs] - bias
            img[ys[vis], xs[vis]] = EDGE
    _axis_triad(np, img, R, size)
    return img


def _axis_triad(np: Any, img: Any, R: Any, size: int) -> None:
    origin = np.array([28.0, size - 28.0])
    for axis in range(3):
        d = R[:2, axis]  # projection of the world axis onto the screen
        end = origin + np.array([d[0], -d[1]]) * 22
        n = 30
        for t in np.linspace(0, 1, n):
            x, y = (origin + (end - origin) * t).astype(int)
            img[max(y - 1, 0) : y + 1, max(x - 1, 0) : x + 1] = AXIS_COLORS[axis]


def _png(path: str, img: Any) -> None:
    h, w, _ = img.shape
    raw = b"".join(b"\x00" + img[y].tobytes() for y in range(h))

    def chunk(tag: bytes, data: bytes) -> bytes:
        return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)

    with open(path, "wb") as fh:
        fh.write(
            b"\x89PNG\r\n\x1a\n"
            + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0))
            + chunk(b"IDAT", zlib.compress(raw, 6))
            + chunk(b"IEND", b"")
        )


def _vertex_normals(np: Any, pts: Any, tris: Any, nrm: Any) -> Any:
    """Area-weighted average of the triangle normals at each vertex (vertices are per face, so sharp edges
    between faces stay sharp). Triangles of one face share an orientation, so the sum does not cancel."""
    a, b, c = pts[tris[:, 0]], pts[tris[:, 1]], pts[tris[:, 2]]
    weighted = np.cross(b - a, c - a)
    vn = np.zeros_like(pts)
    for col in range(3):
        np.add.at(vn, tris[:, col], weighted)
    lengths = np.linalg.norm(vn, axis=1, keepdims=True)
    vn /= np.maximum(lengths, 1e-12)
    return vn


def _fix_pole_normals(np: Any, face: Any, pts: Any, vn: Any) -> None:
    """Vertices touched only by zero-area triangles (e.g. sphere poles) get the exact surface normal."""
    import FreeCAD as App

    for i in np.nonzero(np.linalg.norm(vn, axis=1) < 0.5)[0]:
        try:
            u, v = face.Surface.parameter(App.Vector(*pts[i]))
            n = face.Surface.normal(u, v)
            vn[i] = [n.x, n.y, n.z]
        except Exception:
            pass


def _colored_shapes(objs: List[Any]) -> List[Tuple[Any, Any]]:
    """(shape, colour or None) per part; assemblies are split into their placed parts."""
    from .assembly import parts_of, placed_shape
    from .material import render_color

    out = []
    for o in objs:
        if o.TypeId == "Assembly::AssemblyObject":
            for link in parts_of(o):
                src = getattr(link, "LinkedObject", None)
                out.append((placed_shape(link), render_color(src) if src is not None else None))
        else:
            out.append((o.Shape, render_color(o)))
    return out


def _mesh(np: Any, objs: List[Any]) -> Tuple[Any, Any, Any, List[Any], float, Any, Any]:
    import Part

    parts = _colored_shapes(objs)
    compound = Part.makeCompound([shape for shape, _ in parts])
    diag = compound.BoundBox.DiagonalLength or 1.0
    deflection = diag / 400.0
    all_pts, all_tris, all_vn, all_rgb = [], [], [], []
    offset = 0
    for shape, color in parts:
        shape.tessellate(deflection)  # meshes every face once; per-face calls reuse it, so faces join without gaps
        rgb = np.array(color if color is not None else BASE, float)
        for face in shape.Faces:
            verts, faces = face.tessellate(deflection)
            if not faces:
                continue
            fp = np.array([[v.x, v.y, v.z] for v in verts], float)
            ft = np.array(faces, int).reshape(-1, 3)
            fvn = _vertex_normals(np, fp, ft, None)
            _fix_pole_normals(np, face, fp, fvn)
            all_pts.append(fp)
            all_tris.append(ft + offset)
            all_vn.append(fvn)
            all_rgb.append(np.tile(rgb, (len(fp), 1)))
            offset += len(fp)
    pts = np.vstack(all_pts) if all_pts else np.zeros((0, 3))
    tris = np.vstack(all_tris) if all_tris else np.zeros((0, 3), int)
    vnrm = np.vstack(all_vn) if all_vn else np.zeros((0, 3))
    vrgb = np.vstack(all_rgb) if all_rgb else np.zeros((0, 3))
    a, b, c = pts[tris[:, 0]], pts[tris[:, 1]], pts[tris[:, 2]]
    nrm = np.cross(b - a, c - a)
    nrm /= np.maximum(np.linalg.norm(nrm, axis=1, keepdims=True), 1e-12)
    seams = [e for f in compound.Faces for e in f.Edges if e.isSeam(f)]
    edges = []
    for e in compound.Edges:
        if any(e.isSame(s) for s in seams):
            continue  # seam lines of cylinders/tori are not real edges
        if e.Length < 1e-9:
            continue  # degenerate edges (sphere and cone poles) would show as dots
        try:
            ps = e.discretize(Deflection=diag / 500.0)
        except Exception:
            continue
        if len(ps) >= 2:
            edges.append(np.array([[p.x, p.y, p.z] for p in ps], float))
    return pts, tris, nrm, edges, deflection, vnrm, vrgb


def render(ctx: Context, p: Dict[str, Any]) -> Dict[str, Any]:
    try:
        import numpy as np
    except ImportError:
        raise SkillError(errors.UNSUPPORTED, "Rendering needs numpy, which this FreeCAD installation lacks") from None
    dest = workspace.resolve(ctx.root, p["filename"])
    if dest.suffix.lower() != ".png":
        raise SkillError(errors.INVALID_PARAM, "render writes PNG files: use a .png filename")
    if any(pe["dest"] == dest for pe in ctx.pending_exports):
        raise SkillError(errors.INVALID_PARAM, f"'{p['filename']}' is already written earlier in this request")
    if p.get("targets"):
        objs = [ctx.get(t) for t in p["targets"]]
        for o in objs:
            if o.Shape.isNull() or not o.Shape.Faces:
                raise SkillError(
                    errors.INVALID_PARAM,
                    f"'{o.Name}' has no faces to render (it is a {o.TypeId} wire/profile)",
                    hint="Render the solid built from it (e.g. the extrusion), or omit 'targets' to render all results.",
                )
    else:
        objs = [o for o in visible_objects(ctx.doc) if role(o) == "result" and not o.Shape.isNull() and o.Shape.Faces]
    if not objs:
        raise SkillError(errors.EMPTY_RESULT, "Nothing to render", hint="Create geometry first or name 'targets'.")
    views = p["views"]
    size = p["size"]
    pts, tris, nrm, edges, deflection, vnrm, vrgb = _mesh(np, objs)
    bases = [_basis(np, v) for v in views]
    # One scale for all views, so sizes are comparable between them.
    extent = max(float(np.ptp(pts @ R[:2].T, axis=0).max()) for R in bases) or 1.0
    scale = 0.86 * size / extent
    tiles = []
    for R in bases:
        light = R[2] * 0.8 + R[1] * 0.45 + R[0] * -0.3
        light /= np.linalg.norm(light)
        tiles.append(
            _raster(
                np,
                pts,
                tris,
                nrm,
                edges,
                R,
                scale,
                size,
                light,
                deflection,
                vertex_normals=vnrm,
                vertex_rgb=vrgb,
                material_colors=True,
            )
        )
    cols = 1 if len(tiles) == 1 else 2
    rows = (len(tiles) + cols - 1) // cols
    sheet = np.empty((rows * size + (rows - 1) * 2, cols * size + (cols - 1) * 2, 3), np.uint8)
    sheet[:] = (180, 180, 180)  # separator lines
    blank = np.full((size, size, 3), 255, np.uint8)
    for idx in range(rows * cols):
        r, c = divmod(idx, cols)
        sheet[r * (size + 2) : r * (size + 2) + size, c * (size + 2) : c * (size + 2) + size] = (
            tiles[idx] if idx < len(tiles) else blank
        )
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_name(f".{dest.stem}.fcskill-tmp.png")
    _png(str(tmp), sheet)
    record = {
        "file": workspace.relative(ctx.root, dest),
        "views": views,
        "layout": f"{rows} row(s) x {cols} column(s), views in reading order",
        "mm_per_pixel": geometry.num(1.0 / scale, 4),
        "objects": [o.Name for o in objs],
        "triangles": int(len(tris)),
        "legend": "axis triad bottom-left of each view: X red, Y green, Z blue; edges dark grey",
    }
    ctx.pending_exports.append({"tmp": tmp, "dest": dest, "record": dict(record, format="png")})
    return {"data": record}


HANDLERS = {"render": render}

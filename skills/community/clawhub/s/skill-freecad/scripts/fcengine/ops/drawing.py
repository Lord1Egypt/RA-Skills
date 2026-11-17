"""2D technical drawings (TechDraw) exported to DXF, headless.

Findings from probing FreeCAD 1.1 headless:
- A page computes nothing without a template.
- Views compute on a background thread, so the Qt event loop must be pumped.
- writeDXFPage works headless (lines, circles, DIMENSION entities, texts);
  SVG/PDF page export needs the GUI, so the .FCStd keeps the page for that.
"""

from __future__ import annotations

import datetime
import glob
import os
import time
from typing import Any, Dict, List, Tuple

import FreeCAD as App

from .. import errors, geometry, workspace
from ..document import Context, role, visible_objects
from ..errors import SkillError

SHEETS = {"A4": (297.0, 210.0), "A3": (420.0, 297.0)}
STANDARD_SCALES = (10, 5, 2, 1, 0.5, 0.2, 0.1, 0.05, 0.02, 0.01)
GAP = 18.0  # mm on paper between views, room for dimensions
# Drawing area (mm on paper), leaving the margin and the title block band free.
MARGIN, TITLE_BAND = 20.0, 60.0
VIEW_DIRS = {"front": (0, -1, 0), "top": (0, 0, 1), "right": (1, 0, 0), "left": (-1, 0, 0), "iso": (1, -1, 1)}
# Horizontal drawing axis of each view, so that height (Z) is vertical in front/side views.
VIEW_XDIRS = {"front": (1, 0, 0), "top": (1, 0, 0), "right": (0, 1, 0), "left": (0, -1, 0)}


def _template(sheet: str) -> str:
    root = os.path.join(App.getResourceDir(), "Mod", "TechDraw", "Templates")
    for pattern in (
        f"ISO/{sheet}_Landscape_ISO5457_minimal.svg",
        f"**/{sheet}_Landscape*.svg",
        "Default_Template_A4_Landscape.svg",
    ):
        found = sorted(glob.glob(os.path.join(root, pattern), recursive=True))
        if found:
            return found[0]
    raise SkillError(errors.UNSUPPORTED, f"No TechDraw template found for {sheet}")


def _pump(objs: List[Any], doc: Any, timeout: float = 30.0) -> None:
    """TechDraw computes views on a background thread: run the Qt event loop until they are done."""
    from PySide import QtCore

    if QtCore.QCoreApplication.instance() is None:
        QtCore.QCoreApplication([])
    t0 = time.time()
    while time.time() - t0 < timeout:
        doc.recompute()
        QtCore.QCoreApplication.processEvents()
        if all("Touched" not in o.State and (not hasattr(o, "getVisibleEdges") or o.getVisibleEdges()) for o in objs):
            return
        time.sleep(0.05)
    raise SkillError(
        errors.TIMEOUT, "TechDraw views did not finish computing", hint="Try a simpler drawing (fewer views)."
    )


def _pick_scale(need_w: float, need_h: float, avail_w: float, avail_h: float) -> float:
    for s in STANDARD_SCALES:
        if need_w * s <= avail_w and need_h * s <= avail_h:
            return s
    return STANDARD_SCALES[-1]


def _scale_text(s: float) -> str:
    return f"{int(s)}:1" if s >= 1 else f"1:{int(round(1 / s))}"


def _vertex_extremes(view: Any) -> Tuple[int, int, int, int]:
    pts = []
    for i, v in enumerate(view.getVisibleVertexes()):
        pt = v if hasattr(v, "x") else v.Point
        pts.append((i, pt.x, pt.y))
    xmin = min(pts, key=lambda t: t[1])[0]
    xmax = max(pts, key=lambda t: t[1])[0]
    ymin = min(pts, key=lambda t: t[2])[0]
    ymax = max(pts, key=lambda t: t[2])[0]
    return xmin, xmax, ymin, ymax


MAX_TABLE_ROWS = 12


def vertical_holes(shape: Any) -> List[Dict[str, Any]]:
    """Round holes along Z (those a plan view shows as circles): diameter and centre, measured from the
    minimum X/Y corner of the part. A hole is a full cylindrical face whose material lies outside it."""
    import math

    bb = geometry.tight_bbox(shape)
    found: Dict[Tuple[float, float, float], Dict[str, Any]] = {}
    for f in shape.Faces:
        try:
            surf = f.Surface
            if type(surf).__name__ != "Cylinder" or abs(abs(surf.Axis.z) - 1) > 1e-6:
                continue
            u0, u1, v0, v1 = f.ParameterRange
            if abs((u1 - u0) - 2 * math.pi) > 1e-6:
                continue  # a rounded corner or slot end, not a full hole
            u, v = (u0 + u1) / 2, (v0 + v1) / 2
            radial = f.valueAt(u, v) - surf.Center
            radial.z = 0
            if f.normalAt(u, v).dot(radial) >= 0:
                continue  # material inside the cylinder: a boss or pin
            key = (round(surf.Radius, 4), round(surf.Center.x, 4), round(surf.Center.y, 4))
            found.setdefault(
                key,
                {
                    "diameter": geometry.num(2 * surf.Radius),
                    "x": geometry.num(surf.Center.x - bb.XMin),
                    "y": geometry.num(surf.Center.y - bb.YMin),
                },
            )
        except Exception:
            continue
    holes = sorted(found.values(), key=lambda h: (h["diameter"], h["x"], h["y"]))
    for k, h in enumerate(holes, start=1):
        h["id"] = f"H{k}"
    return holes


def _remove_page(doc: Any, page: Any) -> None:
    # Collect names first: removing a view also removes its dimensions.
    names = [v.Name for v in page.Views] + [page.Name] + ([page.Template.Name] if page.Template is not None else [])
    for n in names:
        if doc.getObject(n) is not None:
            doc.removeObject(n)


def drawing(ctx: Context, p: Dict[str, Any]) -> Dict[str, Any]:
    import Part
    import TechDraw

    dest = workspace.resolve(ctx.root, p["filename"])
    if dest.suffix.lower() != ".dxf":
        raise SkillError(
            errors.INVALID_PARAM,
            "Drawings are written as DXF headless",
            hint="Use a .dxf filename. For PDF/SVG, open the saved .FCStd in FreeCAD and export the page.",
        )
    if any(pe["dest"] == dest for pe in ctx.pending_exports):
        raise SkillError(errors.INVALID_PARAM, f"'{p['filename']}' is already written earlier in this request")
    if p.get("targets"):
        objs = [ctx.get(t) for t in p["targets"]]
    else:
        objs = [o for o in visible_objects(ctx.doc) if role(o) == "result" and not o.Shape.isNull() and o.Shape.Solids]
    if not objs:
        raise SkillError(errors.EMPTY_RESULT, "Nothing to draw", hint="Create a solid first, or name 'targets'.")
    for o in objs:
        if o.Shape.isNull() or not o.Shape.Faces:
            raise SkillError(errors.INVALID_PARAM, f"'{o.Name}' has no faces to draw")

    doc = ctx.doc
    name = p.get("name") or "Drawing"
    old = doc.getObject(name)
    if old is not None:
        if old.TypeId != "TechDraw::DrawPage":
            raise SkillError(errors.NAME_CONFLICT, f"'{name}' exists and is not a drawing page")
        _remove_page(doc, old)  # drawings are generated: re-running replaces them

    shape = Part.makeCompound([o.Shape for o in objs])
    bb = geometry.tight_bbox(shape)
    L, W, H = bb.XLength, bb.YLength, bb.ZLength
    sheet_w, sheet_h = SHEETS[p["sheet"]]
    area = (MARGIN, TITLE_BAND, sheet_w - MARGIN, sheet_h - MARGIN)
    avail_w, avail_h = area[2] - area[0] - GAP, area[3] - area[1] - GAP
    side = "left" if p["projection"] == "first_angle" else "right"
    s = p["scale"] if p.get("scale") else _pick_scale(L + W, H + W, avail_w, avail_h)

    page = ctx.add("TechDraw::DrawPage", name, "Drawing")
    tpl = doc.addObject("TechDraw::DrawSVGTemplate", f"{page.Name}_Template")
    tpl.Template = _template(p["sheet"])
    page.Template = tpl
    page.Scale = s

    # Layout: front with the plan view and the side view around it.
    tw, th = (L + W) * s + GAP, (H + W) * s + GAP
    x0 = area[0] + (area[2] - area[0] - tw) / 2
    y0 = area[1] + (area[3] - area[1] - th) / 2
    fx = x0 + L * s / 2
    sx = x0 + L * s + GAP + W * s / 2
    if p["projection"] == "first_angle":  # ISO: plan below the front view, left view on the right
        fy = y0 + W * s + GAP + H * s / 2
        ty = y0 + W * s / 2
    else:  # third angle: plan above the front view, right view on the right
        fy = y0 + H * s / 2
        ty = y0 + H * s + GAP + W * s / 2
    layout = {"front": (fx, fy), "top": (fx, ty), side: (sx, fy)}
    views: Dict[str, Any] = {}
    for vname, (x, y) in layout.items():
        v = doc.addObject("TechDraw::DrawViewPart", f"{page.Name}_{vname.capitalize()}")
        page.addView(v)
        v.Source = objs
        v.Direction = App.Vector(*VIEW_DIRS[vname])
        v.XDirection = App.Vector(*VIEW_XDIRS[vname])
        v.ScaleType = "Page"
        v.X, v.Y = x, y
        views[vname] = v
    if p.get("iso"):
        v = doc.addObject("TechDraw::DrawViewPart", f"{page.Name}_Iso")
        page.addView(v)
        v.Source = objs
        v.Direction = App.Vector(*VIEW_DIRS["iso"])
        v.ScaleType = "Custom"
        v.Scale = s / 2
        v.X, v.Y = sx, ty
        views["iso"] = v
    _pump(list(views.values()), doc)

    # Dimensions, attached to the views' extreme vertices / circles, then checked against the model.
    dims: List[Tuple[Any, float, str]] = []

    def add_dim(view: Any, kind: str, refs: List[str], expected: float, label: str, dx: float, dy: float) -> None:
        dim = doc.addObject("TechDraw::DrawViewDimension", f"{page.Name}_Dim{len(dims) + 1}")
        dim.Type = kind
        dim.References2D = [(view, r) for r in refs]
        page.addView(dim)
        dim.X, dim.Y = dx, dy
        dims.append((dim, expected, label))

    if p["dimensions"] in ("overall", "overall_and_holes"):
        f = views["front"]
        xmin, xmax, ymin, ymax = _vertex_extremes(f)
        add_dim(f, "DistanceX", [f"Vertex{xmin}", f"Vertex{xmax}"], L, "length (X)", 0, H * s / 2 + 8)
        add_dim(f, "DistanceY", [f"Vertex{ymin}", f"Vertex{ymax}"], H, "height (Z)", -(L * s / 2 + 10), 0)
        t = views["top"]
        xmin, xmax, ymin, ymax = _vertex_extremes(t)
        add_dim(t, "DistanceY", [f"Vertex{ymin}", f"Vertex{ymax}"], W, "width (Y)", -(L * s / 2 + 10), 0)
    holes = vertical_holes(shape) if p["dimensions"] == "overall_and_holes" else []
    counted: List[Tuple[Any, int]] = []
    if p["dimensions"] == "overall_and_holes":
        seen = set()
        t = views["top"]
        for i, e in enumerate(t.getVisibleEdges()):
            c = getattr(e, "Curve", None)
            if type(c).__name__ != "Circle" or not e.isClosed():
                continue  # arcs (rounded corners, slot ends) get no diameter
            key = round(c.Radius, 3)
            if key in seen or len(seen) >= 8:
                continue
            seen.add(key)
            add_dim(t, "Diameter", [f"Edge{i}"], None, "diameter", c.Center.x + c.Radius + 6, c.Center.y + c.Radius + 6)
            same = sum(1 for h in holes if abs(h["diameter"] / 2 - c.Radius) <= 1e-3)
            if same > 1:  # "4x" before the value: one dimension stands for every hole of this size
                dims[-1][0].FormatSpec = f"{same}x " + dims[-1][0].FormatSpec
                counted.append((dims[-1][0], same))

    # Title block: the template's fields (FCStd/PDF) and a text block that is also written to the DXF.
    lines = [
        p.get("title") or objs[0].Label,
        f"Scale {_scale_text(s)}  ({p['projection'].replace('_', ' ')} projection)",
        "Dimensions in mm",
    ] + [x for x in (p.get("material"), p.get("author"), p.get("number")) if x]
    for k, line in enumerate(lines):  # one annotation per line: the DXF writer keeps only the first line of each
        note = doc.addObject("TechDraw::DrawViewAnnotation", f"{page.Name}_Title{k + 1}")
        page.addView(note)
        note.Text = [line]
        note.TextSize = 5.0 if k == 0 else 3.5
        note.X, note.Y = sheet_w - 80, 48 - 7 * k
    # Hole table: where each hole is, from the part's lower-left corner in the plan view (X right, Y up).
    table = [f"{h['id']}  dia {h['diameter']:g}  X {h['x']:g}  Y {h['y']:g}" for h in holes[:MAX_TABLE_ROWS]]
    if len(holes) > MAX_TABLE_ROWS:
        table.append(f"+ {len(holes) - MAX_TABLE_ROWS} more holes: see the hole list of the model")
    if table:
        table.insert(0, "HOLES (from lower-left corner of plan view, mm)")
    for k, line in enumerate(table):
        note = doc.addObject("TechDraw::DrawViewAnnotation", f"{page.Name}_Hole{k}")
        page.addView(note)
        note.Text = [line]
        note.TextSize = 2.5
        note.X, note.Y = MARGIN + 55, 54 - 3.6 * k
    if hasattr(tpl, "EditableTexts"):
        texts = dict(tpl.EditableTexts)
        values = {
            "title": p.get("title") or objs[0].Label,
            "creator": p.get("author", ""),
            "scale": _scale_text(s),
            "date_of_issue": datetime.date.today().isoformat(),
            "part_material": p.get("material", ""),
            "drawing_number": p.get("number", ""),
        }
        for k, v in values.items():
            if k in texts and v:
                texts[k] = v
        tpl.EditableTexts = texts
    _pump([o for o, _e, _l in dims] + list(views.values()), doc)

    model_radii = [e.Curve.Radius for e in shape.Edges if type(getattr(e, "Curve", None)).__name__ == "Circle"]
    results = []
    for dim, expected, label in dims:
        raw = float(dim.getRawValue())
        entry = {"what": label, "value": geometry.num(raw), "text": dim.getText() if hasattr(dim, "getText") else None}
        count = next((n for d, n in counted if d is dim), None)
        if count:
            entry["count"] = count
        if expected is None:  # a diameter: must be one of the model's circle diameters
            if not any(abs(raw / 2 - r) <= 1e-3 for r in model_radii):
                raise SkillError(
                    errors.EXPORT_FAILED,
                    f"Drawing diameter {raw:.4f} mm matches no circle of the model",
                    details={"dimension": dim.Name},
                )
        elif abs(raw - expected) > 1e-3 + 1e-6 * expected:
            raise SkillError(
                errors.EXPORT_FAILED,
                f"Drawing dimension '{label}' reads {raw:.4f} mm but the model measures {expected:.4f} mm",
                details={"dimension": dim.Name},
            )
        results.append(entry)

    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_name(f".{dest.stem}.fcskill-tmp.dxf")
    TechDraw.writeDXFPage(page, str(tmp))
    from collections import Counter

    from .export import dxf_file_entities

    text = tmp.read_text(encoding="utf-8", errors="replace") if tmp.exists() else ""
    counts = Counter(k for k, _ in dxf_file_entities(text)) if text else Counter()
    if not counts or counts.get("DIMENSION", 0) != len(dims):
        if tmp.exists():
            os.remove(tmp)
        raise SkillError(
            errors.EXPORT_FAILED, f"The DXF drawing is incomplete ({dict(counts)}; expected {len(dims)} dimensions)"
        )
    record = {
        "file": workspace.relative(ctx.root, dest),
        "format": "dxf",
        "page": page.Name,
        "sheet": p["sheet"],
        "scale": _scale_text(s),
        "projection": p["projection"],
        "views": list(views),
        "dimensions": results,
        "holes": holes,
        "hole_table_on_sheet": min(len(holes), MAX_TABLE_ROWS),
        "entities": dict(counts),
        "objects": [o.Name for o in objs],
    }
    ctx.pending_exports.append({"tmp": tmp, "dest": dest, "record": record})
    if p.get("preview"):
        from .. import dxfpreview

        pdest = workspace.resolve(ctx.root, p["preview"])
        if pdest.suffix.lower() != ".png":
            raise SkillError(errors.INVALID_PARAM, "'preview' must be a .png filename")
        ptmp = pdest.with_name(f".{pdest.stem}.fcskill-tmp.png")
        pdest.parent.mkdir(parents=True, exist_ok=True)
        stats = dxfpreview.render_png(text, str(ptmp), SHEETS[p["sheet"]])
        ctx.pending_exports.append(
            {
                "tmp": ptmp,
                "dest": pdest,
                "record": {
                    "file": workspace.relative(ctx.root, pdest),
                    "format": "png",
                    "preview_of": workspace.relative(ctx.root, dest),
                    "legend": "rendered from the DXF: geometry black, dimension lines blue, sheet border grey; texts not drawn",
                    **stats,
                },
            }
        )
    ctx.mutated = True
    return {"object": None, "data": record}


HANDLERS = {"drawing": drawing}

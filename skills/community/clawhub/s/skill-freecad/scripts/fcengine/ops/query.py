"""Read-only operations: inspect and check."""

from __future__ import annotations

from typing import Any, Dict, List

from .. import errors, geometry
from ..document import CONSUMES_PROP, HELPERS_PROP, SEL_PROP, Context, object_entry, visible_objects
from ..errors import SkillError

MAX_ELEMENTS = 300
HIDDEN_PROPS = {
    "Label",
    "Label2",
    "Visibility",
    "ExpressionEngine",
    "Shape",
    "Proxy",
    "Placement",
    "Content",
    "cells",
    "ExportPython",
    "Refine",
    HELPERS_PROP,
    SEL_PROP,
    CONSUMES_PROP,
}
SKIP_GROUPS = {"Base"}


def _value(obj: Any, prop: str) -> Any:
    v = getattr(obj, prop)
    if hasattr(v, "Value") and hasattr(v, "Unit"):  # Quantity
        return geometry.num(v.Value)
    if hasattr(v, "x") and hasattr(v, "y") and hasattr(v, "z") and not hasattr(v, "Name"):
        return geometry.vec(v)
    if hasattr(v, "Name") and hasattr(v, "TypeId"):
        return v.Name
    if isinstance(v, (list, tuple)):
        out = []
        for x in v:
            if hasattr(x, "Name") and hasattr(x, "TypeId"):
                out.append(x.Name)
            elif hasattr(x, "x") and hasattr(x, "z"):
                out.append(geometry.vec(x))
            elif isinstance(x, tuple):
                out.append([_plain(y) for y in x])
            else:
                out.append(_plain(x))
        return out[:200]
    return _plain(v)


def _plain(v: Any) -> Any:
    if isinstance(v, float):
        return geometry.num(v)
    if isinstance(v, (int, str, bool)) or v is None:
        return v
    if hasattr(v, "Name") and hasattr(v, "TypeId"):
        return v.Name
    if isinstance(v, (list, tuple)):
        return [_plain(x) for x in v]
    return str(v)


def editable_properties(obj: Any) -> Dict[str, Any]:
    props: Dict[str, Any] = {}
    for prop in obj.PropertiesList:
        if prop in HIDDEN_PROPS:
            continue
        try:
            mode = obj.getEditorMode(prop)
            if "Hidden" in mode or "ReadOnly" in mode:
                continue
            if obj.getGroupOfProperty(prop) in SKIP_GROUPS:
                continue
            props[prop] = _value(obj, prop)
        except Exception:
            continue
    return props


def _params(doc: Any) -> Dict[str, Any]:
    sheet = doc.getObject("Params")
    if sheet is None or not sheet.TypeId.startswith("Spreadsheet::"):
        return {}
    out: Dict[str, Any] = {}
    for cell in sheet.getUsedCells():
        alias = sheet.getAlias(cell)
        if alias:
            v = sheet.get(cell)
            out[alias] = geometry.num(v.Value) if hasattr(v, "Value") else _plain(v)
    return out


def inspect(ctx: Context, p: Dict[str, Any]) -> Dict[str, Any]:
    doc = ctx.doc
    if not p.get("target"):
        # No validity here: checking every object of a large tree takes seconds; inspect one object for it.
        objs = [
            object_entry(o, validity=False) for o in visible_objects(doc) if not o.TypeId.startswith("Spreadsheet::")
        ]
        data: Dict[str, Any] = {"objects": objs}
        params = _params(doc)
        if params:
            data["params"] = params
        if p.get("topology"):
            ctx.warn("IGNORED", "topology=true needs a target")
        return {"data": data}
    obj = ctx.get(p["target"], need_shape=False)
    entry = object_entry(obj, detailed=True)
    entry["used_by"] = list(dict.fromkeys(o.Name for o in obj.InList if not o.TypeId.startswith("App::Origin")))
    entry["properties"] = editable_properties(obj)
    if hasattr(obj, "Placement"):
        pl = obj.Placement
        entry["position"] = geometry.vec(pl.Base)
        entry["rotation"] = {
            "axis": geometry.vec(pl.Rotation.Axis, 6),
            "angle": geometry.num(pl.Rotation.Angle * 180 / 3.141592653589793),
        }
    exprs = {prop: expr for prop, expr in obj.ExpressionEngine}
    if exprs:
        entry["expressions"] = exprs
    if SEL_PROP in obj.PropertiesList:
        import json

        entry["selector"] = json.loads(getattr(obj, SEL_PROP))
    if obj.TypeId == "Assembly::AssemblyObject":
        from .assembly import bom

        entry["bom"] = bom(obj)
    if obj.TypeId == "Sketcher::SketchObject":
        try:
            entry["sketch"] = {"degrees_of_freedom": int(obj.DoF), "fully_constrained": bool(obj.FullyConstrained)}
        except Exception:
            pass
    if geometry.is_part_shape(obj) and not obj.Shape.isNull() and obj.Shape.Solids:
        verdict, reason = geometry.self_check(obj.Shape)
        entry["self_intersecting"] = verdict if verdict is not None else f"not checked ({reason})"
    if p.get("topology") and geometry.is_part_shape(obj) and not obj.Shape.isNull():
        faces = geometry.describe_faces(obj.Shape)
        edges = geometry.describe_edges(obj.Shape)
        entry["topology"] = {
            "faces": faces[:MAX_ELEMENTS],
            "edges": edges[:MAX_ELEMENTS],
        }
        if len(faces) > MAX_ELEMENTS or len(edges) > MAX_ELEMENTS:
            entry["topology"]["truncated"] = True
    return {"object": obj, "data": entry}


def check(ctx: Context, p: Dict[str, Any]) -> Dict[str, Any]:
    obj = ctx.get(p["target"])
    failures = geometry.check_expectations(obj.Shape, p["expect"])
    if failures:
        raise SkillError(
            errors.EXPECTATION_FAILED,
            f"'{obj.Name}' does not meet expectations",
            hint="Compare expected and actual values to find the wrong dimension or position.",
            details={"failures": failures},
        )
    return {
        "object": obj,
        "data": {"passed": sorted(k for k in p["expect"] if k not in ("tolerance", "volume_tolerance"))},
    }


HANDLERS = {"inspect": inspect, "check": check}

__all__: List[str] = ["HANDLERS", "editable_properties"]

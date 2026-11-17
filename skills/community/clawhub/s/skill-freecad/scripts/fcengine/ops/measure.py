"""Clearance, interference and mass between objects (read-only)."""

from __future__ import annotations

from itertools import combinations
from typing import Any, Dict, List

from .. import errors, geometry
from ..document import Context, role, visible_objects
from ..errors import SkillError
from . import assembly

MAX_OBJECTS = 30
TOUCH = 1e-6


class _Item:
    """A measured object: a solid, a body, or an assembly part (a link, measured where it is placed)."""

    def __init__(self, obj: Any) -> None:
        from .material import density_of

        self.Name = obj.Name
        self.Shape = assembly.placed_shape(obj) if obj.TypeId == "App::Link" else obj.Shape
        source = (
            obj.LinkedObject if obj.TypeId == "App::Link" and getattr(obj, "LinkedObject", None) is not None else obj
        )
        self.density = density_of(source)


def _items(ctx: Context, refs: Any) -> List[_Item]:
    if refs:
        objs = [ctx.get(n, need_shape=False) for n in refs]
    else:
        objs = [o for o in visible_objects(ctx.doc) if role(o) == "result" and geometry.is_part_shape(o)]
    out: List[_Item] = []
    for o in objs:
        if assembly._is_assembly(o):
            out += [_Item(x) for x in assembly.parts_of(o)]  # compare the parts as assembled
        elif o.TypeId == "App::Link" or geometry.is_part_shape(o):
            out.append(_Item(o))
        else:
            raise SkillError(errors.INVALID_PARAM, f"'{o.Name}' ({o.TypeId}) has no shape and cannot be measured")
    return out


def _pair(a: Any, b: Any) -> Dict[str, Any]:
    sa, sb = a.Shape, b.Shape
    overlap = 0.0
    if sa.BoundBox.intersect(sb.BoundBox) and sa.Solids and sb.Solids:
        try:
            overlap = sa.common(sb).Volume
        except Exception:
            overlap = 0.0
    dist, pts, _info = sa.distToShape(sb)
    if overlap > TOUCH:
        status, dist = "interfering", 0.0
    elif dist <= TOUCH:
        status = "touching"
    else:
        status = "clear"
    out: Dict[str, Any] = {"a": a.Name, "b": b.Name, "status": status, "distance": geometry.num(dist)}
    if overlap > TOUCH:
        out["overlap_volume"] = geometry.num(overlap, 3)
    elif pts:
        out["closest"] = [geometry.vec(pts[0][0]), geometry.vec(pts[0][1])]
    return out


def measure(ctx: Context, p: Dict[str, Any]) -> Dict[str, Any]:
    objs = [o for o in _items(ctx, p.get("objects")) if p.get("objects") or (not o.Shape.isNull() and o.Shape.Solids)]
    if len(objs) > MAX_OBJECTS:
        raise SkillError(
            errors.INVALID_PARAM,
            f"Too many objects to compare ({len(objs)}; max {MAX_OBJECTS})",
            hint="Name the objects to compare with 'objects'.",
        )
    for o in objs:
        if o.Shape.isNull() or not o.Shape.Faces:
            raise SkillError(errors.INVALID_PARAM, f"'{o.Name}' has no geometry to measure")
    data: Dict[str, Any] = {"objects": [o.Name for o in objs]}
    pairs: List[Dict[str, Any]] = [_pair(a, b) for a, b in combinations(objs, 2)]
    if pairs:
        data["pairs"] = pairs
        data["min_distance"] = min(x["distance"] for x in pairs)
        data["interferences"] = sum(1 for x in pairs if x["status"] == "interfering")
    rho_all = None
    if "material" in p or "density" in p:
        rho_all = float(p["density"]) if "density" in p else _material_density(p["material"])
        data["density_g_cm3"] = rho_all
    elif any(o.density for o in objs):  # materials assigned with the 'material' op
        data["mass_source"] = "assigned materials"
    props: Dict[str, Any] = {}
    for o in objs:
        if not o.Shape.Solids:
            continue
        rho = rho_all or o.density
        entry = {"volume": geometry.num(o.Shape.Volume, 3), "area": geometry.num(o.Shape.Area, 3)}
        entry.update(geometry.mass_properties(o.Shape, rho))
        props[o.Name] = entry
    if props:
        data["properties"] = props
    weighed = {n: e for n, e in props.items() if "mass_g" in e}
    if weighed:
        data["mass_g"] = {n: geometry.num(e["mass_g"], 2) for n, e in weighed.items()}
        if len(weighed) == len(props) and len(props) > 1:  # every part has a mass: the set as a whole
            total = sum(e["mass_g"] for e in weighed.values())
            com = [sum(e["mass_g"] * e["center_of_mass"][k] for e in weighed.values()) / total for k in range(3)]
            data["total"] = {"mass_g": geometry.num(total, 2), "center_of_mass": [geometry.num(c) for c in com]}
    req = p.get("require") or {}
    failures = []
    if "min_clearance" in req:
        bad = [x for x in pairs if x["distance"] < req["min_clearance"] - 1e-9 or x["status"] == "interfering"]
        failures += [
            {
                "check": "min_clearance",
                "pair": [x["a"], x["b"]],
                "expected": req["min_clearance"],
                "actual": x["distance"],
                "status": x["status"],
            }
            for x in bad
        ]
    if req.get("no_interference"):
        failures += [
            {"check": "no_interference", "pair": [x["a"], x["b"]], "overlap_volume": x["overlap_volume"]}
            for x in pairs
            if x["status"] == "interfering"
        ]
    if failures:
        raise SkillError(
            errors.EXPECTATION_FAILED,
            f"{len(failures)} requirement(s) not met",
            hint="Move or resize the parts; 'closest' gives the points where the gap is smallest.",
            details={"failures": failures, "pairs": pairs},
        )
    return {"data": data}


def _material_density(name: str) -> float:
    """g/cm3 of a material preset or FreeCAD library material (the same names as the 'material' op)."""
    from . import material

    rho = material.resolve(name, material._library())["density"]
    if not rho:
        raise SkillError(
            errors.INVALID_PARAM,
            f"Material '{name}' has no density",
            hint="Give 'density' in g/cm3 instead.",
        )
    return rho


HANDLERS = {"measure": measure}

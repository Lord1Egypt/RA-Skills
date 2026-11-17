"""Dress-up features: fillet, chamfer, shell."""

from __future__ import annotations

from typing import Any, Dict

from .. import errors, geometry, selectors
from ..document import Context, apply_selector
from ..errors import SkillError


def _pd_base(ctx: Context, target: Any, op: str) -> Any:
    """For a PartDesign body, the feature a new dress-up builds on (its tip)."""
    from .partdesign import body_of

    if target.TypeId == "PartDesign::Body":
        if target.Tip is None or target.Shape.isNull():
            raise SkillError(errors.INVALID_PARAM, f"Body '{target.Name}' has no material yet", hint="Add a pad first.")
        return target.Tip
    if body_of(target) is not None:
        raise SkillError(
            errors.INVALID_PARAM,
            f"'{target.Name}' is a feature inside body '{body_of(target).Name}'",
            hint=f"Give the body as target; the {op} is added at the end of its feature tree.",
        )
    return None


def _pd_dressup(
    ctx: Context,
    body: Any,
    tip: Any,
    type_id: str,
    default: str,
    p: Dict[str, Any],
    sel_param: str,
    size_prop: str,
    size: float,
    extra: Any = None,
    remove: bool = True,
) -> Any:
    before = body.Shape.Volume
    obj = ctx.add(type_id, p.get("name"), default)
    body.addObject(obj)
    obj.Base = (tip, ["Edge1" if sel_param == "edges" else "Face1"])
    sel = p[sel_param]
    apply_selector(obj, sel_param, sel, size)
    if selectors.is_dynamic(sel):
        ctx.set_selector(obj, sel_param, sel)
    setattr(obj, size_prop, size)
    for k, v in (extra or {}).items():
        setattr(obj, k, v)
    from .partdesign import finish

    finish(ctx, body, obj, before, remove=remove)
    return obj


def _edge_feature(ctx: Context, type_id: str, default: str, p: Dict[str, Any], size: float) -> Any:
    target = ctx.get(p["target"])
    tip = _pd_base(ctx, target, default.lower())
    if tip is not None:
        pd_type = {"Part::Fillet": "PartDesign::Fillet", "Part::Chamfer": "PartDesign::Chamfer"}[type_id]
        # Fillets/chamfers remove material on convex edges and add it on concave ones.
        return _pd_dressup(
            ctx,
            target,
            tip,
            pd_type,
            default,
            p,
            "edges",
            "Radius" if default == "Fillet" else "Size",
            size,
            remove=None,
        )
    obj = ctx.add(type_id, p.get("name"), default)
    obj.Base = target
    try:
        idx = apply_selector(obj, "edges", p["edges"], size)
    except Exception:
        ctx.doc.removeObject(obj.Name)
        raise
    if selectors.is_dynamic(p["edges"]):
        ctx.set_selector(obj, "edges", p["edges"])
    ctx.recompute()
    ctx.verify_solid(obj, default)
    shortest = min(target.Shape.Edges[i - 1].Length for i in idx)
    if size >= shortest:
        ctx.warn(
            "LARGE_SIZE",
            f"size {size} >= shortest selected edge ({geometry.num(shortest)} mm); check the result carefully",
        )
    return obj


def fillet(ctx: Context, p: Dict[str, Any]) -> Any:
    return _edge_feature(ctx, "Part::Fillet", "Fillet", p, float(p["radius"]))


def chamfer(ctx: Context, p: Dict[str, Any]) -> Any:
    return _edge_feature(ctx, "Part::Chamfer", "Chamfer", p, float(p["size"]))


def shell(ctx: Context, p: Dict[str, Any]) -> Any:
    target = ctx.get(p["target"])
    tip = _pd_base(ctx, target, "shell")
    if tip is not None:
        return _pd_dressup(
            ctx,
            target,
            tip,
            "PartDesign::Thickness",
            "Shell",
            p,
            "open_faces",
            "Value",
            float(p["thickness"]),
            extra={"Reversed": not p["outward"], "Join": "Intersection" if p["join"] == "intersection" else "Arc"},
            remove=not p["outward"],
        )
    target_volume = target.Shape.Volume
    obj = ctx.add("Part::Thickness", p.get("name"), "Shell")
    obj.Faces = (target, ["Face1"])  # placeholder, replaced by the selector
    try:
        apply_selector(obj, "open_faces", p["open_faces"], None)
    except Exception:
        ctx.doc.removeObject(obj.Name)
        raise
    if selectors.is_dynamic(p["open_faces"]):
        ctx.set_selector(obj, "open_faces", p["open_faces"])
    t = float(p["thickness"])
    obj.Value = t if p["outward"] else -t
    obj.Mode = "Skin"
    obj.Join = "Intersection" if p["join"] == "intersection" else "Arc"
    ctx.recompute()
    ctx.verify_solid(obj, "Shell")
    if not p["outward"] and obj.Shape.Volume >= target_volume:
        ctx.warn("UNEXPECTED_VOLUME", "shell did not reduce the volume; the result may not be hollow")
    return obj


HANDLERS = {"fillet": fillet, "chamfer": chamfer, "shell": shell}

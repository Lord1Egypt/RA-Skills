"""Parametric arrays, built on Draft's Array feature (or PartDesign patterns for features of a body)."""

from __future__ import annotations

from typing import Any, Dict

import FreeCAD as App

from ..document import Context


def _pd_target(ctx: Context, p: Dict[str, Any]) -> Any:
    """A PartDesign feature (inside a body) to pattern natively, else None."""
    from .partdesign import body_of

    target = ctx.get(p["target"], need_shape=False)
    return (
        target
        if target.TypeId.startswith("PartDesign::") and target.TypeId != "PartDesign::Body" and body_of(target)
        else None
    )


def _new_array(ctx: Context, p: Dict[str, Any], default: str) -> Any:
    from draftobjects.array import Array  # needs FreeCAD 1.1 headless (see compat.py)

    target = ctx.get(p["target"])
    obj = ctx.add("Part::FeaturePython", p.get("name"), default)
    Array(obj)
    obj.Base = target
    obj.Fuse = bool(p["fuse"])
    return obj


def _finish(ctx: Context, obj: Any, expected: int) -> Any:
    ctx.recompute()
    ctx.verify_solid(obj, "Array")
    # Separate instances are normal (hole patterns, legs); only check the count.
    if not obj.Fuse and len(obj.Shape.Solids) != expected:
        ctx.warn("UNEXPECTED_COUNT", f"array has {len(obj.Shape.Solids)} solids, expected {expected}")
    return obj


def linear_array(ctx: Context, p: Dict[str, Any]) -> Any:
    feat = _pd_target(ctx, p)
    if feat is not None:
        from .partdesign import pattern

        return pattern(ctx, p, "linear", feat)
    obj = _new_array(ctx, p, "LinearArray")
    obj.ArrayType = "ortho"
    obj.NumberX, obj.NumberY, obj.NumberZ = p["count"], 1, 1
    obj.IntervalX = App.Vector(*p["step"])
    return _finish(ctx, obj, p["count"])


def grid_array(ctx: Context, p: Dict[str, Any]) -> Any:
    feat = _pd_target(ctx, p)
    if feat is not None:
        from .partdesign import pattern

        return pattern(ctx, p, "grid", feat)
    obj = _new_array(ctx, p, "GridArray")
    obj.ArrayType = "ortho"
    obj.NumberX, obj.NumberY, obj.NumberZ = p["count_x"], p["count_y"], p["count_z"]
    obj.IntervalX = App.Vector(p["step_x"], 0, 0)
    obj.IntervalY = App.Vector(0, p["step_y"], 0)
    obj.IntervalZ = App.Vector(0, 0, p["step_z"])
    return _finish(ctx, obj, p["count_x"] * p["count_y"] * p["count_z"])


def polar_array(ctx: Context, p: Dict[str, Any]) -> Any:
    feat = _pd_target(ctx, p)
    if feat is not None:
        from .partdesign import pattern

        return pattern(ctx, p, "polar", feat)
    obj = _new_array(ctx, p, "PolarArray")
    obj.ArrayType = "polar"
    obj.NumberPolar = p["count"]
    obj.Angle = p["angle"]
    obj.Axis = App.Vector(*p["axis"])
    obj.Center = App.Vector(*p["center"])
    obj.IntervalAxis = App.Vector(0, 0, 0)
    return _finish(ctx, obj, p["count"])


HANDLERS = {"linear_array": linear_array, "grid_array": grid_array, "polar_array": polar_array}

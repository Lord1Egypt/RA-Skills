"""Loft (solid through cross-sections) and sweep (profile along a path).

Probed on FreeCAD 1.1:

- Part::Sweep cannot sweep a profile with holes ("fatal error"); a stand-alone
  tube is therefore the outer sweep minus the inner sweeps. PartDesign pipes
  handle holes directly.
- With a sharp-cornered path, Part::Sweep's default 'Transformed' transition
  silently returns about half the volume; 'Right corner' is exact.
- A PartDesign pipe cannot use a path outside its body; the path is bound
  into the body with a SubShapeBinder.
- A sketch's own profile frame is placed at the start of the path, normal to
  it, so agents draw profiles in 2D around the origin.
"""

from __future__ import annotations

import json
from typing import Any, Dict, List, Optional, Tuple

import FreeCAD as App

from .. import errors, geometry, profiles
from ..document import Context
from ..errors import SkillError
from .sketch import fill_sketch, plane_placement

OFFSET_AXIS = {"XY": "z", "XZ": "y", "YZ": "x"}
PATH_PROP = "FCSkillPath"


# ------------------------------------------------------------------ helpers


def _plain_sketch(ctx: Context, name: str, shapes: Any, plane: str = "XY", offset: Any = 0) -> Any:
    sk = ctx.doc.addObject("Sketcher::SketchObject", name)
    sk.Label = sk.Name
    sk.Placement = plane_placement(plane, 0 if isinstance(offset, str) else float(offset))
    if isinstance(offset, str):
        ctx.assign(sk, f".Placement.Base.{OFFSET_AXIS[plane]}", offset)
    fill_sketch(sk, shapes)
    return sk


def _single_loop(shape: Any, what: str) -> None:
    try:
        profiles.shape_segments(shape, 0)
    except profiles.ProfileError as e:
        raise SkillError(errors.INVALID_PARAM, f"{what}: {str(e).replace('shapes[0]', 'shape')}") from None


def _set_offset(ctx: Context, sk: Any, prop: str, axis: str, value: Any) -> None:
    if isinstance(value, str):
        ctx.assign(sk, f".{prop}.Base.{axis}", value)
        return
    sk.setExpression(f".{prop}.Base.{axis}", None)
    pl = getattr(sk, prop)
    base = App.Vector(pl.Base)
    setattr(base, axis, float(value))
    setattr(sk, prop, App.Placement(base, pl.Rotation))


# ------------------------------------------------------------------ loft


def loft(ctx: Context, p: Dict[str, Any]) -> Any:
    sections = p["sections"]
    for i, sec in enumerate(sections):
        _single_loop(sec["shape"], f"sections[{i}]")
    if p.get("body"):
        return _pd_loft(ctx, p)
    obj = ctx.add("Part::Loft", p.get("name"), "Loft")
    sketches = []
    for i, sec in enumerate(sections):
        sk = _plain_sketch(ctx, f"{obj.Name}_Section{i}", [sec["shape"]], sec.get("plane", "XY"), sec.get("offset", 0))
        ctx.own_helper(obj, sk)
        sketches.append(sk)
    obj.Sections = sketches
    obj.Solid = True
    obj.Ruled = bool(p.get("ruled", False))
    obj.Closed = bool(p.get("closed", False))
    ctx.recompute()
    ctx.verify_solid(obj, "Loft")
    return obj


def _pd_loft(ctx: Context, p: Dict[str, Any]) -> Any:
    from . import partdesign

    bd = partdesign.get_body(ctx, p["body"])
    remove = p.get("mode", "add") == "remove"
    if remove:
        partdesign._require_material(bd, "cut")
    before = partdesign._volume(bd)
    obj = ctx.add("PartDesign::SubtractiveLoft" if remove else "PartDesign::AdditiveLoft", p.get("name"), "Loft")
    sketches = [
        partdesign.make_sketch(ctx, bd, obj.Name, sec, [sec["shape"]], suffix=f"Section{i}")
        for i, sec in enumerate(p["sections"])
    ]
    bd.addObject(obj)
    for sk in sketches:
        ctx.own_helper(obj, sk)
    obj.Profile = sketches[0]
    obj.Sections = sketches[1:]
    obj.Ruled = bool(p.get("ruled", False))
    obj.Closed = bool(p.get("closed", False))
    return partdesign.finish(ctx, bd, obj, before, remove)


def loft_sketches(obj: Any) -> List[Any]:
    def unwrap(x: Any) -> Any:  # PartDesign link-sub properties give (object, [subelements])
        return x[0] if isinstance(x, tuple) else x

    if obj.TypeId == "Part::Loft":
        return [unwrap(x) for x in obj.Sections]
    return [unwrap(obj.Profile)] + [unwrap(x) for x in obj.Sections]


def set_sections(ctx: Context, obj: Any, value: Any) -> None:
    """'set' on a loft: same number of sections, new shapes/planes/offsets."""
    from .. import validate

    msg = validate._check_value(_catalog_param("loft", "sections"), value)
    if msg:
        raise SkillError(errors.INVALID_PARAM, f"{obj.Name}: 'sections' {msg}")
    sketches = loft_sketches(obj)
    if len(value) != len(sketches):
        raise SkillError(
            errors.INVALID_PARAM,
            f"'{obj.Name}' has {len(sketches)} sections; give exactly {len(sketches)}",
            hint="To change the number of sections, delete the loft and create it again.",
        )
    in_body = obj.TypeId != "Part::Loft"
    for i, (sk, sec) in enumerate(zip(sketches, value)):
        _single_loop(sec["shape"], f"sections[{i}]")
        plane, off = sec.get("plane", "XY"), sec.get("offset", 0)
        prop = "AttachmentOffset" if in_body else "Placement"
        for ax in "xyz":
            sk.setExpression(f".{prop}.Base.{ax}", None)
        setattr(sk, prop, plane_placement(plane, 0))
        _set_offset(ctx, sk, prop, OFFSET_AXIS[plane], off)
        fill_sketch(sk, [sec["shape"]])


def _catalog_param(op: str, name: str) -> Any:
    from ..catalog import OPS_BY_NAME

    return next(x for x in OPS_BY_NAME[op].params if x.name == name)


# ------------------------------------------------------------------ sweep paths


def _up(p: Dict[str, Any]) -> Optional[List[float]]:
    if p.get("up") is not None:
        return p["up"]
    return p["helix"].get("axis", [0, 0, 1]) if "helix" in p else None


def _path_spec(p: Dict[str, Any]) -> Dict[str, Any]:
    if "helix" in p:
        if p.get("smooth") or p.get("corner_radius"):
            raise SkillError(errors.INVALID_PARAM, "'smooth' and 'corner_radius' apply to 'path', not to 'helix'")
        return {"helix": p["helix"]}
    return {
        "path": p["path"],
        "smooth": bool(p.get("smooth", False)),
        "corner_radius": float(p.get("corner_radius", 0)),
    }


def _check_path(spec: Dict[str, Any]) -> None:
    if "helix" in spec:
        return
    pts = [App.Vector(*q) for q in spec["path"]]
    for i in range(len(pts) - 1):
        if (pts[i + 1] - pts[i]).Length < 1e-6:
            raise SkillError(errors.INVALID_PARAM, f"path points {i} and {i + 1} coincide")
    if spec["smooth"] and spec["corner_radius"]:
        raise SkillError(
            errors.INVALID_PARAM,
            "'corner_radius' rounds the corners of a straight-segment path; a 'smooth' path has no corners",
            hint="Give one of them.",
        )
    if len(pts) == 2 and (spec["smooth"] or spec["corner_radius"]):
        raise SkillError(
            errors.INVALID_PARAM, "a 2-point path is a straight line; 'smooth' and 'corner_radius' need 3+ points"
        )


def _make_path(ctx: Context, owner: str, spec: Dict[str, Any]) -> Any:
    if "helix" in spec:
        h = spec["helix"]
        obj = ctx.doc.addObject("Part::Helix", f"{owner}_Path")
        obj.Radius, obj.Pitch, obj.Height = float(h["radius"]), float(h["pitch"]), float(h["height"])
        obj.LocalCoord = "Left-handed" if h.get("left_handed") else "Right-handed"
        obj.Placement = App.Placement(
            App.Vector(*h.get("center", [0, 0, 0])), geometry.rotation_to(h.get("axis", [0, 0, 1]))
        )
    else:
        import Draft

        pts = [App.Vector(*q) for q in spec["path"]]
        obj = Draft.make_bspline(pts, closed=False) if spec["smooth"] else Draft.make_wire(pts, closed=False)
        obj.Label = obj.Name
        if not spec["smooth"] and spec["corner_radius"]:
            obj.FilletRadius = spec["corner_radius"]
        obj.Label = f"{owner}_Path"
    obj.Label = f"{owner}_Path"
    _store_spec(obj, spec)
    return obj


def _local_placement(spec: Dict[str, Any]) -> Any:
    if "helix" in spec:
        h = spec["helix"]
        return App.Placement(App.Vector(*h.get("center", [0, 0, 0])), geometry.rotation_to(h.get("axis", [0, 0, 1])))
    return App.Placement()


def _follow_body(path: Any, body: Any, spec: Dict[str, Any]) -> None:
    """Place the path in body coordinates. (A placement expression on the body would make a dependency cycle:
    body -> binder -> path -> body.) sync_body_paths re-applies this after the body moves."""
    spec["body"] = body.Name
    path.Placement = body.Placement.multiply(_local_placement(spec))


def sync_body_paths(ctx: Context) -> None:
    """After edits: keep the paths of body sweeps in step with their body's placement."""
    from ..document import _helpers

    for path in [o for o in ctx.doc.Objects if PATH_PROP in o.PropertiesList]:
        spec = json.loads(getattr(path, PATH_PROP))
        body = ctx.doc.getObject(spec.get("body", "")) if spec.get("body") else None
        if body is None:
            continue
        want = body.Placement.multiply(_local_placement(spec))
        if want.isSame(path.Placement, 1e-9):
            continue
        path.Placement = want
        owner = next((o for o in ctx.doc.Objects if path.Name in _helpers(o)), None)
        parts = sweep_parts(ctx, owner) if owner is not None else None
        if parts is not None:
            replace_profiles(ctx, parts)


def _store_spec(obj: Any, spec: Dict[str, Any]) -> None:
    if PATH_PROP not in obj.PropertiesList:
        obj.addProperty("App::PropertyString", PATH_PROP, "FCSkill", "Path spec this object was built from")
        obj.setEditorMode(PATH_PROP, 2)
    setattr(obj, PATH_PROP, json.dumps(spec))


def _start_frame(path_shape: Any, up: Optional[List[float]]) -> Tuple[Any, Any, Any, Any]:
    """Origin, x, y, normal of the profile frame at the start of the path."""
    edges = path_shape.Wires[0].OrderedEdges if path_shape.Wires else path_shape.Edges
    e = edges[0]
    start = path_shape.Wires[0].OrderedVertexes[0].Point if path_shape.Wires else e.Vertexes[0].Point
    u = (
        e.FirstParameter
        if (e.valueAt(e.FirstParameter) - start).Length <= (e.valueAt(e.LastParameter) - start).Length
        else e.LastParameter
    )
    t = App.Vector(e.tangentAt(u))
    if u == e.LastParameter:
        t = -t
    t.normalize()
    if up is None:
        up_v = App.Vector(0, 0, 1) if abs(t.z) < 0.9 else App.Vector(1, 0, 0)
    else:
        up_v = App.Vector(*up)
    y = up_v - t * up_v.dot(t)
    if y.Length < 1e-6:
        raise SkillError(
            errors.INVALID_PARAM,
            "'up' is parallel to the path at its start",
            hint="Give an 'up' direction that is not along the start of the path.",
        )
    y.normalize()
    x = t.cross(y)  # to the right when looking along the path with y up; radially outward on a helix
    return start, x, y, t


def _frame_placement(origin: Any, x: Any, y: Any, n: Any) -> Any:
    z = x.cross(y)  # = -n: a sketch frame must be right-handed; sweeps do not depend on the profile's facing
    m = App.Matrix(x.x, y.x, z.x, origin.x, x.y, y.y, z.y, origin.y, x.z, y.z, z.z, origin.z, 0, 0, 0, 1)
    return App.Placement(m)


def _frame_data(origin: Any, x: Any, y: Any, n: Any) -> Dict[str, Any]:
    return {"origin": geometry.vec(origin), "x": geometry.vec(x), "y": geometry.vec(y), "normal": geometry.vec(n)}


def _loops(shapes: Any) -> List[List[Any]]:
    """Split profile shapes into outer shapes and the holes nested in them (one level)."""
    from .sketch import _loop_face

    loops = profiles.all_segments(shapes)
    faces = [_loop_face(lp) for lp in loops]
    holes = set()
    for i, fi in enumerate(faces):
        for j, fj in enumerate(faces):
            if i != j and fj.Area > fi.Area and abs(fi.common(fj).Area - fi.Area) < 1e-6 * fi.Area:
                holes.add(i)
    if len(shapes) - len(holes) != 1:
        raise SkillError(
            errors.INVALID_PARAM,
            "a sweep profile must be one outline (optionally with holes inside it)",
            hint="Sweep separate outlines with separate sweep ops.",
        )
    outer = next(i for i in range(len(shapes)) if i not in holes)
    return [[shapes[outer]]] + [[shapes[i]] for i in sorted(holes)]


# ------------------------------------------------------------------ sweep


def sweep(ctx: Context, p: Dict[str, Any]) -> Any:
    spec = _path_spec(p)
    _check_path(spec)
    try:
        groups = _loops(p["shapes"])
    except profiles.ProfileError as e:
        raise SkillError(errors.INVALID_PARAM, str(e)) from None
    if p.get("body"):
        return _pd_sweep(ctx, p, spec)
    name = p.get("name")
    holes = groups[1:]
    obj = ctx.add("Part::Cut" if holes else "Part::Sweep", name, "Sweep")
    spec["up"] = _up(p)
    path = _make_path(ctx, obj.Name, spec)
    path.recompute()
    frame = _start_frame(path.Shape, spec["up"])
    pl = _frame_placement(*frame)

    def one(tag: str, shapes: Any) -> Any:
        sw = obj if not holes and tag == "" else ctx.doc.addObject("Part::Sweep", f"{obj.Name}{tag}")
        sk = ctx.doc.addObject("Sketcher::SketchObject", f"{obj.Name}{tag}_Profile")
        sk.Label = sk.Name
        sk.Placement = pl
        fill_sketch(sk, shapes)
        sw.Sections = [sk]
        sw.Spine = (path, [])
        sw.Solid = True
        sw.Frenet = "helix" in spec
        sw.Transition = "Right corner"
        ctx.own_helper(obj, sk)
        if sw is not obj:
            sw.Label = sw.Name
            ctx.own_helper(obj, sw)
        return sw

    ctx.own_helper(obj, path)
    if holes:
        outer = one("_Outer", groups[0])
        cutters = [one(f"_Hole{k}", g) for k, g in enumerate(holes)]
        obj.Base = outer
        if len(cutters) == 1:
            obj.Tool = cutters[0]
        else:
            fused = ctx.doc.addObject("Part::MultiFuse", f"{obj.Name}_Holes")
            fused.Shapes = cutters
            ctx.own_helper(obj, fused)
            obj.Tool = fused
    else:
        one("", groups[0])
    ctx.recompute()
    ctx.verify_solid(obj, "Sweep")
    return {
        "object": obj,
        "data": {"profile_frame": _frame_data(*frame), "path_length": geometry.num(path.Shape.Length)},
    }


def _pd_sweep(ctx: Context, p: Dict[str, Any], spec: Dict[str, Any]) -> Any:
    from . import partdesign

    bd = partdesign.get_body(ctx, p["body"])
    remove = p.get("mode", "add") == "remove"
    if remove:
        partdesign._require_material(bd, "cut")
    before = partdesign._volume(bd)
    obj = ctx.add("PartDesign::SubtractivePipe" if remove else "PartDesign::AdditivePipe", p.get("name"), "Sweep")
    spec["up"] = _up(p)
    path = _make_path(ctx, obj.Name, spec)
    _follow_body(path, bd, spec)  # path coordinates are body coordinates
    _store_spec(path, spec)
    path.recompute()
    binder = ctx.doc.addObject("PartDesign::SubShapeBinder", f"{obj.Name}_PathBinder")
    binder.Label = binder.Name
    bd.addObject(binder)
    binder.Support = [(path, ("",))]
    binder.recompute()
    frame = _start_frame(binder.Shape, spec["up"])
    sk = ctx.doc.addObject("Sketcher::SketchObject", f"{obj.Name}_Profile")
    sk.Label = sk.Name
    bd.addObject(sk)
    sk.MapMode = "Deactivated"
    sk.Placement = _frame_placement(*frame)
    fill_sketch(sk, p["shapes"])
    bd.addObject(obj)
    for helper in (path, binder, sk):
        ctx.own_helper(obj, helper)
    ctx.mark_consumes(binder, path)  # the path lies outside the body; the binder is what uses it
    obj.Profile = sk
    obj.Spine = (binder, [])
    obj.Mode = "Frenet" if "helix" in spec else "Standard"
    obj.Transition = "Right corner"
    partdesign.finish(ctx, bd, obj, before, remove)
    return {
        "object": obj,
        "data": {"profile_frame": _frame_data(*frame), "path_length": geometry.num(binder.Shape.Length)},
    }


# ------------------------------------------------------------------ editing

SWEEP_KEYS = ("path", "smooth", "corner_radius", "helix", "up", "shapes")


def sweep_parts(ctx: Context, obj: Any) -> Optional[Dict[str, Any]]:
    """Path object, binder and profile sketches of a sweep made by this skill (None if obj is not one)."""
    from ..document import _helpers

    helpers = [ctx.doc.getObject(n) for n in _helpers(obj)]
    paths = [h for h in helpers if h is not None and PATH_PROP in h.PropertiesList]
    if not paths:
        return None
    return {
        "path": paths[0],
        "binder": next((h for h in helpers if h is not None and h.TypeId == "PartDesign::SubShapeBinder"), None),
        "profiles": [h for h in helpers if h is not None and h.TypeId == "Sketcher::SketchObject"],
        "spec": json.loads(getattr(paths[0], PATH_PROP)),
    }


def set_sweep(ctx: Context, obj: Any, parts: Dict[str, Any], key: str, value: Any) -> None:
    from .. import validate

    spec, path = parts["spec"], parts["path"]
    if key != "shapes" and key != "up":
        if key == "helix" and "helix" not in spec or key in ("path", "smooth", "corner_radius") and "helix" in spec:
            raise SkillError(
                errors.INVALID_PARAM,
                f"'{obj.Name}' was swept along a {'helix' if 'helix' in spec else 'path'}; '{key}' does not apply",
                hint="To change the kind of path, delete the sweep and create it again.",
            )
    if key in ("path", "helix", "corner_radius", "up"):
        param = _catalog_param("sweep", key)
        msg = validate._check_value(param, value) if value is not None or key != "up" else None
        if msg:
            raise SkillError(errors.INVALID_PARAM, f"{obj.Name}: '{key}' {msg}")
    if key == "smooth":
        if bool(value) != spec["smooth"]:
            raise SkillError(
                errors.INVALID_PARAM,
                f"'smooth' cannot be toggled on '{obj.Name}'",
                hint="Delete the sweep and create it again with the other kind of path.",
            )
        return
    if key == "path":
        new = dict(spec, path=value)
        _check_path(new)
        path.Points = [App.Vector(*q) for q in value]
        spec = new
    elif key == "corner_radius":
        new = dict(spec, corner_radius=float(value))
        _check_path(new)
        path.FilletRadius = float(value)
        spec = new
    elif key == "helix":
        path.Radius, path.Pitch, path.Height = float(value["radius"]), float(value["pitch"]), float(value["height"])
        path.LocalCoord = "Left-handed" if value.get("left_handed") else "Right-handed"
        spec = dict(spec, helix=value)
        if parts["binder"] is not None:
            _follow_body(path, ctx.doc.getObject(spec["body"]), spec)
        else:
            path.Placement = App.Placement(
                App.Vector(*value.get("center", [0, 0, 0])), geometry.rotation_to(value.get("axis", [0, 0, 1]))
            )
    elif key == "up":
        spec = dict(
            spec, up=value if value is not None else (spec["helix"].get("axis", [0, 0, 1]) if "helix" in spec else None)
        )
    elif key == "shapes":
        _set_profile_shapes(obj, parts, value)
    _store_spec(path, spec)
    replace_profiles(ctx, parts)


def _set_profile_shapes(obj: Any, parts: Dict[str, Any], shapes: Any) -> None:
    from .. import validate

    msg = validate._check_value(_catalog_param("sweep", "shapes"), shapes)
    if msg:
        raise SkillError(errors.INVALID_PARAM, f"{obj.Name}: 'shapes' {msg}")
    groups = _loops(shapes)
    sketches = parts["profiles"]
    if obj.TypeId.startswith("PartDesign::"):
        fill_sketch(sketches[0], shapes)
        return
    if len(groups) != len(sketches):
        raise SkillError(
            errors.INVALID_PARAM,
            f"'{obj.Name}' has {len(sketches) - 1} hole(s) in its profile; keep the same number",
            hint="To add or remove holes, delete the sweep and create it again.",
        )
    for sk, g in zip(sketches, groups):
        fill_sketch(sk, g)


def replace_profiles(ctx: Context, parts: Dict[str, Any]) -> None:
    """Re-place the profile sketches at the (possibly moved) start of the path."""
    path = parts["path"]
    path.recompute()
    src = path
    if parts["binder"] is not None:
        parts["binder"].recompute()
        src = parts["binder"]
    frame = _start_frame(src.Shape, json.loads(getattr(path, PATH_PROP)).get("up"))
    for sk in parts["profiles"]:
        sk.Placement = _frame_placement(*frame)


HANDLERS = {"loft": loft, "sweep": sweep}

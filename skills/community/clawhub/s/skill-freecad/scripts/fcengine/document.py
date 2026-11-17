"""Document access, object lookup, recompute checks and object roles."""

from __future__ import annotations

import difflib
import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence

import FreeCAD as App

from . import errors, geometry
from .errors import SkillError

# Features whose links are *inputs* that get consumed into their result.
CONSUMER_TYPES = {
    "Part::Cut",
    "Part::Fuse",
    "Part::MultiFuse",
    "Part::Common",
    "Part::MultiCommon",
    "Part::Fillet",
    "Part::Chamfer",
    "Part::Thickness",
    "Part::Extrusion",
    "Part::Revolution",
    "Part::Offset",
    "Part::Loft",
    "Part::Sweep",
    "Part::Section",
}
SKIP_TYPES_PREFIX = ("App::Origin", "App::Line", "App::Plane", "App::Point")
SEL_PROP = "FCSkillSelector"  # JSON {"param": "edges"|"open_faces", "value": selector}
HELPERS_PROP = "FCSkillHelpers"  # helper objects owned by this feature
CONSUMES_PROP = "FCSkillConsumes"  # extra consumption marker (scale clones)

# Hints for recompute failures, by feature type.
FAILURE_HINTS = {
    "Part::Fillet": "The radius is probably too large for the selected edges or adjacent faces. Try a smaller radius or fewer edges (inspect with topology=true shows edge lengths).",
    "Part::Chamfer": "The chamfer size is probably too large for the selected edges. Try a smaller size or fewer edges.",
    "Part::Thickness": "The wall thickness may be too large for the smallest feature, or the shape too complex for an offset. Try a thinner wall, or shell before adding fillets.",
    "Part::Cut": "Coincident or tangent faces between base and tool often break booleans. Extend the tool slightly past the faces it cuts.",
    "Part::MultiFuse": "Coincident or tangent faces often break booleans. Overlap the objects slightly instead of touching exactly.",
    "Part::MultiCommon": "The objects may not overlap.",
    "Part::Extrusion": "The profile may be self-intersecting or degenerate.",
    "Part::Revolution": "The profile may cross or touch the revolution axis, or be self-intersecting.",
    "PartDesign::Fillet": "The radius is probably too large for the selected edges or adjacent faces. Try a smaller radius or fewer edges.",
    "PartDesign::Chamfer": "The chamfer size is probably too large for the selected edges. Try a smaller size or fewer edges.",
    "PartDesign::Thickness": "The wall thickness may be too large for the smallest feature. Try a thinner wall, or shell before adding fillets.",
    "PartDesign::Pad": "The profile must be closed, and added material must touch the existing solid (a body is one solid).",
    "PartDesign::Pocket": "The profile must be closed and overlap the part; pockets cut against the plane normal unless 'reversed'.",
    "PartDesign::Hole": "Holes start on the profile plane ('offset') and drill against its normal unless 'reversed'.",
    "PartDesign::Revolution": "The profile may cross the axis, or the result may not touch the existing solid.",
    "PartDesign::Groove": "The profile may cross the axis or miss the part.",
}


def type_name(obj: Any) -> str:
    proxy = getattr(obj, "Proxy", None)
    ptype = getattr(proxy, "Type", None) if proxy is not None else None
    if obj.TypeId == "Part::FeaturePython" and isinstance(ptype, str):
        return f"Draft::{ptype}"
    return obj.TypeId


def _helpers(obj: Any) -> List[str]:
    return list(getattr(obj, HELPERS_PROP, []) or [])


def consumes(consumer: Any, obj: Any) -> bool:
    if consumer.TypeId in CONSUMER_TYPES:
        return True
    if obj.Name in _helpers(consumer):  # helper geometry owned by a feature (profiles, FEM load directions)
        return True
    if obj.Name in (getattr(consumer, CONSUMES_PROP, []) or []):
        return True
    if type_name(consumer) == "Draft::Array" and getattr(consumer, "Base", None) == obj:
        return True
    if consumer.TypeId == "App::Link" and getattr(consumer, "LinkedObject", None) == obj:
        parent = consumer.getParentGeoFeatureGroup() if hasattr(consumer, "getParentGeoFeatureGroup") else None
        if parent is not None and parent.TypeId == "Assembly::AssemblyObject":
            return True  # a part placed in an assembly
    return False


def role(obj: Any) -> str:
    """'result', 'intermediate', 'parameters' or 'other'."""
    if obj.TypeId.startswith("Spreadsheet::"):
        return "parameters"
    if not geometry.is_part_shape(obj):
        return "other"
    parent = obj.getParentGeoFeatureGroup() if hasattr(obj, "getParentGeoFeatureGroup") else None
    if parent is not None and parent.TypeId == "PartDesign::Body":
        return "intermediate"
    if any(consumes(c, obj) for c in obj.InList):
        return "intermediate"
    return "result"


def visible_objects(doc: Any) -> List[Any]:
    return [o for o in doc.Objects if not o.TypeId.startswith(SKIP_TYPES_PREFIX)]


def object_entry(obj: Any, detailed: bool = False, validity: bool = True) -> Dict[str, Any]:
    entry: Dict[str, Any] = {"name": obj.Name}
    if obj.Label != obj.Name:
        entry["label"] = obj.Label
    entry["type"] = type_name(obj)
    entry["role"] = role(obj)
    inputs = list(
        dict.fromkeys(
            o.Name
            for o in obj.OutList
            if not o.TypeId.startswith(SKIP_TYPES_PREFIX) and not o.TypeId.startswith("Spreadsheet::")
        )
    )
    if inputs:
        entry["inputs"] = inputs
    bad = [s for s in obj.State if s in ("Invalid", "Error")]
    if bad:
        entry["state"] = bad
        entry["error"] = obj.getStatusString()
    if geometry.is_part_shape(obj):
        entry.update(geometry.summary(obj.Shape, detailed=detailed, validity=validity))
    return entry


class Context:
    """State shared by the operations of one request."""

    def __init__(self, doc: Any, root: Path, doc_path: Optional[Path] = None) -> None:
        self.doc = doc
        self.root = root
        self.doc_path = doc_path
        self.step = -1
        self.warnings: List[Dict[str, Any]] = []
        self.step_warnings: List[str] = []
        self.pending_exports: List[Dict[str, Any]] = []
        self.mutated = False
        self.gui_before: Optional[Dict[str, Any]] = None  # GUI data of the file before the request
        self.appearance_changed: set = set()  # objects whose colour/material this request set
        self.shapes_before: Dict[str, Any] = {}  # shape fingerprints at the start of the request
        self.read_only = False  # the request has no step that changes the document

    # -------------------------------------------------------------- messages
    def warn(self, code: str, message: str) -> None:
        self.step_warnings.append(f"{code}: {message}")
        self.warnings.append({"step": self.step, "code": code, "message": message})

    # -------------------------------------------------------------- lookup
    def find(self, ref: str) -> Optional[Any]:
        doc = self.doc
        obj = doc.getObject(ref)
        if obj is None:
            matches = doc.getObjectsByLabel(ref)
            obj = matches[0] if matches else None
        if obj is None and " " in ref:
            obj = doc.getObject(ref.replace(" ", "_"))
        return obj

    def get(self, ref: str, need_shape: bool = True) -> Any:
        obj = self.find(ref)
        if obj is None:
            names = [o.Name for o in visible_objects(self.doc)]
            labels = [o.Label for o in visible_objects(self.doc)]
            close = difflib.get_close_matches(ref, list(dict.fromkeys(names + labels)), n=3, cutoff=0.5)
            raise SkillError(
                errors.OBJECT_NOT_FOUND,
                f"No object named '{ref}' in the document",
                hint=(f"Did you mean {close}? " if close else "")
                + "Object names are case-sensitive; 'inspect' lists the document.",
                details={"available": names[:50]},
            )
        if need_shape and not geometry.is_part_shape(obj):
            raise SkillError(errors.INVALID_PARAM, f"'{ref}' ({obj.TypeId}) has no shape and cannot be used here")
        return obj

    # -------------------------------------------------------------- creation
    def add(self, type_id: str, name: Optional[str], default: str) -> Any:
        if name is not None:
            clash = self.doc.getObject(name) or (self.doc.getObjectsByLabel(name) or [None])[0]
            if clash is not None:
                raise SkillError(
                    errors.NAME_CONFLICT,
                    f"An object named '{name}' already exists ({type_name(clash)})",
                    hint="Pick another name, use 'set' to modify the existing object, or delete it first. "
                    'To rebuild the whole document from scratch, resend the request with "new": true.',
                )
        obj = self.doc.addObject(type_id, name or default)
        if name is not None and obj.Name != name:  # FreeCAD sanitised/renamed it
            self.doc.removeObject(obj.Name)
            raise SkillError(
                errors.NAME_CONFLICT, f"FreeCAD cannot use '{name}' as an object name", hint="Use another identifier."
            )
        obj.Label = obj.Name
        self.mutated = True
        return obj

    def own_helper(self, owner: Any, helper: Any) -> None:
        if HELPERS_PROP not in owner.PropertiesList:
            owner.addProperty(
                "App::PropertyStringList", HELPERS_PROP, "FCSkill", "Helper objects created with this feature"
            )
            owner.setEditorMode(HELPERS_PROP, 2)
        setattr(owner, HELPERS_PROP, _helpers(owner) + [helper.Name])

    def set_selector(self, obj: Any, param: str, value: Any) -> None:
        if SEL_PROP not in obj.PropertiesList:
            obj.addProperty("App::PropertyString", SEL_PROP, "FCSkill", "Selector re-evaluated when inputs change")
        setattr(obj, SEL_PROP, json.dumps({"param": param, "value": value}))

    def mark_consumes(self, obj: Any, consumed: Any) -> None:
        if CONSUMES_PROP not in obj.PropertiesList:
            obj.addProperty("App::PropertyStringList", CONSUMES_PROP, "FCSkill", "Objects this feature replaces")
            obj.setEditorMode(CONSUMES_PROP, 2)
        setattr(obj, CONSUMES_PROP, [consumed.Name])

    # -------------------------------------------------------------- values
    def assign(self, obj: Any, prop: str, value: Any) -> None:
        """Assign a number or an '=expression' to a property."""
        if isinstance(value, str) and value.startswith("="):
            try:
                obj.setExpression(prop, value[1:].strip())
            except Exception as e:
                raise SkillError(
                    errors.INVALID_EXPRESSION,
                    f"Invalid expression for {obj.Name}.{prop}: {value!r}: {e}",
                    hint="Expressions use FreeCAD syntax, e.g. '=Params.width * 2' or '=Plate.Length - 10'. Parameters are created with set_params.",
                ) from None
        else:
            setattr(obj, prop, value)

    # -------------------------------------------------------------- recompute
    def recompute(self) -> None:
        """Recompute the document; raise a diagnosable error on failure."""
        self.doc.recompute()
        failed = [o for o in self.doc.Objects if "Invalid" in o.State or "Error" in o.State]
        if not failed:
            check_expression_units(self.doc)
            return
        # The root cause is the failed object with the fewest dependencies.
        failed.sort(key=lambda o: len(o.OutListRecursive))
        first = failed[0]
        msg = first.getStatusString() or "recompute failed"
        details: Dict[str, Any] = {"object": first.Name, "type": type_name(first), "freecad_message": msg}
        if len(failed) > 1:
            details["also_failed"] = [o.Name for o in failed[1:]]
        hint = FAILURE_HINTS.get(first.TypeId) or (
            "Check this object's dimensions (positive, in mm) and any expressions it uses; "
            "'inspect' with target shows its properties and expressions."
        )
        if "edge link" in msg.lower() or "missing element" in msg.lower():
            # The edges/faces this feature was built on no longer exist (topological naming), not a size problem.
            hint = (
                f"'{first.Name}' refers to edges or faces by index, and an upstream change removed or renumbered "
                f"them. Set its 'edges' (or 'open_faces') again with 'set', preferably as a selector such as "
                "'|Z and %LINE', which is re-evaluated after every edit."
            )
        elif first.TypeId in ("Part::Fillet", "Part::Chamfer", "PartDesign::Fillet", "PartDesign::Chamfer"):
            hint = (hint or "") + _edge_size_hint(first)
        raise SkillError(
            errors.RECOMPUTE_FAILED,
            f"{first.Name} ({type_name(first)}) failed to compute: {msg}",
            hint=hint,
            details=details,
        )

    def reselect(self) -> None:
        """Re-evaluate stored selectors after upstream changes."""
        tracked = [o for o in self.doc.Objects if SEL_PROP in o.PropertiesList]
        tracked.sort(key=lambda o: len(o.OutListRecursive))
        for obj in tracked:
            self.doc.recompute()
            spec = json.loads(getattr(obj, SEL_PROP))
            apply_selector(obj, spec["param"], spec["value"], None)
        if any("FCSkillPath" in o.PropertiesList for o in self.doc.Objects):
            from .ops.sweeps import sync_body_paths

            sync_body_paths(self)
        if any("FCSkillJoint" in o.PropertiesList for o in self.doc.Objects):
            from .ops.assembly import reselect_joints

            self.doc.recompute()
            reselect_joints(self)

    # -------------------------------------------------------------- checks
    def verify_solid(self, obj: Any, what: str) -> None:
        shape = obj.Shape
        if shape.isNull() or not shape.Solids:
            raise SkillError(
                errors.EMPTY_RESULT,
                f"{what} '{obj.Name}' produced no solid",
                hint=FAILURE_HINTS.get(obj.TypeId, "Check the inputs' positions and sizes with inspect."),
                details={"bbox": geometry.bbox(shape)},
            )
        if not geometry.is_valid(shape):
            hint = FAILURE_HINTS.get(obj.TypeId, "Check for self-intersections or degenerate inputs.")
            if obj.TypeId in ("Part::Fillet", "Part::Chamfer", "PartDesign::Fillet", "PartDesign::Chamfer"):
                hint += _edge_size_hint(obj)
            raise SkillError(errors.GEOMETRY_INVALID, f"{what} '{obj.Name}' produced invalid geometry", hint=hint)
        if shape.Volume <= 1e-9:
            raise SkillError(errors.EMPTY_RESULT, f"{what} '{obj.Name}' has zero volume")


def _declared_unit(obj: Any, prop: str) -> Any:
    """Unit a property is declared with (its current value can carry a wrong unit)."""
    try:
        ptype = obj.getTypeIdOfProperty(prop)
    except Exception:
        return None
    if "Angle" in ptype:
        return App.Units.Angle
    if "Length" in ptype or "Distance" in ptype:
        return App.Units.Length
    return None


def check_expression_units(doc: Any) -> None:
    """Reject expressions whose unit does not match the property.

    FreeCAD silently accepts an incompatible quantity: an angle parameter
    ("15 deg") bound to a box Length makes the Length "15 deg", used as 15 mm.
    """
    dimensionless = App.Units.Unit()
    for o in doc.Objects:
        if o.TypeId.startswith("Spreadsheet::"):
            continue
        for prop, expr in o.ExpressionEngine:
            if "." in prop:
                continue
            want = _declared_unit(o, prop)
            if want is None:
                continue
            try:
                value = o.evalExpression(expr)
            except Exception:
                continue
            unit = getattr(value, "Unit", None)
            if unit is None or unit == dimensionless or unit == want:
                continue
            raise SkillError(
                errors.INVALID_EXPRESSION,
                f"{o.Name}.{prop} = {expr} gives {value} but {prop} expects a {_unit_kind(want)}",
                hint="Use a parameter with a matching unit (or a plain number, which means mm/deg), "
                "or convert explicitly, e.g. '=Params.angle / 1 deg * 1 mm'.",
                details={"object": o.Name, "property": prop, "expression": expr},
            )


def _unit_kind(unit: Any) -> str:
    text = str(unit)
    return text[text.rfind("[") + 1 : text.rfind("]")].lower() if "[" in text else text


def _face_width_across(face: Any, edge: Any) -> float:
    """Width of ``face`` measured perpendicular to ``edge`` (planar faces), else its smallest extent."""
    pts = [v.Point for v in face.Vertexes]
    for e in face.Edges:
        try:
            pts.extend(e.discretize(12))
        except Exception:
            pass
    try:
        u0, u1, v0, v1 = face.ParameterRange
        normal = face.normalAt((u0 + u1) / 2, (v0 + v1) / 2)
        d = edge.Vertexes[-1].Point - edge.Vertexes[0].Point
        if face.Surface.__class__.__name__ == "Plane" and d.Length > 1e-9:
            perp = normal.cross(d.normalize())
            vals = [p.dot(perp) for p in pts]
            return max(vals) - min(vals)
    except Exception:
        pass
    bb = face.BoundBox
    ext = [x for x in (bb.XLength, bb.YLength, bb.ZLength) if x > 1e-6]
    return min(ext) if ext else 0.0


def _edge_size_hint(obj: Any) -> str:
    """Explain what limits a fillet/chamfer: edge lengths and the faces between edges."""
    try:
        if obj.TypeId.startswith("PartDesign::"):
            shape = obj.Base[0].Shape
            selected = [int(n[4:]) for n in obj.Base[1] if n.startswith("Edge")]
            r = float(getattr(obj, "Radius", getattr(obj, "Size", 0)).Value)
        else:
            shape = obj.Base.Shape
            selected = [e[0] for e in obj.Edges]
            r = max(e[1] for e in obj.Edges)
        edges = shape.Edges
        msg = f" Requested size {geometry.num(r)} mm; the shortest selected edge is {geometry.num(min(edges[i - 1].Length for i in selected))} mm."
        # Faces adjacent to selected edges, and how many selected edges each one borders.
        per_face: Dict[int, List[int]] = {}
        for fi, f in enumerate(shape.Faces, start=1):
            for i in selected:
                if any(edges[i - 1].isSame(fe) for fe in f.Edges):
                    per_face.setdefault(fi, []).append(i)
        best = None
        for fi, eids in per_face.items():
            width = _face_width_across(shape.Faces[fi - 1], edges[eids[0] - 1])
            limit = width / 2 if len(eids) >= 2 else width
            if best is None or limit < best[0]:
                best = (limit, fi, width, len(eids))
        if best is not None:
            limit, fi, width, n = best
            both = f", and {n} selected edges border it" if n >= 2 else ""
            msg += (
                f" The narrowest adjacent face (Face{fi}) is {geometry.num(width)} mm wide{both}, "
                f"so the size must be below about {geometry.num(limit)} mm."
            )
        return msg
    except Exception:
        return ""


def apply_selector(obj: Any, param: str, value: Any, size: Optional[float]) -> List[int]:
    """(Re)apply an edge/face selection to a fillet, chamfer or shell (Part or PartDesign)."""
    pd = obj.TypeId.startswith("PartDesign::")
    if param == "edges":
        base = obj.Base[0] if pd else obj.Base
        if size is None and not pd:
            size = obj.Edges[0][1] if obj.Edges else 1.0
        idx = geometry.select_edges(base.Shape, value, filletable=True)
        if not idx:
            raise SkillError(
                errors.INVALID_SELECTOR,
                f"Edge selector {value!r} matches no filletable edge of '{base.Name}'",
                hint="Use inspect with topology=true on the base object to see its edges.",
            )
        if pd:
            obj.Base = (base, [f"Edge{i}" for i in idx])
        else:
            obj.Edges = [(i, size, size) for i in idx]
        return idx
    if param == "open_faces":
        base = obj.Base[0] if pd else obj.Faces[0]
        idx = geometry.select_faces(base.Shape, value)
        if not idx:
            raise SkillError(
                errors.INVALID_SELECTOR,
                f"Face selector {value!r} matches no face of '{base.Name}'",
                hint="Use inspect with topology=true on the base object to see its faces.",
            )
        if pd:
            obj.Base = (base, [f"Face{i}" for i in idx])
        else:
            obj.Faces = (base, [f"Face{i}" for i in idx])
        return idx
    raise ValueError(param)


# ------------------------------------------------------------------ files


def open_document(path: Path, new: bool) -> Any:
    if path.exists() and not new:
        try:
            return App.openDocument(str(path))
        except Exception as e:
            raise SkillError(
                errors.INVALID_REQUEST,
                f"Cannot open '{path.name}': {e}",
                hint="Is it a valid FreeCAD document? Use new=true to replace it.",
            ) from None
    doc = App.newDocument(_doc_name(path))
    return doc


def _doc_name(path: Path) -> str:
    stem = "".join(c if c.isalnum() else "_" for c in path.stem) or "Model"
    return stem if stem[0].isalpha() else "D" + stem


APPEARANCE_PROP = "FCSkillAppearance"


def body_features(body: Any) -> List[Any]:
    """Features of a PartDesign body that the GUI draws with their own appearance."""
    return [f for f in body.Group if geometry.is_part_shape(f) and f.TypeId.startswith("PartDesign::")]


def appearances(doc: Any) -> Dict[str, Dict[str, Any]]:
    """Custom colours set with the 'material' op, by object name.

    A body's colour is also given to its features: the GUI draws a body through its tip feature, and copies
    a body's colour to the features only when it is changed interactively, not when a file is loaded.
    """
    out = {}
    for o in doc.Objects:
        raw = getattr(o, APPEARANCE_PROP, "") if APPEARANCE_PROP in o.PropertiesList else ""
        if raw:
            a = json.loads(raw)
            if a.get("color") is not None:
                out[o.Name] = a
                if o.TypeId == "PartDesign::Body":
                    for f in body_features(o):
                        out.setdefault(f.Name, a)
    return out


def expand_changed(doc: Any, names: Any) -> set:
    """Objects whose GUI appearance must be rewritten: the changed ones, plus the features of changed bodies."""
    out = set(names)
    for n in names:
        o = doc.getObject(n)
        if o is not None and o.TypeId == "PartDesign::Body":
            out |= {f.Name for f in body_features(o)}
    return out


def save_document(doc: Any, path: Path, gui: Optional[Dict[str, Any]] = None) -> None:
    """Atomic save without FreeCAD backup files, with GUI data (see guidata).

    gui: {"captured": GUI data of the file before the request, "visibility": {...}, "changed": {...}}.
    """
    from . import guidata

    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(f".{path.stem}.fcskill-tmp.FCStd")
    doc.Label = path.stem
    doc.saveCopy(str(tmp))
    gui = gui or {}
    try:
        xml = guidata.build(
            gui.get("captured"),
            {o.Name for o in doc.Objects},
            gui.get("visibility", {}),
            appearances(doc),
            expand_changed(doc, gui.get("changed", ())),
        )
        guidata.write(tmp, xml, gui.get("captured"))
    except Exception:
        os.remove(tmp)
        raise
    os.replace(tmp, path)


def apply_visibility(doc: Any) -> Dict[str, bool]:
    """Show only result objects when the file is opened in the FreeCAD GUI.

    Headless documents carry no GUI state, so without this every
    intermediate (tools, sketches, earlier stages) is drawn on top of the
    finished part. The choice is stored twice: in each object's Visibility
    (Document.xml) and in GuiDocument.xml, which the GUI actually uses (see
    guidata). Returns the managed objects and their visibility.
    """
    tips = set()
    managed: Dict[str, bool] = {}
    for o in doc.Objects:
        if o.TypeId == "PartDesign::Body" and role(o) == "result" and o.Tip is not None:
            tips.add(o.Tip.Name)  # the GUI displays a body through its tip feature
    for o in doc.Objects:
        if "Visibility" not in o.PropertiesList or o.TypeId.startswith("TechDraw::"):
            continue
        parent = o.getParentGeoFeatureGroup() if hasattr(o, "getParentGeoFeatureGroup") else None
        in_assembly = parent is not None and parent.TypeId == "Assembly::AssemblyObject" and o.TypeId == "App::Link"
        want = role(o) == "result" or o.Name in tips or in_assembly
        if o.Visibility != want:
            o.Visibility = want
        managed[o.Name] = want
    return managed


def close_document(doc: Any) -> None:
    try:
        App.closeDocument(doc.Name)
    except Exception:
        pass


def topo_sorted(objs: Sequence[Any]) -> List[Any]:
    return sorted(objs, key=lambda o: len(o.OutListRecursive))

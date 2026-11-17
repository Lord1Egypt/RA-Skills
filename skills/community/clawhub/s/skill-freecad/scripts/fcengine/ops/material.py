"""Materials and colours of finished parts.

A part gets FreeCAD's own material (ShapeMaterial: density, mechanical data and
an appearance from the built-in library) and, when useful, a custom colour.
Probed on FreeCAD 1.1:

- ShapeMaterial is stored as a library UUID only, so a material created on the
  fly does not survive saving ("Material not found"); custom colours are
  therefore written to GuiDocument.xml as legacy ShapeColor (see guidata).
- The library's plastics have densities but no appearance (they would show
  FreeCAD's default grey-blue), and there is no rubber: presets add colours.
"""

from __future__ import annotations

import json
from typing import Any, Dict, List, Optional

from .. import errors, geometry, matdata
from ..document import APPEARANCE_PROP, Context
from ..errors import SkillError

PRESETS = matdata.PRESETS  # one table for materials, masses and stress analysis (see matdata)


def _library() -> Dict[str, Any]:
    """Library materials by lower-case name (the one with physical data wins on duplicates)."""
    import Materials

    mm = Materials.MaterialManager()
    out: Dict[str, Any] = {}
    for uuid in mm.Materials:
        try:
            m = mm.getMaterial(uuid)
        except Exception:
            continue
        key = m.Name.lower()
        if key not in out or (_density(m) is not None and _density(out[key]) is None):
            out[key] = m
    return out


def _density(m: Any) -> Optional[float]:
    """g/cm3 from a library material, or None."""
    try:
        raw = dict(m.PhysicalProperties).get("Density")
    except Exception:
        return None
    if not raw:
        return None
    try:
        import FreeCAD as App

        return float(App.Units.Quantity(raw).getValueAs("g/cm^3"))
    except Exception:
        return None


def _color(value: Any) -> List[float]:
    if isinstance(value, str):
        h = value.lstrip("#")
        return [int(h[i : i + 2], 16) / 255.0 for i in (0, 2, 4)]
    return [float(c) for c in value]


def resolve(name: str, lib: Dict[str, Any]) -> Dict[str, Any]:
    key = matdata.canonical(name)
    if key is not None:
        preset = PRESETS[key]
        mat = lib.get(preset.library.lower()) if preset.library else None
        return {
            "material": key,
            "library": mat.Name if mat is not None else None,
            "object": mat,
            "color": preset.color,
            "transparency": matdata.TRANSPARENCY.get(key, 0),
            "density": preset.density or (_density(mat) if mat is not None else None),
        }
    mat = lib.get(name.strip().lower())
    if mat is None:
        import difflib

        close = difflib.get_close_matches(name.strip().lower(), list(PRESETS) + list(lib), n=4, cutoff=0.5)
        raise SkillError(
            errors.INVALID_PARAM,
            f"Unknown material '{name}'",
            hint=(f"Did you mean {close}? " if close else "") + f"Presets: {sorted(PRESETS)}; or any FreeCAD "
            "library material name, e.g. 'Steel-C45E'.",
        )
    return {
        "material": mat.Name,
        "library": mat.Name,
        "object": mat,
        "color": None,
        "transparency": 0,
        "density": _density(mat),
    }


def _owner(ctx: Context, obj: Any) -> Any:
    """The object that carries the material: a body for its features, the source of an assembly link."""
    from .partdesign import body_of

    if obj.TypeId == "App::Link" and getattr(obj, "LinkedObject", None) is not None:
        ctx.warn(
            "REDIRECTED",
            f"'{obj.Name}' is a link to '{obj.LinkedObject.Name}'; the material was set on "
            f"'{obj.LinkedObject.Name}' (every instance shows it)",
        )
        return obj.LinkedObject
    body = body_of(obj)
    if body is not None:
        ctx.warn("REDIRECTED", f"'{obj.Name}' is a feature of body '{body.Name}'; the material was set on the body")
        return body
    if obj.TypeId == "Assembly::AssemblyObject":
        raise SkillError(
            errors.INVALID_PARAM,
            f"'{obj.Name}' is an assembly; give its parts",
            hint="Materials belong to parts: name the parts (or their source objects) in 'targets'.",
        )
    if "ShapeMaterial" not in obj.PropertiesList:
        raise SkillError(errors.INVALID_PARAM, f"'{obj.Name}' ({obj.TypeId}) cannot carry a material")
    return obj


def material(ctx: Context, p: Dict[str, Any]) -> Dict[str, Any]:
    if "material" not in p and "color" not in p:
        raise SkillError(errors.INVALID_REQUEST, "Give 'material', 'color', or both")
    spec: Dict[str, Any] = {
        "material": None,
        "library": None,
        "object": None,
        "color": None,
        "transparency": 0,
        "density": None,
    }
    if "material" in p:
        spec = resolve(p["material"], _library())
    if "color" in p:
        spec["color"] = _color(p["color"])
    if "transparency" in p:
        spec["transparency"] = int(p["transparency"])
    records = []
    for ref in p["targets"]:
        obj = _owner(ctx, ctx.get(ref, need_shape=False))
        if spec["object"] is not None:
            obj.ShapeMaterial = spec["object"]
        if APPEARANCE_PROP not in obj.PropertiesList:
            obj.addProperty("App::PropertyString", APPEARANCE_PROP, "FCSkill", "Material and colour set by the skill")
            obj.setEditorMode(APPEARANCE_PROP, 2)
        old = json.loads(getattr(obj, APPEARANCE_PROP) or "{}")
        new = {k: spec[k] for k in ("material", "library", "color", "transparency", "density")}
        if "material" not in p:  # colour only: keep the material chosen before
            new.update({k: old.get(k) for k in ("material", "library", "density")})
        setattr(obj, APPEARANCE_PROP, json.dumps(new))
        ctx.appearance_changed.add(obj.Name)
        rec: Dict[str, Any] = {"object": obj.Name, "material": new["material"]}
        if new["library"]:
            rec["freecad_material"] = new["library"]
        if new["color"] is not None:
            rec["color"] = [geometry.num(c, 3) for c in new["color"]]
        if new["density"]:
            rec["density_g_cm3"] = new["density"]
            if geometry.is_part_shape(obj) and not obj.Shape.isNull() and obj.Shape.Solids:
                rec["mass_g"] = geometry.num(obj.Shape.Volume / 1000.0 * new["density"], 2)
        records.append(rec)
    ctx.mutated = True
    return {"data": {"parts": records}}


def render_color(obj: Any) -> Optional[List[float]]:
    """Colour for the skill's own renders: the custom colour, else the material's look, else None."""
    if APPEARANCE_PROP in obj.PropertiesList and getattr(obj, APPEARANCE_PROP):
        a = json.loads(getattr(obj, APPEARANCE_PROP))
        if a.get("color") is not None:
            return list(a["color"])
    try:
        m = obj.ShapeMaterial
        if m is None or m.Name == "Default":
            return None
        ap = dict(m.AppearanceProperties)
    except Exception:
        return None

    def rgb(key: str) -> List[float]:
        raw = ap.get(key, "(0, 0, 0, 1)").strip("()")
        return [float(x) for x in raw.split(",")[:3]]

    if "DiffuseColor" not in ap:
        return None
    d, s = rgb("DiffuseColor"), rgb("SpecularColor") if "SpecularColor" in ap else [0.0, 0.0, 0.0]
    # A metal like steel is mostly specular (dark diffuse, bright specular); a Lambert renderer needs a body
    # colour, so add specular in proportion to how dark the diffuse colour is (brass keeps its own hue).
    w = 0.5 * (1.0 - max(d))
    return [min(1.0, dc + w * sc) for dc, sc in zip(d, s)]


def density_of(obj: Any) -> Optional[float]:
    """g/cm3 of a part's assigned material, or None."""
    if APPEARANCE_PROP in obj.PropertiesList and getattr(obj, APPEARANCE_PROP):
        dens = json.loads(getattr(obj, APPEARANCE_PROP)).get("density")
        if dens:
            return float(dens)
    try:
        m = obj.ShapeMaterial
        return _density(m) if m is not None and m.Name != "Default" else None
    except Exception:
        return None


HANDLERS = {"material": material}

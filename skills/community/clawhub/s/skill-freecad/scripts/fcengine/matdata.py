"""Material data (pure Python): the one table behind the 'material' op, 'measure' masses and 'fem_static'.

Each preset names the FreeCAD library material that carries its look and data (if there is one), a default
colour for the skill's renders, and a density. Presets that describe a definite grade also carry the
mechanical data a stress analysis needs. Generic ones ("steel", "aluminium") do not: yield strength varies
several-fold between grades, so 'fem_static' asks for a grade instead of guessing.

Values are typical room-temperature handbook figures, for estimates only. Printed plastics are anisotropic
and weaker between layers.
"""

from __future__ import annotations

from typing import Dict, List, NamedTuple, Optional


class Material(NamedTuple):
    library: Optional[str]  # FreeCAD library material name
    color: Optional[List[float]]  # default render colour; None = the library material's look
    density: Optional[float]  # g/cm3
    youngs_mpa: Optional[float] = None
    poisson: Optional[float] = None
    yield_mpa: Optional[float] = None

    @property
    def structural(self) -> bool:
        return None not in (self.density, self.youngs_mpa, self.poisson, self.yield_mpa)


_ALU = [0.78, 0.79, 0.81]
_STEEL = [0.60, 0.61, 0.63]

PRESETS: Dict[str, Material] = {
    "steel": Material("Steel-Generic", None, 7.85),
    "steel_s235": Material("Steel-Generic", _STEEL, 7.85, 210000, 0.30, 235),
    "steel_s355": Material("Steel-Generic", _STEEL, 7.85, 210000, 0.30, 355),
    "stainless_steel": Material("AusteniticStainlessSteel", [0.72, 0.73, 0.75], 8.0),
    "stainless_304": Material("AusteniticStainlessSteel", [0.72, 0.73, 0.75], 8.0, 193000, 0.29, 215),
    "cast_iron": Material("GrayCastIron", [0.30, 0.30, 0.31], 7.2),
    "aluminium": Material("Aluminum-Generic", _ALU, 2.7),
    "aluminium_6061": Material("Aluminum-6061-T6", _ALU, 2.7, 68900, 0.33, 276),
    "aluminium_7075": Material("Aluminum-7075-T6", _ALU, 2.81, 71700, 0.33, 503),
    "aluminium_5754": Material("Aluminum-Generic", _ALU, 2.67, 70000, 0.33, 80),
    "titanium": Material("Ti-6Al-4V", [0.55, 0.55, 0.58], 4.43, 113800, 0.34, 880),
    "copper": Material("Copper-Generic", None, 8.96),
    "brass": Material("Brass", None, 8.5, 100000, 0.34, 200),
    "bronze": Material("Bronze", None, 8.8),
    "gold": Material("Gold", None, 19.3),
    "silver": Material("Silver", None, 10.5),
    "chrome": Material("Chrome", None, None),
    "pla": Material("PLA-Generic", [0.92, 0.92, 0.90], 1.24, 3500, 0.36, 50),
    "abs": Material("ABS-Generic", [0.18, 0.18, 0.19], 1.04, 2200, 0.35, 40),
    "petg": Material("PET-Generic", [0.80, 0.88, 0.93], 1.27, 2100, 0.38, 45),
    "nylon": Material("PA6-Generic", [0.93, 0.92, 0.87], 1.15),
    "nylon_pa12": Material(None, [0.93, 0.92, 0.87], 1.01, 1700, 0.40, 45),
    "pom": Material("POM-Copolymer-Generic", [0.95, 0.95, 0.93], 1.41),
    "polypropylene": Material("PP-Generic", [0.90, 0.90, 0.88], 0.92),
    "polycarbonate": Material("PC-Molded", [0.85, 0.90, 0.95], 1.2),
    "acrylic": Material("PMMA-Generic", [0.85, 0.93, 0.97], 1.17),
    "ptfe": Material("PTFE-Generic", [0.97, 0.97, 0.96], 2.07),
    "pvc": Material("PVC-Generic", [0.75, 0.76, 0.78], 1.38),
    "rubber": Material(None, [0.07, 0.07, 0.07], 1.15),
    "glass": Material("Glass-Generic", [0.80, 0.90, 0.95], 2.52),
    "wood": Material("Wood-Generic", None, 0.7),
    "concrete": Material("Concrete-Generic", None, 2.4),
    "default": Material("Default", None, None),
}
TRANSPARENCY = {"glass": 70, "acrylic": 60}
ALIASES = {
    "aluminum": "aluminium",
    "aluminum_6061": "aluminium_6061",
    "aluminium_6061_t6": "aluminium_6061",
    "aluminum_6061_t6": "aluminium_6061",
    "aluminum_7075": "aluminium_7075",
    "aluminium_7075_t6": "aluminium_7075",
    "aluminum_5754": "aluminium_5754",
    "titanium_gr5": "titanium",
    "ti_6al_4v": "titanium",
    "s235": "steel_s235",
    "s355": "steel_s355",
    "stainless": "stainless_steel",
    "inox": "stainless_steel",
    "stainless_steel_304": "stainless_304",
    "plastic": "abs",
    "pa": "nylon",
    "pa6": "nylon",
    "pa12": "nylon_pa12",
    "pet": "petg",
    "pp": "polypropylene",
    "pc": "polycarbonate",
    "pmma": "acrylic",
    "plexiglass": "acrylic",
    "wood_oak": "wood",
}


def canonical(name: str) -> Optional[str]:
    """Preset key for a user-written name ('Aluminium 6061-T6' -> 'aluminium_6061'), or None."""
    key = name.strip().lower().replace(" ", "_").replace("-", "_")
    key = ALIASES.get(key, key)
    return key if key in PRESETS else None


def structural_names() -> List[str]:
    return sorted(k for k, m in PRESETS.items() if m.structural)

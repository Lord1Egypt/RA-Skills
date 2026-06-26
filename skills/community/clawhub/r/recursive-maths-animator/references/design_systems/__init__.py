"""
Design Systems Registry for recursive-maths-animator

Built-in aesthetic systems inspired by world-class designers and movements.
Each module exports Colors, Typography, Motion (easing), Background,
Containers, and a BaseScene class following the same API as
soft_enterprise_palette.SoftEnterpriseScene.

Usage:
    from design_systems import get_scheme
    scheme = get_scheme("swiss")
    scene_class = scheme["scene_class"]

Or import directly:
    from design_systems.swiss_international import SwissScene

Schemes:
    A — swiss       : Swiss International (Josef Müller-Brockmann)
    B — bauhaus     : Bauhaus Modern (Herbert Bayer)
    C — braun       : Braun Minimal (Dieter Rams)
    D — editorial   : Editorial Bold (Paula Scher / Pentagram)
    E — apple       : Apple Precision (Jony Ive)
    F — soft        : Soft Enterprise (existing fallback; import from soft_enterprise_palette)
"""

import sys
from pathlib import Path

# Ensure sibling imports resolve when this package is on sys.path
_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))


# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------

_REGISTRY = {
    "swiss": {
        "name": "Swiss International",
        "designer": "Josef Müller-Brockmann",
        "module": "swiss_international",
        "scene_class": "SwissScene",
        "colors_class": "SwissColors",
        "typography_class": "SwissTypography",
        "easing": "EASE_SWISS_SNAP",
        "mood": "Strict grid, rational hierarchy, clinical precision",
        "font_primary": "Inter",
        "font_mono": "JetBrains Mono",
    },
    "bauhaus": {
        "name": "Bauhaus Modern",
        "designer": "Herbert Bayer",
        "module": "bauhaus_modern",
        "scene_class": "BauhausScene",
        "colors_class": "BauhausColors",
        "typography_class": "BauhausTypography",
        "easing": "EASE_BAUHAUS_SPRING",
        "mood": "Geometric, primary colors, asymmetric, functional art",
        "font_primary": "Space Grotesk",
        "font_mono": "Space Mono",
    },
    "braun": {
        "name": "Braun Minimal",
        "designer": "Dieter Rams",
        "module": "braun_minimal",
        "scene_class": "BraunScene",
        "colors_class": "BraunColors",
        "typography_class": "BraunTypography",
        "easing": "EASE_BRAUN_LINEAR",
        "mood": "Warm light grays, systematic spacing, less but better",
        "font_primary": "Work Sans",
        "font_mono": None,
    },
    "editorial": {
        "name": "Editorial Bold",
        "designer": "Paula Scher / Pentagram",
        "module": "editorial_bold",
        "scene_class": "EditorialScene",
        "colors_class": "EditorialColors",
        "typography_class": "EditorialTypography",
        "easing": "EASE_EDITORIAL_DRAMA",
        "mood": "Dramatic scale contrast, deep navy + warm cream, magazine confidence",
        "font_primary": "Playfair Display",
        "font_secondary": "Inter",
        "font_mono": None,
    },
    "apple": {
        "name": "Apple Precision",
        "designer": "Jony Ive",
        "module": "apple_precision",
        "scene_class": "AppleScene",
        "colors_class": "AppleColors",
        "typography_class": "AppleTypography",
        "easing": "EASE_APPLE_FLOAT",
        "mood": "Cool neutrals, generous whitespace, subtle depth, sleek motion",
        "font_primary": "DM Sans",
        "font_mono": None,
    },
}


def list_schemes():
    """Return a list of scheme keys and human-readable summaries."""
    return [
        {
            "key": key,
            "name": meta["name"],
            "designer": meta["designer"],
            "mood": meta["mood"],
            "font_primary": meta["font_primary"],
        }
        for key, meta in _REGISTRY.items()
    ]


def get_scheme(key: str):
    """Get metadata for a design system by key (e.g. 'swiss', 'bauhaus')."""
    key = key.lower().strip()
    if key not in _REGISTRY:
        available = ", ".join(_REGISTRY.keys())
        raise KeyError(f"Unknown scheme '{key}'. Available: {available}")
    return _REGISTRY[key]


def scheme_keys():
    """Return all available scheme keys."""
    return list(_REGISTRY.keys())


# ---------------------------------------------------------------------------
# Lazy import helpers
# ---------------------------------------------------------------------------

def import_module(key: str):
    """Import the module for a given scheme key."""
    meta = get_scheme(key)
    mod_name = meta["module"]
    __import__(mod_name)
    return sys.modules[mod_name]


def get_scene_class(key: str):
    """Import and return the base scene class for a scheme."""
    meta = get_scheme(key)
    mod = import_module(key)
    return getattr(mod, meta["scene_class"])


def get_colors_class(key: str):
    """Import and return the colors class for a scheme."""
    meta = get_scheme(key)
    mod = import_module(key)
    return getattr(mod, meta["colors_class"])


def get_typography_class(key: str):
    """Import and return the typography class for a scheme."""
    meta = get_scheme(key)
    mod = import_module(key)
    return getattr(mod, meta["typography_class"])


def get_easing(key: str):
    """Import and return the easing function for a scheme."""
    meta = get_scheme(key)
    mod = import_module(key)
    return getattr(mod, meta["easing"])


# ---------------------------------------------------------------------------
# Brief-first pitch helper
# ---------------------------------------------------------------------------

_SCHEME_LABELS = {
    "A": "swiss",
    "B": "bauhaus",
    "C": "braun",
    "D": "editorial",
    "E": "apple",
}


def resolve_scheme_label(label: str) -> str:
    """Map 'A', 'B', 'C', 'D', 'E' or a raw key to a canonical scheme key."""
    label = label.strip().upper()
    if label in _SCHEME_LABELS:
        return _SCHEME_LABELS[label]
    label = label.lower()
    if label in _REGISTRY:
        return label
    raise KeyError(f"Cannot resolve scheme label '{label}'")


def pitch_text() -> str:
    """Return a ready-to-paste brief-first palette pitch."""
    lines = [
        "Pick a look:",
        "",
        "A — Swiss grid (Inter, clinical, data-forward)",
        "B — Bauhaus primary (Space Grotesk, geometric, educational)",
        "C — Braun minimal (Work Sans, warm gray, product)",
        "D — Editorial bold (Playfair + Inter, dramatic, storytelling)",
        "E — Apple precision (DM Sans, cool, tech)",
        "",
        "Or: F — Soft Enterprise (warm cream + Roboto, existing default)",
        "",
        "Reply with the letter (e.g. 'D + 16:9 + calm') or name.",
    ]
    return "\n".join(lines)

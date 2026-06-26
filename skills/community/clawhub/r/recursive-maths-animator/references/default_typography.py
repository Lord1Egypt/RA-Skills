"""
Default on-screen typography for this skill.

Skill convention: use **Roboto** for all Manim ``Text()`` unless the user asks for
another font in ``DESIGN_THEME.md``.

Manim resolves ``font`` by family name against installed system fonts. For
reproducible renders (CI, minimal Linux images), add ``Roboto*.ttf`` under the
project's ``assets/fonts/`` and register the font with Manim's font system if
needed, or install ``fonts-roboto`` / ``ttf-roboto`` from the OS package manager.

``MathTex`` / ``Tex`` keep LaTeX math fonts unless the user requests otherwise.

---

Built-in Design Systems
-----------------------

The skill now ships five world-class designer-inspired design systems under
``design_systems/``. Each exports Colors, Typography, Motion (easing), Background,
Containers, and a BaseScene class (same API as ``SoftEnterpriseScene``).

Import a scheme directly::

    from design_systems.swiss_international import SwissScene, SwissColors, EASE_SWISS_SNAP
    from design_systems.bauhaus_modern import BauhausScene, BauhausColors, EASE_BAUHAUS_SPRING
    from design_systems.braun_minimal import BraunScene, BraunColors, EASE_BRAUN_LINEAR
    from design_systems.editorial_bold import EditorialScene, EditorialColors, EASE_EDITORIAL_DRAMA
    from design_systems.apple_precision import AppleScene, AppleColors, EASE_APPLE_FLOAT

Or use the registry::

    from design_systems import get_scheme, get_scene_class
    SceneClass = get_scene_class("swiss")  # -> SwissScene

Font download-on-demand::

    from design_systems.font_catalog import install_fonts
    install_fonts("swiss", target_dir="assets/fonts")

Available schemes
~~~~~~~~~~~~~~~~

+--------+----------------------------+-------------------------+--------------------------+
| Key    | Name                       | Designer / Movement       | Primary Font (OFL)       |
+========+============================+=========================+==========================+
| swiss  | Swiss International        | Josef Müller-Brockmann  | Inter                    |
+--------+----------------------------+-------------------------+--------------------------+
| bauhaus| Bauhaus Modern             | Herbert Bayer           | Space Grotesk            |
+--------+----------------------------+-------------------------+--------------------------+
| braun  | Braun Minimal              | Dieter Rams             | Work Sans                |
+--------+----------------------------+-------------------------+--------------------------+
|editorial| Editorial Bold             | Paula Scher / Pentagram | Playfair Display + Inter |
+--------+----------------------------+-------------------------+--------------------------+
| apple  | Apple Precision            | Jony Ive                | DM Sans                  |
+--------+----------------------------+-------------------------+--------------------------+

The existing ``soft_enterprise_palette.py`` (warm cream + Roboto) remains the
implicit fallback when no scheme is chosen.
"""

# Single default family for body, titles, labels, and code-style on-screen text.
DEFAULT_FONT = "Roboto"

# Registry of design system keys for quick agent lookup.
# Values match the keys accepted by design_systems.get_scheme() and
# design_systems.font_catalog.install_fonts().
DESIGN_SYSTEMS = {
    "swiss": {
        "name": "Swiss International",
        "designer": "Josef Müller-Brockmann",
        "font_primary": "Inter",
        "font_mono": "JetBrains Mono",
        "mood": "Strict grid, rational hierarchy, clinical precision",
        "module": "design_systems.swiss_international",
    },
    "bauhaus": {
        "name": "Bauhaus Modern",
        "designer": "Herbert Bayer",
        "font_primary": "Space Grotesk",
        "font_mono": "Space Mono",
        "mood": "Geometric, primary colors, asymmetric, functional art",
        "module": "design_systems.bauhaus_modern",
    },
    "braun": {
        "name": "Braun Minimal",
        "designer": "Dieter Rams",
        "font_primary": "Work Sans",
        "font_mono": None,
        "mood": "Warm light grays, systematic spacing, less but better",
        "module": "design_systems.braun_minimal",
    },
    "editorial": {
        "name": "Editorial Bold",
        "designer": "Paula Scher / Pentagram",
        "font_primary": "Playfair Display",
        "font_secondary": "Inter",
        "font_mono": None,
        "mood": "Dramatic scale contrast, deep navy + warm cream, magazine confidence",
        "module": "design_systems.editorial_bold",
    },
    "apple": {
        "name": "Apple Precision",
        "designer": "Jony Ive",
        "font_primary": "DM Sans",
        "font_mono": None,
        "mood": "Cool neutrals, generous whitespace, subtle depth, sleek motion",
        "module": "design_systems.apple_precision",
    },
    "soft": {
        "name": "Soft Enterprise",
        "designer": "Skill default",
        "font_primary": "Roboto",
        "font_mono": None,
        "mood": "Warm cream backgrounds, dot grid patterns, gas-spring easing",
        "module": "soft_enterprise_palette",
    },
}


def resolve_font_family(system_key: str, role: str = "primary") -> str:
    """
    Return the font family name for a design system and role.

    Args:
        system_key: One of the keys in DESIGN_SYSTEMS.
        role: "primary", "secondary", or "mono".

    Returns:
        Font family string (e.g. "Inter", "Playfair Display").
    """
    system_key = system_key.lower().strip()
    meta = DESIGN_SYSTEMS.get(system_key)
    if meta is None:
        available = ", ".join(DESIGN_SYSTEMS.keys())
        raise KeyError(f"Unknown design system '{system_key}'. Available: {available}")

    if role == "primary":
        return meta["font_primary"]
    if role == "secondary":
        return meta.get("font_secondary") or meta["font_primary"]
    if role == "mono":
        return meta.get("font_mono") or meta["font_primary"]
    raise ValueError(f"Unknown role '{role}'")

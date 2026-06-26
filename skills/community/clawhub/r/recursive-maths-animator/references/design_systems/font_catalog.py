"""
Font Catalog — metadata, download URLs, and install helpers for design systems.

All fonts listed here are SIL Open Font License (OFL) 1.1 and freely
redistributable.  We do **not** bundle TTF files in the repository;
instead we download them on demand into the project's ``assets/fonts/``
folder so renders are reproducible on CI and minimal containers.

Usage:
    from design_systems.font_catalog import install_fonts, get_font_family
    install_fonts("swiss", target_dir="assets/fonts")
    family = get_font_family("swiss")   # -> "Inter"
"""

import json
import shutil
import subprocess
import zipfile
from pathlib import Path
from typing import Dict, List, Optional


# ---------------------------------------------------------------------------
# Font metadata
# ---------------------------------------------------------------------------

# Google Fonts download endpoint:  https://fonts.google.com/download?family={Family+Name}
# Static TTF variants we need for Manim (Manim resolves by family name).

_FONT_META: Dict[str, Dict] = {
    "Inter": {
        "url": "https://fonts.google.com/download?family=Inter",
        "license": "SIL Open Font License 1.1",
        "license_url": "https://fonts.google.com/specimen/Inter#license",
        "variants": [
            "Inter-Regular.ttf",
            "Inter-Medium.ttf",
            "Inter-SemiBold.ttf",
            "Inter-Bold.ttf",
        ],
        "family_name": "Inter",
    },
    "Space Grotesk": {
        "url": "https://fonts.google.com/download?family=Space+Grotesk",
        "license": "SIL Open Font License 1.1",
        "license_url": "https://fonts.google.com/specimen/Space+Grotesk#license",
        "variants": [
            "SpaceGrotesk-Regular.ttf",
            "SpaceGrotesk-Medium.ttf",
            "SpaceGrotesk-SemiBold.ttf",
            "SpaceGrotesk-Bold.ttf",
        ],
        "family_name": "Space Grotesk",
    },
    "Space Mono": {
        "url": "https://fonts.google.com/download?family=Space+Mono",
        "license": "SIL Open Font License 1.1",
        "license_url": "https://fonts.google.com/specimen/Space+Mono#license",
        "variants": [
            "SpaceMono-Regular.ttf",
            "SpaceMono-Bold.ttf",
        ],
        "family_name": "Space Mono",
    },
    "Work Sans": {
        "url": "https://fonts.google.com/download?family=Work+Sans",
        "license": "SIL Open Font License 1.1",
        "license_url": "https://fonts.google.com/specimen/Work+Sans#license",
        "variants": [
            "WorkSans-Regular.ttf",
            "WorkSans-Medium.ttf",
            "WorkSans-SemiBold.ttf",
            "WorkSans-Bold.ttf",
        ],
        "family_name": "Work Sans",
    },
    "Playfair Display": {
        "url": "https://fonts.google.com/download?family=Playfair+Display",
        "license": "SIL Open Font License 1.1",
        "license_url": "https://fonts.google.com/specimen/Playfair+Display#license",
        "variants": [
            "PlayfairDisplay-Regular.ttf",
            "PlayfairDisplay-Medium.ttf",
            "PlayfairDisplay-SemiBold.ttf",
            "PlayfairDisplay-Bold.ttf",
        ],
        "family_name": "Playfair Display",
    },
    "DM Sans": {
        "url": "https://fonts.google.com/download?family=DM+Sans",
        "license": "SIL Open Font License 1.1",
        "license_url": "https://fonts.google.com/specimen/DM+Sans#license",
        "variants": [
            "DMSans-Regular.ttf",
            "DMSans-Medium.ttf",
            "DMSans-SemiBold.ttf",
            "DMSans-Bold.ttf",
        ],
        "family_name": "DM Sans",
    },
    "JetBrains Mono": {
        "url": "https://fonts.google.com/download?family=JetBrains+Mono",
        "license": "SIL Open Font License 1.1",
        "license_url": "https://fonts.google.com/specimen/JetBrains+Mono#license",
        "variants": [
            "JetBrainsMono-Regular.ttf",
            "JetBrainsMono-Medium.ttf",
            "JetBrainsMono-Bold.ttf",
        ],
        "family_name": "JetBrains Mono",
    },
}

# Map scheme key -> list of font family names needed
_SCHEME_FONTS = {
    "swiss": ["Inter", "JetBrains Mono"],
    "bauhaus": ["Space Grotesk", "Space Mono"],
    "braun": ["Work Sans"],
    "editorial": ["Playfair Display", "Inter"],
    "apple": ["DM Sans"],
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _download_zip(url: str, dest: Path) -> Path:
    """Download a zip file from Google Fonts to ``dest``. Returns path."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    cmd = ["curl", "-L", "-o", str(dest), url]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"Failed to download font from {url}: {result.stderr}")
    return dest


def _extract_needed(ttf_names: List[str], zip_path: Path, out_dir: Path) -> List[Path]:
    """Extract only the listed TTF files from a Google Fonts zip."""
    out_dir.mkdir(parents=True, exist_ok=True)
    extracted = []
    with zipfile.ZipFile(zip_path, "r") as zf:
        for item in zf.namelist():
            # Google Fonts zips sometimes nest under a folder
            basename = Path(item).name
            if basename in ttf_names:
                data = zf.read(item)
                target = out_dir / basename
                target.write_bytes(data)
                extracted.append(target)
    return extracted


def install_fonts(scheme_key: str, target_dir: str | Path) -> List[Path]:
    """
    Download and install all fonts needed for a design system.

    Args:
        scheme_key: One of "swiss", "bauhaus", "braun", "editorial", "apple".
        target_dir: Directory to write TTF files (e.g. ``assets/fonts``).

    Returns:
        List of paths to installed TTF files.
    """
    scheme_key = scheme_key.lower().strip()
    if scheme_key not in _SCHEME_FONTS:
        available = ", ".join(_SCHEME_FONTS.keys())
        raise KeyError(f"Unknown scheme '{scheme_key}'. Available: {available}")

    target = Path(target_dir).resolve()
    installed = []

    for family in _SCHEME_FONTS[scheme_key]:
        meta = _FONT_META[family]
        zip_path = target / f"{family.replace(' ', '_')}.zip"

        # Skip if all variants already exist
        needed = [v for v in meta["variants"] if not (target / v).exists()]
        if not needed:
            installed.extend([target / v for v in meta["variants"]])
            continue

        print(f"Downloading {family} …")
        _download_zip(meta["url"], zip_path)
        extracted = _extract_needed(meta["variants"], zip_path, target)
        installed.extend(extracted)

        # Clean up zip
        zip_path.unlink(missing_ok=True)

    return installed


def get_font_family(scheme_key: str, role: str = "primary") -> str:
    """
    Return the Manim ``font=`` family name for a scheme.

    Args:
        scheme_key: One of the built-in scheme keys.
        role: "primary", "secondary", or "mono".

    Returns:
        Font family string (e.g. "Inter", "Playfair Display").
    """
    scheme_key = scheme_key.lower().strip()

    # Import the scheme module to read its Typography class
    import sys
    ds_dir = Path(__file__).resolve().parent
    if str(ds_dir) not in sys.path:
        sys.path.insert(0, str(ds_dir))

    from design_systems import import_module  # noqa: E402
    mod = import_module(scheme_key)
    typography = getattr(mod, f"{scheme_key.title()}Typography")

    if role == "primary":
        return getattr(typography, "FONT_FAMILY", typography.FONT_FAMILY_PRIMARY)
    if role == "secondary":
        return getattr(typography, "FONT_FAMILY_SECONDARY", None) or getattr(
            typography, "FONT_FAMILY", None
        )
    if role == "mono":
        return getattr(typography, "FONT_FAMILY_MONO", None)
    raise ValueError(f"Unknown role '{role}'")


def attribution_text(scheme_key: str) -> str:
    """Return OFL attribution lines for all fonts used by a scheme."""
    lines = ["# Font Attribution", ""]
    for family in _SCHEME_FONTS.get(scheme_key, []):
        meta = _FONT_META[family]
        lines.append(f"{meta['family_name']}")
        lines.append(f"  License: {meta['license']}")
        lines.append(f"  {meta['license_url']}")
        lines.append("")
    return "\n".join(lines)


def write_attribution_file(scheme_key: str, target_dir: str | Path) -> Path:
    """Write a FONT_ATTRIBUTION.txt into the target directory."""
    target = Path(target_dir).resolve()
    target.mkdir(parents=True, exist_ok=True)
    path = target / "FONT_ATTRIBUTION.txt"
    path.write_text(attribution_text(scheme_key), encoding="utf-8")
    return path

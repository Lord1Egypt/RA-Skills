from __future__ import annotations

from pathlib import Path

PICTOGRAM_LABELS = {
    "GHS01": "Exploding Bomb",
    "GHS02": "Flame",
    "GHS03": "Flame Over Circle",
    "GHS04": "Gas Cylinder",
    "GHS05": "Corrosion",
    "GHS06": "Skull and Crossbones",
    "GHS07": "Exclamation Mark",
    "GHS08": "Health Hazard",
    "GHS09": "Environment",
}


def _find_asset(code: str, assets_root: Path | None) -> Path | None:
    if assets_root is None:
        return None
    for suffix in (".png", ".jpg", ".jpeg"):
        candidate = assets_root / "pictograms" / f"{code.lower()}{suffix}"
        if candidate.exists():
            return candidate
    return None


def render_pictogram_line(paragraph, codes: list[str], assets_root: Path | None = None) -> list[str]:
    warnings: list[str] = []
    if not codes:
        paragraph.add_run("No data available")
        return warnings

    for index, code in enumerate(codes):
        asset = _find_asset(code, assets_root)
        if index:
            paragraph.add_run("  ")
        if asset is None:
            label = PICTOGRAM_LABELS.get(code, "Unknown pictogram")
            paragraph.add_run(f"[{code} - {label}]")
            warnings.append(f"Pictogram asset missing for {code}; inserted placeholder.")
            continue
        paragraph.add_run().add_picture(str(asset))
    return warnings

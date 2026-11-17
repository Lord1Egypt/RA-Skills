#!/usr/bin/env python3
"""Render and validate all golden Workday Companion card artifacts."""

from __future__ import annotations

import argparse
import json
import shutil
import struct
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CARDS_DIR = ROOT / "assets" / "golden-cards"
RENDER_SCRIPT = ROOT / "scripts" / "render_card.py"
EXPECTED_COUNT = 8
PUBLIC_STEMS = ["work-sign-low-energy", "lunch-hot-meal", "mood-low-battery", "afterwork-direct-home"]
PUBLIC_DIR = ROOT / "assets" / "public-cards"
MIN_HTML_BYTES = 3000
MIN_SVG_BYTES = 1600


def load_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path.name} must be a JSON object")
    return payload


def render_card(card_path: Path, out_dir: Path) -> tuple[Path, Path]:
    stem = card_path.stem
    html_path = out_dir / f"{stem}.html"
    svg_path = out_dir / f"{stem}.svg"
    subprocess.run(
        [
            sys.executable,
            str(RENDER_SCRIPT),
            str(card_path),
            "--html",
            str(html_path),
            "--svg",
            str(svg_path),
        ],
        cwd=ROOT,
        check=True,
    )
    return html_path, svg_path


def require_text(text: str, needle: str, label: str, errors: list[str]) -> None:
    if needle not in text:
        errors.append(f"missing {label}: {needle}")


def validate_rendered(card_path: Path, html_path: Path, svg_path: Path) -> list[str]:
    errors: list[str] = []
    card = load_json(card_path)

    if not html_path.is_file():
        errors.append(f"missing html output: {html_path.name}")
        return errors
    if not svg_path.is_file():
        errors.append(f"missing svg output: {svg_path.name}")
        return errors
    if html_path.stat().st_size < MIN_HTML_BYTES:
        errors.append(f"html output too small: {html_path.stat().st_size}")
    if svg_path.stat().st_size < MIN_SVG_BYTES:
        errors.append(f"svg output too small: {svg_path.stat().st_size}")

    html_text = html_path.read_text(encoding="utf-8")
    svg_text = svg_path.read_text(encoding="utf-8")
    require_text(html_text, '<!doctype html>', "html doctype", errors)
    require_text(svg_text, "<svg", "svg root", errors)
    require_text(html_text, f'route-{card["route"]}', "route class", errors)

    for field in ("module", "time_label", "title", "reason", "action", "footer"):
        value = str(card[field])
        require_text(html_text, value, f"html {field}", errors)
        require_text(svg_text, value, f"svg {field}", errors)
    for tag in card.get("tags", []):
        require_text(html_text, str(tag), "html tag", errors)
        require_text(svg_text, str(tag), "svg tag", errors)

    ratio = card.get("ratio", "9:16")
    if ratio == "3:4":
        require_text(svg_text, 'width="900" height="1200"', "3:4 svg size", errors)
    else:
        require_text(svg_text, 'width="900" height="1600"', "9:16 svg size", errors)
    return errors


def png_dimensions(path: Path) -> tuple[int, int]:
    header = path.read_bytes()[:24]
    if len(header) != 24 or header[:8] != b"\x89PNG\r\n\x1a\n" or header[12:16] != b"IHDR":
        raise ValueError(f"invalid PNG header: {path.name}")
    return struct.unpack(">II", header[16:24])


def validate_public_assets(render_dir: Path) -> list[str]:
    errors: list[str] = []
    for stem in PUBLIC_STEMS:
        source_svg = PUBLIC_DIR / f"{stem}.svg"
        source_png = PUBLIC_DIR / f"{stem}.png"
        rendered_svg = render_dir / f"{stem}.svg"
        if not source_svg.is_file() or not source_png.is_file():
            errors.append(f"public asset missing: {stem}")
            continue
        if source_svg.read_text(encoding="utf-8") != rendered_svg.read_text(encoding="utf-8"):
            errors.append(f"public SVG stale: {source_svg.name}")
        try:
            width, height = png_dimensions(source_png)
        except ValueError as exc:
            errors.append(str(exc))
            continue
        if (width, height) != (900, 1600):
            errors.append(f"public PNG size drifted: {source_png.name} {width}x{height}")
        if source_png.stat().st_size < 20_000:
            errors.append(f"public PNG too small: {source_png.name}")
    return errors


def validate_stress_layout(render_dir: Path) -> list[str]:
    errors: list[str] = []
    fixture = {
        "module": "今日工作签",
        "route": "sign-strip",
        "time_label": "09:30",
        "title": "一二三四五六七八九十一二三四五六七八",
        "reason": "一二三四五六七八九十一二三四五六七八九十一二三四五六七八九十一二三四五六七八九十",
        "action": "一二三四五六七八九十一二三四五六七八九十一二三四五六七八九十一二三四五六七八九十",
        "tags": ["一二三四五六七八", "九十一二三四五六", "七八九十一二三四", "五六七八九十一二"],
        "corner": "完整卡",
        "footer": "今天先这么过。",
        "alt_text": "图卡最大长度排版压力样例。",
        "ratio": "3:4",
        "share_safe": True,
    }
    fixture_path = render_dir / "stress-layout.json"
    svg_path = render_dir / "stress-layout.svg"
    fixture_path.write_text(json.dumps(fixture, ensure_ascii=False), encoding="utf-8")
    subprocess.run([sys.executable, str(RENDER_SCRIPT), str(fixture_path), "--svg", str(svg_path)], cwd=ROOT, check=True)
    svg = svg_path.read_text(encoding="utf-8")
    if svg.count("<tspan") < 8:
        errors.append("stress layout did not wrap title, reason and action")
    if svg.count('y="930"') == 0 or svg.count('y="994"') == 0:
        errors.append("stress layout did not wrap tags")
    return errors


def validate_all(out_dir: str | Path | None = None, keep: bool = False) -> None:
    cards = sorted(CARDS_DIR.glob("*.json"))
    if len(cards) != EXPECTED_COUNT:
        raise RuntimeError(f"golden-cards must contain {EXPECTED_COUNT} json files; got {len(cards)}")

    created_temp = out_dir is None
    base_dir = Path(tempfile.mkdtemp(prefix="workday-render-")) if created_temp else Path(out_dir).resolve()
    base_dir.mkdir(parents=True, exist_ok=True)

    errors: list[str] = []
    try:
        for card_path in cards:
            try:
                html_path, svg_path = render_card(card_path, base_dir)
                card_errors = validate_rendered(card_path, html_path, svg_path)
            except (OSError, ValueError, subprocess.CalledProcessError) as exc:
                card_errors = [str(exc)]
            if card_errors:
                errors.append(f"{card_path.relative_to(ROOT)}:")
                errors.extend(f"  - {error}" for error in card_errors)
            else:
                print(f"OK rendered {card_path.relative_to(ROOT)}")
        errors.extend(validate_public_assets(base_dir))
        errors.extend(validate_stress_layout(base_dir))
    finally:
        if created_temp and not keep:
            shutil.rmtree(base_dir, ignore_errors=True)

    if errors:
        print("FAIL rendered cards")
        for error in errors:
            print(f"- {error}")
        raise SystemExit(1)
    print(f"OK rendered cards {len(cards)}/{len(cards)} public={len(PUBLIC_STEMS)} stress=1")


def main() -> None:
    parser = argparse.ArgumentParser(description="Render and validate Workday Companion golden cards.")
    parser.add_argument("--out-dir", help="Directory for rendered HTML/SVG files.")
    parser.add_argument("--keep", action="store_true", help="Keep temporary rendered files.")
    args = parser.parse_args()
    validate_all(out_dir=args.out_dir, keep=args.keep)


if __name__ == "__main__":
    main()

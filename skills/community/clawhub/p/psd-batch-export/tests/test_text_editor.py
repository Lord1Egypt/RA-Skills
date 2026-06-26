from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

from psd_text_editor import patch_psd_text  # noqa: E402


def marker(text: str, char_count: int = 6) -> bytes:
    body = text.encode("utf-16-be")
    max_len = char_count * 2
    return b"prefix Txt TEXT" + char_count.to_bytes(4, "big") + body + (b"\x00" * (max_len - len(body))) + b" suffix"


def test_patch_psd_text_replaces_synthetic_marker(tmp_path: Path) -> None:
    src = tmp_path / "in.psd"
    dst = tmp_path / "out.psd"
    src.write_bytes(marker("OLD", char_count=6))

    replaced = patch_psd_text(src, dst, {"OLD": "NEW"})

    assert replaced == 1
    data = dst.read_bytes()
    assert "NEW".encode("utf-16-be") in data
    assert "OLD".encode("utf-16-be") not in data


def test_patch_psd_text_truncates_long_values(tmp_path: Path) -> None:
    src = tmp_path / "in.psd"
    dst = tmp_path / "out.psd"
    src.write_bytes(marker("AB", char_count=2))

    replaced = patch_psd_text(src, dst, {"AB": "WXYZ"})

    assert replaced == 1
    data = dst.read_bytes()
    assert "WX".encode("utf-16-be") in data
    assert "WXYZ".encode("utf-16-be") not in data


def test_patch_psd_text_returns_zero_when_not_found(tmp_path: Path) -> None:
    src = tmp_path / "in.psd"
    dst = tmp_path / "out.psd"
    src.write_bytes(marker("AB", char_count=4))

    replaced = patch_psd_text(src, dst, {"NOPE": "XY"})

    assert replaced == 0
    assert dst.exists()

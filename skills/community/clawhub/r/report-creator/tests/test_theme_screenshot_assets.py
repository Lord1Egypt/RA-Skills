from __future__ import annotations

from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCREENSHOT_DIR = REPO_ROOT / "templates" / "screenshots"
EXPECTED_SIZE = (1280, 800)


def read_png_size(path: Path) -> tuple[int, int]:
    data = path.read_bytes()
    assert data[:8] == b"\x89PNG\r\n\x1a\n", f"{path.name} is not a valid PNG file"
    assert data[12:16] == b"IHDR", f"{path.name} is missing a PNG IHDR header"
    width = int.from_bytes(data[16:20], "big")
    height = int.from_bytes(data[20:24], "big")
    return width, height


def test_theme_preview_screenshots_use_consistent_dimensions():
    screenshots = sorted(SCREENSHOT_DIR.glob("*.png"))
    assert screenshots, "Expected theme preview screenshots under templates/screenshots/"

    sizes = {path.name: read_png_size(path) for path in screenshots}
    assert all(size == EXPECTED_SIZE for size in sizes.values()), (
        "README theme preview screenshots must stay aligned. "
        f"Expected every screenshot to be {EXPECTED_SIZE}, got: {sizes}"
    )

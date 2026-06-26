import importlib.util
from pathlib import Path

import pytest

MODULE_PATH = Path(__file__).with_name("generate_image.py")
SPEC = importlib.util.spec_from_file_location("generate_image", MODULE_PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


@pytest.mark.parametrize(
    ("max_input_dim", "expected"),
    [
        (0, "2K"),
        (2499, "2K"),
        (2500, "3K"),
        (4000, "3K"),
    ],
)
def test_auto_detect_resolution_thresholds(max_input_dim, expected):
    assert MODULE.auto_detect_resolution(max_input_dim) == expected


def test_choose_size_resolution_only():
    assert MODULE.choose_size("2K", None) == "2K"
    assert MODULE.choose_size("3K", None) == "3K"


def test_choose_size_with_aspect_ratio():
    assert MODULE.choose_size("2K", "9:16") == "1600x2848"
    assert MODULE.choose_size("3K", "1:1") == "3072x3072"
    assert MODULE.choose_size("2K", "16:9") == "2848x1600"

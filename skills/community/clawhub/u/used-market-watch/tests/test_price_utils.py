from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from price_utils import parse_price_kr


def test_parse_price_formats():
    assert parse_price_kr("10,000원") == 10000
    assert parse_price_kr("10만") == 100000
    assert parse_price_kr("2만5천") == 25000
    assert parse_price_kr("1.2만") == 12000
    assert parse_price_kr("무료나눔") == 0

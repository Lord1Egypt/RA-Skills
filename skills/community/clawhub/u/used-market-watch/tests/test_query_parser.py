from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from query_parser import parse_search_intent


def test_parse_markets_and_excludes():
    intent = parse_search_intent("당근 번장에서 아이폰 15 프로 max 120만원 이하 -깨짐 제외: 고장")
    assert "danggeun" in intent.markets
    assert "bunjang" in intent.markets
    assert "깨짐" in intent.exclude_terms
    assert "고장" in intent.exclude_terms
    assert intent.max_price == 1200000


def test_parse_location_and_keyword():
    intent = parse_search_intent("잠실 당근마켓에서 맥북 에어 m2 찾아줘")
    assert intent.location and "잠실" in intent.location
    assert "맥북" in intent.keyword

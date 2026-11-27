"""A hotel button opens that hotel, or says it is a search.

The Tokyo plan's five hotel cards all opened Booking.com searches for an area ("Harbin Taiping
Airport", "Ningyocho, Tokyo"), labelled "Review option": the traveller booked whatever came first.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from check_plan_consistency import _search_names, check_hotel_search_names_the_hotel  # noqa: E402
from plan_flags import is_search_url, search_text  # noqa: E402

BOOKING = "https://www.booking.com/searchresults.html?ss={}&checkin=2026-09-08&checkout=2026-09-09"


def _errors(acc: dict) -> list[str]:
    errors: list[str] = []
    check_hotel_search_names_the_hotel({"booking_options": {"accommodations": [acc]}}, errors, [])
    return errors


def test_search_links_are_told_apart_from_exact_pages() -> None:
    assert is_search_url(BOOKING.format("x")) and search_text(BOOKING.format("AC+Hotel")) == "AC Hotel"
    assert is_search_url("https://www.kayak.com/flights/AMS-ALC/2027-02-12/2027-02-16?adults=1")
    assert not is_search_url("https://www.booking.com/hotel/es/ac-alicante.html")
    assert not is_search_url("https://hotels.ctrip.com/hotels/436921.html")


def test_an_area_search_is_refused_and_a_name_search_passes() -> None:
    area = _errors({"property_name": "新启航酒店（哈尔滨太平机场店）",
                    "review_url": BOOKING.format("Harbin+Taiping+Airport")})
    assert area and "Harbin Taiping Airport" in area[0]
    assert _errors({"property_name": "西鉄イン日本橋（人形町）Nishitetsu Inn Nihonbashi Ningyocho",
                    "review_url": BOOKING.format("Ningyocho%2C+Tokyo")}), "an area word alone is not the hotel"
    assert not _errors({"property_name": "Ars Magna Bleisure Hotel",
                        "review_url": BOOKING.format("Ars+Magna+Bleisure+Hotel+Palma")})
    assert not _errors({"property_name": "AC Hotel by Marriott Alicante",
                        "review_url": "https://www.transavia.com/en-EU/home/"}), "not a search: not this check"
    assert _search_names("Hôtel Café Royal", "Hotel Cafe Royal Lyon")
    assert _search_names("东直门 智选假日", "北京东直门智选假日酒店")


def test_an_exact_link_must_be_exact() -> None:
    ok = {"property_name": "AC Hotel Alicante", "exact_booking_url": "https://www.booking.com/hotel/es/ac-alicante.html"}
    assert not _errors(ok)
    assert _errors(dict(ok, exact_booking_url=BOOKING.format("AC+Hotel+Alicante")))
    assert _errors(dict(ok, exact_booking_url="https://www.marriott.com/"))


def test_the_page_labels_a_search_and_offers_the_exact_page_first() -> None:
    from render_final_trip_html import localize_static_page, option_card  # noqa: PLC0415
    hotel = {"id": "acc-1", "provider": "Booking.com", "checked_at": "2026-11-26",
             "property_name": "AC Hotel Alicante", "review_url": BOOKING.format("AC+Hotel+Alicante"),
             "exact_booking_url": "https://www.booking.com/hotel/es/ac-alicante.html",
             "exact_booking_provider": "Booking.com"}
    card = option_card("hotel", hotel)
    exact = card.index('data-booking-purpose="exact-option"')
    assert exact < card.index('data-booking-purpose="review-option"'), "the exact page is the first button"
    en = localize_static_page(card, "en")
    assert "Open this exact property on Booking.com" in en
    assert "Search Booking.com and pick this option from the results" in en
    zh = localize_static_page(card, "zh-CN")
    assert "在 Booking.com 打开这家住宿的页面" in zh and "在 Booking.com 搜索，需要在结果里自己找到这一项" in zh

    plain = option_card("hotel", dict(hotel, review_url="https://www.booking.com/hotel/es/ac-alicante.html",
                                      exact_booking_url=None))
    assert "Review option in Booking.com" in localize_static_page(plain, "en") and "exact-option" not in plain

#!/usr/bin/env python3
"""Regression tests for the provider/target match rule in scripts/validate_trip_html.py.

Nine buttons shipped in a real Travel Buddy run reading "Review option in KLM" and opening
Google Flights, and "View restaurant in Google Maps" and opening a Spanish food blog. All three
gates were green: the URLs were HTTPS, unique, tracker-free, and carried every required
attribute. Nothing any of them checks says anything about *where* a link goes, so nothing fired,
and the defect was found by a human clicking a button.

The visible label and the data-*-provider attribute are rendered from the same plan field, so
comparing that attribute to the href reproduces the click. These tests keep that comparison
honest in both directions: it must fire on the shipped defects, and it must not fire on
legitimate pages, including non-Latin provider names where a host cannot be matched by tokens.

Run:  python tests/test_link_provider_match.py
      python -m pytest tests/test_link_provider_match.py
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from validate_trip_html import provider_target_verdict, validate  # noqa: E402


PAGE = """<!doctype html><html lang="zh"><head><title>t</title></head><body>
<a class="booking-link" data-booking-type="flight" data-provider="{fp}"
   data-verified-at="2026-08-04" href="{fu}" target="_blank" rel="noopener noreferrer">x</a>
<a class="dining-link" data-dining-provider="{dp}" data-verified-at="2026-08-04"
   href="{du}" target="_blank" rel="noopener noreferrer">y</a>
</body></html>"""


def page_errors(fp: str, fu: str, dp: str, du: str) -> tuple[list[str], list[str]]:
    notes: list[str] = []
    errors = validate(PAGE.format(fp=fp, fu=fu, dp=dp, du=du), None, set(), None, notes)
    relevant = [e for e in errors if "names provider" in e]
    return relevant, notes


def main() -> int:
    failures: list[str] = []

    def check(label: str, condition: bool, detail: str = "") -> None:
        if not condition:
            failures.append(f"{label}{': ' + detail if detail else ''}")

    # --- unit level -------------------------------------------------------------------
    # The two defects exactly as they shipped.
    check("KLM button opening Google Flights must not pass",
          provider_target_verdict("KLM", "https://www.google.com/travel/flights?q=AMS") is False)
    check("Google Maps button opening a food blog must not pass",
          provider_target_verdict("Google Maps", "https://chiringuitopicasso.es/los-7-mejores/") is False)

    # Legitimate pairings must stay legitimate, or the gate gets routed around.
    for provider, url in [
        ("KLM", "https://www.klm.nl/"),
        ("Transavia", "https://www.transavia.com/"),
        ("Skyscanner", "https://www.skyscanner.net/transport/flights/ams/agp/"),
        ("Google Flights", "https://www.google.com/travel/flights?q=AMS"),
        ("Google Maps", "https://www.google.com/maps/dir/?api=1&origin=a&destination=b"),
        ("Booking.com", "https://www.booking.com/searchresults.html?ss=Malaga"),
        # Provider labels that mix a script with a Latin proper noun still match on the noun.
        ("Catedral de Málaga 官方", "https://malagacatedral.com/cultural-visit/"),
        ("马拉加市政 Alcazaba y Gibralfaro", "https://alcazabaygibralfaro.malaga.eu/en/visits/"),
        ("Museo Picasso Málaga 官方票务", "https://tickets.museopicassomalaga.org/es/"),
        # Aliased non-Latin providers stay checkable rather than falling to undecidable.
        ("高德地图", "https://uri.amap.com/navigation?from=1,2,a&to=3,4,b&mode=bus"),
    ]:
        check(f"legitimate pairing must pass: {provider}",
              provider_target_verdict(provider, url) is True, url)

    # An aliased provider pointed at the wrong host is still a defect.
    check("高德地图 opening Google must not pass",
          provider_target_verdict("高德地图", "https://www.google.com/maps/dir/?api=1") is False)

    # Undecidable is a third state, never a silent pass.
    check("unmatchable provider name is undecidable, not True",
          provider_target_verdict("市政旅游局", "https://example.org/x") is None)

    # --- page level -------------------------------------------------------------------
    errors, _ = page_errors("KLM", "https://www.google.com/travel/flights?q=a",
                            "Google Maps", "https://chiringuitopicasso.es/x/")
    check("page-level gate must report both shipped defects", len(errors) == 2, f"got {len(errors)}")

    errors, _ = page_errors("KLM", "https://www.klm.nl/",
                            "Google Maps", "https://www.google.com/maps/search/?api=1&query=a")
    check("clean page must produce no provider errors", not errors, str(errors))

    errors, notes = page_errors("市政旅游局", "https://example.org/a",
                                "Google Maps", "https://www.google.com/maps/search/?api=1&query=b")
    check("undecidable provider must not error", not errors, str(errors))
    check("undecidable provider must be reported as a note", any("undecidable" in n for n in notes),
          str(notes))

    if failures:
        print("FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("OK: provider/target match rule holds in both directions.")
    return 0


def test_link_provider_match() -> None:
    """Pytest surface: with no test_* function pytest collects nothing from this file and prints
    "no tests ran", which a contributor or CI reads as green. Running the file directly is
    unchanged."""
    assert main() == 0


if __name__ == "__main__":
    raise SystemExit(main())

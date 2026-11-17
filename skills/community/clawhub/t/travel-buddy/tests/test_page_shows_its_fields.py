#!/usr/bin/env python3
"""What a plan holds for the traveller must be readable on the page, and nothing else must be.

An audit of v2.8.0 (2026-10-09) ran a canary sweep: every free-text value in the self-drive fixture
was prefixed with a unique token, the plan rendered, and the page searched for each token. Every
gate stayed green while these never reached the page:

* `attraction_tickets[].sale_opens_at` -- the consistency gate REQUIRES it on every ticket a day
  schedules, and it reached only the calendar file embedded in the page. A traveller who never
  imports the calendar never learns that the tickets go on sale at 09:30 a week ahead.
* `budget.note` -- "per person across two adults and two children; the party total is four times
  this range", i.e. the one sentence that says how to read the headline figure.
* a route segment's `detour_reason` -- the gate's own escape for a long detour, so the traveller
  saw the detour and never the reason.

The same audit found the opposite leak, skill machinery printed as page text: every booking card
ended in `Source: operator_and_comparison_platform`, on Chinese pages too; the machine-identifier
check missed a token glued to Chinese text (`字段source_type未填`) and dropped a whole Chinese
clause that contained one slash; the save path never collected its notes, so the check did not run
on delivery at all. And the "research is N days old / departure in N days" line was dark brown on
the dark hero gradient, 1.0-2.0:1 in all five palettes.

Case 1 is the sweep itself, so a free-text field added later that the renderer forgets fails here
the day it is added, with the field's path in the message.

Run:  python tests/test_page_shows_its_fields.py
      python -m pytest tests/test_page_shows_its_fields.py
"""

from __future__ import annotations

import contextlib
import copy
import html
import io
import json
import re
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import plan_flags  # noqa: E402
import render_final_trip_html as renderer  # noqa: E402
import validate_trip_html as htmlgate  # noqa: E402

SELF_DRIVE = json.loads((ROOT / "tests" / "self-drive-fixture.json").read_text(encoding="utf-8"))
BOOKING_READY = json.loads((ROOT / "tests" / "booking-ready-fixture.json").read_text(encoding="utf-8"))

failures: list[str] = []


def check(label: str, condition: object, detail: object = "") -> None:
    if not condition:
        failures.append(f"{label}\n    {detail}")


# --- 1. the sweep -----------------------------------------------------------------------------

# Keys whose values are machine-facing by shape -- links, ids, dates, enums, codes -- and so are
# not page copy whatever they hold. A value that appears more than once in the plan is skipped
# too: it is a cross-reference (a stop name a segment must match), and prefixing one copy breaks
# the reference rather than testing the page.
MACHINE_KEY = re.compile(
    r"(url|_id$|^id$|_at$|date|time|href|coords|lat|lon|slug|status|mode|type|currency|code|lang)",
    re.IGNORECASE)

# Free-text fields the page deliberately does not print, each with the reason. A field reaches
# this list by a decision someone can read, never by being forgotten -- and an entry that starts
# showing up on the page fails below, so the list cannot rot into a second set of exemptions.
NOT_PAGE_COPY = {
    "$.trip.destination_coords[].label":
        "a geocoder lookup key for the map figure, not a caption",
    "$.intake_context.source_note":
        "evidence for the save gate about how requirements were collected",
    "$.days[].dining[].venue_hours":
        "superseded on the page by venue_hours_by_weekday, which prints the meal's own weekday",
    "$.transport_overview.headline":
        "not read: the renderer composes the overview headline from the legs (audit 2026-10-09)",
    "$.trip.traveler_preferences.pace":
        "duplicates trip.pace, which the page prints (audit 2026-10-09)",
}


def _shape(path: str) -> str:
    return re.sub(r"\[\d+\]", "[]", path)


def sweep(plan: dict) -> tuple[dict[str, str], str]:
    """Prefix every free-text leaf with its own token; return {token: path} and the page."""
    marked = copy.deepcopy(plan)
    raw = json.dumps(plan, ensure_ascii=False)
    tokens: dict[str, str] = {}

    def walk(node: object, path: str) -> None:
        if isinstance(node, dict):
            for key, value in node.items():
                if key.startswith("_"):
                    continue
                if (isinstance(value, str) and len(value) >= 12 and " " in value
                        and not MACHINE_KEY.search(key) and not value.startswith("http")
                        and "TODO" not in value
                        and raw.count(json.dumps(value, ensure_ascii=False)) == 1):
                    token = f"QZ{len(tokens):04d}X"
                    tokens[token] = f"{path}.{key}"
                    node[key] = f"{token} {value}"
                else:
                    walk(value, f"{path}.{key}")
        elif isinstance(node, list):
            for index, value in enumerate(node):
                walk(value, f"{path}[{index}]")

    walk(marked, "$")
    return tokens, renderer.render(marked)


def sweep_cases() -> None:
    for name, plan in (("self-drive", SELF_DRIVE), ("booking-ready", BOOKING_READY)):
        tokens, page = sweep(plan)
        check(f"the {name} sweep has something to sweep", len(tokens) >= 40, len(tokens))
        shown = htmlgate.visible_text(page)
        unshown = sorted({_shape(path) for token, path in tokens.items() if token not in shown})
        forgotten = [path for path in unshown if path not in NOT_PAGE_COPY]
        check(f"every free-text field of the {name} fixture reaches the page", not forgotten,
              "never printed: " + ", ".join(forgotten))
        if name == "self-drive":
            swept = {_shape(path) for path in tokens.values()}
            stale = [path for path in NOT_PAGE_COPY if path in swept and path not in unshown]
            check("every NOT_PAGE_COPY entry is still absent from the page", not stale,
                  "now printed, so drop the exemption: " + ", ".join(stale))


# --- 2. the three fields the sweep found -------------------------------------------------------

def with_scheduled_release(plan: dict) -> dict:
    plan = copy.deepcopy(plan)
    ticket = plan["booking_options"]["attraction_tickets"][0]
    ticket["sale_opens_at"] = {
        "status": "scheduled_release", "opens_at": "2026-10-10T09:30:00+01:00",
        "basis": "The castle's ticket page says timed tickets for a date are released at 09:30 "
                 "seven days ahead."}
    return plan


def chinese(plan: dict) -> dict:
    plan = copy.deepcopy(plan)
    plan["trip"]["language"] = "zh-CN"
    return plan


def ticket_card(page: str) -> str:
    match = re.search(r'<article class="option" data-option-kind="ticket"[^>]*>.*?</article>', page,
                      re.DOTALL)
    return match.group(0) if match else ""


def renderer_english(page: str, plan: dict) -> list[str]:
    flags = plan_flags.derive_html_flags(plan)
    return [e for e in htmlgate.validate(page, flags.expected_days, set(flags.required_booking_types),
                                         flags.transport_mode, [],
                                         require_unverified_banner=flags.require_unverified_banner)
            if "English" in e]


def field_cases() -> None:
    plan = with_scheduled_release(SELF_DRIVE)
    basis = plan["booking_options"]["attraction_tickets"][0]["sale_opens_at"]["basis"]
    for language, variant in (("English", plan), ("Chinese", chinese(plan))):
        card = htmlgate.visible_text(ticket_card(renderer.render(variant)))
        check(f"a scheduled release prints its date and time on the ticket card ({language})",
              "2026-10-10 09:30" in card, card[:400])
        check(f"and the sentence saying where that came from ({language})", basis in card, card[:400])
    page = renderer.render(chinese(plan))
    check("a Chinese ticket card adds no renderer English", not renderer_english(page, chinese(plan)),
          renderer_english(page, chinese(plan))[:2])

    # Every status word is translated, each one checked on its own: a table with one missing entry
    # still passes a test that tries only the status that has one.
    for status in (*renderer.TICKET_SALE_ENGLISH, "probably_fine"):
        variant = chinese(plan)
        variant["booking_options"]["attraction_tickets"][0]["sale_opens_at"]["status"] = status
        page = renderer.render(variant)
        check(f"a Chinese ticket card translates the {status!r} sale status",
              not renderer_english(page, variant), renderer_english(page, variant)[:2])

    # A ticket on sale now still says so, with its basis: "always_available" is the value someone
    # types without opening anything, so the page shows what it rests on.
    standing = SELF_DRIVE["booking_options"]["attraction_tickets"][0]["sale_opens_at"]
    card = htmlgate.visible_text(ticket_card(renderer.render(SELF_DRIVE)))
    check("an always-available ticket prints its basis", standing["basis"] in card, card[:400])

    # Budget note and detour reason, in both languages.
    detour = copy.deepcopy(SELF_DRIVE)
    detour["days"][1]["route"]["segments"][0]["detour_reason"] = (
        "Via the Hermitage so the children can stretch their legs halfway.")
    for language, variant in (("English", detour), ("Chinese", chinese(detour))):
        shown = htmlgate.visible_text(renderer.render(variant))
        check(f"the budget note reaches the page ({language})", SELF_DRIVE["budget"]["note"] in shown)
        check(f"a segment's detour reason reaches the page ({language})",
              "Via the Hermitage so the children" in shown)


# --- 3. machinery that must not be page text ---------------------------------------------------

def source_type_cases() -> None:
    for language, variant in (("English", SELF_DRIVE), ("Chinese", chinese(SELF_DRIVE))):
        page = renderer.render(variant)
        values = {option.get("source_type") for options in variant["booking_options"].values()
                  if isinstance(options, list) for option in options
                  if isinstance(option, dict) and option.get("source_type")}
        shown = htmlgate.visible_text(page)
        check(f"the fixture's options carry source_type values to test ({language})", len(values) >= 3,
              values)
        check(f"no booking card prints its source_type as text ({language})",
              not [value for value in values if value in shown],
              [value for value in values if value in shown])
        check(f"but still rides on the card for machines ({language})",
              'data-source-type="operator_and_comparison_platform"' in page)


def identifier_cases() -> None:
    found = htmlgate.machine_identifiers
    check("a token glued to Chinese text is found", "source_type" in found("字段source_type未填"),
          found("字段source_type未填"))
    check("one slash does not hide the rest of a Chinese clause",
          "source_type" in found("比例5/6，见：source_type"), found("比例5/6，见：source_type"))
    check("links, addresses and file paths are still not reported",
          not found("详见 https://example.com/a_b_c?group_adults=2 或 a_b@x.com 和 scripts/plan_x.py"),
          found("详见 https://example.com/a_b_c?group_adults=2 或 a_b@x.com 和 scripts/plan_x.py"))


def leaked(plan: dict, text: str) -> list[str]:
    """Errors from the delivery checks for a page whose first activity detail carries `text`."""
    plan = copy.deepcopy(plan)
    plan["days"][0]["activities"][0]["detail"] = text
    page = renderer.render(plan)
    flags = plan_flags.derive_html_flags(plan)
    return [e for e in htmlgate.validate(page, flags.expected_days, set(flags.required_booking_types),
                                         flags.transport_mode, [],
                                         require_unverified_banner=flags.require_unverified_banner,
                                         plan=plan)
            if "plan's own" in e]


def vocabulary_cases() -> None:
    # The plan's own keys and ids are this skill's machinery by construction, so on a delivered
    # page they are an error, not a note: no traveller sentence contains `cross_border_or_
    # restriction_note` or `acc-pit-1`, and neither needs a word list to recognise.
    check("a plan key printed as text fails delivery",
          leaked(SELF_DRIVE, "See cross_border_or_restriction_note before driving."),
          "no error")
    check("a plan id printed as text fails delivery",
          leaked(SELF_DRIVE, "Ask for acc-pit-1 at the desk."), "no error")
    check("a plan key glued to Chinese text fails delivery",
          leaked(chinese(SELF_DRIVE), "字段venue_hours_by_weekday未填。"), "no error")
    for prose in ("Boarding gate 12; step-free access; check-in from 15:00 at KGX.",
                  "Day-trip by car; the A9 is a self-drive road.",
                  "Wi-Fi network hotel_guest, see https://example.com/stay_info"):
        check(f"ordinary prose is not a vocabulary leak: {prose!r}", not leaked(SELF_DRIVE, prose),
              leaked(SELF_DRIVE, prose))


def save_path_cases() -> None:
    """The delivery path runs the identifier check and prints what it finds."""
    import save_trip_deliverables as save_module  # noqa: PLC0415

    def save(plan: dict, slug: str) -> tuple[int, str]:
        with tempfile.TemporaryDirectory() as tmp:
            plan_path = Path(tmp) / "plan.json"
            plan_path.write_text(json.dumps(plan, ensure_ascii=False), encoding="utf-8")
            argv, out = sys.argv, io.StringIO()
            sys.argv = ["save_trip_deliverables.py", str(plan_path), "--workspace",
                        str(Path(tmp) / "ws"), "--unverified", "--slug", slug]
            try:
                with contextlib.redirect_stdout(out), contextlib.redirect_stderr(out):
                    code = save_module.main()
            finally:
                sys.argv = argv
            return code, out.getvalue()

    plain = copy.deepcopy(SELF_DRIVE)
    plain["days"][0]["activities"][0]["detail"] = "Basis: member_state_residence_permit."
    code, out = save(plain, "note")
    check("a free-text identifier still saves", code == 0, out[-600:])
    check("and the save prints it as a note", "member_state_residence_permit" in out, out[-600:])

    machinery = copy.deepcopy(SELF_DRIVE)
    machinery["days"][0]["activities"][0]["detail"] = "Ask for acc-pit-1 at the desk."
    code, out = save(machinery, "leak")
    check("a plan id on the page refuses the save", code != 0 and "acc-pit-1" in out, out[-600:])


# --- 4. the plan-age line can be read ----------------------------------------------------------

def _luminance(hex_colour: str) -> float:
    value = hex_colour.lstrip("#")
    if len(value) == 3:
        value = "".join(c * 2 for c in value)
    channels = [int(value[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    linear = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in channels]
    return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]


def _contrast(a: str, b: str) -> float:
    light, dark = sorted((_luminance(a), _luminance(b)), reverse=True)
    return (light + 0.05) / (dark + 0.05)


def contrast_cases() -> None:
    page = renderer.render(SELF_DRIVE)
    style = "".join(re.findall(r"<style>(.*?)</style>", page, re.DOTALL))
    declarations: dict[str, str] = {}
    for body in re.findall(r"(?:^|})\s*\.plan-age\s*\{([^}]*)\}", style):
        for prop, value in re.findall(r"([\w-]+)\s*:\s*([^;]+)", body):
            declarations[prop.strip()] = value.strip()

    def resolve(value: str | None) -> str | None:
        while value and value.startswith("var("):
            name = value[4:-1].strip()
            found = re.findall(re.escape(name) + r"\s*:\s*(#[0-9a-fA-F]{3,6})", style)
            value = found[-1] if found else None
        return value

    fg = resolve(declarations.get("color"))
    bg = resolve(declarations.get("background") or declarations.get("background-color"))
    check("the plan-age line sets a background of its own rather than sitting on the hero",
          bool(bg and bg.startswith("#")),
          f"declarations {declarations}: on the hero gradient this measured 1.0-2.0:1")
    if fg and bg and bg.startswith("#"):
        check("and its text reaches 4.5:1 on it", _contrast(fg, bg) >= 4.5,
              f"{fg} on {bg} = {_contrast(fg, bg):.2f}:1")
    check("an empty plan-age line (no script, nothing to say) draws no empty chip",
          re.search(r"\.plan-age:empty\s*\{[^}]*display\s*:\s*none", style), "no :empty rule")


def main() -> int:
    sweep_cases()
    field_cases()
    source_type_cases()
    identifier_cases()
    vocabulary_cases()
    save_path_cases()
    contrast_cases()
    if failures:
        print(f"FAILED {len(failures)} case(s):\n", file=sys.stderr)
        for failure in failures:
            print(f"--- {failure}\n", file=sys.stderr)
        return 1
    print("page field cases passed")
    return 0


def test_page_shows_its_fields() -> None:
    assert main() == 0


if __name__ == "__main__":
    raise SystemExit(main())

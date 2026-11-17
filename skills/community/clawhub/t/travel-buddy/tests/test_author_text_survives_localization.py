#!/usr/bin/env python3
"""Localization translates the renderer's words and never the author's.

A non-English page is produced by rendering English and then substituting: a table of renderer
strings ("Provider: ", "Opening hours: ", " reviews") and a set of unit rules ("(\\d+) minutes?",
"km", "1h 30m"). Every one of them ran over the whole page, author text included. Found on
2026-10-09 in a Chinese render of the self-drive fixture -- "no walk longer than 30 minutes" came
out as 「no walk longer than 30分钟」 -- and a probe then put each substitution key into an
activity's detail: all 96 rewrote it. "Provider recommends the early slot" printed as 「供应商
recommends the early slot」; a quoted "4.5 (1,203 reviews)" lost its English mid-quote.

The file had met this class before, one rule at a time: enum_cell's docstring records the word
"researched" translated inside an author's sentence, and localize_enum_values scopes its budget
rule for the same reason. Fixing it rule by rule leaves the next rule unfixed, so the fix is
structural: a value from the plan is marked where it is escaped, localization sets the marked
text aside before any rule runs, and puts it back untouched afterwards.

Run:  python tests/test_author_text_survives_localization.py
      python -m pytest tests/test_author_text_survives_localization.py
"""

from __future__ import annotations

import copy
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import plan_flags  # noqa: E402
import render_final_trip_html as renderer  # noqa: E402
import validate_trip_html as htmlgate  # noqa: E402

SELF_DRIVE = json.loads((ROOT / "tests" / "self-drive-fixture.json").read_text(encoding="utf-8"))
BOOKING_READY = json.loads((ROOT / "tests" / "booking-ready-fixture.json").read_text(encoding="utf-8"))
FRENCH_LABELS = json.loads(
    (ROOT / "templates" / "renderer-ui-labels.example.json").read_text(encoding="utf-8"))

# One sentence an author could plausibly write -- or quote from a venue's English page -- that
# contains a unit rule's input and several of the table's keys at once.
BATTERY = ("Allow 30 minutes, 45 min or 1h 30m; Walk 5 min, 12 km, 2 transfer(s). "
           "Provider: the castle. Rating: 4.5 (1,203 reviews). Opening hours: 09:30-17:30. "
           "Fallback: taxi.")

MACHINE_KEY = re.compile(
    r"(url|_id$|^id$|_at$|date|time|href|coords|lat|lon|slug|status|mode|type|currency|code|lang)",
    re.IGNORECASE)

failures: list[str] = []


def check(label: str, condition: object, detail: object = "") -> None:
    if not condition:
        failures.append(f"{label}\n    {detail}")


def in_language(plan: dict, language: str) -> dict:
    plan = copy.deepcopy(plan)
    plan["trip"]["language"] = language
    if language.startswith("fr"):
        plan["ui_labels"] = FRENCH_LABELS
    return plan


def free_text_paths(plan: dict) -> list[tuple]:
    """Paths (as key tuples) to every free-text leaf the page prints, chosen as the field sweep in
    test_page_shows_its_fields.py chooses them: prose-shaped, machine keys skipped, cross-referenced
    values skipped because rewriting one copy breaks the reference rather than testing the page."""
    raw = json.dumps(plan, ensure_ascii=False)
    found: list[tuple] = []

    def walk(node: object, path: tuple) -> None:
        if isinstance(node, dict):
            for key, value in node.items():
                if key.startswith("_"):
                    continue
                if (isinstance(value, str) and len(value) >= 12 and " " in value
                        and not MACHINE_KEY.search(key) and not value.startswith("http")
                        and raw.count(json.dumps(value, ensure_ascii=False)) == 1):
                    found.append((*path, key))
                else:
                    walk(value, (*path, key))
        elif isinstance(node, list):
            for index, value in enumerate(node):
                walk(value, (*path, index))

    walk(plan, ())
    return found


def set_path(plan: dict, path: tuple, value: str) -> None:
    node = plan
    for step in path[:-1]:
        node = node[step]
    node[path[-1]] = value


def intact(page: str, opener: str, sentence: str) -> tuple[bool, str]:
    """Every occurrence of `opener` on the page starts the whole `sentence`, escaped.

    EVERY occurrence: a field printed twice (text, and an alt, title or data attribute) must not pass
    because one copy survived while the other did not.
    """
    escaped_opener = html.escape(opener, quote=True)
    starts = [m.start() for m in re.finditer(re.escape(escaped_opener), page)]
    broken = [s for s in starts if not page.startswith(html.escape(sentence, quote=True), s)]
    if starts and not broken:
        return True, ""
    at = broken[0] if broken else 0
    return False, html.unescape(page[at:at + 260]) if starts else "not printed at all"


def every_field_keeps_the_authors_words() -> None:
    """Every free-text field at once, one render per language: each carries its own marker."""
    # Skip the fields the page deliberately never prints (test_page_shows_its_fields.NOT_PAGE_COPY).
    hidden = {"destination_coords", "source_note", "headline", "venue_hours"}
    for name, plan in (("self-drive", SELF_DRIVE), ("booking-ready", BOOKING_READY)):
        paths = [p for p in free_text_paths(plan) if not hidden & {str(step) for step in p}
                 and p != ("trip", "traveler_preferences", "pace")]
        check(f"the {name} fixture offers fields to test", len(paths) >= 20, len(paths))
        for language in ("zh-CN", "fr-FR"):
            variant = in_language(plan, language)
            sentences = {}
            for path in paths:
                marker = "/".join(str(step) for step in path)
                sentences[marker] = f"[{marker}] {BATTERY}"
                set_path(variant, path, sentences[marker])
            page = renderer.render(variant)
            for marker, sentence in sentences.items():
                ok, seen = intact(page, f"[{marker}]", sentence)
                if not ok:
                    failures.append(f"{language} page rewrote the author's {marker}\n    {seen}")


def every_table_key_keeps_the_authors_words() -> None:
    """Each key of the substitution table inside author text -- the probe that found this.

    One key per free-text field, all in one render, so the probe costs a render rather than a
    hundred.
    """
    labels = renderer.labels_for("zh-CN")
    keys = [key for key in renderer.static_replacements(labels)
            if "<" not in key and ">" not in key and '"' not in key and key.strip()]
    check("the table has keys to probe", len(keys) >= 60, len(keys))
    hidden = {"destination_coords", "source_note", "headline", "venue_hours"}
    paths = [p for p in free_text_paths(SELF_DRIVE) if not hidden & {str(step) for step in p}
             and p != ("trip", "traveler_preferences", "pace")]
    rewritten: list[str] = []
    for offset in range(0, len(keys), len(paths)):
        plan = in_language(SELF_DRIVE, "zh-CN")
        placed = {}
        for index, (key, path) in enumerate(zip(keys[offset:], paths)):
            opener = f"[probe {offset + index}]"
            placed[opener] = (key, f"{opener} before {key} after.")
            set_path(plan, path, placed[opener][1])
        page = renderer.render(plan)
        rewritten += [key for opener, (key, sentence) in placed.items()
                      if not intact(page, opener, sentence)[0]]
    check("no key of the substitution table rewrites author text", not rewritten,
          f"{len(rewritten)} rewritten, e.g. {rewritten[:6]}")


def the_renderers_words_are_still_translated() -> None:
    for name, plan in (("self-drive", SELF_DRIVE), ("booking-ready", BOOKING_READY)):
        variant = in_language(plan, "zh-CN")
        page = renderer.render(variant)
        flags = plan_flags.derive_html_flags(variant)
        english = [e for e in htmlgate.validate(page, flags.expected_days,
                                                set(flags.required_booking_types),
                                                flags.transport_mode, [],
                                                require_unverified_banner=flags.require_unverified_banner,
                                                plan=variant)
                   if "English" in e]
        check(f"the {name} Chinese page carries no renderer English", not english, english[:2])
        # The unit rules still reach the renderer's own figures.
        check(f"the {name} Chinese page still converts the renderer's own minutes",
              "分钟" in htmlgate.visible_text(page))


def the_renderers_fallback_words_are_translated() -> None:
    """A name the plan leaves out is printed as the renderer's own word, which is translated.

    `comparison_platform` is optional; without it a card prints "Direct provider", and that word is
    the renderer's -- fencing it with the author's text would leave it English on every Chinese page.
    """
    plan = in_language(SELF_DRIVE, "zh-CN")
    plan["booking_options"]["accommodations"][0].pop("comparison_platform", None)
    check("the trimmed plan is still a valid plan", not renderer.validate_plan(plan),
          renderer.validate_plan(plan)[:2])
    shown = htmlgate.visible_text(renderer.render(plan))
    check("a missing comparison platform prints the translated fallback",
          "Direct provider" not in shown and renderer.labels_for("zh-CN")["direct_provider_fallback"] in shown,
          [line for line in shown.split("\n") if "provider" in line.lower()][:2])


def a_copied_renderer_sentence_is_still_translated() -> None:
    """An author value that IS the renderer's own sentence, word for word, is translated.

    booking-ready-fixture.json's recheck list holds the renderer's default recheck sentence: it was
    copied from the renderer, not written for this trip, and before the fence it came out in Chinese.
    """
    sentence = "Recheck price, availability, entry requirements, and operating conditions before purchase."
    plan = in_language(SELF_DRIVE, "zh-CN")
    plan["recheck_before_purchase"] = [sentence]
    shown = htmlgate.visible_text(renderer.render(plan))
    check("the renderer's own sentence, copied into the plan, is translated",
          sentence not in shown and renderer.labels_for("zh-CN")["default_recheck"] in shown)


def nothing_the_author_wrote_is_lost() -> None:
    """With the shipped Chinese labels and the example set, every fenced passage comes back.

    restore_author_text() tolerates a missing passage at render time, because a custom label set
    may leave a provider out of a button on purpose. The labels this repository ships may not:
    here a substitution rule that matches across author text without re-emitting it fails.
    """
    for name, plan in (("self-drive", SELF_DRIVE), ("booking-ready", BOOKING_READY)):
        for language in ("en", "zh-CN", "fr-FR"):
            variant = in_language(plan, language)
            page = renderer.decorate_primary_map_links(renderer.render_unlocalized(variant), variant)
            aside, kept = renderer.set_author_text_aside(page)
            check(f"the {name} {language} page has author passages to protect", len(kept) >= 20,
                  len(kept))
            lost: list[str] = []
            renderer.restore_author_text(
                renderer._localize_renderer_text(aside, language, variant.get("ui_labels")),
                kept, lost)
            check(f"no author passage is lost on the {name} {language} page", not lost, lost[:4])


def the_gate_does_not_blame_the_renderer_for_an_authors_quote() -> None:
    """An English quote on a Chinese page is the author's, and the delivery gate knows it."""
    plan = in_language(SELF_DRIVE, "zh-CN")
    plan["days"][0]["activities"][0]["detail"] = "Sign at the gate: Opening hours: 09:30-17:30. Free time after."
    page = renderer.render(plan)
    flags = plan_flags.derive_html_flags(plan)
    with_plan = [e for e in htmlgate.validate(page, flags.expected_days, set(flags.required_booking_types),
                                              flags.transport_mode, [],
                                              require_unverified_banner=flags.require_unverified_banner,
                                              plan=plan) if "English" in e]
    check("with the plan, an author's English quote is not renderer English", not with_plan, with_plan)
    # The renderer's own word is still caught when it really is left in English.
    check("the Chinese budget heading is where this case expects it", "<h2>预算概览</h2>" in page)
    broken = page.replace("<h2>预算概览</h2>", "<h2>Budget at a glance</h2>", 1)
    caught = [e for e in htmlgate.validate(broken, flags.expected_days, set(flags.required_booking_types),
                                           flags.transport_mode, [],
                                           require_unverified_banner=flags.require_unverified_banner,
                                           plan=plan) if "English" in e]
    check("and the renderer's own English is still caught with the plan", caught, "nothing caught")


def no_marker_reaches_any_page() -> None:
    for name, plan in (("self-drive", SELF_DRIVE), ("booking-ready", BOOKING_READY)):
        for language in ("en", "zh-CN", "fr-FR"):
            page = renderer.render(in_language(plan, language))
            check(f"no protection marker survives on the {name} {language} page",
                  "" not in page and "" not in page)
    # An author value that already contains the marker characters cannot open or close a region.
    plan = in_language(SELF_DRIVE, "zh-CN")
    plan["days"][0]["activities"][0]["detail"] = "odd  text  with 30 minutes"
    page = renderer.render(plan)
    check("marker characters typed into a plan are dropped, and the text still survives",
          "odd  text  with 30 minutes" in page and "" not in page and "" not in page,
          re.findall(r"odd.{0,40}", page)[:1])


def main() -> int:
    every_field_keeps_the_authors_words()
    every_table_key_keeps_the_authors_words()
    the_renderers_words_are_still_translated()
    the_renderers_fallback_words_are_translated()
    a_copied_renderer_sentence_is_still_translated()
    nothing_the_author_wrote_is_lost()
    the_gate_does_not_blame_the_renderer_for_an_authors_quote()
    no_marker_reaches_any_page()
    if failures:
        print(f"FAILED {len(failures)} case(s):\n", file=sys.stderr)
        for failure in failures[:40]:
            print(f"--- {failure}\n", file=sys.stderr)
        return 1
    print("author text survives localization")
    return 0


def test_author_text_survives_localization() -> None:
    assert main() == 0


if __name__ == "__main__":
    raise SystemExit(main())

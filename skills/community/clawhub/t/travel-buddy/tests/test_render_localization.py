#!/usr/bin/env python3
"""Regression tests for the budget-figure half of scripts/render_final_trip_html.py.

`validate_trip_html.py` fails a non-English page that prints renderer-owned English, and that
gate is what caught the original defect: the budget breakdown table read "市内交通: €47–62"
while the chart directly above it read "local_transport 54" -- the same fact, in two languages,
because `budget_bar()` was handed raw category keys.

The repair is a rewrite pass over generated markup, which is the kind of thing that works on the
page it was written against and quietly damages the next one. Both directions are asserted here:
the figure must be translated, and everything outside it must not be.

Network-free by construction.
"""

from __future__ import annotations

import importlib.util
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

BUDGET_FIGURE = (
    '<figure class="pv-figure pv-budget">'
    '<svg role="img" aria-label="占比: flight 225; accommodation 320; local_transport 54">'
    '<title>占比</title></svg>'
    '<div class="pv-keys">'
    '<span class="pv-key pv-key-0">flight 225</span>'
    '<span class="pv-key pv-key-3">local_transport 54</span>'
    '<span class="pv-key pv-key-4">fuel_tolls_parking 12</span>'
    '</div><figcaption>占比</figcaption></figure>'
)
# Author prose that happens to look exactly like the figure's alt text. An unscoped version of
# the rewrite translated the first two entries here and left the third, because only the first
# two were followed by a semicolon -- half a sentence in each language.
PROSE = '<p class="meta">分类如下: food 120; accommodation 300; local_transport 54</p>'
MACHINE = ('<td data-budget-category="local_transport">x</td>'
           '<a href="https://example.invalid/?c=flight 1">flight 1</a>')


def load(name: str):
    sys.path.insert(0, str(ROOT / "scripts"))
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module




def _stamp_notes(validate_html, page: str) -> list[str]:
    """Run the page validator purely to collect its notes."""
    notes: list[str] = []
    validate_html.validate(page, 1, {"hotel"}, "public-transit", notes)
    return notes


def check_traveller_preferences(render, check) -> None:
    """What the traveller asked for has to reach the page, not just the JSON.

    Measured with canary strings pushed through the whole save path: avoid_list, each
    avoid_list_handling.how_avoided, and the natural/cultural subtypes were all present in the plan
    and none of them appeared in the HTML. check_plan_consistency meanwhile *required* every avoid
    entry to carry a handling entry -- so the gate demanded an answer the traveller was never shown,
    which is the defect this skill names in its own words about ratings: stored and never shown is
    the same as never gathered. These canaries are the backstop.
    """
    import copy, json  # noqa: PLC0415
    validate_html = load("validate_trip_html")
    base = json.loads((ROOT / "tests" / "booking-ready-fixture.json").read_text(encoding="utf-8"))

    def rendered(language="en", labels=None, stated=True):
        plan = copy.deepcopy(base)
        plan["trip"]["language"] = language
        if labels is not None:
            plan["ui_labels"] = labels
        prefs = plan["trip"]["traveler_preferences"]
        if stated:
            prefs["avoid_list"] = ["CANARYAVOID red-eye arrivals"]
            prefs["avoid_list_handling"] = [{"item": "CANARYAVOID red-eye arrivals",
                                             "how_avoided": "CANARYHOW only daytime buses."}]
            prefs["human_cultural_subtypes"] = ["CANARYCULTURE neighbourhood walking"]
            prefs["natural_subtypes"] = ["CANARYNATURE riverside"]
        else:
            for field in ("avoid_list", "avoid_list_handling",
                          "human_cultural_subtypes", "natural_subtypes"):
                prefs[field] = []
        return render.render(plan)

    page = rendered()
    for token, what in (("CANARYAVOID", "the avoid-list the traveller wrote"),
                        ("CANARYHOW", "what keeps each avoided thing out"),
                        ("CANARYCULTURE", "the cultural subtypes they chose"),
                        ("CANARYNATURE", "the natural subtypes they chose")):
        check(f"{what} reaches the page", token in page,
              "carried in the plan JSON and never rendered")

    check("no panel is drawn when the traveller stated none of it",
          "traveller-preferences" not in rendered(stated=False),
          "an empty section is furniture, not information")

    # Same terms as the constraints panel: the label keys stay optional so no saved label set is
    # invalidated outright, but the English is caught rather than shipped to a non-English reader.
    zh = render.labels_for("zh-CN")
    older = {k: v for k, v in zh.items() if not k.startswith("preferences_")}
    leaked = validate_html.untranslated_renderer_text(rendered("fr", older, stated=True))
    check("an outdated label set fails loudly rather than printing English",
          any("asked for" in item or "Asked to avoid" in item for item in leaked), str(leaked))
    check("an outdated label set is no burden when the panel is not drawn",
          not validate_html.untranslated_renderer_text(rendered("fr", older, stated=False)))
    check("a current label set localizes the panel",
          not validate_html.untranslated_renderer_text(rendered("fr", zh, stated=True)))

    # The gate stamp. Every gate here is a script and a script runs only when called, so a
    # hand-written page bypasses all of them; nothing in the scripts can fix that, because the
    # enforcement point is upstream of them. What the page can do is carry the evidence.
    # save_trip_deliverables.py stamped gates_passed into the plan JSON and it stopped there --
    # the same gap this repo closed for the unverified banner, on the grounds that a flag stored
    # only in JSON never reaches the person holding the itinerary at an airline counter.
    def with_stamp(language="en", labels=None, checks=22):
        plan = copy.deepcopy(base)
        plan["trip"]["language"] = language
        if labels is not None:
            plan["ui_labels"] = labels
        if checks is not None:
            plan["gates_passed"] = {"checks": checks,
                                    "checked_by": "check_plan_consistency.PLAN_CHECKS"}
        return render.render(plan)

    stamped = with_stamp()
    check("a gated page carries the stamp where a reader can see it",
          'data-gates-checks="22"' in stamped and "Structure checks passed: " in stamped,
          "the plan JSON recorded the gates and the page said nothing")
    check("the stamp says what it does NOT mean",
          "never that its facts are true" in stamped,
          "22 checks read as 'fact-checked' is worse than no stamp at all")
    check("an ungated render carries no stamp",
          "data-gates-checks" not in with_stamp(checks=None),
          "presence is the signal; a stamp on an ungated page destroys it")
    check("validate_trip_html notices a page with no stamp",
          any("no gate stamp" in note for note in _stamp_notes(validate_html, with_stamp(checks=None))),
          "one command has to be able to answer 'did the gates run on this file'")
    check("and stays quiet on a stamped one",
          not any("no gate stamp" in note for note in _stamp_notes(validate_html, stamped)))
    check("the stamp localizes rather than printing English to a Chinese reader",
          "Structure checks passed: " not in with_stamp("zh-CN"),
          "renderer-owned English on a non-English page")


def check_source_confidence(render, check) -> None:
    """The source register's confidence value, and the gate that could not see it.

    The defect: render_final_trip_html rendered `{esc(source.get("confidence"), "researched")}` --
    a bare value with an English literal for a fallback -- and validate_trip_html's detector was
    two hand-written tuples of known English strings that had never heard of it. Three DELIVERED
    Chinese pages printed "high" and "medium" in an otherwise fully Chinese register while both
    gates reported `VALID: booking-ready HTML structure passed.` One of them, 拉纳卡, was the only
    gate-stamped plan in the workspace: the best plan there shipped the defect with every light
    green.

    Both halves are asserted, because either alone leaves the failure intact: the value must be
    translated, AND a value that is not must be caught by something that nobody had to remember.
    """
    import copy, json  # noqa: PLC0415
    validate_html = load("validate_trip_html")
    base = json.loads((ROOT / "tests" / "booking-ready-fixture.json").read_text(encoding="utf-8"))

    def rendered(language="zh-CN", confidence="high", drop=False, **overrides):
        plan = copy.deepcopy(base)
        plan["trip"]["language"] = language
        for key, value in overrides.items():
            plan[key] = value
        for source in plan["sources"]:
            if drop:
                source.pop("confidence", None)
            else:
                source["confidence"] = confidence
        return render.render(plan)

    zh = rendered()
    check("a Chinese page shows the confidence in Chinese",
          '<span class="source-confidence" data-source-confidence="high">高</span>' in zh,
          "the register read 「… · high」 to a Chinese reader on three delivered pages")
    check("the machine token survives for the gates that read it",
          'data-source-confidence="high"' in zh,
          "translating the attribute too would break every structural check on the row")
    check("the renderer's OWN fallback is localized, not the English word it used to be",
          '<span class="source-confidence" data-source-confidence="researched">已调研</span>'
          in rendered(drop=True),
          "a plan that records no confidence printed the literal 'researched'")
    check("every level in the enum localizes",
          all(f'data-source-confidence="{level}">{level}<' not in rendered(confidence=level)
              for level in render.SOURCE_CONFIDENCE_LEVELS),
          str([level for level in render.SOURCE_CONFIDENCE_LEVELS
               if f'data-source-confidence="{level}">{level}<' in rendered(confidence=level)]))
    # English has no label set, and until 2026-09-24 that meant the token printed raw. An English
    # page now gets a word from ENGLISH_ENUM_LABELS, while the attribute keeps the token.
    check("an English page prints the confidence as an English word",
          '<span class="source-confidence" data-source-confidence="high">High</span>'
          in rendered(language="en"),
          "the English page printed the machine token")

    # The plan-side constraint. SKILL.md's rule is that a visible-text field is a CLOSED ENUM
    # precisely because an arbitrary string cannot be translated; confidence was the one visible
    # field that had never been constrained.
    def plan_with(confidence):
        plan = copy.deepcopy(base)
        for source in plan["sources"]:
            source["confidence"] = confidence
        return plan

    for value in render.SOURCE_CONFIDENCE_LEVELS:
        check(f"validate_plan accepts the enum member {value!r}",
              not [e for e in render.validate_plan(plan_with(value)) if "confidence" in e])
    dropped = copy.deepcopy(base)
    for source in dropped["sources"]:
        source.pop("confidence", None)
    check("validate_plan accepts a plan that records no confidence at all",
          not [e for e in render.validate_plan(dropped) if "confidence" in e],
          "the field is optional; the renderer supplies the default")
    # "高" was in this list for one round, and it is the reason check_localized_confidence()
    # exists below. It is a hand-localized enum MEMBER, not prose, and refusing it made the one
    # workspace plan that had already solved this problem the one plan that could not render.
    for value in ("primary source; timetable requires recheck", "HIGH", "medium；须由12306复核", 5, ""):
        errors = [e for e in render.validate_plan(plan_with(value)) if "confidence" in e]
        if value == "":
            check("an empty confidence is the same as none, not an error", not errors, str(errors))
        else:
            check(f"validate_plan refuses the unlocalizable value {value!r}", bool(errors),
                  "an unconstrained field that renders visibly is the hole SKILL.md argues against")
            check(f"the refusal of {value!r} names the vocabulary that would work",
                  errors and all(level in errors[0] for level in render.SOURCE_CONFIDENCE_LEVELS),
                  str(errors))
    check("a value the renderer cannot translate is still shown, never swapped for the default",
          "primary source; recheck" in rendered(confidence="primary source; recheck"),
          "silently printing 'researched' would turn an authoring slip into a claim about a source")

    # The day-route mode, found by the same sweep. RENDERER_ENGLISH_MARKUP already had a pattern
    # for this exact shape -- and it spells the heading `<h2>` while the day card uses `<h3>`, so
    # every Chinese itinerary this skill has ever delivered opened its 路线与交通 section with the
    # English words `public-transit` and no gate said anything.
    def with_mode(mode, language="zh-CN"):
        plan = copy.deepcopy(base)
        plan["trip"]["language"] = language
        for day in plan["days"]:
            day["route"]["mode"] = mode
        return render.render(plan)

    check("the day-route mode is translated on a Chinese page",
          '<span class="route-mode" data-route-mode="public-transit">公共交通</span>'
          in with_mode("public-transit"),
          "delivered pages printed `public-transit` at the head of every day card")
    check("a mode written in the trip's own language is left exactly as the author wrote it",
          '<span class="route-mode" data-route-mode="地铁 + 步行">地铁 + 步行</span>'
          in with_mode("地铁 + 步行"),
          "route.mode is free text by contract; real plans write 「步行 + KTEL 东岸公交」")
    check("and that page raises no i18n finding",
          not validate_html.untranslated_renderer_text(with_mode("地铁 + 步行")),
          str(validate_html.untranslated_renderer_text(with_mode("地铁 + 步行"))))
    check("a day that records no mode keeps the old fallback rather than an empty slot",
          "未提供" in with_mode(None))

    # The allergy severity, third of the same family: a closed enum validate_plan has always
    # enforced, printed into a pill with no label key anywhere in the renderer. No delivered plan
    # sets the field, so no artifact ever showed it and no gate ever could.
    def with_severity(severity, language="zh-CN"):
        plan = copy.deepcopy(base)
        plan["trip"]["language"] = language
        plan["trip"]["traveler_constraints"] = {"allergy_severity": severity,
                                                "allergy_card_text": "我对花生严重过敏。"}
        return render.render(plan)

    check("a severe allergy is described in the reader's language",
          '<span class="pill allergy-severity" data-allergy-severity="severe">严重（可致命）</span>'
          in with_severity("severe"),
          "the panel exists to be read out loud at a restaurant table")
    check("no severity in the enum survives as English",
          not any(f'data-allergy-severity="{value}">{value}<' in with_severity(value)
                  for value in render.ALLERGY_SEVERITIES if value != "none"),
          "ALLERGY_SEVERITIES had no label key at all until this change")
    check("a 'none' severity still draws no row",
          "allergy-severity" not in with_severity("none"),
          "an absent constraint printed as a constraint is noise")


def check_localized_confidence(render, check) -> None:
    """A plan that already stored the localized value must not be refused for storing it.

    Closing sources[].confidence to an enum was right, and the first draft of it made
    plans/2026-09-18-马略卡-帕尔马四日-老城-山间古董火车与索列尔港.json unrenderable: that plan stores 高
    six times and 中 twice, an author doing by hand exactly what the enum now does by
    construction. `validate_plan` answered "source confidence '高' is not one of: high, medium,
    low, researched, unverified" eight times and exited non-zero, so the one plan in the workspace
    that had already solved this problem was the one plan that could no longer be delivered.

    This file's precedent is intake_context_errors, which lives in save_trip_deliverables rather
    than in validate_plan precisely so a new requirement cannot retroactively invalidate plans
    already sitting in a workspace. A plan is a portable document.

    Both edges are asserted, because either alone is a different defect: the localized member is
    accepted AND canonicalized to its token (so the page stays machine-readable and re-localizable
    into a third language), and prose is still refused (so the unclosed-field hole stays shut).
    """
    import copy, json  # noqa: PLC0415
    base = json.loads((ROOT / "tests" / "booking-ready-fixture.json").read_text(encoding="utf-8"))

    def plan_with(confidence, language="zh-CN"):
        plan = copy.deepcopy(base)
        plan["trip"]["language"] = language
        for source in plan["sources"]:
            source["confidence"] = confidence
        return plan

    def confidence_errors(value, language="zh-CN"):
        return [e for e in render.validate_plan(plan_with(value, language)) if "confidence" in e]

    # The alias table itself: built from labels_for, so it must cover the whole enum and collide
    # with nothing. A collision would silently relabel one source's evidence as another's.
    check("every level has a built-in localized spelling that maps back to it",
          all(any(token == level for token in render.SOURCE_CONFIDENCE_ALIASES.values())
              for level in render.SOURCE_CONFIDENCE_LEVELS),
          str(render.SOURCE_CONFIDENCE_ALIASES))
    check("no localized spelling is also a machine token of a DIFFERENT level",
          not (set(render.SOURCE_CONFIDENCE_ALIASES) & set(render.SOURCE_CONFIDENCE_LEVELS)),
          str(set(render.SOURCE_CONFIDENCE_ALIASES) & set(render.SOURCE_CONFIDENCE_LEVELS)))
    # Compared casefolded, because the lookup is: a second built-in table in a cased script must
    # not turn this assertion into a spurious failure the day somebody adds one.
    check("the alias table is exactly the built-in table, not a second hand-written list",
          render.SOURCE_CONFIDENCE_ALIASES
          == {render.labels_for("zh-CN")[f"confidence_{level}"].casefold(): level
              for level in render.SOURCE_CONFIDENCE_LEVELS},
          str(render.SOURCE_CONFIDENCE_ALIASES))
    check("a value padded with an ideographic space is still the value somebody typed",
          render.canonical_enum_value("　高　", render.SOURCE_CONFIDENCE_LEVELS,
                                      render.SOURCE_CONFIDENCE_ALIASES) == "high",
          "a hand-edited CJK plan is exactly where U+3000 comes from")

    for spelling, token in sorted(render.SOURCE_CONFIDENCE_ALIASES.items()):
        check(f"validate_plan accepts the hand-localized member {spelling!r}",
              not confidence_errors(spelling),
              str(confidence_errors(spelling)))
        page = render.render(plan_with(spelling))
        check(f"{spelling!r} renders with its MACHINE token in the data attribute",
              f'data-source-confidence="{token}">{spelling}<' in page,
              "storing the localized word must not push it into the attribute the gates read")

    # Padding and a mixed register, because a hand-typed value is a hand-typed value.
    check("surrounding whitespace does not turn a good value into a refusal",
          not confidence_errors("  高  "), str(confidence_errors("  高  ")))
    # A four-row register in two spellings at once, because the workspace plan that forced this
    # is not uniform either and a one-source fixture would prove nothing about the second row.
    mixed = copy.deepcopy(base)
    mixed["trip"]["language"] = "zh-CN"
    template = copy.deepcopy(mixed["sources"][0])
    mixed["sources"] = []
    for index, value in enumerate(("高", "medium", "中", "researched")):
        row = copy.deepcopy(template)
        row["confidence"] = value
        row["url"] = f"{template['url']}?row={index}"
        row["claim_or_decision_supported"] = f"第 {index} 行证明的事"
        mixed["sources"].append(row)
    mixed_errors = [e for e in render.validate_plan(mixed) if "confidence" in e]
    mixed_page = render.render(mixed) if not mixed_errors else ""
    check("a register mixing localized and machine spellings validates",
          not mixed_errors, str(mixed_errors))
    check("and every row of it reaches the reader in Chinese, token intact",
          all(f'data-source-confidence="{token}">{word}<' in mixed_page
              for token, word in (("high", "高"), ("medium", "中"), ("researched", "已调研"))),
          mixed_page[mixed_page.find("source-register"):][:600])

    # The concession is bounded. Prose is what reopens the hole, and four other plans in the same
    # workspace store exactly this shape.
    for prose in ("primary source; timetable requires recheck", "official",
                  "researched; dynamic", "medium；须由12306复核", "高 (需复核)", "很高"):
        check(f"a qualification wearing a value's clothes is still refused: {prose!r}",
              bool(confidence_errors(prose)),
              "this is the hole the enum was closed to shut")

    # Empty / null / wrong-type, the inputs a hand-edited plan actually produces.
    check("canonical_enum_value answers None for everything that is not a string",
          all(render.canonical_enum_value(value, render.SOURCE_CONFIDENCE_LEVELS,
                                          render.SOURCE_CONFIDENCE_ALIASES) is None
              for value in (None, 5, 0, [], {}, ["high"], True)),
          "a non-string must not be coerced into a plausible level")
    check("source_confidence_token hands back an unrecognised value untouched",
          render.source_confidence_token("primary source") == "primary source"
          and render.source_confidence_token(None) is None
          and render.source_confidence_token(5) == 5,
          "laundering an odd value into a token would print a claim the plan never made")
    empty = copy.deepcopy(base)
    empty["sources"] = []
    check("a plan with no sources at all still validates and renders",
          not [e for e in render.validate_plan(empty) if "confidence" in e]
          and "source-register" in render.render(empty),
          str([e for e in render.validate_plan(empty) if "confidence" in e]))

    # The third language. A plan carrying its own ui_labels must show ITS word, not 高 -- which
    # is the whole reason the token, and not the stored spelling, goes into the page.
    labels = json.loads(
        (ROOT / "templates" / "renderer-ui-labels.example.json").read_text(encoding="utf-8"))
    labels["confidence_high"] = "élevée"
    french = plan_with("高", language="fr-FR")
    french["ui_labels"] = labels
    check("a plan storing 高 renders in the language its own ui_labels declare",
          '<span class="source-confidence" data-source-confidence="high">élevée</span>'
          in render.render(french),
          "the stored spelling would have shipped 高 onto a French page")
    check("but a French plan cannot invent its own value spelling",
          bool(confidence_errors("élevée", language="fr-FR")),
          "ui_labels are author-supplied; using them as a value domain lets any string back in")


def check_optional_label_subscripts(render, check) -> None:
    """An OPTIONAL ui_labels key read with a hard subscript is a KeyError, not a fallback.

    `_apply_replacements` read `labels['round_trip_in']` while `'round_trip_in'` sits in
    OPTIONAL_UI_LABEL_KEYS -- so a label set written before that key existed passes validate_plan
    whole and then raises `KeyError: 'round_trip_in'` inside render(). The renderer produced NO
    PAGE, where the entire point of making a key optional is that one label falls back to English
    and the i18n gate fails that one page loudly. Predates the localization work; found by
    checking every other hard subscript after the first one was reported.

    Asserted twice on purpose. The behavioural check proves this key; the AST check states the
    invariant for every key, so the next optional key added with a subscript fails here instead of
    in a workspace.
    """
    import ast, json  # noqa: PLC0415

    tree = ast.parse((ROOT / "scripts" / "render_final_trip_html.py").read_text(encoding="utf-8"))
    optional = {node.value for assign in ast.walk(tree)
                if isinstance(assign, ast.Assign)
                and any(isinstance(target, ast.Name) and target.id == "OPTIONAL_UI_LABEL_KEYS"
                        for target in assign.targets)
                for node in ast.walk(assign.value)
                if isinstance(node, ast.Constant) and isinstance(node.value, str)}
    check("the AST scan found the optional-key set it is checking against",
          "round_trip_in" in optional and len(optional) > 20, str(sorted(optional)))
    hard = sorted((node.lineno, node.slice.value) for node in ast.walk(tree)
                  if isinstance(node, ast.Subscript)
                  and isinstance(node.value, ast.Name) and node.value.id == "labels"
                  and isinstance(node.slice, ast.Constant)
                  and node.slice.value in optional)
    check("no optional ui_labels key is read with a hard subscript anywhere in the renderer",
          not hard,
          f"labels[<optional key>] raises KeyError instead of falling back: {hard}")

    labels = json.loads(
        (ROOT / "templates" / "renderer-ui-labels.example.json").read_text(encoding="utf-8"))
    removed = labels.pop("round_trip_in")
    check("the shipped example set really did carry the key being removed", bool(removed))
    button = ('<a class="booking-link" data-booking-type="flight" '
              'data-booking-purpose="round-trip-search" href="https://example.invalid/">'
              'Search round trip in Skyscanner — 2026-09-11 to 2026-09-14</a>')
    check("a label set written before the key existed is still a COMPLETE set",
          render.REQUIRED_UI_LABEL_KEYS.issubset(labels),
          "if it were rejected the whole page would drop to English and this would not be a bug")
    try:
        page = render.localize_static_page(button, "fr-FR", labels)
    except KeyError as exc:  # pragma: no cover - the defect this test exists for
        page = ""
        check("rendering survives a label set missing an optional key", False,
              f"KeyError: {exc} -- the renderer produced no page at all")
    if page:
        check("the missing label falls back to the English the renderer emitted",
              "Search round trip in Skyscanner" in page,
              page)
        check("and every other label in the set is still applied",
              "Skyscanner" in page and "2026-09-11" in page, page)
        validate_html = load("validate_trip_html")
        check("the English fallback is LOUD: the i18n gate names it",
              any("Search round trip" in leak for leak in
                  validate_html.untranslated_renderer_text(
                      f'<html lang="fr"><body>{page}</body></html>')),
              str(validate_html.untranslated_renderer_text(
                  f'<html lang="fr"><body>{page}</body></html>')))


def check_enum_reflection_property(render, check) -> None:
    """The i18n gate's vocabulary must be decided by a property, not by a list of exceptions.

    renderer_enum_values() reflected every uppercase machine-token container in the renderer and
    subtracted four names. Three sets of search-URL PARAMETER names were not among them, so
    `origin`, `destination`, `guests`, `rooms`, `travellers`, `check_in`, `check_out`,
    `outbound_date`, `return_date`, `pickup_location`, `pickup_time`, `dropoff_location` and
    `dropoff_time` were error-level "untranslated enum" vocabulary on a gate whose stated promise
    is that it never invents a defect -- 70 reflected values where 57 are enums.

    Adding three names would have fixed the instance. The property is positive now: a constant
    counts when the renderer tests a value for membership in it, which is what "closed enum a plan
    field may hold" MEANS. Asserted from both ends, since a property that admits everything and a
    property that admits nothing both pass a one-sided test.
    """
    validate_html = load("validate_trip_html")
    values, failure = validate_html.renderer_enum_reflection()
    check("the reflection reports no failure on a renderer it can read", not failure, failure)

    for name in ("ALLERGY_SEVERITIES", "ARRIVAL_MODES", "BOOKING_STATES", "BUDGET_CATEGORIES",
                 "ENTRY_STATUSES", "INTAKE_METHODS", "MEAL_TYPES", "PRICE_STATUSES",
                 "ROUTE_MAP_SCOPES", "SOURCE_CONFIDENCE_LEVELS", "TRANSPORT_MODES"):
        missing = sorted(set(getattr(render, name)) - values)
        check(f"{name} is still covered in full", not missing,
              f"a closed enum the renderer validates against dropped out of the gate: {missing}")

    for name in ("REQUIRED_STAY_SEARCH_FIELDS", "REQUIRED_FLIGHT_SEARCH_FIELDS",
                 "REQUIRED_RENTAL_SEARCH_FIELDS"):
        leaked = sorted(set(getattr(render, name)) & values)
        check(f"{name} is not enum vocabulary", not leaked,
              f"URL parameter names read as untranslated enums: {leaked}")
    for word in ("origin", "destination", "guests", "rooms", "travellers"):
        check(f"the ordinary English word {word!r} is not enum vocabulary", word not in values)

    # The property, not the outcome: a set the renderer never tests membership against must not
    # become vocabulary just because it is uppercase and full of lowercase tokens.
    render.INVENTED_STYLE_TOKENS = ("wide", "narrow", "tall")
    try:
        validate_html.renderer_enum_reflection.cache_clear()
        fresh, _ = validate_html.renderer_enum_reflection()
        check("a new non-enum constant is excluded with no edit to the validator",
              not ({"wide", "narrow", "tall"} & fresh),
              "the old exclusion list would have swallowed this until somebody named it")
    finally:
        del render.INVENTED_STYLE_TOKENS
        validate_html.renderer_enum_reflection.cache_clear()

    # And the new way for the gate to go quiet: the vocabulary now depends on the renderer's
    # SOURCE, not only on importing it. A report that still ends in VALID while the check did not
    # run is the failure mode this whole section was written to answer.
    class Moved:
        __file__ = str(ROOT / "scripts" / "no-such-renderer.py")

    original = validate_html.import_renderer
    try:
        validate_html.renderer_enum_reflection.cache_clear()
        validate_html.import_renderer = lambda: Moved()
        broken_values, broken_failure = validate_html.renderer_enum_reflection()
        check("an unreadable renderer source is REPORTED, not silently tolerated",
              bool(broken_failure), "the gate would have run on an empty word list, quietly")
        check("and the failure reaches the page report",
              broken_failure in validate_html.untranslated_renderer_text(
                  '<html lang="zh-CN"><body><p>你好</p></body></html>'),
              broken_failure)
        check("the validator's own contract enums survive a total reflection failure",
              validate_html.ALLOWED_BOOKING_TYPES <= broken_values,
              str(sorted(broken_values)))
    finally:
        validate_html.import_renderer = original
        validate_html.renderer_enum_reflection.cache_clear()


def check_page_age_element(render, check) -> None:
    """The page has to say how old it is, and say it in the reader's language.

    The plan carries fixed dates and the page carries fixed timestamps, so a reader opening it four
    months later sees exactly what a reader opening it the same day sees -- while every price,
    opening hour and entry rule has drifted underneath. The cue is computed when the page is
    OPENED, which means a script; the script is progressive enhancement, so with scripting off the
    element stays empty and the static sentence beside it is already complete.

    Its strings live in data attributes rather than in text, and that is exactly why they are
    checked here: an attribute is renderer-owned text like any other, and a Chinese page carrying
    "Departure is in N day(s)." would leak English through a door the visible-text rules do not
    watch.
    """
    zh = render.labels_for("zh-CN")
    for key, english in (("age_since", "Opened N day(s) after that research."),
                         ("age_until", "Departure is in N day(s)."),
                         ("age_past", "This trip has already started or passed."),
                         ("age_stale", "Prices, opening hours and entry rules drift; treat every "
                                       "figure here as needing a recheck.")):
        check(f"{key} has a Chinese label", zh.get(key) and zh[key] != english,
              f"{zh.get(key)!r}")
        # Optional, for the reason every label added since 2.2 is: a required key rejects every
        # ui_labels set written before it existed and drops the whole page back to English.
        check(f"{key} is optional", key in render.OPTIONAL_UI_LABEL_KEYS,
              "it is required, so an older custom label set now fails and its page loses Chinese")

    page = f'<span id="plan-age" data-age-tpl="Opened N day(s) after that research." ' \
           f'data-until-tpl="Departure is in N day(s)."></span>'
    # static_replacements is the table that owns whole-string renderer text; localize_enum_values
    # handles the closed enums. The age templates are the first kind.
    localized = page
    for needle, replacement in render.static_replacements(zh).items():
        localized = localized.replace(needle, replacement)
    check("the templates are substituted, not left in English",
          "Opened N day" not in localized and "Departure is in" not in localized, localized[:160])
    check("and the substitution puts the Chinese in",
          zh["age_since"] in localized and zh["age_until"] in localized, localized[:160])


def check_structural_i18n_gate(render, check) -> None:
    """The half of the fix that has to survive the NEXT field nobody remembers.

    Appending "high|medium|low" to RENDERER_ENGLISH_TEXT would have closed the reported defect and
    rebuilt the design that caused it: a deny-list fails only English somebody wrote down. These
    cases add a new enum, a new enum level and a new renderer sentence WITHOUT touching a single
    list in validate_trip_html.py, and require the gate to fail anyway.
    """
    import copy, json  # noqa: PLC0415
    validate_html = load("validate_trip_html")
    # The validator imports the renderer by name, so it holds its own module object; patching the
    # instance it actually reads is the only way a test can stand in for "somebody edited the
    # renderer tomorrow". Asserting the handle exists first, because a silently-different object
    # would make every case below vacuously pass.
    renderer = validate_html.import_renderer()
    check("the validator can reach the renderer it validates",
          hasattr(renderer, "static_replacements") and hasattr(renderer, "SOURCE_CONFIDENCE_LEVELS"),
          repr(renderer))
    base = json.loads((ROOT / "tests" / "booking-ready-fixture.json").read_text(encoding="utf-8"))

    def zh_page(**edits):
        plan = copy.deepcopy(base)
        plan["trip"]["language"] = "zh-CN"
        for source in plan["sources"]:
            source.update(edits)
        return renderer.render(plan)

    check("a correctly rendered Chinese page raises nothing",
          not validate_html.untranslated_renderer_text(zh_page()),
          str(validate_html.untranslated_renderer_text(zh_page())))
    check("an English page is not judged at all",
          not validate_html.untranslated_renderer_text(renderer.render(copy.deepcopy(base))),
          "an English page is not judged for untranslated renderer text; its enum tokens get "
          "English words from ENGLISH_ENUM_LABELS instead")

    # The delivered-artifact case: pages saved before enum_cell existed carry no attribute to
    # compare against, so the check that catches them cannot depend on the markup at all.
    legacy = zh_page().replace(
        '<span class="source-confidence" data-source-confidence="high">高</span>', "high")
    check("a page saved by the OLD renderer is still caught",
          any("high" in finding for finding in validate_html.untranslated_renderer_text(legacy)),
          str(validate_html.untranslated_renderer_text(legacy)))

    # An author's own sentence that happens to contain an enum word must NOT be reported. Written
    # without this guard first, and a dining card carrying data-meal="lunch" beside the author's
    # "Sichuan lunch" was reported as an untranslated enum on a page that was translated perfectly.
    prose = zh_page().replace("</main>", '<p class="meta">午餐安排在 Sichuan lunch 附近，high season 除外。</p></main>')
    check("an enum word inside an author sentence is left alone",
          not validate_html.untranslated_renderer_text(prose),
          str(validate_html.untranslated_renderer_text(prose)))

    # What the attribute-versus-text comparison catches that nothing else does: a value emitted
    # through enum_cell whose vocabulary is declared NOWHERE -- no enum constant, no label key, no
    # substitution table entry. The segment check cannot see it (it only knows declared enums) and
    # the identifier sweep only reports it as a note. Written after deleting the layer and finding
    # every test still green, which is the same false-green this whole file exists to refuse.
    invented = zh_page().replace(
        "</main>",
        '<p class="meta">计价方式 · '
        + renderer.enum_cell("fare-basis", "fare-basis", "per_seat_per_leg", "per_seat_per_leg")
        + "</p></main>")
    findings = validate_html.untranslated_renderer_text(invented)
    check("a value emitted through enum_cell is checked even when no constant declares it",
          any("per_seat_per_leg" in finding for finding in findings), str(findings))
    check("and it is an error, not only an advisory note",
          any("prints its own machine value" in finding for finding in findings), str(findings))
    translated = zh_page().replace(
        "</main>",
        '<p class="meta">计价方式 · '
        + '<span class="fare-basis" data-fare-basis="per_seat_per_leg">每人每程</span>'
        + "</p></main>")
    check("the same cell, translated, raises nothing",
          not validate_html.untranslated_renderer_text(translated),
          str(validate_html.untranslated_renderer_text(translated)))

    saved_levels = renderer.SOURCE_CONFIDENCE_LEVELS
    saved_table = renderer.static_replacements
    try:
        # 1. A new level added to an existing enum, with no label key and no edit to any list.
        renderer.SOURCE_CONFIDENCE_LEVELS = saved_levels + ("corroborated",)
        validate_html.renderer_enum_reflection.cache_clear()
        findings = validate_html.untranslated_renderer_text(zh_page(confidence="corroborated"))
        check("a NEW enum level with no translation fails the gate, list untouched",
              any("corroborated" in finding for finding in findings), str(findings))

        # 2. A brand-new enum constant nobody told the validator about.
        #
        # REWRITTEN, and the original claim is kept above rather than deleted because the change
        # is a real narrowing and should be arguable. This case used to bind a constant the
        # renderer merely DECLARES and assert that printing its member failed the page. The
        # vocabulary is no longer "every uppercase tuple of tokens minus four remembered names" --
        # that exclusion list had let three sets of search-URL parameter names through, making
        # `origin`, `destination`, `guests` and `rooms` error-level vocabulary -- it is "every
        # constant the renderer tests a value for membership in", which is what a closed enum IS.
        # A constant nothing validates against is not closed, and this file already refuses to
        # fail a page for an unclosed field: that is the machine_identifiers note two blocks down,
        # in its own words.
        #
        # So the guarantee asserted here is the one that survived and is the one that matters:
        # the day the renderer starts VALIDATING a new constant, this validator covers it with no
        # edit. Nothing here names SHUTTLE_KINDS; the reflection reads it from the renderer.
        renderer.SHUTTLE_KINDS = ("airport_shuttle", "hotel_shuttle")
        shuttle_source = (
            "SHUTTLE_KINDS = ('airport_shuttle', 'hotel_shuttle')\n"
            "def validate_plan(plan):\n"
            "    if plan.get('shuttle_kind') not in SHUTTLE_KINDS:\n"
            "        return ['bad shuttle_kind']\n"
            "    return []\n")
        renderer_source = ROOT / "scripts" / "render_final_trip_html.py"
        saved_reader = validate_html.Path.read_text
        try:
            validate_html.Path.read_text = (  # type: ignore[method-assign]
                lambda self, *args, **kwargs:
                saved_reader(self, *args, **kwargs) + "\n" + shuttle_source
                if self == renderer_source else saved_reader(self, *args, **kwargs))
            validate_html.renderer_enum_reflection.cache_clear()
            page = zh_page().replace("</main>", '<p class="meta">接驳方式 · airport_shuttle</p></main>')
            findings = validate_html.untranslated_renderer_text(page)
            check("a NEW validated enum constant printed raw fails the gate, list untouched",
                  any("airport_shuttle" in finding for finding in findings), str(findings))
        finally:
            validate_html.Path.read_text = saved_reader  # type: ignore[method-assign]
            validate_html.renderer_enum_reflection.cache_clear()

        # The narrowing, asserted rather than left implicit. A constant the renderer declares and
        # never checks anything against contributes no vocabulary, so `hotel_shuttle` printed as
        # bare text is a NOTE from machine_identifiers, not an error. Written down here because a
        # blind spot nobody records is how the last one lasted a whole release.
        validate_html.renderer_enum_reflection.cache_clear()
        unvalidated = zh_page().replace(
            "</main>", '<p class="meta">接驳方式 · hotel_shuttle</p></main>')
        check("a DECLARED-but-unvalidated constant is a note, not an error",
              not any("hotel_shuttle" in finding
                      for finding in validate_html.untranslated_renderer_text(unvalidated))
              and any("hotel_shuttle" in note
                      for note in validate_html.machine_identifier_notes(unvalidated)),
              str(validate_html.untranslated_renderer_text(unvalidated)))

        # 3. A new renderer SENTENCE. The renderer's own substitution table is the authority on
        #    what must never survive; this file reads it rather than keeping a second copy.
        def extended(labels):
            table = dict(saved_table(labels))
            table["Prices shown exclude local tourist tax"] = "Prices shown exclude local tourist tax"
            return table

        renderer.static_replacements = extended
        validate_html.renderer_owned_english.cache_clear()
        page = zh_page().replace(
            "</main>", '<p class="meta">Prices shown exclude local tourist tax</p></main>')
        findings = validate_html.untranslated_renderer_text(page)
        check("a NEW renderer sentence left in English fails the gate, list untouched",
              any("tourist tax" in finding for finding in findings), str(findings))
    finally:
        renderer.SOURCE_CONFIDENCE_LEVELS = saved_levels
        renderer.static_replacements = saved_table
        delattr(renderer, "SHUTTLE_KINDS")
        validate_html.renderer_enum_reflection.cache_clear()
        validate_html.renderer_owned_english.cache_clear()

    check("the caches were restored, so later cases judge the real renderer",
          "corroborated" not in validate_html.renderer_enum_values()
          and not validate_html.untranslated_renderer_text(zh_page()),
          str(validate_html.untranslated_renderer_text(zh_page())))

    # Machine identifiers are reported, but as a NOTE. They come out of free-text plan fields --
    # a booking option's source_type, entry_context.traveler_basis, an anchor's category -- and
    # failing a page for those would fail three delivered plans and new_plan_skeleton.py's own
    # output for a contract nobody has written yet. The day those fields close, promote it.
    leaky = zh_page().replace("</main>", '<p class="meta">依据的身份：member_state_residence_permit</p></main>')
    check("a machine identifier in visible text is reported",
          any("member_state_residence_permit" in note
              for note in validate_html.machine_identifier_notes(leaky)),
          str(validate_html.machine_identifier_notes(leaky)))
    check("but it does not fail the page",
          not validate_html.untranslated_renderer_text(leaky),
          str(validate_html.untranslated_renderer_text(leaky)))
    scaffold = zh_page().replace(
        "</main>", '<p class="meta">供应商：TODO: provider 1 (must own review_url)</p></main>')
    check("a placeholder's own scaffolding is not reported as a defect",
          not validate_html.machine_identifier_notes(scaffold),
          "SKILL.md's rule: an error about a problem that does not exist costs a round trip")
    # English pages used to be skipped, because they printed renderer enums raw on purpose. They
    # get words now, so an underscored token left on one is author text, as on a Chinese page.
    check("an English page's author text is checked for machine identifiers too",
          any("member_state_residence_permit" in note
              for note in validate_html.machine_identifier_notes(
                  renderer.render(copy.deepcopy(base)).replace(
                      "</main>", '<p class="meta">basis: member_state_residence_permit</p></main>'))),
          "an English page's machine identifiers went unreported")

    # The gate must not be able to disappear quietly. It reads the renderer at runtime, so a moved
    # or broken renderer would otherwise turn this check off while the report still says VALID --
    # which is the exact failure mode the whole section was written to answer.
    validate_html.renderer_owned_english.cache_clear()
    saved_import = validate_html.import_renderer
    try:
        def broken():
            raise ImportError("render_final_trip_html moved")

        validate_html.import_renderer = broken
        validate_html.renderer_owned_english.cache_clear()
        findings = validate_html.untranslated_renderer_text(zh_page())
        check("a renderer it cannot read is a loud failure, not a silent pass",
              any("could not read the renderer" in finding for finding in findings), str(findings))
    finally:
        validate_html.import_renderer = saved_import
        validate_html.renderer_owned_english.cache_clear()
        validate_html.renderer_enum_reflection.cache_clear()


def check_english_enum_words(render, check) -> None:
    """An English page prints words, not machine tokens.

    English had no label set, so the localisation pass never ran on an English page and every
    underscored enum reached the reader raw: 'rental_car: £56–82', 'fuel_tolls_parking',
    'rail_or_ground · available' -- measured on a synthetic English road trip, 2026-09-24. The
    English markup is already English; only the tokens need words, from a table that has to cover
    every value of every enum the renderer prints, or the next value added prints raw again.
    """
    table = getattr(render, "ENGLISH_ENUM_LABELS", None)
    check("the renderer has an English word for its enum tokens", isinstance(table, dict),
          repr(type(table)))
    if not isinstance(table, dict):
        return
    wanted = ([f"state_{v}" for v in render.BOOKING_STATES]
              + [f"meal_{v}" for v in render.MEAL_TYPES]
              + [f"arrival_{v}" for v in render.ARRIVAL_MODES]
              + [f"cat_{v}" for v in render.BUDGET_CATEGORIES]
              + [f"confidence_{v}" for v in render.SOURCE_CONFIDENCE_LEVELS]
              + [f"severity_{v}" for v in render.ALLERGY_SEVERITIES]
              + [f"entry_{v}" for v in render.ENTRY_STATUSES]
              + ["mode_self_drive", "mode_public_transit"]
              + [f"access_{v}" for v in ("flight", "accommodation", "attraction_ticket",
                                         "rental_car", "rail_or_ground", "available", "limited",
                                         "unknown")])
    missing = [key for key in wanted if not str(table.get(key) or "").strip()]
    check("every enum value has an English word", not missing, str(missing))

    fixture = json.loads((ROOT / "tests" / "self-drive-fixture.json").read_text(encoding="utf-8"))
    fixture["entry_context"] = {"status": "not_required", "summary": "Domestic trip.",
                                "traveler_basis": "UK residents travelling in the UK",
                                "source_url": "https://www.gov.uk/", "checked_at": "2026-09-12"}
    page = render.render(fixture)
    visible = re.sub(r"<script.*?</script>|<style.*?</style>", " ", page, flags=re.S)
    visible = re.sub(r"<[^>]+>", " ", visible)
    raw = [token for token in ("rental_car", "fuel_tolls_parking", "local_transport",
                               "rail_or_ground", "not_required", "public-transit")
           if re.search(rf"(?<![\w/=.-]){re.escape(token)}(?![\w-])", visible)]
    check("an English page prints no machine token as visible text", not raw, str(raw))
    check("an English page says the category in words", "Rental car" in visible,
          "no 'Rental car' on the page")


def main() -> int:
    render = load("render_final_trip_html")
    failures: list[str] = []

    def check(name: str, condition: bool, detail: str = "") -> None:
        if not condition:
            failures.append(f"{name}\n{detail}")

    check_traveller_preferences(render, check)
    check_source_confidence(render, check)
    check_localized_confidence(render, check)
    check_optional_label_subscripts(render, check)
    check_enum_reflection_property(render, check)
    check_structural_i18n_gate(render, check)
    check_page_age_element(render, check)
    check_english_enum_words(render, check)

    labels = render.labels_for("zh")
    page = render.localize_enum_values(PROSE + BUDGET_FIGURE + MACHINE, labels)

    check("the legend a reader sees is translated",
          '<span class="pv-key pv-key-0">机票 225</span>' in page, page)
    check("an underscored category is translated, not left half-English",
          '<span class="pv-key pv-key-3">市内交通 54</span>' in page, page)
    # Longest-first alternation: "fuel_tolls_parking" must not be matched as "fuel" or "parking".
    check("a multi-word category is matched whole",
          '<span class="pv-key pv-key-4">油费/过路费/停车 12</span>' in page, page)
    check("the alt text a screen reader announces is translated",
          'aria-label="占比: 机票 225; 住宿 320; 市内交通 54"' in page, page)

    check("author prose outside the figure is left alone",
          'food 120; accommodation 300; local_transport 54' in page, page)
    check("data attributes stay machine-readable",
          'data-budget-category="local_transport"' in page, page)
    check("URLs stay machine-readable",
          'https://example.invalid/?c=flight 1' in page, page)

    figure = page.split('pv-budget')[1].split('</figure>')[0]
    check("no category survives untranslated inside the figure",
          not any(f'>{value} ' in figure or f': {value} ' in figure or f'; {value} ' in figure
                  for value in render.BUDGET_CATEGORIES), figure)

    # English still has no label OVERRIDES: labels_for("en") stays empty, so the zh/custom label
    # path -- static replacements and all -- never runs on an English page. What changed on
    # 2026-09-24 is that English pages no longer print raw enum tokens: they get a separate,
    # tokens-only pass with render.ENGLISH_ENUM_LABELS (check_english_enum_words above).
    check("English has no label overrides, so the zh label pass never runs on it",
          not render.labels_for("en"), repr(render.labels_for("en")))

    if failures:
        print(f"FAILED {len(failures)} case(s):\n", file=sys.stderr)
        for failure in failures:
            print(f"--- {failure}\n", file=sys.stderr)
        return 1
    print("all budget-figure localization cases passed")
    return 0


def test_render_localization() -> None:
    assert main() == 0


if __name__ == "__main__":
    raise SystemExit(main())

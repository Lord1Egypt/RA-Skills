#!/usr/bin/env python3
"""Deterministic consistency lint for a Travel Buddy final-trip-plan JSON.

`validate_trip_html.py` proves the page is *well-formed*. Nothing proved it was *true*.
A real run once passed every existing gate while shipping: a day labelled "the lightest
walking day" that was in fact the heaviest, five of six days whose route totals disagreed
with their own segments, a dinner 2.5 km off-route with no transport leg, meals booked at
venues that close three hours earlier, and a budget high case that silently broke the
traveller's stated cap.

A later run passed this checker too, while shipping a day whose own numbers did not fit in
its own clock, a "42 minutes on foot" figure this gate itself REQUIRED to be printed for a
day holding roughly 3.5 hours of walking, and realistic opening hours ("周二至周日 15:00-21:00")
whose weekday prefix made the hours check silently skip -- so the plan was rewarded for
writing the less informative string.

Every one of those is decidable by a program, so it belongs here rather than in prose.
This checker reads the plan JSON only -- no network, no model -- and exits non-zero on any
finding. Checks that need the world (opening hours, fares, entry rules, carrier identity)
cannot live here; they are the parallel-verification stage described in
references/verification.md, whose report this script validates when one is supplied.

Usage:
    python scripts/check_plan_consistency.py <plan.json> --verification <report.json>
    python scripts/check_plan_consistency.py <plan.json> --no-verification-yet
    python scripts/check_plan_consistency.py <plan.json> --emit-walking

`--verification` is required, or waived out loud with `--no-verification-yet`. It used to be
optional, which meant the documented invocation was the disarmed one: check_verification -- the
only thing that reads the report at all -- is not in PLAN_CHECKS and runs nowhere else, so
omitting the flag silently skipped every check that the report covers its required domains and
both audits, that each claims_checked pointer resolves, and that the report is not stale or bound
to a different plan. Measured on a real workspace plan (plans/2027-02-12-阿利坎特...json): bare
reported 13 findings, the same plan handed a report belonging to another trip reported 21.
"""

from __future__ import annotations

import argparse
import ast
import datetime as dt
import functools
import hashlib
import json
import math
import traceback
import urllib.parse
import re
import sys
from pathlib import Path

# The one sibling module this file reads, found beside it rather than wherever an import path
# happens to point: tests load this file by path, and so can any caller that never put scripts/ on
# sys.path. Without this the gate did not import at all in that case -- measured, the standalone run
# of tests/test_plan_consistency.py died on ModuleNotFoundError while the pytest run, which shares
# one sys.path across files, stayed green.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from verification_sections import (  # noqa: E402
    changed_sections,
    delivered_workspace,
    digest_is_current,
    recheck_command,
    resave_command,
    section_of_pointer,
)
import bookings as booking_rules  # noqa: E402 - the booking-record rules (scripts/bookings.py)
import trip_zones  # noqa: E402 - the time-zone rules (scripts/trip_zones.py)

# Route totals are authored in round numbers; allow a little slack before failing.
DURATION_TOLERANCE_MIN = 5
DISTANCE_TOLERANCE_KM = 1.0
COST_TOLERANCE = 1.0
# What is left of a meal window after travel, below which the meal is not a meal. Set at the
# length of a hurried sit-down rather than a generous one, because this gate exists to catch a
# window that is impossible, not one that is merely tight -- a tight lunch is the author's call.
MEAL_MINIMUM_MINUTES = 30

WALK_MODES = {"步行", "walk", "walking", "on foot"}

WEEKDAYS = {
    0: ("周一", "星期一", "monday"),
    1: ("周二", "星期二", "tuesday"),
    2: ("周三", "星期三", "wednesday"),
    3: ("周四", "星期四", "thursday"),
    4: ("周五", "星期五", "friday"),
    5: ("周六", "星期六", "saturday"),
    6: ("周日", "星期日", "sunday"),
}
_CN_WEEKDAY = {"周一": 0, "周二": 1, "周三": 2, "周四": 3, "周五": 4, "周六": 5, "周日": 6,
               "星期一": 0, "星期二": 1, "星期三": 2, "星期四": 3, "星期五": 4, "星期六": 5, "星期日": 6}

# Only a claim *about this day* is checkable. Opening hours ("周一至周六 17:30–22:00") and
# service spans ("周一至周四 07:30–21:00") name other days on purpose, so matching bare
# weekday tokens produces nothing but noise -- and a noisy gate gets switched off, which is
# worse than no gate. Anchor on phrases that actually assert what today is.
_DAY_CLAIM = re.compile(
    r"(?:本日|当日|当天|该日|今天|本行程)\s*(?:为|是)?\s*(周[一二三四五六日]|星期[一二三四五六日])")

# The same rule in English, and deliberately narrower. WEEKDAYS has carried English names since
# the beginning, but only for error messages -- so an English plan could assert "Day 3 is a Monday"
# on a Tuesday and nothing fired. The anchor must bolt the claim to *this* day: "today"/"this day",
# or a day number or ISO date, immediately followed by a copula and a weekday. Anything looser
# catches the honest weekday prose that opening hours are made of ("closed on Monday"), and an
# author who gets flagged for honest hours text deletes the hours text.
_EN_WEEKDAY_NAMES = "|".join(names[2] for names in WEEKDAYS.values())
_EN_DAY_ANCHOR = r"(?:day\s*(?P<daynum>\d{1,2})|(?P<date>\d{4}-\d{2}-\d{2})|today|this day)"
_EN_DAY_CLAIM = re.compile(
    rf"\b{_EN_DAY_ANCHOR}\b[^.!?;\n\"]{{0,24}}?\b(?:is|was|falls on|lands on)\s+(?:an?\s+|the\s+)?"
    rf"(?P<weekday>{_EN_WEEKDAY_NAMES})\b(?![-–—])",
    re.IGNORECASE)
# "Day 2 (Monday)" is the other form that actually appears, and it is tight enough to trust.
_EN_DAY_PAREN = re.compile(
    rf"\b(?:day\s*(?P<daynum>\d{{1,2}})|(?P<date>\d{{4}}-\d{{2}}-\d{{2}}))\s*[(（]\s*"
    rf"(?P<weekday>{_EN_WEEKDAY_NAMES})\s*[)）]",
    re.IGNORECASE)
_EN_WEEKDAY_INDEX = {names[2]: index for index, names in WEEKDAYS.items()}

# "而非最轻的一天" is a correction, not a claim. Strip negated forms before judging.
_NEGATED_LIGHT = re.compile(r"(?:而非|并非|不是|非)\s*(?:本行程)?(?:步行量)?最轻")
_LIGHT_CLAIM = re.compile(r"最轻|最省力|最少的一天|lightest|easiest")
_HEAVY_CLAIM = re.compile(r"最重|最高的一天|heaviest")


def _num(value) -> float:
    return float(value) if isinstance(value, (int, float)) else 0.0


def _obj(value) -> dict:
    """Malformed input must produce a finding, never a traceback -- an operator who sees a
    stack trace learns nothing about their plan and tends to stop running the gate."""
    return value if isinstance(value, dict) else {}


def _seq(value) -> list:
    return value if isinstance(value, list) else []


def _route(day: dict) -> dict:
    return _obj(_obj(day).get("route"))


def _segments(day: dict) -> list:
    return [s for s in _seq(_route(day).get("segments")) if isinstance(s, dict)]


def _is_walk(segment: dict) -> bool:
    return str(segment.get("mode", "")).strip().lower() in {m.lower() for m in WALK_MODES}


def walking_totals(day: dict) -> tuple[int, float]:
    """Scheduled walking a day actually contains: every segment's walking_minutes, and the
    distance of the legs whose mode *is* walking. Terminal/pier walking inside a ferry or
    rail segment counts toward minutes -- it is still the traveller on their feet."""
    segments = _segments(day)
    minutes = int(sum(_num(s.get("walking_minutes")) for s in segments))
    km = round(sum(_num(s.get("distance_km")) for s in segments if _is_walk(s)), 1)
    return minutes, km


def _parse_hhmm(text: str) -> int | None:
    match = re.match(r"^\s*(\d{1,2})[:：](\d{2})\s*$", text)
    if not match:
        return None
    hour, minute = int(match.group(1)), int(match.group(2))
    if hour > 47 or minute > 59:
        return None
    return hour * 60 + minute


def _fmt_hhmm(minutes: int) -> str:
    return f"{minutes // 60:02d}:{minutes % 60:02d}"


def _weekday_tokens() -> dict[str, int]:
    """Every spelling of a weekday a plan may legitimately use, mapped to Python's weekday index."""
    tokens: dict[str, int] = {}
    for index, (cn, _cn_full, en) in WEEKDAYS.items():
        for prefix in ("周", "星期", "礼拜"):
            tokens[prefix + cn[-1]] = index
        tokens[en] = index
        tokens[en[:3]] = index
    for prefix in ("周", "星期", "礼拜"):
        tokens[prefix + "天"] = 6  # 周天 is Sunday in speech and on shop signage
    tokens.update({"tues": 1, "weds": 2, "thur": 3, "thurs": 3})
    # German and Dutch, because this skill's most common cross-border trips are inside western
    # Europe and an author copying hours off a venue's own site copies them in the venue's
    # language. "Mo-Sa 09:00-18:00" is the standard form on German opening-hours pages; without
    # these it parsed as nothing, and the "hours must be machine-checkable" rule then rejected a
    # perfectly honest string. The two-letter forms are safe here because a weekday prefix is only
    # ever matched at the head of an hours string, never inside prose.
    tokens.update({
        "montag": 0, "dienstag": 1, "mittwoch": 2,
        "donnerstag": 3, "freitag": 4,
        "samstag": 5, "sonnabend": 5, "sonntag": 6,
        "maandag": 0, "dinsdag": 1, "woensdag": 2,
        "donderdag": 3, "vrijdag": 4,
        "zaterdag": 5, "zondag": 6,
        # Two-letter forms, but only the ones that mean the same day in every language likely to
        # appear on a European venue's own opening-hours page. AMBIGUOUS_WEEKDAY_TOKENS below
        # holds the three that do not, and they are refused rather than guessed.
        "mo": 0, "mi": 2, "wo": 2, "fr": 4, "vr": 4, "sa": 5, "za": 5, "so": 6, "zo": 6,
        # ma/di/do MUST stay in the tokenizer even though they are ambiguous, because removing them
        # did not make them refuse -- it made them invisible. "Mo-Do 11:00-23:00", the most ordinary
        # German brewpub string there is, then tokenized as "Mo" with unparsed trailing text and the
        # gate reported the venue as open on Mondays only, blocking a correct Wednesday dinner while
        # stating the opposite of the truth. The AMBIGUOUS_WEEKDAY_TOKENS guards below are what
        # refuse them; they can only run on tokens the tokenizer still sees.
        "ma": 0, "di": 1, "do": 3,
        # Japanese, French, Spanish, Italian, Portuguese, Korean. Same reason German and Dutch were
        # added: an author copying hours off a venue's own site copies them in the venue's language,
        # and until a language is in this table its rest day is invisible -- a Kyoto temple or a
        # Paris bistro could be booked on the one day it is shut and every gate stayed green.
        # Single CJK characters (月火水木金土日, 월화수목금토일) are matched without a word boundary,
        # which the tokenizer already handles for Chinese.
        "月曜日": 0, "火曜日": 1, "水曜日": 2, "木曜日": 3, "金曜日": 4, "土曜日": 5, "日曜日": 6,
        "月曜": 0, "火曜": 1, "水曜": 2, "木曜": 3, "金曜": 4, "土曜": 5, "日曜": 6,
        "lundi": 0, "mardi": 1, "mercredi": 2, "jeudi": 3, "vendredi": 4, "samedi": 5, "dimanche": 6,
        "lun": 0, "mar": 1, "mer": 2, "jeu": 3, "ven": 4, "sam": 5, "dim": 6,
        "lunes": 0, "martes": 1, "miércoles": 2, "miercoles": 2, "jueves": 3, "viernes": 4,
        "sábado": 5, "sabado": 5, "domingo": 6,
        "lunedì": 0, "lunedi": 0, "martedì": 1, "martedi": 1, "mercoledì": 2, "mercoledi": 2,
        "giovedì": 3, "giovedi": 3, "venerdì": 4, "venerdi": 4, "sabato": 5, "domenica": 6,
        "segunda-feira": 0, "terça-feira": 1, "terca-feira": 1, "quarta-feira": 2,
        "quinta-feira": 3, "sexta-feira": 4,
        "월요일": 0, "화요일": 1, "수요일": 2, "목요일": 3, "금요일": 4, "토요일": 5, "일요일": 6,
    })
    return tokens


# Three two-letter abbreviations mean different days depending on the language, and a venue writes
# its hours in its own. Reading French "Ma-Sa" (mardi-samedi) as Dutch maandag-zaterdag hands the
# gate a set that says the place opens Mondays, and it then approves a dinner booked on the one day
# the kitchen is shut -- a confidently wrong answer, which is worse than no answer, because the
# "hours are not machine-checkable" error already tells the author exactly what to write instead.
#   ma  nl maandag = Mon   |  fr mardi, es martes, it martedì = Tue
#   di  de Dienstag = Tue  |  fr dimanche = Sun
#   do  de/nl donderdag = Thu | es domingo, it domenica = Sun
AMBIGUOUS_WEEKDAY_TOKENS = frozenset({"ma", "di", "do"})
# An ambiguous token anywhere in the weekday PREFIX makes the whole prefix unusable, not just one
# at the head: "Mo-Do 11:00-23:00" is the most ordinary German brewpub string there is, and its
# ambiguity is in the second half. Bounded to the text before the first time so a venue called
# "Do Forno" or a note reading "Mar 2026" is never mistaken for a weekday.
_AMBIGUOUS_TOKEN = re.compile(
    r"(?<![A-Za-z])(?:{})\.?(?![A-Za-z])".format("|".join(sorted(AMBIGUOUS_WEEKDAY_TOKENS))),
    re.IGNORECASE)
_FIRST_TIME = re.compile(r"\d{1,2}[:：]\d{2}")
# What may legitimately follow a weekday prefix: time windows, the separators between them,
# and nothing else. Any other word means the string says something this parser does not
# understand, and guessing is how "Montag geschlossen" became "open on Mondays".
_ONLY_HOURS = re.compile(r"[\s,，、;；/&+和]*(?:\d{1,2}[:：]\d{2}\s*[-–—~～至到]\s*\d{1,2}[:：]\d{2}[\s,，、;；/&+和]*)+")


def has_ambiguous_weekday(hours: str) -> bool:
    """True when the weekday prefix contains ma/di/do, which name different days per language."""
    if not isinstance(hours, str):
        return False
    match = _FIRST_TIME.search(hours)
    prefix = hours[:match.start()] if match else hours
    return bool(prefix.strip()) and bool(_AMBIGUOUS_TOKEN.search(prefix))


_WEEKDAY_TOKENS = _weekday_tokens()
# Longest-first so 'monday' wins over 'mon'; the trailing (?![a-z]) keeps 'Sun' out of 'Sunset',
# which would otherwise turn a normal venue name into a claim that the place opens only on Sundays.
_WEEKDAY_TOKEN = re.compile(
    "(?:{cn})|(?:{en})\\.?(?![a-z])".format(
        cn="|".join(sorted((t for t in _WEEKDAY_TOKENS if not t.isascii()), key=len, reverse=True)),
        en="|".join(sorted((t for t in _WEEKDAY_TOKENS if t.isascii()), key=len, reverse=True))),
    re.IGNORECASE)
_WEEKDAY_RANGE_SEP = re.compile(r"\s*(?:[-–—~～]|至|到|through|thru|to|\ba\b|\bà\b|\bau\b|~)\s*",
                                re.IGNORECASE)
_WEEKDAY_LIST_SEP = re.compile(r"\s*(?:[、,，/&+]|and|和|以及)\s*", re.IGNORECASE)
_EVERY_DAY = re.compile(
    r"^\s*(?:daily|open\s+daily|every\s*day|täglich|taeglich|dagelijks|每日|每天|天天)\s*[:：]?\s*",
    re.IGNORECASE)
_HOUR_WINDOW = re.compile(r"(\d{1,2})[:：](\d{2})\s*[-–—~～至到]\s*(\d{1,2})[:：](\d{2})")
_ALL_DAY_HOURS = re.compile(r"24\s*(?:小时|hours?|hrs?|/7)|全天|通宵", re.IGNORECASE)
# "Monday closed, 11:00-22:00 otherwise" names the day the venue is SHUT. Read as an open-days set
# it inverts the verdict and reports the six days it opens as the six days it does not.
_CLOSED_MARKER = re.compile(r"^(?:closed|closes|close\b|rest\s*day|休息|休业|闭馆|不营业|打烊)", re.IGNORECASE)


def _parse_weekday_prefix(text: str) -> tuple[frozenset[int] | None, str]:
    """Split a leading weekday prefix off an hours string: ('Tue-Sun 15:00-21:00') -> ({1..6}, '15:00-21:00').

    Handles both languages, ranges that wrap (Sat-Mon = {5,6,0}), lists ('周一、周三', 'Mon, Wed'),
    and 'daily'/'每日'. Returns (None, text) when there is no prefix, so the bare '15:00-21:00'
    that plans already carry parses exactly as it did before.

    One deliberate refusal: if a weekday token also appears *after* the prefix, the string is
    per-day ('Sat 10:00-14:00, Sun 11:00-15:00') and a single set of open days would describe it
    wrongly. Reporting nothing is the right answer there -- a gate that is wrong about a correct
    plan gets switched off, and takes the cases it did decide correctly with it.
    """
    every = _EVERY_DAY.match(text)
    if every:
        return frozenset(range(7)), text[every.end():]

    days: set[int] = set()
    position = 0
    while True:
        if days:
            separator = _WEEKDAY_LIST_SEP.match(text, position)
            if not separator:
                break
            position = separator.end()
        first = _WEEKDAY_TOKEN.match(text, position)
        if not first:
            break
        first_token = first.group(0).rstrip(".").lower()
        if first_token in AMBIGUOUS_WEEKDAY_TOKENS:
            return None, text  # see AMBIGUOUS_WEEKDAY_TOKENS: refuse rather than guess a language
        start = _WEEKDAY_TOKENS[first_token]
        position = first.end()
        end = start
        dash = _WEEKDAY_RANGE_SEP.match(text, position)
        if dash:
            last = _WEEKDAY_TOKEN.match(text, dash.end())
            if last:
                last_token = last.group(0).rstrip(".").lower()
                if last_token in AMBIGUOUS_WEEKDAY_TOKENS:
                    return None, text
                end = _WEEKDAY_TOKENS[last_token]
                position = last.end()
        cursor = start
        days.add(cursor)
        while cursor != end:  # ranges wrap: Sat-Mon is Sat, Sun, Mon
            cursor = (cursor + 1) % 7
            days.add(cursor)

    if not days:
        return None, text
    rest = text[position:].lstrip(" \t:：,，、")

    # Accept the prefix only when everything after it is time windows and separators. Enumerating
    # closed-markers instead was a whitelist, and it inverted the answer on the most ordinary
    # German string there is: "Montag geschlossen, 11:00-22:00" means shut on Monday, and the
    # parser -- matching "Montag", then failing to recognise "geschlossen" because _CLOSED_MARKER
    # only anchors at the head -- returned {Monday} as the OPEN set. The gate then approves a
    # dinner on the one day the kitchen is dark, and refuses it with full confidence on every day
    # it is actually open. The same shape appears as "gesloten" (nl), "休息" (zh), "Ruhetag",
    # "fermé", "chiuso", "cerrado", and any wording nobody has thought of yet -- which is exactly
    # why this now fails closed on the unknown word rather than trying to list them.
    if _WEEKDAY_TOKEN.search(rest) or not _ONLY_HOURS.fullmatch(rest):
        return None, rest
    return frozenset(days), rest


def _hour_windows(text: str) -> list[tuple[int, int]]:
    """Every HH:MM-HH:MM window in a string, past-midnight ends rolled over.

    A list rather than one window because split service ('11:00-15:00, 17:00-21:00') is ordinary
    and a dinner sitting inside the second block must not be reported as closed.
    """
    windows: list[tuple[int, int]] = []
    for match in _HOUR_WINDOW.finditer(text):
        start_h, start_m, end_h, end_m = (int(group) for group in match.groups())
        if start_h > 47 or end_h > 47 or start_m > 59 or end_m > 59:
            continue
        start, end = start_h * 60 + start_m, end_h * 60 + end_m
        if end <= start:
            end += 24 * 60
        windows.append((start, end))
    if not windows and _ALL_DAY_HOURS.search(text):
        windows.append((0, 24 * 60))
    return windows


def _parse_venue_hours(text: str) -> tuple[frozenset[int] | None, list[tuple[int, int]]]:
    """Open weekdays (None when the string does not say) and the service windows, from venue_hours."""
    days, rest = _parse_weekday_prefix(text)
    return days, _hour_windows(rest)


def _parse_window(text: object) -> tuple[int, int] | None:
    """Accept '18:30-20:00', '18:30–20:00', '17:00~02:00'. Past-midnight ends roll over.

    A leading weekday prefix is stripped first: splitting 'Tue-Sun 15:00-21:00' on its first dash
    produced two unparseable halves, so the string that carries *more* information used to parse
    as nothing at all."""
    if not isinstance(text, str):
        return None
    _, text = _parse_weekday_prefix(text)
    parts = re.split(r"[-–—~至]", text, maxsplit=1)
    if len(parts) != 2:
        return None
    start, end = _parse_hhmm(parts[0]), _parse_hhmm(parts[1])
    if start is None or end is None:
        return None
    if end <= start:
        end += 24 * 60
    return start, end


def _route_text(day: dict) -> str:
    """Everything naming a place on this day's route, for on-route venue matching."""
    route = _route(day)
    chunks = [str(route.get("start") or ""), str(route.get("end") or "")]
    chunks += [str(s) for s in _seq(route.get("stops_in_order"))]
    for seg in _segments(day):
        chunks += [
            str(seg.get("from") or ""), str(seg.get("to") or ""),
            str(seg.get("journey_instruction") or ""), str(seg.get("arrival_instruction") or ""),
        ]
    return "\n".join(chunks)


# --------------------------------------------------------------------------------------------
# Where the rule is written
# --------------------------------------------------------------------------------------------
# This file had well over a hundred places it can refuse a plan and four mentions of
# `references/`, three of them in comments no failing run ever prints. So the run that trips a gate is told WHAT is wrong and
# never WHERE the rule it broke is written down.
#
# That is not a documentation nicety, and the measurement is the argument. The owner runs this
# skill on Chinese-provider models under non-Claude-Code CLIs. references/booking-html-output.md
# is the largest file in the reference layer -- about a third of it -- and SKILL.md's only trigger
# for it is one sentence buried inside its longest paragraph. A run that never opened that file
# gets a 300-character English refusal and has nowhere to go: it cannot guess that a reference it
# never read is the thing that would explain the rule. Naming the file in the failure turns the dead end
# into a self-correcting loop, and it loads the reference at the cheapest possible moment -- after
# the run has demonstrated it needs it, rather than speculatively at the top of every run.
#
# Three rules this registry is built to keep, each one a mistake that was available here:
#
# 1. APPEND, never prepend. Several hundred assertions in tests/ match a needle as a substring of
#    the whole output (`needle not in out`), and many of those needles are the opening words of a
#    message. A prefix would move every one of them and break the suite for no benefit; a suffix
#    is invisible to a substring match. Verified before writing a line of this: `grep -rnE
#    '\.endswith\(' tests/*.py` finds one hit and it is on a filename, not on gate output, and
#    there is no assertion in tests/ that anchors a regex to the end of a message.
#
# 2. Derive the citation from THE ENFORCING CODE, never from SKILL.md's description of itself.
#    SKILL.md currently asserts that the map-endpoint rules are "invisible to every structural
#    gate" twelve lines above its own description of check_map_endpoints, which is the gate that
#    enforces them. A registry built by reading SKILL.md would have inherited that error and sent
#    every author with a broken map URL to the wrong place. Every entry below was instead read off
#    the check that emits it and confirmed against the reference section that states the rule --
#    e.g. the dining rating fields are cited to the destination-coverage-and-food section of
#    booking-html-output.md, because that section is where `rating_value`/`rating_scale`/
#    `rating_count`/`rating_source` are actually enumerated (`grep -n rating_value
#    references/*.md` finds them there and nowhere else).
#
#    Written out in prose rather than as a filename-plus-fragment string on purpose, and twice
#    over. The packaging test scans this file for anything shaped like a citation and resolves
#    every one it finds, without caring whether the string sat in executable code or in a comment
#    -- correctly, because a reader follows a pointer either way. The first draft of this
#    paragraph wrapped the anchor across a line break, leaving `#destination-coverage-and-` in the
#    source, and the test failed on it at once. The second draft wrote a made-up example fragment
#    to explain the first, and the test failed on THAT, because a placeholder shaped like a
#    citation is indistinguishable from one. Both lessons are kept here rather than worked around:
#    a citation is a claim about where something is, and prose makes that claim as loudly as an
#    f-string does. If an example is ever genuinely needed here, make it a real anchor.
#
# 3. Cite the RULE, not the file. A pointer at a 41 KB file's title is barely better than no
#    pointer -- the reader still has to find the paragraph. Each anchor below names the section
#    that states the specific rule the citing check enforces. And a check that has no reference
#    home gets NO citation rather than a plausible-looking one: a fabricated pointer is worse than
#    silence, because it costs a read and teaches the wrong location.
#
# Anchors are `<a id="...">` markers written into the reference files in this same change, not
# heading slugs, so that rewording a heading cannot silently 404 a citation. A test in
# tests/test_packaging.py resolves every anchor any gate here can emit; a citation that 404s is
# worse than none, so it is a test failure rather than a convention.
CHECK_REFERENCES: dict[str, str] = {
    # Day route arithmetic, the walking burden, and the clock. All of it is the "keep the day's
    # actual travel burden visible" contract -- start/end, mode, distance, transfers, walking,
    # duration, fare -- which is stated once, in the route-burden section.
    # A multi-stop trip is a sequence of stays, and the one arithmetic mistake it makes that
    # every per-day check passes is paying for two hotels on one night.
    "check_entry_covers_every_jurisdiction": "booking-html-output.md#multi-stop-trips",
    # A separate-ticket connection needs the traveller's own words accepting it.
    "check_self_transfer_consent": "booking-html-output.md#self-transfer",
    # The traveller's recorded decisions: one per group, real options, honest dates.
    "check_bookings": "replanning.md#bookings",
    "check_time_zones": "booking-html-output.md#calendar",
    # Settling the entry answer is the entry domain's job, stated with the verification domains.
    "check_verified_plan_entry_answer": "verification.md#verify-domains",
    "check_stay_groups_do_not_overlap": "booking-html-output.md#multi-stop-trips",
    # A card for fewer guests than the trip is what a party change leaves behind when it is typed
    # into trip.traveler_count and traced no further.
    "check_rooms_hold_the_party": "replanning.md#party-changes",
    "check_routes": "booking-html-output.md#day-route-burden",
    "check_implied_speed": "booking-html-output.md#day-route-burden",
    "check_map_link_modes": "booking-html-output.md#map-modes",
    "check_clock_closure": "booking-html-output.md#day-route-burden",
    "check_day_internals": "booking-html-output.md#day-route-burden",
    # The walking cap is a number the interview has to produce, and this check is the reason it
    # has to be a number: left as prose the field stays null and every walking check passes
    # silently. That is the failure initial-intake.md's machine-readable-values section exists to
    # describe, so an author who trips this gate is sent to the question that was skipped.
    "check_walking_budget": "initial-intake.md#machine-readable-values",
    "check_untyped_constraints": "initial-intake.md#machine-readable-values",
    "check_preference_coverage": "initial-intake.md#experience-taxonomy",
    "check_preferences_came_from_the_intake": "initial-intake.md#experience-taxonomy",
    # Map URLs: endpoints are geocoder queries, transit takes no waypoints, a day map's scope has
    # to match the stops it claims to cover.
    "check_map_endpoints": "booking-html-output.md#map-endpoints",
    # Dining: the route anchor and the checked weekday hours, then the quality signal. Both live
    # in the same section, which is also where the rating field names come from.
    "check_dining": "booking-html-output.md#destination-coverage-and-food",
    "check_meal_reachability": "booking-html-output.md#destination-coverage-and-food",
    "check_venue_quality": "booking-html-output.md#destination-coverage-and-food",
    # A button that names one provider and opens another, a comparison link scoped to a city
    # rather than to the property, two options sharing one URL.
    "check_booking_identity": "booking-html-output.md#button-provider-identity",
    "check_accommodation_coverage": "booking-html-output.md#booking-links",
    "check_ticket_sale_windows": "booking-html-output.md#ticket-constraints",
    # Whether the links work from where the traveller will be standing.
    "check_service_market": "regional-service-routing.md#final-plan-contract",
    # What the page prints verbatim, and the shapes the renderer refuses to print.
    "check_prose_rendering": "booking-html-output.md#render-what-the-plan-collects",
    "check_prose_agrees_with_data": "booking-html-output.md#render-what-the-plan-collects",
    "check_prose_texture": "booking-html-output.md#render-what-the-plan-collects",
    "check_list_typed_fields": "booking-html-output.md#list-typed-fields",
    "check_cross_references": "booking-html-output.md#render-what-the-plan-collects",
    "check_budget": "initial-intake.md#budget-model",
    "check_replan_context": "replanning.md#the-gate-that-stops-it-shipping",
    "check_dates_agree_with_the_gates_that_ran": "replanning.md#the-gate-that-stops-it-shipping",
    "check_verification": "verification.md#report-schema",
    # check_dates and check_sentinel_timestamps are deliberately absent; see
    # CHECKS_WITHOUT_A_REFERENCE below, which is where that decision is recorded so a test can
    # hold it.
}

# The other half of the registry, and the reason it is a named constant rather than an absence.
#
# A check that is simply MISSING from CHECK_REFERENCES and a check somebody decided needs no
# citation are indistinguishable from outside, and the first one is a bug. That is the same shape
# as every incident in this file's history: the gap looks exactly like the deliberate choice, so
# nobody finds it until a real run does. Listing the exemptions by name with their reason turns
# "not in the dict" into a third state that tests/test_packaging.py can refuse -- a new check must
# now name its reference or say out loud that it has none, and cannot quietly do neither.
#
# The bar for landing here is that NO reference section states the rule. Both of these decide on
# arithmetic alone: an end date that precedes its start date, and a skeleton epoch nobody
# replaced. Their messages already name the field and the contradiction, so a reference would add
# a lookup and no information.
CHECKS_WITHOUT_A_REFERENCE: dict[str, str] = {
    "check_dates": "date arithmetic; no reference states it and the message names the two dates",
    "check_sentinel_timestamps": "refuses the skeleton's own 1970 placeholder; nothing to read",
    "check_verification_tier_is_stated":
        "refuses nothing -- it reads the tier out of the plan's own fields as a note, because "
        "SKILL.md tells the author to 'read what it printed' about a choice this gate had never "
        "actually printed. verification.md#verify-domains states the tiers; the note quotes "
        "required_domains_for's own reason, so it carries its argument with it",
}


def _citation_for(check_name: str) -> str | None:
    """The reference an author should open when `check_name` refuses their plan, or None.

    None is a real answer, not a gap to be filled later: see rule 3 in the block above.
    """
    target = CHECK_REFERENCES.get(check_name)
    return f" [see references/{target}]" if target else None


# The marker a message already carries, so a nested check cannot be cited twice and so
# check_verification's findings survive being merged into the same list.
_CITED = " [see references/"


def cites(check):
    """Stamp every finding a check appends with the reference that states the rule it enforces.

    Why a decorator rather than an edit at each of the 135 `errors.append(...)` sites. Both were
    tried on paper. The per-site edit is 135 chances to paste the wrong anchor and it covers only
    the sites that exist today -- a check gains a branch next release and that branch ships
    uncited, which is exactly the drift this whole change is against. Stamping at the boundary
    covers every site in the function including the ones nested inside it (`endpoints_of` and
    `walk` are closures that append to the same list, and between them they produce most of what
    this check reports on the real workspace) and it covers branches nobody has written yet.

    Why not wrap the tuple entries in PLAN_CHECKS instead, which would have been a one-line
    change: tests/test_plan_consistency.py asserts `CHECKER_MODULE.check_untyped_constraints in
    CHECKER_MODULE.PLAN_CHECKS` -- an identity test, and a deliberate one, because a check absent
    from that tuple is a check nothing runs. Wrapping at the tuple would put an object in
    PLAN_CHECKS that is not the module attribute and fail that test. Decorating at the `def` keeps
    the two the same object, because the name is rebound to the wrapper before PLAN_CHECKS is
    built. `functools.wraps` is not decoration either: `__name__` is what audit_workspace.py and
    the skeleton's worklist print, and what this decorator itself reads to find the citation.

    Findings already carrying a citation are left alone, so a site that wants a narrower anchor
    than its check's default can call cite() itself and win.

    The wrapper takes `*args` rather than the `(plan, errors, notes)` the checks in PLAN_CHECKS
    all share, because check_verification does not share it: its first argument is the verification
    REPORT, and its callers pass the plan by keyword (`check_verification(report, errors, notes,
    plan=plan, plan_path=...)`). A wrapper that named its first parameter `plan` would collide with
    that keyword and raise "got multiple values for argument 'plan'" -- turning the one check that
    reads the verification report into a crash, which is worse than the missing citation this
    decorator exists to add. Every call site in this repo passes errors second and positionally,
    which is what args[1] relies on; an errors list handed over by keyword would be a new calling
    convention and is asserted against below rather than guessed at.
    """
    suffix = _citation_for(check.__name__)

    @functools.wraps(check)
    def cited(*args, **kwargs):
        if suffix is None:
            return check(*args, **kwargs)
        if len(args) < 2 or not isinstance(args[1], list):
            raise TypeError(
                f"{check.__name__} was called without its errors list as the second positional "
                f"argument, so its findings cannot be cited. Every caller in this repo passes "
                f"(subject, errors, notes) positionally; if that changed, update cites().")
        errors = args[1]
        before = len(errors)
        result = check(*args, **kwargs)
        for index in range(before, len(errors)):
            if _CITED not in errors[index]:
                errors[index] += suffix
        return result

    return cited


def cite(rule_id: str, message: str) -> str:
    """Append a narrower citation than the emitting check's default.

    Raises on an unknown rule_id rather than returning the message unchanged. A silent fallthrough
    here would be the same class of bug this file exists to catch: the gate would keep passing its
    own tests while quietly shipping the uncited message, and nobody would find out until an
    author hit a dead end in a run nobody was watching. A KeyError fails on the first test that
    reaches the site, which is before any traveller sees it.
    """
    if rule_id not in RULE_REFERENCES:
        raise KeyError(
            f"cite() called with unknown rule_id {rule_id!r}. Add it to RULE_REFERENCES with the "
            f"reference section that states the rule, or drop the cite() call -- see rule 3 in "
            f"the registry comment above: no citation beats a wrong one.")
    return f"{message} [see references/{RULE_REFERENCES[rule_id]}]"


# Narrower homes than the emitting check's default. Kept small on purpose: an entry here is a
# claim that this one rule is written somewhere other than where the rest of its check's rules
# are, and every entry has to be worth a reader's second lookup.
RULE_REFERENCES: dict[str, str] = {
    # check_map_endpoints' default sends the reader to the endpoint-writing rules, which is right
    # for a free-text origin or a mismatched scope. The transit-waypoint refusal is a different
    # fact about a different system -- Google computes waypoints for driving, walking and cycling
    # and refuses them for transit -- and it is stated in the public-transport section.
    "map.transit_waypoints": "booking-html-output.md#public-transport",
    # A Google link shipped into a market where Google does not answer is a routing-policy
    # question before it is a final-plan-contract one: the fix is to pick the market's provider,
    # not to add an attribute to the page.
    "market.unreachable_provider": "regional-service-routing.md#routing-policy",
    # The intake cross-check's default home is the experience taxonomy, which is right for a
    # dropped must-have. A dropped allergy, walking limit, party size or cap is the other half of
    # the form: the values the interview has to produce in machine-readable shape.
    "intake.constraints": "initial-intake.md#machine-readable-values",
    # Whether the traveller may enter is settled by the entry domain of the verification pass, and
    # that is where the rule that a verified plan cannot leave it open is stated.
    "entry.answer": "verification.md#verify-domains",
    # An edit after verification is rechecked by section, and the report records each recheck.
    "verification.rechecks": "verification.md#rechecks",
}


@cites
def check_routes(plan: dict, errors: list[str], notes: list[str]) -> None:
    for day in _seq(plan.get("days")):
        day = _obj(day)
        number = day.get("number")
        route = _route(day)
        segments = _segments(day)
        if not segments:
            continue

        seg_duration = sum(_num(s.get("duration_minutes")) for s in segments)
        seg_distance = sum(_num(s.get("distance_km")) for s in segments)
        seg_cost_low = sum(_num(s.get("cost_low")) for s in segments)
        seg_cost_high = sum(_num(s.get("cost_high")) for s in segments)

        stated_duration = _num(route.get("duration_minutes"))
        if abs(stated_duration - seg_duration) > DURATION_TOLERANCE_MIN:
            errors.append(
                f"day {number}: route.duration_minutes={stated_duration:g} but its segments sum to "
                f"{seg_duration:g}. Route totals must be derived from segments, not authored.")

        stated_distance = _num(route.get("distance_km"))
        if abs(stated_distance - seg_distance) > DISTANCE_TOLERANCE_KM:
            errors.append(
                f"day {number}: route.distance_km={stated_distance:g} but its segments sum to "
                f"{seg_distance:.1f}.")

        if abs(_num(route.get("cost_low")) - seg_cost_low) > COST_TOLERANCE:
            errors.append(
                f"day {number}: route.cost_low={_num(route.get('cost_low')):g} but its segments sum to "
                f"{seg_cost_low:g}.")
        if abs(_num(route.get("cost_high")) - seg_cost_high) > COST_TOLERANCE:
            errors.append(
                f"day {number}: route.cost_high={_num(route.get('cost_high')):g} but its segments sum to "
                f"{seg_cost_high:g}.")

    # On a self-drive trip the overview's distance is the whole drive, and it is the first number
    # a traveller budgeting fuel and time reads. It was only ever used as a map bound, so an overview
    # saying 334 km over days that add up to 366 passed (2026-09-24). Five percent of slack, because
    # a stated overview is often rounded.
    if _self_drive(plan):
        overall = _num(_obj(plan.get("transport_overview")).get("overall_distance_km"))
        days_total = sum(_num(_route(_obj(d)).get("distance_km")) for d in _seq(plan.get("days")))
        if overall > 0 and days_total > 0 and abs(overall - days_total) > 0.05 * days_total:
            errors.append(
                f"transport_overview.overall_distance_km is {overall:g} km and the days' routes add "
                f"up to {days_total:.1f} km. On a self-drive trip the overview is the whole drive; "
                f"make it the sum, or fix the day that is wrong.")


def activity_on_foot_minutes(day: dict) -> int:
    """Minutes on foot *inside* the day's activities, which no segment records.

    Segments only know the connecting legs. Queuing at a gate, a park loop, a market crawl and a
    two-hour standing tour are not segments at all, so a plan that reported only its segments told
    the truth about the wrong number. Optional by contract: a plan that omits on_foot_minutes
    computes 0 here, and every rule that depends on it stays off rather than guessing."""
    total = 0
    for activity in [_obj(a) for a in _seq(day.get("activities"))]:
        value = activity.get("on_foot_minutes")
        if isinstance(value, (int, float)) and not isinstance(value, bool):
            total += int(value)
    return total


# A leg's mode is free text -- 31 spellings across the author's workspace, most of them Chinese --
# so it is classified by the words it contains, and only when they name ONE class. An ambiguous leg
# ("公共交通或网约车", "metro/bus/taxi (choose one)") is not guessed at: SKILL.md already asks for one
# primary mode, and a check that picked one on the author's behalf would be arguing with a sentence.
#
# The English and the rest were added after a probe on 2026-09-24 of 46 mode strings a plan outside
# that workspace writes: 34 named no class, so the check was blind to London's Tube, Singapore's
# MRT, a vaporetto or a hike. System names (Tube, MRT, RER, ...) and the ride-hail apps that name one
# mode (Uber, Grab, 滴滴) are here; train and bus operator brands are not, because a brand names a
# company, and an unclassified leg is merely unjudged. Traditional characters are read too: the
# intake reads zh-TW and Cantonese as Chinese, so those plans reach this check.
_MODE_WORDS = {
    "air": (r"航班", r"飞机", r"飛機", r"\bflights?\b", r"\bplanes?\b"),
    "ferry": (r"渡轮", r"轮渡", r"渡輪", r"輪渡", r"渡船", r"水上", r"游船", r"遊船", r"船", r"快艇",
              r"\bferr(?:y|ies)\b",
              r"boats?\b", r"\bwater ?(?:bus|taxi)(?:es|s)?\b", r"\bvaporett[oi]\b",
              r"\bcatamarans?\b", r"\bhydrofoils?\b"),
    "rail": (r"地铁", r"轻轨", r"电车", r"有轨", r"火车", r"高铁", r"动车", r"铁路", r"城铁", r"单轨",
             r"轨道", r"新干线", r"列车", r"磁悬浮", r"捷运", r"港铁",
             # the same in Traditional characters, which the intake reads as Chinese too
             r"捷運", r"地鐵", r"輕軌", r"電車", r"火車", r"高鐵", r"動車", r"鐵路", r"城鐵", r"單軌",
             r"軌道", r"新幹線", r"列車", r"磁浮", r"港鐵", r"\bmetro\b", r"\bsubway\b",
             r"\bunderground\b", r"\btube\b", r"\boverground\b", r"\bdlr\b", r"\b[ml]rt\b",
             r"\bmtr\b", r"\bskytrain\b", r"\brer\b", r"\bmonorails?\b", r"\btrams?\b",
             r"\btrains?\b", r"\brail\b", r"\b[su]-bahn\b", r"\bice\b", r"\btgv\b",
             r"\bshinkansen\b", r"\bfuniculars?\b", r"\bstreet ?cars?\b",
             r"\b(?:sleeper|dining|couchette|rail) ?cars?\b"),
    # "shuttle" is not here: an airport shuttle bus says "bus", and "Le Shuttle" is the car train
    # under the Channel -- read as a bus, a self-drive trip's crossing was told to stop driving.
    "bus": (r"公交", r"巴士", r"大巴", r"班车", r"班車", r"公車", r"客運", r"\bbus(?:es)?\b",
            r"\bminibus(?:es)?\b",
            r"\btrolley ?bus(?:es)?\b", r"\bcoach(?:es)?\b"),
    "car": (r"网约车", r"出租", r"打车", r"驾车", r"自驾", r"开车", r"租车", r"包车", r"滴滴", r"专车",
            r"拼车", r"網約車", r"計程車", r"的士", r"駕車", r"自駕", r"開車", r"租車", r"包車", r"專車",
            r"\btaxi\b", r"\b(?:mini)?cabs?\b", r"\buber\b", r"\blyft\b", r"\bbolt\b",
            r"\bgrab\b", r"\bdidi\b", r"\bride[- ]?(?:hail|share)(?:ing)?\b", r"\bcar\b",
            r"\bdriv(?:e|ing)\b"),
    "walk": (r"步行", r"徒步", r"散步", r"漫步", r"\bwalk(?:ing)?\b", r"\bon foot\b",
             r"\bhik(?:e|es|ing)\b", r"\bstroll(?:ing)?\b"),
    "transit": (r"公共交通", r"\bpublic transport\b", r"\btransit\b"),
    # An aerial lift names no map mode -- some cities route one as transit, most do not -- so it is
    # classified only to be left alone, and to stop a self-drive trip reading it as a road leg.
    "lift": (r"缆车", r"纜車", r"索道", r"\bgondolas?\b", r"\bropeways?\b", r"\bcable ?cars?\b",
             r"\bchair ?lifts?\b", r"\baerial tram(?:way)?s?\b"),
    # The same for anything pedalled or scooted: no map button this skill writes is judged for it,
    # and a self-drive trip must not read it as a road leg.
    "bike": (r"自行车", r"单车", r"骑行", r"电动车", r"單車", r"腳踏車", r"騎行", r"電動車",
             r"\bbikes?\b", r"\bbicycles?\b",
             r"\bcycl(?:e|es|ing)\b", r"\be-?scooters?\b"),
}
# "car" inside these names another vehicle: a cable car, a street car, a sleeper car, a water taxi.
# Removed before the car patterns are tried, so "hire car + cable car" still names both and stays
# unjudged.
_NOT_A_CAR = re.compile(r"\b(?:(?:cable|street|sleeper|dining|couchette|rail|tram)[ -]?cars?"
                        r"|water[ -]?taxis?)\b")
# 动车 is a bullet train, and it is also the tail of 电动车 (an e-bike) and 机动车 (any motor
# vehicle): removed before the rail patterns are tried, so a scooter leg is not told to take transit.
_NOT_A_TRAIN = re.compile(r"电动车|机动车|電動車|機動車")
# 单车 is a bike, and also the head of 单车道, a single-lane road -- a drive, not a ride.
_NOT_A_BIKE = re.compile(r"单车道|單車道")
# Average speeds no leg of that kind reaches door to door, so a figure above one is a duration or a
# distance borrowed from another leg. Deliberately generous: a rule tight enough to argue with is a
# rule people learn to route around.
MODE_SPEED_CEILINGS = {"car": 130.0, "bus": 110.0, "rail": 350.0, "ferry": 80.0}


def _mode_class(mode: str) -> str | None:
    """walk | car | bus | rail | ferry | air | transit | lift | bike, "mixed" for more than one,
    None for none."""
    text = str(mode or "").casefold()
    stripped = {"car": _NOT_A_CAR.sub(" ", text), "rail": _NOT_A_TRAIN.sub(" ", text),
                "bike": _NOT_A_BIKE.sub(" ", text)}
    found = {cls for cls, patterns in _MODE_WORDS.items()
             if any(re.search(pattern, stripped.get(cls, text)) for pattern in patterns)}
    if "ferry" in found:
        found.discard("bus")          # 水上巴士, a water bus, is a boat
    if len(found) == 1:
        return found.pop()
    return "mixed" if found else None


def _url_travel_mode(url: str) -> str | None:
    """The travel mode a directions URL asks for: Google travelmode, Amap mode, Apple dirflg."""
    try:
        query = urllib.parse.parse_qs(urllib.parse.urlparse(str(url or "")).query)
    except ValueError:
        return None
    value = (query.get("travelmode") or query.get("mode") or query.get("dirflg") or [""])[0]
    return {"walking": "walk", "walk": "walk", "w": "walk", "driving": "car", "car": "car",
            "d": "car", "taxi": "car", "transit": "transit", "bus": "transit", "r": "transit",
            "train": "transit", "subway": "transit", "bicycling": "bike",
            "ride": "bike"}.get(value.casefold())


def _self_drive(plan: dict) -> bool:
    return str(_obj(plan.get("transport_preference")).get("mode") or "") == "self-drive"


@cites
def check_implied_speed(plan: dict, errors: list[str], notes: list[str]) -> None:
    """A leg's distance and its duration have to be survivable by the mode that connects them.

    Both halves of this shipped. A "6 minute" walk between two coordinates 1.1 km apart is
    11 km/h -- a run, written when the leg had no coordinates and never revisited once it did.
    The reverse also passes every other gate: a leg whose numbers are fine but whose endpoints
    belong to a different pair of stops looks like a bus averaging 2 km/h.

    The bounds are deliberately wide. Walking is capped at 6 km/h because a brisk walk is 5 and
    anything past 6 is jogging; transit is floored at 4 km/h, which is slower than walking and
    therefore only fires on numbers that cannot describe a bus at all. A rule tight enough to
    argue with is a rule people learn to route around.
    """
    self_drive = _self_drive(plan)
    for day in [_obj(d) for d in _seq(plan.get("days"))]:
        number = day.get("number")
        for index, seg in enumerate(_segments(day), start=1):
            minutes = _num(seg.get("duration_minutes"))
            km = _num(seg.get("distance_km"))
            if minutes <= 0 or km <= 0:
                continue
            kmh = km / (minutes / 60.0)
            mode = str(seg.get("mode") or "")
            walking = ("步行" in mode) or ("walk" in mode.casefold())
            if walking and kmh > 6.0:
                errors.append(
                    f"day {number} segment {index}: {km:g} km on foot in {minutes:g} minutes is "
                    f"{kmh:.1f} km/h, which is running. Give the leg the time the walk actually "
                    f"takes -- this is a traveller with a stated walking limit, so an optimistic "
                    f"number here understates the burden the whole plan is built around.")
            elif not walking and kmh < 4.0 and km > 2.0:
                errors.append(
                    f"day {number} segment {index}: {km:g} km by {mode or 'transit'} in "
                    f"{minutes:g} minutes is {kmh:.1f} km/h, slower than walking. Either the "
                    f"duration or the distance belongs to a different leg.")
            if not walking:
                # A ceiling as well as a floor. Only walking had one, so a 118 km drive claimed in
                # 20 minutes -- 354 km/h -- passed every gate on the kind of trip whose days are
                # planned around the drive. On a self-drive trip a leg whose words name no class
                # is a road leg; on any other trip it is left alone rather than guessed.
                cls = _mode_class(mode) or ("car" if self_drive else None)
                ceiling = MODE_SPEED_CEILINGS.get(cls or "")
                if ceiling and kmh > ceiling:
                    errors.append(
                        f"day {number} segment {index}: {km:g} km by {mode or cls} in "
                        f"{minutes:g} minutes is {kmh:.0f} km/h, faster than a {cls} averages "
                        f"door to door. One of the two numbers belongs to another leg -- and on "
                        f"a self-drive day this is the time the whole day is planned around.")


@cites
def check_map_link_modes(plan: dict, errors: list[str], notes: list[str]) -> None:
    """A segment's button opens directions in the segment's own mode.

    Nothing compared the two. A walking leg whose button asked for driving directions passed, and
    the author's workspace held 20 taxi and ride-hail legs whose Amap buttons were in bus mode --
    the traveller pressing "open this leg" got a bus route for a taxi ride. Judged only when both
    sides are unambiguous: the leg's words name one class and the URL names a mode.
    """
    self_drive = _self_drive(plan)
    expected_for = {"walk": "walk", "car": "car", "bus": "transit", "rail": "transit",
                    "ferry": "transit", "transit": "transit"}
    for day in [_obj(d) for d in _seq(plan.get("days"))]:
        number = day.get("number")
        for index, seg in enumerate(_segments(day), start=1):
            url = str(seg.get("verified_map_url") or "")
            got = _url_travel_mode(url)
            if got not in {"walk", "car", "transit"}:
                continue
            leg = _mode_class(str(seg.get("mode") or ""))
            if leg is None and self_drive:
                leg = "car"
            expected = expected_for.get(leg or "")
            # With the car aboard, a vehicle ferry is part of the drive, and driving directions are
            # the ones that include the crossing.
            if expected and got == "car" and leg == "ferry" and self_drive:
                continue
            if expected and got != expected:
                words = {"walk": "walking", "car": "driving", "transit": "public-transport"}
                errors.append(
                    f"day {number} segment {index}: the leg is {seg.get('mode')!r} and its button "
                    f"opens {words[got]} directions. Set the button's travel mode to "
                    f"{words[expected]} -- the traveller follows the button, not the label.")


@cites
def check_walking_budget(plan: dict, errors: list[str], notes: list[str]) -> None:
    """The traveller's accessibility constraint is decided here, not in adjectives.

    A day's walking is two numbers, not one: the connecting legs (walking_totals) and the minutes
    the activities themselves keep the traveller on their feet (on_foot_minutes). A real run
    printed "42 minutes on foot" for a day scheduling roughly 3.5 hours of it against a hard
    mobility constraint -- and the old rule REQUIRED that misleading figure be on the page,
    because it only knew about the segments. Both must now be quoted, both feed the
    lightest/heaviest claim, and neither may exceed a limit the traveller stated."""
    days = [_obj(d) for d in _seq(plan.get("days"))]
    totals = {d.get("number"): walking_totals(d) for d in days}
    if not totals:
        return
    on_foot = {d.get("number"): activity_on_foot_minutes(d) for d in days}
    # Lightest/heaviest is a claim about what the traveller's legs do, so judge it on both numbers.
    load = {number: minutes + on_foot[number] for number, (minutes, _) in totals.items()}
    max_day = max(load, key=lambda n: load[n])
    min_day = min(load, key=lambda n: load[n])

    constraints = _obj(_obj(plan.get("trip")).get("traveler_constraints"))
    cap = constraints.get("max_continuous_walking_minutes")
    if isinstance(cap, bool) or not isinstance(cap, (int, float)):
        cap = None

    # Whether a null cap is the traveller's answer or nobody's, which is a distinction the note
    # further down asserted an answer to without ever asking. It said "this traveller stated no
    # walking limit" on every day of every plan whose cap was null -- including the skeleton's own
    # output, where the cap is null for the opposite reason: nobody has been asked yet. Measured on
    # a freshly generated three-day skeleton before this line existed, the one report carried three
    # copies of "Not an error -- this traveller stated no walking limit" AND the two
    # check_untyped_constraints errors, one of them "max_continuous_walking_minutes was never typed
    # -- untyped_constraints still names it". Two claims about one field in one report, and the
    # reassuring one was the false one. The marker is the authority here; the note follows it.
    # The third element is deliberately dropped here: which junk entries the marker carries is
    # check_untyped_constraints' business to report, and this note only has to know whether the
    # CAP is among the fields the marker readably names.
    marker_state, marker_fields, _ = read_untyped_constraints(constraints)
    cap_untyped = (marker_state == UNTYPED_MARKER_FIELDS
                   and "max_continuous_walking_minutes" in marker_fields)

    for day in days:
        number = day.get("number")
        minutes, km = totals[number]
        walked_in_activities = on_foot[number]

        # An undeclared on_foot_minutes and a measured zero are the same value, and that inversion
        # made this gate reward silence. Measured on this fixture: a traveller with a stated 20
        # minute cap, activities declaring nothing, saved clean with the page reading "20 min" --
        # and the SAME plan with the walking honestly written as 180 was refused. The traveller
        # whose legs the rule exists for got the plan that never counted them.
        #
        # So when the traveller put a number on their walking, every activity has to answer. Note
        # what is being demanded: a DECLARATION, not a small value. An author who looks at a
        # concert or a sit-down dinner and writes 0 has measured it, and passes. Only silence
        # fails, because silence is the one answer nobody can check.
        if cap is not None:
            silent = [str(_obj(a).get("name") or f"activity {i}")
                      for i, a in enumerate(_seq(day.get("activities")), 1)
                      if not isinstance(_obj(a).get("on_foot_minutes"), (int, float))
                      or isinstance(_obj(a).get("on_foot_minutes"), bool)]
            if silent:
                errors.append(
                    f"day {number}: the traveller stated max_continuous_walking_minutes={cap:g}, so "
                    f"every activity must declare on_foot_minutes -- these do not: "
                    f"{', '.join(silent)}. Undeclared is not zero. Write the measured minutes, or "
                    f"0 where the activity genuinely involves no walking; that is a fact the gate "
                    f"can check and silence is not.")
        elif walked_in_activities == 0 and any(_seq(day.get("activities"))):
            # The measurement is identical in all three branches and only the standing of the null
            # cap differs, so the sentence that reports the measurement is written once. The third
            # branch is not hypothetical bookkeeping: an unreadable marker is a live state --
            # check_untyped_constraints refuses it by name -- and routing it to the "stated no
            # walking limit" wording would rebuild the same contradiction one shape to the left.
            floor = (f"day {number}: no activity declares on_foot_minutes, so the page's walking "
                     f"figure counts only the legs between stops, not the time spent on foot at "
                     f"them.")
            if cap_untyped:
                notes.append(
                    f"{floor} Nobody has stated a walking limit either -- "
                    f"{UNTYPED_CONSTRAINTS_MARKER} still names max_continuous_walking_minutes, so "
                    f"the null cap is the skeleton's default and not the traveller's answer. This "
                    f"day's walking is unmeasured from both ends: no per-activity minutes, and no "
                    f"cap to measure them against. check_untyped_constraints reports the untyped "
                    f"field itself; this note is what it costs on this day.")
            elif marker_state == UNTYPED_MARKER_UNREADABLE:
                notes.append(
                    f"{floor} Whether anybody stated a walking limit cannot be read off this plan: "
                    f"{UNTYPED_CONSTRAINTS_MARKER} is present in a shape nothing can act on, which "
                    f"check_untyped_constraints reports on its own terms. Until it is readable "
                    f"this note will not tell you the null cap was the traveller's answer.")
            else:
                notes.append(
                    f"{floor} Not an error -- this traveller stated no walking limit -- but the "
                    f"figure is a floor.")

        burden = str(_route(day).get("walking_burden") or "")
        if not burden.strip():
            errors.append(f"day {number}: route.walking_burden is empty.")
        else:
            # Substring matching let a day whose real total was 5 satisfy the rule by writing
            # "15 minutes" -- the exact inversion the check exists to prevent. Match a whole number.
            if not re.search(rf"(?<!\d){minutes}(?!\d)", burden):
                errors.append(
                    f"day {number}: walking_burden does not quote the computed walking total "
                    f"({minutes} min / {km} km) as a number. Derive the text from the segments, and "
                    f"write the figure in digits so it cannot drift from the data.")
            # Only demanded when the plan actually carries the second number, so a plan written
            # before on_foot_minutes existed passes exactly as it did before. A negative total is
            # reported below on its own terms; demanding the prose quote "-40" would be nonsense.
            if walked_in_activities > 0 and not re.search(rf"(?<!\d){walked_in_activities}(?!\d)", burden):
                errors.append(
                    f"day {number}: walking_burden quotes the connecting legs but not the "
                    f"{walked_in_activities} minutes this day's activities declare on foot "
                    f"(on_foot_minutes). Write both figures in digits -- "
                    f"'{minutes} min between stops plus {walked_in_activities} min at them, "
                    f"{minutes + walked_in_activities} in total' -- because the traveller reads the "
                    f"page and their legs pay for whichever number it left out.")
            light_text = _NEGATED_LIGHT.sub("", burden)
            if _LIGHT_CLAIM.search(light_text) and number != min_day:
                errors.append(
                    f"day {number}: walking_burden claims it is the lightest day, but day {min_day} "
                    f"is ({load[min_day]} min vs {load[number]} min on foot in total).")
            if _HEAVY_CLAIM.search(burden) and number != max_day:
                errors.append(
                    f"day {number}: walking_burden claims it is the heaviest day, but day {max_day} "
                    f"is ({load[max_day]} min vs {load[number]} min on foot in total).")

        for position, segment in enumerate(_segments(day), 1):
            walk = int(_num(segment.get("walking_minutes")))
            if cap is not None and walk > cap:
                errors.append(
                    f"day {number} segment {position} ({segment.get('from')} -> {segment.get('to')}): "
                    f"walking_minutes={walk} exceeds the traveller's stated "
                    f"max_continuous_walking_minutes={cap:g}. Split the leg with a seated stop, or "
                    f"move it onto transport. The limit is a constraint they gave us, not a target.")
        for activity in [_obj(a) for a in _seq(day.get("activities"))]:
            value = activity.get("on_foot_minutes")
            if not isinstance(value, (int, float)) or isinstance(value, bool):
                continue
            if value < 0:
                errors.append(
                    f"day {number}: activity '{activity.get('name')}' has on_foot_minutes={value}, "
                    f"which is negative. The day's on-foot total is summed from these, so one "
                    f"negative entry cancels a real one and leaves the day looking easy.")
            elif cap is not None and value > cap:
                errors.append(
                    f"day {number}: activity '{activity.get('name')}' has on_foot_minutes={int(value)}, "
                    f"over the traveller's stated max_continuous_walking_minutes={cap:g}. Build in a "
                    f"seated break, shorten the visit, or say in the plan how they sit down inside it.")

    notes.append("walking per day (min/km): " + ", ".join(
        f"d{n}={m}/{k}" for n, (m, k) in sorted(totals.items(), key=lambda kv: kv[0] or 0)))
    if any(on_foot.values()):
        notes.append("on-foot minutes inside activities: " + ", ".join(
            f"d{n}={m}" for n, m in sorted(on_foot.items(), key=lambda kv: kv[0] or 0)))


# save_trip_deliverables.py imports this name to build its own copy of the check list. Renaming it
# outright would have broken the save path -- the one path that writes files a traveller keeps.
check_walking = check_walking_budget


@cites
def check_clock_closure(plan: dict, errors: list[str], notes: list[str]) -> None:
    """A day's own numbers must fit in the day's own clock.

    The run this was written for ended a promenade at 14:00, started the next activity at 15:00,
    and put a lunch in a third neighbourhood plus 35 minutes of its OWN segment durations in
    between. Every gate passed: the route totals summed correctly, the timeline read forwards, and
    nothing compared the arithmetic against the hours available. A day that does not close on
    paper does not close on the ground -- the traveller finds out standing in a station."""
    for day in [_obj(d) for d in _seq(plan.get("days"))]:
        number = day.get("number")
        timed = []
        for activity in [_obj(a) for a in _seq(day.get("activities"))]:
            duration = activity.get("duration_minutes")
            if isinstance(duration, (int, float)) and not isinstance(duration, bool) and duration < 0:
                # The same shape as the negative-segment rule below: the day's clock is summed from
                # these, so one negative entry buys back time the day never had and every rule here
                # goes quiet on a day that is genuinely overpacked.
                errors.append(
                    f"day {number}: activity '{activity.get('name')}' has "
                    f"duration_minutes={duration}, which is negative. Write the real length, or "
                    f"leave the field out if it is unknown.")
            stamp = _parse_hhmm(str(activity.get("time") or ""))
            if stamp is None:
                continue  # an untimed stop has no clock to close; judging it would be guesswork
            timed.append((stamp, int(_num(duration)), activity))
        if len(timed) < 2:
            continue

        overlapped = False
        for (start, length, first), (next_start, _, second) in zip(timed, timed[1:]):
            if start <= next_start < start + length:
                errors.append(
                    f"day {number}: '{second.get('name')}' starts at {_fmt_hhmm(next_start)} while "
                    f"'{first.get('name')}' is still running -- it begins {first.get('time')} and "
                    f"lasts {length} min, to {_fmt_hhmm(start + length)}. Two stops cannot hold the "
                    f"same minutes: move one later, or shorten its duration_minutes.")
                overlapped = True
                break
        if overlapped:
            continue

        # NOT CHECKED, and stated rather than left as a silent gap: whether the gap between two
        # consecutive activities is long enough for the leg between them. A real plan had a museum
        # ending 12:45, its own 20-minute leg to the station, and a 12:49 train -- the traveller
        # arrives sixteen minutes after departure and nothing objects, because the overlap rule
        # compares clock times only and the span rule is inflated by the 193-minute train ride it
        # counts as an activity.
        #
        # Two attempts failed for the same reason, so the reason is worth recording. Pairing gap i
        # with segments[i+1] is wrong: activities and segments are different sequences (5 and 4 on
        # that day, the first activity being the arrival), and it invented a 10-minute shortfall on
        # a correct plan. Matching the leg by endpoints instead is exact but never fires: measured
        # on the real plan, 0 of 15 gaps matched, because `activities[].area_or_venue` is prose
        # ("Kölner Dom, Domplatte") while segments name stops ("科隆大教堂 Kölner Dom").
        #
        # The plan carries no key joining an activity to the leg that reaches it. Adding
        # `activities[].arrives_via_segment` (an index) would close this properly, and until then a
        # check that cannot fire is worse than none: it reads as coverage in the source and reports
        # nothing on real input.

        # A backwards list is check_day_internals' finding ("time travel"). Measuring a span across
        # it would only add a second, more confusing error for one defect.
        if any(later[0] < earlier[0] for earlier, later in zip(timed, timed[1:])):
            continue

        span = (timed[-1][0] + timed[-1][1]) - timed[0][0]
        activity_total = sum(length for _, length, _ in timed)

        # Only the legs BETWEEN the first and last timed activity compete for that span: the leg
        # that carries the traveller to the first stop happens before the span opens, and the leg
        # home after it closes. Charging both rejected a feasible day on this repo's own fixture --
        # hotel->A 25 min and B->hotel 30 min are 55 of that day's 73 segment minutes, so A
        # 09:00-14:00 then B 15:00-16:00 (leave 08:35, home 16:30) was reported as needing 433 out
        # of 420.
        #
        # But `segments[1:-1]` is the wrong way to find them, because position is not meaning. On a
        # departure day the route runs hotel -> museum -> station in TWO segments, and slicing drops
        # both -- including the 20-minute leg to the platform, which is the one that decides whether
        # the train is caught. That shipped: a museum extended to 12:45 with a 12:49 train was
        # reported as fine. Bound by the stops instead: drop a leg only when it lies outside the
        # window the timed activities actually span.
        stops = [str(s) for s in _seq(_route(day).get("stops_in_order"))]
        first_stop = str(_route(day).get("start") or "").strip()
        last_stop = str(_route(day).get("end") or "").strip()
        # One rule: a leg is outside the window when it connects the day's lodging to the itinerary
        # and the traveller is not there during the timed activities. `route.start` / `route.end`
        # are the anchors, not `base_location` -- the contract lets base_location name an area
        # ("Central Chengdu") while segments name the property ("Fixture Hotel A"), so comparing
        # against it silently matches nothing and charges every leg.
        #
        # The test is "does the day return to where it started". A round trip hotel -> ... -> hotel
        # has both ends outside the window. A one-way day (hotel -> museum -> station, the shape of
        # every departure day) has only the first, and the leg to the station stays counted -- it is
        # the one whose overrun means a missed train, and slicing by list position dropped it.
        segments = _segments(day)
        start_point = str(_route(day).get("start") or "").strip()
        end_point = str(_route(day).get("end") or "").strip()
        returns_home = bool(start_point) and start_point == end_point
        # ...unless a timed activity happens AT the lodging. A hotel breakfast puts the traveller
        # there during the window, so the leg out of it is inside the window after all, and
        # dropping it hid a morning that cannot happen: breakfast to 09:10, a 25-minute leg, and
        # the next stop starting 09:15. The traveller arrives twenty minutes after it began and
        # every gate was green.
        timed_at_start = any(str(_obj(a).get("area_or_venue") or "").strip() == start_point
                             for _, _, a in timed) if start_point else False

        interior = []
        for index, segment in enumerate(segments):
            leaves_lodging = index == 0 and start_point and not timed_at_start and \
                str(segment.get("from") or "").strip() == start_point
            returns_lodging = returns_home and index == len(segments) - 1 and \
                str(segment.get("to") or "").strip() == end_point
            if leaves_lodging or returns_lodging:
                continue
            interior.append(segment)
        segment_total = int(sum(_num(s.get("duration_minutes")) for s in interior))
        needed = activity_total + segment_total
        if needed > span:
            errors.append(
                f"day {number}: the day does not close. Between {_fmt_hhmm(timed[0][0])} and "
                f"{_fmt_hhmm(timed[-1][0] + timed[-1][1])} there are {span} minutes, but the day's "
                f"own numbers need {needed}: {activity_total} min of timed activities plus "
                f"{segment_total} min of route legs between the first and last of them (the leg in "
                f"and the leg home fall outside this window and are not counted). Cut a stop, "
                f"shorten a duration_minutes, or move the last activity later -- do not leave the "
                f"arithmetic for the traveller to discover in a station.")


@cites
def check_day_internals(plan: dict, errors: list[str], notes: list[str]) -> None:
    """Within-day coherence: a timeline that runs backwards, or a transfer count that does not
    match the route it summarises, is wrong on the page in a way no structure gate can see."""
    for day in [_obj(d) for d in _seq(plan.get("days"))]:
        number = day.get("number")

        previous = None
        previous_label = None
        for activity in [_obj(a) for a in _seq(day.get("activities"))]:
            stamp = _parse_hhmm(str(activity.get("time") or ""))
            if stamp is None:
                continue
            if previous is not None and stamp < previous:
                errors.append(
                    f"day {number}: activity '{activity.get('name')}' at {activity.get('time')} comes "
                    f"after '{previous_label}' at {_fmt_hhmm(previous)} in the list but earlier on the "
                    f"clock. The timeline renders in order, so it would read as time travel.")
                break
            previous, previous_label = stamp, activity.get("name")

        segments = _segments(day)
        for position, segment in enumerate(segments, 1):
            for field in ("duration_minutes", "distance_km", "cost_low", "cost_high", "walking_minutes"):
                if _num(segment.get(field)) < 0:
                    errors.append(
                        f"day {number} segment {position}: {field}={segment.get(field)} is negative. "
                        f"Route totals are summed from these, so a negative leg can cancel a real one "
                        f"out and leave the day looking self-consistent.")
        if segments and _route(day).get("transfer_count") is not None:
            stated = int(_num(_route(day).get("transfer_count")))
            non_walking = sum(1 for seg in segments if not _is_walk(seg))
            within_segments = int(sum(_num(seg.get("transfer_count")) for seg in segments))
            # The upper bound is the interchanges the day can actually contain: one per boundary
            # between consecutive legs, plus every interchange declared INSIDE a leg. Bounding by
            # the segment count alone was wrong for the ordinary case of one ticketed journey with
            # two changes -- with three segments the lower bound demanded 3 and this demanded at
            # most 3, so exactly one value passed and it was not necessarily the true one. An
            # author whose only way past a gate is to write a number they know is wrong will write
            # it, and the figure on the page stops meaning anything.
            ceiling = max(len(segments) - 1, 0) + within_segments
            if stated > ceiling:
                errors.append(
                    f"day {number}: route.transfer_count={stated} exceeds the {ceiling} this day can "
                    f"contain -- {max(len(segments) - 1, 0)} boundaries between its {len(segments)} "
                    f"legs ({non_walking} of them not walking), plus {within_segments} declared "
                    f"inside a leg.")
            # A day cannot contain fewer interchanges than happen inside its own legs. This is a
            # lower bound rather than equality on purpose: bus -> walk -> bus is two segments with
            # no internal transfer each, yet one vehicle change for the traveller, so summing the
            # segments would under-count a correct plan and summing them as equality would reject it.
            if stated < within_segments:
                errors.append(
                    f"day {number}: route.transfer_count={stated} is fewer than the "
                    f"{within_segments} transfer(s) its own segments declare. The day cannot contain "
                    f"fewer interchanges than the legs inside it.")


@cites
def check_cross_references(plan: dict, errors: list[str], notes: list[str]) -> None:
    """An id or day number pointing at nothing renders as a blank or a dropped card."""
    day_numbers = {_obj(d).get("number") for d in _seq(plan.get("days"))}
    booking = _obj(plan.get("booking_options"))
    for ticket in [t for t in _seq(booking.get("attraction_tickets")) if isinstance(t, dict)]:
        target = ticket.get("day_number")
        if target is not None and target not in day_numbers:
            errors.append(
                f"attraction ticket '{ticket.get('attraction_name')}' references day {target}, "
                f"which is not in this plan (days: {sorted(n for n in day_numbers if n is not None)}).")

    # A ticket's day_number was only ever checked for EXISTING among the days, so a ticket saying
    # day 1 while the activity that uses it sat on day 2 passed -- which is the recorded defect
    # from the Tokyo run, a time-critical ticket pointed at the wrong evening, and it survived the
    # fix that was supposed to close it. Membership is not agreement. Reproduced on a two-day plan
    # before this was written: zero findings either way.
    scheduled_on: dict[str, set] = {}
    for day in [_obj(d) for d in _seq(plan.get("days"))]:
        for activity in [_obj(a) for a in _seq(day.get("activities"))]:
            ref = activity.get("ticket_option_id")
            if ref:
                scheduled_on.setdefault(ref, set()).add(day.get("number"))
    for ticket in [t for t in _seq(booking.get("attraction_tickets")) if isinstance(t, dict)]:
        target = ticket.get("day_number")
        days_used = {n for n in scheduled_on.get(ticket.get("id"), set()) if n is not None}
        if target is None or not days_used:
            # A ticket nobody scheduled is a booking option, not a contradiction. Only a ticket
            # that names a day AND is used on one can disagree with itself.
            continue
        if days_used != {target}:
            errors.append(
                f"attraction ticket '{ticket.get('attraction_name')}' is dated day {target}, but "
                f"the activity using it is on day {', '.join(str(n) for n in sorted(days_used))}. "
                f"A dated ticket is what the traveller shows at a door on one particular evening, "
                f"so the two have to name the same day -- fix whichever moved.")

    ticket_ids = {t.get("id") for t in _seq(booking.get("attraction_tickets")) if isinstance(t, dict)}
    for day in [_obj(d) for d in _seq(plan.get("days"))]:
        for activity in [_obj(a) for a in _seq(day.get("activities"))]:
            ref = activity.get("ticket_option_id")
            if ref and ref not in ticket_ids:
                errors.append(
                    f"day {day.get('number')}: activity '{activity.get('name')}' references ticket "
                    f"'{ref}', which no attraction_tickets entry defines.")


def _english_weekday_claim(day: dict, date: dt.date, blob: str) -> str | None:
    """The first English weekday assertion in this day's text that the calendar contradicts.

    A claim counts only when it names this day: "today"/"this day", or a day number or ISO date
    equal to this day's own. A sentence about day 3 sitting inside day 1's text is judged against
    day 3, or not at all -- charging it to the wrong day would be a false accusation, and the first
    of those teaches an author to stop reading this gate's output."""
    for pattern in (_EN_DAY_CLAIM, _EN_DAY_PAREN):
        for match in pattern.finditer(blob):
            number = match.group("daynum")
            if number is not None and str(day.get("number")) != str(int(number)):
                continue
            iso = match.group("date")
            if iso is not None and iso != date.isoformat():
                continue
            index = _EN_WEEKDAY_INDEX.get(match.group("weekday").lower())
            if index is None or index == date.weekday():
                continue
            quoted = re.sub(r"\s+", " ", match.group(0)).strip()
            return (
                f"day {day.get('number')} ({date}) is a {WEEKDAYS[date.weekday()][2].title()} but its "
                f"text asserts '{quoted}'. A weekday-gated venue or service will be wrong. Recompute "
                f"the weekday from the date, or fix the date.")
    return None


@cites
def check_dates(plan: dict, errors: list[str], notes: list[str]) -> None:
    trip = _obj(plan.get("trip"))
    try:
        start = dt.date.fromisoformat(str(trip.get("start_date")))
        end = dt.date.fromisoformat(str(trip.get("end_date")))
    except (TypeError, ValueError):
        errors.append("trip.start_date / trip.end_date must be ISO dates.")
        return

    if end < start:
        # Left unguarded this passes silently: the day-coverage loop below builds an empty
        # expected list, so it compares the plan's days against nothing and finds no gap.
        errors.append(
            f"trip.start_date {start} is after trip.end_date {end}. Every date check downstream "
            f"iterates the window, so a reversed one disables them all instead of failing.")
        return

    expected = []
    cursor = start
    while cursor <= end:
        expected.append(cursor)
        cursor += dt.timedelta(days=1)

    actual = []
    for day in [_obj(d) for d in _seq(plan.get("days"))]:
        try:
            actual.append(dt.date.fromisoformat(str(day.get("date"))))
        except (TypeError, ValueError):
            errors.append(f"day {day.get('number')}: date is not an ISO date.")
            return

    if actual != expected:
        errors.append(
            f"days must cover every date from {start} to {end} exactly once in order; "
            f"got {[d.isoformat() for d in actual]}.")

    # A weekday named in prose is a claim the calendar can settle.
    for day in [_obj(d) for d in _seq(plan.get("days"))]:
        try:
            date = dt.date.fromisoformat(str(day.get("date")))
        except (TypeError, ValueError):
            continue
        blob = json.dumps(day, ensure_ascii=False)
        problem = None
        for match in _DAY_CLAIM.finditer(blob):
            token = match.group(1)
            index = _CN_WEEKDAY.get(token)
            if index is not None and index != date.weekday():
                problem = (
                    f"day {day.get('number')} ({date}) is a {WEEKDAYS[date.weekday()][0]} but its text "
                    f"asserts '{match.group(0)}'. A weekday-gated venue or service will be wrong.")
                break
        if problem is None:
            problem = _english_weekday_claim(day, date, blob)
        if problem:
            errors.append(problem)


def _jurisdiction_key(value: object) -> str:
    """One jurisdiction, one key, however the author spelled it.

    Compared raw, `Japan` and `japan ` were two jurisdictions and the traveller was told their
    single-country trip entered both -- the same free-text trap this file warns about for
    `base_location`, reintroduced in the field that was added to avoid it.

    A full-width space needs no special handling, and an earlier version stripped one anyway with
    a comment claiming it was necessary: `str.strip()` already removes U+3000, because Python
    counts it as whitespace. The redundant call was harmless and the comment was not -- a false
    reason in a comment is what the next reader builds on.
    """
    return str(value or "").strip().casefold()


@cites
def check_entry_covers_every_jurisdiction(plan: dict, errors: list[str], notes: list[str]) -> None:
    """A trip that enters two places needs two entry answers, and used to need one.

    `entry_context` is a single object -- one status, one summary, one source_url, one checked_at --
    and every gate was satisfied by it. So a Bangkok/Hanoi/Phnom Penh trip could carry Thailand's
    answer alone, cite an official Thai source, pass, and print "visa-free" on a page that is wrong
    for two of the three countries. A wrong entry answer is not a disappointment like a closed
    restaurant; it is a denial of boarding, and it is the one finding on this page the traveller
    cannot recover from at the airport.

    Multi-stop trips only. A single-stay trip keeps the flat form exactly as it was, so nothing
    that already ships changes shape.

    `jurisdiction` and not `country`, because the distinction that matters here is not political:
    Hong Kong and the mainland are one country and two entry regimes, and a mainland passport needs
    a permit to cross between them. It is free text on purpose -- the gate checks COVERAGE, never
    identity, so an author who writes 「申根区」 for Paris and Berlin gets one record and an author
    who writes 「法国」/「德国」 gets two, and both are defensible readings of the same trip.
    """
    stays = [_obj(a) for a in _seq(_obj(plan.get("booking_options")).get("accommodations"))]
    groups: dict[str, set[str]] = {}
    for stay in stays:
        group = str(stay.get("stay_group_id") or "").strip()
        if not group:
            continue
        groups.setdefault(group, set()).add(_jurisdiction_key(stay.get("jurisdiction")))
    if len(groups) < 2:
        return

    unnamed = sorted(g for g, values in groups.items() if not any(values - {""}))
    if unnamed:
        errors.append(
            f"this trip sleeps in {len(groups)} places and {len(unnamed)} of them do not say which "
            f"entry jurisdiction they are in ({', '.join(unnamed)}). Set `jurisdiction` on each "
            f"accommodation -- 「日本」, 「中国大陆」, 「香港」, 「申根区」 -- because without it "
            f"nothing can tell whether this trip needs one entry answer or three, and one answer "
            f"covering three countries is wrong about two of them.")
        return

    needed = {v for values in groups.values() for v in values if v}
    if len(needed) < 2:
        return

    context = _obj(plan.get("entry_context"))
    records = [_obj(r) for r in _seq(context.get("per_jurisdiction"))]
    covered = {_jurisdiction_key(r.get("jurisdiction")) for r in records} - {""}
    missing = sorted(needed - covered)
    if missing:
        errors.append(
            f"this trip enters {len(needed)} jurisdictions ({', '.join(sorted(needed))}) and "
            f"entry_context answers for {len(covered) or 'none'} of them. Missing: "
            f"{', '.join(missing)}. Add one entry_context.per_jurisdiction record per jurisdiction, "
            f"each with its own status, summary, traveler_basis, source_url and checked_at -- a "
            f"second country's rules are not a footnote to the first country's, and the flat "
            f"entry_context fields describe one place only.")
        return

    incomplete = [str(r.get("jurisdiction")) for r in records
                  if not all(r.get(f) for f in
                             ("status", "summary", "traveler_basis", "source_url", "checked_at"))]
    if incomplete:
        errors.append(
            f"entry_context.per_jurisdiction names {', '.join(incomplete)} without the evidence "
            f"the single-jurisdiction form has always required (status, summary, traveler_basis, "
            f"source_url, checked_at). A record that names a country and cites nothing reads on "
            f"the page as an answer that was checked.")


def unverified_entry_answers(plan: dict) -> list[str]:
    """Every entry answer the plan still marks `unverified` -- the flat one and each jurisdiction's."""
    entry = _obj(plan.get("entry_context"))
    found = ["entry_context"] if str(entry.get("status") or "") == "unverified" else []
    for index, record in enumerate(_seq(entry.get("per_jurisdiction"))):
        if str(_obj(record).get("status") or "") == "unverified":
            found.append(f"entry_context.per_jurisdiction[{index}] "
                         f"({_obj(record).get('jurisdiction')})")
    return found


def _unverified_entry_message(open_answers: list[str]) -> str:
    return (f"this plan is marked verified while its entry answer is still unverified: "
            f"{', '.join(open_answers)}. Whether the traveller may enter is the one answer that "
            f"decides whether they board; settle it (it is the entry domain's job), or save with "
            f"--unverified so the page says so.")


@cites
def check_verified_plan_entry_answer(plan: dict, errors: list[str], notes: list[str]) -> None:
    """A plan that calls itself verified cannot leave open the answer that decides boarding.

    Measured 2026-09-24 against v2.7.0: a Netherlands-to-US plan saved as verified with
    `entry_context.status: unverified` produced 0 findings and a page with no banner. A plan that
    says it is unverified already carries the banner, so only the verified claim is tested here;
    check_verification refuses the same thing on the way in, before the claim is written.
    """
    if str(plan.get("verification_status") or "") != "verified":
        return
    open_answers = unverified_entry_answers(plan)
    if open_answers:
        errors.append(_unverified_entry_message(open_answers))


@cites
def check_rooms_hold_the_party(plan: dict, errors: list[str], notes: list[str]) -> None:
    """A hotel card is booked for the whole party: its guest_count is the trip's traveler_count.

    Walked on 2026-09-24: a party that grew from four to five after a verified save kept four hotel
    cards "for 4 guests", each with a search link for 2 adults + 2 children, and the page shipped
    verified. The link check compares a link with its own card's guest_count, so a card and a link
    that agree with each other and not with the trip passed everything. A room for four is the
    wrong room for five whether or not the page is verified, so this is a plan check rather than a
    verification one. Measured before it existed: none of the 18 real plans in the author's
    workspace disagrees, so it refuses nothing that was right.
    """
    count = _obj(plan.get("trip")).get("traveler_count")
    if isinstance(count, bool) or not isinstance(count, int) or count < 1:
        return
    for option in [_obj(o) for o in _seq(_obj(plan.get("booking_options")).get("accommodations"))]:
        guests = option.get("guest_count")
        if isinstance(guests, bool) or not isinstance(guests, int) or guests == count:
            continue
        name = str(option.get("property_name") or "?")
        errors.append(
            f"accommodation '{name}' ({option.get('id') or 'no id'}) is for {guests} guest(s) and "
            f"the trip is for {count}. Re-price the room product for {count}: room_count, "
            f"room_basis, the nightly cost and the search link all follow the party.")


@cites
def check_stay_groups_do_not_overlap(plan: dict, errors: list[str], notes: list[str]) -> None:
    """Two stay groups must not claim the same night.

    A multi-stop trip is a sequence of stays, and the one arithmetic mistake it makes that no
    existing check catches is paying for two hotels on one night. Every per-day check passes:
    each day points at one accommodation, and that accommodation's window really does cover the
    day. It is the pair that is wrong, and nothing had ever looked at a pair, because until a trip
    has more than one stay group there is no pair to look at.

    Checkout day is not a night, so `[check_in, check_out)` is the interval and a group starting on
    the day the previous one ends is the correct shape rather than a collision -- which is exactly
    what the two real multi-stay plans in the author's workspace do (10-25..10-27 then
    10-27..10-28). Dates only: no string matching against place names, which are free text and
    were already found being written three different ways for one base.
    """
    windows: dict[str, list[tuple[dt.date, dt.date]]] = {}
    for option in [_obj(a) for a in _seq(_obj(plan.get("booking_options")).get("accommodations"))]:
        group = str(option.get("stay_group_id") or "").strip()
        if not group:
            continue
        try:
            start = dt.date.fromisoformat(str(option.get("check_in")))
            end = dt.date.fromisoformat(str(option.get("check_out")))
        except (TypeError, ValueError):
            continue          # check_accommodation_coverage already reports a non-ISO window
        windows.setdefault(group, []).append((start, end))

    spans = {group: (min(w[0] for w in pairs), max(w[1] for w in pairs))
             for group, pairs in windows.items() if pairs}
    ordered = sorted(spans.items(), key=lambda kv: kv[1])
    for (left, (left_in, left_out)), (right, (right_in, right_out)) in zip(ordered, ordered[1:]):
        if right_in < left_out:
            nights = (min(left_out, right_out) - right_in).days
            errors.append(
                f"stay groups '{left}' ({left_in}..{left_out}) and '{right}' "
                f"({right_in}..{right_out}) overlap by {nights} night(s), so the traveller is "
                f"booked into two places at once and paying for both. A checkout date may equal "
                f"the next check-in date; it may not fall after it.")


@cites
def check_accommodation_coverage(plan: dict, errors: list[str], notes: list[str]) -> None:
    stays = {a.get("id"): a for a in _seq(_obj(plan.get("booking_options")).get("accommodations")) if isinstance(a, dict)}
    for day in [_obj(d) for d in _seq(plan.get("days"))]:
        stay_id = day.get("accommodation_option_id")
        if not stay_id:
            continue
        stay = _obj(stays.get(stay_id)) or None
        if stay is None:
            errors.append(f"day {day.get('number')}: accommodation_option_id '{stay_id}' has no matching option.")
            continue
        try:
            date = dt.date.fromisoformat(str(day.get("date")))
            check_in = dt.date.fromisoformat(str(stay.get("check_in")))
            check_out = dt.date.fromisoformat(str(stay.get("check_out")))
        except (TypeError, ValueError):
            errors.append(f"day {day.get('number')}: accommodation '{stay_id}' has non-ISO check_in/check_out.")
            continue
        # The departure day is a checkout, never an extra night, so it may equal check_out.
        if not (check_in <= date <= check_out):
            errors.append(
                f"day {day.get('number')} ({date}) references stay '{stay_id}' whose window is "
                f"{check_in}..{check_out}.")
        if day.get("day_type") == "departure" and date != check_out:
            errors.append(
                f"day {day.get('number')}: departure day {date} should be the checkout date "
                f"({check_out}), otherwise a night is being paid for twice.")


@cites
def check_dining(plan: dict, errors: list[str], notes: list[str]) -> None:
    """Three failures that shipped once: a dinner 2.5 km off the day's route with no leg to
    reach it, meals scheduled at venues that had already closed, and -- once this check existed --
    opening hours written the realistic way ("周二至周日 15:00-21:00"), which parsed as nothing and
    turned the hours check off in silence."""
    for day in [_obj(d) for d in _seq(plan.get("days"))]:
        number = day.get("number")
        route_blob = _route_text(day)
        stops = [str(s) for s in _seq(_route(day).get("stops_in_order"))]
        try:
            date = dt.date.fromisoformat(str(day.get("date")))
        except (TypeError, ValueError):
            date = None  # check_dates owns that finding; reporting it twice helps nobody
        for raw in _seq(day.get("dining")):
            if not isinstance(raw, dict):
                errors.append(f"day {number}: a dining entry is {type(raw).__name__}, not an object.")
                continue
            card = raw
            venue = str(card.get("venue_name") or "").strip()
            if not venue:
                errors.append(f"day {number}: a dining card has no venue_name.")
                continue

            # Matching the venue name against stop names does not work -- stops name areas
            # ("Pike Place 市场") while a card names a business ("IL Bistro"). Require the
            # author to say which stop the meal hangs off, and check that stop is real.
            anchor = str(card.get("route_anchor") or "").strip()
            justification = str(card.get("off_route_justification") or "").strip()
            if anchor:
                if anchor not in stops:
                    errors.append(
                        f"day {number}: dining venue '{venue}' has route_anchor '{anchor}', which is "
                        f"not one of this day's stops_in_order {stops}.")
            elif not justification and venue not in route_blob:
                errors.append(
                    f"day {number}: dining venue '{venue}' has no route_anchor and no "
                    f"off_route_justification. Every meal must hang off a stop on the day's route, "
                    f"or state the detour it costs -- an unrouted dinner is how 4 km of walking "
                    f"goes unnoticed.")

            hours = card.get("venue_hours")
            status = str(card.get("hours_status") or "").strip().lower()
            if _unfilled(venue, hours):
                continue      # an unfilled card is reported once by check_venue_quality
            if not hours:
                errors.append(
                    f"day {number}: dining venue '{venue}' has no venue_hours. This card names a "
                    f"seating time, and naming one is the claim that the venue is open then -- so "
                    f"the hours for that weekday have to be read, not left blank. (This used to "
                    f"offer hours_status='unverified' as a way out. It is not one: a card without "
                    f"a time_window is refused by the renderer, so the escape led nowhere. Ratings "
                    f"keep an honest 'none' path because a market has no single score; hours do "
                    f"not, because a traveller standing at a closed door is not an information "
                    f"gap, it is a ruined afternoon.)")
                continue
            window = _parse_window(card.get("time_window"))
            if not isinstance(hours, str) or not hours.strip():
                continue

            # Until this rewrite the hours check rewarded the *less* informative string: the
            # realistic "Tue-Sun 15:00-21:00" parsed as nothing and silently skipped, while the
            # information-losing "15:00-21:00" turned the check on. So an unreadable string is now
            # a finding rather than a free pass, and the format is spelled out here rather than
            # left for the author to guess.
            open_days, opening = _parse_venue_hours(hours)
            if open_days is None and has_ambiguous_weekday(hours):
                # The string opens with Ma/Di/Do, which name different days in different languages
                # (see AMBIGUOUS_WEEKDAY_TOKENS). Guessing one would hand the weekday check a set
                # that can be wrong by a whole day; saying nothing would silently drop the check,
                # which is the failure this rewrite exists to end. So ask, and say what to write.
                errors.append(
                    f"day {number}: dining venue '{venue}' has venue_hours {hours!r}, which starts "
                    f"with a weekday abbreviation that means different days in different languages "
                    f"-- 'Ma' is Monday in Dutch but Tuesday in French, Spanish and Italian; 'Di' "
                    f"is Tuesday in German but Sunday in French; 'Do' is Thursday in German and "
                    f"Dutch but Sunday in Spanish and Italian. Write the day in full "
                    f"('Mittwoch-Samstag', 'mardi-samedi') or in English ('Tue-Sat'), so the "
                    f"closed-day check can run instead of quietly skipping this venue.")
                continue
            if open_days is None and _WEEKDAY_TOKEN.search(hours):
                # The string names a weekday and the parser still could not settle the open set --
                # so it says something more than "these days, these hours", and the most common
                # something is a rest day: "Montag geschlossen", "周一休息", "Ruhetag Montag",
                # "lundi fermé". Reading those as the open set inverts the answer exactly, which is
                # how a dinner gets approved on the one day the kitchen is dark. Refusing is right;
                # refusing SILENTLY is not, because the closed-day check then just stops running.
                errors.append(
                    f"day {number}: dining venue '{venue}' has venue_hours {hours!r}, which names a "
                    f"weekday but does not reduce to open days plus times, so the closed-day check "
                    f"cannot run on it. Rewrite it as the days the venue is OPEN -- a rest day of "
                    f"Monday becomes 'Tue-Sun 11:00-22:00' -- because a string that states a "
                    f"closure reads as its own opposite to any parser that guesses.")
                continue
            if not opening:
                errors.append(
                    f"day {number}: dining venue '{venue}' has venue_hours {hours!r}, which contains "
                    f"no readable time window, so the opening-hours check would skip it in silence. "
                    f"Write it machine-checkably -- '15:00-21:00', '11:00-15:00, 17:00-21:00', "
                    f"'Tue-Sun 15:00-21:00', '周二至周日 15:00-21:00' -- or drop venue_hours and set "
                    f"hours_status='unverified' to say plainly that nobody checked.")
                continue
            # The per-weekday table wins when the card carries one: it is the sharper claim, and
            # it is the only one that can say "closed on Tuesday" without inverting into its
            # opposite the way a prose closure does.
            exact, exact_raw = _per_weekday_window(card, date)
            if exact == "unreadable":
                errors.append(
                    f"day {number}: '{venue}' has venue_hours_by_weekday for this weekday set to "
                    f"{exact_raw!r}, which carries no readable time window. Write it as "
                    f"'11:00-22:00' (two windows as '11:00-15:00, 17:00-21:00'), or as 'closed'/"
                    f"「休息」 for a day it is shut -- an unreadable string is not a closed day, and "
                    f"reading it as one refuses a meal at a venue that is open. Use ASCII colons "
                    f"and hyphens: a full-width 「－」 does not parse.")
            elif exact is not None:
                if not exact:
                    errors.append(
                        f"day {number} ({date}) is a {WEEKDAYS[date.weekday()][0]}/"
                        f"{WEEKDAYS[date.weekday()][2].title()}, and '{venue}' lists that weekday "
                        f"as closed in venue_hours_by_weekday. Move the meal, or take the backup.")
                elif window and not any(window[0] >= start and window[1] <= end
                                        for start, end in exact):
                    errors.append(
                        f"day {number}: '{venue}' is scheduled {card.get('time_window')} but its "
                        f"hours on that weekday are {exact_raw}.")
            elif window and not any(window[0] >= start and window[1] <= end for start, end in opening):
                errors.append(
                    f"day {number}: '{venue}' is scheduled {card.get('time_window')} but its hours "
                    f"are {hours}.")
            if open_days is not None and date is not None and date.weekday() not in open_days:
                errors.append(
                    f"day {number} ({date}) is a {WEEKDAYS[date.weekday()][0]}/"
                    f"{WEEKDAYS[date.weekday()][2].title()}, but '{venue}' has venue_hours {hours!r}, "
                    f"which only cover "
                    f"{', '.join(f'{WEEKDAYS[i][0]}({WEEKDAYS[i][2][:3].title()})' for i in sorted(open_days))}. "
                    f"Move the meal to a day the venue opens, choose the backup venue, or correct "
                    f"the weekday prefix -- a closed door at 19:00 is a missed dinner, not a note.")


WEEKDAY_KEYS = ("mon", "tue", "wed", "thu", "fri", "sat", "sun")


def _per_weekday_window(card: dict, date) -> tuple[list[tuple[int, int]] | None, str | None]:
    """(windows for THIS date, the raw string) from venue_hours_by_weekday, or (None, None).

    `venue_hours` has to reduce to one open-days-plus-times set so the closed-day check can run on
    it, and that requirement costs real information: a venue open 11:00-22:00 on weekdays and
    08:30-23:00 at the weekend can only be written as the narrowest window that holds every day.
    On a real run all eight venues were researched per weekday and all eight were flattened -- the
    traveller received less than had been checked, and the loss was not necessary, only unmodelled.

    So the card may ALSO carry the per-weekday table. When it does, this is what the meal is
    checked against, because it is the sharper claim: `null` for a day means closed that day, which
    the flattened string cannot express at all. `venue_hours` stays required as the human summary
    and the fallback.
    """
    table = card.get("venue_hours_by_weekday")
    if not isinstance(table, dict) or date is None:
        return None, None
    raw = table.get(WEEKDAY_KEYS[date.weekday()], None)
    # `null` keeps the meaning it has everywhere else in this contract -- NOT FILLED IN -- and
    # falls back to the flattened venue_hours. Closure is written as the word, because a null that
    # silently meant "closed" would turn an unfilled skeleton into a venue shut seven days a week,
    # and the one convention this file must not break is the one every other field follows.
    if raw is None or not str(raw).strip():
        return None, None
    if str(raw).strip().casefold() in ("closed", "休息", "闭店", "不营业"):
        return [], None
    _, windows = _parse_venue_hours(str(raw))
    if not windows:
        # UNREADABLE IS NOT CLOSED, and conflating them inverts the answer exactly. The flattened
        # path has refused an unparseable venue_hours since the day it was written -- "contains no
        # readable time window, so the opening-hours check would skip it in silence" -- and this
        # path was built without the same guard, so a full-width dash (「11:30－23:00」, which a
        # Chinese keyboard produces by default) or a phrase like 「看心情」 silently became "shut
        # all day" and refused a meal at a venue that was open. Same Latin-constant-meets-CJK
        # shape this repository has now paid for five times.
        return "unreadable", str(raw)
    return windows, str(raw)


@cites
def check_meal_reachability(plan: dict, errors: list[str], notes: list[str]) -> None:
    """A meal must be reachable, not merely well-placed on the map.

    `check_dining` already proves a meal hangs off a real stop, and `check_clock_closure` proves
    the day's activities do not overlap. Neither notices the case in between: a lunch window that
    opens while the traveller is still at the previous stop, because the leg that carries them to
    the meal's anchor takes time the window never accounts for.

    That shipped. A Sunday lunch was written 13:00-14:30 anchored at a stop the traveller could
    not reach before 14:15 -- the preceding activity ran to 14:00 and the plan's own segment to
    that stop costs 15 minutes -- leaving fifteen minutes of a ninety-minute window. Every gate
    passed: the anchor was real, the hours contained the window, the activities did not overlap,
    and the day had 142 minutes of slack overall, so no span check could see it either.

    REPORTS AS A NOTE, NOT AN ERROR, and that demotion is the honest position rather than a
    softening. The arithmetic needs one fact the plan does not carry: whether the traveller is
    already standing at the anchor when the window opens. Charging the leg unconditionally --
    which is what the first two versions did -- rejects the most ordinary shape `route_anchor`
    produces: a lunch at the stop the morning activity happened at, billed for the ride that
    brought them there hours earlier. On this repo's own fixture, three hours at 'Fixture activity
    A' followed by lunch at 'Fixture activity A' was reported unreachable before 12:25.

    Nothing available distinguishes the two cases. `activities[].area_or_venue` is empty in the
    fixture and free text in real plans ('Belgisches Viertel' against an anchor of '比利时区
    Belgisches Viertel'), so matching it is locale-dependent guessing. A `dining[].activity_ref`
    would settle it and is the right fix when someone next touches the contract.

    Until then the number is worth printing and not worth enforcing: it caught a real defect (a
    departure-day meal with ten minutes of its window actually reachable) and it produced two
    distinct shapes of false positive. A gate that fails correct work gets switched off, and then
    the true positives go too."""
    for day in [_obj(d) for d in _seq(plan.get("days"))]:
        number = day.get("number")
        segments = _segments(day)
        if not segments:
            continue

        # Latest end of any activity that finishes before this point in the day.
        timed: list[tuple[int, int]] = []
        for activity in [_obj(a) for a in _seq(day.get("activities"))]:
            start = _parse_hhmm(str(activity.get("time") or ""))
            if start is None:
                continue
            timed.append((start, start + int(_num(activity.get("duration_minutes")))))
        if not timed:
            continue

        for raw in _seq(day.get("dining")):
            card = _obj(raw)
            anchor = str(card.get("route_anchor") or "").strip()
            window = _parse_window(card.get("time_window"))
            if not anchor or not window:
                continue
            leg = next((s for s in segments if str(s.get("to") or "").strip() == anchor), None)
            if leg is None:
                continue  # no modelled leg to that stop; nothing to compute from
            travel = int(_num(leg.get("duration_minutes")))

            # Only activities that finish before the window OPENS count. The first draft used
            # "before the window closes", which swept in the meal's own activity slot -- a dinner
            # scheduled 19:00-20:30 with a matching 19:00-20:30 activity was read as needing to
            # travel 25 minutes after that activity ended, and the gate reported a real dinner as
            # impossible. Three false positives on a four-day plan, which is how a gate gets
            # switched off.
            #
            # The cost of the narrower rule, stated plainly: an activity that starts before the
            # window and runs into it is no longer counted, so a meal overlapping a *different*
            # stop's activity is not caught here. Distinguishing "this activity IS the meal" from
            # "this activity conflicts with the meal" needs a link the plan does not carry; adding
            # dining[].activity_ref would close it. Until then this gate is deliberately narrow
            # and silent rather than broad and wrong.
            prior_ends = [end for _, end in timed if end <= window[0]]
            if not prior_ends:
                continue
            earliest = max(prior_ends) + travel
            if earliest <= window[0]:
                continue
            remaining = window[1] - earliest
            if remaining >= MEAL_MINIMUM_MINUTES:
                continue
            notes.append(
                f"day {number}: '{card.get('venue_name')}' is booked {card.get('time_window')} at "
                f"'{anchor}'. If the traveller is not already at that stop, they cannot arrive "
                f"before {_fmt_hhmm(earliest)} -- the previous activity ends at "
                f"{_fmt_hhmm(max(prior_ends))} and this day's leg to that stop takes {travel} min "
                f"-- leaving {max(remaining, 0)} min of the window, under the "
                f"{MEAL_MINIMUM_MINUTES} min a meal needs. Check this one by eye: the plan cannot "
                f"say whether that leg is still ahead of them.")


@cites
def check_budget(plan: dict, errors: list[str], notes: list[str]) -> None:
    budget = _obj(plan.get("budget"))
    rows = [r for r in _seq(budget.get("breakdown")) if isinstance(r, dict)]
    included = set(_seq(budget.get("included_categories")))
    if not rows:
        return

    priced = {r.get("category") for r in rows}
    for category in sorted(c for c in included if c not in priced):
        errors.append(
            f"budget.included_categories lists {category!r} but no breakdown row prices it. The "
            f"page then claims the per-person total covers something it never itemises, which is "
            f"the black-box total the breakdown exists to prevent.")

    low = sum(_num(r.get("per_person_low")) for r in rows if r.get("category") in included)
    high = sum(_num(r.get("per_person_high")) for r in rows if r.get("category") in included)
    stated_low = _num(budget.get("estimated_per_person_low"))
    stated_high = _num(budget.get("estimated_per_person_high"))
    if included:
        if abs(stated_low - low) > COST_TOLERANCE:
            errors.append(
                f"budget.estimated_per_person_low={stated_low:g} but the included categories "
                f"{sorted(included)} sum to {low:g}.")
        if abs(stated_high - high) > COST_TOLERANCE:
            errors.append(
                f"budget.estimated_per_person_high={stated_high:g} but the included categories "
                f"sum to {high:g}.")

    # Ticket prices and the attractions budget line must agree with each other.
    tickets = [t for t in _seq(_obj(plan.get("booking_options")).get("attraction_tickets")) if isinstance(t, dict)]
    if tickets:
        t_low = sum(_num(t.get("price_low")) for t in tickets)
        t_high = sum(_num(t.get("price_high")) for t in tickets)
        for row in rows:
            if row.get("category") == "attractions":
                if abs(_num(row.get("per_person_low")) - t_low) > COST_TOLERANCE:
                    errors.append(
                        f"budget attractions low={_num(row.get('per_person_low')):g} but the listed "
                        f"tickets sum to {t_low:g}.")
                if abs(_num(row.get("per_person_high")) - t_high) > COST_TOLERANCE:
                    errors.append(
                        f"budget attractions high={_num(row.get('per_person_high')):g} but the listed "
                        f"tickets sum to {t_high:g}.")

    cap = budget.get("cap_per_person")
    if isinstance(cap, (int, float)) and stated_high > cap + COST_TOLERANCE:
        if budget.get("overrun_acknowledged") is not True:
            errors.append(
                f"budget high case {stated_high:g} exceeds cap_per_person {cap:g} but "
                f"budget.overrun_acknowledged is not true. A cap the traveller never agreed to "
                f"break must not be broken silently.")
        else:
            notes.append(f"budget high case {stated_high:g} exceeds cap {cap:g} (acknowledged).")


@cites
def check_replan_context(plan: dict, errors: list[str], notes: list[str]) -> None:
    """A replanned trip carries a list of facts the change invalidated; none may still be open.

    Dates are the dangerous delta, because almost everything researched under a day is keyed to a
    *weekday* rather than to a date: opening hours, closure days, market days, Sunday retail law,
    a museum that shuts Mondays. Move the window by one day and all of it quietly becomes a guess
    while the plan still looks complete and still passes every other check here. replan_trip.py
    records each such fact in replan_context.must_reverify; this is the gate that refuses to ship
    the plan while any of them is unresolved -- the same rule, and deliberately the same shape, as
    an unresolved verification finding in check_verification.

    A plan with no replan_context has nothing to re-verify, and nothing here fires.
    """
    context = plan.get("replan_context")
    if context is None:
        return
    if not isinstance(context, dict):
        errors.append(
            f"replan_context is {type(context).__name__}, not an object. Its must_reverify list is "
            f"the only record of what the replan could not recompute, so a block this gate cannot "
            f"read drops every one of those entries in silence. Write the shape in "
            f"templates/replan-request.json, or remove replan_context entirely.")
        return

    entries = context.get("must_reverify")
    if entries is not None and not isinstance(entries, list):
        errors.append(
            f"replan_context.must_reverify is {type(entries).__name__}, not a list. It holds one "
            f"entry per fact the replan could not carry over: "
            f'{{"path": "days[2].dining[0].venue_hours", "reason": "...", "resolved": false, '
            f'"resolution": null}}.')
        return

    open_entries = 0
    for position, raw in enumerate(_seq(entries)):
        if not isinstance(raw, dict):
            errors.append(
                f"replan_context.must_reverify[{position}] is {type(raw).__name__}, not an object. "
                f'Each entry needs at least a "path", a "reason" and "resolved".')
            continue
        resolved = raw.get("resolved")
        if resolved is True:
            # The message below asks for two things and this used to check one. Flipping every
            # flag to true with no resolution text shipped a replanned plan whose weekday-keyed
            # facts -- opening hours researched for a Monday that is now a Thursday -- were never
            # re-checked, and the gate said all resolved. Same reasoning as `not_pursued` owing a
            # sentence: an escape nobody has to justify is a way to switch a rule off rather than
            # to answer it, and here the rule being switched off is the only record that the
            # research underneath the plan has expired.
            resolution = raw.get("resolution")
            if not isinstance(resolution, str) or not resolution.strip():
                errors.append(
                    f"replan_context.must_reverify[{position}] is marked resolved with no "
                    f"'resolution': {raw.get('path')!r}. Write what you actually found when you "
                    f"re-checked it -- the new hours, the new fare, or that it was unaffected. A "
                    f"bare true is the same claim as an unresolved entry, made harder to see.")
            elif any(marker in resolution for marker in PLACEHOLDER_MARKERS):
                errors.append(
                    f"replan_context.must_reverify[{position}].resolution still holds a "
                    f"placeholder: {_short(resolution)}.")
            continue
        open_entries += 1
        # Anything other than the literal `true` is called out for what it is: "resolved": "yes"
        # reads as done to a human skimming the JSON and is not done to anything that checks.
        wording = "" if resolved is None or resolved is False else (
            f" (resolved is {_short(resolved)}, not the JSON literal true)")
        errors.append(
            f"replan_context.must_reverify[{position}] is unresolved{wording}: "
            f"{raw.get('path')!r} -- {raw.get('reason')}. Re-check that field against the new "
            f"plan, record what you found in 'resolution', and set 'resolved': true. Until then "
            f"the plan is shipping a fact that was researched for conditions it no longer has.")

    total = len([e for e in _seq(entries) if isinstance(e, dict)])
    if total and not open_entries:
        notes.append(
            f"replanned from {context.get('replanned_from')}: {total} must_reverify "
            f"entr{'y' if total == 1 else 'ies'}, all resolved.")


# --------------------------------------------------------------------------------------
# Verification report (produced by the parallel-verify stage; see references/verification.md)
# --------------------------------------------------------------------------------------

REQUIRED_DOMAINS = {"entry", "transport", "sights_and_hours", "booking_and_lodging", "seasonality"}
REQUIRED_AUDITS = {"consistency", "completeness"}
# The light tier keeps the two domains whose facts strand a traveller rather than disappoint one:
# `sights_and_hours`, because opening hours are weekday-keyed and a wrong one is a locked door, and
# `transport`, because the leg between two places is the single point of failure in any day. The
# first draft dropped `transport` on the reasoning that a trip with no flight has no transport to
# check -- which is exactly backwards for the trip the light tier is FOR: a two-night rail city
# break is nothing but transport, and nobody would have verified that the named train runs on that
# date, in that direction, at that fare.
#
# What light still drops, and why each is defensible: `entry` re-derives a fact the research budget
# forbids re-litigating once the traveller has stated it; `booking_and_lodging`'s airline-window and
# codeshare checks have no subject where there is no flight; `seasonality` matters where the plan
# schedules a sunset or leans on a seasonal service, and a short indoor-anchored city break does
# neither. The two audits are never optional at any tier: they need no network and, in the run that
# made them mandatory, produced 27 of 55 findings and 5 of the 6 criticals.
LIGHT_TIER_DOMAINS = {"sights_and_hours", "transport"}


def required_domains_for(plan: dict | None) -> tuple[set[str], str]:
    """Which truth domains this specific plan must carry, read off the plan rather than asserted.

    A two-night rail trip inside the traveller's own country, with no allergy and no walking cap,
    was paying the same seven-block pass as a multi-city flight itinerary with an anaphylactic
    traveller -- and three of those blocks had no subject: `entry` re-litigates a fact the research
    budget forbids re-litigating, `booking_and_lodging`'s airline-window and codeshare checks apply
    to a trip with no flight, and `seasonality` matters where a sunset or a seasonal service is
    scheduled. Charging for them anyway teaches operators to reach for --unverified, which costs
    far more than it saves.

    Deliberately conservative: every condition must hold, anything unknown counts as not holding,
    and the tier is computed here rather than declared in the report, because a tier the report
    asserts is a tier the run grades itself on."""
    plan = _obj(plan)
    if not plan:
        return set(REQUIRED_DOMAINS), "Every domain must be checked, or the gap is invisible."

    disqualifiers: list[str] = []

    if not isinstance(plan.get("booking_options"), dict):
        disqualifiers.append("no booking_options (flights and cars unexamined)")
    else:
        booking = _obj(plan.get("booking_options"))
        # ground_transport belongs here for the same reason flights do, and the reason is the
        # card's contents rather than the vehicle: it asserts a fare range, an availability status
        # and a prefilled search URL, which is precisely what booking_and_lodging verifies. On a
        # rail city break that card is the largest and most time-sensitive purchase on the page,
        # so dropping the domain would leave the one thing the traveller must buy on a deadline as
        # the one thing no verifier looked at. The light tier still stands for a trip that books
        # no transport at all -- already ticketed, or everything within walking distance.
        for field, label in (("flights", "a flight"), ("rental_cars", "a rental car"),
                             ("ground_transport", "a ticketed rail/coach/ferry leg")):
            if _seq(booking.get(field)):
                disqualifiers.append(label)
    arrival = str(_obj(plan.get("trip")).get("arrival_transport_mode") or "")
    if arrival == "flight":
        disqualifiers.append("a flight arrival")
    elif not arrival:
        disqualifiers.append("no arrival_transport_mode (how they get there is unexamined)")

    # A ferry is not expressible in arrival_transport_mode, whose enum is flight/rail/road/other,
    # so the only place it shows up is a budget row. SKILL.md says a ferry needs the full pass --
    # sailings are seasonal, weather-cancelled and often the single point of failure in a day --
    # and without this the doc would promise a check the code cannot see. Same for the two other
    # scheduled-vehicle categories a light-tier trip should not quietly contain.
    if not isinstance(plan.get("budget"), dict):
        disqualifiers.append("no budget (what the trip contains is unexamined)")
    priced = {str(row.get("category")) for row in _seq(_obj(plan.get("budget")).get("breakdown"))
              if isinstance(row, dict)}
    for category, label in (("ferry", "a ferry crossing"), ("flight", "a priced flight"),
                            ("rental_car", "a rental car")):
        if category in priced:
            disqualifiers.append(label)

    # An ABSENT block is not a clean bill of health, it is an unanswered question -- and every plan
    # written before these fields existed lacks both, so treating absence as "no constraint" would
    # silently downgrade exactly the plans nobody has re-examined.
    if not isinstance(plan.get("entry_context"), dict):
        disqualifiers.append("no entry_context (entry unexamined)")
    else:
        entry_status = str(_obj(plan.get("entry_context")).get("status") or "")
        if entry_status != "not_required":
            disqualifiers.append(f"entry_context.status={entry_status or 'unset'!r}")

    trip = _obj(plan.get("trip"))
    if not isinstance(trip.get("traveler_constraints"), dict):
        disqualifiers.append("no traveler_constraints (allergy and mobility unexamined)")
    else:
        constraints = _obj(trip.get("traveler_constraints"))

        # Allowlist, not denylist, and the difference is the whole finding. Written as
        # `if severity in {"intolerance", "severe"}` with an `or "none"` default, every value the
        # code did not recognise passed as safe: null, an absent key, "Severe" with a capital S,
        # "anaphylactic". Worse, new_plan_skeleton.py hardcodes "none" and --from-intake has no
        # source for this field, so the DEFAULT of a plan built the documented way was the value
        # that bought the cheap tier. A traveller who wrote "anaphylactic peanut allergy, I carry
        # an EpiPen" on the form got a plan whose gate printed "no severe allergy".
        severity = constraints.get("allergy_severity")
        if severity not in {"none", "preference"}:
            disqualifiers.append(f"allergy_severity={severity!r} (not a settled 'none'/'preference')")
        elif severity == "none" and _seq(constraints.get("dietary_or_religious_needs")):
            # Only "none" is untrusted here, because "none" is what new_plan_skeleton.py writes
            # automatically and --from-intake never overwrites -- so prose beside it means nobody
            # typed the severity. "preference" is a value an operator can only have entered on
            # purpose, and treating it as suspect billed a vegetarian on a three-night rail trip
            # for four extra verification agents, roughly 400k tokens, to re-derive a fact they had
            # already stated. A tier nobody can reach is a tier nobody uses.
            disqualifiers.append(
                "dietary needs stated in prose while allergy_severity is still the default 'none' "
                "-- type the real severity before claiming the light tier")

        # Same shape for mobility: a prose note nobody converted into a number is a constraint
        # nobody can measure, and dropping four verification domains on the strength of an
        # unconverted note is exactly backwards.
        if constraints.get("max_continuous_walking_minutes") is not None:
            disqualifiers.append("a stated walking cap")
        elif _seq(constraints.get("mobility_notes")):
            disqualifiers.append(
                "mobility notes stated in prose while max_continuous_walking_minutes is null")

        # And the case both branches above still read as settled: nobody typed the field at all.
        # The two clauses this function tests for -- a severity of none/preference, and a null cap
        # -- were, until the skeleton started marking them, EXACTLY the values new_plan_skeleton.py
        # emitted when it could not know the answer. So the plan that had never been asked the
        # question qualified for the cheap tier on the strength of not having been asked, and the
        # reason string above would have told the operator, in so many words, "no severe allergy or
        # walking cap". An untyped constraint is an open question, and an open question is the one
        # thing a tier decision must never read as a clean bill of health.
        # UNTYPED_CONSTRAINTS_MARKER is defined beside check_untyped_constraints further down,
        # with the measurement that motivated it; module-level names resolve at call time, so the
        # constant lives next to the check that owns it rather than being hoisted up here.
        #
        # This was the THIRD inline reading of the one key, and it kept its own shape test long
        # after read_untyped_constraints was written to end exactly that. It cost the same defect
        # the reviewer found in check_untyped_constraints: `sorted(str(f) for f in untyped)` on a
        # marker of {"": "x"} produced named == [""], so the tier explained itself to the operator
        # as "the skeleton's untyped_constraints marker on  -- nobody typed that constraint",
        # naming nothing after the word "on". One reader now, so the two cannot drift again.
        state, named, _ = read_untyped_constraints(constraints)
        if state != UNTYPED_MARKER_CLEAR:
            named = sorted(name.strip() for name in named)
            # The named fields are spliced in rather than the sentence naming both by hand: an
            # author who types one and leaves the other should read which one is still open, and a
            # reason string that says "the allergy severity or the walking cap" when only the cap
            # is marked is the tier explaining itself with a fact that is not true of this plan.
            #
            # And when the marker names nothing readable at all, the reason says THAT rather than
            # pretending to a field list it does not have. Withholding the light tier is still
            # right in that case -- an unreadable marker is an open question nobody can close --
            # but the operator has to be told the tier was withheld because the marker is
            # illegible, not because some field they cannot see is untyped.
            if named:
                disqualifiers.append(
                    "the skeleton's " + UNTYPED_CONSTRAINTS_MARKER + " marker"
                    + f" on {', '.join(named)}"
                    + " -- nobody typed "
                    + ("those constraints" if len(named) != 1 else "that constraint")
                    + ", so the defaults sitting in them are an unanswered question rather than a "
                      "settled 'no constraint'")
            else:
                disqualifiers.append(
                    "the skeleton's " + UNTYPED_CONSTRAINTS_MARKER + " marker in a shape that "
                    "names no field -- check_untyped_constraints reports it entry by entry; until "
                    "it is readable nobody can say which constraints are still unanswered, and an "
                    "unanswerable question is not a settled 'no constraint'")

    # The reason string claimed "single-city" and nothing tested it. Four days across Ghent and
    # Bruges with a coach between them read as light, dropping `transport` -- so nobody checked
    # whether the intercity service runs on that weekday, in that direction, at that fare, which is
    # the one leg whose failure strands the traveller between two hotels. Both fields below are
    # already required by the renderer, so this costs nothing to read.
    bases = {str(_obj(d).get("base_location") or "").strip() for d in _seq(plan.get("days"))} - {""}
    stays = {str(_obj(a).get("stay_group_id") or "").strip()
             for a in _seq(_obj(plan.get("booking_options")).get("accommodations"))} - {""}
    if len(bases) > 1 or len(stays) > 1:
        disqualifiers.append(
            f"{max(len(bases), len(stays))} bases/stay groups (the light tier is single-city)")

    if not isinstance(plan.get("days"), list) or not plan.get("days"):
        disqualifiers.append("no days (length unexamined)")
    elif len(_seq(plan.get("days"))) > 4:
        disqualifiers.append(f"{len(_seq(plan.get('days')))} days")

    if disqualifiers:
        return set(REQUIRED_DOMAINS), (
            "This plan needs the full pass because it carries " + ", ".join(disqualifiers)
            + ". A missing domain is a gap nobody can see.")
    return set(LIGHT_TIER_DOMAINS), (
        "This plan qualifies for the light tier (short, single-city, no flight, no entry question, "
        "no severe allergy or walking cap), so only sights_and_hours is required among the truth "
        "domains -- but both audits are still mandatory and cost no network.")
VERDICTS = {"confirmed", "wrong", "misleading", "unverifiable"}
FINDING_SEVERITIES = ("critical", "major", "minor")


def _open_finding_problem(finding: dict) -> str | None:
    """Why a wrong or misleading finding is still open, or None when it is properly closed.

    Mirrors replan_context.must_reverify, which learned this first: a bare `true` is the same
    claim as an unresolved entry, made harder to see. Measured 2026-09-24 against v2.7.0:
    `resolved: true` with no resolution, and `resolved: "yes"`, both made a wrong finding vanish,
    and with it the page's reason to carry a banner. The five legacy reports in the author's
    workspace write a resolution on every one of their 81 closed findings, so this asks for
    nothing a real report did not already do.
    """
    resolved = finding.get("resolved")
    if resolved is not True:
        return "unresolved" if resolved in (None, False) else \
            f"resolved is {_short(resolved)}, not the JSON literal true"
    resolution = finding.get("resolution")
    if not isinstance(resolution, str) or not resolution.strip():
        return ("marked resolved with no resolution -- name the change that fixed it, or that "
                "the traveller accepted it")
    if any(marker in resolution for marker in PLACEHOLDER_MARKERS):
        return "its resolution still holds a placeholder"
    return None


def _finding_errors(finding: dict, where: str, errors: list[str], unresolved: list[str]) -> None:
    """Hold one wrong or misleading finding to the report's rules; other verdicts pass through.

    Severity is checked only here, where it means something. The report scaffold used to write
    `low / medium / high` against the spec's `critical / major / minor`, and the one real report
    built from it put `high` on confirmed findings -- where a severity ranks nothing.
    """
    if str(finding.get("verdict") or "").lower() not in {"wrong", "misleading"}:
        return
    if str(finding.get("severity") or "").lower() not in FINDING_SEVERITIES:
        errors.append(
            f"verification finding in {where} has severity {finding.get('severity')!r}; a wrong or "
            f"misleading finding is {', '.join(FINDING_SEVERITIES[:-1])} or "
            f"{FINDING_SEVERITIES[-1]}, which is what decides whether it can be accepted rather "
            f"than fixed.")
    problem = _open_finding_problem(finding)
    if problem:
        unresolved.append(f"[{where}] {finding.get('claim')} ({problem})")
# A dining card whose hours_status is one of these says a human went and looked. Anything else
# ("unverified", "closed_unknown", an unrecognised word) claims nothing, so nothing is demanded.
RESEARCHED_HOURS_STATUS = {"verified", "researched"}

# One step of a plan pointer: a key, then any number of [n] subscripts. Split on '.' first, so a
# key is anything that is not a dot or a bracket -- plan keys are identifiers, never dotted.
_POINTER_STEP = re.compile(r"^([^.\[\]]+)((?:\[\d+\])*)$")
_POINTER_INDEX = re.compile(r"\[(\d+)\]")


def resolve_pointer(plan: object, pointer: object) -> bool:
    """Does this pointer name a field the plan actually has? 'days[0].dining[1].venue_hours'.

    "Resolves" means the path EXISTS, null values included -- a verifier who opened a field and
    found it empty did real work, and demanding a non-null value would push reports toward citing
    only the fields that happen to be filled in.

    Never raises. A malformed string, an index into something that is not a list, an index past
    the end, a missing key: all are simply unresolvable, and the caller quotes the pointer back.
    A traceback here would take the whole gate down over one typo in one report, and a gate that
    crashes on bad input is a gate the next operator stops running.
    """
    if not isinstance(pointer, str):
        return False
    text = pointer.strip()
    if not text:
        return False
    current: object = plan
    for part in text.split("."):
        step = _POINTER_STEP.match(part)
        if not step:
            return False
        key, subscripts = step.group(1), step.group(2)
        if not isinstance(current, dict) or key not in current:
            return False
        current = current[key]
        for index in _POINTER_INDEX.findall(subscripts):
            if not isinstance(current, list):
                return False
            position = int(index)
            if position >= len(current):
                return False
            current = current[position]
    return True


def _example_pointer(plan: object) -> str:
    """A pointer drawn from the plan in front of the operator, for the error messages to quote.

    An example that resolves against their own file is worth several sentences of syntax: it shows
    the dotted keys, the [n] indexing and a field worth verifying in one line they can paste."""
    for candidate in ("days[0].dining[0].venue_hours",
                      "days[0].route.segments[0].duration_minutes",
                      "booking_options.accommodations[0].price_low",
                      "trip.start_date"):
        if resolve_pointer(plan, candidate):
            return candidate
    return "days[0].route.segments[0].duration_minutes"


def _short(value: object, limit: int = 60) -> str:
    text = repr(value)
    return text if len(text) <= limit else text[:limit - 3] + "..."


def _claims_pointer_errors(label: str, checked: object, plan: object) -> list[str]:
    """Validate one block's claims_checked: a non-empty list of pointers into the plan, no repeats.

    This was an integer until a run made the cost of it visible. A count is a promise the same run
    writes about itself: a model whose verifier subagent died -- which happens -- writes 1, the
    gate goes green, and the word "verified" lands on a page someone books a train from. A list of
    pointers costs what it claims, because a fabricated one has to resolve against the plan, and
    making ten of them resolve means opening the plan ten times.
    """
    example = _example_pointer(plan)
    if isinstance(checked, bool) or isinstance(checked, (int, float)):
        return [
            f"verification {label} reports claims_checked={_short(checked)}, a number. "
            f"claims_checked is now the LIST of plan pointers that block examined -- "
            f'"claims_checked": ["{example}", ...]. A count is a promise the run writes about '
            f"itself, so a block that writes 1 is indistinguishable from a block nobody ran. "
            f"Replace the number with the paths you actually opened."]
    if not isinstance(checked, list):
        return [
            f"verification {label} has claims_checked={_short(checked)}. It must be a list of "
            f"plan pointers naming what that block examined -- "
            f'"claims_checked": ["{example}", ...].']
    if not checked:
        # The one empty block with a known cause: a plan with no entry answer gives the entry
        # domain nothing to cite, and the scaffold writes it empty. Say what is missing.
        no_entry = (label == "domain 'entry'" and isinstance(plan, dict)
                    and not isinstance(plan.get("entry_context"), dict))
        return [
            f"verification {label} reports claims_checked: []. A block with no findings and no "
            f"pointers is indistinguishable from a block nobody ran. List the paths it examined, "
            f'e.g. "{example}".'
            + (" This plan has no entry_context, so there is nothing for it to cite: record the "
               "entry answer first -- a trip that stays in the travellers' own country states "
               "status not_required, with the page that says so -- and cite entry_context.status."
               if no_entry else "")]

    errors: list[str] = []
    seen: set[str] = set()
    repeated: set[str] = set()
    for entry in checked:
        if not isinstance(entry, str) or not entry.strip():
            errors.append(
                f"verification {label} has a claims_checked entry that is not a pointer string: "
                f'{_short(entry)}. Every entry names one field of the plan, e.g. "{example}".')
            continue
        text = entry.strip()
        if text in seen:
            # One finding per repeated pointer, not one per repeat. A list carrying the same path
            # three times is a single defect, and printing it twice reads as two -- padding the
            # gate's own output is exactly the inflation this rule exists to refuse.
            if text not in repeated:
                repeated.add(text)
                errors.append(
                    f"verification {label} lists the pointer {text!r} twice. Repeating a path "
                    f"inflates the apparent coverage without examining anything new; list each "
                    f"field once.")
            continue
        seen.add(text)
        # Reported one pointer at a time on purpose: a report can carry dozens, and "a pointer
        # failed" leaves the author diffing the list by eye to find which.
        if plan is not None and not resolve_pointer(plan, text):
            errors.append(
                f"verification {label} lists the pointer {text!r}, which does not resolve against "
                f"this plan -- no such key, or an index past the end of a list. Pointers are "
                f'dotted keys with [n] indexing, e.g. "{example}". Cite the field you really '
                f"opened; a list nobody can follow back to the plan is the count it replaced.")
    return errors


def _hours_coverage_errors(domains: list[dict], plan: object) -> list[str]:
    """The one coverage rule: sights_and_hours must cite every dining card that claims research.

    Scoped this narrowly because this is exactly where the shipped defect lived. A restaurant card
    declared its hours researched while they were wrong by 90 minutes at the front and an hour at
    the back, and the meal sat on the venue's rest day -- and the report's sights_and_hours block
    was clean and counted its claims in the double digits. Nothing tied the count to the cards.
    Naming the card is what turns "we checked the hours" into a lookup someone had to perform.

    No second coverage rule belongs here. Widening it would demand pointers for fields nobody
    agreed to check, and a gate that fires on honest work is a gate the next author deletes.
    """
    if not isinstance(plan, dict):
        return []
    blocks = [d for d in domains if str(d.get("domain")) == "sights_and_hours"]
    if not blocks:
        return []  # the missing-domain error already names this gap; saying it twice is noise
    listed = [b.get("claims_checked") for b in blocks]
    if not any(isinstance(c, list) for c in listed):
        return []  # the shape is already a finding; stacking coverage on top of it just repeats it
    # Read every sights_and_hours block, not just the first. Nothing rejects a report that carries
    # a domain twice -- the required-domain check compares sets -- so an operator who ran the hours
    # agent in two passes and appended both blocks would have the second one ignored, and this rule
    # would accuse a card that was in fact cited. One false accusation is what teaches an author to
    # stop reading a gate, and this gate has exactly one coverage rule to spend that credit on.
    pointers = [p.strip() for c in listed if isinstance(c, list) for p in c if isinstance(p, str)]

    errors: list[str] = []
    for day_index, raw_day in enumerate(_seq(plan.get("days"))):
        day = _obj(raw_day)
        for card_index, raw_card in enumerate(_seq(day.get("dining"))):
            card = _obj(raw_card)
            status = str(card.get("hours_status") or "").strip().lower()
            if status not in RESEARCHED_HOURS_STATUS:
                continue
            prefix = f"days[{day_index}].dining[{card_index}]"
            if any(p == prefix or p.startswith(prefix + ".") for p in pointers):
                continue
            errors.append(
                f"verification domain 'sights_and_hours' cites nothing under {prefix} -- day "
                f"{day.get('number')}'s '{card.get('venue_name')}' card, whose hours_status is "
                f"'{status}'. Either add the pointer that block opened, e.g. "
                f'"{prefix}.venue_hours", or set hours_status="unverified" to say plainly that '
                f"nobody checked. A card that claims its hours were researched while no verifier "
                f"touched it is how a meal gets booked at a venue closed that day.")
    return errors


@cites
def _walk_strings(node: object, path: str = "") -> list[tuple[str, str]]:
    """Every string in the report with the path it sits at, so a refusal can name the entry."""
    found: list[tuple[str, str]] = []
    if isinstance(node, dict):
        for key, value in node.items():
            found.extend(_walk_strings(value, f"{path}.{key}" if path else str(key)))
    elif isinstance(node, list):
        for index, value in enumerate(node):
            found.extend(_walk_strings(value, f"{path}[{index}]"))
    elif isinstance(node, str):
        found.append((path or "report", node))
    return found


def check_verification(report: dict, errors: list[str], notes: list[str],
                       plan: dict | None = None, plan_path: str | None = None,
                       report_path: str | None = None, receipt_from: str | None = None,
                       also_binds: tuple[str, ...] = ()) -> None:
    """The report is written by the same run it vouches for, so treat it as an interested
    witness. These checks make the cheap forgeries fail; see the limitation note below for the
    one that cannot be automated."""
    report = _obj(report)

    # An unfilled report is not a report, and nothing was refusing one. `new_plan_skeleton.py` has
    # always marked what it cannot know with `TODO:` and the page gate has always refused to ship a
    # plan still carrying one -- the verification report, which is the EVIDENCE document, had no
    # such rule. Anyone could hand in a shell of placeholder text and this function would grade it
    # on its dates and its pointers and pass it. That matters more here than anywhere else in the
    # skill: a plan with a TODO in it looks unfinished, while a report with a TODO in it looks like
    # somebody checked.
    _placeholders = sorted({
        f"{where}: {_short(value)}"
        for where, value in _walk_strings(report)
        if value.strip().upper().startswith("TODO")})
    if _placeholders:
        errors.append(
            "verification report still carries placeholder text at "
            + "; ".join(_placeholders[:4])
            + (f" (and {len(_placeholders) - 4} more)" if len(_placeholders) > 4 else "")
            + ". A report is the evidence for every 'verified' claim on the delivered page, so an "
            "unfilled one is worse than none: the page renders without its banner and the "
            "traveller reads an authority that nobody earned. Fill each entry with what was "
            "actually checked, or delete the block and let the tier gate report the gap.")

    checked_at = str(report.get("checked_at") or "")
    if not re.match(r"^\d{4}-\d{2}-\d{2}$", checked_at[:10]) or len(checked_at) < 10:
        errors.append("verification report needs an ISO checked_at date.")
    else:
        # A report older than the plan it certifies cannot have seen the plan -- unless the plan
        # carries the receipt of this very report. Then the receipt says, section by section,
        # which content the report saw, and every section that moved since needs a recheck dated
        # after it (below): a stronger test than one date. Without this exception an author who
        # bumped generated_at along with a covered edit had the valid recheck refused.
        generated = str(_obj(plan).get("generated_at") or "")[:10] if plan else ""
        bound_receipt = _obj(_obj(plan).get("verification_receipt")) if plan else {}
        bound = str(bound_receipt.get("report_checked_at") or "") == checked_at
        if (not bound and re.match(r"^\d{4}-\d{2}-\d{2}$", generated)
                and checked_at[:10] < generated):
            errors.append(
                f"verification report is dated {checked_at[:10]}, before the plan's generated_at "
                f"{generated}. It cannot have checked this plan.")
        # And the other side of the same window, which was open: only the lower bound was
        # checked, so a report stamped years ahead certified a plan happily. It matters because
        # checked_at is the field a reader uses to judge how stale a fare or an opening time is,
        # and a date in the future reads as "checked more recently than possible" -- the one
        # direction that makes stale research look fresh.
        if checked_at[:10] > dt.date.today().isoformat():
            errors.append(
                f"verification report is dated {checked_at[:10]}, which is in the future. "
                f"checked_at records when the facts were confirmed, and a reader judges "
                f"staleness by it.")

    # Bind the report to the plan, so one report cannot silently certify every trip. Besides its
    # own name, a report binds the delivered copy a save names for it (also_binds) and the plan it
    # sits beside as that plan's recorded report: the save puts it there, and a report written for
    # `plan.json` and delivered beside <start>-<slug>.json refused to check or save that copy.
    if plan_path:
        claimed = str(report.get("plan") or "")
        names = {Path(str(plan_path)).name} | {Path(str(name)).name for name in also_binds if name}
        own = _obj(plan).get("verification_report") if plan else None
        beside = bool(report_path and str(plan_path) != "-" and isinstance(own, str) and own.strip()
                      and Path(str(report_path)).expanduser().resolve()
                      == Path(str(plan_path)).expanduser().resolve().with_name(Path(own).name))
        if not claimed:
            errors.append(
                "verification report has no 'plan' field naming what it verified. Without it the "
                "same report certifies any plan it is handed.")
        elif Path(claimed).name not in names and not beside:
            errors.append(
                f"verification report says it verified '{claimed}' but was supplied for "
                f"'{Path(plan_path).name}'.")

    domains = [_obj(d) for d in _seq(report.get("domains"))]
    # A block with no name key used to fold into the set as the string "None" and be reported as
    # a domain "not part of the protocol: None" -- which names no field, suggests deleting
    # something, and sends the author looking for a domain they never wrote. The key was simply
    # absent. Say that instead; a message the reader cannot act on is a failed check even when
    # the exit code is right.
    unnamed = sum(1 for d in domains if not str(d.get("domain") or "").strip())
    if unnamed:
        errors.append(
            f"{unnamed} verification block(s) under 'domains' have no 'domain' key naming which "
            f"of {', '.join(sorted(REQUIRED_DOMAINS))} they cover. The name is what binds a block "
            f"to the protocol, so an unnamed block counts as a missing domain.")
    covered = {str(d.get("domain")) for d in domains if str(d.get("domain") or "").strip()}
    required, tier_reason = required_domains_for(plan)
    missing = required - covered
    if missing:
        errors.append(
            "verification report is missing required domains: " + ", ".join(sorted(missing))
            + f". {tier_reason}")
    unknown = covered - REQUIRED_DOMAINS
    if unknown:
        errors.append(
            "verification report contains domains that are not part of the protocol: "
            + ", ".join(sorted(unknown)) + ".")

    # An all-empty report is indistinguishable from one where nothing ran, unless each domain
    # states what it actually examined -- by pointer, so the claim can be followed back to a field.
    for domain in domains:
        name = domain.get("domain")
        if name not in REQUIRED_DOMAINS:
            continue
        errors.extend(_claims_pointer_errors(f"domain '{name}'", domain.get("claims_checked"), plan))
    errors.extend(_hours_coverage_errors(domains, plan))

    unresolved = []
    for domain in domains:
        for finding in [_obj(f) for f in _seq(domain.get("findings"))]:
            verdict = str(finding.get("verdict") or "").lower()
            if verdict not in VERDICTS:
                errors.append(
                    f"verification finding in '{domain.get('domain')}' has invalid verdict "
                    f"'{verdict}'.")
                continue
            _finding_errors(finding, str(domain.get("domain")), errors, unresolved)
    # The two network-free auditors carry the same weight as a domain and are checked the same
    # way. They are separate from `domains` because the five domains are truth checks against the
    # outside world and these two are checks of the plan against itself -- but keeping them out of
    # the artifact entirely, which is what this gate used to do, was worse: references/
    # verification.md tells the operator to run seven agents, the schema accepted five, and the
    # cheapest way past the failure was to delete the two extra blocks. In the run that prompted
    # this, those two produced 27 of 55 findings and 5 of the 6 criticals.
    audits = [_obj(a) for a in _seq(report.get("audits"))]
    unnamed_audits = sum(1 for a in audits if not str(a.get("audit") or "").strip())
    if unnamed_audits:
        errors.append(
            f"{unnamed_audits} verification block(s) under 'audits' have no 'audit' key naming "
            f"which of {', '.join(sorted(REQUIRED_AUDITS))} they cover.")
    audited = {str(a.get("audit")) for a in audits if str(a.get("audit") or "").strip()}
    if missing_audits := REQUIRED_AUDITS - audited:
        errors.append(
            "verification report is missing required audits: " + ", ".join(sorted(missing_audits))
            + ". Both run without network and cost little; a missing one is an invisible gap.")
    if unknown_audits := audited - REQUIRED_AUDITS:
        errors.append(
            "verification report contains audits that are not part of the protocol: "
            + ", ".join(sorted(unknown_audits)) + ".")
    for audit in audits:
        name = audit.get("audit")
        if name not in REQUIRED_AUDITS:
            continue
        errors.extend(_claims_pointer_errors(f"audit '{name}'", audit.get("claims_checked"), plan))
        for finding in [_obj(f) for f in _seq(audit.get("findings"))]:
            verdict = str(finding.get("verdict") or "").lower()
            if verdict not in VERDICTS:
                errors.append(f"verification finding in audit '{name}' has invalid verdict '{verdict}'.")
                continue
            _finding_errors(finding, f"audit {name}", errors, unresolved)

    if unresolved:
        errors.append(
            "verification found defects that were never resolved in the plan:\n    - "
            + "\n    - ".join(unresolved))
    # A report certifies the plan it is handed, and it cannot certify one whose entry answer is
    # still open, whatever its domains found -- that answer is the entry domain's whole subject.
    # A re-save of a plan already marked verified meets check_verified_plan_entry_answer first,
    # so the second saying of the same fact is skipped.
    open_answers = unverified_entry_answers(_obj(plan)) if plan else []
    if open_answers and not any("entry answer is still unverified" in e for e in errors):
        errors.append(cite(
            "entry.answer",
            f"this report cannot certify the plan while its entry answer is still unverified: "
            f"{', '.join(open_answers)}. Settle the entry answer in the plan -- it decides whether "
            f"the traveller boards -- or save with --unverified so the page says so."))
    # The receipt a verified save stamped binds this report to the content it covered. When the
    # plan has moved since, only the sections that moved need a recheck -- a day re-timed, one
    # hotel swapped -- and the report records each as an entry in `rechecks`. A receipt stamped
    # against a different report date belongs to an earlier verification and binds nothing here:
    # a fresh full report is a fresh verification.
    receipt = _obj(_obj(plan).get("verification_receipt")) if plan else {}
    if receipt and str(receipt.get("report_checked_at") or "") == checked_at:
        changed, removed = changed_sections(_obj(receipt.get("sections")), _obj(plan))
        recheck_unresolved: list[str] = []
        outdated: set[str] = set()
        rechecked = _valid_rechecks(report, _obj(plan), checked_at, errors, recheck_unresolved,
                                    outdated)
        if recheck_unresolved:
            errors.append("a recheck found defects that were never resolved in the plan:\n    - "
                          + "\n    - ".join(recheck_unresolved))
        uncovered = [section for section in changed if section not in rechecked]
        if uncovered:
            stale = sorted(set(uncovered) & outdated)
            # The command is printed whole when this knows both files, so it runs as printed.
            runnable = bool(plan_path and report_path and str(plan_path) != "-")
            errors.append(cite(
                "verification.rechecks",
                f"these parts of the plan changed after it was verified on {checked_at}, and the "
                f"report has no recheck of them as they are now: {', '.join(uncovered)}. "
                + (f"The report's recheck of {', '.join(stale)} checked an earlier version -- the "
                   f"part has changed again since. " if stale else "")
                + "Re-verify only those parts and append one `rechecks` entry each, or save with "
                  "--unverified so the page says so. Every other part keeps its verification. "
                # The command gets a line of its own, and a sentence after it for the citation
                # suffix to land on: appended to the command line, it became two more arguments.
                + ("The scaffold appends the entries to the report for you to fill:\n    NEXT: "
                   + recheck_command(plan_path, report_path, receipt_from)
                   + "\n    It then prints the save that finishes the recheck."
                   if runnable else
                   "python scripts/new_verification_report.py --recheck --from-plan <plan.json> "
                   "--report <report.json> --out <report.json> writes them for you to fill.")))
        if removed:
            notes.append(f"note: removed since verification (nothing to recheck): "
                         f"{', '.join(removed)}")
    cited = {p.strip() for block in domains + audits for p in _seq(block.get("claims_checked"))
             if isinstance(p, str) and p.strip()}
    notes.append(
        f"verification covered {len(covered)} domains and {len(audited & REQUIRED_AUDITS)} audits, "
        f"cited {len(cited)} distinct plan pointers, checked {checked_at}.")
    # KNOWN LIMIT, stated rather than hidden: nothing here can prove a finding marked resolved
    # actually changed the plan, and a pointer that resolves proves the field exists, not that
    # anyone read it. Code cannot diff an edit it never saw. That one relies on the
    # resolution string a reader can check by eye.


def _valid_rechecks(report: dict, plan: dict, checked_at: str, errors: list[str],
                    unresolved: list[str], outdated: set[str] | None = None) -> dict[str, dict]:
    """Each recheck the report carries, validated; returns {section: entry} for the sound ones.

    A recheck is held to what a verification block is held to, scoped to one section: it says
    when and why, it cites pointers that resolve and that all fall inside the section it claims,
    and its findings follow the same closing rule. A recheck citing another section's fields is
    not a recheck of this one.

    It also covers only the content it checked. Each entry carries the `section_digest` of the part
    as it was rechecked (the scaffold writes it), and counts only while the part still has that
    digest. Without it, one recheck of a day covered every later edit of that day: a second change
    re-saved as verified, and the page said the day had been re-checked. An entry whose part has
    moved on is history -- skipped, not validated against content it never saw, and named in
    `outdated` so the refusal can say why the report's recheck no longer counts.
    """
    kept: dict[str, dict] = {}
    today = dt.date.today().isoformat()
    for position, raw in enumerate(_seq(report.get("rechecks"))):
        entry = _obj(raw)
        section = str(entry.get("section") or "").strip()
        when = str(entry.get("checked_at") or "")
        where = f"verification recheck {position} ({section or 'no section'})"
        if not section:
            errors.append(f"{where} names no section.")
            continue
        if not re.match(r"^\d{4}-\d{2}-\d{2}", when):
            errors.append(f"{where} needs an ISO checked_at date.")
            continue
        if when[:10] < checked_at[:10]:
            errors.append(f"{where} is dated {when[:10]}, before the report it amends "
                          f"({checked_at[:10]}).")
            continue
        if when[:10] > today:
            errors.append(f"{where} is dated {when[:10]}, which is in the future.")
            continue
        reason = entry.get("reason")
        if not isinstance(reason, str) or not reason.strip():
            errors.append(f"{where} gives no reason -- say what changed and why it was rechecked.")
            continue
        digest = entry.get("section_digest")
        if not isinstance(digest, str) or not digest.strip():
            errors.append(f"{where} carries no section_digest, so nothing says which version of the "
                          f"part it checked. Write rechecks with python "
                          f"scripts/new_verification_report.py --recheck, which records it.")
            continue
        if not digest_is_current(plan, section, digest):
            if outdated is not None:
                outdated.add(section)
            continue
        claims = [c for c in _seq(entry.get("claims_checked")) if isinstance(c, str) and c.strip()]
        if not claims:
            errors.append(f"{where} checked nothing: claims_checked is empty.")
            continue
        broken = [c for c in claims if not resolve_pointer(plan, c)]
        if broken:
            errors.append(f"{where}: claims_checked pointer(s) do not resolve against the plan: "
                          f"{', '.join(broken[:5])}.")
            continue
        outside = [c for c in claims if section_of_pointer(plan, c) != section]
        if outside:
            errors.append(f"{where}: claims_checked points outside {section}: "
                          f"{', '.join(outside[:5])}.")
            continue
        for finding in [_obj(f) for f in _seq(entry.get("findings"))]:
            verdict = str(finding.get("verdict") or "").lower()
            if verdict not in VERDICTS:
                errors.append(f"{where} has a finding with invalid verdict '{verdict}'.")
                continue
            _finding_errors(finding, where, errors, unresolved)
        kept[section] = entry
    return kept


PLACEHOLDER_MARKERS = ("TODO:", "example.invalid")


def _unfilled(*values: object) -> bool:
    """Is this still the skeleton's placeholder rather than an answer?

    Content rules must not run on a card nobody has filled in yet, because the error they
    produce describes a problem that does not exist. The skeleton writes rating_value 0, and
    the floor rule read that as "you are recommending a venue rated 0/5. Replace it" -- sending
    an author to hunt for a badly-reviewed restaurant that was never chosen. A fresh four-day
    skeleton produced 38 errors that way, most of them about values nobody had entered.

    Saying "not filled in" once per card is both kinder and shorter: validate_trip_html.py
    already refuses to ship a TODO, so nothing is lost by staying quiet here.
    """
    return any(marker in str(v) for v in values if v is not None for marker in PLACEHOLDER_MARKERS)


_BRACKETED = re.compile(r"[（(\[【][^）)\]】]*[）)\]】]")


def _fold(text: str) -> str:
    """Case-folded, punctuation-free, script-agnostic form for substring comparison.

    Twice written as an allow-list and twice wrong. The first version tokenised on a Latin
    character class, so '东京银座三井花园酒店' produced nothing and the property-scoping rule
    skipped every CJK market. The second added kana, CJK and hangul to the allow-list and
    silently exempted 'Кафе Пушкинъ', 'Ταβέρνα', 'ร้านอาหาร', 'مطعم', 'מלון' and 'होटल' instead:
    an empty key makes the caller's `if key and ...` guard false, so the card passes with no
    error and no note.

    The lesson is the shape, not the script list. Enumerating what to keep means the rule
    protects the alphabets whoever wrote it happened to think of, and goes quiet everywhere
    else -- quiet in the same way the original bug was quiet. So keep whatever Unicode calls a
    letter or a digit and drop the rest; str.isalnum() knows every script, including the ones
    added after this line was written.
    """
    return "".join(ch for ch in (text or "").casefold() if ch.isalnum())


def _property_key(name: str) -> str:
    """The part of a property name a search URL should carry, minus any bracketed gloss.

    'Hotel Cristina by Tigotan Las Palmas（仅限 16 岁以上）' is searched as the hotel; the
    parenthetical is the plan's own annotation and never appears in the provider's URL.
    """
    return _fold(_BRACKETED.sub("", name or ""))


def _prefill_pattern(form: str, *, date: bool = False) -> str:
    """The boundary a prefilled value must have inside one discrete part of a search URL.

    A number may sit against a letter (`1adults`) but never against another digit, so the `4` in
    `14:30` or `2026-10-14` is not a party of four -- the loose match used to find exactly that and
    call it "free text". A code like `AMS` must not run into more letters. A date may run straight
    into its own time (`2026-10-17T08:00:00`): that is ISO 8601, still one field, and refusing it
    as free text is what a real Trainline URL got.
    """
    if form.isdigit():
        return r"(?<![0-9])" + re.escape(form) + r"(?![0-9])"
    tail = r"(?:(?![0-9a-z])|t\d)" if date else r"(?![0-9a-z])"
    return r"(?<![0-9a-z])" + re.escape(form) + tail


_ADULT_KEY = re.compile(r"adult", re.I)
_AGE_LIST_KEYS = {"childrenv2"}
_CHILD_KEY = re.compile(r"child|kid|infant|youth", re.I)


def _party_sizes_in_url(url: str) -> set[int]:
    """The party a search URL states as adults plus children, however the provider spells it.

    No provider states the total: Booking writes group_adults=2&group_children=2 (and one age=
    per child), Airbnb adults=2&children=2, Expedia children=1_7,1_10, Skyscanner
    childrenv2=7|10, KAYAK /2adults/children-7-10. Demanding the total as one value meant a family
    could never declare its party prefilled, and the only URL that passed searched for four adults,
    which hides the family rooms it was booking for.
    """
    parsed = urllib.parse.urlparse(url)
    query = urllib.parse.parse_qs(parsed.query)
    # One total per parameter family. A Booking link copied from the results states the party
    # twice, group_* and req_*; adding every adult and child key together read a family of four as
    # eight -- and "2 adults" stated twice as a party of four. The family is what precedes the word.
    families: dict[str, list[int]] = {}

    def count(value: str) -> int | None:
        parts = [part.strip() for part in re.split(r"[,;|]", value) if part.strip()]
        # Expedia lists one figure per room (adults=2,2): the party is their sum.
        return sum(int(part) for part in parts) if parts and all(p.isdigit() for p in parts) else None

    for key, values in query.items():
        if adult := _ADULT_KEY.search(key):
            tally = families.setdefault(key[:adult.start()].casefold(), [0, 0])
            tally[0] += sum(n for n in (count(v) for v in values) if n is not None)
    child_keys = [k for k in query if _CHILD_KEY.search(k)]
    # Within one family, count keys add up (children=1&infants=1 is two people) while an age list
    # restates the children the count already gave: Agoda writes children=2&childages=7,10, and
    # adding both read a family of four as six. The family's children are the larger of the two.
    # Age lists kept per room (childages1, childages2) are different children, so they add up; and
    # Skyscanner's childrenv2 is an age list even when it holds one age.
    counted: dict[str, int] = {}
    aged: dict[str, int] = {}
    for key in child_keys:
        family = key[:_CHILD_KEY.search(key).start()].casefold()
        values = query[key]
        entries = 0
        ages = "age" in key.casefold() or key.casefold() in _AGE_LIST_KEYS
        for value in values:
            if value.isdigit() and len(values) == 1 and not ages:
                entries += int(value)
            else:
                entries += len([part for part in re.split(r"[|,;]", value) if part.strip()])
        if ages:
            aged[family] = aged.get(family, 0) + entries
        else:
            counted[family] = counted.get(family, 0) + entries
    for family in set(counted) | set(aged):
        families.setdefault(family, [0, 0])[1] += max(counted.get(family, 0), aged.get(family, 0))
    if not child_keys:
        for tally in families.values():
            tally[1] += len(query.get("age", []))
    path = families.setdefault("/path/", [0, 0])
    for segment in (urllib.parse.unquote(s) for s in parsed.path.split("/") if s):
        if match := re.fullmatch(r"(\d+)adults?", segment, re.I):
            path[0] += int(match.group(1))
        if match := re.fullmatch(r"children((?:-\d{1,2})+)", segment, re.I):
            path[1] += len(match.group(1).strip("-").split("-"))
    # Families that differ only by a number are rooms of one party (Hilton's room1NumAdults and
    # room2NumAdults), so they are one total; group_* and req_* stay two statements of one party.
    rooms: dict[str, list[int]] = {}
    for family, (adults, children) in families.items():
        tally = rooms.setdefault(re.sub(r"\d+", "#", family), [0, 0])
        tally[0] += adults
        tally[1] += children
    return {adults + children for adults, children in rooms.values() if adults}


def prefill_date_forms(value: str) -> list[str]:
    """The spellings a search URL may use for one date (Skyscanner 270108, KAYAK 2027-01-08, ...)."""
    try:
        d = dt.date.fromisoformat(str(value)[:10])
    except Exception:  # noqa: BLE001 - a malformed date is reported by the date checks
        return []
    return [d.isoformat(), d.strftime("%Y%m%d"), d.strftime("%y%m%d"),
            d.strftime("%d-%m-%Y"), d.strftime("%d/%m/%Y"), d.strftime("%m/%d/%Y"),
            d.strftime("%d.%m.%Y")]


def url_discrete_parts(url: str) -> set[str]:
    parsed = urllib.parse.urlparse(urllib.parse.unquote_plus(url))
    parts = {p.casefold() for p in parsed.path.split("/") if p}
    for values in urllib.parse.parse_qs(parsed.query).values():
        for value in values:
            # A value with whitespace in it is a search box someone typed a sentence into.
            # Its contents are not prefilled fields; they are one field holding prose.
            if value and not re.search(r"\s", value):
                parts.add(value.casefold())
    return parts


def url_whole_values(url: str) -> set[str]:
    """Every path segment and every whole query value, folded -- spaces allowed.

    The whitespace rule above keeps a sentence typed into a search box from counting as
    fields. A whole value that EQUALS the declared field is not a sentence, though: SBB writes
    `von=Zürich HB`, one station, one field. Excluding it meant a multi-word station could
    never be carried at all.
    """
    parsed = urllib.parse.urlparse(url)
    values = {_fold(urllib.parse.unquote_plus(segment)) for segment in parsed.path.split("/")
              if segment}
    for found in urllib.parse.parse_qs(parsed.query).values():
        values.update(_fold(value) for value in found if value)
    return values - {""}


def undelivered_prefill_fields(url: str, declared: list, wanted: dict,
                               ids: dict | None = None) -> list[tuple[str, object, bool]]:
    """Each declared field this URL does not carry as a discrete part: (field, value, loose).

    Lifted out of check_booking_identity so kiwi_flights.py can ask the same rule which fields its
    search URL really carries instead of re-implementing it. `loose` is True when the value occurs
    only inside free text -- a search box with a sentence in it rather than a filled-in field.
    """
    if not url or not declared:
        return []
    parts = url_discrete_parts(url)
    whole = url_whole_values(url)
    haystack = urllib.parse.unquote_plus(url).casefold()
    missing: list[tuple[str, object, bool]] = []
    for field in [str(d) for d in declared]:
        value = wanted.get(field)
        if value in (None, ""):
            continue
        is_date = field.endswith("_date") or field in ("check_in", "check_out")
        forms = [str(value).casefold()]
        if is_date:
            forms = [f.casefold() for f in prefill_date_forms(str(value))] or forms
        # Inside a discrete part, not equal to it: a provider may pack two fields into one
        # segment (KAYAK writes the pair as `AMS-HKG`) or decorate one (`1adults`), and both
        # are still structured. _prefill_pattern holds the boundaries.
        if any(re.search(_prefill_pattern(f, date=is_date), part) for f in forms for part in parts):
            continue
        if field in ("guests", "travellers") and isinstance(value, int) \
                and not isinstance(value, bool) and value in _party_sizes_in_url(url):
            continue
        if field in ("origin", "destination"):
            if _fold(str(value)) in whole:
                continue
            # A provider that keys stations by its own id (Trainline's urn:trainline:...)
            # never names them; the card declares the id it saw, and the id is what is asked.
            station_id = (ids or {}).get(field)
            if isinstance(station_id, str) and station_id.strip() and _fold(station_id) in whole:
                continue
        loose = any(re.search(_prefill_pattern(f, date=is_date), haystack) for f in forms)
        missing.append((field, value, loose))
    return missing


@cites
def check_booking_identity(plan: dict, errors: list[str], notes: list[str]) -> None:
    """A comparison link that opens a city is not a link to the thing being compared.

    Two hotels once shipped with byte-identical Booking.com URLs -- a search for the city, with
    the trip's dates -- and the cards passed every gate. The cost was not tidiness. Because no
    button ever opened either property on the platform that actually sells it, nobody saw that
    one of them cost EUR 1,256 for the week (over the traveller's whole cap, before flights) and
    the other had no availability on those dates at all. The missing link was the reason two
    unbookable recommendations survived to delivery.

    So a comparison search has to be scoped to the product: its URL must carry a token of the
    property's own name, or a property/hotel id. Hand-built property paths are still forbidden
    elsewhere in the skill for a separate and equally measured reason -- Booking's bare
    /hotel/<cc>/<slug>.html answers with an error page unless it carries the session parameters
    this skill will not embed -- which is exactly why the property-scoped *search* is the form
    that works: it is stable, shareable, tracker-free, and lands on the one property.
    """
    stays: dict[str, list[tuple[str, str]]] = {}
    low: list[str] = []
    thin: list[str] = []
    for option in [_obj(o) for o in _seq(_obj(plan.get("booking_options")).get("accommodations"))]:
        name = str(option.get("property_name") or option.get("id") or "?")
        if _unfilled(name, option.get("review_url")):
            continue      # already reported once as an unfilled card
        key = _property_key(name)
        searches = [_obj(s) for s in _seq(option.get("comparison_searches"))]
        if not searches:
            errors.append(f"accommodation '{name}': no comparison_searches. Give the traveller a "
                          f"way to open this exact property on a platform that sells it.")
            continue
        for search in searches:
            url = str(search.get("search_url") or "")
            stays.setdefault(str(option.get("stay_group_id") or ""), []).append((name, url))
            haystack = _fold(urllib.parse.unquote_plus(url))
            # dest_id / dest_type are Booking's *city* identifiers and were briefly on this
            # allow-list, which exempted the canonical city search -- the very URL the rule
            # exists to reject. Only identifiers that name one property may buy an exemption.
            if key and key not in haystack and not re.search(
                    r"(hotel_?id|property[_-]?id|hotelId|propertyId)=", url):
                errors.append(
                    f"accommodation '{name}': its comparison search URL is not scoped to this "
                    f"property -- the URL carries none of its name and no property id, so the "
                    f"button opens a list, not the thing the card is about. Search the property "
                    f"by name with the trip's dates and store the URL that resolves.")

    # Keyed on the whole plan rather than on stay_group_id, because the group label is written by
    # the same author as the URL: relabelling two hotels into different groups used to be enough
    # to let them share one link, which is the defect wearing a different hat.
    seen_urls: dict[str, str] = {}
    for group, entries in stays.items():
        for name, url in entries:
            if url in seen_urls and seen_urls[url] != name:
                errors.append(
                    f"accommodation '{seen_urls[url]}' and '{name}' share the same comparison "
                    f"URL. Two options that open the same page are one option shown twice, "
                    f"whichever stay groups they are filed under.")
            seen_urls.setdefault(url, name)

    # review_url is deliberately NOT held to the same name test. A property's own site is
    # addressed in its own market's script -- '东京銀座三井ガーデンホテル' lives at
    # gardenhotels.co.jp/ginza -- so demanding the property name inside that URL would fail
    # exactly the non-Latin markets the folding fix above was written to protect. The
    # comparison search is different: its query string is written here, so the name is in it
    # by construction, and that is where the property-scoping guarantee belongs.

    # The renderer labels direct_review_url "view the official direct-booking page", so a bare
    # host root under it promises a booking page and delivers a front door. Two flight cards
    # shipped pointing at transavia.com/ and tui.nl/ that way. An own-site link is allowed to
    # carry no dates -- many carriers cannot be deep-linked at all -- but it has to be a page
    # about this product rather than the company.
    for kind in ("flights", "ground_transport", "accommodations", "rental_cars"):
        for option in [_obj(o) for o in _seq(_obj(plan.get("booking_options")).get(kind))]:
            label = str(option.get("property_name") or option.get("provider")
                        or option.get("id") or "?")
            direct = str(option.get("direct_review_url") or "")
            if _unfilled(label, direct):
                continue
            if not direct:
                continue
            path = urllib.parse.urlparse(direct).path.strip("/")
            if not path:
                errors.append(
                    f"{kind} '{label}': direct_review_url is {direct!r}, a bare home page, but the "
                    f"button above it reads 'view the official direct-booking page'. Point it at "
                    f"the page for this route or property, or drop the field so no button claims "
                    f"more than it opens.")

    # A search button that does not carry the traveller's dates makes them type the trip in
    # again, which is the whole difference between a link and a lead. The plan declares
    # round_trip_prefilled_fields / prefilled_fields listing "outbound_date" and the rest, and
    # until now that list was a promise the same run wrote about itself: nothing compared it to
    # the URL sitting beside it. Providers encode dates differently -- Skyscanner writes 270108,
    # KAYAK writes 2027-01-08 -- so every common spelling counts as present.
    _date_forms = prefill_date_forms

    def _dates_in_url(url: str, dates: list[tuple[str, str]], where: str) -> None:
        if not url:
            return
        haystack = urllib.parse.unquote_plus(url)
        for label, value in dates:
            forms = _date_forms(value)
            if forms and not any(f in haystack for f in forms):
                errors.append(
                    f"{where}: the search URL does not carry the {label} ({value}), so it opens a "
                    f"blank search the traveller has to fill in again. Run the search on the "
                    f"provider with the trip's own dates and store the URL it produces.")

    options = _obj(plan.get("booking_options"))
    for kind in ("flights", "ground_transport"):
        for option in [_obj(o) for o in _seq(options.get(kind))]:
            label = str(option.get("provider") or option.get("id") or "?")
            if _unfilled(label, option.get("review_url"), option.get("round_trip_search_url")):
                continue
            _dates_in_url(str(option.get("round_trip_search_url") or ""),
                          [("outbound date", option.get("outbound_date")),
                           ("return date", option.get("return_date"))],
                          f"{kind} '{label}' round-trip search")
    for option in [_obj(o) for o in _seq(options.get("accommodations"))]:
        label = str(option.get("property_name") or option.get("id") or "?")
        if _unfilled(label, option.get("review_url")):
            continue
        for search in [_obj(s) for s in _seq(option.get("comparison_searches"))]:
            _dates_in_url(str(search.get("search_url") or ""),
                          [("check-in date", option.get("check_in")),
                           ("check-out date", option.get("check_out"))],
                          f"accommodation '{label}' comparison search")

    # The other half of the same promise, and it was missing. `_dates_in_url` above checks the two
    # DATES a search must carry; the plan also declares `round_trip_prefilled_fields` /
    # `prefilled_fields` naming origin, destination and travellers, and nothing compared those to
    # the URL at all -- they were an attestation, and an attestation records that a rule was
    # claimed, never that it was followed.
    #
    # Measured: a delivered plan carried
    # `https://www.google.com/travel/flights?q=Flights+from+AMS+to+HKG+on+2027-04-17+through+2027-04-22`
    # while declaring all five fields prefilled. It passed this gate with zero findings. The dates
    # were "in the URL" as literal text inside one free-text `q=` parameter, and origin,
    # destination and travellers were never looked for. The traveller opened the button and got a
    # search box, which is the exact failure the prefill rule exists to prevent, shipped under a
    # declaration that it had been prevented.
    #
    # So a value only counts when it is a DISCRETE part of the URL -- a path segment, or the whole
    # of a query value -- and never when it is buried in a value that reads as prose. That
    # distinction is what separates KAYAK's `/flights/AMS-HKG/2027-04-17/2027-04-22/1adults`,
    # where each field is its own segment, from a sentence typed into a search box. It is the same
    # rule this skill already applies to map endpoints: the string a button carries is a query,
    # not a caption.
    _discrete_parts = url_discrete_parts
    _whole_values = url_whole_values

    def _declared_fields_in_url(url: str, declared: list, wanted: dict, where: str,
                                ids: dict | None = None) -> None:
        for field, value, loose in undelivered_prefill_fields(url, declared, wanted, ids):
            errors.append(
                f"{where}: it declares {field!r} prefilled, but the URL "
                + (f"carries {value!r} only inside a free-text parameter, which is a search box "
                   f"with a sentence in it rather than a filled-in field."
                   if loose else
                   f"does not carry {value!r} at all.")
                + f" Run the search on the provider with the trip's own values and store the URL "
                  f"it produces, or drop {field!r} from the declaration so the page does not "
                  f"promise a button it cannot open.")

    travellers = _obj(plan.get("trip")).get("traveler_count")
    for kind in ("flights", "ground_transport"):
        for option in [_obj(o) for o in _seq(options.get(kind))]:
            label = str(option.get("provider") or option.get("id") or "?")
            if _unfilled(label, option.get("round_trip_search_url")):
                continue
            _declared_fields_in_url(
                str(option.get("round_trip_search_url") or ""),
                _seq(option.get("round_trip_prefilled_fields")),
                # A rail card names stations, not airports. Reading origin_airport here meant a rail
                # search's stations were never compared at all: remove both from the URL and every
                # gate passed.
                {"origin": option.get("origin_airport") or option.get("origin_station"),
                 "destination": option.get("destination_airport") or option.get("destination_station"),
                 "outbound_date": option.get("outbound_date"),
                 "return_date": option.get("return_date"),
                 "travellers": travellers},
                f"{kind} '{label}' round-trip search",
                # A flight card may name the provider's own place ids the same way: Kiwi keys its
                # search page by city slug (amsterdam-netherlands), never by the IATA code the card
                # carries, and the id the card declares is what is asked for in the URL.
                ids={"origin": option.get("origin_station_id") or option.get("origin_place_id"),
                     "destination": option.get("destination_station_id")
                     or option.get("destination_place_id")})
    for option in [_obj(o) for o in _seq(options.get("accommodations"))]:
        label = str(option.get("property_name") or option.get("id") or "?")
        if _unfilled(label, option.get("review_url")):
            continue
        for search in [_obj(s) for s in _seq(option.get("comparison_searches"))]:
            _declared_fields_in_url(
                str(search.get("search_url") or ""),
                _seq(search.get("prefilled_fields")),
                {"check_in": option.get("check_in"), "check_out": option.get("check_out"),
                 "guests": option.get("guest_count"), "rooms": option.get("room_count")},
                f"accommodation '{label}' comparison search")

    # A rental search declared its pickup and return prefilled and nothing ever read the URL: both
    # car links pointed at bare home pages, still declaring every field, and every gate passed.
    # Dates are compared -- as one discrete date, or as the separate day/month/year integers some
    # providers use. Locations are not: rental providers key a desk by their own location id, so
    # the place name never appears, and asking for it would refuse every honest link.
    def _date_carried_in_url(url: str, value: object) -> bool:
        forms = [f.casefold() for f in _date_forms(str(value or ""))]
        if not forms:
            return True                      # a malformed time is the time checks' to report
        if any(re.search(_prefill_pattern(f, date=True), part) for f in forms
               for part in _discrete_parts(url)):
            return True
        day = dt.date.fromisoformat(str(value)[:10])
        integers = {int(v) for vs in urllib.parse.parse_qs(urllib.parse.urlparse(url).query).values()
                    for v in vs if v.isdigit()}
        return {day.day, day.month, day.year} <= integers

    for option in [_obj(o) for o in _seq(options.get("rental_cars"))]:
        label = str(option.get("provider") or option.get("id") or "?")
        url = str(option.get("review_url") or "")
        declared = [str(d) for d in _seq(option.get("rental_search_prefilled_fields"))]
        if not url or not declared or _unfilled(label, url):
            continue
        parsed = urllib.parse.urlparse(url)
        if not parsed.path.strip("/") and not parsed.query:
            errors.append(
                f"rental car '{label}': it declares {', '.join(declared)} prefilled, but its search "
                f"link is the provider's bare home page, which carries none of them. Run the search "
                f"with the pickup and return and store the URL it produces.")
            continue
        for field in ("pickup_time", "dropoff_time"):
            if field in declared and not _date_carried_in_url(url, option.get(field)):
                errors.append(
                    f"rental car '{label}': it declares {field!r} prefilled, but the URL does not "
                    f"carry the date of {option.get(field)!r}. Run the search with the trip's own "
                    f"pickup and return and store the URL it produces, or drop {field!r} from the "
                    f"declaration.")

    # Two "competing" options that open the same page are one option shown twice. The rule was
    # written for hotels and the same defect shipped on flights: both candidates in a delivered
    # plan carried an identical round-trip search URL, so the comparison compared nothing.
    for kind in ("flights", "ground_transport", "accommodations", "rental_cars"):
        seen: dict[tuple[str, str], str] = {}
        for option in [_obj(o) for o in _seq(_obj(plan.get("booking_options")).get(kind))]:
            label = str(option.get("property_name") or option.get("provider")
                        or option.get("id") or "?")
            for field in ("review_url", "round_trip_search_url"):
                url = str(option.get(field) or "")
                if not url:
                    continue
                previous = seen.get((field, url))
                if previous and previous != label:
                    errors.append(
                        f"{kind}: '{previous}' and '{label}' share the same {field}. Two options "
                        f"that open the same page are one option shown twice.")
                seen.setdefault((field, url), label)

    # Hotels were judged on price and location and nothing else. The traveller asked for the
    # same standard as restaurants, and it had never existed: a plan could recommend a 6.1/10
    # property and every gate stayed green. Booking and Agoda publish out of 10, Google and
    # TripAdvisor out of 5, so the scale travels with the value or the number means nothing.
    for option in [_obj(o) for o in _seq(_obj(plan.get("booking_options")).get("accommodations"))]:
        name = str(option.get("property_name") or option.get("id") or "?")
        if _unfilled(name, option.get("guest_rating_source"), option.get("review_url")):
            errors.append(
                f"accommodation '{name}' is still the skeleton's placeholder. Fill it from the "
                f"property's page on the platform that sells it -- one visit yields the price, "
                f"the availability on these dates and the guest score together.")
            continue
        # A REVIEW SCORE CANNOT BE READ OFF A PRICE SEARCH, and citing one as if it could is how
        # a made-up number gets a source. Shipped, and caught by the traveller rather than by any
        # gate here: both hotels on a delivered plan carried `guest_rating_source: "Booking.com"`
        # with `guest_rating_url` set to the SAME dated Booking search the "compare prices" button
        # used. That page shows rooms and rates; it has never shown a review score. The figures
        # themselves were taken from a search-result summary that pooled several platforms -- a
        # cross-platform review COUNT ("2776 reviews across platforms") ended up paired with one
        # platform's SCORE, and the pairing was attributed to a site nobody had opened. The real
        # figures, read off the property's own detail page, were 9.1 from 105 reviews and 8.1 from
        # 101; the plan said 9.2 from 2776 and 7.9 from 2271.
        #
        # Checkable part: the citation may not be the availability search. A URL carrying check-in,
        # check-out or occupancy parameters is a price-and-availability query by construction, and
        # a citation byte-identical to the card's own comparison search is one nobody read a score
        # from. What stays uncheckable is whether the number is right -- which is exactly why the
        # link has to point somewhere a reader can go and see for themselves.
        rating_url = str(option.get("guest_rating_url") or "")
        if rating_url:
            searches = {str(_obj(x).get("search_url") or "")
                        for x in _seq(option.get("comparison_searches"))}
            searches.discard("")
            if rating_url in searches:
                errors.append(
                    f"accommodation '{name}': guest_rating_url is the same link as the price "
                    f"comparison search. A search page shows rooms and rates, never a review "
                    f"score, so nothing could have been read from it -- point it at the property's "
                    f"own page on the platform the score comes from.")
            elif re.search(r"[?&](checkin|checkout|check_in|check_out|group_adults|no_rooms|"
                           r"adults|nights)=", rating_url):
                errors.append(
                    f"accommodation '{name}': guest_rating_url carries date/occupancy parameters, "
                    f"so it is an availability search rather than the property's page. A review "
                    f"score is not shown on one; cite the page the score was actually read from.")
        # THE RECORD-ONCE RULE, ENFORCED. references/decision-and-research.md has said since it was
        # written that "every accommodation carries its guest score beside a price and an
        # availability that came off the same visit", and nothing read it -- so a card could claim
        # a VERIFIED score while its availability stayed `unknown`, which is self-contradictory:
        # the sellability of the dates is on the same page as the score. Either the page was never
        # opened, in which case the score is not verified, or it was opened and two of the three
        # fields were left behind.
        #
        # That combination is exactly what a delivered plan carried -- verified / unknown /
        # estimate -- while its scores had in fact been lifted from a multi-platform search
        # summary. tests/booking-ready-fixture.json carried it too, so the known-good example was
        # teaching it. This is the check the citation rules above do not reach: they prove the link
        # goes somewhere a score can be read, and this one asks whether anyone went.
        #
        # `unknown` stays available, because a platform really can refuse this machine -- but then
        # it is a fact about the run and the traveller has to see it, so it costs a sentence.
        #
        # Keyed on the SCORE, not on what the card says about it. The first version read
        # guest_rating_status, an optional field the author writes about their own card, so leaving
        # it blank passed the same score beside the same unknown availability (measured
        # 2026-09-24). A number on the card is the claim somebody read the page; only an explicit
        # "none" says nobody did.
        rating_status = str(option.get("guest_rating_status") or "").lower()
        claims_score = rating_status in ("verified", "researched") or (
            rating_status != "none" and _num(option.get("guest_rating_value")) > 0)
        if claims_score \
                and str(option.get("availability_status") or "").lower() == "unknown" \
                and not str(option.get("availability_unknown_reason") or "").strip():
            errors.append(
                f"accommodation '{name}': the card carries a guest score while availability is "
                f"'unknown' and nothing says why. Those two live on the same page, so one visit "
                f"answers both -- open the property for these dates and set availability, or write "
                f"availability_unknown_reason saying what stopped you. A score with no sellable "
                f"dates beside it is a recommendation the traveller cannot act on, and this is the "
                f"shape a score copied from a search summary takes.")
        status = str(option.get("guest_rating_status") or "").lower()
        if status == "none":
            if not str(option.get("guest_rating_absence_reason") or "").strip():
                errors.append(
                    f"accommodation '{name}': guest_rating_status is 'none' with no reason. A new "
                    f"property with no reviews yet can still be the right call -- say which.")
            if _num(option.get("guest_rating_value")) > 0:
                errors.append(
                    f"accommodation '{name}': guest_rating_status is 'none' while "
                    f"guest_rating_value is {_num(option.get('guest_rating_value')):g}. That pair "
                    f"is how a floor gets dodged rather than met.")
            continue
        # The URL and the date are the score's citation, held to what a dining card has always owed.
        # Optional, they were the way around the citation rule above: it runs only when a URL is
        # there to check, so leaving it out skipped the rule written for a score lifted from a
        # search summary.
        missing = [k for k in ("guest_rating_value", "guest_rating_scale", "guest_rating_count",
                               "guest_rating_source", "guest_rating_url", "guest_rating_checked_at")
                   if option.get(k) in (None, "")]
        if missing:
            errors.append(
                f"accommodation '{name}': missing {', '.join(missing)}. A place someone sleeps for "
                f"a week needs the same quality evidence as a place they eat one dinner at, and "
                f"the platform that sells it publishes one on the page you already opened to read "
                f"the price.")
            continue
        scale = _num(option.get("guest_rating_scale")) or 10
        if scale not in (5, 10):
            errors.append(f"accommodation '{name}': guest_rating_scale must be 5 or 10, got "
                          f"{scale:g}.")
            continue
        out_of_ten = _num(option.get("guest_rating_value")) * (10.0 / scale)
        count = _num(option.get("guest_rating_count"))
        if out_of_ten < 7.0 and not str(
                option.get("guest_rating_below_floor_reason") or "").strip():
            errors.append(
                f"accommodation '{name}': guest rating {_num(option.get('guest_rating_value')):g}"
                f"/{scale:g} ({out_of_ten:.1f}/10) is below the 7.0/10 floor. On Booking's own "
                f"published wording 7 is 'good' and 6 is 'pleasant', which is the polite end of a "
                f"scale where the complaints start -- pick another property, or write "
                f"guest_rating_below_floor_reason saying what makes this one worth a week "
                f"of nights. A field rather than prose, because this message used to point "
                f"at selection_rationale and no code ever read it.")
        elif out_of_ten < 8.0:
            low.append(f"accommodation '{name}' -- {out_of_ten:.1f}/10")
        if count and count < 50:
            thin.append(f"accommodation '{name}' -- only {count:g} reviews")

    # "Read the price off the platform page" is a process rule no code can watch. Its mechanical
    # shadow can be: if you opened the page far enough to read a current price, you saw whether
    # the dates were sellable. A card claiming a researched price while leaving availability
    # unknown is claiming a page it did not finish reading -- and the plan that prompted all of
    # this shipped a hotel that was sold out on exactly those dates, marked unknown.
    #
    # Every DATED search, not just hotels: a flight, a train or a car priced for these dates is read
    # off a page that also says whether they sell, and the rule stopped at the one kind it was
    # written for. A ticket price list is undated -- a museum's adult fare is the same every day and
    # says nothing about a day's availability -- so tickets are left out on purpose.
    for kind, name_key in (("accommodations", "property_name"), ("flights", "provider"),
                           ("ground_transport", "provider"), ("rental_cars", "provider")):
        for option in [_obj(o) for o in _seq(_obj(plan.get("booking_options")).get(kind))]:
            name = str(option.get(name_key) or option.get("id") or "?")
            if _unfilled(name, option.get("review_url")):
                continue
            if (str(option.get("price_status") or "").lower() == "researched_current"
                    and str(option.get("availability_status") or "").lower() == "unknown"):
                errors.append(
                    f"{kind} '{name}': price_status is 'researched_current' while "
                    f"availability_status is 'unknown'. The page that gave you today's price also "
                    f"said whether these dates are sellable -- record what it said, or mark the "
                    f"price an estimate to match what was actually read.")

    unknown = [str(o.get("property_name")) for o in
               [_obj(x) for x in _seq(_obj(plan.get("booking_options")).get("accommodations"))]
               if str(o.get("availability_status") or "").lower() == "unknown"]
    if low:
        notes.append("note: accommodation rated below 8.0/10 -- defensible, but say why in "
                     "selection_rationale:\n    - " + "\n    - ".join(low))
    if thin:
        notes.append("note: accommodation whose score rests on few reviews:\n    - "
                     + "\n    - ".join(thin))
    if unknown:
        notes.append("note: accommodation whose availability on the selling platform was never "
                     "checked -- one such card shipped sold out:\n    - " + "\n    - ".join(unknown))


@cites
def check_venue_quality(plan: dict, errors: list[str], notes: list[str]) -> None:
    """A recommendation with no quality signal is an assertion of taste, not a finding.

    The dining contract used to require venue, style, area, price, queue note, rationale, link
    and backup -- everything except whether the place is any good, or whether it exists. A
    measured run shipped a dinner at a venue that returns no listing on any platform, two
    lunches at restaurants that do not open until 20:00, and a farewell dinner priced at
    EUR 55-90 that actually bills EUR 100+. Every gate passed, because none of those facts had
    a field to live in.

    Two rules, and the second is the one that hurts:
      * every card carries a rating with its scale, count and source, or says plainly that it
        has none. A 4.8 from 12 reviews and a 4.3 from 2,000 are not the same claim, so the
        count is required alongside the value rather than optional beside it.
      * a card may not name a time window while admitting its hours are unverified. Scheduling
        a meal IS a claim that the venue is open then; 'unverified' beside '13:15-14:30' is that
        claim with the evidence removed, which reads to the traveller as researched and to the
        gate as compliant.
    """
    low: list[str] = []
    thin: list[str] = []
    for day in [_obj(d) for d in _seq(plan.get("days"))]:
        number = day.get("number")
        for card in [_obj(c) for c in _seq(day.get("dining"))]:
            # SKILL.md names venue_url as "the same defect in a second field" and nothing measured
            # it: a delivered plan searched the map provider for the phrase 酒店自助早餐（…）--
            # "hotel buffet breakfast" -- instead of a venue. A place lookup needs a NAME rather
            # than a coordinate, so the rule here is different from the route one: the query has
            # to be keyed on the venue this card is about. It cannot prove the name exists, which
            # is what the rating requirement and opening the page are for.
            venue = str(card.get("venue_name") or "")
            if _unfilled(venue, card.get("venue_url"), card.get("venue_hours"),
                         card.get("rating_source")):
                errors.append(
                    f"day {number}: the {card.get('meal') or 'meal'} card is still the skeleton's "
                    f"placeholder. Fill it from the venue's own page -- one visit yields the name, "
                    f"the hours, the rating and the link.")
                continue
            key = _property_key(venue)
            url = str(card.get("venue_url") or "")
            # A URL that addresses the venue by identifier is a STRONGER claim than one that
            # searches its name -- an Amap /place/B0… or a Google place_id resolves to exactly
            # one venue -- so an id buys the exemption the name test would otherwise deny it.
            identified = re.search(
                r"(/place/|place_id=|[?&]cid=|/maps/place/|ftid=)", url) is not None
            if key and url and not identified and key not in _fold(urllib.parse.unquote_plus(url)):
                errors.append(
                    f"day {number}: the venue link for '{venue}' searches something else -- the "
                    f"query in venue_url does not contain the venue's own name. A map link keyed "
                    f"on a description finds a phrase; only one keyed on the registered name "
                    f"finds the restaurant.")

        for index, card in enumerate([_obj(c) for c in _seq(day.get("dining"))]):
            if _unfilled(card.get("venue_name"), card.get("venue_url"),
                         card.get("venue_hours"), card.get("rating_source")):
                continue      # already reported once, above, as an unfilled card
            where = f"day {number} {card.get('meal') or 'meal'} ('{card.get('venue_name')}')"
            status = str(card.get("rating_status") or "").lower()
            value, count = card.get("rating_value"), card.get("rating_count")
            if status == "none":
                if not str(card.get("rating_absence_reason") or "").strip():
                    errors.append(
                        f"{where}: rating_status is 'none' but rating_absence_reason is empty. "
                        f"A venue with no public rating can still be the right call -- a market "
                        f"stall, a hotel breakfast -- but say which, so the gap reads as a "
                        f"decision rather than an omission.")
                if _num(card.get("rating_value")) > 0:
                    errors.append(
                        f"{where}: rating_status is 'none' while rating_value is "
                        f"{_num(card.get('rating_value')):g}. One object cannot both have a "
                        f"score and not have one, and that pair is exactly how the floor gets "
                        f"dodged -- flipping the status hides the number instead of replacing "
                        f"the venue.")
                continue
            missing = [k for k in ("rating_value", "rating_scale", "rating_count",
                                   "rating_source", "rating_url", "rating_checked_at")
                       if card.get(k) in (None, "")]
            if missing:
                errors.append(
                    f"{where}: missing {', '.join(missing)}. Every recommended venue needs a "
                    f"quality signal with its scale, its count and where it came from, or "
                    f"rating_status='none' with a reason. Without it nothing distinguishes a "
                    f"venue you checked from one a blog listed and no one ever opened.")
                continue
            scale = _num(card.get("rating_scale")) or 5
            if scale not in (5, 10):
                errors.append(f"{where}: rating_scale must be 5 or 10, got {scale:g}. "
                              f"TheFork and Booking publish out of 10 and Google out of 5, so a "
                              f"bare number is not comparable across sources.")
                continue
            out_of_five = _num(value) * (5.0 / scale)
            if out_of_five < 3.5 and not str(card.get("rating_below_floor_reason") or "").strip():
                errors.append(
                    f"{where}: rating is {_num(value):g}/{scale:g} ({out_of_five:.1f}/5), "
                    f"below the 3.5/5 floor. Replace it, or write rating_below_floor_reason "
                    f"saying what makes it worth the traveller's evening anyway -- the only "
                    f"place in town serving a dietary need, a legendary stall whose score is "
                    f"all queue complaints. A field rather than prose, because this message "
                    f"used to offer that escape and no code read it: an author who wrote the "
                    f"justification was rejected anyway, while one who flipped rating_status "
                    f"to 'none' walked straight through.")
            elif out_of_five < 4.0:
                low.append(f"{where} -- {out_of_five:.1f}/5")
            if _num(count) < 30:
                thin.append(f"{where} -- only {_num(count):g} reviews")

    for day in [_obj(d) for d in _seq(plan.get("days"))]:
        number = day.get("number")
        for card in [_obj(c) for c in _seq(day.get("dining"))]:
            if _unfilled(card.get("venue_name"), card.get("venue_hours"),
                         card.get("time_window")):
                continue
            hours_status = str(card.get("hours_status") or "").lower()
            window = str(card.get("time_window") or "").strip()
            if window and hours_status not in {"verified", "researched"}:
                errors.append(
                    f"day {number}: '{card.get('venue_name')}' is scheduled at {window} while "
                    f"hours_status is '{hours_status or 'unset'}'. Putting a meal on the clock is "
                    f"a claim the venue is open then -- verify the hours for that weekday, or "
                    f"drop the venue. A measured run scheduled two lunches at restaurants that "
                    f"open at 20:00 and every gate passed.")

    if low:
        notes.append("note: venues rated below 4.0/5 -- justified or replaceable, but not "
                     "invisible:\n    - " + "\n    - ".join(low))
    if thin:
        notes.append("note: venues whose rating rests on few reviews (a high score from a "
                     "handful of people is weaker evidence than a good one from thousands):"
                     "\n    - " + "\n    - ".join(thin))


MAP_ENDPOINT_PARAMS = ("origin", "destination", "from", "to", "saddr", "daddr")
# OpenStreetMap packs both ends into one parameter, so a plan routed through OSM used to carry
# no endpoint this function could see at all.
OSM_ROUTE_PARAM = "route"
_LATLON = re.compile(r"^\s*(-?\d{1,3}(?:\.\d+)?)\s*,\s*(-?\d{1,3}(?:\.\d+)?)\s*(?:,.*)?$")


LON_FIRST_HOSTS = ("amap.com", "gaode.com")


def _lon_first(url: str) -> bool:
    """Does this provider write lon,lat? Amap documents that order; the rest write lat,lon."""
    host = urllib.parse.urlparse(url or "").netloc.casefold()
    return any(h in host for h in LON_FIRST_HOSTS)


def _endpoint_coords(value: str, lon_first: bool = False) -> tuple[float, float] | None:
    """Read 'lat,lon' (Google/Apple/OSM) or 'lon,lat,name' (Amap) out of a map URL parameter.

    Range alone cannot tell the two dialects apart, and believing it could broke the one market
    this skill mandates a non-Google provider for. The old rule swapped only when the first
    number exceeded 90, so Beijing (116.4,39.9) decoded correctly while Ürümqi (87.6,43.8) --
    a correct Amap URL -- was read as latitude 87.6 and landed 4,946 km away in the Arctic
    Ocean. Kashgar was out by 4,439 km and Shigatse by 6,691. Worse than the false accusation
    was the remedy it printed: an author who "checked the coordinate order" as told and wrote
    lat,lon got a green gate and every map button pointing at the Arctic -- the exact defect
    this function exists to catch, inverted. references/regional-service-routing.md said so all
    along: the order is provider-specific and is not recoverable from the numbers.

    So take the order from the provider, which is the one thing that actually knows it. The host
    in the URL says which dialect the button will be read in, and reading it that way is what
    makes a genuine mistake visible: an author who writes lon,lat into a Google URL gets the
    endpoint Google will resolve -- somewhere in the Atlantic off Africa -- rather than a
    charitable re-reading. Guessing the nearer interpretation was tried and is worse than the
    bug it fixed: it silently repairs the plan's text while the traveller's button stays broken.
    """
    m = _LATLON.match(value or "")
    if not m:
        return None
    a, b = float(m.group(1)), float(m.group(2))
    if lon_first:
        a, b = b, a
    if abs(a) > 90 or abs(b) > 180:
        # Not a coordinate in the dialect this provider reads. Fall back to the other order only
        # to decide it is unusable rather than to rescue it.
        return None
    return a, b


def _great_circle_km(a: tuple[float, float], b: tuple[float, float]) -> float:
    p = math.pi / 180
    return 2 * 6371 * math.asin(math.sqrt(
        math.sin((b[0] - a[0]) * p / 2) ** 2
        + math.cos(a[0] * p) * math.cos(b[0] * p) * math.sin((b[1] - a[1]) * p / 2) ** 2))


def located_any(coords: list) -> bool:
    return any(point is not None for _, point, _ in coords)


def _map_endpoints(url: str) -> list[tuple[str, str]]:
    try:
        query = urllib.parse.parse_qs(urllib.parse.urlparse(url).query)
    except Exception:  # noqa: BLE001 - a malformed URL is caught by the URL checks
        return []
    pairs = [(k, value) for k in MAP_ENDPOINT_PARAMS for values in [query.get(k)]
             if values for value in values]
    for value in query.get(OSM_ROUTE_PARAM) or []:
        for index, half in enumerate(str(value).split(";")):
            if half.strip():
                pairs.append((f"{OSM_ROUTE_PARAM}[{index}]", half.strip()))
    return pairs


MARKDOWN_IN_PROSE = re.compile(r"\*\*[^*\n]{1,80}\*\*|(?<![\w*])\*[^*\n]{1,60}\*(?![\w*])")


@cites
def check_prose_rendering(plan: dict, errors: list[str], notes: list[str]) -> None:
    """Prose fields are printed verbatim: what you type is what the traveller reads.

    The page has no Markdown renderer, so `**路线概览**` printed its asterisks on a delivered
    plan -- beside a paragraph that had exploded into dot-separated characters, which is how it
    was noticed at all. Emphasis in these fields is not styling; it is four stray asterisks in
    the middle of a sentence.

    Only paired markers are flagged. A lone asterisk is often a real footnote, and a rule that
    fired on those would be argued with rather than obeyed.
    """
    def walk(value: object, path: str) -> None:
        if isinstance(value, str):
            if MARKDOWN_IN_PROSE.search(value):
                sample = MARKDOWN_IN_PROSE.search(value).group(0)[:40]
                errors.append(
                    f"{path} contains Markdown emphasis ({sample!r}), which the page prints "
                    f"literally -- there is no Markdown renderer. Write the sentence so the "
                    f"emphasis is unnecessary, or say the important part first.")
        elif isinstance(value, dict):
            for k, v in value.items():
                if k.endswith("_url") or k in {"id", "map_link_kind"}:
                    continue
                walk(v, f"{path}.{k}")
        elif isinstance(value, (list, tuple)):
            for i, v in enumerate(value):
                walk(v, f"{path}[{i}]")

    for key in ("assumptions", "recheck_before_purchase", "days", "transport_overview",
                "booking_options", "destination_experience_anchors", "entry_context",
                "regional_service_context", "budget"):
        if key in plan:
            walk(plan[key], key)


@cites
def check_prose_agrees_with_data(plan: dict, errors: list[str], notes: list[str]) -> None:
    """A minute figure written into prose must match the field it describes.

    Prose duplicates data, and duplicated facts drift apart: an airport transfer corrected
    everywhere else to 20-35 minutes still read "about 25 minutes" in the transport overview,
    because that paragraph was written before the correction and nothing tied the two together.
    The traveller has no way to know which of the two numbers is the current one.

    Only the overview is checked, and only against the legs that actually exist, because that
    is where the measured drift happened and a rule that guessed at every number in every
    sentence would produce noise instead of findings.
    """
    overview = _obj(plan.get("transport_overview"))
    leg_minutes = {int(_num(s.get("duration_minutes")))
                   for day in [_obj(d) for d in _seq(plan.get("days"))]
                   for s in _segments(day) if _num(s.get("duration_minutes")) > 0}
    if not leg_minutes:
        return
    # Only a figure that reads as "this journey takes N minutes" counts. The first version
    # flagged "walks over 30 minutes were converted" (30 is the traveller's limit, not a leg)
    # and "about 20-35 minutes" (a range, not a single claim), which is how a rule earns the
    # reputation that gets it routed around. A restatement is a bare number followed by the
    # unit, not preceded by a comparison word and not one end of a range.
    RESTATEMENT = re.compile(
        r"(?<![-–—0-9])(\d{1,3})\s*(?:分钟|minutes|min\b)(?!\s*[-–—]\s*\d)")
    COMPARISON = ("超过", "超出", "不超过", "以上", "以内", "上限", "至少", "最多",
                  "over", "under", "within", "at least", "at most", "limit")
    # "every 20 minutes" is a headway, not a journey time, and it lives in the same sentence as
    # the journey time it is not: "€4.60, about 20-35 minutes, 24 hours, every 20 minutes".
    # The first version read that last figure as a claim about the leg and was wrong twice over.
    FREQUENCY = ("每", "间隔", "一班", "发车", "every", "headway", "interval")
    for index, note in enumerate(_seq(overview.get("notes"))):
        text = str(note)
        for m in RESTATEMENT.finditer(text):
            stated = int(m.group(1))
            if stated in leg_minutes:
                continue
            before = text[max(0, m.start() - 12):m.start()]
            after = text[m.end():m.end() + 8]
            if any(w in before for w in COMPARISON):
                continue
            if any(w in before or w in after for w in FREQUENCY):
                continue
            # Three minutes, not five: 40 sat within five of a 35-minute leg while describing
            # a lift's last ascent, and a rule that has to be argued with is a rule that gets
            # worked around. A stale figure is usually the old value of the same fact, which
            # lands very close; an unrelated number rarely does.
            near = [v for v in leg_minutes if abs(v - stated) <= 3]
            if near:
                errors.append(
                    f"transport_overview.notes[{index}] says {stated} minutes, but the nearest "
                    f"leg in the plan declares {sorted(near)[0]}. Prose that restates a number "
                    f"drifts from it -- one plan kept saying 'about 25 minutes' after the leg "
                    f"had been corrected to 35. Quote the field or drop the figure.")


@cites
def check_list_typed_fields(plan: dict, errors: list[str], notes: list[str]) -> None:
    """Fields the contract declares as lists must not be given a bare string.

    The renderer joins these with a separator, and iterating a str yields its characters, so a
    paragraph written as one string instead of a one-element list rendered as
    "这 · 是 · 路 · 线 · 概 · 览" -- every character of a whole paragraph, spaced by dots, on a
    page that passed every gate. The renderer now normalises a lone string so it can never emit
    that again, but normalising quietly would leave the plan wrong and the next author would
    write it the same way. So the shape is checked where the data lives.
    """
    LIST_FIELDS = [
        ("assumptions", plan.get("assumptions")),
        ("recheck_before_purchase", plan.get("recheck_before_purchase")),
        ("sources", plan.get("sources")),
        ("transport_overview.notes", _obj(plan.get("transport_overview")).get("notes")),
        ("budget.included_categories", _obj(plan.get("budget")).get("included_categories")),
        ("budget.unverified_categories", _obj(plan.get("budget")).get("unverified_categories")),
    ]
    for day in [_obj(d) for d in _seq(plan.get("days"))]:
        number = day.get("number")
        LIST_FIELDS.append((f"days[{number}].activities", day.get("activities")))
        LIST_FIELDS.append((f"days[{number}].dining", day.get("dining")))
        LIST_FIELDS.append((f"days[{number}].route.segments", _route(day).get("segments")))
    for path, value in LIST_FIELDS:
        if value is None:
            continue
        if isinstance(value, str):
            errors.append(
                f"{path} is a string, but the contract declares it a list. The renderer joins "
                f"these, and joining a string joins its characters -- a paragraph written this "
                f"way printed as every character separated by dots. Wrap it: [\"…\"].")
        elif not isinstance(value, (list, tuple)):
            errors.append(f"{path} must be a list, got {type(value).__name__}.")


@cites
def check_map_endpoints(plan: dict, errors: list[str], notes: list[str]) -> None:
    """A map URL parameter is a geocoder query, not a caption.

    This exists because a shipped plan wrote its own Chinese display label into the URL --
    origin='酒店（拉斯坎特拉斯海滨）', literally the word "hotel" plus a description. Google
    geocoded it to Taiwan and offered a 65-hour drive to the Canary Islands, while every gate
    passed: the host was right, the status was 200, no parameter was dropped. Nothing measured
    whether the endpoint named a place that exists, because a label and a query had never been
    separate fields.

    The rule that catches it needs no geocoder and no bounding box, only the plan's own numbers:
    the straight line between a leg's two endpoints cannot be longer than the distance that leg
    claims to cover. Taiwan to Gran Canaria is 11,000 km against a declared 6.2 -- it fails on
    arithmetic. Endpoints written as free text are reported rather than failed, because a real
    place name ('Mercado de Vegueta') is a perfectly good query and only a geocoder could tell
    the two apart.
    """
    tolerance = 1.30  # road distance exceeds great-circle; only a gross mismatch is a defect
    checked = 0

    # An absolute reference, because the distance rule alone is relative and therefore blind to
    # a consistently swapped pair: writing lon,lat for BOTH ends of a Las Palmas leg leaves the
    # two points 4.73 km apart instead of 4.70, so the leg passes -- while every pin has moved to
    # latitude -15.4, longitude 28.1, which is southern Africa. Measured, not imagined. One
    # declared destination coordinate turns every endpoint check from relative into absolute.
    # A trip can have more than one destination, and the single-anchor model quietly assumed it
    # could not: New York plus Los Angeles is 3,936 km apart, so one of the two always fell
    # outside any radius wide enough to be useful. Beijing plus Ürümqi is 2,411 km and sat one
    # rounding away from the same fate. Declare every base the trip actually uses -- as one
    # object or a list of them -- and each endpoint is judged against the nearest.
    raw_anchor = _obj(_obj(plan.get("trip")).get("destination_coords")) or None
    anchor_list = _seq(_obj(plan.get("trip")).get("destination_coords")) if isinstance(
        _obj(plan.get("trip")).get("destination_coords"), list) else ([raw_anchor] if raw_anchor else [])
    anchor_points: list[tuple[float, float]] = []
    for item in anchor_list:
        item = _obj(item)
        lat, lon = _num(item.get("lat")), _num(item.get("lon"))
        if abs(lat) <= 90 and abs(lon) <= 180 and (lat or lon):
            anchor_points.append((lat, lon))
    anchor = bool(anchor_list)
    anchor_point = anchor_points[0] if anchor_points else None
    # Derived rather than picked. A reversed pair moves a point 4,300 km (Rome) to 12,000 km
    # (Reykjavik) -- the smallest swap is the floor this has to catch. Legitimate multi-city
    # domestic trips reach 1,067 km (Beijing-Shanghai) and 1,419 km (Sapporo-Fukuoka) -- the
    # largest is the ceiling this must not fail. 800 km was the first guess and sat below both
    # of those, i.e. it would have rejected two ordinary trips to catch nothing extra.
    ANCHOR_RADIUS_KM = 2500.0

    def endpoints_of(url: str, where: str, declared_km: float | None,
                     ratio_check: bool = True, detour_reason: object = None) -> None:
        nonlocal checked
        pairs = _map_endpoints(url)
        if not pairs:
            return
        lon_first = _lon_first(url)
        coords = [(k, _endpoint_coords(v, lon_first), v) for k, v in pairs]
        for key, point, raw in coords:
            if point is None:
                # Free text is refused rather than reported, and this is the whole rule: the
                # distance check below can only run on coordinates, so a plan written entirely
                # in labels used to sail through with a note. That is exactly the plan that
                # shipped -- every endpoint a Chinese caption, one of them geocoded to Taiwan --
                # and a gate that cannot catch the bug it was written for is theatre.
                # A name is not an acceptable substitute because no offline check can tell
                # 'Mercado de Vegueta' (which resolves) from '酒店（拉斯坎特拉斯海滨）' (which
                # resolves to another continent); only a geocoder can, and it is not here.
                # Coordinates cost nothing: the place page that gave you the venue's rating and
                # opening hours put the lat/lon in its own URL.
                errors.append(
                    f"{where}: {key}={raw!r} is free text, not a coordinate pair. A map URL "
                    f"parameter is a geocoder query -- write it as 'lat,lon' (Amap: 'lon,lat,name') "
                    f"so it cannot resolve to the wrong continent and so the distance check can "
                    f"run on it.")
        if anchor_points:
            for key, point, raw in coords:
                if point is None:
                    continue
                away = min(_great_circle_km(a, point) for a in anchor_points)
                if away > ANCHOR_RADIUS_KM:
                    errors.append(
                        f"{where}: {key}={raw!r} sits {away:,.0f} km from the trip's declared "
                        f"destination. Check the coordinate order -- 'lat,lon' reversed reads as "
                        f"a point on another continent while staying the right distance from its "
                        f"partner, so the leg-length rule cannot see it.")
        # A place id beats coordinates at the provider: Google resolves destination_place_id and
        # ignores the numbers beside it. So a URL carrying both is one this checker cannot judge
        # -- the arithmetic below measures a point the traveller will never be sent to. The id
        # cannot be verified offline either, which leaves exactly one honest rule: do not carry
        # both. Keep the id (it names one venue exactly) or keep the coordinates (they can be
        # checked), never a pair that disagree silently.
        if re.search(r"(origin|destination|waypoint)_place_id=", url) and located_any(coords):
            errors.append(
                f"{where}: the URL carries both coordinates and a place id. The provider resolves "
                f"the place id and ignores the coordinates, so every distance rule here is "
                f"measuring somewhere the traveller will not be taken -- and no offline check can "
                f"read a place id. Carry one or the other.")

        located = [p for _, p, _ in coords if p is not None]
        if len(located) == 2 and declared_km and ratio_check:
            straight_now = _great_circle_km(located[0], located[1])
            # The other direction of the leg-length rule, and it catches a different mistake.
            # A road follows the ground, so it runs 1.1x to 1.6x the straight line; a declared
            # distance several times the gap between its own endpoints means the endpoints are
            # not the ones the leg describes. That is how a day shipped with two stops swapped:
            # both coordinates were real places in the right city and the right distance apart,
            # so the bounding-box and leg-length rules both passed, while segment 1 pointed at
            # stop 3. Only applied above 1 km, because the ratio is noise on a 200 m walk that
            # follows a seafront.
            if (straight_now >= 1.0 and declared_km > straight_now * 3.0
                    and not str(detour_reason or "").strip()):
                errors.append(
                    f"{where}: declares {declared_km:g} km but its two endpoints are only "
                    f"{straight_now:.1f} km apart ({declared_km / straight_now:.1f}x). A road is "
                    f"1.1-1.6x its straight line, so at this ratio the endpoints are probably not "
                    f"the stops this leg names -- check that the URL matches the segment's own "
                    f"from/to rather than another pair on the same day. Geography does sometimes "
                    f"force a detour this large: the Grand Canyon rims are 18 km apart and 350 km "
                    f"by road. But no ratio separates that from a mis-wired endpoint -- a "
                    f"legitimate fjord crossing runs 5.0x and a leg pointing at the wrong stop ran "
                    f"5.1x -- so when the detour is real, say so in detour_reason and this passes.")
        if len(located) == 2:
            checked += 1
            straight = _great_circle_km(located[0], located[1])
            if declared_km is not None and declared_km <= 0:
                declared_km = None      # _num() returns 0.0 for a missing value; without this the
                                        # "no declared distance" fallback below was dead code, and
                                        # deleting distance_km switched the whole rule off.
            if declared_km is not None and straight > declared_km * tolerance + 1:
                errors.append(
                    f"{where}: its two map endpoints are {straight:,.0f} km apart in a straight "
                    f"line, but the leg declares distance_km={declared_km:g}. One of the two "
                    f"endpoints does not name the place its label says it does -- a map URL "
                    f"parameter is a geocoder query, not a caption.")
            elif declared_km is None and straight > 400:
                errors.append(
                    f"{where}: its two map endpoints are {straight:,.0f} km apart, which no "
                    f"single day's route covers. Check that both endpoints resolve to the "
                    f"intended places.")

    for day in [_obj(d) for d in _seq(plan.get("days"))]:
        number = day.get("number")
        route = _route(day)
        segments = _segments(day)
        for index, seg in enumerate(segments):
            endpoints_of(str(seg.get("verified_map_url") or ""),
                         f"day {number} segment {index + 1}", _num(seg.get("distance_km")),
                         detour_reason=seg.get("detour_reason"))
            for alt in [_obj(a) for a in _seq(seg.get("alternative_map_links"))]:
                endpoints_of(str(alt.get("url") or ""),
                             f"day {number} segment {index + 1} alternative "
                             f"({alt.get('provider')})", _num(seg.get("distance_km")))
        for alt in [_obj(a) for a in _seq(route.get("alternative_map_links"))]:
            endpoints_of(str(alt.get("url") or ""),
                         f"day {number} route alternative ({alt.get('provider')})",
                         _num(route.get("distance_km")), ratio_check=False)
        multi = len([s for s in _seq(route.get("stops_in_order")) if s]) > 2
        # A single-leg day inherits its segment's detour note: the route URL and the segment URL
        # describe the same journey, so a reason good enough for one is good enough for both.
        route_detour = route.get("detour_reason") or (
            segments[0].get("detour_reason") if len(segments) == 1 else None)
        endpoints_of(str(route.get("verified_map_url") or ""),
                     f"day {number} route", _num(route.get("distance_km")),
                     ratio_check=not multi, detour_reason=route_detour)

        # A walking URL over a distance nobody walks is a mode error the distance rule cannot
        # see, because the distance itself is right: one plan's departure-day button asked
        # Google to walk 25 km from the seafront to the airport. Google answers it, too --
        # with a five-hour route no traveller will ever take.
        try:
            route_query = urllib.parse.parse_qs(urllib.parse.urlparse(
                str(route.get("verified_map_url") or "")).query)
        except Exception:  # noqa: BLE001
            route_query = {}
        route_mode = (route_query.get("travelmode") or [""])[0].lower()
        route_km = _num(route.get("distance_km"))
        if route_mode == "walking" and route_km > 15:
            errors.append(
                f"day {number}: the day's map button asks for WALKING directions over "
                f"{route_km:g} km. Set the travelmode to the mode the day actually uses -- the "
                f"distance can be right while the mode makes the route useless.")

        # A button that says "full-day route" and carries only two of the day's stops is a
        # promise the URL does not keep. The renderer prints the label from this field, so the
        # field has to be true rather than aspirational.
        scope = str(route.get("route_map_scope") or "")
        stops = [s for s in _seq(route.get("stops_in_order")) if s]
        url = str(route.get("verified_map_url") or "")
        try:
            query = urllib.parse.parse_qs(urllib.parse.urlparse(url).query)
        except Exception:  # noqa: BLE001
            query = {}
        carries_waypoints = bool(query.get("waypoints") or query.get("via"))
        mode = (query.get("travelmode") or [""])[0].lower()
        if carries_waypoints and mode == "transit":
            # Learned by opening one: Google Maps computes waypoints for driving, walking and
            # cycling but NOT for transit -- the same URL that routes fine in walking mode
            # answers "cannot calculate public transport directions" and shows nothing. This is
            # checked whatever the declared scope says, because the URL returns no route either
            # way. A multi-stop transit day therefore cannot have a true full-day button at all;
            # the honest scope is primary_leg with the segment buttons as the navigation source,
            # which is what the skill already says when a provider can navigate only one leg.
            errors.append(cite(
                "map.transit_waypoints",
                f"day {number}: the full-day button asks Google for a transit route with "
                f"waypoints, and Google does not compute those -- it returns 'cannot "
                f"calculate public transport directions' and no route. Drop the waypoints "
                f"and set route_map_scope to 'primary_leg', so the label says route overview "
                f"and the per-segment buttons carry the navigation."))
        if scope == "multi_stop" and len(stops) > 2:
            waypoint_count = 0
            for value in (query.get("waypoints") or []) + (query.get("via") or []):
                waypoint_count += len([part for part in re.split(r"[|;]", str(value)) if part.strip()])
            if carries_waypoints and waypoint_count < len(stops) - 2:
                errors.append(
                    f"day {number}: route_map_scope is 'multi_stop' and the URL carries "
                    f"{waypoint_count} waypoint(s), but the day has {len(stops) - 2} stop(s) "
                    f"between its ends. Requiring waypoints and then not counting them let a "
                    f"single throwaway waypoint certify a five-stop day.")
            if not carries_waypoints:
                errors.append(
                    f"day {number}: route_map_scope is 'multi_stop' -- which prints the button as "
                    f"a full-day route -- but its URL carries only an origin and a destination, "
                    f"skipping {len(stops) - 2} intermediate stop(s). Either add the waypoints or "
                    f"set route_map_scope to 'primary_leg' so the label matches what opens.")

    overview = _obj(plan.get("transport_overview"))
    endpoints_of(str(overview.get("overall_route_map_url") or ""),
                 "transport_overview", _num(overview.get("overall_distance_km")) or None,
                 ratio_check=False)

    declared_anchor = anchor
    if checked and not anchor_points and declared_anchor:
        errors.append(
            "trip.destination_coords is present but still at its placeholder (0/0 or blank), so "
            "no map endpoint could be checked against it. Replace it with the destination's own "
            "pair -- the skeleton writes zeros precisely so this is a filled-in field rather than "
            "a forgotten one.")
    elif checked and not anchor_points:
        # Optional was not good enough: without the anchor the endpoint rule is purely relative,
        # and a consistently reversed lat/lon pair keeps its partner the right distance away while
        # moving every pin to another continent. A plan that uses coordinates must say where the
        # trip is, once.
        errors.append(
            "trip.destination_coords is missing, so every map endpoint was checked only against "
            "its own partner. Declare the destination once as {\"lat\": .., \"lon\": ..}: "
            "without it a lat/lon pair written in the wrong order passes the leg-length rule "
            "while pointing at another continent.")

    if checked:
        notes.append(f"note: {checked} map link(s) had both endpoints as coordinates and were "
                     f"distance-checked against the leg they belong to.")


# Hosts that do not answer, or answer uselessly, from inside a market that blocks them. Kept to
# what the skill actually routes through rather than a general blocklist: each entry is a host
# this repo's own code or docs propose as a default somewhere.
GOOGLE_HOSTS = ("google.com", "google.co", "goo.gl", "gstatic.com", "youtube.com")

# Declared-market spellings that mean "Google is not the working default here". Matched against
# regional_service_context.destination_service_market, which the plan writes itself. Deliberately
# NOT derived from the destination name or a coordinate box: this file already learned that
# guessing a market from numbers produces a confident wrong answer (see _lon_first), and a
# bounding box wide enough to hold mainland China also holds Mongolia, Nepal and the Koreas.
#
# Only explicit "mainland" spellings are listed, never a bare "china". That single decision is
# what makes Hong Kong, Macau and Taiwan -- separate markets where Google works normally -- safe
# here, because none of 'hong_kong', 'macau_sar' or 'taiwan_china' contains 'mainlandchina'. An
# earlier draft carried an exclusion list for those three on top of the narrow tokens, which was
# both redundant and unsafe in one direction: it could only ever turn a match OFF, so the one
# case it changed was 'mainland_china_and_hong_kong' -- a trip whose mainland half genuinely
# cannot open Google, quietly exempted. A rule about reachability must fail toward "unreachable".
RESTRICTED_MARKET_TOKENS = ("mainlandchina", "中国大陆", "中國大陸", "prcmainland")


def _plan_urls(node: object, path: str = "$") -> list[tuple[str, str]]:
    """Every http(s) URL in the plan, with the pointer that holds it.

    Walked recursively rather than read from a list of known fields, because a hand-kept field
    list is a gate that falls behind the contract it guards -- this repo already carries one such
    copy (save_trip_deliverables.py's required_booking_types) and says so in a comment. A new
    link field added to the plan contract is covered here the day it appears.
    """
    found: list[tuple[str, str]] = []
    if isinstance(node, dict):
        for key, value in node.items():
            found.extend(_plan_urls(value, f"{path}.{key}"))
    elif isinstance(node, list):
        for index, value in enumerate(node):
            found.extend(_plan_urls(value, f"{path}[{index}]"))
    elif isinstance(node, str) and node.startswith(("http://", "https://")):
        found.append((path, node))
    return found


def _host_of(url: str) -> str:
    return (urllib.parse.urlparse(url or "").hostname or "").casefold()


def _is_google_host(url: str) -> bool:
    host = _host_of(url)
    return any(host == h or host.endswith("." + h) for h in GOOGLE_HOSTS)


def _provider_owns(provider: str, url: str) -> bool | None:
    """Does `provider` own `url`? True/False, or None when the name yields no matchable token.

    Imported lazily so that check_plan_consistency.py keeps working as a standalone lint if
    validate_trip_html.py is ever absent -- an undecidable answer degrades this rule to silent,
    which is the safe direction, whereas an ImportError would take the other seventeen checks
    down with it.
    """
    try:
        from validate_trip_html import provider_target_verdict
    except ImportError:  # pragma: no cover - only when the file is used outside the skill tree
        return None
    return provider_target_verdict(provider, url)


@cites
def check_service_market(plan: dict, errors: list[str], notes: list[str]) -> None:
    """The links must work from where the traveller will be standing.

    The coordinate rule fixed where a link *points*. This fixes who is allowed to *open* it, and
    the two are genuinely different failures.

    Partial cover already existed and is worth stating exactly, because the gap is narrower and
    stranger than "nothing checked this". render_final_trip_html.map_link_allowed refuses a Google
    map link when the market string equals "mainland_china" or access equals "unavailable" -- but
    it runs only inside validate_plan, so this lint saw none of it (a Beijing plan with all 18
    Amap links swapped for Google ones scored 36 errors before and 36 after), and it reads only
    three fields. Measured, on the fixture, these all passed it:

      - transport_overview.overall_route_map_url, the trip's top-level map button
      - a market written "中国大陆" or "mainland_china_prc" rather than exactly "mainland_china"
      - a dining card's venue_url, and every booking or comparison URL in the plan

    So the escape was not the rule being absent; it was the rule being keyed to an exact string
    and pointed at three fields out of a plan full of links. This check walks every URL, matches
    the market by token, and treats `unknown` access as the unchecked state it is.

    The plan's own declarations are what make that possible. regional_service_context carries
    destination_service_market, google_services_access, primary_map_provider and an unused
    primary_map_exception_reason; the renderer displayed all four and no consistency check read
    any of them. A field nobody enforces is a field the next run is free to contradict.

    check_link_targets.py cannot cover any of this, because it measures whether a host answers
    *the machine running it*, which is never the machine inside the blocked market.
    """
    context = _obj(plan.get("regional_service_context"))
    urls = _plan_urls(plan)
    if not urls:
        return
    access = str(context.get("google_services_access") or "").strip().casefold()
    market_raw = str(context.get("destination_service_market") or "")
    market = _fold(market_raw)
    provider = str(context.get("primary_map_provider") or "").strip()
    exception_reason = context.get("primary_map_exception_reason")
    google_links = [(pointer, url) for pointer, url in urls if _is_google_host(url)]

    restricted = any(_fold(token) in market for token in RESTRICTED_MARKET_TOKENS)

    if restricted and access != "unavailable":
        errors.append(
            f"regional_service_context declares destination_service_market "
            f"{market_raw!r} but google_services_access is {access or 'unset'!r}. In that market "
            f"Google services do not answer, so the honest value is 'unavailable' -- and it is "
            f"that value, not the market string, that the link rule below reads.")

    if access == "unavailable" and google_links:
        listed = "\n    - ".join(f"{pointer} -> {url[:110]}" for pointer, url in google_links[:8])
        more = f"\n    ... and {len(google_links) - 8} more" if len(google_links) > 8 else ""
        errors.append(
            f"the plan declares google_services_access 'unavailable' for "
            f"{market_raw or 'this destination'} and then links to Google {len(google_links)} "
            f"time(s). Every one of these is a button the traveller cannot open where they will "
            f"be standing:\n    - {listed}{more}\n  Route them to the provider named in "
            f"primary_map_provider instead.")

    # A declared primary provider that the links do not use. The escape already exists in the
    # contract and was never read; a plan may legitimately mix providers (an official venue map,
    # a rail operator's own planner), so this asks for the reason rather than forbidding it.
    #
    # The comparison is delegated to validate_trip_html.provider_target_verdict rather than
    # rewritten here, and that is not tidiness. The first version of this rule folded the
    # provider name and looked for it in the host, which asks whether '高德地图' appears in
    # 'uri.amap.com'. It does not, so a correct Beijing plan was accused of routing 18 links
    # away from the provider they actually use -- and the identical false positive hit the one
    # Alicante plan that passes every other check. That function already carries the 高德->amap
    # alias table and, crucially, returns None for a name that yields no matchable token, so an
    # undecidable case stays undecided instead of becoming an accusation.
    if provider and not _unfilled(provider):
        route_links = [(pointer, url) for pointer, url in urls
                       if "map_url" in pointer or "map_links" in pointer]
        off_provider = [(pointer, url) for pointer, url in route_links
                        if _provider_owns(provider, url) is False]
        undecidable = [p for p, u in route_links if _provider_owns(provider, u) is None]
        if off_provider and (not exception_reason or _unfilled(exception_reason)):
            listed = "\n    - ".join(f"{p} -> {u[:110]}" for p, u in off_provider[:6])
            errors.append(
                f"primary_map_provider is {provider!r} but {len(off_provider)} map link(s) "
                f"open a different provider, and primary_map_exception_reason is empty:"
                f"\n    - {listed}\n  Either route them through {provider}, or write the "
                f"reason in primary_map_exception_reason so the mix is a decision rather "
                f"than an oversight.")
        if undecidable:
            notes.append(
                f"note: primary_map_provider {provider!r} yields no token matchable against a "
                f"host, so {len(undecidable)} map link(s) could not be checked against it. Open "
                f"one yourself -- this is the set no gate can decide for you.")

    # 'unknown' is not a neutral value once you are asking the traveller to press the button.
    if access in ("", "unknown") and google_links:
        errors.append(cite(
            "market.unreachable_provider",
            f"the plan ships {len(google_links)} Google link(s) while google_services_access is "
            f"{access or 'unset'!r} -- nobody established that the traveller can open them at "
            f"{market_raw or 'the destination'}. Check once and record 'available' or "
            f"'unavailable'; an unchecked link reads as researched to the traveller."))

    if not market_raw.strip():
        errors.append(
            "regional_service_context.destination_service_market is empty while the plan carries "
            f"{len(urls)} link(s). The market is what decides which map, rail and booking hosts "
            "are reachable, so leaving it blank means no check can defend any of them.")


# Every plan check this script runs, in report order. A check that is written but never added
# here does nothing at all, which is the one failure mode worse than not writing it.
# save_trip_deliverables.py imports this tuple, so adding a check here also arms the save path --
# the only path that writes files a traveller keeps.
@cites
def check_prose_texture(plan: dict, errors: list[str], notes: list[str]) -> None:
    """The page must read like a person wrote it, not like a template filled itself in.

    Two different faults, both measured on delivered plans rather than imagined.

    THE SAME SENTENCE TWICE. `focus` and `route_logic` came back byte-identical on 4 of 5 days of
    one plan and 5 of 8 of another, so the page printed one sentence under two headings. Nothing
    caught it because each field, considered alone, was filled in and sensible. It reads as
    padding, which is what it is.

    ONE SENTENCE SHAPE, USED FOR EVERYTHING. The prose in those plans is specific and reason-led
    -- no "vibrant tapestry", no "nestled in the heart of" -- and it still reads mechanical,
    because half the narrative fields are built as fact—dash—significance. Wikipedia's "Signs of
    AI writing" lists em-dash overuse among its structural tells for the same reason: the device
    is fine, the monotony is the tell. Measured at 50% of narrative fields on a shipped plan, so
    the ceiling here is 35%: high enough that the dash stays available where it earns its place,
    low enough that it cannot be the default way a sentence is built.

    Deliberately NOT a banned-word list. A list of forbidden adjectives is trivially satisfied by
    swapping synonyms while the writing stays exactly as hollow, and it fires on a traveller's own
    words. Structure is what these checks can see honestly.
    """
    days = [_obj(d) for d in _seq(plan.get("days"))]
    if not days:
        return

    # (display label, folded-on-demand text, SCOPE). Three elements, and the annotation now says
    # three: it read `list[tuple[str, str]]` while every append below passed a triple, so the
    # third element -- the only one the cross-scope comparison actually needs -- was invisible to
    # a reader and to a type checker alike. That is how the comparison below ended up re-deriving
    # the scope by slicing the human-readable label instead of reading the field that carries it.
    # The label is prose for an operator to act on; the scope is the datum. Kept separate on
    # purpose, because the label's shape changes whenever someone adds a new kind of field here
    # and the scope's meaning does not.
    narrative: list[tuple[str, str, str]] = []
    for position, day in enumerate(days):
        number = day.get("number")
        # The scope identifies the day RECORD by its place in the list, not by the number printed
        # on it. `number` is traveller-supplied data and can be missing or repeated: two days that
        # both omit it used to fold into one scope named "dayNone", and the within-scope rule --
        # the one that is an ERROR because it is always wrong -- then fired on two fields that sit
        # on two different cards. That is the false positive this rule's own comment warns about,
        # arriving through the identity key rather than through the comparison. A record's
        # position is the one thing about it that is always present and always unique.
        scope = f"day#{position}"
        route = _obj(day.get("route"))
        for field, value in (("focus", day.get("focus")),
                             ("contingency", day.get("contingency")),
                             ("route.route_logic", route.get("route_logic")),
                             ("route.walking_burden", route.get("walking_burden")),
                             ("route.fallback_plan", route.get("fallback_plan"))):
            if isinstance(value, str) and len(value.strip()) > 20 and not _blank(value):
                narrative.append((f"day {number} {field}", value.strip(), scope))
        for index, card in enumerate(_seq(day.get("dining")), 1):
            reason = _obj(card).get("why_this_stop")
            if isinstance(reason, str) and len(reason.strip()) > 20 and not _blank(reason):
                narrative.append((f"day {number} dining[{index}].why_this_stop", reason.strip(),
                                  scope))
    for index, anchor in enumerate(_seq(plan.get("destination_experience_anchors"))):
        reason = _obj(anchor).get("why_it_matters")
        if isinstance(reason, str) and len(reason.strip()) > 20 and not _blank(reason):
            narrative.append((f"anchor[{index}].why_it_matters", reason.strip(), "anchors"))
    if not narrative:
        return

    # Scoped WITHIN a day, which is the defect that was measured and the only one that is always
    # wrong: two fields on the same card, under two different headings, printing one sentence.
    # Across days it stays a note, because two days can honestly carry the same walking figure or
    # the same wet-weather fallback, and an error there would fire on correct work -- it fired on
    # a test that legitimately clones a day to exercise replanning.
    #
    # THE ANCHOR LIST IS ONE SCOPE, and that is a decision rather than a leftover. Two anchors are
    # two DIFFERENT places, so one rationale copied onto both is false about at least one of them:
    # "the one place the whole trip was planned around" cannot be two places. That is the same
    # always-wrong shape as one sentence under two headings of a day card, so identical anchor
    # rationales stay an ERROR. It is NOT the honest-repetition case that keeps the cross-scope
    # finding at note level -- two days really can share a wet-weather fallback; two anchors
    # cannot share the reason they are each singular.
    seen: dict[tuple[str, str], str] = {}
    cross_scope: list[str] = []
    for where, text, scope in narrative:
        key = _fold(text)
        if (scope, key) in seen:
            # Same defect, two different pages, so the sentence that tells the operator WHERE to
            # look has to follow the scope. Telling someone their two anchors sit "under two
            # headings on the same card" sends them to a day card that is fine, and a message
            # that points at the wrong place is how a real finding gets dismissed as noise.
            printed = ("under two different headings on the same card, so the traveller reads one "
                       "sentence twice and learns nothing the second time. Say something "
                       "different, or leave the weaker field out."
                       if scope != "anchors" else
                       "as the reason for two different anchors, so one sentence stands in for "
                       "two separate places and cannot be true of both. Say what each anchor is "
                       "actually for, or drop the weaker one.")
            errors.append(
                f"{where} repeats {seen[(scope, key)]} word for word. The page prints both, "
                f"{printed}")
        else:
            seen[(scope, key)] = where
    # The cross-SCOPE pass reads the scope the tuple already carries. The version before this one
    # recovered the day number by splitting the DISPLAY LABEL on whitespace and taking token 1 --
    # "day 3 focus" -> "3" -- which held only because every label it had ever been tried on began
    # with "day <N> ". Anchor labels are "anchor[0].why_it_matters": one token, no space, so
    # `.split()[1]` raised IndexError. Not a cosmetic crash: check_prose_texture is in PLAN_CHECKS
    # and save_trip_deliverables.py runs PLAN_CHECKS, so a plan whose two anchors shared a sentence
    # took down the only path that writes files a traveller keeps, and took it down with a
    # traceback -- the operator saw a broken tool instead of a plan to fix, which is worse than a
    # missed finding because it stops the run rather than the ship. Parsing a label to recover a
    # value the record already holds re-breaks the moment anyone adds a label in a new shape, and
    # adding anchors to this list was exactly that moment.
    elsewhere: dict[str, tuple[str, str]] = {}
    for where, text, scope in narrative:
        key = _fold(text)
        earlier = elsewhere.get(key)
        if earlier is not None and earlier[1] != scope:
            cross_scope.append(f"{where} = {earlier[0]}")
        elsewhere.setdefault(key, (where, scope))
    if len(cross_scope) > 2:
        # Wording follows the fix: the pairs this collects are no longer necessarily two days --
        # a day field and an anchor rationale is the same repetition and is now reachable, so the
        # note must not tell the operator to go compare two days that may not be involved.
        notes.append(f"note: {len(cross_scope)} narrative field(s) are word-for-word identical "
                     f"in two different places -- two days, or a day and the destination "
                     f"anchors. Sometimes honest, often a day nobody wrote: "
                     f"{'; '.join(cross_scope[:3])}")

    # Every dash a writer of any language actually reaches for. The first version matched the
    # Chinese —— and the typographic em dash only, so an English plan written with the ASCII "--"
    # or an en dash escaped the rule completely -- the tell is the sentence shape, and the shape
    # does not change with the codepoint.
    def leans_on_a_dash(text: str) -> bool:
        # A dash between digits is a RANGE -- "09:00–18:00", "20–35 minutes", "2014-07-04" -- and
        # is correct typography, not a sentence shape. Counting those fired on an opening-hours
        # line, which is exactly the false positive that gets a style rule routed around. Only a
        # dash joining clauses counts, so ranges are removed before looking.
        prose = re.sub(r"\d\s*[—–-]+\s*\d", " ", text)
        return bool(re.search(r"——|\s[—–]\s|\s--\s|[—–]", prose))

    dashed = [where for where, text, _ in narrative if leans_on_a_dash(text)]
    if len(dashed) > max(2, int(len(narrative) * 0.35)):
        errors.append(
            f"{len(dashed)} of {len(narrative)} narrative fields build their sentence around a "
            f"dash. The dash is not the problem; using one shape for everything is — every "
            f"rationale lands as fact-dash-significance and the whole page reads generated. "
            f"Rewrite most of these as plain sentences: {', '.join(dashed[:4])}"
            + (f" and {len(dashed) - 4} more" if len(dashed) > 4 else ""))

    hollow = [where for where, text, _ in narrative
              if re.search(r"(不仅[^。]{0,24}(而且|也|还)|not only[^.]{0,30}but also)", text)]
    if hollow:
        notes.append(
            f"note: {len(hollow)} field(s) use a not-only-but-also construction, which is on "
            f"every list of AI writing tells because it inflates two ordinary facts into a "
            f"contrast: {', '.join(hollow[:3])}")


def _blank(value: object) -> bool:
    """Empty, missing, or still a placeholder.

    Not the same question as _unfilled(), and the difference is a live trap rather than a nicety:
    in THIS file _unfilled asks only "does this contain a TODO marker", so _unfilled("") is False.
    check_shortlist_consistency.py defines a function of the same name that also treats None and
    "" as unfilled. Two helpers, one name, two meanings, one skill. Writing the rules below
    against the wrong one made two of their tests pass while asserting a failure -- the check
    looked present and measured nothing, which is the exact defect class this file exists to
    catch, arriving through a helper instead of through prose.
    """
    if value is None:
        return True
    if isinstance(value, str):
        text = value.strip()
        return not text or _unfilled(text)
    return False


@cites
def check_preference_coverage(plan: dict, errors: list[str], notes: list[str]) -> None:
    """Did the trip deliver what the traveller came for?

    Every other check in this file measures whether the plan is safe and agrees with itself. None
    of them measures whether it is the trip that was asked for, and until the contract carried
    `traveler_preferences` none of them could: the intake collected `ranked_must_haves`, the plan
    had no field to put it in, and the sentence "coast is my must-have" was gone by the time any
    JSON existed.

    State the existing cover precisely, because the gap is narrower than "nothing checked this"
    and the imprecise version is how a rule gets built twice. render_final_trip_html.validate_plan
    already requires at least three anchors on a multi-day city trip, so a plan cannot ship with
    none. What it counts is anchors; what it never asks is whether any of them answers anything.
    Measured on a delivered plan: rewriting every anchor as "somewhere" / "no particular reason"
    produced zero anchor findings from that rule and zero from all nineteen checks here.
    SKILL.md's "do not substitute a list of famous sights for real fit" had a headcount behind it
    and nothing else.

    Only the ranked must-haves bind. A must-have is the traveller's own ranking of what the trip
    is for, so an itinerary that never touches one is the wrong trip however well it validates.
    The softer preferences produce a note instead, because "prefer mild warmth" is a dimension of
    a choice already made rather than a thing the days must contain, and a rule that failed on it
    would fire on correct work every winter.

    The link is declared by the author on the anchor, never inferred. Guessing whether "Old town
    lanes at dusk" satisfies "街区漫步" is exactly the judgement call this file has learned not to
    make -- and the same guess, made in the other direction, is what a checker would need to
    decide that it does not.
    """
    trip = _obj(plan.get("trip"))
    if "traveler_preferences" not in trip:
        # Required rather than optional, and an empty ranked_must_haves is a positive claim -- the
        # traveller stated no must-have -- exactly as the skeleton already says of an empty
        # traveler_constraints. Optional would make omission the escape from this rule, which is
        # the shape of every hole this skill has had to close.
        errors.append(
            "trip.traveler_preferences is missing. It carries what the traveller asked FOR, and "
            "without it nothing can check that the itinerary is the trip they wanted -- only that "
            "it is internally consistent. Copy the block from templates/final-trip-plan.json; "
            "empty lists are a claim that they stated no preference, not a placeholder.")
        return
    preferences = _obj(trip.get("traveler_preferences"))
    must_haves = [str(m).strip() for m in _seq(preferences.get("ranked_must_haves"))
                  if isinstance(m, str) and m.strip() and not _blank(m)]
    anchors = [_obj(a) for a in _seq(plan.get("destination_experience_anchors"))]
    satisfied: dict[str, list[str]] = {}
    for anchor in anchors:
        claim = anchor.get("satisfies_preference")
        if _blank(claim):
            continue
        satisfied.setdefault(_fold(str(claim)), []).append(str(anchor.get("name") or "?"))

    excused = {}
    for entry in _seq(preferences.get("unmet_preferences")):
        entry = _obj(entry)
        name, reason = entry.get("preference"), entry.get("reason")
        if _blank(name):
            continue
        if _blank(reason):
            errors.append(
                f"trip.traveler_preferences.unmet_preferences lists {name!r} with no reason. The "
                f"reason is the entire content of the claim: 'the season cannot deliver it' is an "
                f"answer, an empty field is a way to switch the rule off.")
            continue
        excused[_fold(str(name))] = str(reason)

    for must in must_haves:
        key = _fold(must)
        if key in satisfied or key in excused:
            continue
        errors.append(
            f"the traveller ranked {must!r} as a must-have and no experience anchor names it in "
            f"satisfies_preference. Either point an anchor at it, or record it in "
            f"trip.traveler_preferences.unmet_preferences with what the season or the place makes "
            f"impossible. A plan that validates perfectly and misses what the trip was for is "
            f"still the wrong trip.")

    for soft_field in ("natural_subtypes", "human_cultural_subtypes"):
        for value in _seq(preferences.get(soft_field)):
            if _blank(value) or _fold(str(value)) in satisfied:
                continue
            notes.append(f"note: stated preference {str(value)!r} ({soft_field}) is not named by "
                         f"any anchor. Not an error -- a softer preference can be a quality of the "
                         f"days rather than a thing in them -- but worth a look.")

    # An anchor claiming to satisfy something nobody asked for is a mislabel, not a bonus: it is
    # the field the must-have rule reads, so a typo in it silently un-answers a must-have.
    declared = {_fold(p) for p in must_haves}
    declared |= {_fold(str(v)) for f in ("natural_subtypes", "human_cultural_subtypes")
                 for v in _seq(preferences.get(f)) if isinstance(v, str)}
    for key, names in sorted(satisfied.items()):
        if declared and key not in declared:
            errors.append(
                f"anchor(s) {', '.join(names)} claim to satisfy a preference the traveller never "
                f"stated. satisfies_preference must quote one of their own words, because that is "
                f"the string the must-have rule matches on -- a near miss here reads as an "
                f"unanswered must-have and nothing says the two are related.")

    # The avoid list is answered rather than pattern-matched. Deciding from a plan's own fields
    # whether it contains a red-eye, or a crowd, or a long transfer, needs a different fact for
    # every entry the traveller might write; asking how each was honoured needs none.
    handled = {_fold(str(_obj(h).get("item") or "")) for h in _seq(preferences.get("avoid_list_handling"))}
    for entry in _seq(preferences.get("avoid_list_handling")):
        entry = _obj(entry)
        if not _blank(entry.get("item")) and _blank(entry.get("how_avoided")):
            errors.append(
                f"trip.traveler_preferences.avoid_list_handling names {entry.get('item')!r} with "
                f"no how_avoided. Say what in the plan keeps it away.")
    for item in _seq(preferences.get("avoid_list")):
        if _blank(item) or _fold(str(item)) in handled:
            continue
        errors.append(
            f"the traveller asked to avoid {str(item)!r} and the plan says nothing about it. Add "
            f"an avoid_list_handling entry naming what keeps it out of this itinerary -- silence "
            f"about an avoidance reads exactly like an itinerary that contains it.")


def gates_stamp(plan: dict | None = None) -> dict:
    """What this plan was checked against, recorded so a later audit can tell two things apart.

    Auditing the eleven saved plans in a real workspace meant separating "fails a rule that did
    not exist yet" from "fails a rule it always broke", and the only way to do that was to read
    every finding by hand and classify it. The answer mattered -- most findings turned out to be
    the second kind -- and nothing in the plan recorded which gates had ever run on it. A stamp
    costs one field and makes that question answerable instead of archaeological.

    It also records the window the gates ran against, and that half answers a different question.
    Almost every researched fact under a day is keyed to a WEEKDAY, so a date change silently
    invalidates opening hours, closure days, market days and Sunday retail law while the plan still
    looks complete. `replan_trip.py` exists for exactly that and records what it could not
    recompute in `replan_context` -- but `check_replan_context` opens with "a plan with no
    replan_context has nothing to re-verify, and nothing here fires", and the author who edits two
    date strings by hand is precisely the author who writes no replan_context. The gate was
    unreachable by the defect it was written for. Stamping the window the checks actually saw makes
    the hand edit visible without asking anybody to declare it: the plan now disagrees with its own
    receipt.

    No wall-clock here, deliberately. A timestamp would make two saves of the same plan differ, and
    this field is meant to be diffable; the date is the only part any check reads.
    """
    trip = _obj(plan.get("trip")) if isinstance(plan, dict) else {}
    stamp = {"checks": len(PLAN_CHECKS), "checked_by": "check_plan_consistency.PLAN_CHECKS"}
    start = trip.get("start_date")
    end = trip.get("end_date")
    if isinstance(start, str) and start.strip():
        stamp["start_date"] = start
    if isinstance(end, str) and end.strip():
        stamp["end_date"] = end
    return stamp



# new_plan_skeleton.py stamps every date it cannot know as the epoch, and its own docstring lists
# that as a hole with no backstop: "1970-01-01 is conspicuous on the page but no gate rejects it".
# Measured -- a dining card checked_at, a route map_checked_at and a source accessed_at all set to
# 1970-01-01 saved clean, and the page went on printing "verified" beside each one. A timestamp is
# the whole evidence that somebody opened the page, so a sentinel one is not a blank the reader can
# see through: it is the plan asserting a check that never happened.
EPOCH_SENTINEL = "1970-01-01"


@cites
def check_sentinel_timestamps(plan: dict, errors: list[str], notes: list[str]) -> None:
    """No date field may still hold the skeleton's epoch placeholder.

    Walks the whole plan rather than naming the fields, because the fields that carry evidence keep
    being added -- rating_checked_at and hours_status arrived after the skeleton did -- and a list
    written today protects the keys whoever wrote it happened to remember. Anything whose key ends
    in _at is a timestamp by this contract's own naming, and that convention does not go stale.
    """
    def walk(node: object, path: str) -> None:
        if isinstance(node, dict):
            for key, value in node.items():
                # intake_context carries its own, better-worded message about the same sentinel.
                if path == "" and key == "intake_context":
                    continue
                if (key.endswith("_at") and isinstance(value, str)
                        and value.startswith(EPOCH_SENTINEL)):
                    found.append(f"{path}{'.' if path else ''}{key}")
                else:
                    walk(value, f"{path}{'.' if path else ''}{key}")
        elif isinstance(node, list):
            for index, item in enumerate(node):
                walk(item, f"{path}[{index}]")

    found: list[str] = []
    walk(plan, "")
    if not found:
        return
    # One error, not sixty-one. A fresh four-day skeleton carries a sentinel in every timestamp it
    # cannot know, and reporting each separately buried the other seventeen findings under
    # identical text -- which is how a check trains people to skim past it. The paths are what the
    # author needs; the sentence only has to be read once.
    shown = ", ".join(found[:8])
    more = f", and {len(found) - 8} more" if len(found) > 8 else ""
    errors.append(
        f"{len(found)} timestamp(s) still hold the skeleton's {EPOCH_SENTINEL} placeholder: "
        f"{shown}{more}. A checked-at date is the evidence that somebody opened the page, so "
        f"shipping the sentinel claims a check that never happened. Write the date each was "
        f"actually checked, or remove the claim it supports.")


# The two traveller constraints the gates MEASURE -- the allergy severity and the walking cap --
# arrive from intake as prose, and nothing converts a sentence into an enum or a number. The
# skeleton therefore cannot know either one, and until it said so it emitted values that read as
# answers: allergy_severity "none" and max_continuous_walking_minutes null. Measured on a real
# five-day plan: with those untouched defaults, deleting EVERY activity's on_foot_minutes changed
# the error count not at all, 2 -> 2, because check_walking_budget arms itself off `cap is not
# None`; with the cap typed as 25, the same deletion produced five precise findings naming each
# day. Worse than lax, it was profitable: SKILL.md's light verification tier is allowed only when
# allergy_severity is none/preference AND the cap is null -- which is to say the skeleton's
# untouched defaults were exactly what bought the cheap tier. A model that never typed those two
# fields switched the walking checks off and skipped four verification domains in one move, and
# neither gate said a word.
#
# Neither field can hold a `TODO:` string the way the free-text fields do: validate_plan requires
# allergy_severity to be an ALLERGY_SEVERITIES member or null, and max_continuous_walking_minutes
# to be a positive whole number or null, so prose in either one stops the skeleton rendering at
# all -- and the enum's message would then read "must be one of: none, preference, intolerance,
# severe" about a placeholder, sending the author hunting for a typo instead of telling them
# nobody answered the question. And null cannot carry the meaning either: for the cap, null IS the
# documented answer "the traveller stated no limit", so overloading it would destroy the very
# distinction this exists to make.
#
# So the marker sits BESIDE them, keyed by the field it stands for, carrying the same `TODO:`
# prose every other unfilled value in the skeleton carries. new_plan_skeleton.py imports this name
# rather than restating the string, because a gate keyed on a spelling nothing produces passes
# every test in the suite while never once firing on a real plan.
UNTYPED_CONSTRAINTS_MARKER = "untyped_constraints"

# What each marked field means when it IS typed, quoted back to the author so the error says what
# to write rather than only what is wrong. Keyed by field name; a field named in the marker that
# is not listed here still reports, with a generic instruction, because a marker nobody recognises
# is still a question nobody answered.
UNTYPED_CONSTRAINT_GUIDANCE = {
    "allergy_severity": (
        "type none | preference | intolerance | severe from the traveller's own words -- 'none' "
        "is a claim that there is nothing to avoid, so it has to be a claim somebody made"),
    "max_continuous_walking_minutes": (
        "type the minutes they said they can walk at a stretch, or null if they stated no limit "
        "-- null switches every per-leg and per-activity walking check off, so it has to be a "
        "decision rather than a default"),
}


# The three answers the marker can give, named once rather than re-derived at each call site.
# THREE functions in this file read this one key -- required_domains_for for the verification
# tier, check_untyped_constraints for the refusal, and check_walking_budget for its per-day note --
# and each read it with its own inline shape test. That is exactly how the first two came to
# disagree about the same plan. required_domains_for asks `if untyped:`, so
# `"untyped_constraints": false` is falsy and the light tier is allowed; check_untyped_constraints
# asked `isinstance(marker, (dict, list, tuple, str)) and not marker`, which no bool and no number
# satisfies, so the SAME plan was refused with "is a bool (False). It must be an object keyed by
# the constraint fields nobody has typed yet". Measured on this module before this function
# existed: False -> 1 error, 0 -> 1 error, 0.0 -> 1 error, while "" -> 0, {} -> 0, [] -> 0 -- six
# spellings of one sentence and three of them were refused. One reader, so the disagreement has
# nowhere left to live.
UNTYPED_MARKER_CLEAR = "clear"            # no marker, or a marker that says "nothing is untyped"
UNTYPED_MARKER_FIELDS = "fields"          # the marker names the fields nobody has typed
UNTYPED_MARKER_UNREADABLE = "unreadable"  # a marker is there in a shape nothing can act on


def _as_json_text(value: object) -> str:
    """The value as it is spelled in the .json file the author is looking at, never as Python.

    The author reads a JSON document. Telling them an entry is `None` sends them searching a file
    whose word is `null`, and telling them it is `['allergy_severity']` sends them searching for
    single quotes JSON does not have. check_untyped_constraints already applied this rule to the
    marked field's VALUE and the rule was never carried across to the marker's own ENTRIES, which
    is how `trip.traveler_constraints.None` and `trip.traveler_constraints.['allergy_severity']`
    reached an operator. Falls back to repr rather than raising, because a crash inside an error
    message loses every other finding in the report with it.
    """
    try:
        return json.dumps(value, ensure_ascii=False)
    except (TypeError, ValueError):
        return repr(value)


# What separates a marker entry that can be reported from one that can only be refused.
#
# A marker entry has exactly one job: name a field of traveler_constraints, so the refusal can say
# "type THIS, then delete THIS entry". An entry that does that is READABLE, and it stays readable
# even when the name is one this module has never heard of ("pace") or is not in the block yet --
# those are answerable questions with a concrete subject, and the message tells the author which
# case they are in. An entry that does NOT name anything is UNREADABLE, and there are exactly two
# ways to fail to name something: be an empty or whitespace-only string, or not be a string at all
# (a number, null, true, a nested list or object -- shapes a hand-edit produces and JSON permits
# inside a list).
#
# The decision the reviewer's finding forced: both categories are REFUSED, and neither is dropped.
# What differs is what the message is allowed to claim. A readable entry gets the full instruction
# quoting the field. An unreadable entry gets an honest "this entry names no field" refusal that
# says what is wrong with it and shows it in JSON spelling -- because the previous behaviour,
# str()-ing it into an error path, produced `trip.traveler_constraints.` with nothing after the
# dot: a message that is loud, points at nothing, and cannot be acted on, which is the same
# silence the check exists to prevent wearing a different coat.
#
# And the split is PER ENTRY, not per marker. `{"allergy_severity": "TODO", "": "x"}` carries one
# perfectly good question and one piece of junk; refusing the whole marker as unreadable would
# bury the half the author can actually act on.
def _split_marker_entries(entries: list[tuple[str, object]]) -> tuple[list[str], list[tuple[str, object]]]:
    """(readable field names, unreadable [location, entry] pairs) from the marker's raw entries.

    `location` is the JSON path suffix the entry sits at -- "" for a dict key, "[2]" for the third
    member of a list -- so the refusal can point an author at one entry of many rather than at the
    marker as a whole.
    """
    readable: list[str] = []
    unreadable: list[tuple[str, object]] = []
    for location, entry in entries:
        # str.strip() removes U+3000 IDEOGRAPHIC SPACE as well as ASCII blanks, so a marker key
        # pasted out of a Chinese intake is judged by the same rule as an English one rather than
        # slipping through as a "name" made of invisible width.
        if isinstance(entry, str) and entry.strip():
            readable.append(entry)
        else:
            unreadable.append((location, entry))
    return readable, unreadable


def read_untyped_constraints(constraints: object) -> tuple[str, list[str], list[tuple[str, object]]]:
    """What the skeleton's "nobody typed this" marker says, for every check that must obey it.

    Returns (state, fields, unreadable): one of the UNTYPED_MARKER_* constants; the field names the
    marker readably carries; and the entries that name no field, as (location, entry) pairs kept
    verbatim so a refusal can show the author exactly what to delete. Takes the
    traveler_constraints block rather than the plan, and _obj()s it, so a plan whose constraints are
    a string or a list gets a finding from the caller instead of a traceback that loses every other
    finding in the report.

    The states are what callers need to say different things about. A refusal wants to name the
    untyped fields; a note about a null walking cap wants to know whether anybody answered at all;
    a tier decision wants to know only whether a question is open. None of them can be written
    correctly against a raw `if marker:`.

    UNTYPED_MARKER_FIELDS means the marker names at least one field. A container whose every entry
    is unreadable is UNTYPED_MARKER_UNREADABLE, not FIELDS with an empty list: `{"": "x"}` asserts
    that a question is open and then names nothing, which is the same standing as a bare `true`,
    and callers that branch on the state must not be told a field list exists when it does not.
    `unreadable` is populated in BOTH of those states, because the FIELDS case can carry junk
    beside good names and the junk must still be refused.
    """
    marker = _obj(constraints).get(UNTYPED_CONSTRAINTS_MARKER)
    if marker is None:
        return UNTYPED_MARKER_CLEAR, [], []
    # An emptied container is the author saying "I typed them and cleared the marker", which is
    # the intended exit. Accepting {} and [] rather than only a deleted key means the honest edit
    # does not depend on knowing that the whole key must go.
    if isinstance(marker, (dict, list, tuple, str)) and not marker:
        return UNTYPED_MARKER_CLEAR, [], []
    # `false` and `0` are that same sentence in the scalar spelling, and an author who writes
    # either one plainly means "nothing here is untyped" -- there is no second reading. Excluded
    # deliberately: `true` and any non-zero number, which say a question is open while naming
    # nothing, and are handled as unreadable below. NaN fails `== 0` and lands there too, which is
    # right: nobody can act on it either.
    if isinstance(marker, (int, float)) and marker == 0:
        return UNTYPED_MARKER_CLEAR, [], []
    if isinstance(marker, dict):
        # Keys are taken RAW rather than str()-ed. JSON can only produce string keys, but this
        # module is imported and called with Python-built dicts by tests and by sibling scripts,
        # and str()-ing a key was precisely what turned `{7: "x"}` into a field named "7" and
        # `{None: "x"}` into a field named "None" -- names that appear nowhere in any plan file.
        entries = [("", name) for name in marker]
    elif isinstance(marker, (list, tuple)):
        # Tolerated because a hand-edit that keeps only the field names is still an honest,
        # readable marker; refusing it would fail the author for a shape that says the same thing.
        # Indexed, because a list is the shape where one bad member sits among good ones and
        # "delete the entry" is only actionable if the author is told which entry.
        entries = [(f"[{i}]", item) for i, item in enumerate(marker)]
    else:
        return UNTYPED_MARKER_UNREADABLE, [], []
    fields, unreadable = _split_marker_entries(entries)
    state = UNTYPED_MARKER_FIELDS if fields else UNTYPED_MARKER_UNREADABLE
    return state, fields, unreadable


@cites
def check_untyped_constraints(plan: dict, errors: list[str], notes: list[str]) -> None:
    """Refuse a plan still carrying the skeleton's "nobody typed this" marker.

    This is check_sentinel_timestamps' sibling and it is written to the same rule: fire on the
    SENTINEL, never on the value the sentinel stands in for. That rule is the whole reason this
    check can live in PLAN_CHECKS at all.

    Where it belongs was the real decision. render_final_trip_html.intake_context_errors solves a
    similar-looking problem -- a field a plan must answer before a traveller may be handed it --
    and is called from save_trip_deliverables.py rather than from validate_plan, deliberately,
    because it fires on ABSENCE: putting it in the shared validator would fail the skeleton's own
    output and retroactively invalidate every plan already saved in a workspace, which
    audit_workspace.py re-reads with these same checks. That precedent does not transfer here, and
    the difference is exactly the one it names. This check fires only when a key is PRESENT, and
    the only thing that writes that key is a skeleton generated after this change: no plan written
    before it can carry the marker, so no plan written before it can newly fail. Verified rather
    than assumed -- all fifteen plans in the measured workspace produce byte-identical findings
    with this check in PLAN_CHECKS, twelve because they carry no traveler_constraints block at all
    and three because they carry a typed cap and no marker.

    Being in PLAN_CHECKS is what makes it worth having: that tuple is what save_trip_deliverables.py
    runs on the one path that writes files a traveller keeps, what audit_workspace.py runs over a
    whole workspace, and what an author sees in the skeleton's own worklist. A save-time-only check
    would let the marker survive every intermediate run and surface at the end, which is the point
    where an operator is most tempted to reach for a bypass.
    """
    constraints = _obj(_obj(plan.get("trip")).get("traveler_constraints"))
    marker = constraints.get(UNTYPED_CONSTRAINTS_MARKER)
    # The three shape branches this function used to carry inline now live in
    # read_untyped_constraints, with their reasoning moved across word for word, because
    # check_walking_budget has to reach the same verdict about the same key and a second copy of
    # the logic is a second answer waiting to happen.
    state, fields, unreadable = read_untyped_constraints(constraints)
    if state == UNTYPED_MARKER_CLEAR:
        return
    if state == UNTYPED_MARKER_UNREADABLE and not unreadable:
        # A truthy value of any other shape -- a bare string, a number, True -- is a marker
        # nobody can act on. Say so loudly rather than guessing which fields it meant: silently
        # ignoring an unrecognised marker is how this whole class of defect stayed invisible.
        #
        # Guarded on `not unreadable` because there is now a second way to reach UNREADABLE: a
        # container whose every ENTRY is junk, e.g. {"": "x"}. That one is not a marker of the
        # wrong shape -- the shape is right and the contents name nothing -- so it falls through
        # to the per-entry refusals below, which can point at the offending entry instead of
        # re-describing the whole object back to its author.
        errors.append(
            f"trip.traveler_constraints.{UNTYPED_CONSTRAINTS_MARKER} is a "
            f"{type(marker).__name__} ({marker!r}). It must be an object keyed by the constraint "
            f"fields nobody has typed yet, as new_plan_skeleton.py writes it, or be deleted once "
            f"they are typed. A marker whose shape nothing can read is a question nobody answered "
            f"and nobody can see. If you meant that nothing here is untyped, the readable "
            f"spellings are {{}}, [], \"\", false and 0, and all five are accepted -- "
            f"{marker!r} is refused because it cannot be told apart from an author who set out to "
            f"list the open fields and never did.")
        return

    # The entries that name no field, refused on their own terms. Reported BEFORE the readable
    # ones and sorted by their JSON location so the order is stable run to run: a report whose
    # lines reshuffle between runs cannot be diffed, and audit_workspace.py diffs these.
    #
    # This whole loop is the reviewer's finding. These entries used to be str()-ed straight into
    # the readable path, which produced "trip.traveler_constraints. was never typed" for {"": "x"}
    # -- an error naming no field, telling the author to type "it" and then delete '' -- and
    # "trip.traveler_constraints.None" / ".7" / ".['allergy_severity']" for the non-string members
    # of a list. Every one of those is loud and unactionable, which is the failure this check
    # exists to prevent, not a milder version of it.
    for location, entry in sorted(unreadable, key=lambda pair: (pair[0], _as_json_text(pair[1]))):
        where = (f"{UNTYPED_CONSTRAINTS_MARKER}{location}" if location
                 else f"a key of {UNTYPED_CONSTRAINTS_MARKER}")
        if isinstance(entry, str):
            # Split from the non-string case because the fix differs. Whitespace is invisible on
            # screen, so an author told only "unreadable" would look at a line that appears to
            # hold a name; naming the character count is what makes it findable.
            wrong = ("it is an empty string" if not entry
                     else f"it is {len(entry)} whitespace character"
                          f"{'' if len(entry) == 1 else 's'} and nothing else")
        else:
            # "of type int" rather than "a int": the type name is chosen by Python, so no article
            # written here can be right for all of them, and a report that reads as broken English
            # is a report an operator trusts less than it deserves.
            wrong = f"it is of type {type(entry).__name__} ({_as_json_text(entry)}), not a string"
        errors.append(
            f"trip.traveler_constraints.{UNTYPED_CONSTRAINTS_MARKER}: the entry at {where} names "
            f"no field -- {wrong}. This entry is unreadable, so there is nothing to tell you to "
            f"type: a marker entry exists to name one field of trip.traveler_constraints, and "
            f"this one names none. Replace it with the field name the traveller's answer belongs "
            f"in, or delete the entry outright if it is left-over punctuation from a hand-edit. "
            f"Refused rather than skipped because an entry nobody can read is still an author "
            f"asserting that a question is open, and dropping it silently would hand the "
            f"traveller a plan whose open question nothing ever printed. If you meant that "
            f"nothing here is untyped, the readable spellings are {{}}, [], \"\", false and 0.")

    for field in sorted(fields):
        # The name as it will be quoted and looked up. A key carrying surrounding whitespace is
        # readable -- it names something -- but " allergy_severity " matches no key in the block by
        # string equality and looks identical to the clean spelling in any editor, so the padding
        # is stripped for the lookup and called out separately below rather than silently producing
        # a "not even present" that sends the author hunting a field that is right there.
        clean = field.strip()
        guidance = UNTYPED_CONSTRAINT_GUIDANCE.get(
            clean, "type it from the traveller's own words, then delete this entry")
        # Quoted in JSON spelling, not Python's: the author is looking at a .json file, and an
        # error that says the field is "still None" sends them searching a document that has no
        # such word in it. json.dumps falls back to repr for a value it cannot serialise rather
        # than raising, because a crash inside an error message loses the other findings with it.
        present = field in constraints or clean in constraints
        held = constraints.get(field, constraints.get(clean))
        shown = _as_json_text(held)
        current = (f"still {shown}" if present
                   else "not even present in trip.traveler_constraints")
        # Two different jobs wearing one message. A KNOWN field that the block has not got yet is
        # answered by typing it into the block. A name this module has never heard of -- "pace",
        # a typo, a constraint the schema has no slot for -- cannot be answered that way at all,
        # and an author told to "type it" would add a key nothing reads. Say which case it is.
        unknown = (clean not in UNTYPED_CONSTRAINT_GUIDANCE and not present)
        tail = ""
        if unknown:
            tail = (f" Note that {_as_json_text(clean)} is not a field this checker recognises and "
                    f"is not in the block either, so typing it into trip.traveler_constraints buys "
                    f"nothing on its own: either it is a misspelling of a real constraint field, "
                    f"or the traveller's answer belongs somewhere this schema does carry it.")
        if field != clean:
            tail += (f" The marker entry is spelled {_as_json_text(field)}, with whitespace around "
                     f"the name; that padding never matches the block's key and is invisible in an "
                     f"editor, so fix the entry to {_as_json_text(clean)} as well.")
        errors.append(
            # The path carries `clean`, never the padded spelling: an error path ending in
            # invisible whitespace is unclickable, ungreppable, and indistinguishable from the
            # clean field it is not.
            f"trip.traveler_constraints.{clean} was never typed -- "
            f"{UNTYPED_CONSTRAINTS_MARKER} still names it and the field is {current}. {guidance}, "
            f"then delete {_as_json_text(field)} from {UNTYPED_CONSTRAINTS_MARKER}. Until then "
            f"this is not the "
            f"traveller's answer, it is the skeleton's default: the intake collects this as prose "
            f"and nothing converts a sentence into an enum or a number, so an untyped field leaves "
            f"the walking and dining gates measuring nothing while the plan reads as though the "
            f"traveller had no constraint at all.{tail}")


SALE_STATUSES = ("always_available", "scheduled_release", "at_the_door", "sold_out_or_unavailable")


def _sale_clock_minutes(value: object) -> int | None:
    """Minutes past midnight from the time half of an ISO date-time, e.g. "12:00:00+09:00".

    Delegates to _parse_hhmm rather than matching HH:MM again. The first version of this file's
    sale-window rule carried its own regex and it was ASCII-only, so a Chinese plan writing
    09：00 with a fullwidth colon parsed everywhere else in this module and nowhere in that rule --
    the check went quiet on exactly the plans this skill added a second language for. One parser,
    and it is the one that already knows both colons.
    """
    text = str(value or "")
    head = re.split(r"[+\-Z]", text, maxsplit=1)[0]
    parts = re.split(r"[:：]", head)
    return _parse_hhmm(f"{parts[0]}:{parts[1]}") if len(parts) >= 2 else None


@cites
def check_ticket_sale_windows(plan: dict, errors: list[str], notes: list[str]) -> None:
    """A ticket you cannot be at a screen to buy is not a ticket the traveller has.

    The recorded case: Kabukiza single-act seats go on sale at 12:00 the day before, and at that
    moment the plan itself had the traveller in the Narita immigration queue. The plan's own
    timeline refuted its own instruction, and nothing compared the two because the sale moment was
    not data -- `timed_entry_or_reservation` is free text.

    Required only on tickets an activity actually schedules. A ticket listed as a booking option
    nobody put on a day cannot strand anyone, and taxing every ordinary museum admission with a
    research item is how a rule earns its way around a research budget. The field is cheap on the
    common case: `always_available` with one sentence of basis.

    `basis` is the point of the design, not paperwork. An optional field would have been this
    skill's own recurring defect a seventh time -- the agent that never researched the sale window
    is the one that omits the field, so the gate reports clean on the run that motivated it. But a
    required field with a free vocabulary invites the opposite failure: `always_available` typed
    reflexively without opening anything, which is a fabricated fact rather than a visible blank,
    and worse than what it replaces. One sentence saying where the rule came from is writable by
    someone who opened the official page and not by someone who guessed.
    """
    days = [_obj(d) for d in _seq(plan.get("days"))]
    day_by_number = {d.get("number"): d for d in days}
    day_by_date = {str(d.get("date") or "").strip(): d for d in days if d.get("date")}

    scheduled: dict[str, set] = {}
    for day in days:
        for activity in [_obj(a) for a in _seq(day.get("activities"))]:
            ref = activity.get("ticket_option_id")
            if ref:
                scheduled.setdefault(ref, set()).add(day.get("number"))

    for ticket in [t for t in _seq(_obj(plan.get("booking_options")).get("attraction_tickets"))
                   if isinstance(t, dict)]:
        name = ticket.get("attraction_name") or ticket.get("id") or "unnamed ticket"
        if not scheduled.get(ticket.get("id")):
            continue

        window = ticket.get("sale_opens_at")
        if not isinstance(window, dict):
            errors.append(
                f"attraction ticket {name!r} is scheduled on a day but declares no sale_opens_at. "
                f"Say when it can be bought: status always_available | scheduled_release | "
                f"at_the_door | sold_out_or_unavailable, plus one sentence of basis. A ticket the "
                f"traveller cannot be at a screen to buy is not a ticket they have.")
            continue

        status = str(window.get("status") or "").strip()
        if status not in SALE_STATUSES:
            errors.append(
                f"attraction ticket {name!r} sale_opens_at.status is {status!r}, which is not one "
                f"of {', '.join(SALE_STATUSES)}.")
            continue

        basis = window.get("basis")
        if not isinstance(basis, str) or not basis.strip():
            errors.append(
                f"attraction ticket {name!r} sale_opens_at has no basis. Write the sentence that "
                f"says where the rule came from -- it is what separates a sale window somebody "
                f"read from one somebody assumed, and an assumed 'always_available' is an invented "
                f"fact rather than a blank.")
        elif _unfilled(basis):
            errors.append(
                f"attraction ticket {name!r} sale_opens_at.basis is still a placeholder.")

        if status != "scheduled_release":
            continue

        opens_at = str(window.get("opens_at") or "").strip()
        try:
            # Only the date half has to parse; the clock is read separately because a plan may
            # write "2026-09-27T12:00+09:00", which date.fromisoformat rejects on older Pythons.
            dt.date.fromisoformat(opens_at.split("T")[0])
            parseable = bool(opens_at)
        except ValueError:
            parseable = False
        if not parseable:
            errors.append(
                f"attraction ticket {name!r} declares a scheduled_release but no ISO opens_at "
                f"date-time. That moment is the whole subject of this field.")
            continue

        sale_date, _, sale_clock = opens_at.partition("T")
        sale_minutes = _sale_clock_minutes(sale_clock)

        # 1. The sale must not fall after the traveller needs the ticket.
        for number in sorted(n for n in scheduled[ticket.get("id")] if n is not None):
            used_on = str(_obj(day_by_number.get(number)).get("date") or "").strip()
            if used_on and sale_date > used_on:
                errors.append(
                    f"attraction ticket {name!r} goes on sale {opens_at}, after day {number} "
                    f"({used_on}) when the plan already has the traveller using it.")

        # 2. The recorded defect: the sale falls on a day inside the trip, at an hour the plan
        #    itself has the traveller not yet arrived anywhere. Only fires when the sale lands on
        #    a planned day -- a sale before departure is the normal case and says nothing.
        day = day_by_date.get(sale_date)
        if day is None or sale_minutes is None:
            continue
        activity_times = [t for t in (_parse_hhmm(str(_obj(a).get("time") or ""))
                                      for a in _seq(day.get("activities"))) if t is not None]
        if activity_times and sale_minutes < min(activity_times):
            errors.append(
                f"attraction ticket {name!r} goes on sale at {sale_clock or opens_at} on "
                f"{sale_date}, and the plan's own day {day.get('number')} has the traveller "
                f"nowhere until {min(activity_times) // 60:02d}:{min(activity_times) % 60:02d} -- "
                f"they are still in transit when the seats are released. Buy it earlier, drop it, "
                f"or say in the plan who buys it and from where.")


# The limits the intake form collects, as (intake path, plan path). The same mapping
# new_plan_skeleton.py --from-intake copies by, so what the skeleton carries is exactly what this
# compares -- a second, drifting copy of "which field goes where" is how a check ends up guarding a
# field nobody writes.
INTAKE_CONSTRAINT_FIELDS: dict[str, tuple[tuple[str, ...], tuple[str, ...]]] = {
    "dietary_or_religious_needs": (("feasibility", "dietary_or_religious_needs"),
                                   ("trip", "traveler_constraints", "dietary_or_religious_needs")),
    "mobility_notes": (("party", "mobility_or_access_needs"),
                       ("trip", "traveler_constraints", "mobility_notes")),
    "traveler_count": (("party", "traveler_count"), ("trip", "traveler_count")),
    "cap_per_person": (("budget", "hard_cap_amount"), ("budget", "cap_per_person")),
}


def _intake_path_value(node: object, path: tuple[str, ...]) -> object:
    for key in path:
        node = node.get(key) if isinstance(node, dict) else None
    return node


def _declared_intake_changes(plan: dict, errors: list[str]) -> list[dict]:
    """trip.intake_changes, each naming a compared field and saying why it moved.

    The escape exists because travellers change their minds at the checkpoint -- a real run raised
    its cap from the form's figure to 1300 -- and a gate that refused every such plan would be
    routed around. It costs a sentence, and the page prints the sentence, so the traveller sees
    their own change rather than a plan that quietly disagrees with what they typed.
    """
    raw = _obj(plan.get("trip")).get("intake_changes")
    if raw is None:
        return []
    if not isinstance(raw, list):
        errors.append("trip.intake_changes must be a list of {field, intake_value, plan_value, "
                      "reason} objects, one per constraint the traveller changed after the form.")
        return []
    kept = []
    for position, entry in enumerate(raw):
        entry = _obj(entry)
        field, reason = entry.get("field"), entry.get("reason")
        if field not in INTAKE_CONSTRAINT_FIELDS:
            errors.append(
                f"trip.intake_changes[{position}].field is {field!r}; it must be one of "
                f"{', '.join(INTAKE_CONSTRAINT_FIELDS)}.")
        elif not isinstance(reason, str) or not reason.strip() or _blank(reason):
            errors.append(
                f"trip.intake_changes[{position}] ({field}) gives no reason. A change to what the "
                f"traveller told the form is theirs to make -- write when and why, in their words; "
                f"the page prints it beside their constraints.")
        else:
            kept.append(entry)
    return kept


def _intake_constraint_findings(intake: dict, plan: dict, errors: list[str],
                                notes: list[str]) -> None:
    """The allergy, the walking limit, the party and the cap: the form's answers against the plan.

    Measured 2026-09-24 against v2.7.0: an intake carrying a severe dairy allergy and a 20-minute
    walking limit, a plan carrying neither, and 0 findings -- while the same plan missing one
    ranked must-have produced 1. The must-haves had a cross-check; the constraints whose violation
    is a medical or a stranding risk did not. The skeleton copies them, but a plan built from
    flags, edited afterwards, or written by a second planner never went through the skeleton.
    """
    changes = _declared_intake_changes(plan, errors)

    def excused(field: str, value: object = None) -> bool:
        return any(change.get("field") == field and (
            value is None or _fold(str(change.get("intake_value") or "")) == _fold(str(value)))
            for change in changes)

    def figure(value: object) -> float | None:
        if isinstance(value, bool):
            return None
        try:
            return float(str(value).strip())
        except ValueError:
            return None

    def excused_figure(field: str, intake_value: object, plan_value: object) -> bool:
        """A recorded change excuses a figure only while it still describes this plan: the value
        the intake holds and the value the plan now holds. A stale entry -- 2 -> 1 recorded, the
        plan since moved to 5 -- used to silence the check for the field outright, and the page
        printed the recorded change beside the figure that contradicted it."""
        return any(change.get("field") == field
                   and figure(change.get("intake_value")) is not None
                   and figure(change.get("plan_value")) is not None
                   and figure(intake_value) is not None and figure(plan_value) is not None
                   and abs(figure(change.get("intake_value")) - figure(intake_value)) <= 0.005
                   and abs(figure(change.get("plan_value")) - figure(plan_value)) <= 0.005
                   for change in changes)

    def stale(field: str) -> str:
        recorded = [c for c in changes if c.get("field") == field]
        if not recorded:
            return ""
        return (f" trip.intake_changes records {field} "
                f"{recorded[-1].get('intake_value')!r} -> {recorded[-1].get('plan_value')!r}, which no "
                f"longer describes this plan; update that entry to the figures the traveller agreed.")

    for field in ("dietary_or_religious_needs", "mobility_notes"):
        source, target = INTAKE_CONSTRAINT_FIELDS[field]
        collected = [v.strip() for v in _seq(_intake_path_value(intake, source))
                     if isinstance(v, str) and v.strip() and not _blank(v)]
        carried = {_fold(v) for v in _seq(_intake_path_value(plan, target)) if isinstance(v, str)}
        dropped = [v for v in collected if _fold(v) not in carried and not excused(field, v)]
        if dropped:
            errors.append(cite(
                "intake.constraints",
                f"the intake recorded {field} {', '.join(repr(v) for v in dropped)} and the plan "
                f"does not carry it at {'.'.join(target)}. This is the traveller's own statement of "
                f"what can hurt them; copy it in (new_plan_skeleton.py --from-intake does), or, "
                f"when they changed it after the form, record that in trip.intake_changes with "
                f"their reason."))

    source, target = INTAKE_CONSTRAINT_FIELDS["traveler_count"]
    wanted, have = _intake_path_value(intake, source), _intake_path_value(plan, target)
    if isinstance(wanted, int) and not isinstance(wanted, bool) and wanted > 0 \
            and have != wanted and not excused_figure("traveler_count", wanted, have):
        errors.append(cite(
            "intake.constraints",
            f"the intake says {wanted} traveller(s) and trip.traveler_count is {have!r}. Rooms, "
            f"fares and every per-person figure follow this number; fix it, or record the change "
            f"in trip.intake_changes with the reason.{stale('traveler_count')}"))

    source, target = INTAKE_CONSTRAINT_FIELDS["cap_per_person"]
    cap = _intake_path_value(intake, source)
    if isinstance(cap, (int, float)) and not isinstance(cap, bool) and cap > 0:
        intake_currency = str(_obj(intake.get("budget")).get("currency") or "").strip().casefold()
        plan_currency = str(_obj(plan.get("trip")).get("currency") or "").strip().casefold()
        if intake_currency and plan_currency and intake_currency != plan_currency:
            notes.append(
                f"note: the intake's cap is in {intake_currency.upper()} and the plan is in "
                f"{plan_currency.upper()}, so budget.cap_per_person was not compared with it.")
        elif abs(_num(_intake_path_value(plan, target)) - float(cap)) > 0.005 \
                and not excused_figure("cap_per_person", cap, _intake_path_value(plan, target)):
            errors.append(cite(
                "intake.constraints",
                f"the intake's per-person cap is {cap:g} and budget.cap_per_person is "
                f"{_intake_path_value(plan, target)!r}. The cap is what the over-budget check "
                f"compares against; carry it, or record the change in trip.intake_changes."
                f"{stale('cap_per_person')}"))


def _intake_entry_findings(intake: dict, plan: dict, errors: list[str]) -> None:
    """The intake knows whether this trip leaves the country; the plan alone cannot say.

    The template tells a domestic trip to delete entry_context, so an absent block reads the same
    as a block nobody wrote. The form separates the two: a traveller staying home answers
    `not_applicable_domestic` for passport validity, and one who has to apply for a visa sets
    entry_assessment_required. Either other answer means a border, and a border means the page owes
    the traveller its entry conclusion.
    """
    feasibility = _obj(intake.get("feasibility"))
    passport = str(feasibility.get("passport_validity_status") or "").strip()
    leaves = feasibility.get("entry_assessment_required") is True or \
        bool(passport and passport != "not_applicable_domestic")
    if leaves and not isinstance(plan.get("entry_context"), dict):
        errors.append(cite(
            "entry.answer",
            f"the intake says this trip leaves the traveller's country of residence "
            f"(passport_validity_status={passport or None!r}, entry_assessment_required="
            f"{feasibility.get('entry_assessment_required')!r}) and the plan carries no "
            f"entry_context. The entry conclusion is what decides whether they board; put it on "
            f"the page with its basis, source and date."))


@cites
def check_preferences_came_from_the_intake(plan: dict, errors: list[str],
                                           notes: list[str]) -> None:
    """What the form collected must reach the plan, checked against the form's own file.

    check_preference_coverage holds every ranked must-have to an anchor that answers it -- and it
    iterates `ranked_must_haves`, so an empty list produces nothing. Its own docstring blesses that
    as a positive claim: the traveller stated no must-have. Measured on a real workspace of fifteen
    saved plans, `ranked_must_haves` is empty on ALL FIFTEEN, so the whole check has never once
    fired, and with it every rule downstream -- satisfies_preference quoting the traveller's own
    words, unmet_preferences carrying a reason -- was unreachable.

    The obvious reading is that those travellers stated no must-have. The intake files say
    otherwise: SEVEN of the fifteen intakes in that same workspace carry a non-empty
    experience.ranked_must_haves, and not one plan does. The form asked, the traveller answered, and
    the answer stopped at the plan boundary -- which is the defect SKILL.md's "the plan must carry
    what the traveller asked FOR" section was written about, surviving the gate written to prevent
    it. A gate that binds only what the author chose to transcribe cannot see a transcription that
    did not happen; it needs the other document.

    A NOTE and not an error when the intake cannot be read, and that asymmetry is deliberate. This
    repo treats a plan as a portable document -- re-rendered, replanned weeks later, audited from a
    moved workspace, restored from backup -- and render_final_trip_html.intake_context_errors
    records why requiring `intake_file` to resolve was tried and reverted: it failed every
    legitimate re-save, and the way out the error suggested was to relabel the intake method, i.e.
    to write something false. So an unreadable intake costs the cross-check, never the plan.
    """
    context = _obj(plan.get("intake_context"))
    path = context.get("intake_file")
    if not isinstance(path, str) or not path.strip() or _blank(path):
        return

    # SECURITY. `path` is a string out of the plan, and a plan is a document this repo deliberately
    # treats as portable -- re-rendered, replanned, audited from a moved workspace, and therefore
    # sometimes received from somebody else. Opening whatever it names turned that into an
    # arbitrary local file read: the note below reports the OS error verbatim, which distinguishes
    # "no such file" from "permission denied" and makes this an existence oracle for any path, and
    # a target that happens to parse as a JSON object with experience.ranked_must_haves gets its
    # strings echoed into the gate's own findings.
    #
    # Scoped by FILENAME, not by directory. run_plan_checks takes a plan and not a path, so no
    # absolute root is available here without changing a signature save_trip_deliverables imports
    # -- and the directory could not be constrained anyway, because --from-intake accepts any file
    # the operator names: the first version of this fix demanded a parent named `plans` and broke
    # the repo's own fixtures. The filename is enough, because nothing worth stealing is called
    # `intake*.json`. /etc/passwd, ~/.ssh/id_rsa, ~/.aws/credentials and /proc/self/environ are all
    # refused, while every real intake -- including one in a workspace that moved, which is the
    # case the note below exists for -- still reads. `is_file()` additionally refuses a FIFO, which
    # would otherwise hang this gate forever.
    candidate = Path(path).expanduser()
    if not (candidate.name.startswith("intake") and candidate.suffix == ".json"):
        notes.append(
            f"note: intake_context.intake_file ({path.strip()}) was NOT opened: this gate only "
            f"reads a file named intake*.json. A plan can be shared or hand-edited, so a path it "
            f"names is a request rather than an instruction. The preference cross-check did not "
            f"run; rename the intake, or point the key at the file the form actually saved.")
        return
    if not candidate.is_file():
        notes.append(
            f"note: intake_context.intake_file ({path.strip()}) is not a regular file, so the "
            f"preference cross-check did not run.")
        return
    try:
        intake = json.loads(candidate.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        notes.append(
            f"note: intake_context.intake_file ({path.strip()}) could not be read ({exc}), so the "
            f"plan's ranked_must_haves were not checked against what the form actually collected. "
            f"Not an error -- a plan outlives the workspace it was built in -- but this run did "
            f"not verify that the traveller's own answers reached the plan.")
        return
    if not isinstance(intake, dict):
        notes.append(f"note: intake_context.intake_file ({path.strip()}) is not a JSON object, so "
                     f"the preference cross-check did not run.")
        return

    collected = [str(m).strip() for m in _seq(_obj(intake.get("experience")).get("ranked_must_haves"))
                 if isinstance(m, str) and m.strip() and not _blank(m)]
    preferences = _obj(_obj(plan.get("trip")).get("traveler_preferences"))
    carried = {_fold(str(m)) for m in _seq(preferences.get("ranked_must_haves"))
               if isinstance(m, str) and m.strip()}
    dropped = [m for m in collected if _fold(m) not in carried]
    if dropped:
        errors.append(
            f"the intake collected {len(collected)} ranked must-have(s) and the plan carries "
            f"{len(collected) - len(dropped)}. Missing: {'; '.join(repr(m) for m in dropped)}. "
            f"These are the traveller's own answers to what the trip is FOR, and every rule that "
            f"reads them -- an anchor pointing at each through satisfies_preference, an unmet one "
            f"carrying its reason -- iterates this list, so dropping an entry does not fail those "
            f"rules, it deletes them. Copy each into trip.traveler_preferences.ranked_must_haves in "
            f"the traveller's own words (new_plan_skeleton.py --from-intake does it), or, where the "
            f"season or the place genuinely cannot deliver one, carry it and say so in "
            f"unmet_preferences.")

    # The must-haves used to be the whole of this check, and it returned as soon as they were
    # settled -- so the constraints below have to run whatever the must-haves said.
    _intake_constraint_findings(intake, plan, errors, notes)
    _intake_entry_findings(intake, plan, errors)




def check_verification_tier_is_stated(plan: dict, errors: list[str], notes: list[str]) -> None:
    """Say which verification tier this plan qualifies for, BEFORE anyone pays for one.

    SKILL.md tells the author, about the light/full choice: "check_plan_consistency.py computes
    this from the plan's own fields, so do not argue with it -- read what it printed." That
    sentence was not true. `required_domains_for` has exactly one call site, inside
    check_verification, and check_verification is not in PLAN_CHECKS -- it runs only when a
    finished verification report is passed in. So the tier was computed after the verification had
    already been bought, and the decision it exists to settle was made without it.

    The cost of that is one-sided and large. The full pass is five truth domains plus two auditors;
    the light one is four blocks. references/research-budget.md prices the difference at roughly
    300k against 700k. Left to judgement, the answer is whatever the author feels thorough enough
    to say -- and measured across fifteen real saved plans, every single one computes `full`, so
    nobody has ever been told they could have stopped at four.

    A note and not an error, because there is nothing here to be wrong about: the plan's own fields
    decide, this function only reads them out. It is the same move as everything else in this gate
    -- do not ask the author to declare something the artifact already answers; print the answer
    where the decision is made.
    """
    if not isinstance(plan, dict) or not plan.get("days"):
        return
    required, reason = required_domains_for(plan)
    tier = "light" if required <= LIGHT_TIER_DOMAINS else "full"
    blocks = sorted(required) + sorted(REQUIRED_AUDITS)
    notes.append(
        f"verification tier: {tier.upper()} -- {len(blocks)} block(s): {', '.join(blocks)}. "
        f"{reason} Computed from this plan's own fields before any verification is bought; "
        f"references/research-budget.md prices the difference between the tiers, so this is the "
        f"cheapest sentence in the run to read.")



def check_dates_agree_with_the_gates_that_ran(plan: dict, errors: list[str],
                                              notes: list[str]) -> None:
    """A delivered plan whose dates moved since its gates ran, with nothing saying they moved.

    check_replan_context is the gate for a date change, and it opens with `if context is None:
    return` -- so it never sees the case it exists for. `replan_trip.py` writes replan_context;
    an author who edits two date strings by hand writes nothing, and every weekday-keyed fact in
    the plan quietly becomes a guess: opening hours, closure days, market days, the museum that
    shuts Mondays. SKILL.md records the measured cost twice -- a one-day shift redone by hand put
    an off-by-one in every ticket and every anchor day index.

    Asking the author to declare the edit cannot work, because not declaring it IS the edit. So
    this reads the receipt instead. save_trip_deliverables.py stamps the window the checks ran
    against into `gates_passed`, before it rewrites the stamp, so a plan that was delivered and
    then hand-edited disagrees with its own record.

    Three ways this deliberately stays quiet, because a check that accuses honest work gets routed
    around:

      * No stamp at all -- a plan that has never been delivered has nothing to disagree with, and
        a freshly authored one must not be told its dates are wrong.
      * A stamp that predates this field. The fifteen plans in a real workspace carry `gates_passed`
        on one of them, written before the window was recorded; it has no start_date, so it is not
        evidence either way and produces nothing.
      * replan_context present. That is the declaration this check exists to notice the absence of,
        and check_replan_context then holds the plan to every entry it raised. replan_trip.py also
        clears gates_passed outright, so a legitimate shift has no stamp to compare against for a
        second, independent reason.
    """
    stamp = _obj(plan.get("gates_passed"))
    if not stamp:
        return
    trip = _obj(plan.get("trip"))
    if plan.get("replan_context") is not None:
        return
    for field, label in (("start_date", "start"), ("end_date", "end")):
        was = stamp.get(field)
        now = trip.get(field)
        if not isinstance(was, str) or not was.strip():
            continue
        if not isinstance(now, str) or not now.strip():
            continue
        if was == now:
            continue
        errors.append(
            f"trip.{field} is {now} but the gates that stamped this plan ran on {was}. The "
            f"{label} of the window moved after the plan was delivered and nothing records it: "
            f"opening hours, closure days and market days are keyed to the WEEKDAY, so every one "
            f"of them is now a guess while the plan still reads as checked. Shift it with "
            f"`python scripts/replan_trip.py <plan.json> --shift-days N --out <new.json>`, which "
            f"rewrites what is a pure function of the delta and lists the rest in "
            f"replan_context.must_reverify -- or, if the dates were re-researched by hand, say so "
            f"in replan_context so this gate can hold you to each entry.")


@cites
def check_self_transfer_consent(plan: dict, errors: list[str], notes: list[str]) -> None:
    """A separate-ticket connection is the traveller's risk to take, in their own words.

    kiwi_flights.py excludes self-transfer unless asked, and marks a leg `self_transfer: true` when
    the traveller accepted it. A missed connection on separate tickets is nobody's problem but
    theirs -- no rebooking, bags to collect, check-in to redo -- so a marked leg needs
    trip.traveler_preferences.accepts_self_transfer to hold their words, not a placeholder.
    """
    consent = _obj(_obj(_obj(plan.get("trip")).get("traveler_preferences"))).get("accepts_self_transfer")
    consented = isinstance(consent, str) and bool(consent.strip()) and not _unfilled(consent)
    for option in [_obj(o) for o in _seq(_obj(plan.get("booking_options")).get("flights"))]:
        label = str(option.get("provider") or option.get("id") or "?")
        for leg in ("outbound_itinerary", "return_itinerary"):
            value = _obj(option.get(leg)).get("self_transfer")
            if value is None:
                continue
            if not isinstance(value, bool):
                errors.append(f"flight '{label}' {leg}.self_transfer is {value!r}; it must be true, false or absent.")
            elif value and not consented:
                errors.append(
                    f"flight '{label}' {leg} is a self-transfer (separate tickets), but "
                    f"trip.traveler_preferences.accepts_self_transfer does not hold the traveller's own "
                    f"words accepting that. Ask them and record their words, or choose a protected itinerary.")


@cites
def check_bookings(plan: dict, errors: list[str], notes: list[str]) -> None:
    """The traveller's recorded decisions name real options, one per group, with honest dates.

    The rules live in scripts/bookings.py so the renderer, the page gate and record_booking.py ask
    the same ones. Today is the machine's: a booking cannot be dated after it. A decided stay also
    means no day may still send the traveller to a sibling hotel of that stay.
    """
    errors.extend(booking_rules.record_problems(plan, dt.date.today()))
    errors.extend(booking_rules.stale_stay_mentions(plan))


@cites
def check_time_zones(plan: dict, errors: list[str], notes: list[str]) -> None:
    """Every zone the plan names is a real IANA zone, every leg of a multi-zone trip names both its
    zones, and every leg's zones agree with its duration_minutes.

    The rules live in scripts/trip_zones.py so plan_to_calendar.py writes UTC from the same answers.
    """
    errors.extend(trip_zones.zone_problems(plan))
    notes.extend(trip_zones.zone_notes(plan))


PLAN_CHECKS = (
    check_entry_covers_every_jurisdiction,
    check_verified_plan_entry_answer,
    check_stay_groups_do_not_overlap,
    check_rooms_hold_the_party,
    check_verification_tier_is_stated,
    check_dates_agree_with_the_gates_that_ran,
    check_preferences_came_from_the_intake,
    check_routes,
    check_walking_budget,
    check_implied_speed,
    check_map_link_modes,
    check_clock_closure,
    check_day_internals,
    check_cross_references,
    check_dates,
    check_accommodation_coverage,
    check_dining,
    check_meal_reachability,
    check_budget,
    check_replan_context,
    check_list_typed_fields,
    check_prose_rendering,
    check_prose_agrees_with_data,
    check_map_endpoints,
    check_venue_quality,
    check_booking_identity,
    check_service_market,
    check_preference_coverage,
    check_prose_texture,
    check_sentinel_timestamps,
    # Next to check_sentinel_timestamps on purpose: both refuse a value new_plan_skeleton.py wrote
    # because it could not know the answer, and both are safe here only because they fire on the
    # sentinel rather than on the field it stands in for.
    check_untyped_constraints,
    check_ticket_sale_windows,
    check_self_transfer_consent,
    check_bookings,
    check_time_zones,
)


# ----------------------------------------------------------------------------------------------
# What gets PRINTED, and how many times the same sentence gets printed.
#
# Measured on plans/2026-09-09-tokyo-5d4n.json with --no-verification-yet, at the commit before
# this one: 122 findings in 48,841 bytes of output, and the same handful of rule rationales was
# most of it -- the top one re-printed 48 times, and the `[see references/...]` citations added in
# the previous commit had become the single most repeated string in the file. The gate loop runs
# this script once per fix cycle, so every repeat is paid again on every cycle.
#
# The fix is NOT to collapse findings into bare pointers. What an author acts on is each finding's
# own HEAD -- which venue, which value, which two strings disagree -- and replacing that with "see
# rule 7" sends them back into the plan to rediscover what the gate already knew, which costs more
# than it saves. So every finding keeps its own dashed line and its own instance text verbatim;
# only the repeated TAIL is suppressed, and only after the rule has been stated in full once.
#
# Nothing below decides WHETHER a finding fires. It is all presentation, and the finding set is
# byte-identical to what the checks produced.


class FindingLog(list):
    """The findings list, plus a record of the source line each finding was appended from.

    It is a `list` everywhere that matters: `cites()` type-checks `isinstance(args[1], list)`,
    save_trip_deliverables.py builds a plain list and hands it to these same checks, and every
    check appends to it exactly as before. The only thing added is a parallel note of WHERE each
    string came from, which is what lets the printer tell a rule's fixed rationale from the part
    of the message that is about this venue on this day.

    Reading the site off the stack rather than asking each check to name its rule is deliberate,
    and it is the same argument cites() makes two hundred lines up about citations. Not one of
    this file's many `errors.append(...)` sites carries a rule id; adding one to each is a chance
    to paste the wrong id at every site, it covers only the sites that exist today, and -- worst
    -- it would edit the finding strings themselves, which is the one thing this change must not
    do. A stack frame cannot drift out of date with the code it points at.

    `extend` is overridden as well as `append` because check_verification merges whole lists in
    (`errors.extend(_claims_pointer_errors(...))`). Without it those findings would have no site
    and the two lists would fall out of step, silently mis-attributing every finding after them --
    the sites list must stay exactly as long as self or the attribution is nonsense rather than
    absent, and nonsense is the failure this file exists to refuse.
    """

    def __init__(self, *args) -> None:
        super().__init__(*args)
        self.sites: list[tuple[str, int] | None] = []
        self.checks: list[str] = []
        # Set by the caller around each check, so a finding can be attributed to the check that
        # produced it without wrapping PLAN_CHECKS (which would break the identity assertions in
        # tests/test_plan_consistency.py for the same reason cites() decorates at the `def`).
        # A finding appended outside any check keeps the empty string.
        self.current_check = ""

    def _site(self, depth: int) -> tuple[str, int] | None:
        try:
            frame = sys._getframe(depth)
        except (AttributeError, ValueError):  # pragma: no cover - non-CPython, or too shallow
            # An interpreter without frame introspection loses the exact split and falls back to
            # the estimate below. It must not lose the findings, so this is None, not an error.
            return None
        return (frame.f_code.co_filename, frame.f_lineno)

    def append(self, item) -> None:
        # depth 2: 0 is _site, 1 is this method, 2 is the check that called append.
        self.sites.append(self._site(2))
        self.checks.append(self.current_check)
        super().append(item)

    def extend(self, items) -> None:
        # Materialised first: a generator consumed by super().extend() would leave the site and
        # check lists short by however many items it yielded.
        items = list(items)
        site = self._site(2)
        for _ in items:
            self.sites.append(site)
            self.checks.append(self.current_check)
        super().extend(items)


@functools.lru_cache(maxsize=8)
def _emission_templates(filename: str) -> dict[int, tuple[int, str | None]]:
    """Source line -> (the line the append starts on, the trailing string literal written there).

    That trailing literal is the rule's own words. An f-string's constant parts are the sentence
    the author wrote and its `{}` holes are the only instance-specific part, so the literal that
    ENDS the expression is exactly the rationale that repeats. Recovering it from the source is
    what makes the head/tail split exact rather than guessed.

    The alternative -- taking the longest common suffix of the findings one site produced -- was
    built first and measurably eats instance text. On the Tokyo plan it cut the venue-link rule at
    the two characters every venue name in that group happened to end with, leaving a dashed line
    that no longer named the venue: precisely the "bare pointer" failure this whole change is
    against. That estimate survives below as the fallback for the few sites whose message is not a
    single f-string, where nothing better is available.

    Every line of a multi-line call maps to the same entry, because a frame's line number is the
    line the call expression starts on under some interpreters and the line being executed under
    others, and this must not depend on which.

    Returns {} rather than raising when the source cannot be read or parsed -- a zipped skill, a
    .pyc-only install, a syntax error introduced by an editor mid-save. The printer then falls
    back to the estimate, which is fatter but still correct. A lint that refuses to run because it
    could not read its own source would be a far bigger outage than a fatter report.
    """
    try:
        source = Path(filename).read_text(encoding="utf-8")
        tree = ast.parse(source, filename=filename)
    except (OSError, SyntaxError, ValueError, UnicodeDecodeError):  # pragma: no cover
        return {}

    index: dict[int, tuple[int, str | None]] = {}
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        if not (isinstance(func, ast.Attribute) and func.attr in ("append", "extend")
                and isinstance(func.value, ast.Name) and func.value.id == "errors"):
            continue
        trailing = _trailing_literal(node.args[0]) if len(node.args) == 1 else None
        for line in range(node.lineno, (node.end_lineno or node.lineno) + 1):
            index.setdefault(line, (node.lineno, trailing))
    return index


def _trailing_literal(expression: ast.AST | None) -> str | None:
    """The constant text an appended message ends with, or None when it does not end in one.

    None is a real answer and has to stay one. `errors.append(f"...{tail_chosen_above}")` ends in
    a hole, and `errors.append("a" + b)` is not an f-string at all; guessing a literal for either
    would put instance text into the rules table, where it would be printed once and dropped from
    every other finding that fired the same rule. The caller falls back to the estimate instead.
    """
    node = expression
    # cite() wraps a message to attach a narrower citation than the check's default; the message
    # is its second argument, so look through it rather than at it.
    while (isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
           and node.func.id == "cite" and len(node.args) > 1):
        node = node.args[1]
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    if isinstance(node, ast.JoinedStr) and node.values:
        last = node.values[-1]
        if isinstance(last, ast.Constant) and isinstance(last.value, str):
            return last.value
    return None


def _estimated_tails(messages: list[str]) -> list[str]:
    """A tail per message for a group whose source template could not be read.

    Only suffixes that begin at a WORD START are considered, and that is the whole safety of the
    estimate. The raw longest common suffix splits mid-word: findings about venues whose names all
    end "店）" share those two characters, so the shared part begins inside the venue name and the
    head that survives no longer says which venue -- the bare-pointer failure, arrived at from the
    other direction. A whitespace boundary means every head ends on a whole word, so anything
    unique to one finding stays on that finding's own line. A message with no whitespace at all
    (a Chinese sentence) therefore shares nothing rather than being cut inside a name.

    Greedy by bytes saved: repeatedly take the word-aligned suffix with the highest
    (occurrences - 1) * length, assign it to every message that ends with it, and look again at
    what is left. One site can emit two different sentences -- a branch that picks one of two
    rationales before interpolating it -- and a single common suffix over the whole group would
    collapse to the citation alone, so the clusters have to be found rather than assumed.

    Messages with nothing to share get "": the caller prints those in full, which is what the
    output did before any of this existed.
    """
    tails = [""] * len(messages)
    remaining = set(range(len(messages)))
    while len(remaining) > 1:
        counts: dict[str, list[int]] = {}
        for index in remaining:
            message = messages[index]
            seen: set[str] = set()
            # Only the tail end of each message is a candidate. Every word start would make the
            # candidate set quadratic in message length, and one check here already emits a
            # kilobyte-and-a-half finding with a list embedded in it -- enough for a lint to
            # start allocating megabytes over a report nobody reads. Nothing in this file writes
            # a rationale anywhere near this long, so the bound costs no real dedupe.
            first = max(0, len(message) - _MAX_ESTIMATED_TAIL)
            for position in range(first, len(message)):
                if position and not message[position - 1].isspace():
                    continue
                suffix = message[position:]
                if suffix not in seen:
                    seen.add(suffix)
                    counts.setdefault(suffix, []).append(index)
        best: tuple[int, int, str] | None = None
        for suffix, owners in counts.items():
            if len(owners) < 2:
                continue
            # Ties broken by length then by the text itself, so two runs of the same input print
            # the same bytes -- a report that reorders itself cannot be diffed across a fix.
            score = (len(owners) - 1) * len(suffix)
            candidate = (score, len(suffix), suffix)
            if best is None or candidate > best:
                best = candidate
        if best is None:
            break
        suffix = best[2]
        owners = counts[suffix]
        for index in owners:
            tails[index] = suffix
            remaining.discard(index)
    return tails


class Finding:
    """One finding, split into what it says about this instance and what its rule says.

    `head + tail` is the original string, byte for byte. That invariant is the whole defence
    against this becoming a summary: nothing is reworded, nothing is dropped, and a reader given
    the head and the rules table can reconstruct exactly what the old output printed.
    """

    __slots__ = ("message", "rule_id", "head", "tail")

    def __init__(self, message: str, rule_id: str, head: str, tail: str) -> None:
        self.message = message
        # The check name is the rule id's prefix rather than a field of its own: one place for it
        # means the two cannot disagree, and a second copy would only ever be read to confirm the
        # first.
        self.rule_id = rule_id
        self.head = head
        self.tail = tail


def split_findings(findings: list[str],
                   sites: list[tuple[str, int] | None] | None = None,
                   checks: list[str] | None = None) -> list[Finding]:
    """Attach a rule id to every finding and cut off the part of it that is the rule.

    Accepts a plain list -- callers that did not use a FindingLog, and older tests -- and then
    falls back to the estimate for everything, so this is never the reason a report fails to
    print.

    Two sites that end in the same sentence get the same rule id: same words, same rule, and the
    reader should not be told twice that they need to read it. Sites in different checks stay
    apart even then, because the check name is what the citation and the worklist are keyed on.
    """
    count = len(findings)
    sites = list(sites) if sites is not None else [None] * count
    checks = list(checks) if checks is not None else [""] * count
    # A short sites/checks list would silently mis-attribute every finding past the end rather
    # than fail, and mis-attribution here means printing one rule's rationale under another's id.
    if len(sites) != count or len(checks) != count:
        raise ValueError(
            f"split_findings got {count} findings but {len(sites)} site(s) and {len(checks)} "
            f"check name(s). They are parallel lists; a mismatch means some finding would be "
            f"printed under another finding's rule.")

    groups: dict[tuple[str, object], list[int]] = {}
    for index in range(count):
        site = sites[index]
        anchor: object = None
        if site is not None:
            anchor = _emission_templates(site[0]).get(site[1], (site[1], None))[0]
        groups.setdefault((checks[index], anchor), []).append(index)

    tails: list[str] = [""] * count
    for (_check, _anchor), members in groups.items():
        site = sites[members[0]]
        template = None
        if site is not None:
            template = _emission_templates(site[0]).get(site[1], (0, None))[1]
        cuts = [_template_cut(findings[index], template) for index in members] if template else []
        if template and all(cut is not None for cut in cuts):
            for index, cut in zip(members, cuts):
                tails[index] = findings[index][cut:]
            continue
        for index, tail in zip(members, _estimated_tails([findings[i] for i in members])):
            tails[index] = tail

    split: list[Finding] = []
    for index in range(count):
        tail = tails[index][_closing_punctuation(tails[index]):]
        check = checks[index] or "check"
        # A tail is the rule, so identical tails are one rule. With no tail there is nothing to
        # hash, and the site stands in -- those findings are printed whole anyway, so the id only
        # has to be unique within the run, not stable across edits.
        material = tail if tail else f"@{sites[index]!r}"
        rule_id = f"{check}#{hashlib.sha1(material.encode('utf-8')).hexdigest()[:8]}"
        head = findings[index][:len(findings[index]) - len(tail)] if tail else findings[index]
        split.append(Finding(findings[index], rule_id, head, tail))
    return split


def _closing_punctuation(tail: str) -> int:
    """How many characters at the front of `tail` belong to the head instead.

    A template's trailing literal starts wherever the last `{}` hole ended, which is usually just
    INSIDE the punctuation that closes the value: the dining rule's literal begins "' has no
    venue_hours", so cutting there leaves a head ending on an unclosed quote and a rule that opens
    with a stray one. Moving a leading run of punctuation back to the head fixes both.

    Only a run of non-alphanumeric characters, and only when whitespace (or the end) follows it,
    so this can never move a word. "_url. Two options..." keeps its "_url." on the rule side
    because a letter follows the underscore, which is the case that makes a naive "move the
    punctuation" rule eat half a field name. CJK counts as alphanumeric to str.isalnum(), so a
    Chinese rationale is never mistaken for punctuation.
    """
    length = 0
    while length < len(tail) and not tail[length].isalnum() and not tail[length].isspace():
        length += 1
    if length and (length == len(tail) or tail[length].isspace()):
        return length
    return 0


def _template_cut(message: str, template: str) -> int | None:
    """Where `template` starts in `message`, or None if this message did not come from it.

    Searched in the message MINUS its citation, because the citation is appended after the
    f-string was rendered and is full of dots and slashes: a one-character template like "." would
    otherwise match inside `references/booking-html-output.md` and cut the message in the middle
    of its rationale. Anchored with endswith rather than a search, so a template that matches
    anywhere other than the very end of the rendered message is refused instead of guessed at.
    """
    cut = message.rfind(_CITED)
    body = message[:cut] if cut >= 0 else message
    if not template or not body.endswith(template):
        return None
    return len(body) - len(template)


# The longest tail the estimate will look for; see _estimated_tails.
_MAX_ESTIMATED_TAIL = 2000

# The tags that carry a rule from its first finding to the rest. Two different strings on purpose:
# a reader who lands in the middle of the output and wants the rule can search for "R7, stated
# here" and land on the one line that states it, which a single shared tag would not give them.
_RULE_STATED_HERE = "[rule {tag}, stated here]"
_RULE_STATED_ABOVE = "[rule {tag}, stated above]"
_DEDUPE_LEGEND = (
    'Rules are stated once. A finding tagged "[rule R1, stated here]" carries that rule\'s full '
    'wording; later findings of the same rule print what is specific to them and carry '
    '"[rule R1, stated above]" instead. Search for "R1, stated here" to read the rule. '
    'Pass --json for the same findings with each rule listed once and a pointer per finding.'
)


def format_findings(split: list[Finding]) -> tuple[list[str], list[str]]:
    """(legend lines, one line per finding) for the failure block, rule rationales stated once.

    Every finding keeps its own line and its own instance text. Only a rule that fired more than
    once is deduplicated, and only when suppressing its tail actually saves more than the
    back-reference costs -- otherwise the finding prints exactly the bytes it printed before.

    A finding whose head is blank is left whole as well, and the test is made per finding rather
    than per rule. That happens when the rule's message has no interpolation at all, so the head
    would be nothing but a tag and the reader would learn less than the old output told them.

    A report where the whole scheme would not pay for itself prints byte-for-byte what it printed
    before the scheme existed. A two-finding plan repeating one rule saves one tail and spends the
    legend explaining how to read it, which came out 60 bytes WORSE on a real workspace plan --
    and a "saving" that can make the output bigger is one nobody can reason about.
    """
    # Suppressing a tail is only worth it if the tail is longer than the back-reference that
    # replaces it. Sized from the tags themselves rather than from numbers somebody picked, so
    # they stay true if the wording changes.
    repeat_cost = len(_RULE_STATED_ABOVE.format(tag="R99")) + 1
    state_cost = len(_RULE_STATED_HERE.format(tag="R99")) + 1
    legend_cost = len(_DEDUPE_LEGEND) + 3
    seen: dict[str, int] = {}
    for finding in split:
        seen[finding.rule_id] = seen.get(finding.rule_id, 0) + 1

    tags: dict[str, str] = {}
    for finding in split:
        if finding.rule_id in tags or seen[finding.rule_id] < 2:
            continue
        if len(finding.tail) <= repeat_cost:
            continue
        tags[finding.rule_id] = f"R{len(tags) + 1}"

    saved = -legend_cost if tags else 0
    counted: set[str] = set()
    for finding in split:
        if finding.rule_id not in tags:
            continue
        if finding.rule_id not in counted:
            counted.add(finding.rule_id)
            saved -= state_cost
        elif finding.head.strip():
            saved += len(finding.tail) - repeat_cost
    if saved <= 0:
        tags = {}

    lines: list[str] = []
    stated: set[str] = set()
    for finding in split:
        tag = tags.get(finding.rule_id)
        if tag is None:
            lines.append(finding.message)
        elif finding.rule_id not in stated:
            stated.add(finding.rule_id)
            lines.append(f"{finding.message} {_RULE_STATED_HERE.format(tag=tag)}")
        elif not finding.head.strip():
            lines.append(finding.message)
        else:
            separator = "" if finding.head[-1:].isspace() else " "
            lines.append(f"{finding.head}{separator}{_RULE_STATED_ABOVE.format(tag=tag)}")

    legend = [_DEDUPE_LEGEND] if stated else []
    return legend, lines


# ----------------------------------------------------------------------------------------------
# Where in the plan, not just what.
#
# The prose report tells an author WHAT is wrong and leaves them to open the plan and find WHERE.
# Measured on this workspace: 15 saved plans run from 28,943 to 2,132,252 bytes, median 85,836 --
# roughly 21.5k tokens to re-read a median plan, once per fix cycle, because the finding named a
# venue and not a field. Every pointer below is derived from what the finding itself says and is
# then required to RESOLVE against the plan in hand; one that does not resolve is dropped rather
# than printed, because a pointer into a field that does not exist costs the same read it was
# meant to save and teaches the author to stop trusting the field.

_EXPLICIT_POINTER = re.compile(r"\$\.([^\s'\"]+)")
_LEADING_POINTER = re.compile(r"^([^\s.\[\]]+(?:\[\d+\])*(?:\.[^\s.\[\]]+(?:\[\d+\])*)+)")
_DAY_SEGMENT = re.compile(r"^day (\d+) segment (\d+)\b")
_DAY_ONLY = re.compile(r"^day (\d+)\b")
_QUOTED = re.compile(r"'([^']{2,})'|\"([^\"]{2,})\"")
_IDENTIFIER = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")


def _day_pointer(plan: object, number: str) -> str | None:
    """`days[i]` for the day the message calls "day N", found by the day's own number field.

    Positional guessing (day 3 -> days[2]) is wrong the moment a plan numbers its days from
    anything but 1, or a replan drops a day and leaves the numbers alone. Both are shapes this
    repo has shipped, so the index is looked up rather than assumed.
    """
    for index, day in enumerate(_seq(_obj(plan).get("days"))):
        if str(_obj(day).get("number")) == number:
            return f"days[{index}]"
    return None


def _plan_value_locations(plan: object) -> dict[str, list[str]]:
    """Every string in the plan, mapped to the pointers that hold it.

    This is what turns "the venue link for 'X'" into a field: the finding quotes a value, and the
    plan holds that value in exactly one place often enough to be worth looking. Values held in
    more than one place are kept with all their pointers so the caller can see the ambiguity and
    decline, rather than picking the first and being wrong half the time.

    Short strings are skipped. A two-character value is a status code or a mode, matches
    everywhere, and would only ever produce an ambiguous answer.
    """
    locations: dict[str, list[str]] = {}

    def walk(node: object, pointer: str) -> None:
        if isinstance(node, dict):
            for key, value in node.items():
                # A key holding a dot or a bracket cannot be written in the pointer syntax
                # resolve_pointer accepts, so its subtree is left out rather than given a path
                # that would not resolve. Fewer pointers, never a wrong one.
                if isinstance(key, str) and not set("[].").intersection(key):
                    walk(value, f"{pointer}.{key}" if pointer else key)
        elif isinstance(node, list):
            for index, value in enumerate(node):
                walk(value, f"{pointer}[{index}]")
        elif isinstance(node, str) and len(node) > 2 and pointer:
            locations.setdefault(node, []).append(pointer)

    walk(plan, "")
    return locations


def _refine_to_named_field(plan: object, pointer: str, text: str) -> str:
    """Append the one field of `pointer`'s object that `text` names, if there is exactly one.

    "origin='...' is free text" names `origin`, and pointing at the field beats pointing at the
    segment that holds it. Exactly one, because a message that names two fields does not say
    which one is wrong, and a pointer that picks the wrong one of two sends the author to a field
    that is fine -- worse than the coarser pointer it replaced.
    """
    node: object = plan
    for part in pointer.split("."):
        step = _POINTER_STEP.match(part)
        if not step or not isinstance(node, dict):
            return pointer
        node = node.get(step.group(1))
        for index in _POINTER_INDEX.findall(step.group(2)):
            if not isinstance(node, list) or int(index) >= len(node):
                return pointer
            node = node[int(index)]
    if not isinstance(node, dict):
        return pointer
    words = set(_IDENTIFIER.findall(text))
    named = [key for key in node if isinstance(key, str) and key in words]
    return f"{pointer}.{named[0]}" if len(named) == 1 else pointer


def pointer_for(text: str, plan: object, values: dict[str, list[str]] | None = None) -> str | None:
    """A path into this plan for the thing the finding is about, or None if it does not name one.

    None is a first-class answer and the caller prints it as such. An author who cannot tell "this
    gate could not name a location" from "somebody forgot the field" is back to reading the whole
    plan, which is the cost this exists to remove.

    Candidates run most specific first and each one must resolve against the plan before it is
    used. The value-derived candidate is additionally required to sit under the day the finding
    names: an exact string match somewhere else in the plan contradicts the finding's own words,
    and the finding's words win.
    """
    if not isinstance(text, str) or not text:
        return None

    explicit = _EXPLICIT_POINTER.search(text)
    if explicit:
        # A pointer quoted mid-sentence carries the sentence's punctuation with it. No pointer
        # ends in one of these, so trimming them cannot shorten a real path.
        quoted = explicit.group(1).rstrip(".,;:)")
        if resolve_pointer(plan, quoted):
            return quoted

    base: str | None = None
    leading = _LEADING_POINTER.match(text)
    if leading and resolve_pointer(plan, leading.group(1)):
        base = leading.group(1)
    if base is None:
        day_segment = _DAY_SEGMENT.match(text)
        day_only = _DAY_ONLY.match(text)
        if day_segment:
            day = _day_pointer(plan, day_segment.group(1))
            candidate = f"{day}.route.segments[{int(day_segment.group(2)) - 1}]" if day else None
            if candidate and resolve_pointer(plan, candidate):
                base = candidate
            elif day and resolve_pointer(plan, day):
                base = day
        elif day_only:
            day = _day_pointer(plan, day_only.group(1))
            if day and resolve_pointer(plan, day):
                base = day

    if values is None:
        values = _plan_value_locations(plan)
    for match in _QUOTED.finditer(text):
        quoted = match.group(1) or match.group(2)
        held = values.get(quoted)
        if not held or len(held) != 1:
            continue
        owner = held[0].rsplit(".", 1)[0] if "." in held[0] else held[0]
        if base is not None and not owner.startswith(base):
            continue
        if resolve_pointer(plan, owner):
            return _refine_to_named_field(plan, owner, text)

    if base is not None:
        return _refine_to_named_field(plan, base, text)
    return None


def json_report(split: list[Finding], notes: list[str], plan: object,
                ok: bool, extra: dict | None = None) -> str:
    """The same findings, addressed to a model that would otherwise re-read the plan to place them.

    `message` is the finding's own instance text and `rules[rule_id]` is its rule, stated once for
    however many findings hit it -- verbatim, including the citation. Concatenating them gives
    back the exact line the prose report prints, which is the property that keeps this from
    quietly becoming a summary: the reasoning is what lets a reader generalise to the case the
    rule never enumerated, so it is carried, not compressed.

    `notes` rides along because the prose report prints notes and one of them is the NOT VERIFIED
    warning. A --json mode that dropped it would let a caller who switched modes call an unchecked
    plan clean, which is the exact disarm this script's own history is made of.
    """
    values = _plan_value_locations(plan) if split else {}
    rules: dict[str, str] = {}
    # Named `entries`, not `findings`: tests/test_packaging.py takes an AST census of every
    # `findings.append(...)` in the two gates that cite per call site and requires each one to be
    # a cite() call. This list holds JSON records rather than findings, and a sink name that lies
    # to that census would either fail it or teach the next person to widen it.
    entries: list[dict] = []
    for finding in split:
        rules.setdefault(finding.rule_id, finding.tail)
        entries.append({
            "rule_id": finding.rule_id,
            "pointer": pointer_for(finding.head or finding.message, plan, values),
            "message": finding.head,
        })
    payload = {"ok": ok, "findings": entries, "rules": rules, "notes": list(notes)}
    if extra:
        payload.update(extra)
    return json_document(payload)


def json_document(payload: dict) -> str:
    """`payload` as JSON with one line per finding and one per rule.

    Measured on the Tokyo plan: 35,663 bytes at indent=2 against 32,736 this way, because a
    pretty-printer spends four lines and twenty spaces of indentation on every finding. A single
    line also means a finding can be quoted, grepped and diffed as a unit, which the one-giant-
    line alternative (32,117 bytes) gives up for another 600.

    Hand-assembled JSON is exactly the kind of thing that ships subtly invalid, so the result is
    parsed before it is returned. A failure falls back to the standard encoder rather than taking
    the gate down -- the caller asked for machine-readable output and must get it -- but says so
    on stderr, because a formatter quietly disagreeing with itself is worth knowing about.
    """
    lines = ["{"]
    items = list(payload.items())
    for position, (key, value) in enumerate(items):
        comma = "," if position < len(items) - 1 else ""
        prefix = f"  {json.dumps(key, ensure_ascii=False)}: "
        if isinstance(value, list) and value:
            body = ",\n".join(f"    {json.dumps(item, ensure_ascii=False)}" for item in value)
            lines.append(f"{prefix}[\n{body}\n  ]{comma}")
        elif isinstance(value, dict) and value:
            body = ",\n".join(
                f"    {json.dumps(name, ensure_ascii=False)}: {json.dumps(item, ensure_ascii=False)}"
                for name, item in value.items())
            lines.append(f"{prefix}{{\n{body}\n  }}{comma}")
        else:
            lines.append(f"{prefix}{json.dumps(value, ensure_ascii=False)}{comma}")
    lines.append("}")
    text = "\n".join(lines)
    try:
        json.loads(text)
    except ValueError as exc:  # pragma: no cover - a formatter bug, not an input problem
        print(f"WARNING: the compact JSON writer produced text json.loads rejected ({exc}); "
              f"falling back to the standard encoder.", file=sys.stderr)
        return json.dumps(payload, ensure_ascii=False, indent=2)
    return text


def json_refusal(rule_id: str, message: str) -> str:
    """A --json body for a run that was refused before it could read the plan.

    A caller that adds --json to every invocation gets JSON from every exit, including the ones
    that used to be a bare stderr line. Anything else makes the flag unusable in a wrapper: the
    one run that fails is the one whose output cannot be parsed.
    """
    return json_document(
        {"ok": False,
         "findings": [{"rule_id": rule_id, "pointer": None, "message": message}],
         "rules": {rule_id: ""},
         "notes": []})


def run_plan_checks(plan: dict) -> tuple[FindingLog, list[str], list[str]]:
    """Run every check over `plan`, surviving a check that raises.

    A crashing check used to take the whole gate down with a traceback, which loses every other
    check's findings and hands the operator a broken tool instead of a plan to fix.
    The traceback is still printed in full -- this is not a swallow -- but the crash is also
    recorded as a finding so it is visible in whichever form the caller asked for, and the caller
    exits 2 rather than 1 so "the gate could not finish" never reads as "the plan is wrong".
    """
    errors = FindingLog()
    notes: list[str] = []
    crashed: list[str] = []
    for check in PLAN_CHECKS:
        errors.current_check = check.__name__
        try:
            check(plan, errors, notes)
        except Exception as exc:  # noqa: BLE001 - reported, not swallowed; see the docstring
            traceback.print_exc(file=sys.stderr)
            crashed.append(check.__name__)
            errors.append(
                f"{check.__name__} raised {type(exc).__name__}: {exc}. The check could not finish, "
                f"so whatever it enforces was NOT enforced on this plan and the findings below are "
                f"incomplete. The traceback is on stderr.")
    errors.current_check = ""
    return errors, notes, crashed


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("plan", help="Plan JSON path")
    parser.add_argument("--verification", default=None,
                        help="Verification report JSON from the parallel-verify stage. Required "
                             "unless --no-verification-yet is passed.")
    parser.add_argument("--no-verification-yet", action="store_true",
                        help="Run the plan checks without a verification report, when the "
                             "parallel-verify stage has not run yet. Prints a banner and records "
                             "the gap instead of leaving a silent exit 0.")
    parser.add_argument("--emit-walking", action="store_true",
                        help="Print computed per-day walking totals and exit 0")
    parser.add_argument("--json", action="store_true",
                        help="Print the findings as JSON on stdout instead of prose on stderr: "
                             "{ok, findings:[{rule_id, pointer, message}], rules:{rule_id: the "
                             "rule's own wording, stated once}, notes}. `pointer` is a path into "
                             "this plan (days[0].dining[1].venue_hours) that has been checked to "
                             "resolve, or null when the finding names no location -- null means "
                             "this gate could not place it, not that the field is missing. Exit "
                             "codes are unchanged. Every exit prints JSON, including the refusals "
                             "above, so a wrapper can parse every run.")
    args = parser.parse_args()

    def refuse(rule_id: str, message: str) -> None:
        """Print a pre-check refusal in whichever form the caller asked for.

        stderr keeps the prose either way. A caller reading stderr for the reason and stdout for
        the JSON gets both, and neither reader has to know which mode the other is in.
        """
        print(message, file=sys.stderr)
        if args.json:
            print(json_refusal(rule_id, message))

    # Same shape as check_shortlist_consistency.py's --intake/--no-intake pair and
    # save_trip_deliverables.py's --verification/--unverified pair, and for the same reason.
    # `--verification` used to default to None, so omitting it exited 0 having run only
    # PLAN_CHECKS -- and check_verification is not in PLAN_CHECKS and has no other call site in
    # this script, so the whole family it owns (required domains present, both audits present,
    # every claims_checked pointer resolving, the report not stale and not bound to another plan)
    # ran nowhere at all. SKILL.md named the bare form in both places it names this script, so the
    # documented invocation WAS the disarmed one, and an exit 0 is what an assistant reads.
    # Measured on plans/2027-02-12-阿利坎特...json: bare 13 findings, the same plan handed a
    # report belonging to another trip 21 -- the 8 that only exist when the flag is supplied.
    # Catching a mis-bound report here rather than at save time is worth a re-verification pass,
    # which references/research-budget.md prices at ~300k (light) to ~700k (full).
    # The escape hatch stays, because a gate people route around warns nobody, but it costs
    # visibility rather than silence.
    #
    # --emit-walking is exempt on purpose: it dumps per-day walking totals and exits before any
    # check runs, so there is no verification for it to skip. Requiring a report to print a data
    # dump would be friction that teaches people to reach for the waiver by reflex, which is how
    # an escape hatch stops meaning anything.
    if not args.emit_walking:
        # An empty string is its own case, and a common one: `--verification "$REPORT"` with the
        # variable unset passes argparse and lands here falsy, i.e. indistinguishable from having
        # asked for nothing. Saying "no --verification" to someone who wrote --verification sends
        # them looking in the wrong place, so name what actually arrived.
        if args.verification is not None and not str(args.verification).strip():
            refuse(
                "cli.empty_verification_path",
                "ERROR: --verification was given an empty path. That is what an unset shell "
                "variable expands to, so the report you meant to pass is not the one that "
                "arrived. Pass the report JSON, or pass --no-verification-yet deliberately.")
            return 1
        # Both flags at once is a contradiction, not a preference order. The shortlist's version
        # silently lets --intake win; here it is refused, because the only way to write both is a
        # caller that appends the waiver unconditionally, and that caller would go on "passing"
        # forever with whatever report it also happened to hand over.
        if args.verification and args.no_verification_yet:
            refuse(
                "cli.contradictory_verification_flags",
                "ERROR: --verification and --no-verification-yet are mutually exclusive. One says "
                "the report exists and the other says it does not. Pass whichever is true.")
            return 1
        if not args.verification and not args.no_verification_yet:
            refuse(
                "cli.missing_verification",
                "ERROR: No --verification. Pass the verification report JSON produced by the "
                "parallel-verify stage in references/verification.md, or pass "
                "--no-verification-yet to run the plan checks without it and record the gap. "
                "Without it the checks that read the report do not run at all: a report missing "
                "a required domain, an audit, or a resolvable pointer -- or one written for a "
                "different plan entirely -- reports clean on exactly the run that motivated "
                "them.")
            return 1

    try:
        plan = json.loads(Path(args.plan).read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001 - surfaced verbatim to the operator
        refuse("cli.unreadable_plan", f"ERROR: could not read plan JSON: {exc}")
        return 2

    if not isinstance(plan, dict):
        refuse("cli.plan_not_an_object",
               f"ERROR: plan JSON must be an object, got {type(plan).__name__}.")
        return 2

    if args.emit_walking:
        # --json is honoured here too rather than refused. A wrapper that appends the flag to
        # every gate call would otherwise get prose from exactly one of them, which is how a
        # caller ends up parsing output it cannot parse.
        walking = []
        for day in [_obj(d) for d in _seq(plan.get("days"))]:
            minutes, km = walking_totals(day)
            on_foot = activity_on_foot_minutes(day)
            walking.append({"day": day.get("number"), "date": day.get("date"),
                            "minutes": minutes, "km": km, "on_foot_minutes": on_foot})
            if args.json:
                continue
            # Appended only when the plan carries it, so the line an existing plan prints is
            # byte-for-byte what it printed before.
            extra = f" (+{on_foot} min on foot inside activities)" if on_foot else ""
            print(f"day {day.get('number')} ({day.get('date')}): {minutes} min / {km} km{extra}")
        if args.json:
            print(json_report([], [], plan, True, extra={"walking": walking}))
        return 0

    errors, notes, crashed = run_plan_checks(plan)

    if args.verification:
        try:
            report = json.loads(Path(args.verification).read_text(encoding="utf-8"))
        except Exception as exc:  # noqa: BLE001
            refuse("cli.unreadable_verification",
                   f"ERROR: could not read verification report: {exc}")
            return 2
        # The plan gets this guard two screens up and the report did not, which mattered because
        # check_verification opens with `_obj(report)`: a report that is a bare list -- a hand-
        # assembled file holding just the domains array, which is the shape people write -- became
        # {} without a word, and every one of its real blocks was then reported as a MISSING
        # domain. Eight findings that all name the wrong problem, on a report whose contents were
        # fine. Name the shape instead; the domains are not missing, the object around them is.
        if not isinstance(report, dict):
            refuse("cli.verification_not_an_object",
                   f"ERROR: verification report JSON must be an object, got "
                   f"{type(report).__name__}. A bare list of domain blocks is not a report -- wrap "
                   f"it as {{\"checked_at\": ..., \"plan\": ..., \"domains\": [...], "
                   f"\"audits\": [...]}}; see templates/verification-report.json.")
            return 2
        errors.current_check = check_verification.__name__
        check_verification(report, errors, notes, plan=plan, plan_path=args.plan,
                           report_path=args.verification)
        errors.current_check = ""
    elif args.no_verification_yet:
        # Printed here, before the notes and before any finding, and printed to stderr as well as
        # carried in notes. Those are two different readers: the note loop below writes to stdout
        # and is where an operator scanning the summary looks, while a caller that keeps only
        # stderr -- which is where this script puts everything that means "not OK" -- would
        # otherwise see a bare "PLAN CONSISTENCY OK". The whole defect being fixed here is that a
        # clean exit 0 reads as "verified", so the waiver has to be unmissable on both streams.
        print("=" * 78, file=sys.stderr)
        print("NOT VERIFIED: --no-verification-yet was passed. No verification report was read.",
              file=sys.stderr)
        # The waiver is, by its own name, the moment the author still owes a report -- so it is the
        # moment to say how one is started. Before this line the chain went straight from here to
        # the renderer, and an assistant following the printed order reached delivery with
        # --unverified having never learned a scaffold existed. Every plan in the author's
        # workspace took exactly that path: seventeen delivered, zero surviving reports.
        print(f"  START ONE: python scripts/new_verification_report.py --from-plan {args.plan} "
              f"--out <report.json>  — it binds the report to this plan, computes the tier, and "
              f"pre-lists every pointer. Then re-run this command with "
              f"--verification <report.json> instead of --no-verification-yet.", file=sys.stderr)
        print("=" * 78, file=sys.stderr)
        notes.append(
            "NO VERIFICATION REPORT: the report checks did not run. This plan has NOT been "
            "tested for required-domain coverage, both audits, resolvable claims_checked "
            "pointers, or a report bound to this plan and not another -- and nothing here has "
            "checked a fare, an opening time or an entry rule against the world. A clean exit "
            "below means the plan agrees with itself, not that it is true. Say so when you "
            "present it, and do not call it verified. Pass --verification <report.json> to arm "
            "the check.")

    # A check that raised did not enforce whatever it enforces, so the run is incomplete whether
    # or not anything else fired. Exit 2 -- the code this script already uses for "could not run"
    # -- keeps that distinct from exit 1, "the plan is wrong".
    status = 2 if crashed else (1 if errors else 0)

    if args.json:
        print(json_report(split_findings(errors, errors.sites, errors.checks), notes, plan,
                          ok=not errors and not crashed))
        return status

    for note in notes:
        print(f"note: {note}")
    if errors:
        print("PLAN CONSISTENCY FAILED", file=sys.stderr)
        legend, lines = format_findings(split_findings(errors, errors.sites, errors.checks))
        for line in legend:
            print(f"({line})", file=sys.stderr)
        for line in lines:
            print(f"- {line}", file=sys.stderr)
        return status
    print("PLAN CONSISTENCY OK")
    # Name the next command. Measured with a different assistant on a deliberately broken plan:
    # codex ran check_plan_contract and check_plan_consistency, fixed everything both of them
    # reported, saw two clean exits and reported the plan fixed -- while a third defect survived,
    # because the rule that catches it lives in render_final_trip_html.validate_plan, a command it
    # never reached. Nothing was wrong with its reasoning; the pipeline simply did not say where it
    # continues, and an assistant that cannot hold 110KB of prose reconstructs the order from
    # whatever the last command printed. A clean gate is the most dangerous place to stay silent.
    #
    # A delivered plan being revised continues differently: the save is what renders the page,
    # carries the amended report beside it and records the recheck, so pointing at the renderer
    # sent a literal-minded assistant to overwrite the page by hand with the receipt left behind.
    resave = (resave_command(args.plan, args.verification)
              if args.verification and isinstance(plan.get("verification_receipt"), dict)
              and delivered_workspace(args.plan) is not None else "")
    if resave:
        print("This plan was delivered verified; saving it again renders the page, runs the page "
              "checks and records the recheck:", file=sys.stderr)
        print(f"NEXT: {resave}", file=sys.stderr)
        return status
    print(f"NEXT: python scripts/render_final_trip_html.py {args.plan} <final.html>  "
          f"— it runs its own contract checks (booking options, leg groups, map endpoints) that "
          f"this gate does not, and a clean run here is not a clean plan.", file=sys.stderr)
    return status


if __name__ == "__main__":
    raise SystemExit(main())

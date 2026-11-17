#!/usr/bin/env python3
"""Render a safe, self-contained Travel Buddy final itinerary from JSON.

Usage: python render_final_trip_html.py <plan.json|-> [<output.html|->]
"""

from __future__ import annotations

import argparse
import base64
import html
import json
import re
import sys
import unicodedata
from functools import lru_cache
from datetime import date, datetime, timedelta
from pathlib import Path
from urllib.parse import parse_qsl, urlparse

from plan_flags import is_mainland_market, stay_sequence
from plan_to_calendar import build_with_summary as build_calendar
from fetch_plan_imagery import ImagerySidecarError, resolve_plan_imagery
from travel_workspace import find_sensitive_values


REQUIRED_STAY_SEARCH_FIELDS = {"destination", "check_in", "check_out", "guests", "rooms"}
REQUIRED_FLIGHT_SEARCH_FIELDS = {"origin", "destination", "outbound_date", "return_date", "travellers"}
REQUIRED_RENTAL_SEARCH_FIELDS = {"pickup_location", "dropoff_location", "pickup_time", "dropoff_time"}
BOOKING_ACCESS_CATEGORIES = {"flight", "accommodation", "attraction_ticket", "rental_car", "rail_or_ground"}
BOOKING_ACCESS_STATUSES = {"available", "limited", "unknown"}
PRICE_STATUSES = {"researched_current", "estimate", "user_confirmed"}
ROUTE_MAP_SCOPES = {"multi_stop", "primary_leg"}
# Booking states from references/decision-and-research.md. Constrained so the page can
# localize them; a free-form status would print an English enum on a Chinese page.
BOOKING_STATES = ("idea", "researched", "held", "booked")
DAY_TYPES = ("arrival", "departure", "full", "transfer")
# A flight number is either the right string or a lie -- it cannot be estimated the way a fare
# can. `unresearched` is the dining rating's `none` for this field: a blank that says why.
SERVICE_IDENTIFIER_STATUSES = ("researched", "unresearched")
# The four questions the first hour on the ground has to answer, and the three states each may
# be in. Module-level so check_plan_contract.py can report a wrong value in its one pass rather
# than leaving it to a second round trip through this gate.
ESSENTIAL_ENTRIES = ("payment", "connectivity", "emergency", "health_and_insurance")
ESSENTIAL_STATUSES = ("researched", "unverified", "not_applicable")
# How much the source register says a row can be trusted. Printed as visible text beside every
# source, and therefore a closed enum for precisely the reason SKILL.md gives for plan_status and
# the budget categories: an arbitrary string cannot be translated, so it leaks.
#
# It was NOT constrained until now, and the cost was measured, not theoretical. Three DELIVERED
# Chinese pages -- 2026-11-16-拉纳卡, 2027-01-08-拉斯帕尔马斯, 2027-02-12-阿利坎特 -- printed the
# bare English words "high" and "medium" in an otherwise fully Chinese source register, and both
# gates reported the pages VALID. 拉纳卡 was the only gate-stamped plan in the workspace, so the
# best plan there shipped the defect with every light green. The renderer's own fallback was the
# English word "researched", which is untranslatable by construction, and validate_trip_html.py
# could not see any of it because its detector was a hand-maintained list of English strings
# somebody had remembered to write down.
#
# The decision to CONSTRAIN rather than to translate-what-we-recognise is deliberate, and it has a
# price worth stating. Delivered workspaces contain confidence values that are prose --
# "primary source; timetable requires recheck", "climate average; forecast requires recheck",
# and even hand-localized "高"/"中" where an author did by typing what this enum now does by
# construction. Those plans now fail validate_plan and have to move the qualification into
# `claim_or_decision_supported`, the field whose entire job is to say what the source proves.
# The alternative -- render the recognised tokens and pass everything else straight through --
# reopens the hole for every value nobody predicted, which is exactly how this defect arrived.
# A field that renders visibly and accepts anything is not a field with a small bug in it.
SOURCE_CONFIDENCE_LEVELS = ("high", "medium", "low", "researched", "unverified")
# What a source row shows when the plan recorded no confidence at all. It is a MEMBER of the enum
# above, so it localizes through the same label table as every authored value; the previous
# default was the bare literal "researched" spliced into the markup, which no label key could
# reach and no translator could fix. Its meaning is unchanged on purpose: this fix is about the
# word the reader sees, and quietly re-defaulting delivered pages from "researched" to something
# weaker would change what those pages claim about sources nobody re-examined.
SOURCE_CONFIDENCE_DEFAULT = "researched"
# Budget categories are an enum for the same reason, and so `included_categories` and
# `breakdown` can be compared without string-matching two different spellings.
BUDGET_CATEGORIES = (
    "flight",
    "rail",
    "intercity_bus",
    "ferry",
    "rental_car",
    "fuel_tolls_parking",
    "accommodation",
    "food",
    "local_transport",
    "attractions",
    "tours_and_activities",
    "insurance",
    "visa_and_entry",
    "shopping_and_misc",
    "contingency",
)
MEAL_TYPES = ("breakfast", "lunch", "dinner", "snack")
# Whether a meal needs booking, as the calendar's reminder reads it (scripts/plan_to_calendar.py).
RESERVATION_NEEDS = ("required", "recommended", "walk_in", "not_accepted")
RESERVATION_NEED_ENGLISH = {"required": "Booking required", "recommended": "Booking recommended",
                            "walk_in": "Walk-in", "not_accepted": "No reservations"}
CALENDAR_NOTE = ("Downloads a calendar file. Opening it puts the transport you have chosen or booked, "
                 "your stays, meals and timed stops into your own calendar, which is how this page "
                 "reaches your phone — reminders included.")
CALENDAR_UNDECIDED = "transport group(s) not decided yet — they join the calendar once you record a choice."
CALENDAR_FLOATING = ("Times in this file carry no time zone: Apple Calendar shows them as written, while "
                     "Google Calendar and Outlook shift them to your phone's zone.")
ARRIVAL_MODES = ("flight", "rail", "road", "other")
# What the traveller's own status means for getting into this destination. Nationality
# alone cannot answer it: a permit holder may need no visa where their passport would.
#
# Six spellings, three of them newer: the intake contract words the same question as
# not_required / required_held / required_to_apply, splitting "visa required" into
# already-held versus still-to-apply -- the difference between a trip that can be booked
# now and one that cannot. Both vocabularies are accepted because a plan written before
# the split must keep validating and rendering exactly as it did.
ENTRY_STATUSES = (
    "no_visa_required",
    "visa_required",
    "unverified",
    "not_required",
    "required_held",
    "required_to_apply",
)
ALLERGY_SEVERITIES = ("none", "preference", "intolerance", "severe")
# The parts of a plan a recheck can name that are neither a day nor a booking option. Everything
# else a traveller would recognise by its own heading; these four cover the blocks a verification
# actually reads, and the rest are grouped rather than printed by their JSON key names.
RECHECK_PART_LABELS = {
    "entry_context": "Entry eligibility",
    "arrival_essentials": "First hour on the ground",
    "budget": "Budget",
    "transport_overview": "Transport overview",
}
RECHECK_PART_OTHER = "Other trip details"
# check_plan_consistency.INTAKE_CONSTRAINT_FIELDS names the fields a plan may change after the form
# only by saying so in trip.intake_changes; these are the words the page uses for each. The first
# two reuse the constraint panel's own labels so a translated page says them the same way twice.
INTAKE_CHANGE_LABELS = {
    "dietary_or_religious_needs": "Dietary needs",
    "mobility_notes": "Mobility",
    "traveler_count": "Party size",
    "cap_per_person": "Budget cap per person",
}

# How this plan's requirements were collected. SKILL.md makes the loopback HTML form the required
# path and the chat questionnaire a fallback the TRAVELLER chooses; until this field existed that
# rule was prose, and prose is exactly what a second agent skipped. Measured: assistants on other
# harnesses opened no form at all and went straight to chat, which loses the intake server's
# rejection of document/payment/address fields, its scope-versus-work-mode consistency check, the
# profile's never_recommend and dietary prefill, and the saved intake that
# check_shortlist_consistency.py --intake computes the hard-constraint roster from. Each method
# has to carry the evidence that it was allowed, so that skipping the form costs more than using
# it rather than less.
INTAKE_METHODS = ("html_form", "user_supplied", "chat_fallback")
# Opening-hours provenance, as recorded by the dining research. Anything that is not an
# explicit "verified" is shown in the warning treatment: "researched" means somebody read
# a website once, which is not the same as somebody confirming the venue is open on the
# evening this plan sends the traveller there.
HOURS_STATUS_ENGLISH = {
    "verified": "verified",
    "researched": "researched",
    "unverified": "not verified",
    "closed_unknown": "opening status unknown",
}
HOURS_STATUS_LABEL_KEYS = {
    "verified": "hours_verified",
    "researched": "hours_researched",
    "unverified": "hours_unverified",
    "closed_unknown": "hours_closed_unknown",
}
TRANSPORT_MODES = ("self-drive", "public-transit")
CURRENCY_SYMBOLS = {
    "AUD": "A$", "BRL": "R$", "CAD": "C$", "CNY": "¥", "DKK": "kr", "EUR": "€", "GBP": "£",
    "HKD": "HK$", "IDR": "Rp", "INR": "₹", "JPY": "¥", "KRW": "₩", "MXN": "MX$", "MYR": "RM",
    "NOK": "kr", "NZD": "NZ$", "PHP": "₱", "RUB": "₽", "SEK": "kr", "SGD": "S$", "THB": "฿",
    "TRY": "₺", "TWD": "NT$", "USD": "$", "VND": "₫",
}
DISALLOWED_URL_QUERY_KEYS = {
    "aff",
    "affiliate",
    "aid",
    "api_key",
    "auth",
    "authorization",
    "cart",
    "key",
    "password",
    "payment",
    "ref",
    "referral",
    "referrer",
    "secret",
    "session",
    "sid",
    "token",
}
DISALLOWED_URL_PATH_PARTS = {"account", "cart", "checkout", "login", "payment", "signin"}

# One palette per trip character, chosen from what the traveller said they came for.
# trip.destination_type would be the obvious key and is useless: it reads "city" on all eleven
# saved plans. trip.traveler_preferences is the honest signal -- a coast trip and a forest trip
# are different trips even when both are technically cities, and the traveller is the one who
# said which this is.
#
# Each palette is written out rather than generated. A generated hue would eventually produce
# grey-on-grey or a warning colour that reads as decoration, and this page is read in sunlight on
# a phone. The figures in plan_visuals.py all draw with var(--accent), so they re-tone for free.
TRIP_PALETTES = {
    "coast": {  # sea and sand: the default holiday register
        "--ink": "#10283a", "--muted": "#5b7183", "--paper": "#f3f2ea", "--card": "#fffefb",
        "--accent": "#0e7490", "--accent-deep": "#0b5a70", "--accent-soft": "#d9eef5",
        "--line": "#d7ded9", "--warm": "#e8924a", "--warm-soft": "#fdf0e0",
        "hero": "linear-gradient(135deg,#0d2b43 0%,#0f5f80 55%,#12879b 100%)",
        "glow_a": "#cfe9f2", "glow_b": "#fbe3c6",
    },
    "highland": {  # forest, lakes, mountains
        "--ink": "#16261d", "--muted": "#5d7065", "--paper": "#f2f2ec", "--card": "#fffefc",
        "--accent": "#2f7d55", "--accent-deep": "#1f5c3e", "--accent-soft": "#dcefe1",
        "--line": "#d8ded4", "--warm": "#c9762f", "--warm-soft": "#fbeedd",
        "hero": "linear-gradient(135deg,#152b21 0%,#2c5c40 55%,#3f8358 100%)",
        "glow_a": "#d7ead9", "glow_b": "#efe3c4",
    },
    "urban": {  # streets, museums, food, nightlife
        "--ink": "#1b1a22", "--muted": "#6b6875", "--paper": "#f5f2f0", "--card": "#fffdfd",
        "--accent": "#8a3f6b", "--accent-deep": "#6b2d52", "--accent-soft": "#f3e2ec",
        "--line": "#e0d9dc", "--warm": "#d08033", "--warm-soft": "#fdf0e1",
        "hero": "linear-gradient(135deg,#231d2c 0%,#5c2f52 55%,#8a3f6b 100%)",
        "glow_a": "#efdfe9", "glow_b": "#f8e5cd",
    },
    "arid": {  # desert, canyon, dry heat
        "--ink": "#2a1c14", "--muted": "#7a675b", "--paper": "#f7f1e7", "--card": "#fffdf8",
        "--accent": "#b45a24", "--accent-deep": "#8d431a", "--accent-soft": "#fae5d2",
        "--line": "#e3d9c9", "--warm": "#3f7f86", "--warm-soft": "#e0f0f1",
        "hero": "linear-gradient(135deg,#3a2216 0%,#8a4520 55%,#c0682c 100%)",
        "glow_a": "#f6ddc4", "glow_b": "#d9ecec",
    },
    "alpine": {  # snow, ice, winter sport
        "--ink": "#16222e", "--muted": "#61707f", "--paper": "#f1f4f7", "--card": "#ffffff",
        "--accent": "#3f6ea8", "--accent-deep": "#2b527f", "--accent-soft": "#e0eaf6",
        "--line": "#d8e0e8", "--warm": "#c2703f", "--warm-soft": "#fbebe0",
        "hero": "linear-gradient(135deg,#1a2a3b 0%,#33567f 55%,#5688bd 100%)",
        "glow_a": "#dde9f5", "glow_b": "#f2e2d6",
    },
}

# Matched against the traveller's own words, in their own language. Kept explicit rather than
# clever: a word list can be read and argued with, while a classifier cannot be told why it was
# wrong about somebody's holiday.
PALETTE_HINTS = {
    # Multilingual on purpose. The first version held English and Chinese only, so a French plan
    # saying "forêt et lac" scored zero everywhere and fell to the default -- silently, which is
    # the worst way for a styling decision to be wrong. The traveller writes these words in their
    # own language and the plan records that language, so the vocabulary has to travel too.
    "coast": ("coast", "beach", "sea", "island", "ocean", "seaside",
              "playa", "costa", "mar", "isla", "plage", "côte", "mer", "île",
              "strand", "küste", "meer", "insel", "spiaggia", "costiera", "praia",
              "пляж", "море", "ビーチ", "海岸", "海", "岛", "滨", "沙滩", "바다"),
    "highland": ("forest", "lake", "mountain", "hik", "trail", "nature", "wood", "valley",
                 "bosque", "lago", "montaña", "sender", "forêt", "lac", "montagne", "randonn",
                 "wald", "see", "berg", "wander", "foresta", "lago", "montagna",
                 "лес", "озеро", "гора", "森", "湖", "山", "徒步", "自然", "숲", "산"),
    "alpine": ("snow", "ski", "glacier", "winter sport", "nieve", "esquí", "neige", "glacier",
               "schnee", "gletscher", "neve", "снег", "лыж", "雪", "滑雪", "冰川", "スキー"),
    "arid": ("desert", "dune", "canyon", "oasis", "desierto", "duna", "cañón",
             "désert", "wüste", "deserto", "пустын", "沙漠", "戈壁", "峡谷", "砂漠"),
    "urban": ("city", "street", "museum", "food", "market", "nightlife", "architect", "art",
              "ciudad", "calle", "museo", "gastronom", "mercado", "ville", "rue", "musée",
              "stadt", "straße", "città", "cidade", "город", "музей",
              "街区", "美食", "博物馆", "建筑", "市集", "城市", "都市", "グルメ", "도시"),
}


def palette_for(plan: dict) -> dict:
    """Pick the page's colour register from what the traveller asked for."""
    # `or {}` and `or []` treat a wrongly-typed value as present rather than absent, so a
    # traveler_preferences that arrived as a string, or a subtypes list that arrived as a number,
    # crashed the renderer with a traceback on the delivery path instead of failing cleanly.
    # Predates this fix (reproduced on 2.3.0); found by fuzzing the checks added around it. The
    # page colour is a decoration -- it must never be the thing that stops a plan being saved.
    trip = plan.get("trip")
    preferences = trip.get("traveler_preferences") if isinstance(trip, dict) else None
    if not isinstance(preferences, dict):
        preferences = {}
    words = []
    for field in ("ranked_must_haves", "natural_subtypes", "human_cultural_subtypes"):
        value = preferences.get(field)
        if isinstance(value, (list, tuple)):
            words += [v for v in value if isinstance(v, str)]
    haystack = " ".join(words).casefold()
    if not haystack.strip():
        return TRIP_PALETTES["coast"]
    scores = {name: sum(haystack.count(hint.casefold()) for hint in hints)
              for name, hints in PALETTE_HINTS.items()}
    # Ranked must-haves are ranked, so the first one breaks a tie rather than dictionary order.
    best = max(scores, key=lambda name: (scores[name], name == "coast"))
    return TRIP_PALETTES[best if scores[best] else "coast"]


def palette_css(palette: dict) -> str:
    variables = "".join(f"{key}:{value};" for key, value in palette.items()
                        if key.startswith("--"))
    return (f":root{{{variables}}}"
            f"body{{background:radial-gradient(circle at 8% -8%,{palette['glow_a']} 0 13%,"
            f"transparent 32%),radial-gradient(circle at 100% 5%,{palette['glow_b']} 0 12%,"
            f"transparent 29%),var(--paper)}}"
            f".hero{{background:{palette['hero']}}}")


FINAL_PAGE_DESIGN = r"""
:root{--ink:#132238;--muted:#637186;--paper:#f6f1e9;--card:#fffdfa;--accent:#0f766e;--accent-deep:#075c58;--accent-soft:#dff3ee;--line:#d9d9d1;--warm:#ee8d4a;--warm-soft:#fff0e3;--shadow:0 20px 54px rgb(26 42 57/.10);--radius:22px}
body{background:radial-gradient(circle at 8% -8%,#d5ede8 0 13%,transparent 32%),radial-gradient(circle at 100% 5%,#f9dfc3 0 12%,transparent 29%),var(--paper)}
main{max-width:1180px;padding:42px 22px 74px}h1,h2,h3,h4{color:var(--ink)}h1{max-width:780px;color:#fff}h2{letter-spacing:-.025em}
.hero{position:relative;isolation:isolate;overflow:hidden;padding:clamp(30px,5vw,54px);border:0;border-radius:30px;color:#e3f5f1;background:linear-gradient(135deg,#102c43 0%,#105f63 57%,#0d776e 100%);box-shadow:0 24px 60px rgb(10 41 55/.22)}
.hero::before{content:"";position:absolute;z-index:-1;width:440px;height:440px;right:-150px;top:-250px;border:1px solid rgb(255 255 255/.22);border-radius:50%;box-shadow:0 0 0 36px rgb(255 255 255/.06),0 0 0 98px rgb(255 255 255/.04)}
.hero::after{content:"✦";position:absolute;z-index:-1;right:28px;bottom:-22px;color:rgb(255 255 255/.09);font:800 clamp(5rem,16vw,12rem)/1 ui-serif,Georgia,serif;letter-spacing:-.1em}
.hero p{max-width:760px;color:#e3f5f1}.hero .meta{color:#c7e7e2}.hero .eyebrow{color:#b6e9df}
.panel,.day-card{border:1px solid rgb(19 34 56/.10);border-radius:var(--radius);background:rgb(255 253 250/.94);box-shadow:var(--shadow)}.panel{padding:clamp(22px,3vw,30px)}.grid{gap:16px}.fact,.option{border:1px solid #dce4e0;border-radius:16px;background:linear-gradient(145deg,#fff,#fbfaf5)}
.fact{position:relative;overflow:hidden;min-height:116px;padding:17px}.fact::after{content:"";position:absolute;width:54px;height:54px;right:-19px;top:-19px;border-radius:50%;background:var(--accent-soft)}.fact strong{position:relative;z-index:1;font-size:1.22rem}
.option{padding:18px;transition:transform .18s ease,box-shadow .18s ease}.option:hover{transform:translateY(-3px);box-shadow:0 16px 28px rgb(26 42 57/.12)}.pill{padding:5px 9px;background:var(--accent-soft);color:var(--accent-deep);letter-spacing:.04em}
.day-card{position:relative;overflow:hidden;padding:clamp(22px,3vw,30px)}.day-card::before{content:"";position:absolute;inset:0 auto 0 0;width:5px;background:linear-gradient(var(--warm),#f6c06e)}.day-top{align-items:flex-start;padding-bottom:18px;border-bottom:1px solid #e2e5e0}.day-number{min-width:54px;height:54px;border:1px solid rgb(255 255 255/.2);border-radius:16px;background:linear-gradient(135deg,#102c43,#17676b);box-shadow:0 10px 20px rgb(15 78 83/.20)}
.day-card section{padding:18px 0 0}.day-card h3{display:flex;align-items:center;gap:8px}.day-card h3::before{content:"";width:7px;height:7px;border-radius:50%;background:var(--warm);box-shadow:0 0 0 4px var(--warm-soft)}.timeline li{padding:15px 0}.timeline time{color:var(--accent-deep)}
.route-map{border:1px solid #d8e6e3;border-radius:17px;background:linear-gradient(135deg,#edf7f5,#f7fbfa)}.route-map figcaption{color:var(--muted)}.route-segment{padding:14px 0}
.booking-link,.map-link{border-radius:12px;padding:10px 14px;background:linear-gradient(135deg,var(--accent),#138b80);box-shadow:0 8px 15px rgb(15 118 110/.18);transition:transform .18s ease,filter .18s ease}.map-link{background:linear-gradient(135deg,#17324a,#254e69);box-shadow:0 8px 15px rgb(23 50 74/.18)}.booking-link:hover,.map-link:hover{color:#fff;filter:brightness(1.04);transform:translateY(-1px)}
.warning{border:1px solid #f2cf9d;border-left:4px solid var(--warm);border-radius:14px;background:linear-gradient(100deg,#fff7ed,#fff0e2);color:#744016}details{padding:14px 0 0}summary{color:var(--accent-deep)}.source-item{margin:10px 0}
@media(max-width:600px){main{padding:22px 13px 48px}.hero{border-radius:24px;padding:30px 23px 38px}.panel,.day-card{padding:20px}.day-number{min-width:46px;height:46px}}
.page-nav{position:sticky;top:0;z-index:5;display:flex;gap:8px;overflow-x:auto;margin:18px 0;padding:10px 12px;border:1px solid rgb(19 34 56/.10);border-radius:16px;background:rgb(255 253 250/.94);backdrop-filter:blur(12px);box-shadow:0 8px 20px rgb(26 42 57/.07)}
.page-nav-link{flex:0 0 auto;display:flex;flex-direction:column;padding:7px 12px;border-radius:11px;background:#eef4f2;color:var(--accent-deep);font-size:.86rem;font-weight:750;text-decoration:none;white-space:nowrap}
.page-nav-link:hover{background:var(--accent-soft)}.day-nav-date{color:var(--muted);font-size:.76rem;font-weight:600}
.panel,.day-card{scroll-margin-top:74px}
.route-rail{list-style:none;margin:0;padding:2px 0 0}
.route-stop{position:relative;display:flex;align-items:flex-start;gap:12px;padding-bottom:15px}
.route-stop::before{content:"";position:absolute;left:12px;top:27px;bottom:-1px;width:2px;background:#b6d5cf}
.route-stop:last-child{padding-bottom:0}.route-stop:last-child::before{display:none}
.route-stop-index{flex:0 0 auto;display:grid;place-items:center;width:26px;height:26px;border-radius:50%;background:var(--accent);color:#fff;font-size:.76rem;font-weight:800}
.route-stop-name{padding-top:3px;font-weight:700}
.unpriced-list{margin:0 0 5px;padding-left:19px;font-weight:700}.fact.unpriced{padding-top:19px}
.route-fallback{border-left:3px solid #cfe0dc;padding-left:11px}
.single-option-reason{border-left:3px solid var(--warm);padding-left:11px}
.ticket-note{margin:6px 0 0;border-left:3px solid var(--warm);padding-left:11px;color:#744016}
@media print{body{background:#fff}.page-nav{display:none}.day-card{break-inside:auto}.day-card section,.option,.dining-stop{break-inside:avoid}.hero{color:var(--ink);background:#fff;border:1px solid #d9d9d1}.hero h1{color:var(--ink)}.hero p,.hero .meta,.hero .eyebrow{color:var(--muted)}.hero::before,.hero::after{display:none}.panel,.day-card{box-shadow:none}h2,h3,h4{break-after:avoid}.booking-link,.map-link,.dining-link,.dining-reservation-link{padding:0;border-radius:0;background:none;box-shadow:none;color:#075952;text-decoration:underline}}
"""

sys.path.insert(0, str(Path(__file__).resolve().parent))

import plan_visuals  # noqa: E402
import bookings as booking_rules  # noqa: E402 - the booking-record rules (scripts/bookings.py)


def labels_for(language: object, custom_labels: object = None) -> dict[str, str]:
    """Return presentation labels for the supported final-plan interface languages."""
    normalized = str(language).casefold()
    if normalized.startswith("zh") or "chinese" in normalized or "中文" in normalized:
        return {
            "review_option": "查看选项",
            "review_option_provider": "在 {provider} 查看选项",
            "direct_provider": "在 {provider} 查看官方直订页面",
            "review_reservation": "查看预订",
            "view_source": "查看来源",
            "no_meal_recommendation": "未调研到用餐推荐。",
            "opening_hours_recheck": "切换前请核验当前营业时间。",
            "per_person_suffix": "/ 人",
            "round_trip": "搜索往返行程",
            "round_trip_in": "在 {provider} 搜索往返行程（已带入日期）",
            "compare_booking": "在 Booking.com 比较（已带入日期和住客）",
            "compare_platform_prefix": "在 ",
            "compare_platform_suffix": " 比较（已带入日期和住客）",
            "segment_map": "在地图中打开此路段",
            "segment_map_provider": "在 {provider} 中打开此路段",
            "ticket_prefix": "查看门票：",
            "anchor_serves_label": "你要的是：",
            "fig_walking_caption": "每日步行分钟：接驳段加上各站点站立行走的时间",
            "fig_map_caption": "按到访顺序的真实相对位置。导航请用地图按钮。",
            "fig_budget_caption": "占人均总额的比例，以及用掉了多少上限",
            "fig_shape_caption": "当天的固定时间点",
            "fig_longest_walk": "最长单次步行",
            "photo_credit_label": "图片来源",
            "photo_source_label": "经 Wikimedia，取自条目",
            "unverified_banner_title": "未经事实核验",
            "unverified_banner_body": (
                "本计划没有任何核验记录。其中的票价、营业时间、入境规则与可订状态"
                "均未与运营方或官方来源核对过。请把每一个数字都当作估算，预订前自行核实。"),
            "pill_flight": "机票", "pill_hotel": "酒店", "pill_ticket": "门票",
            "pill_car": "租车", "pill_ground": "铁路/巴士/渡轮",
            "schematic_aria": "按游览顺序的路线示意图",
            "schematic_start": "起点", "schematic_end": "终点",
            # 直飞 means specifically "direct by air", so a through train printed it. The English
            # "non-stop" is fine for both, but a language that distinguishes them needs two keys.
            "nonstop": "直飞", "nonstop_ground": "直达",
            "stops_suffix": "次中转", "unit_km": "公里",
            "group_ground": "铁路 / 长途巴士 / 渡轮选项",
            "station_access": "车站与接驳：",
            "why_providers": "为什么选这些服务商：",
            "constraints_heading": "你的硬性约束",
            "constraints_severity": "过敏严重程度：",
            "constraints_dietary": "饮食限制：",
            "constraints_mobility": "行动能力：",
            "constraints_walk_cap": "单段连续步行上限：",
            "constraints_card": "过敏卡 —— 到店请出示这段文字：",
            "intake_changed_heading": "表单之后的调整：",
            "rechecked_heading": "主核验之后又复核过：",
            "rental_restriction_label": "限制说明：",
            "fig_straight_line": "直线跨度",
            "overall_route_overview_general": "打开路线总览（每日分段见下方）",
            "overall_route_overview_general_provider": "在 {provider} 中打开路线总览（每日分段见下方）",
            "transport_tickets_pointer": "当天的交通票见上方的预订选项。",
            "recheck_part_entry": "入境资格",
            "recheck_part_arrival": "落地第一小时",
            "recheck_part_budget": "预算",
            "recheck_part_transport": "交通总览",
            "recheck_part_other": "其他行程信息",
            "intake_field_party": "人数：",
            "intake_field_cap": "人均预算上限：",
            "preferences_heading": "你提出的需求",
            "preferences_direction": "体验方向：",
            "preferences_avoid": "希望避开的：",
            "gates_label": "已通过的结构检查：",
            "gates_caveat": "它们证明这份计划自身前后一致，绝不证明其中的事实为真。",
            "plan_status_prefix": "行程状态 · ",
            "arrival": "抵达方式：",
            "pace": "节奏：",
            "currency": "货币：",
            "last_checked": "调研最后核验：",
            "price_recheck": "价格与库存均须在购买前再次核验。",
            "budget": "预算概览",
            "total": "人均可比较预算",
            "included": "包含的假设",
            "ground": "地面交通方案",
            "browse": "浏览选项 — 尚未购买",
            "no_reservation": "仅展示当前调研选项；打开链接不会创建预订。",
            "booking_access_checks": "预订可访问性核验",
            "access_flight": "机票",
            "access_accommodation": "住宿",
            "access_attraction_ticket": "景点门票",
            "access_rental_car": "租车",
            "access_rail_or_ground": "铁路/地面交通",
            "access_available": "可用",
            "access_limited": "受限",
            "access_unknown": "待核验",
            "overall_transport": "全程交通",
            "overall_route": "打开全程路线",
            "overall_route_provider": "在 {provider} 中打开全程路线",
            "overall_route_overview": "打开机场接驳路线（每日分段见下方）",
            "overall_route_overview_provider": "在 {provider} 中打开机场接驳路线（每日分段见下方）",
            "sources": "来源、可信度与购买前复核清单",
            "sources_used": "使用的来源",
            "recheck_before": "购买前复核",
            "no_purchase_options": "本行程未请求购买选项。",
            "price_unverified": "价格暂未核验",
            "time_unverified": "时间暂未核验",
            "up_to": "最高",
            "hour": "小时",
            "minute": "分钟",
            "conditions_recheck": "条款须复核",
            "price_per_person": "人均往返价格：",
            "price_per_room_night": "每间每晚价格：",
            "price_trip_total": "本次住宿总价：",
            "price_ticket": "每人门票价格：",
            "price_car_day": "每车每日价格：",
            "availability": "库存状态：",
            "price_checked": "价格核验：",
            "price_status": "价格状态：",
            "price_researched_current": "已调研现价",
            "price_estimate": "估算",
            "price_user_confirmed": "用户确认",
            "outbound": "去程：",
            "return": "返程：",
            "hotel_location": "位置与通勤：",
            "guest_rating_label": "住客评分：",
            "hotel_fit": "适配原因：",
            "provider": "供应商：",
            "compared": "比较平台：",
            "checked": "核验时间：",
            "source": "来源：",
            "source_link": "来源",
            "to": "至",
            "travellers": "位旅行者",
            "guest": "位住客",
            "room": "间客房",
            "arranged_independently": "自行安排住宿",
            "departure_checkout": "退房 / 当晚无住宿",
            "day": "第",
            "day_suffix": "天",
            "stay": "住宿",
            "avail_available": "有房/有位",
            "avail_limited": "余量有限",
            "avail_unknown": "尚未核实",
            "essentials_heading": "落地第一小时",
            "essentials_payment": "怎么付钱",
            "essentials_connectivity": "怎么上网",
            "essentials_emergency": "出事找谁",
            "essentials_health": "医疗与保险",
            "calendar_add": "把这趟行程加进日历",
            "calendar_note": "会下载一个日历文件。打开它，你已选或已订的交通、住宿、用餐和有时刻的安排都会进入你自己的日历——这也是这份页面到达你手机的方式，提醒一并带过去。",
            "calendar_undecided": "组交通还没决定——记录选择后才会进入日历。",
            "calendar_floating": "这个文件里的时间没有时区：苹果日历按原样显示，Google 日历和 Outlook 会按手机所在时区平移。",
            "age_since": "距这次调研已过去 N 天。",
            "age_until": "距出发还有 N 天。",
            "age_past": "这趟行程的出发日期已经过去。",
            "age_stale": "价格、营业时间与入境规则都会变；这里的每个数字都请在下单前重新确认。",
            "spine_heading": "住宿主线",
            "spine_nights": "晚",
            "spine_move": "转场日",
            "spine_note": "每一次转场都是一个更换住宿的日子；下面的每日卡片会说明是哪一天。",
            "plan": "行程",
            "dining": "用餐建议",
            "dining_map": "在 {provider} 中查看餐厅",
            "dining_backup": "备选：",
            "free_time": "自由活动",
            "route": "路线与交通",
            "schematic": "示意图 — 不用于导航。按游览顺序展示站点；请使用实时地图获取路线。",
            "full_day_route": "打开当日完整路线",
            "full_day_route_provider": "在 {provider} 中打开当日完整路线",
            "full_day_route_overview": "打开路线概览（请查看下方分段）",
            "full_day_route_overview_provider": "在 {provider} 中打开路线概览（请查看下方分段）",
            "alternative_map_provider": "在 {provider} 中打开备选路线",
            "route_by_segment": "分段路线",
            "operating_recheck": "出发前请再次核验运营情况。",
            "tickets": "门票与复核",
            "no_ticket": "列出的活动没有需要单独购买或已核验的门票。",
            "contingency": "请为突发情况预留灵活备选方案。",
            "plan_evidence": "行程依据",
            "destination_essentials": "目的地体验重点",
            "budget_breakdown": "人均预算明细",
            "default_recheck": "购买前请再次核验价格、可订性、入境要求和运营情况。",
            "walk": "步行",
            "transfers": "次换乘",
            "meal_breakfast": "早餐",
            "meal_lunch": "午餐",
            "meal_dinner": "晚餐",
            "meal_snack": "小食",
            "state_idea": "构想",
            "state_researched": "已调研",
            "state_held": "已预留",
            "state_booked": "已预订",
            "arrival_flight": "飞机",
            "arrival_rail": "铁路",
            "arrival_road": "陆路",
            "arrival_other": "其他方式",
            "mode_self_drive": "自驾",
            "mode_public_transit": "公共交通",
            "cat_flight": "机票",
            "cat_rail": "铁路",
            "cat_intercity_bus": "长途巴士",
            "cat_ferry": "轮渡",
            "cat_rental_car": "租车",
            "cat_fuel_tolls_parking": "油费/过路费/停车",
            "cat_accommodation": "住宿",
            "cat_food": "餐饮",
            "cat_local_transport": "市内交通",
            "cat_attractions": "景点门票",
            "cat_tours_and_activities": "体验与活动",
            "cat_insurance": "保险",
            "cat_visa_and_entry": "签证与入境",
            "cat_shopping_and_misc": "购物与杂项",
            "cat_contingency": "预备金",
            "not_supplied": "未提供",
            "provider_fallback": "供应商",
            "direct_provider_fallback": "官方直订渠道",
            "map_provider_fallback": "地图服务",
            "comparison_platform_fallback": "比较平台",
            "flexible_time": "灵活安排",
            "route_start": "起点",
            "route_end": "终点",
            "route_fallback_label": "备选方案：",
            "walking_burden_label": "全天步行：",
            "fare_conditions_label": "票价条款：",
            "single_option_label": "仅列一个选项的原因：",
            "unpriced_categories": "尚未核价的类别",
            "none_unpriced": "无",
            "planning_assumptions": "规划假设",
            "platform_note_label": "平台选择说明：",
            "ticket_state_label": "门票状态：",
            "ticket_note_label": "门票：",
            "ticket_sale_label": "开售：",
            "ticket_sale_always_available": "现已开售",
            "ticket_sale_scheduled_release": "定时开售",
            "ticket_sale_at_the_door": "现场售票",
            "ticket_sale_sold_out": "已售罄或无法购买",
            "ticket_sale_unknown": "开售时间未确认",
            "self_transfer_label": "自行转机：",
            "self_transfer_sentence": "分开出票。误了衔接航班不受保护，需要自己取行李并为下一段重新值机。",
            "booking_booked": "已订",
            "booking_chosen": "已选，尚未预订",
            "booking_via": "渠道",
            "booking_paid": "实付",
            "booking_confirmed": "（用户确认）",
            "booking_alternatives": "未选的备选",
            "booking_heading": "你的预订与选项",
            "booked_so_far": "已付合计（用户确认）",
            "still_to_book": "尚未预订的组",
            "reservation_required": "需提前订位",
            "reservation_recommended": "建议提前订位",
            "reservation_walk_in": "可直接入座",
            "reservation_not_accepted": "不接受预订",
            "nav_label": "本页导航",
            "nav_budget": "预算",
            "nav_options": "预订选项",
            "nav_transport": "全程交通",
            "nav_sources": "来源",
            "no_separate_ticket": "无需单独购票，或尚未核验。",
            "entry_heading": "入境资格",
            "entry_basis": "依据的身份：",
            "entry_no_visa_required": "无需另办签证",
            "entry_visa_required": "需要提前办理签证",
            "entry_unverified": "待核验",
            "entry_not_required": "无需另办签证",
            "entry_required_held": "需要签证（已持有）",
            "entry_required_to_apply": "需要签证（尚未办理）",
            "budget_cap": "人均预算上限",
            "venue_hours_label": "营业时间：",
            "hours_closed_today": "本日闭店",
            "hours_today_suffix": "（本日）",
            "rating_label": "评分：",
            "rating_none": "无公开评分",
            "rating_reviews": " 条评价",
            "hours_verified": "已核验",
            "hours_researched": "已调研（未核验）",
            "hours_unverified": "未核验",
            "hours_closed_unknown": "营业状态未知",
            "group_flight": "机票选项",
            "group_hotel": "住宿选项",
            "group_ticket": "门票选项",
            "group_car": "租车选项",
            # Source-register confidence, one key per SOURCE_CONFIDENCE_LEVELS member. Named
            # confidence_<value> on purpose: localize_enum_values looks the key up by value, the
            # way state_<value> and meal_<value> already work, so adding a level to that tuple and
            # a key here is the whole of what a new level costs. "已调研" deliberately reads the
            # same as hours_researched -- it is the same claim about the same kind of evidence,
            # and two spellings of it on one page would be the register contradicting itself.
            "confidence_high": "高",
            "confidence_medium": "中",
            "confidence_low": "低",
            "confidence_researched": "已调研",
            "confidence_unverified": "未核验",
            # ALLERGY_SEVERITIES, which validate_plan has always enforced and nothing has ever
            # translated. `severity_none` is not rendered today -- the panel skips a "none"
            # severity rather than printing "no allergy" as though it were a constraint -- and is
            # written out anyway so the table matches the enum instead of matching today's caller.
            "severity_none": "无",
            "severity_preference": "偏好",
            "severity_intolerance": "不耐受",
            "severity_severe": "严重（可致命）",
        }
    if isinstance(custom_labels, dict) and all(
        isinstance(value, str) and (value.strip() or key == "day_suffix")
        for key, value in custom_labels.items()
    ) and REQUIRED_UI_LABEL_KEYS.issubset(custom_labels):
        return {str(key): html.escape(value, quote=True) for key, value in custom_labels.items()}
    return {}


# Keys added after custom ui_labels became a supported input. Requiring them would reject every
# label set authored before they existed, silently dropping that page back to English -- so they
# are optional, and localize_static_page falls back to the English source string when absent.
OPTIONAL_UI_LABEL_KEYS = frozenset({
    "anchor_serves_label",
    "fig_walking_caption",
    "fig_map_caption",
    "fig_budget_caption",
    "fig_shape_caption",
    "fig_longest_walk",
    "photo_credit_label",
    "photo_source_label",
    "unverified_banner_title",
    "unverified_banner_body",
    # Added with the booking-page fixes: the stated budget cap, dining opening hours and
    # their provenance, and the three intake spellings of entry status.
    "round_trip_in",
    "budget_cap",
    "venue_hours_label",
    "hours_closed_today",
    "hours_today_suffix",
    "rating_label",
    "rating_none",
    "rating_reviews",
    "hours_verified",
    "hours_researched",
    "hours_unverified",
    "hours_closed_unknown",
    "entry_not_required",
    "entry_required_held",
    "entry_required_to_apply",
    # Added with the per-activity ticket note, and optional for the same reason: making it
    # required would make REQUIRED_UI_LABEL_KEYS reject every label set written before it
    # existed, and a rejected set drops the entire page back to English -- trading one
    # untranslated prefix for a hundred translated ones.
    "ticket_note_label",
    # Added with the ticket sale window on the ticket card (2026-10-09), optional for the same
    # reason as the ticket note above.
    "ticket_sale_label",
    "ticket_sale_always_available",
    "ticket_sale_scheduled_release",
    "ticket_sale_at_the_door",
    "ticket_sale_sold_out",
    "ticket_sale_unknown",
    # Added with the self-transfer warning on flight cards (2026-10-11), optional for the same
    # reason as the ticket note.
    "self_transfer_label",
    "self_transfer_sentence",
    # Added with the booking lifecycle (2026-10-11), optional for the same reason as the ticket note.
    "booking_booked",
    "booking_chosen",
    "booking_via",
    "booking_paid",
    "booking_confirmed",
    "booking_alternatives",
    "booking_heading",
    "booked_so_far",
    "still_to_book",
    # Added with the reservation_need enum (2026-10-11), optional for the same reason as the ticket note.
    "reservation_required",
    "reservation_recommended",
    "reservation_walk_in",
    "reservation_not_accepted",
    # Added with the multi-stop spine, optional for the reason stated directly above and for a
    # third demonstration of it: a plan that sleeps in one place renders no spine at all, so
    # demanding four labels for it would reject every single-base label set ever written in order
    # to translate a section those pages do not contain.
    "avail_available",
    "avail_limited",
    "avail_unknown",
    "essentials_heading",
    "essentials_payment",
    "essentials_connectivity",
    "essentials_emergency",
    "essentials_health",
    "calendar_add",
    "calendar_note",
    "calendar_undecided",
    "calendar_floating",
    "age_since",
    "age_until",
    "age_past",
    "age_stale",
    "spine_heading",
    "spine_nights",
    "spine_move",
    "spine_note",
    # Added with the rail/coach/ferry category, the traveller-constraints panel, the provider
    # rationale and the ten formerly-hardcoded Chinese strings. Optional for the reason stated
    # above and demonstrated by this exact slip: requiring them hard-failed every French,
    # Japanese and Spanish plan already saved in a workspace, naming labels for a booking
    # category those trips do not contain and their author had never heard of.
    "group_ground",
    "station_access",
    "constraints_heading",
    "constraints_severity",
    "constraints_dietary",
    "constraints_mobility",
    "constraints_walk_cap",
    "constraints_card",
    # Added with trip.intake_changes, optional for the same reason as every key around it.
    "intake_changed_heading",
    "rechecked_heading",
    "rental_restriction_label",
    "fig_straight_line",
    "overall_route_overview_general",
    "overall_route_overview_general_provider",
    "transport_tickets_pointer",
    "recheck_part_entry",
    "recheck_part_arrival",
    "recheck_part_budget",
    "recheck_part_transport",
    "recheck_part_other",
    "intake_field_party",
    "intake_field_cap",
    # Added with the traveller-preferences panel, optional for the reason two comments above
    # spell out: making a new key required rejects every label set written before it existed,
    # and a rejected set drops the whole page back to English.
    "preferences_heading",
    "preferences_direction",
    "preferences_avoid",
    # Added with the gate stamp, optional on the same terms as everything above it.
    "gates_label",
    "gates_caveat",
    "why_providers",
    "pill_flight",
    "pill_hotel",
    "pill_ticket",
    "pill_car",
    "pill_ground",
    "schematic_aria",
    "schematic_start",
    "schematic_end",
    "nonstop",
    "nonstop_ground",
    "stops_suffix",
    "unit_km",
    # Added with the source-register confidence enum, and optional on exactly the terms the two
    # comments above spell out: every ui_labels set saved before today lacks these five keys, and
    # making them REQUIRED would reject those sets whole, dropping a hundred correctly translated
    # strings back to English to fix five. Missing keys fall through to the English token instead,
    # which validate_trip_html.py's i18n gate then fails -- loud and one page at a time, which is
    # the trade this file has already made five times.
    "confidence_high",
    "confidence_medium",
    "confidence_low",
    "confidence_researched",
    "confidence_unverified",
    "severity_none",
    "severity_preference",
    "severity_intolerance",
    "severity_severe",
})
REQUIRED_UI_LABEL_KEYS = frozenset(labels_for("zh-CN")) - OPTIONAL_UI_LABEL_KEYS

# Languages with a label table compiled into this file. labels_for() answers {} for anything
# else, so this is the complete set of spellings the renderer itself has ever put on a page --
# which is what makes it the only safe source for the alias tables below.
BUILTIN_LABEL_LANGUAGES = ("zh-CN",)


def localized_enum_aliases(prefix: str, values: tuple[str, ...]) -> dict[str, str]:
    """Map every spelling this file's OWN label tables give `values` back to its machine token.

    Closing sources[].confidence to an enum was right and it refused a delivered plan on the way
    out. plans/2026-09-18-马略卡-帕尔马四日-老城-山间古董火车与索列尔港.json stores 高 six times and 中
    twice -- an author who understood exactly what that field is (one of five graded values, not
    prose) and localized it by hand because in that workspace nothing else would. That is not a
    plan with a bad value in it. It is the one plan that had already solved this problem, and the
    first thing the fix did was make it unrenderable.

    This file's own precedent decides the case: intake_context_errors() is called from
    save_trip_deliverables rather than from validate_plan precisely so a new requirement cannot
    retroactively invalidate plans already sitting in a workspace, and its docstring says so. A
    plan is a portable document. "Retype the English word" is not a good enough reason to refuse
    one that is already correct.

    So the known localized spellings map back, and they map back HERE, next to the table that
    produced them -- a comprehension over labels_for(), not a second hand-written list to drift
    from the first. Adding a level to the enum plus a `<prefix><level>` key to the table is still
    the whole cost of a new level.

    Only BUILT-IN tables are read, and the result is one table for all plans rather than one per
    language: a plan's own `ui_labels` is author-supplied, so treating it as a value domain would
    let any string back into the field through a label key -- which is the hole the enum was
    closed to shut. The consequence is worth naming: an author hand-localizing into a language
    this file does not ship (French, Japanese) still has to store the machine token, because
    there is no spelling of it the renderer could recognise without trusting their own labels.
    validate_plan's error names both the tokens and the spellings, so it says what it will take.

    Raises on a collision rather than picking a winner: if two levels ever share a spelling, or a
    spelling is another level's token, silently mapping one onto the other would mislabel a
    source's evidence on the page. That is a wrong fact, so it fails at import.
    """
    aliases: dict[str, str] = {}
    for language in BUILTIN_LABEL_LANGUAGES:
        labels = labels_for(language)
        for value in values:
            spelling = str(labels.get(f"{prefix}{value}", "")).strip()
            if not spelling:
                continue
            key = spelling.casefold()
            if key in values and key != value:
                raise ValueError(
                    f"{prefix}{value} in the {language} label table is spelled {spelling!r}, "
                    f"which is another member of the same enum. One value would be silently "
                    f"relabelled as another on the page.")
            if aliases.setdefault(key, value) != value:
                raise ValueError(
                    f"{prefix}{value} and {prefix}{aliases[key]} share the spelling {spelling!r} "
                    f"in the {language} label table, so a plan storing it cannot be read back to "
                    f"one token.")
    return aliases


# 高 -> high, 中 -> medium, and the rest. The accepted set stays CLOSED: five tokens plus the five
# spellings this file itself wrote. What is still refused, deliberately, is prose -- other plans
# in the same workspace store "primary source; timetable requires recheck", "official",
# "researched; dynamic" and "medium；须由12306复核", a qualification wearing a value's clothes, and
# those keep failing until the qualification moves into claim_or_decision_supported. Accepting a
# translated TOKEN is not the concession that reopens the hole; accepting a sentence is.
SOURCE_CONFIDENCE_ALIASES = localized_enum_aliases("confidence_", SOURCE_CONFIDENCE_LEVELS)


def canonical_enum_value(value: object, values: tuple[str, ...], aliases: dict[str, str]) -> str | None:
    """The machine token `value` names -- as a token or as a built-in localized spelling -- or None.

    None means "this names no member", never "this is empty": callers distinguish an absent
    optional field from a present wrong one themselves, because those are different errors.
    """
    if not isinstance(value, str):
        return None
    text = value.strip()
    if text in values:
        return text
    return aliases.get(text.casefold())


def source_confidence_token(value: object) -> object:
    """Normalize a stored `sources[].confidence` to its machine token on the way into enum_cell.

    This is the half that makes accepting 高 correct rather than merely permissive. The page ends
    up with data-source-confidence="high" and "high" as the span's text, so localize_enum_values
    translates it like every other enum -- back to 高 on a Chinese page, and to the plan's own
    ui_labels spelling on a French one, which is more than the stored 高 could ever have done.
    Without this the token would sit in the data attribute in Chinese, where the structural i18n
    gate and every downstream reader of that attribute expect a machine value.

    An unrecognised value is returned exactly as it came. enum_cell's docstring argues for showing
    an odd value instead of swapping in a plausible default, and this must not quietly launder
    one into a token it does not mean.
    """
    canonical = canonical_enum_value(value, SOURCE_CONFIDENCE_LEVELS, SOURCE_CONFIDENCE_ALIASES)
    return canonical if canonical is not None else value


def has_builtin_interface_language(language: object) -> bool:
    normalized = str(language).casefold()
    return normalized.startswith(("zh", "en")) or "chinese" in normalized or "english" in normalized or "中文" in normalized


def localize_enum_values(page: str, labels: dict[str, str]) -> str:
    """Translate machine enum values that are printed as visible text.

    Each substitution is anchored on the exact markup the renderer emits, because the
    same tokens also appear inside `data-*` attributes and URLs, which must stay
    machine-readable.  Without this pass a Chinese page shows `flight`, `dinner`, or
    `public-transit` next to fully translated headings.
    """
    states = {value: labels[f"state_{value}"] for value in BOOKING_STATES}
    meals = {value: labels[f"meal_{value}"] for value in MEAL_TYPES}
    arrivals = {value: labels[f"arrival_{value}"] for value in ARRIVAL_MODES}
    modes = {"self-drive": labels["mode_self_drive"], "public-transit": labels["mode_public_transit"]}
    categories = {value: labels[f"cat_{value}"] for value in BUDGET_CATEGORIES}

    # The budget figure prints its own legend and alt text, and both were built from the raw
    # category keys while the breakdown table beside them was translated. A zh page therefore
    # read "市内交通: €47–62" in the table and "local_transport 54" in the chart directly above
    # it -- the same fact in two languages, from one untranslated call site.
    #
    # Scoped to that one figure rather than applied page-wide, which is not tidiness. An
    # unscoped version of this rewrote author prose: a note reading "分类如下: food 120;
    # accommodation 300; local_transport 54" came back with the first two translated and the
    # third left alone, because only the first two happened to be followed by a semicolon.
    # Half a sentence in each language is worse than the defect being fixed.
    category_alternation = "|".join(sorted(BUDGET_CATEGORIES, key=len, reverse=True))

    def localize_budget_figure(figure: str) -> str:
        # Inside the figure every "<category> <number>" IS a legend entry -- in the pv-key spans
        # and again in the svg aria-label/<title>, where a screen reader reads it aloud.
        # Two prefixes, because the same token is punctuated differently in the two places it
        # appears: `">flight 225` opens a legend span with no space, while `: flight 225;`
        # separates entries inside the aria-label. A single lookbehind cannot cover both -- it
        # would have to be variable-width -- and the first version silently translated only the
        # aria-label while the visible legend beside it stayed English.
        return re.sub(
            r'(">|[>;:] )(' + category_alternation + r')(?= \d)',
            lambda match: f"{match.group(1)}{categories[match.group(2)]}",
            figure,
        )

    page = re.sub(
        r'<figure class="pv-figure pv-budget">.*?</figure>',
        lambda match: localize_budget_figure(match.group(0)),
        page,
        flags=re.S,
    )

    page = re.sub(
        r'(<p class="eyebrow">Plan status · )(' + "|".join(BOOKING_STATES) + r')(</p>)',
        lambda match: f"{match.group(1)}{states[match.group(2)]}{match.group(3)}",
        page,
    )
    page = re.sub(
        r'(<p class="meta">Arrival: )(' + "|".join(ARRIVAL_MODES) + r')( · Pace: )',
        lambda match: f"{match.group(1)}{arrivals[match.group(2)]}{match.group(3)}",
        page,
    )
    page = re.sub(
        r'(<strong>)(self-drive|public-transit)(</strong><span>Ground-mobility plan</span>)',
        lambda match: f"{match.group(1)}{modes[match.group(2)]}{match.group(3)}",
        page,
    )
    page = re.sub(
        r'(<h2>Overall transport</h2><p>)(self-drive|public-transit)',
        lambda match: f"{match.group(1)}{modes[match.group(2)]}",
        page,
    )
    # The SAME mode value, printed again at the head of every day's route line. It was localized
    # in the two places above and nowhere here, so every delivered Chinese itinerary opened its
    # 路线与交通 section with the raw word `public-transit` -- five times on the 拉纳卡 page alone --
    # while both gates said VALID. RENDERER_ENGLISH_MARKUP had a pattern for this shape and it
    # spelled the heading `<h2>`; the day card uses `<h3>`, so the deny-list missed it by one
    # character. That is the argument for the structural checks in validate_trip_html.py rather
    # than for a sixth remembered pattern: this leak was on every page the skill has ever shipped.
    # Anchored on the marked span enum_cell() emits, so an author's free-text mode -- the field is
    # not constrained per day -- is left exactly as written instead of being half-matched.
    page = re.sub(
        r'(<span class="route-mode" data-route-mode=")(' + "|".join(TRANSPORT_MODES) + r')(">)[^<]*(</span>)',
        lambda match: f"{match.group(1)}{match.group(2)}{match.group(3)}{modes[match.group(2)]}{match.group(4)}",
        page,
    )
    # Source-register confidence, localized exactly like the states, meals and arrival modes
    # above: anchored on the markup the renderer emits, keyed by value, machine token left intact
    # in the data attribute so every gate can still read it. `labels.get` rather than `labels[]`
    # because the five keys are OPTIONAL -- a ui_labels set written before this enum existed has
    # none of them, and falling through to the English token is what makes the i18n gate fail that
    # one page loudly instead of rejecting the whole label set and printing a hundred others in
    # English. Same trade as pill_ground and entry_not_required.
    page = re.sub(
        r'(<span class="source-confidence" data-source-confidence=")('
        + "|".join(SOURCE_CONFIDENCE_LEVELS) + r')(">)[^<]*(</span>)',
        lambda match: (f"{match.group(1)}{match.group(2)}{match.group(3)}"
                       f"{labels.get('confidence_' + match.group(2), match.group(2))}{match.group(4)}"),
        page,
    )
    # Allergy severity, on identical terms. The pill it sits in is the same pill the booking types
    # use, which is why the deny-list pattern for pills never covered it: that pattern names the
    # five booking types, and this is a different enum wearing the same class.
    page = re.sub(
        r'(<span class="pill allergy-severity" data-allergy-severity=")('
        + "|".join(ALLERGY_SEVERITIES) + r')(">)[^<]*(</span>)',
        lambda match: (f"{match.group(1)}{match.group(2)}{match.group(3)}"
                       f"{labels.get('severity_' + match.group(2), match.group(2))}{match.group(4)}"),
        page,
    )
    page = re.sub(
        r'(<article class="fact budget-item" data-budget-category="[a-z_]+"><strong>)([a-z_]+)(: )',
        lambda match: f"{match.group(1)}{categories.get(match.group(2), match.group(2))}{match.group(3)}",
        page,
    )
    page = re.sub(
        r'(<li class="unpriced-category">)([a-z_]+)(</li>)',
        lambda match: f"{match.group(1)}{categories.get(match.group(2), match.group(2))}{match.group(3)}",
        page,
    )
    page = re.sub(
        r'(<article class="dining-stop" data-meal="[a-z]+"><p class="eyebrow">)(' + "|".join(MEAL_TYPES) + r')( · )',
        lambda match: f"{match.group(1)}{meals[match.group(2)]}{match.group(3)}",
        page,
    )
    entry_labels = {
        "no_visa_required": labels["entry_no_visa_required"],
        "visa_required": labels["entry_visa_required"],
        "unverified": labels["entry_unverified"],
        # Optional keys, so a ui_labels set authored before the intake spellings existed keeps
        # validating instead of failing the whole page back to English.
        "not_required": labels.get("entry_not_required", "No visa required"),
        "required_held": labels.get("entry_required_held", "Visa required — already held"),
        "required_to_apply": labels.get("entry_required_to_apply", "Visa required — not yet applied for"),
    }
    page = re.sub(
        r'(<strong class="entry-status">)(' + "|".join(ENTRY_STATUSES) + r')(</strong>)',
        lambda match: f"{match.group(1)}{entry_labels[match.group(2)]}{match.group(3)}",
        page,
    )
    page = re.sub(
        r'(<strong>Ticket status: </strong>)(' + "|".join(BOOKING_STATES) + r')',
        lambda match: f"{match.group(1)}{states[match.group(2)]}",
        page,
    )
    page = re.sub(
        r'( · )(' + "|".join(BOOKING_STATES) + r')(</li>)',
        lambda match: f"{match.group(1)}{states[match.group(2)]}{match.group(3)}",
        page,
    )
    return page


# English words for the renderer's machine tokens. English markup is already English, so an English
# page needs no label set -- but its enum VALUES were printed raw: 'rental_car: £56–82',
# 'fuel_tolls_parking', 'rail_or_ground · available' on a synthetic English road trip (2026-09-24).
# Every key localize_enum_values and localize_access_tokens read is here, and
# tests/test_render_localization.py derives the list from the enum constants, so a new value
# without a word fails a test rather than printing raw.
ENGLISH_ENUM_LABELS = {
    **{f"state_{v}": v.capitalize() for v in BOOKING_STATES},
    **{f"meal_{v}": v.capitalize() for v in MEAL_TYPES},
    **{f"arrival_{v}": v.capitalize() for v in ARRIVAL_MODES},
    "mode_self_drive": "Self-drive", "mode_public_transit": "Public transport",
    "cat_flight": "Flights", "cat_rail": "Rail", "cat_intercity_bus": "Intercity bus",
    "cat_ferry": "Ferry", "cat_rental_car": "Rental car",
    "cat_fuel_tolls_parking": "Fuel, tolls and parking", "cat_accommodation": "Accommodation",
    "cat_food": "Food", "cat_local_transport": "Local transport", "cat_attractions": "Attractions",
    "cat_tours_and_activities": "Tours and activities", "cat_insurance": "Insurance",
    "cat_visa_and_entry": "Visa and entry", "cat_shopping_and_misc": "Shopping and other",
    "cat_contingency": "Contingency",
    **{f"confidence_{v}": v.capitalize() for v in SOURCE_CONFIDENCE_LEVELS},
    "severity_none": "None", "severity_preference": "Preference",
    "severity_intolerance": "Intolerance", "severity_severe": "Severe (can be life-threatening)",
    "entry_no_visa_required": "No visa required", "entry_visa_required": "Visa required",
    "entry_unverified": "Unverified", "entry_not_required": "No visa required",
    "entry_required_held": "Visa required — already held",
    "entry_required_to_apply": "Visa required — not yet applied for",
    "access_flight": "Flights", "access_accommodation": "Accommodation",
    "access_attraction_ticket": "Attraction tickets", "access_rental_car": "Rental car",
    "access_rail_or_ground": "Rail and ground transport", "access_available": "Available",
    "access_limited": "Limited", "access_unknown": "Unknown",
    "availability": "Availability: ",
}


def _is_english_page(language: object) -> bool:
    normalized = str(language or "").casefold()
    return normalized.startswith("en") or "english" in normalized


def set_author_text_aside(page: str) -> tuple[str, list[str]]:
    """Swap every fenced author passage for a placeholder no rule can match.

    The placeholder's digits are private-use characters too, so neither `\\d` nor `\\w` -- Python's
    `\\w` covers letters and digits of every script, but not private-use code points -- can see
    into it, and a unit rule cannot read the index of the passage as a number of minutes.
    """
    kept: list[str] = []

    def placeholder(text: str) -> str:
        kept.append(text)
        digits = "".join(chr(0xE010 + int(d)) for d in str(len(kept) - 1))
        return f"\ue002{digits}\ue003"

    # Links and data attributes are machine data, never copy: a provider name in data-provider must
    # still equal the button's label, which the delivery gate compares, and a URL must still open.
    # Lower-case machine tokens, numbers and dates stay visible to the rules, which anchor on them
    # (data-booking-purpose="review-option", data-meal="lunch"). aria-label, alt and title are not
    # included: they hold the renderer's own captions, and the author text inside them is fenced
    # where it is composed.
    # The page-age script's sentence templates (data-age-tpl and its siblings) are the renderer's
    # own sentences carried in attributes, and are translated by the same whole-value rule as
    # everywhere else.
    def keep_attribute(match: re.Match) -> str:
        value = match.group(2)
        if (re.fullmatch(r"[a-z0-9][a-z0-9_.-]*", value) or not value
                or html.unescape(value).strip() in renderer_sentences()):
            return match.group(0)
        return match.group(1) + placeholder(value) + match.group(3)

    page = re.sub(r'(\s(?:href|src|data-[a-z0-9-]+)=")([^"]*)(")', keep_attribute, page)
    page = re.sub("\ue000(.*?)\ue001", lambda m: placeholder(m.group(1)), page, flags=re.DOTALL)
    return page, kept


def restore_author_text(page: str, kept: list[str], lost: list[str] | None = None) -> str:
    """Put every passage back exactly as written; report any that no longer has a place.

    A passage can legitimately disappear: a custom label set may translate "Review option in
    {provider}" with a template that leaves the provider out, and that is the translator's call.
    So a missing passage is not an error here -- raising would refuse a page that rendered before
    the fence existed. Pass `lost` to collect them: the tests do, for the shipped Chinese labels
    and the example label set, where nothing may go missing, so a substitution rule that matches
    across author text without re-emitting it fails the day it is written.
    """
    seen: set[int] = set()

    def put_back(match: re.Match) -> str:
        index = int("".join(str(ord(c) - 0xE010) for c in match.group(1)))
        seen.add(index)
        return kept[index]

    page = re.sub("\ue002([\ue010-\ue019]+)\ue003", put_back, page)
    if lost is not None:
        lost.extend(kept[index] for index in sorted(set(range(len(kept))) - seen))
    return page.replace(AUTHOR_OPEN, "").replace(AUTHOR_CLOSE, "")


def localize_static_page(page: str, language: object, custom_labels: object = None) -> str:
    """Localize the renderer's own copy and leave every fenced author passage untouched."""
    page, kept = set_author_text_aside(page)
    return restore_author_text(_localize_renderer_text(page, language, custom_labels), kept)


def _localize_renderer_text(page: str, language: object, custom_labels: object = None) -> str:
    labels = labels_for(language, custom_labels)
    if not labels:
        if _is_english_page(language):
            # The markup is already English; only the machine tokens need words.
            return localize_access_tokens(localize_enum_values(page, ENGLISH_ENUM_LABELS),
                                          ENGLISH_ENUM_LABELS)
        return page

    page = localize_enum_values(page, labels)
    replacements = static_replacements(labels)
    return _apply_replacements(page, replacements, labels)


def static_replacements(labels: dict[str, str]) -> dict[str, str]:
    """Every renderer-owned English string, mapped to its localized form.

    Exposed rather than kept local so a test can assert that none of these KEYS survives into a
    localized page. That is the backstop for a hole this table itself has: the i18n validator
    fails only English it already knows about, so a caption invented after the validator was
    written is invisible to it. Four figure captions shipped English onto a Chinese page exactly
    that way, and every gate stayed green. The keys of this dict are, by construction, the
    complete list of what must never survive.
    """
    replacements = {
        # Renderer-owned fallbacks first: they are substrings of later, shorter keys.
        "Direct provider": labels["direct_provider_fallback"],
        "Map provider": labels["map_provider_fallback"],
        "Comparison platform": labels["comparison_platform_fallback"],
        "Not supplied": labels["not_supplied"],
        ">Review option<": f">{labels['review_option']}<",
        ">Open this segment in maps<": f">{labels['segment_map']}<",
        " night(s) · ": f" {labels.get('spine_nights', 'night(s)')} · ",
        # availability_status is a CLOSED enum that nothing ever translated, so every Chinese
        # page printed `unknown` in the middle of an otherwise Chinese booking card -- the exact
        # leak the closed-enum rule exists to prevent, in the one enum the rule forgot. Substituted
        # in its own printed context rather than as a bare word, because "unknown" also appears in
        # prose the traveller wrote.
        ">Availability: </strong>available": f">{labels['availability']}</strong>{labels.get('avail_available','available')}",
        ">Availability: </strong>limited": f">{labels['availability']}</strong>{labels.get('avail_limited','limited')}",
        ">Availability: </strong>unknown": f">{labels['availability']}</strong>{labels.get('avail_unknown','unknown')}",
        # The page-age strings are template ATTRIBUTES rather than visible text, and the script
        # substitutes N at open time. Replaced whole-value here for the same reason every other
        # renderer-owned string is: a Chinese page must not carry English, and validate_trip_html
        # reads attributes too.
        ">Your first hour on the ground<":
            f">{labels.get('essentials_heading', 'Your first hour on the ground')}<",
        ">Paying<": f">{labels.get('essentials_payment', 'Paying')}<",
        ">Getting online<": f">{labels.get('essentials_connectivity', 'Getting online')}<",
        ">If something goes wrong<":
            f">{labels.get('essentials_emergency', 'If something goes wrong')}<",
        ">Health and insurance<":
            f">{labels.get('essentials_health', 'Health and insurance')}<",
        ">Add this trip to your calendar<":
            f">{labels.get('calendar_add', 'Add this trip to your calendar')}<",
        CALENDAR_NOTE: labels.get("calendar_note", CALENDAR_NOTE),
        f'<span class="calendar-undecided-text">{CALENDAR_UNDECIDED}</span>':
            f'<span class="calendar-undecided-text">{labels.get("calendar_undecided", CALENDAR_UNDECIDED)}</span>',
        f'<span class="calendar-floating">{CALENDAR_FLOATING}</span>':
            f'<span class="calendar-floating">{labels.get("calendar_floating", CALENDAR_FLOATING)}</span>',
        '"Opened N day(s) after that research."':
            f'"{labels.get("age_since", "Opened N day(s) after that research.")}"',
        '"Departure is in N day(s)."':
            f'"{labels.get("age_until", "Departure is in N day(s).")}"',
        '"This trip has already started or passed."':
            f'"{labels.get("age_past", "This trip has already started or passed.")}"',
        '"Prices, opening hours and entry rules drift; treat every figure here as needing a recheck."':
            f'"{labels.get("age_stale", "Prices, opening hours and entry rules drift; treat every figure here as needing a recheck.")}"',
        ">Where you sleep<": f">{labels.get('spine_heading', 'Where you sleep')}<",
        ">Move day<": f">{labels.get('spine_move', 'Move day')}<",
        ">Each move is a day with a change of accommodation; the day cards below say which.<":
            f">{labels.get('spine_note', 'Each move is a day with a change of accommodation; the day cards below say which.')}<",
        ">Budget at a glance<": f">{labels['budget']}<",
        ">Comparable cost per person<": f">{labels['total']}<",
        ">Cap per person<": f">{labels.get('budget_cap', 'Cap per person')}<",
        ">Included assumptions<": f">{labels['included']}<",
        ">Ground-mobility plan<": f">{labels['ground']}<",
        ">Browse options — no purchase made<": f">{labels['browse']}<",
        ">Booking access checks<": f">{labels['booking_access_checks']}<",
        ">Source<": f">{labels['source_link']}<",
        ">Overall transport<": f">{labels['overall_transport']}<",
        ">Open overall route<": f">{labels['overall_route']}<",
        ">Open the airport transfer route — daily segments are below<": f">{labels['overall_route_overview']}<",
        ">Sources, confidence, and recheck list<": f">{labels['sources']}<",
        ">Sources used<": f">{labels['sources_used']}<",
        ">Recheck before purchase<": f">{labels['recheck_before']}<",
        ">No purchase options were requested for this plan.<": f">{labels['no_purchase_options']}<",
        '<span class="pill">flight<': f'<span class="pill">{labels.get("pill_flight", "flight")}<',
        '<span class="pill">hotel<': f'<span class="pill">{labels.get("pill_hotel", "hotel")}<',
        '<span class="pill">ticket<': f'<span class="pill">{labels.get("pill_ticket", "ticket")}<',
        '<span class="pill">car<': f'<span class="pill">{labels.get("pill_car", "car")}<',
        '<span class="pill">ground<': f'<span class="pill">{labels.get("pill_ground", "ground")}<',
        'aria-label="Schematic route in visit order"': f'aria-label="{labels.get("schematic_aria", "Schematic route in visit order")}"',
        '>Start</text>': f'>{labels.get("schematic_start", "Start")}</text>',
        '>End</text>': f'>{labels.get("schematic_end", "End")}</text>',
        '>Start</tspan>': f'>{labels.get("schematic_start", "Start")}</tspan>',
        '>End</tspan>': f'>{labels.get("schematic_end", "End")}</tspan>',
        "Price not currently verified": labels["price_unverified"],
        "Time not currently verified": labels["time_unverified"],
        "Up to ": labels["up_to"] + " ",
        "Conditions require recheck": labels["conditions_recheck"],
        "Price per person, round trip: ": labels["price_per_person"],
        "Price per room/night: ": labels["price_per_room_night"],
        "Trip total for stay: ": labels["price_trip_total"],
        "Ticket price per person: ": labels["price_ticket"],
        "Vehicle price per day: ": labels["price_car_day"],
        "Availability: ": labels["availability"],
        "Price checked: ": labels["price_checked"],
        "Price status: ": labels["price_status"],
        "Outbound: ": labels["outbound"],
        "Return: ": labels["return"],
        "Station and access: ": labels.get("station_access", "Station and access: "),
        "Location and access: ": labels["hotel_location"],
        "Guest rating: ": labels.get("guest_rating_label", "Guest rating: "),
        "Why it fits: ": labels["hotel_fit"],
        "Destination essentials": labels["destination_essentials"],
        "Budget breakdown": labels["budget_breakdown"],
        "Backup: ": labels["dining_backup"],
        "Arranged independently": labels["arranged_independently"],
        "Checkout / no overnight stay": labels["departure_checkout"],
        "Schematic — not for navigation. Stops are shown in visit order; use the live map for directions.": labels["schematic"],
        "Recheck operating conditions before departure.": labels["operating_recheck"],
        "No verified ticket is required for the listed activities.": labels["no_ticket"],
        "Keep a flexible alternative for disruptions.": labels["contingency"],
        "Plan evidence": labels["plan_evidence"],
        "Recheck price, availability, entry requirements, and operating conditions before purchase.": labels["default_recheck"],
        "Prices and availability require recheck before purchase.": labels["price_recheck"],
        "Current researched options only. Opening a link never creates a reservation.": labels["no_reservation"],
        "No meal recommendation was researched.": labels["no_meal_recommendation"],
        "Check current opening hours before switching.": labels["opening_hours_recheck"],
        "Rating: ": labels.get("rating_label", "Rating: "),
        "no public rating": labels.get("rating_none", "no public rating"),
        " reviews": labels.get("rating_reviews", " reviews"),
        # The hours provenance word is anchored inside its own span: bare "researched" also
        # appears as a source-confidence default, and a loose replacement would translate that
        # unrelated word too.
        **{
            f'<span class="dining-hours-status">{english}</span>':
                f'<span class="dining-hours-status">{labels.get(HOURS_STATUS_LABEL_KEYS[status], english)}</span>'
            for status, english in HOURS_STATUS_ENGLISH.items()
        },
        "Opening hours: ": labels.get("venue_hours_label", "Opening hours: "),
        ">closed today ·": f">{labels.get('hours_closed_today', 'closed today')} ·",
        " (today) ·": f"{labels.get('hours_today_suffix', ' (today)')} ·",
        # Anchored on the whole paragraph the renderer emits rather than on the bare word:
        # "Ticket: " is ordinary prose that an author may well have written inside an activity
        # detail or a source note, and a loose replacement would translate the traveller's own
        # text. Same reasoning as the dining hours-status span directly above.
        '<p class="meta ticket-note"><strong>Ticket: </strong>':
            f'<p class="meta ticket-note"><strong>{labels.get("ticket_note_label", "Ticket: ")}</strong>',
        # The sale window, anchored on its own markup for the same reason as the ticket note.
        '<strong>Ticket sale: </strong><span class="ticket-sale-status">':
            f'<strong>{labels.get("ticket_sale_label", "Ticket sale: ")}</strong>'
            '<span class="ticket-sale-status">',
        **{
            f'<span class="ticket-sale-status">{english}</span>':
                f'<span class="ticket-sale-status">{labels.get(TICKET_SALE_LABEL_KEYS[status], english)}</span>'
            for status, english in TICKET_SALE_ENGLISH.items()
        },
        f'<span class="ticket-sale-status">{TICKET_SALE_UNKNOWN}</span>':
            f'<span class="ticket-sale-status">{labels.get("ticket_sale_unknown", TICKET_SALE_UNKNOWN)}</span>',
        # The self-transfer warning: label and sentence are two keys, each anchored on its own
        # markup, so a label set that translates one and not the other leaves an English key on
        # the page that validate_trip_html.py finds. As one combined key, a translated label hid an
        # English sentence from the gate.
        '<strong>Self-transfer: </strong><span class="self-transfer-sentence">':
            f'<strong>{labels.get("self_transfer_label", "Self-transfer: ")}</strong>'
            '<span class="self-transfer-sentence">',
        '<span class="booking-state">Booked</span>':
            f'<span class="booking-state">{labels.get("booking_booked", "Booked")}</span>',
        '<span class="booking-state">Chosen — not booked yet</span>':
            f'<span class="booking-state">{labels.get("booking_chosen", "Chosen — not booked yet")}</span>',
        '<span class="booking-via">via</span>': f'<span class="booking-via">{labels.get("booking_via", "via")}</span>',
        '<span class="booking-paid">paid</span>': f'<span class="booking-paid">{labels.get("booking_paid", "paid")}</span>',
        '<span class="booking-confirmed">(user-confirmed)</span>':
            f'<span class="booking-confirmed">{labels.get("booking_confirmed", "(user-confirmed)")}</span>',
        '<summary class="not-chosen-summary">Alternatives not booked ':
            f'<summary class="not-chosen-summary">{labels.get("booking_alternatives", "Alternatives not booked")} ',
        "<h2>Your bookings and options</h2>": f'<h2>{labels.get("booking_heading", "Your bookings and options")}</h2>',
        "<span>Booked so far (user-confirmed)</span>":
            f'<span>{labels.get("booked_so_far", "Booked so far (user-confirmed)")}</span>',
        "<span>Groups still to book</span>": f'<span>{labels.get("still_to_book", "Groups still to book")}</span>',
        **{f'<span class="reservation-need" data-reservation-need="{need}">{english}</span>':
               f'<span class="reservation-need" data-reservation-need="{need}">{labels.get(f"reservation_{need}", english)}</span>'
           for need, english in RESERVATION_NEED_ENGLISH.items()},
        f'<span class="self-transfer-sentence">{SELF_TRANSFER_SENTENCE}</span>':
            f'<span class="self-transfer-sentence">{labels.get("self_transfer_sentence", SELF_TRANSFER_SENTENCE)}</span>',
        " per person · ": f" {labels['per_person_suffix']} · ",
        ">Not fact-checked<": f">{labels.get('unverified_banner_title', 'Not fact-checked')}<",
        # NOTE: this key must stay byte-identical to the sentence emitted at :2079. It is a
        # substitution table keyed on the rendered English, so editing the banner without editing
        # this key leaves English on a Chinese page and the i18n gate then fails the file.
        ("No verification pass is recorded for this plan. Its fares, opening hours, entry rules, "
         "and availability have not been checked against operators or official sources. Treat "
         "every figure as an estimate and verify before booking."):
            labels.get("unverified_banner_body",
                       "No verification pass is recorded for this plan. Its fares, opening hours, "
                       "entry rules, and availability have not been checked against operators or "
                       "official sources. Treat every figure as an estimate and verify before "
                       "booking."),
        # NOTE: keyed byte-identically on the sentence emitted by destination_anchor_cards.
        # Editing one without the other leaks English onto a Chinese page, and the i18n gate
        # then fails the file -- which is how this table is meant to work, but the failure is
        # cheaper to avoid than to debug.
        "<strong>You asked for: </strong>":
            f"<strong>{labels.get('anchor_serves_label', 'You asked for: ')}</strong>",
        # The photo credit. Not politeness: these are CC BY / CC BY-SA files and the attribution
        # is the condition under which they may sit in this file at all, so it localizes like any
        # other renderer sentence rather than staying English on a Chinese page.
        "<figcaption class=\"photo-credit\">Photo credit: ":
            f"<figcaption class=\"photo-credit\">{labels.get('photo_credit_label', 'Photo credit')}: ",
        " · via Wikimedia, from the article ":
            f" · {labels.get('photo_source_label', 'via Wikimedia, from the article')} ",
        # The four figure captions. They are also each figure's SVG <title>, so one entry
        # localizes both the visible caption and the accessible name. Added here because the
        # i18n gate only fails English it already knows about -- a caption invented after the
        # gate was written is invisible to it, which is how these shipped English on a Chinese
        # page in the first draft and nothing fired.
        "Minutes on foot per day: connecting legs plus time on foot at each stop":
            labels.get("fig_walking_caption",
                       "Minutes on foot per day: connecting legs plus time on foot at each stop"),
        "Relative positions, in visit order. Use the map button to navigate.":
            labels.get("fig_map_caption",
                       "Relative positions, in visit order. Use the map button to navigate."),
        "Share of the per-person total, and how much of the cap it uses":
            labels.get("fig_budget_caption",
                       "Share of the per-person total, and how much of the cap it uses"),
        "Fixed points across the day":
            labels.get("fig_shape_caption", "Fixed points across the day"),
        " · Longest single walk: ":
            f" · {labels.get('fig_longest_walk', 'Longest single walk')}: ",
        ">Your constraints<": f">{labels.get('constraints_heading', 'Your constraints')}<",
        "Allergy severity: ": labels.get("constraints_severity", "Allergy severity: "),
        "Dietary needs: ": labels.get("constraints_dietary", "Dietary needs: "),
        "Mobility: ": labels.get("constraints_mobility", "Mobility: "),
        "Maximum continuous walking: ": labels.get("constraints_walk_cap", "Maximum continuous walking: "),
        "Allergy card — show this to staff: ": labels.get("constraints_card", "Allergy card — show this to staff: "),
        "Changed since your form: ": labels.get("intake_changed_heading", "Changed since your form: "),
        "Re-checked after the main verification: ": labels.get("rechecked_heading", "Re-checked after the main verification: "),
        "<strong>Restrictions: </strong>": f"<strong>{labels.get('rental_restriction_label', 'Restrictions: ')}</strong>",
        " · straight-line span ": f" · {labels.get('fig_straight_line', 'straight-line span')} ",
        ">Open the route overview — daily segments are below<": f">{labels.get('overall_route_overview_general', 'Open the route overview — daily segments are below')}<",
        "The transport tickets for this day are under Browse options above.": labels.get("transport_tickets_pointer", "The transport tickets for this day are under Browse options above."),
        '<span class="recheck-part">Entry eligibility</span>': f'<span class="recheck-part">{labels.get("recheck_part_entry", "Entry eligibility")}</span>',
        '<span class="recheck-part">First hour on the ground</span>': f'<span class="recheck-part">{labels.get("recheck_part_arrival", "First hour on the ground")}</span>',
        '<span class="recheck-part">Budget</span>': f'<span class="recheck-part">{labels.get("recheck_part_budget", "Budget")}</span>',
        '<span class="recheck-part">Transport overview</span>': f'<span class="recheck-part">{labels.get("recheck_part_transport", "Transport overview")}</span>',
        '<span class="recheck-part">Other trip details</span>': f'<span class="recheck-part">{labels.get("recheck_part_other", "Other trip details")}</span>',
        "Party size: ": labels.get("intake_field_party", "Party size: "),
        "Budget cap per person: ": labels.get("intake_field_cap", "Budget cap per person: "),
        ">What you asked for<": f">{labels.get('preferences_heading', 'What you asked for')}<",
        "Experience direction: ": labels.get("preferences_direction", "Experience direction: "),
        "Asked to avoid: ": labels.get("preferences_avoid", "Asked to avoid: "),
        "Structure checks passed: ": labels.get("gates_label", "Structure checks passed: "),
        "They prove the plan agrees with itself, never that its facts are true.":
            labels.get("gates_caveat",
                       "They prove the plan agrees with itself, never that its facts are true."),
        "Why these providers: ": labels.get("why_providers", "Why these providers: "),
        "Plan status · ": labels["plan_status_prefix"],
        "Arrival: ": labels["arrival"],
        " · Pace: ": f" · {labels['pace']}",
        " · Currency: ": f" · {labels['currency']}",
        " · Research last checked: ": f" · {labels['last_checked']}",
        "Provider: ": labels["provider"],
        # After the labelled "Provider: " key, so the bare option-card fallback is caught too.
        "Provider": labels["provider_fallback"],
        " · Compared via: ": f" · {labels['compared']}",
        " · Checked: ": f" · {labels['checked']}",
        " · Source: ": f" · {labels['source']}",
        " guest(s) · ": f" {labels['guest']} · ",
        " room(s)": f" {labels['room']}",
        "Fare conditions: ": labels["fare_conditions_label"],
        "Ticket status: ": labels["ticket_state_label"],
        "Only one option shown: ": labels["single_option_label"],
        "Fallback: ": labels["route_fallback_label"],
        "Walking across the day: ": labels["walking_burden_label"],
        "Platform selection: ": labels["platform_note_label"],
        ">Unpriced categories<": f">{labels['unpriced_categories']}<",
        ">Planning assumptions<": f">{labels['planning_assumptions']}<",
        ">On this page<": f">{labels['nav_label']}<",
        ">Budget<": f">{labels['nav_budget']}<",
        ">Options<": f">{labels['nav_options']}<",
        ">Transport<": f">{labels['nav_transport']}<",
        ">Sources<": f">{labels['nav_sources']}<",
        "<h2>Entry eligibility</h2>": f"<h2>{labels['entry_heading']}</h2>",
        "Basis: ": labels["entry_basis"],
        "<h3>Flight options</h3>": f"<h3>{labels['group_flight']}</h3>",
        "<h3>Rail, coach and ferry options</h3>": f"<h3>{labels.get('group_ground', 'Rail, coach and ferry options')}</h3>",
        "<h3>Accommodation options</h3>": f"<h3>{labels['group_hotel']}</h3>",
        "<h3>Ticket options</h3>": f"<h3>{labels['group_ticket']}</h3>",
        "<h3>Rental-car options</h3>": f"<h3>{labels['group_car']}</h3>",
        ">Start<": f">{labels['route_start']}<",
        ">End<": f">{labels['route_end']}<",
        "No separate ticket is required or it was not verified.": labels["no_separate_ticket"],
    }
    return replacements


def localize_access_tokens(page: str, labels: dict[str, str]) -> str:
    """The booking-access categories and statuses, printed as words. Shared by the translated
    path and the English one, because both have to turn `rail_or_ground · available` into text."""
    access_categories = {
        "flight": labels["access_flight"],
        "accommodation": labels["access_accommodation"],
        "attraction_ticket": labels["access_attraction_ticket"],
        "rental_car": labels["access_rental_car"],
        "rail_or_ground": labels["access_rail_or_ground"],
    }
    access_statuses = {
        "available": labels["access_available"],
        "limited": labels["access_limited"],
        "unknown": labels["access_unknown"],
    }
    page = re.sub(
        r'(<strong>)(flight|accommodation|attraction_ticket|rental_car|rail_or_ground) · (available|limited|unknown)(</strong>)',
        lambda match: f"{match.group(1)}{access_categories[match.group(2)]} · {access_statuses[match.group(3)]}{match.group(4)}",
        page,
    )
    page = re.sub(
        rf'(<strong>{re.escape(labels["availability"])}</strong>)(available|limited|unknown)',
        lambda match: f"{match.group(1)}{access_statuses[match.group(2)]}",
        page,
    )
    return page


def _apply_replacements(page: str, replacements: dict[str, str], labels: dict[str, str]) -> str:
    for source, target in replacements.items():
        page = page.replace(source, target)

    page = re.sub(
        r'(data-booking-purpose="(?:review-option|rental-search)"[^>]*>)Review option in ([^<]+)(</a>)',
        lambda match: f"{match.group(1)}{labels['review_option_provider'].replace('{provider}', match.group(2))}{match.group(3)}",
        page,
    )
    page = re.sub(
        r'(data-booking-purpose="direct-provider"[^>]*>)Review direct provider in ([^<]+)(</a>)',
        lambda match: f"{match.group(1)}{labels['direct_provider'].replace('{provider}', match.group(2))}{match.group(3)}",
        page,
    )
    page = re.sub(
        # The platform name sits inside the label so a card headed "Transavia" cannot open
        # Skyscanner without saying so, the way the hotel button already names Booking.com.
        # It is captured rather than translated: a provider name is a proper noun.
        #
        # `labels.get`, and it took a KeyError to earn the four characters. `round_trip_in` is in
        # OPTIONAL_UI_LABEL_KEYS -- so a ui_labels set authored before that key existed passes
        # validate_plan whole -- and this line subscripted it anyway, which meant that plan did
        # not print one English button among its hundred translated strings: it raised
        # `KeyError: 'round_trip_in'` and produced no page at all. The English fallback is the
        # exact sentence the renderer emitted, so the substitution becomes a no-op and
        # validate_trip_html.py's RENDERER_ENGLISH_TEXT pattern "Search round trip" then fails
        # that one page loudly -- which is the trade every other optional key in this function
        # already makes, and the one this line was silently opted out of.
        r'(data-booking-purpose="round-trip-search"[^>]*>)Search round trip in ([^—<]+) — ([^<]+)(</a>)',
        lambda match: (f"{match.group(1)}"
                       f"{labels.get('round_trip_in', 'Search round trip in {provider}').replace('{provider}', match.group(2).strip())}"
                       f" — {match.group(3).replace(' to ', labels['to'])}{match.group(4)}"),
        page,
    )
    page = re.sub(
        r'(data-booking-purpose="comparison-search"[^>]*>)Compare on Booking\.com — dates and guests included(</a>)',
        lambda match: f"{match.group(1)}{labels['compare_booking']}{match.group(2)}",
        page,
    )
    page = re.sub(
        r'(data-booking-purpose="comparison-search"[^>]*>)Compare on ([^<]+) — dates and guests included(</a>)',
        lambda match: f"{match.group(1)}{labels['compare_platform_prefix']}{match.group(2)}{labels['compare_platform_suffix']}{match.group(3)}",
        page,
    )
    page = re.sub(
        r'(data-booking-type="ticket"[^>]*>)Review ticket: ([^<]+)(</a>)',
        lambda match: f"{match.group(1)}{labels['ticket_prefix']}{match.group(2)}{match.group(3)}",
        page,
    )
    page = re.sub(
        r'(\d+)h (\d+)m',
        lambda match: f"{match.group(1)}{labels['hour']}{match.group(2)}{labels['minute']}",
        page,
    )
    page = re.sub(
        r'\bWalk (\d+) min\b',
        lambda match: f"{labels['walk']} {match.group(1)}{labels['minute']}",
        page,
    )
    page = re.sub(
        r'\b(\d+) transfer\(s\)',
        lambda match: f"{match.group(1)}{labels['transfers']}",
        page,
    )
    page = re.sub(r'(\d+) minutes?\b', lambda match: f"{match.group(1)}{labels['minute']}", page)
    page = re.sub(r'(\d+) min\b', lambda match: f"{match.group(1)}{labels['minute']}", page)
    # These were hardcoded Chinese inside a function every non-English page runs, so a French or
    # Japanese itinerary shipped "82公里" on every segment and "直飞" on every flight card while all
    # four gates reported it valid -- the exact failure the i18n rule exists to prevent, in the one
    # branch that rule cannot see.
    #
    # Two refinements since. First, a through train is not a 直飞 -- that word means specifically
    # "direct by air" -- so the ground branch counts "change(s)", the right English for rail and a
    # marker this flight-shaped substitution cannot claim. `stops_suffix` ("次中转") is
    # vehicle-neutral, so only the zero case needed a twin.
    #
    # Second, the zero cases substitute ONLY when the label exists. `labels.get("nonstop",
    # "non-stop")` printed an English word on a French page that no gate pattern recognises, and
    # "non-stop" and "direct" are both too common in real prose to be safely matchable. Falling
    # through leaves the count for the sibling rule below, and if that label is missing too the
    # page keeps `0 stop(s)` / `0 change(s)`, which RENDERER_ENGLISH_TEXT does catch. Elsewhere an
    # English fallback keeps an incomplete label set readable; here it would keep it silent, and
    # the whole point of the rule is that an untranslated label must be loud.
    #
    # Read into a local instead of re-subscripting inside the guard. The guard already made
    # `labels["nonstop"]` safe, so this changes no behaviour -- it removes the last two hard
    # subscripts on OPTIONAL keys in this file, which is what lets a test state the invariant
    # mechanically ("no labels[<optional key>] anywhere") instead of a reader having to check
    # each one for a guard. `round_trip_in`, four rules up, is the one that had no guard.
    nonstop_ground = labels.get("nonstop_ground")
    if nonstop_ground:
        page = re.sub(r'\b0 change\(s\)', nonstop_ground, page)
    nonstop = labels.get("nonstop")
    if nonstop:
        page = re.sub(r'\b0 stop\(s\)', nonstop, page)
    page = re.sub(r'\b(\d+) change\(s\)',
                  lambda match: f"{match.group(1)}{labels.get('stops_suffix', ' stop(s)')}", page)
    page = re.sub(r'\b(\d+) stop\(s\)',
                  lambda match: f"{match.group(1)}{labels.get('stops_suffix', ' stop(s)')}", page)
    page = re.sub(r'(\d+(?:\.\d+)?) km\b',
                  lambda match: f"{match.group(1)}{labels.get('unit_km', ' km')}", page)
    page = re.sub(
        r'<p class="eyebrow">Day ([^<]+) · ([^<]+)</p>',
        lambda match: f'<p class="eyebrow">{labels["day"]}{match.group(1)}{labels["day_suffix"]} · {match.group(2)}</p>',
        page,
    )
    page = re.sub(
        r'aria-label="Day (\d+)"',
        lambda match: f'aria-label="{labels["day"]}{match.group(1)}{labels["day_suffix"]}"',
        page,
    )
    page = re.sub(
        r'(<span class="day-nav-day">)Day (\d+)(</span>)',
        lambda match: f'{match.group(1)}{labels["day"]}{match.group(2)}{labels["day_suffix"]}{match.group(3)}',
        page,
    )
    page = page.replace('aria-label="On this page"', f'aria-label="{labels["nav_label"]}"')
    page = re.sub(
        r'(<header id="trip-summary" class="hero">.*?</h1><p>)([^<]+) → ([^<]+) · (\d{4}-\d{2}-\d{2}) to (\d{4}-\d{2}-\d{2}) · ([^<]+) traveller\(s\)(</p>)',
        lambda match: f'{match.group(1)}{match.group(2)} → {match.group(3)} · {match.group(4)}{labels["to"]}{match.group(5)} · {match.group(6)}{labels["travellers"]}{match.group(7)}',
        page,
        flags=re.DOTALL,
    )
    page = page.replace('<h3>Stay</h3>', f'<h3>{labels["stay"]}</h3>')
    page = page.replace('<h3>Plan</h3>', f'<h3>{labels["plan"]}</h3>')
    page = page.replace('<h3>Dining suggestions</h3>', f'<h3>{labels["dining"]}</h3>')
    page = page.replace('<h3>Route and mobility</h3>', f'<h3>{labels["route"]}</h3>')
    page = page.replace('>Open full-day route<', f'>{labels["full_day_route"]}<')
    page = page.replace('>Open route overview — see segments below<', f'>{labels["full_day_route_overview"]}<')
    page = re.sub(
        r'>Open full-day route in ([^<]+)<',
        lambda match: ">" + labels["full_day_route_provider"].replace("{provider}", match.group(1)) + "<",
        page,
    )
    page = re.sub(
        r'>Open route overview in ([^<]+) — see segments below<',
        lambda match: ">" + labels["full_day_route_overview_provider"].replace("{provider}", match.group(1)) + "<",
        page,
    )
    page = re.sub(
        r'>Open this segment in ([^<]+)<',
        lambda match: ">" + labels["segment_map_provider"].replace("{provider}", match.group(1)) + "<",
        page,
    )
    page = re.sub(
        r'>Open overall route in ([^<]+)<',
        lambda match: ">" + labels["overall_route_provider"].replace("{provider}", match.group(1)) + "<",
        page,
    )
    page = re.sub(
        r'>Open the route overview in ([^<]+) — daily segments are below<',
        lambda match: ">" + labels.get("overall_route_overview_general_provider",
                                       "Open the route overview in {provider} — daily segments are below"
                                       ).replace("{provider}", match.group(1)) + "<",
        page,
    )
    page = re.sub(
        r'>Open the airport transfer route in ([^<]+) — daily segments are below<',
        lambda match: ">" + labels["overall_route_overview_provider"].replace("{provider}", match.group(1)) + "<",
        page,
    )
    page = re.sub(
        r'>Open alternative route in ([^<]+)<',
        lambda match: ">" + labels["alternative_map_provider"].replace("{provider}", match.group(1)) + "<",
        page,
    )
    page = re.sub(
        r'>View restaurant in ([^<]+)<',
        lambda match: ">" + labels["dining_map"].replace("{provider}", match.group(1)) + "<",
        page,
    )
    page = localize_access_tokens(page, labels)
    page = page.replace('<h4>Route by segment</h4>', f'<h4>{labels["route_by_segment"]}</h4>')
    page = page.replace('<h3>Tickets and recheck</h3>', f'<h3>{labels["tickets"]}</h3>')
    page = page.replace('<time>Flexible</time><div><strong>Free time</strong>', f'<time>{labels["flexible_time"]}</time><div><strong>{labels["free_time"]}</strong>')
    page = page.replace('<time>Flexible</time>', f'<time>{labels["flexible_time"]}</time>')
    page = page.replace('>Review reservation<', f'>{labels["review_reservation"]}<')
    page = page.replace('>View source<', f'>{labels["view_source"]}<')
    page = re.sub(
        r'<span class="pill">Day ([^<]+)<',
        lambda match: f'<span class="pill">{labels["day"]}{match.group(1)}{labels["day_suffix"]}<',
        page,
    )
    # Price provenance is decision-critical: do not leave machine enum values in an
    # otherwise localized checkout-facing page. These replacements only affect
    # renderer-owned visible text, never URLs or data attributes.
    for price_status in PRICE_STATUSES:
        status_label = labels.get(f"price_{price_status}", price_status)
        page = page.replace(f"</strong>{price_status}", f"</strong>{status_label}")
        page = page.replace(f">{price_status} ·", f">{status_label} ·")
    return page


def as_number(value: object) -> float:
    """A number, or 0.0. Figures must not raise on a field the plan left blank."""
    return float(value) if isinstance(value, (int, float)) and not isinstance(value, bool) else 0.0


def as_list(value: object) -> list:
    """Normalise a field the contract declares as a list of strings.

    Iterating a str yields its characters, so a field written as one string instead of a
    one-element list renders as every character joined by the separator: a whole paragraph
    came out as "这 · 是 · 路 · 线 · 概 · 览" on a delivered page, and every gate passed it
    because the value was a perfectly good string and the join was perfectly good code.
    A lone string is semantically one note, so read it as one rather than exploding it --
    the renderer must not be able to produce that output at all. validate_plan reports the
    type mismatch separately so the data still gets fixed at the source.
    """
    if value is None:
        return []
    if isinstance(value, str):
        return [value] if value.strip() else []
    if isinstance(value, (list, tuple)):
        return list(value)
    return [value]


def as_text(value: object, fallback: str = "Not supplied") -> str:
    if value is None or value == "":
        return fallback
    return str(value)


# Author text is fenced where it is escaped, so localization can tell it from the renderer's own
# words. A non-English page is made by rendering English and then substituting renderer strings
# and unit patterns across the page -- and until 2026-10-10 every one of those rules also ran over
# whatever the author wrote: "no walk longer than 30 minutes" came out 「…30分钟」, "Provider
# recommends" came out 「供应商 recommends」, and all 96 substitution keys rewrote an activity's
# detail when probed. The fence is two private-use characters: html.escape leaves them alone, no
# substitution key or rule contains one, and localize_static_page() removes every one of them.
AUTHOR_OPEN = "\ue000"
AUTHOR_CLOSE = "\ue001"


def shield(value: object) -> str:
    """Fence one piece of author text inside a string the renderer composes.

    For a line that mixes the renderer's words with the author's -- "Review option in {provider}",
    a segment's "15 min · 12 km · {fare basis}" -- escape the whole line with markup(), and pass
    each author piece through this first, so the renderer's words are translated and the author's
    are not. Text without a letter in any script is left unfenced: dates, times, prices and counts
    are what the structural rules (a hero line's "2026-10-17 to 2026-10-20") read, and none of
    them is a sentence a rule could damage.
    """
    text = str(value).replace(AUTHOR_OPEN, "").replace(AUTHOR_CLOSE, "")
    if not any(character.isalpha() for character in text):
        return text
    # A value that IS one of the renderer's own sentences, word for word, was copied from the
    # renderer -- the shipped fixture's recheck list holds the renderer's default recheck sentence
    # -- and is translated as the renderer's. Whole-value equality only: a sentence that merely
    # contains a renderer phrase is the author's and stays as written.
    if text.strip() in renderer_sentences():
        return text
    return f"{AUTHOR_OPEN}{text}{AUTHOR_CLOSE}"


@lru_cache(maxsize=1)
def renderer_sentences() -> frozenset[str]:
    """The renderer's own plain-text strings, from the substitution table's keys."""
    keys = static_replacements(labels_for("zh-CN"))
    sentences = set()
    for key in keys:
        # A key quoted as an attribute value ('"Opened N day(s) after that research."') is the
        # same sentence, anchored on its quotes; the page-age templates are keyed that way.
        if len(key) > 2 and key.startswith('"') and key.endswith('"'):
            key = key[1:-1]
        if "<" not in key and ">" not in key and '"' not in key and key.strip():
            sentences.add(key.strip())
    return frozenset(sentences)


def markup(text: object) -> str:
    """Escape a line the renderer composed; fences already inside it are kept."""
    return html.escape(str(text), quote=True)


def told(value: object) -> str:
    """One author piece of a composed line: fenced when present, empty when absent."""
    return "" if value is None or value == "" else shield(value)


def printed(value: object, fallback: str) -> str:
    """The author's value fenced, or the renderer's own fallback word unfenced so it is translated.

    For a line like "Review option in {provider}": a plan that names no provider prints the
    renderer's "Provider", which must still become 「供应商」, while a named one must not be touched.
    """
    return fallback if value is None or value == "" else shield(value)


def vocab(value: object, fallback: str = "Not supplied") -> str:
    """A closed-enum value, which is the renderer's vocabulary and is translated by an anchored rule."""
    return markup(as_text(value, fallback))


def esc(value: object, fallback: str = "Not supplied") -> str:
    """Escape a value from the plan and fence it as the author's.

    The fallback is the renderer's own word ("Not supplied") and stays unfenced, so it is still
    translated. A caller passing a line the renderer composed must use markup() instead, or its
    words will never be translated -- validate_trip_html.py then fails the page for renderer English,
    which is loud, and the right direction to fail in.
    """
    if value is None or value == "":
        return html.escape(fallback, quote=True)
    return markup(shield(value))


def recheck_part_label(plan: dict, section: str) -> str:
    """A rechecked section as the traveller knows it: the day, the hotel, or the panel.

    Never the JSON key: `booking_options.accommodations[stay-b]` on a page is the plan's own
    vocabulary leaking to the person reading it.
    """
    days = plan.get("days") if isinstance(plan.get("days"), list) else []
    if section.startswith("days[") and section.endswith("]"):
        date = section[len("days["):-1]
        for day in days:
            if isinstance(day, dict) and str(day.get("date") or "") == date:
                return f'<span class="pill">Day {esc(day.get("number"))}</span> {esc(date)}'
    if section.startswith("booking_options.") and section.endswith("]") and "[" in section:
        kind, _, option_id = section[len("booking_options."):-1].partition("[")
        options = (plan.get("booking_options") or {}).get(kind)
        for option in options if isinstance(options, list) else []:
            if isinstance(option, dict) and str(option.get("id") or "") == option_id:
                name = (option.get("property_name") or option.get("attraction_name")
                        or option.get("provider") or option_id)
                return esc(name)
    label = RECHECK_PART_LABELS.get(section, RECHECK_PART_OTHER)
    return f'<span class="recheck-part">{label}</span>'


def stamp(value: object) -> str:
    """Show a check time a person can read; the machine form stays in data attributes."""
    if isinstance(value, str) and value.strip():
        try:
            if len(value.strip()) == 10:
                return html.escape(date.fromisoformat(value.strip()).isoformat(), quote=True)
            moment = datetime.fromisoformat(value.strip().replace("Z", "+00:00"))
        except ValueError:
            return esc(value)
        return html.escape(moment.strftime("%Y-%m-%d %H:%M"), quote=True)
    return esc(value)


def attr(value: object) -> str:
    return html.escape(str(value), quote=True)


def enum_cell(css_class: str, attribute: str, value: object, fallback: str) -> str:
    """Print a renderer-owned enum value with its machine token kept beside it.

    Two things ride on this shape, and both were missing when a source's `confidence` was spliced
    into the source register as a bare `{esc(...)}`:

    1. LOCALIZATION. `localize_enum_values` anchors every substitution on the exact markup the
       renderer emits, because the same tokens also live in URLs and data attributes that must
       stay machine-readable. A value with no anchor around it cannot be translated without a
       page-wide search-and-replace, and a page-wide replace is how this file once translated the
       word "researched" inside an author's own sentence. The span IS the anchor.

    2. DETECTION. validate_trip_html.py's structural i18n check compares an element's rendered
       text against the machine token in its own `data-` attribute: still equal on a page whose
       `<html lang>` is not English means nothing translated it. That comparison needs no list of
       known English words -- which is the entire point, because the hand-maintained deny-list is
       what missed `confidence` for the whole life of the feature. Any FUTURE enum printed through
       this helper is checked the day it is added, with no edit to the validator at all.

    `fallback` is deliberately required rather than defaulted: an enum cell exists to show one of
    a known set of values, so the value shown when the plan recorded nothing is a decision the
    caller has to make in the open. Defaulting it here is how "researched" became a hardcoded
    English word in the first place.
    """
    # A value that is present but not a string is stringified rather than swapped for the
    # fallback. Substituting the default would quietly turn a wrong value into a plausible one --
    # a plan whose confidence field holds a number would read "researched" to the traveller and
    # to anyone auditing the page, with nothing anywhere recording that the plan said otherwise.
    # validate_plan rejects such a value before it ever renders; this is what the page does if it
    # is rendered anyway, and showing the odd value is the honest half of that.
    if isinstance(value, str):
        token = value.strip() or fallback
    elif value is None:
        token = fallback
    else:
        token = str(value)
    # markup(), not esc(): the value is the renderer's own vocabulary, which localization replaces
    # whole, so fencing it as author text would hide it from the rule written to translate it.
    return f'<span class="{css_class}" data-{attribute}="{attr(token)}">{markup(token)}</span>'


def visible_text(value: object) -> str:
    """What a reader can actually SEE in this value. Everything else is the empty string.

    `str(value or "").strip()` is the idiom this replaces, and it answers a different question
    than the one being asked. Two shapes get through it, both measured against the real gate:

      * **A non-string.** `summary: ["x", "y"]` became the string `"['x', 'y']"`, which is not
        empty, so the gate passed it -- and the page printed `['x', 'y']` to the traveller. The
        contract cannot catch this either: templates/final-trip-plan.json writes free text as
        `null` on purpose (a specimen string is a string somebody ships verbatim), so
        check_plan_contract.py has no declared type to compare against. A list is not prose, and
        pretending it is turned a type error into rendered output.
      * **Invisible characters.** `str.strip()` removes whitespace, and U+200B ZERO WIDTH SPACE is
        not whitespace to Python. A summary of one zero-width space satisfied "non-empty" and
        rendered a card with a heading and nothing under it. Same for the BOM, soft hyphen, the
        bidi marks, and unassigned code points -- every one of them counts as content to `strip()`
        and as blank to a human. That is the exact failure this block exists to prevent: a gate
        that says filled, a page that shows nothing.

    So: strings only, and only their visible glyphs. Unicode categories C (control, format,
    unassigned, private use, surrogate) and Z (every separator, not just ASCII space) are dropped
    before the emptiness test. CJK, digits, punctuation and emoji all survive -- the test is
    "would a reader see something", not "is this Latin", which is the mistake this file has made
    four times in other places.
    """
    if not isinstance(value, str):
        return ""
    return "".join(ch for ch in value
                   if not unicodedata.category(ch).startswith(("C", "Z"))).strip()


def is_https(value: object) -> bool:
    if not isinstance(value, str):
        return False
    parsed = urlparse(value)
    if parsed.scheme != "https" or not parsed.netloc or parsed.username or parsed.password or parsed.fragment:
        return False
    path_parts = {part.casefold() for part in parsed.path.split("/") if part}
    if DISALLOWED_URL_PATH_PARTS & path_parts:
        return False
    for key, _ in parse_qsl(parsed.query, keep_blank_values=True):
        normalized = key.casefold()
        if normalized in DISALLOWED_URL_QUERY_KEYS or normalized.startswith(("utm_", "ref_", "session_")):
            return False
    return True


def is_google_map(provider: object, url: object) -> bool:
    provider_text = str(provider or "").casefold()
    host = urlparse(str(url or "")).hostname or ""
    normalized_host = host.casefold()
    return "google" in provider_text or normalized_host.endswith(("google.com", ".goo.gl")) or ".google." in normalized_host


def is_amap(provider: object, url: object) -> bool:
    provider_text = str(provider or "").casefold()
    host = urlparse(str(url or "")).hostname or ""
    return "amap" in provider_text or "高德" in str(provider or "") or host.casefold().endswith("amap.com")


def is_amap_directions_url(url: object) -> bool:
    """Validate the public Amap URI route format, not a destination/POI page.

    Amap's public URI documentation requires `https://uri.amap.com/navigation`
    plus `from`, `to`, and a transport `mode`.  Requiring those fields prevents
    a visually plausible `ditu.amap.com/place/...` link from being presented as
    a route that has actually been planned.
    """
    if not isinstance(url, str):
        return False
    parsed = urlparse(url)
    if (parsed.hostname or "").casefold() != "uri.amap.com" or parsed.path.rstrip("/") != "/navigation":
        return False
    query = dict(parse_qsl(parsed.query, keep_blank_values=True))
    return bool(query.get("from") and query.get("to") and query.get("mode"))


def is_directions_url(provider: object, url: object) -> bool:
    """Return whether the provider URL is suitable for a live directions button.

    Provider-specific URI syntaxes differ.  Mainland-China Amap links are
    checked strictly because its documented public URI format is known; other
    verified regional providers are checked by the research workflow and by the
    explicit `map_link_kind` contract instead of guessing undocumented URL
    syntax.
    """
    if not is_https(url):
        return False
    if is_amap(provider, url):
        return is_amap_directions_url(url)
    parsed = urlparse(str(url))
    host = (parsed.hostname or "").casefold()
    path = parsed.path.casefold()
    query = dict(parse_qsl(parsed.query, keep_blank_values=True))
    if is_google_map(provider, url):
        return bool(("/maps/dir" in path and (query.get("origin") and query.get("destination"))) or (query.get("api") == "1" and query.get("origin") and query.get("destination")))
    if host == "maps.apple.com":
        return bool(query.get("saddr") and query.get("daddr"))
    if host.endswith("openstreetmap.org"):
        return bool(query.get("route"))
    place_parts = {part.casefold() for part in parsed.path.split("/") if part}
    return not bool(place_parts & {"place", "poi", "detail", "details", "location", "search"})


def is_ambiguous_route_mode(value: object) -> bool:
    """Detect a choice-list masquerading as one researched primary route."""
    text = str(value or "").casefold()
    return bool(re.search(r"\b(?:or|either|choose|tbd)\b|(?:或|择一|待核验|待确认|/|／)", text))


def map_link_allowed(provider: object, url: object, regional_context: dict) -> bool:
    market = str(regional_context.get("destination_service_market") or "").casefold()
    google_access = regional_context.get("google_services_access")
    return not ((market == "mainland_china" or google_access == "unavailable") and is_google_map(provider, url))


# --------------------------------------------------------------------------------------------
# Where the rule is written
# --------------------------------------------------------------------------------------------
# More places this file can refuse a plan than any other gate, and two mentions of `references/`,
# both in comments that no failing run prints. This is the gate an author meets FIRST -- validate_plan runs before a
# single line of HTML is produced -- so it is also the gate with the most leverage over whether a
# run recovers or stalls.
#
# 144 of those sites are cited below and 63 deliberately are not, which is the interesting half.
# (That split read 143/64 when this block was first written. The census is now taken by AST in
# tests/test_packaging.py rather than by eye, and it disagreed by one -- so the numbers here are
# the measured ones and SITES_WITHOUT_A_REFERENCE below is what the test actually holds. A count
# maintained by hand in a comment is exactly the kind of claim that drifts without anybody
# noticing, which is the failure this whole block is about.)
# The uncited ones are shape rules that already carry their own answer: "budget.calculation_basis
# must be per_person.", "hotel.check_out must be after hotel.check_in.", "trip.end_date cannot be
# before trip.start_date." A reader who cannot act on those is not going to be helped by a
# reference; the field is named, the allowed value is named, and no section of any reference file
# states them -- they are the shape of templates/final-trip-plan.json. Appending a pointer to the
# nearest plausible heading would spend a 41 KB read to teach a wrong location, so those sites
# stay as they are. Citing everything would have been the easier change and the worse one.
#
# What IS cited is every rule where naming the field is not enough to fix it: which map URL is
# acceptable and why, which provider a market allows, what a booking card owes a traveller before
# it counts as a comparison, what a dining card has to have been checked for. Those are the rules
# whose reasoning lives in a reference and whose messages are otherwise a dead end for a run that
# never opened it.
#
# Derived from the enforcing code, not from SKILL.md -- SKILL.md describes this file's map rules
# as "invisible to every structural gate" a dozen lines from its own description of the gate that
# enforces them. Anchors are `<a id="...">` markers added to the reference files in this same
# change; tests/test_packaging.py fails if any anchor emitted here does not resolve.
RULE_REFERENCES: dict[str, str] = {
    # Every map URL rule: directions rather than a place page, HTTPS, a declared scope, and a
    # segment list a whole-day button cannot stand in for.
    # What the traveller needs in the first hour on the ground -- pay, connect, call for help,
    # and what happens if they need a doctor. Researched and dated like any other fact.
    "arrival.essentials": "booking-html-output.md#arrival-essentials",
    "map.link_contract": "booking-html-output.md#map-endpoints",
    # The day's visible travel burden -- one researched primary mode with alternatives in the
    # fallback, and a researched fare for a transit day.
    "route.day_burden": "booking-html-output.md#day-route-burden",
    # Which provider a market allows. Not the same rule as "record the market", which is why the
    # two have different homes: this one is the decision, the other is the record of it.
    "market.provider_routing": "regional-service-routing.md#routing-policy",
    "market.context_contract": "regional-service-routing.md#final-plan-contract",
    # Local booking constraints and the available/limited/unknown vocabulary they are recorded in.
    "booking.access_checks": "booking-html-output.md#ticket-constraints",
    # What each booking card owes: both legs named, dated search buttons, fare basis and status,
    # transfer notes. The section enumerates these per category, which is why one anchor serves
    # flights, rail, hotels, tickets and cars.
    "booking.option_contract": "booking-html-output.md#booking-links",
    # Two comparable candidates or a researched reason there is only one, distinct ids, distinct
    # review URLs. A separate section from the card contract because it is a rule about the SET.
    "booking.comparison": "booking-html-output.md#platform-selection-and-comparison",
    # The dining card's researched content -- venue, price, queue note, source, checked hours.
    "dining.card_contract": "booking-html-output.md#destination-coverage-and-food",
    # ui_labels: the renderer's own interface text on a page in a third language. Cited to the
    # closed-enum section because that is where the leak this prevents is described, and because
    # three delivered Chinese pages printed bare English enum values while both gates said VALID.
    "html.localization": "booking-html-output.md#closed-enums",
    # How the intake happened, and why a chat_fallback record may not also name a file only the
    # form server writes.
    "intake.provenance": "initial-intake.md#conversation-design",
    # One entry answer per jurisdiction the trip enters, each with its own evidence and printed as
    # its own row -- the multi-country rule, where a single answer was wrong for two of three.
    "entry.per_jurisdiction": "booking-html-output.md#per-jurisdiction",
}


def cite(rule_id: str, message: str) -> str:
    """Append the reference that states the rule this finding broke.

    APPENDS, never prepends. The suites for this file match needles as substrings of the whole
    output and many of those needles are a message's opening words; a prefix would move every one
    of them and buy a reader nothing a suffix does not.

    Raises on an unknown rule_id. Returning the message uncited would let this file keep passing
    its own tests while shipping the very dead end the registry exists to close -- and that is the
    exact failure mode, a gate green on wrong output, that most of the comments in this file are
    about.
    """
    if rule_id not in RULE_REFERENCES:
        raise KeyError(
            f"cite() called with unknown rule_id {rule_id!r}. Add it to RULE_REFERENCES with the "
            f"reference section that states the rule, or drop the cite() call. A shape rule that "
            f"names its own field and allowed values is better off uncited -- see the block above.")
    return f"{message} [see references/{RULE_REFERENCES[rule_id]}]"


# The other half of the registry: where an UNCITED finding is allowed to live, and how many.
#
# The block above argues that 63 shape rules are better off uncited, and that argument is sound --
# but until now it lived only in a comment, and a comment refuses nothing. check_plan_consistency
# and check_shortlist_consistency do not have this hole: their citations go on a decorator, so a
# check that names no reference must appear in CHECKS_WITHOUT_A_REFERENCE and tests/
# test_packaging.py refuses the third state where somebody simply forgot. Here the citation goes
# on the call, so a new `errors.append("...")` added to validate_plan() next release ships uncited
# and every test stays green -- the drift the whole change was made to end, one site at a time.
#
# Keyed by ENCLOSING FUNCTION rather than line number, because line numbers move on every edit and
# a registry that must be renumbered to stay true is a registry that will be renumbered wrongly.
# The COUNT is held too, and that is the part that does the work: validate_plan() legitimately
# carries uncited shape rules AND cited map/booking rules, so exempting the function wholesale
# would let a new uncited map rule hide inside the exemption. Holding the count means a new
# uncited site there fails this test and forces the same decision the decorator forces -- cite it,
# or raise the number and say why in this dict.
#
# Raising a number here is cheap and is meant to be. The point is not to make uncited sites hard
# to add; it is to make adding one a thing somebody DID rather than a thing nobody noticed.
SITES_WITHOUT_A_REFERENCE: dict[str, int] = {
    # The plan-shape contract: required keys, closed value sets, and orderings. Every one of these
    # names its own field and its own allowed values ("plan_status must be idea, researched, held,
    # or booked."), and no section of any reference states them -- they are the shape of
    # templates/final-trip-plan.json, which is the thing to open. Citing the nearest plausible
    # heading would spend a 41 KB read to teach a wrong location.
    "validate_plan": 61,
    # "must be an ISO date (YYYY-MM-DD)." twice, for a start and an end. The message is the whole
    # rule; there is nothing to look up.
    "parse_iso_date": 2,
}


def validate_alternative_map_links(value: object, label: str, regional_context: dict, errors: list[str]) -> None:
    if value is None:
        return
    if not isinstance(value, list):
        errors.append(cite("map.link_contract", f"{label}.alternative_map_links must be a list when present."))
        return
    for number, item in enumerate(value, 1):
        if not isinstance(item, dict) or not all(item.get(key) for key in ("provider", "url", "checked_at", "map_link_kind")):
            errors.append(cite("map.link_contract", f"{label}.alternative_map_links[{number}] needs provider, URL, check time, and map_link_kind."))
            continue
        if item["map_link_kind"] != "directions":
            errors.append(cite("map.link_contract", f"{label}.alternative_map_links[{number}].map_link_kind must be directions."))
        if not is_https(item["url"]):
            errors.append(cite("map.link_contract", f"{label}.alternative_map_links[{number}].url must be HTTPS."))
        elif not is_directions_url(item["provider"], item["url"]):
            errors.append(cite("map.link_contract", f"{label}.alternative_map_links[{number}] must be an actual directions URL, not a place page."))
        if not map_link_allowed(item["provider"], item["url"], regional_context):
            errors.append(cite("market.provider_routing", f"{label}.alternative_map_links[{number}] uses Google Maps despite the regional-access rule."))


def validate_booking_access_checks(value: object, errors: list[str]) -> set[str]:
    if not isinstance(value, list) or not value:
        errors.append(cite("booking.access_checks", "regional_service_context.booking_access_checks must be a non-empty list."))
        return set()
    sensitive_values = find_sensitive_values(value, "regional_service_context.booking_access_checks")
    if sensitive_values:
        errors.append(cite("booking.access_checks", "booking_access_checks appears to contain prohibited sensitive values at: " + ", ".join(sensitive_values) + "."))
    categories: set[str] = set()
    for number, item in enumerate(value, 1):
        if not isinstance(item, dict) or not all(
            item.get(key) for key in ("category", "access_status", "provider_or_channel", "requirements_note", "source_url", "checked_at")
        ):
            errors.append(cite("booking.access_checks", f"booking_access_checks[{number}] needs category, access_status, provider_or_channel, requirements_note, source_url, and checked_at."))
            continue
        category = item["category"]
        if category not in BOOKING_ACCESS_CATEGORIES:
            errors.append(cite("booking.access_checks", f"booking_access_checks[{number}].category is invalid."))
        else:
            if category in categories:
                errors.append(cite("booking.access_checks", f"booking_access_checks has duplicate category: {category}."))
            categories.add(category)
        if item["access_status"] not in BOOKING_ACCESS_STATUSES:
            errors.append(cite("booking.access_checks", f"booking_access_checks[{number}].access_status must be available, limited, or unknown."))
        if not is_https(item["source_url"]):
            errors.append(cite("booking.access_checks", f"booking_access_checks[{number}].source_url must be a safe HTTPS browse URL."))
        if not is_iso_datestamp(item["checked_at"]):
            errors.append(cite("booking.access_checks", f"booking_access_checks[{number}].checked_at must be an ISO date or date-time."))
    return categories


def parse_iso_date(value: object, label: str, errors: list[str]) -> date | None:
    if not isinstance(value, str):
        errors.append(f"{label} must be an ISO date (YYYY-MM-DD).")
        return None
    try:
        return date.fromisoformat(value)
    except ValueError:
        errors.append(f"{label} must be an ISO date (YYYY-MM-DD).")
        return None


def is_iso_datestamp(value: object) -> bool:
    """Accept an ISO calendar date or an ISO date-time for source freshness fields."""
    if not isinstance(value, str) or not value.strip():
        return False
    try:
        if len(value) == 10:
            date.fromisoformat(value)
        else:
            datetime.fromisoformat(value.replace("Z", "+00:00"))
        return True
    except ValueError:
        return False


def is_one_of(value: object, allowed: set[str]) -> bool:
    """`value not in {"available", ...}` raises TypeError when the author wrote a list or a dict,
    so a plausible typo killed validate_plan with a bare traceback instead of printing the
    one-line reason the rule exists to print. Non-strings are simply not the allowed value."""
    return isinstance(value, str) and value in allowed


def has_search_fields(value: object, required: set[str]) -> bool:
    """Same crash, one line over: `set(value)` on author-supplied elements raised
    `TypeError: unhashable type: 'dict'` for `[{"origin": "Leiden"}]` -- a believable slip, since
    the itinerary fields beside it really are objects. Non-string elements cannot name a field."""
    if not isinstance(value, list):
        return False
    return required.issubset({field for field in value if isinstance(field, str)})


def dedupe_key(value: object) -> object:
    """Duplicate detection puts author-supplied ids and URLs into a set. Anything unhashable
    reaches its repr instead of crashing, which still distinguishes two different values."""
    try:
        hash(value)
    except TypeError:
        return repr(value)
    return value


def is_nonnegative_money_range(low: object, high: object) -> bool:
    """Keep displayed costs comparable and prevent inverted or text-only ranges."""
    numeric = (int, float)
    if any(not isinstance(value, numeric) or isinstance(value, bool) for value in (low, high)):
        return False
    return low >= 0 and high >= low


def is_nonnegative_number(value: object) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and value >= 0


def format_amount(value: object) -> str:
    """Group thousands so a five-figure fare is readable at a glance."""
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return f"{value:,.0f}" if float(value).is_integer() else f"{value:,.2f}"
    return as_text(value)


def money(low: object, high: object, currency: object) -> str:
    code = as_text(currency, "").strip().upper()
    symbol = CURRENCY_SYMBOLS.get(code)
    priced = lambda text: f"{symbol}{text}" if symbol else f"{code} {text}".strip()
    if low is None and high is None:
        return "Price not currently verified"
    if low == high or high is None:
        return priced(format_amount(low))
    if low is None:
        return f"Up to {priced(format_amount(high))}"
    return f"{priced(format_amount(low))}–{format_amount(high)}"


def minutes(value: object) -> str:
    if not isinstance(value, (int, float)):
        return "Time not currently verified"
    hours, mins = divmod(round(value), 60)
    return f"{hours}h {mins}m" if hours else f"{mins} min"


def read_json(path: str) -> dict:
    raw = sys.stdin.read() if path == "-" else Path(path).read_text(encoding="utf-8")
    data = json.loads(raw)
    if not isinstance(data, dict):
        raise ValueError("The plan must be a JSON object.")
    return data


def day_service_market(day: dict, stays_by_id: dict[str, dict], trip_market: object) -> str:
    """Which service market's rules apply to THIS day.

    The mainland-China map rule was page-wide, which is correct for a trip that stays in one market
    and wrong for every trip that does not. Measured on a real plan: turn the last two days of a
    Shenzhen trip into a Hong Kong leg with Google Maps links -- the correct provider there, since
    Amap is not the tool for Hong Kong transit -- and the gate produced eighteen findings telling
    the author that those Hong Kong days must use Amap. The traveller's only ways out were wrong
    links for half the trip or no delivered page at all.

    A day takes the jurisdiction of the accommodation it sleeps at, and falls back to the trip's
    own market. The fallback is what keeps every single-market plan byte-identical.
    """
    stay = stays_by_id.get(str(day.get("accommodation_option_id") or ""))
    declared = str((stay or {}).get("jurisdiction") or "").strip()
    return declared or str(trip_market or "").strip()


def _leg_groups(items: list[dict]) -> dict[str, list[dict]]:
    """Booking options grouped by the journey they are alternatives for.

    An item with no `leg_group_id` falls into the unnamed group, which is what every single-leg
    plan is and why the field is not required until the items themselves show more than one
    journey.
    """
    groups: dict[str, list[dict]] = {}
    for item in items:
        groups.setdefault(str(item.get("leg_group_id") or "").strip(), []).append(item)
    return groups


def _looks_like_several_legs(items: list[dict]) -> bool:
    """Do these options describe more than one journey, by their own dates and endpoints?

    Used only to decide whether `leg_group_id` is demanded -- never to group, because two genuine
    alternatives for one journey may leave from different stations, and grouping on the endpoints
    would then split a real comparison into two unexplained singles.
    """
    dates = {str(item.get("outbound_date") or "").strip() for item in items} - {""}
    pairs = {(str(item.get("origin_airport") or item.get("origin_station") or "").strip(),
              str(item.get("destination_airport") or item.get("destination_station") or "").strip())
             for item in items} - {("", "")}
    return len(dates) > 1 or len(pairs) > 1


def booking_title(kind: str, item: dict) -> str:
    if kind == "flight":
        return f"{printed(item.get('provider'), 'Not supplied')}: {printed(item.get('origin_airport'), 'Not supplied')} → {printed(item.get('destination_airport'), 'Not supplied')}"
    if kind == "ground":
        return f"{printed(item.get('provider'), 'Not supplied')}: {printed(item.get('origin_station'), 'Not supplied')} → {printed(item.get('destination_station'), 'Not supplied')}"
    if kind == "hotel":
        return f"{printed(item.get('property_name'), 'Not supplied')} · {printed(item.get('stay_location'), 'Not supplied')}"
    if kind == "ticket":
        return printed(item.get("attraction_name"), "Not supplied")
    return f"{printed(item.get('provider'), 'Not supplied')} · {printed(item.get('vehicle_class'), 'Not supplied')}"


def booking_details(kind: str, item: dict) -> str:
    if kind == "ground":
        # Without this branch option_card printed its no-data fallback, "Conditions require
        # recheck", in the slot directly under the fare -- on every ground card, however fully it
        # was researched, and three rows above the line that actually states the conditions. A
        # warning nobody earned, sitting under a price the traveller is about to act on.
        return " · ".join(
            part
            for part in (
                " → ".join(part for part in (told(item.get("outbound_date")), told(item.get("return_date"))) if part),
                told(item.get("travel_class")),
                told(item.get("seat_reservation")),
            )
            if part
        )
    if kind == "flight":
        return " · ".join(
            part
            for part in (
                told(item.get("outbound_date")),
                told(item.get("return_date")),
                told(item.get("cabin")),
                told(item.get("baggage_assumption")),
                told(item.get("connection_summary")),
            )
            if part
        )
    if kind == "hotel":
        return " · ".join(
            part
            for part in (
                " → ".join(part for part in (told(item.get("check_in")), told(item.get("check_out"))) if part),
                f"{as_text(item.get('guest_count'), '')} guest(s) · {as_text(item.get('room_count'), '')} room(s)" if item.get("guest_count") and item.get("room_count") else "",
                told(item.get("room_basis")),
                told(item.get("taxes_and_fees_status")),
                told(item.get("cancellation_terms")),
                told(item.get("accessibility_or_location_note")),
            )
            if part
        )
    if kind == "ticket":
        # `ticket_status` is rendered as a labelled row in option_detail_list; repeating
        # `timed_entry_or_reservation` here as well printed the same sentence twice.
        return told(item.get("timed_entry_or_reservation"))
    return " · ".join(
        part
        for part in (
            told(item.get("pickup_location")),
            told(item.get("dropoff_location")),
            told(item.get("transmission")),
            told(item.get("fuel_policy")),
            told(item.get("mileage_policy")),
        )
        if part
    )


def flight_leg_summary(leg: object, kind: str = "flight") -> str:
    if not isinstance(leg, dict):
        return ""
    # Rail counts changes, not stops, and the distinction is not cosmetic: the localizer rewrites
    # "0 stop(s)" to 直飞 page-wide with no notion of booking type, so a through train on a
    # Chinese page was labelled "direct flight".
    stop_noun = "change(s)" if kind == "ground" else "stop(s)"
    return " · ".join(
        part
        for part in (
            # An unresearched identifier prints its REASON, not a gap. A blank here reads as an
            # oversight; the sentence reads as what it is -- a fact nobody could check yet, with
            # the place to check it named. The gate refuses the third possibility, a number
            # sitting under a label that says nobody looked.
            (told(leg.get("service_identifier"))
             if str(leg.get("service_identifier_status") or "researched") == "researched"
             else told(leg.get("service_identifier_unresearched_reason"))),
            " → ".join(part for part in (told(leg.get("departure_local")), told(leg.get("arrival_local"))) if part),
            minutes(leg.get("duration_minutes")),
            f"{as_text(leg.get('stops'))} {stop_noun}" if leg.get("stops") is not None else "",
            told(leg.get("connection_or_terminal_note")),
        )
        if part
    )


# English for each sale_opens_at.status, translated through its own span the way the dining hours
# status is, so the bare words cannot catch an author's sentence elsewhere on the page.
TICKET_SALE_ENGLISH = {
    "always_available": "On sale now",
    "scheduled_release": "Goes on sale",
    "at_the_door": "Sold at the door",
    "sold_out_or_unavailable": "Sold out or unavailable",
}
TICKET_SALE_UNKNOWN = "Sale window not confirmed"
BOOKING_STATE_WORDS = {"booked": "Booked", "chosen": "Chosen — not booked yet"}
SELF_TRANSFER_SENTENCE = ("separate tickets. A missed connection is not protected; collect your "
                          "bags and check in again for the next flight.")
TICKET_SALE_LABEL_KEYS = {
    "always_available": "ticket_sale_always_available",
    "scheduled_release": "ticket_sale_scheduled_release",
    "at_the_door": "ticket_sale_at_the_door",
    "sold_out_or_unavailable": "ticket_sale_sold_out",
}


def sale_moment(value: object) -> str:
    """`2026-10-10T09:30:00+01:00` as `2026-10-10 09:30 (UTC+01:00)`; anything else verbatim.

    The offset is kept because it is the release's own clock: a traveller in another zone reading
    "09:30" alone would be an hour out, which is the difference between a seat and a sold-out show.
    """
    text = as_text(value, "")
    match = re.fullmatch(
        r"(\d{4}-\d{2}-\d{2})[T ](\d{2}:\d{2})(?::\d{2}(?:\.\d+)?)?\s*(Z|[+-]\d{2}:?\d{2})?", text.strip())
    if not match:
        return text
    day, clock, offset = match.groups()
    zone = "" if not offset else " (UTC)" if offset == "Z" else f" (UTC{offset})"
    return f"{day} {clock}{zone}"


def ticket_sale_row(sale: object) -> str:
    """When the tickets can be bought, and what that rests on, on the ticket's own card.

    check_plan_consistency.py requires sale_opens_at on every ticket a day schedules, because a
    ticket released at a fixed hour can be gone by the time a traveller thinks to look -- and until
    2026-10-09 the field reached only the calendar file embedded in the page. A traveller who never
    imported the calendar was never told. The basis sentence is printed too: it is the field's whole
    defence against an `always_available` typed without opening anything, and a reader can only
    check a claim whose source they can see.
    """
    if not isinstance(sale, dict):
        return ""
    status = str(sale.get("status") or "").strip()
    basis = as_text(sale.get("basis"), "")
    if not status and not basis:
        return ""
    words = TICKET_SALE_ENGLISH.get(status, TICKET_SALE_UNKNOWN)
    moment = sale_moment(sale.get("opens_at")) if status == "scheduled_release" else ""
    treatment = "warning" if status not in ("always_available", "at_the_door") else "meta"
    return (
        f'<li class="ticket-sale {treatment}" data-sale-status="{attr(status)}">'
        f'<strong>Ticket sale: </strong><span class="ticket-sale-status">{words}</span>'
        f'{" " + esc(moment) if moment else ""}{" — " + esc(basis) if basis else ""}</li>'
    )


def option_detail_list(kind: str, item: dict) -> str:
    rows: list[str] = []
    if kind == "ground":
        # Same rows as a flight, because the traveller's questions are the same ones: which
        # service, when, how long, how many changes, what the fare lets them do, and how they get
        # from the station into town. `station_transfer_note` is the ground analogue of the
        # airport-transfer note that stops a cheap-looking flight hiding an impractical arrival.
        rows.extend(
            (
                f'<li><strong>Outbound: </strong>{markup(flight_leg_summary(item.get("outbound_itinerary"), "ground") or "Not supplied")}</li>',
                f'<li><strong>Return: </strong>{markup(flight_leg_summary(item.get("return_itinerary"), "ground") or "Not supplied")}</li>',
                f'<li><strong>Fare conditions: </strong>{esc(item.get("material_conditions"))}</li>',
                f'<li><strong>Station and access: </strong>{esc(item.get("station_transfer_note"))}</li>',
                # Required by validate_plan and, until this line, printed nowhere -- so the card
                # showed a fare with no hint that it was an estimate, priced weeks ago, on limited
                # inventory, while the hotel and flight cards beside it said exactly that. Same
                # labels as the flight row, so they are already localized.
                f'<li><strong>Availability: </strong>{vocab(item.get("availability_status"))} · <strong>Price status: </strong>{vocab(item.get("price_status"))} · <strong>Price checked: </strong>{stamp(item.get("price_checked_at"))}</li>',
            )
        )
    if kind == "flight":
        # A leg kiwi_flights.py marked self_transfer connects on separate tickets: nothing rebooks a
        # missed connection, bags come off and check in again. The card is where the traveller
        # decides, so the warning sits under the leg it belongs to (references/booking-html-output.md#self-transfer).
        warnings = [
            f'<li class="warning self-transfer" data-self-transfer-leg="{leg}">'
            f'<strong>Self-transfer: </strong>'
            f'<span class="self-transfer-sentence">{SELF_TRANSFER_SENTENCE}</span></li>'
            for leg, key in (("outbound", "outbound_itinerary"), ("return", "return_itinerary"))
            if isinstance(item.get(key), dict) and item[key].get("self_transfer") is True
        ]
        rows.extend(
            (
                f'<li><strong>Outbound: </strong>{markup(flight_leg_summary(item.get("outbound_itinerary")) or "Not supplied")}</li>',
                f'<li><strong>Return: </strong>{markup(flight_leg_summary(item.get("return_itinerary")) or "Not supplied")}</li>',
                *warnings,
                f'<li><strong>Fare conditions: </strong>{esc(item.get("material_conditions"))}</li>',
                f'<li><strong>Availability: </strong>{vocab(item.get("availability_status"))} · <strong>Price status: </strong>{vocab(item.get("price_status"))} · <strong>Price checked: </strong>{stamp(item.get("price_checked_at"))}</li>',
                f'<li>{esc(item.get("airport_transfer_note"))}</li>',
            )
        )
    elif kind == "hotel":
        rows.extend(
            (
                # The guest score sits above location and price because it is the field that
                # decides whether the other two are worth having, and because it was collected
                # and rendered nowhere at all until a traveller asked why hotels were not judged
                # the way restaurants are.
                hotel_rating_line(item),
                f'<li><strong>Location and access: </strong>{esc(item.get("neighborhood"))} · {esc(item.get("address_or_location_reference"))} · {esc(item.get("arrival_access_note"))} · {esc(item.get("key_area_access_note"))}</li>',
                f'<li><strong>Why it fits: </strong>{esc(item.get("selection_rationale"))}</li>',
                f'<li><strong>Availability: </strong>{vocab(item.get("availability_status"))} · <strong>Price status: </strong>{vocab(item.get("price_status"))} · <strong>Price checked: </strong>{stamp(item.get("price_checked_at"))}</li>'
                # Collected and not shown is the same defect as never collected, and this is
                # the sentence the traveller most needs: on a trip where no hotel's dates
                # could be confirmed, the page has to say so where the booking decision is
                # made rather than leaving it in the JSON.
                + (f'<p class="warning">{esc(item.get("availability_unknown_reason"))}</p>'
                   if str(item.get("availability_status") or "").lower() == "unknown"
                   and item.get("availability_unknown_reason") else ""),
            )
        )
    elif kind == "ticket":
        rows.extend(
            (
                f'<li><strong>Ticket status: </strong>{vocab(item.get("ticket_status"))}</li>',
                f'<li><strong>Availability: </strong>{vocab(item.get("availability_status"))} · <strong>Price status: </strong>{vocab(item.get("price_status"))} · <strong>Price checked: </strong>{stamp(item.get("price_checked_at"))}</li>',
                ticket_sale_row(item.get("sale_opens_at")),
            )
        )
    elif kind == "car":
        rows.extend(
            (
                f'<li>{esc(item.get("pickup_location"))} → {esc(item.get("dropoff_location"))} · {esc(item.get("pickup_time"))} → {esc(item.get("dropoff_time"))}</li>',
                f'<li>{esc(item.get("transmission"))} · {esc(item.get("capacity_note"))} · {esc(item.get("insurance_excess"))}</li>',
                # Required by validate_plan and printed nowhere until 2026-09-24: ferries, other
                # countries, driver age -- the terms that decide whether the car can go where the
                # itinerary sends it.
                (f'<li class="rental-restriction"><strong>Restrictions: </strong>'
                 f'{esc(item.get("cross_border_or_restriction_note"))}</li>'
                 if item.get("cross_border_or_restriction_note") else ""),
                f'<li><strong>Availability: </strong>{vocab(item.get("availability_status"))} · <strong>Price status: </strong>{vocab(item.get("price_status"))} · <strong>Price checked: </strong>{stamp(item.get("price_checked_at"))}</li>',
            )
        )
    return f'<ul class="option-details">{"".join(rows)}</ul>' if rows else ""


def budget_breakdown_cards(value: object, currency: object) -> str:
    if not isinstance(value, list):
        return ""
    cards = []
    for item in value:
        if not isinstance(item, dict):
            continue
        cards.append(
            f'<article class="fact budget-item" data-budget-category="{attr(item.get("category"))}">'
            f'<strong>{vocab(item.get("category"))}: {markup(money(item.get("per_person_low"), item.get("per_person_high"), item.get("currency") or currency))}</strong>'
            f'<span>{esc(item.get("description"))}</span>'
            f'<p class="meta">{vocab(item.get("price_status"))} · {stamp(item.get("checked_at"))} · {esc(item.get("note"))}</p></article>'
        )
    return f'<section id="budget-breakdown" class="panel"><h2>Budget breakdown</h2><div class="grid">{"".join(cards)}</div></section>' if cards else ""


def booking_link(kind: str, provider: object, checked_at: object, url: object, label: str, purpose: str | None = None, prefilled_fields: list[object] | None = None) -> str:
    purpose_attr = f' data-booking-purpose="{attr(purpose)}"' if purpose else ""
    prefilled_attr = f' data-prefilled-fields="{attr(",".join(str(field) for field in prefilled_fields))}"' if prefilled_fields else ""
    return f'<a class="booking-link" data-booking-type="{attr(kind)}" data-provider="{attr(provider)}" data-verified-at="{attr(checked_at)}"{purpose_attr}{prefilled_attr} href="{attr(url)}" target="_blank" rel="noopener noreferrer">{markup(label)}</a>'


def hotel_comparison_links(item: dict) -> str:
    links = []
    for search in item.get("comparison_searches", []):
        if not isinstance(search, dict):
            continue
        platform = as_text(search.get("platform"), "Comparison platform")
        label = "Compare on Booking.com — dates and guests included" if platform.casefold() in {"booking", "booking.com"} else f"Compare on {printed(search.get('platform'), 'Comparison platform')} — dates and guests included"
        links.append(booking_link("hotel", platform, search.get("checked_at"), search.get("search_url"), label, "comparison-search", search.get("prefilled_fields") if isinstance(search.get("prefilled_fields"), list) else None))
    return "".join(links)


def booking_badge(record: dict | None, option_id: object) -> str:
    """The decision on the card the traveller made it about (scripts/bookings.py)."""
    if not isinstance(record, dict) or record.get("state") not in BOOKING_STATE_WORDS:
        return ""
    state = record["state"]
    parts = [f'<span class="booking-state">{BOOKING_STATE_WORDS[state]}</span>']
    if state == "booked":
        parts.append(esc(record.get("booked_on")))
        parts.append(f'<span class="booking-via">via</span> {esc(record.get("booked_via"))}')
        if record.get("paid_total") is not None:
            total = record["paid_total"]
            parts.append(f'<span class="booking-paid">paid</span> {markup(money(total, total, record.get("paid_currency")))} '
                         f'<span class="booking-confirmed">(user-confirmed)</span>')
    return (f'<p class="booking-badge" data-booking-option="{attr(option_id)}" data-booking-state="{attr(state)}">'
            + " · ".join(parts) + "</p>")


def option_card(kind: str, item: dict, record: dict | None = None) -> str:
    provider = as_text(item.get("provider"), item.get("official_or_authorised_provider") or "Provider")
    checked_at = as_text(item.get("checked_at"))
    comparison_platform = as_text(item.get("comparison_platform"), "Direct provider")
    # The same three names as the page prints them: the author's fenced, the fallbacks translatable.
    provider_shown = printed(item.get("provider") or item.get("official_or_authorised_provider"), "Provider")
    comparison_shown = printed(item.get("comparison_platform"), "Direct provider")
    url = item.get("review_url")
    price = money(item.get("fare_low", item.get("nightly_cost_low", item.get("price_low"))), item.get("fare_high", item.get("nightly_cost_high", item.get("price_high"))), item.get("fare_currency", item.get("currency")))
    price_label = (
        "Price per person, round trip: " if kind == "flight" else
        "Price per room/night: " if kind == "hotel" else
        "Ticket price per person: " if kind == "ticket" else
        "Vehicle price per day: " if kind == "car" else
        "Price per person, round trip: " if kind == "ground" else ""
    )
    # How to read an average: a party total over adults, children and infants, written by
    # kiwi_flights.py beside the per-person figure it was divided into.
    price_note = (f'<p class="meta price-note">{esc(item.get("price_note"))}</p>'
                  if item.get("price_note") else "")
    stay_total = ""
    if kind == "hotel":
        stay_total = f'<p class="meta"><strong>Trip total for stay: </strong>{markup(money(item.get("trip_cost_low"), item.get("trip_cost_high"), item.get("currency")))}</p>'
    actions = [booking_link(kind, provider, checked_at, url, f"Review option in {provider_shown}", "review-option")]
    direct_url = item.get("direct_review_url")
    if direct_url and direct_url != url:
        direct_provider = as_text(item.get("direct_provider"), "Direct provider")
        actions.append(booking_link(kind, direct_provider, item.get("comparison_checked_at") or checked_at, direct_url, f"Review direct provider in {printed(item.get('direct_provider'), 'Direct provider')}", "direct-provider"))
    if kind == "ground":
        # Rail, coach and ferry get the flight treatment because the traveller needs the same
        # things: which service, when it leaves, how long, how many changes, and what the fare
        # conditions are. Before this they got nothing -- a Japan or European rail trip shipped as
        # "booking-ready" with no way to reach, price-check or availability-check the single
        # largest and most time-sensitive thing on it, while the hotels had three compared
        # candidates each.
        actions.insert(0, booking_link("ground", item.get("round_trip_search_provider") or comparison_platform or provider, item.get("round_trip_search_checked_at") or checked_at, item.get("round_trip_search_url"), f"Search round trip in {printed(item.get('round_trip_search_provider'), comparison_shown)} — {as_text(item.get('outbound_date'))} to {as_text(item.get('return_date'))}", "round-trip-search", item.get("round_trip_prefilled_fields") if isinstance(item.get("round_trip_prefilled_fields"), list) else None))
    if kind == "flight":
        actions.insert(0, booking_link("flight", item.get("round_trip_search_provider") or comparison_platform or provider, item.get("round_trip_search_checked_at") or checked_at, item.get("round_trip_search_url"), f"Search round trip in {printed(item.get('round_trip_search_provider'), comparison_shown)} — {as_text(item.get('outbound_date'))} to {as_text(item.get('return_date'))}", "round-trip-search", item.get("round_trip_prefilled_fields") if isinstance(item.get("round_trip_prefilled_fields"), list) else None))
    if kind == "hotel":
        actions.extend(hotel_comparison_links(item))
    if kind == "car":
        actions[0] = booking_link("car", provider, checked_at, url, f"Review option in {provider_shown}", "rental-search", item.get("rental_search_prefilled_fields") if isinstance(item.get("rental_search_prefilled_fields"), list) else None)
    # A single option is allowed only with a researched reason; showing the reason is what
    # keeps the missing comparison legible instead of looking like an oversight.
    single_reason = (
        f'<p class="meta single-option-reason"><strong>Only one option shown: </strong>{esc(item.get("single_option_reason"))}</p>'
        if item.get("single_option_reason")
        else ""
    )
    # data-option-kind carries the machine enum so the delivery gate can attribute each button to
    # the card it sits in. The pill beside it says the same thing in the traveller's language and
    # is therefore unreadable to a gate on a translated page.
    #
    # source_type rides as an attribute and is not printed. It is free text that authors fill with
    # identifiers -- the skeleton's own default is `airline_and_comparison_platform` -- so every
    # card on every page, Chinese ones included, ended in "Source: operator_and_comparison_platform"
    # (audit 2026-10-09). The visible line already says the same thing in words: who provides the
    # option and where it was compared.
    return f'''<article class="option" data-option-kind="{attr(kind)}" data-source-type="{attr(item.get("source_type"))}"><span class="pill">{attr(kind)}</span><h3>{markup(booking_title(kind, item))}</h3>{booking_badge(record, item.get("id"))}<p><strong>{price_label}</strong>{markup(price)}</p>{price_note}{stay_total}<p>{markup(booking_details(kind, item) or "Conditions require recheck")}</p>{option_detail_list(kind, item)}{single_reason}<p class="meta">Provider: {markup(provider_shown)} · Compared via: {markup(comparison_shown)} · Checked: {stamp(checked_at)}</p>{"".join(actions)}</article>'''


def booking_access_details(value: object) -> str:
    if not isinstance(value, list) or not value:
        return ""
    rows = []
    for item in value:
        if not isinstance(item, dict):
            continue
        rows.append(
            f'<li class="booking-access-item" data-booking-access-category="{attr(item.get("category"))}" '
            f'data-booking-access-status="{attr(item.get("access_status"))}" '
            f'data-accessed-at="{attr(item.get("checked_at"))}" data-source-url="{attr(item.get("source_url"))}">'
            f'<strong>{vocab(item.get("category"))} · {vocab(item.get("access_status"))}</strong> — '
            f'{esc(item.get("provider_or_channel"))}: {esc(item.get("requirements_note"))} '
            f'<a class="booking-access-source-link" href="{attr(item.get("source_url"))}" target="_blank" rel="noopener noreferrer">Source</a></li>'
        )
    return f'<details class="booking-access" open><summary>Booking access checks</summary><ul>{"".join(rows)}</ul></details>'


def route_diagram(stops: list[object]) -> str:
    """Render the visit-order schematic as a vertical, text-sized ordered list.

    The previous horizontal SVG needed a ~720px minimum width to keep stop names
    legible, so inside its scroll box a phone silently showed only the first two stops
    of the day — the diagram looked complete and was not.  An ordered list reflows
    instead of truncating, keeps names at real font size, and stays selectable and
    readable by assistive technology.
    """
    names = [as_text(stop) for stop in stops if stop not in (None, "")]
    if len(names) < 2:
        names = ["Start", "End"]
    items = "".join(
        f'<li class="route-stop"><span class="route-stop-index" aria-hidden="true">{index}</span>'
        f'<span class="route-stop-name">{esc(name)}</span></li>'
        for index, name in enumerate(names, 1)
    )
    return f'<ol class="route-rail">{items}</ol>'


def map_link(
    provider: object,
    checked_at: object,
    url: object,
    label: str,
    *,
    segment_number: int | None = None,
    alternative: bool = False,
    link_kind: str = "directions",
    map_scope: str | None = None,
) -> str:
    classes = "map-link map-link-alternative" if alternative else "map-link"
    if segment_number is not None and not alternative:
        classes += " segment-map-link"
    segment_attr = f' data-route-segment="{segment_number}"' if segment_number is not None else ""
    scope_attr = f' data-map-scope="{attr(map_scope)}"' if map_scope else ""
    role = "alternative" if alternative else "primary"
    return f'<a class="{classes}" data-map-provider="{attr(provider)}" data-map-role="{role}" data-map-kind="{attr(link_kind)}"{scope_attr}{segment_attr} data-verified-at="{attr(checked_at)}" href="{attr(url)}" target="_blank" rel="noopener noreferrer">{markup(label)}</a>'


def alternative_map_links(value: object) -> str:
    if not isinstance(value, list):
        return ""
    links = []
    for item in value:
        if not isinstance(item, dict):
            continue
        provider = as_text(item.get("provider"), "Map provider")
        links.append(map_link(provider, item.get("checked_at"), item.get("url"), f"Open alternative route in {printed(item.get('provider'), 'Map provider')}", alternative=True, link_kind=as_text(item.get("map_link_kind"), "directions")))
    return "".join(links)


def decorate_primary_map_links(page: str, plan: dict) -> str:
    """Replace the two legacy primary-map anchors with provider-labelled, attributed links."""
    regional = plan.get("regional_service_context") if isinstance(plan.get("regional_service_context"), dict) else {}
    page = page.replace(
        '<main id="trip-plan" data-trip-plan>',
        f'<main id="trip-plan" data-trip-plan data-service-market="{attr(regional.get("destination_service_market"))}" data-google-services-access="{attr(regional.get("google_services_access"))}" data-primary-map-provider="{attr(regional.get("primary_map_provider"))}" data-primary-map-exception="{attr(regional.get("primary_map_exception_reason") or "")}" data-transport-mode="{attr((plan.get("transport_preference") or {}).get("mode"))}">',
        1,
    )
    booking_access = booking_access_details(regional.get("booking_access_checks"))
    booking_intro = '<p class="meta">Current researched options only. Opening a link never creates a reservation.</p>'
    page = page.replace(booking_intro, booking_intro + booking_access, 1)
    for day in plan.get("days", []):
        if not isinstance(day, dict) or not isinstance(day.get("route"), dict):
            continue
        route = day["route"]
        route_scope = route.get("route_map_scope")
        base_label = "Open full-day route" if route_scope == "multi_stop" else "Open route overview — see segments below"
        old = f'<a class="map-link" data-map-scope="{attr(route_scope)}" data-verified-at="{attr(route.get("map_checked_at"))}" href="{attr(route.get("verified_map_url"))}" target="_blank" rel="noopener noreferrer">{base_label}</a>'
        provider = as_text(route.get("map_provider"), "Map provider")
        provider_shown = printed(route.get("map_provider"), "Map provider")
        provider_label = f"Open full-day route in {provider_shown}" if route_scope == "multi_stop" else f"Open route overview in {provider_shown} — see segments below"
        new = map_link(provider, route.get("map_checked_at"), route.get("verified_map_url"), provider_label, link_kind=as_text(route.get("map_link_kind"), "directions"), map_scope=as_text(route_scope)) + alternative_map_links(route.get("alternative_map_links"))
        page = page.replace(old, new, 1)
    overview = plan.get("transport_overview") if isinstance(plan.get("transport_overview"), dict) else {}
    overview_scope = overview.get("overall_map_scope")
    provider = as_text(overview.get("overall_map_provider"), "Map provider")
    overview_label, overview_provider_label = overview_link_labels(
        plan, printed(overview.get("overall_map_provider"), "Map provider"))
    old_overview = f'<a class="map-link" data-map-scope="{attr(overview_scope)}" data-verified-at="{attr(overview.get("overall_map_checked_at"))}" href="{attr(overview.get("overall_route_map_url"))}" target="_blank" rel="noopener noreferrer">{overview_label}</a>'
    new_overview = map_link(provider, overview.get("overall_map_checked_at"), overview.get("overall_route_map_url"), overview_provider_label, link_kind=as_text(overview.get("map_link_kind"), "directions"), map_scope=as_text(overview_scope)) + alternative_map_links(overview.get("overall_alternative_map_links"))
    return page.replace(old_overview, new_overview, 1)


def overview_link_labels(plan: dict, provider: str) -> tuple[str, str]:
    """The overview button's text: plain, and with its provider.

    It used to read "Open the airport transfer route" whenever the overview was not a multi-stop
    route -- on a rail trip, on a self-drive trip, on any trip with no airport at all.
    """
    overview = plan.get("transport_overview") if isinstance(plan.get("transport_overview"), dict) else {}
    trip = plan.get("trip") if isinstance(plan.get("trip"), dict) else {}
    if overview.get("overall_map_scope") == "multi_stop":
        return "Open overall route", f"Open overall route in {provider}"
    if str(trip.get("arrival_transport_mode") or "") == "flight":
        return ("Open the airport transfer route — daily segments are below",
                f"Open the airport transfer route in {provider} — daily segments are below")
    return ("Open the route overview — daily segments are below",
            f"Open the route overview in {provider} — daily segments are below")


def route_segment_links(route: dict, currency: object) -> str:
    rows = []
    for index, segment in enumerate(route.get("segments", []), 1):
        if not isinstance(segment, dict):
            continue
        details = " · ".join(
            part
            for part in (
                told(segment.get("mode")),
                told(segment.get("service_or_line")),
                minutes(segment.get("duration_minutes")),
                f"{as_text(segment.get('distance_km'))} km" if segment.get("distance_km") is not None else "",
                f"Walk {as_text(segment.get('walking_minutes'))} min" if segment.get("walking_minutes") is not None else "",
                f"{as_text(segment.get('transfer_count'))} transfer(s)" if segment.get("transfer_count") is not None else "",
                money(segment.get("cost_low"), segment.get("cost_high"), segment.get("currency", currency)),
                # validate_plan REQUIRES fare_basis on every segment and nothing printed it, so on
                # the measured plan 15 segments carried "KVB single ticket Preisstufe 1b EUR 4.00,
                # kvb.koeln, checked 2026-08-05" and the page showed a bare number the traveller
                # had no way to question. A price with no basis is the black box the whole source
                # discipline exists to prevent.
                told(segment.get("fare_basis")),
                told(segment.get("journey_instruction")),
                told(segment.get("arrival_instruction")),
                told(segment.get("fallback_note")),
                # The consistency gate lets a leg run far longer than the straight line when the
                # author says why in detour_reason; the traveller saw the detour and never the
                # reason (audit 2026-10-09).
                told(segment.get("detour_reason")),
            )
            if part
        )
        primary = map_link(segment.get("map_provider"), segment.get("map_checked_at"), segment.get("verified_map_url"), f"Open this segment in {printed(segment.get('map_provider'), 'Not supplied')}", segment_number=index, link_kind=as_text(segment.get("map_link_kind"), "directions"))
        rows.append(f'''<li class="route-segment" data-route-segment="{index}"><div><strong>{esc(segment.get("from"))} → {esc(segment.get("to"))}</strong><p class="meta">{markup(details)}</p></div>{primary}{alternative_map_links(segment.get("alternative_map_links"))}</li>''')
    return f'<ol class="segment-list">{"".join(rows)}</ol>'


def hotel_rating_line(item: dict) -> str:
    """The guest score, its count and where it was read, as a row in the option card."""
    status = str(item.get("guest_rating_status") or "").strip().casefold()
    if status == "none":
        reason = item.get("guest_rating_absence_reason")
        return (f'<li class="option-rating" data-rating-status="none"><strong>Guest rating: '
                f'</strong>no public rating{" · " + esc(reason) if reason else ""}</li>')
    value = item.get("guest_rating_value")
    if value is None:
        return ""
    scale = item.get("guest_rating_scale") or 10
    count = item.get("guest_rating_count")
    source = item.get("guest_rating_source")
    url = item.get("guest_rating_url")
    shown = f'{as_text(value)}/{as_text(scale)}'
    inner = (f'<a class="booking-link" data-booking-type="hotel" '
             # The score's source, not the booking platform. This link goes to the page the
             # SCORE was read from, so the provider-identity check must be told that platform --
             # with `comparison_platform` first, a rating could only ever be cited to the site
             # you book on, and that is precisely what pushed a delivered plan into citing both
             # hotels' Booking scores to the dated Booking price search: the one URL that both
             # satisfied the check and cannot show a review score.
             f'data-provider="{attr(source or item.get("comparison_platform"))}" '
             f'data-verified-at="{attr(item.get("guest_rating_checked_at"))}" href="{attr(url)}" '
             f'target="_blank" rel="noopener noreferrer">{esc(shown)}</a>') if url else esc(shown)
    reviews = f' · {as_text(count)} reviews' if count is not None else ""
    origin = f' · {esc(source)}' if source else ""
    return (f'<li class="option-rating" data-rating-status="{attr(item.get("guest_rating_status"))}" '
            f'data-rating-value="{attr(value)}" data-rating-count="{attr(count)}">'
            f'<strong>Guest rating: </strong>{inner}{reviews}{origin}</li>')


def dining_rating_line(item: dict) -> str:
    """Print the venue's rating, its count and where it came from.

    The plan collected all of it and the page printed none of it, so a recommendation looked
    identical whether somebody had opened the venue's page or copied it out of a blog listicle.
    That is not hypothetical: a delivered plan shipped a dinner at a venue with no listing on
    any platform, and the traveller had no way to tell. The count travels with the value on
    purpose -- 4.8 from 12 reviews and 4.3 from 2,000 are different claims -- and a card that
    honestly has no rating says so rather than staying silent, because silence reads as an
    omission while "no public rating: market stalls are rated individually" reads as a decision.
    """
    status = str(item.get("rating_status") or "").strip().casefold()
    if status == "none":
        reason = item.get("rating_absence_reason")
        return (f'<p class="meta dining-rating" data-rating-status="none">'
                f'<strong>Rating: </strong>no public rating'
                f'{" · " + esc(reason) if reason else ""}</p>')
    value, scale, count = item.get("rating_value"), item.get("rating_scale"), item.get("rating_count")
    if value is None:
        return ""
    source = item.get("rating_source")
    url = item.get("rating_url")
    shown = f'{as_text(value)}/{as_text(scale or 5)}'
    reviews = f' · {as_text(count)} reviews' if count is not None else ""
    origin = f' · {esc(source)}' if source else ""
    body = (f'<strong>Rating: </strong>{esc(shown)}{reviews}{origin}')
    if url:
        # Classed rather than bare so check_link_targets.py follows it. The rating is the one
        # field on the card that testifies somebody opened the venue's page, and for a while it
        # was the least verified link on the page: the checker reads booking-link, dining-link
        # and map-link, and this anchor carried none of them.
        body = (f'<strong>Rating: </strong>'
                f'<a class="dining-link" data-dining-provider="{attr(item.get("rating_source"))}" '
                f'data-verified-at="{attr(item.get("rating_checked_at"))}" '
                f'href="{attr(url)}" target="_blank" rel="noopener noreferrer">{esc(shown)}</a>'
                f'{reviews}{origin}')
    return (f'<p class="meta dining-rating" data-rating-status="{attr(item.get("rating_status"))}" '
            f'data-rating-value="{attr(value)}" data-rating-count="{attr(count)}">{body}</p>')


def dining_hours_line(item: dict, day_date: object = None) -> str:
    """Show the researched opening hours, and say plainly when nobody verified them.

    The plan collected `venue_hours` and `hours_status` and the page printed neither, so a
    dinner card looked identical whether its hours had been confirmed with the venue or
    guessed -- which is how a 20:00 dinner survives at a place that closes at 17:00 on that
    weekday. Anything other than "verified" gets the warning treatment, because a quiet meta
    line at the bottom of a card is exactly the presentation that let this go unnoticed.
    """
    hours = item.get("venue_hours")
    # The hours as printed: the author's text fenced, the renderer's "closed today" and "(today)"
    # left translatable.
    shown = esc(hours) if hours else ""
    # When the card carries the per-weekday table, print the hours for the day this meal is
    # actually on. `venue_hours` has to be the narrowest window that holds every weekday so the
    # closed-day check can parse it, which means the page was showing the traveller LESS than had
    # been researched -- on one real run, eight venues were looked up per weekday and all eight
    # were flattened before they reached the page.
    table = item.get("venue_hours_by_weekday")
    if isinstance(table, dict) and isinstance(day_date, str) and len(day_date) >= 10:
        try:
            weekday = date.fromisoformat(day_date[:10]).weekday()
        except ValueError:
            weekday = None
        if weekday is not None:
            today = table.get(("mon", "tue", "wed", "thu", "fri", "sat", "sun")[weekday])
            if str(today or "").strip().casefold() in ("closed", "休息", "闭店", "不营业"):
                hours = "closed today"
                shown = hours
            elif today is not None and str(today).strip():
                hours = f"{today} (today)"
                shown = f"{esc(today)} (today)"
    raw_status = str(item.get("hours_status") or "").strip()
    if not hours and not raw_status:
        return ""
    status = raw_status.casefold()
    # An unrecognised status word is not evidence that anyone checked, so it reads as
    # unverified rather than being trusted or silently dropped.
    status_text = HOURS_STATUS_ENGLISH.get(status, HOURS_STATUS_ENGLISH["unverified"])
    treatment = "meta" if status == "verified" else "warning"
    window = f"{shown} · " if shown else ""
    return (
        f'<p class="{treatment} dining-hours" data-hours-status="{attr(raw_status)}">'
        f'<strong>Opening hours: </strong>{window}'
        f'<span class="dining-hours-status">{status_text}</span></p>'
    )


def reservation_need_label(item: dict) -> str:
    need = item.get("reservation_need")
    if isinstance(need, str) and need.startswith("TODO"):
        # Printed, so the page gate's TODO scan refuses the page: a skeleton still renders, and an
        # unfilled need cannot ship as a card with no reminder rule.
        return f'<span class="reservation-need">{esc(need)}</span> · '
    if need not in RESERVATION_NEED_ENGLISH:
        return ""
    return f'<span class="reservation-need" data-reservation-need="{need}">{RESERVATION_NEED_ENGLISH[need]}</span> · '


def dining_cards(value: object, day_date: object = None) -> str:
    if not isinstance(value, list) or not value:
        return '<p class="meta">No meal recommendation was researched.</p>'
    cards = []
    for item in value:
        if not isinstance(item, dict):
            continue
        provider = as_text(item.get("map_provider"), "Map provider")
        backup = ""
        if item.get("backup_venue_name"):
            backup = f'<p class="meta">Backup: {esc(item.get("backup_venue_name"))} — {esc(item.get("backup_note"), "Check current opening hours before switching.")}</p>'
        reservation = ""
        if item.get("reservation_url"):
            reservation = f'<a class="dining-reservation-link" data-dining-provider="{attr(item.get("reservation_provider") or provider)}" data-verified-at="{attr(item.get("checked_at"))}" href="{attr(item.get("reservation_url"))}" target="_blank" rel="noopener noreferrer">Review reservation</a>'
        cards.append(
            f'<article class="dining-stop" data-meal="{attr(item.get("meal"))}">'
            f'<p class="eyebrow">{vocab(item.get("meal"))} · {esc(item.get("time_window"))}</p>'
            f'<h4>{esc(item.get("venue_name"))}</h4>'
            f'<p>{esc(item.get("cuisine_or_style"))} · {esc(item.get("neighborhood"))}</p>'
            f'<p>{esc(item.get("why_this_stop"))}</p>'
            f'<p class="meta">{markup(money(item.get("price_per_person_low"), item.get("price_per_person_high"), item.get("currency")))} per person · {reservation_need_label(item)}{esc(item.get("reservation_or_queue_note"))}</p>'
            f'{dining_rating_line(item)}'
            f'{dining_hours_line(item, day_date)}'
            f'<a class="dining-link" data-dining-provider="{attr(provider)}" data-verified-at="{attr(item.get("checked_at"))}" href="{attr(item.get("venue_url"))}" target="_blank" rel="noopener noreferrer">View restaurant in {markup(printed(item.get("map_provider"), "Map provider"))}</a>'
            f'{reservation}{backup}</article>'
        )
    return f'<div class="dining-grid">{"".join(cards)}</div>'


def imagery_figure(entry: object, alt: object) -> str:
    """A verified photograph with the attribution its licence requires.

    The credit line is not decoration and not politeness: these are CC BY / CC BY-SA files, and
    the licence is the reason they may be in this file at all. The caption names the article the
    image came from rather than asserting "this is X", because what was verified is the
    provenance -- a lead image is chosen by editors and can show the subject from an angle nobody
    would caption that way.
    """
    entry = entry if isinstance(entry, dict) else {}
    source = entry.get("data_uri")
    if not source:
        return ""
    credit = " · ".join(str(part) for part in
                        (entry.get("artist"), entry.get("license")) if part)
    link = entry.get("file_url") or entry.get("page_url") or ""
    return (f'<figure class="anchor-photo"><img src="{attr(source)}" alt="{attr(alt)}" '
            f'loading="lazy" decoding="async">'
            f'<figcaption class="photo-credit">Photo credit: '
            + (f'<a href="{attr(link)}" target="_blank" rel="noopener noreferrer">{esc(credit)}</a>'
               if link else esc(credit))
            + f' · via Wikimedia, from the article {esc(entry.get("page"))}</figcaption></figure>')


def destination_anchor_cards(value: object, imagery: object = None) -> str:
    if not isinstance(value, list):
        return ""
    items = []
    ordered = sorted(
        (anchor for anchor in value if isinstance(anchor, dict)),
        key=lambda anchor: anchor.get("planned_day") if isinstance(anchor.get("planned_day"), int) else 10**6,
    )
    images = imagery if isinstance(imagery, dict) else {}
    positions = {id(a): i for i, a in enumerate(value) if isinstance(a, dict)}
    for anchor in ordered:
        if not isinstance(anchor, dict):
            continue
        photo = imagery_figure(images.get(f"anchor:{positions.get(id(anchor))}"),
                               anchor.get("name"))
        # The traveller stated what the trip was for; this is where the page answers them. The
        # link exists in the data either way, but a field only they can verify is worth nothing
        # while it stays in the JSON: they are the only reader who knows whether "old-town lanes"
        # is really what they meant by "街区漫步".
        serves = anchor.get("satisfies_preference")
        serves_line = (f'<p class="meta anchor-serves"><strong>You asked for: </strong>'
                       f'{esc(serves)}</p>') if serves else ""
        items.append(
            f'<article class="anchor"><span class="pill">Day {esc(anchor.get("planned_day"))}</span><h3>{esc(anchor.get("name"))}</h3>'
            f'<p>{esc(anchor.get("category"))} · {esc(anchor.get("neighborhood_or_area"))}</p>'
            f'<p>{esc(anchor.get("why_it_matters"))}</p>{serves_line}{photo}'
            f'<a class="anchor-link" data-verified-at="{attr(anchor.get("checked_at"))}" href="{attr(anchor.get("source_url"))}" target="_blank" rel="noopener noreferrer">View source</a></article>'
        )
    return f'<section id="destination-essentials" class="panel"><h2>Destination essentials</h2><div class="grid">{"".join(items)}</div></section>' if items else ""


def link_for_ticket(ticket: dict | None) -> str:
    if not ticket:
        return "No separate ticket is required or it was not verified."
    return f'<a class="booking-link" data-booking-type="ticket" data-provider="{attr(as_text(ticket.get("official_or_authorised_provider"), "Provider"))}" data-verified-at="{attr(as_text(ticket.get("checked_at")))}" href="{attr(ticket.get("review_url"))}" target="_blank" rel="noopener noreferrer">Review ticket: {esc(ticket.get("attraction_name"))}</a>'


def intake_context_errors(intake_context: object) -> list[str]:
    """Refuse a plan that will not say how its requirements were collected.

    This one is required rather than optional, and that is the whole point. SKILL.md already said
    to default to the HTML form and fall back to chat only when the traveller declines, and other
    harnesses read "default" as a preference and opened no form at all. An optional field changes
    nothing there: the agent that skipped the form is exactly the agent that omits the key, so the
    gate reports clean on the run that motivated it. Required, the shortcut has to be declared, and
    declaring it costs more than doing the intake properly.

    Each branch demands the evidence that it was allowed, not just its own name:

    - `html_form` names the saved intake file, which only the intake server writes.
    - `user_supplied` says what the traveller supplied instead, so "they told me already" is a
      claim with content rather than a shrug.
    - `chat_fallback` carries the traveller's own words declining the form, and when they said so.
      Their words, not a summary: this is the one branch the traveller has to authorise, and a
      paraphrase is indistinguishable from an assistant that decided for them.

    Placeholders are rejected outright. A skeleton's `TODO:` string satisfies "is this key
    present" and answers nothing, which is how a whole intake gate goes green on an empty form.

    Called from save_trip_deliverables.py rather than validate_plan, and deliberately: the
    requirement is about handing a plan to a traveller, not about rendering a draft. Putting it in
    validate_plan would fail new_plan_skeleton.py's own output -- a skeleton cannot know how the
    requirements were collected -- and retroactively invalidate every plan already in a workspace,
    which audit_workspace.py reads with this same validator.
    """
    errors: list[str] = []
    if intake_context is None:
        return ["intake_context is required: say how this plan's requirements were collected "
                "(method html_form | user_supplied | chat_fallback). The loopback HTML form is "
                "the required path; chat_fallback is legitimate only when the traveller declined "
                "it, and this field is where that shows."]
    if not isinstance(intake_context, dict):
        return ["intake_context must be an object."]

    method = intake_context.get("method")
    if method not in INTAKE_METHODS:
        return [f"intake_context.method must be one of: {', '.join(INTAKE_METHODS)}."]

    required = {
        "html_form": ("intake_file",),
        "user_supplied": ("source_note",),
        "chat_fallback": ("declined_verbatim", "declined_at"),
    }[method]
    for field in required:
        value = intake_context.get(field)
        if not isinstance(value, str) or not value.strip():
            errors.append(cite("intake.provenance", f"intake_context.{field} is required when method is {method}."))
        elif any(marker in value for marker in ("TODO:", "example.invalid")):
            errors.append(cite("intake.provenance", f"intake_context.{field} still holds a placeholder, which answers nothing."))
        elif field != "declined_verbatim" and re.search(r"<[^<>\s]{1,60}>", value):
            # templates/final-trip-plan.json ships intake_file as
            # "<workspace>/plans/trip-intake-<timestamp>.json", and a template copied without
            # editing is a non-empty string carrying no TODO -- it would pass every check above.
            # Not applied to declined_verbatim: that is a human being quoted, and refusing their
            # sentence because it contains a bracket would be the gate inventing a defect.
            #
            # The bracketed run must contain no whitespace, and that is the whole difference
            # between a gate and a nuisance. Written as `<[^<>]{1,60}>` first, it refused
            # "Budget stated as < 2000 > per person" -- an ordinary sentence, rejected as a
            # placeholder, on the delivery path. Every placeholder this template actually ships
            # is a single token; prose that happens to compare two numbers is not.
            errors.append(cite("intake.provenance", f"intake_context.{field} is still the template's <bracketed> placeholder."))

    # What this deliberately does NOT do: require intake_file to resolve on disk. It was written
    # that way first, on the reasoning that claiming the form ran should cost producing what the
    # form writes -- and it made every legitimate re-save fail. A plan is a portable document: it
    # is re-rendered, replanned weeks later, audited from a moved workspace, restored from backup.
    # Tying its validity to a sibling file still existing on this machine blocks the traveller's
    # own plan for a reason that has nothing to do with how intake happened, and the way out the
    # error suggested was to relabel the method, i.e. to write something false. A forged path is
    # no harder than a forged file anyway, so the check bought little and broke much.
    # A record that contradicts itself is worse than a missing one, because it reads as evidence.
    # new_plan_skeleton.py accepted --from-intake together with --intake-method chat_fallback and
    # emitted exactly that: the traveller's declining words next to the path of the form intake
    # they supposedly never filled. Only one of those can be true.
    intake_file = intake_context.get("intake_file")
    if method != "html_form" and isinstance(intake_file, str) and intake_file.strip():
        errors.append(cite("intake.provenance", 
            f"intake_context says method {method} but also names an intake_file "
            f"({intake_file.strip()}), which only the form server writes. Either the form was "
            "filled -- method html_form -- or it was not, and the file does not belong here."))

    if method == "chat_fallback":
        declined_at = intake_context.get("declined_at")
        if isinstance(declined_at, str) and declined_at.strip():
            if not is_iso_datestamp(declined_at):
                errors.append(cite("intake.provenance", "intake_context.declined_at must be an ISO date or date-time."))
            elif declined_at.startswith("1970-01-01"):
                # new_plan_skeleton.py stamps every date it cannot know as the epoch, and its own
                # docstring lists that as a hole: 1970 is conspicuous on a page but no gate rejects
                # it. Here it would be a fabricated fact in the one record that says the traveller
                # authorised the shortcut, so this is the one date field where the sentinel is an
                # error rather than a visible blank.
                errors.append(cite("intake.provenance", 
                    "intake_context.declined_at is still the skeleton's 1970-01-01 placeholder. "
                    "Write the date the traveller actually declined the form; a provenance record "
                    "with an invented date is worse than none."))
    return errors


def itinerary_findings(leg: object, label: str, cite_fn) -> list[str]:
    """What a flight or ground leg owes, with one honest way out for the service identifier.

    The identifier is the one field on this card that cannot be derived, estimated or bracketed:
    a fare has a range, a duration has a typical value, but a flight number is either the right
    string or a lie. When the author has not been able to price the actual services for the actual
    dates -- which is the ordinary case on a route with no direct flight, where the search page is
    the only place the answer exists -- the contract used to leave two moves: invent a plausible
    number, or put prose in a field meant for a code. Both were taken on one real run, and the
    first is the worse of the two by a distance: a fabricated `KL1927` reads as researched to
    every gate and to the traveller, and this repository has already shipped exactly that.

    So the identifier gets the same escape the dining rating has -- `rating_status: "none"` plus a
    written reason -- and for the same reason: a blank that says why it is blank is information,
    while a confident wrong value is a defect nothing downstream can see. Everything else on the
    leg is still required, because "I could not name the flight" is not "I know nothing about the
    journey": the duration, the stops and the interchange note all come off the route itself.
    """
    found: list[str] = []
    if not isinstance(leg, dict):
        return [cite_fn("booking.option_contract",
                        f"{label} needs the service identifier, local times, duration, changes, "
                        f"and an interchange note.")]
    status = str(leg.get("service_identifier_status") or "researched")
    if status not in SERVICE_IDENTIFIER_STATUSES:
        return [cite_fn("booking.option_contract",
                        f"{label}.service_identifier_status must be researched or unresearched.")]
    required = ["departure_local", "arrival_local", "duration_minutes", "stops",
                "connection_or_terminal_note"]
    if status == "researched":
        required.append("service_identifier")
    else:
        if not visible_text(leg.get("service_identifier_unresearched_reason")):
            found.append(cite_fn("booking.option_contract",
                f"{label} is marked unresearched with no reason. Say what could not be checked and "
                f"where the traveller will find it -- a blank that explains itself is information, "
                f"an invented flight number is not."))
        if visible_text(leg.get("service_identifier")):
            found.append(cite_fn("booking.option_contract",
                f"{label} is marked unresearched but still carries a service identifier "
                f"{leg.get('service_identifier')!r}. Clear it, or drop the unresearched mark: a "
                f"value sitting under a label that says nobody checked it is the worst of both."))
        # The times are what a traveller plans the day around, so an unresearched identifier does
        # not excuse them -- but it does mean they may be the intended window rather than a
        # booked one, which the reason above is where to say.
    # `is None or == ""` lets whitespace through, and a service identifier of "   " then reads as
    # researched to every gate while the page shows a blank. visible_text() is the same test the
    # arrival-essentials block already uses, and it also catches the invisible characters that
    # strip() does not -- a zero-width space is content to Python and blank to a reader.
    def missing(key: str) -> bool:
        value = leg.get(key)
        if isinstance(value, str):
            return not visible_text(value)
        return value is None or value == ""

    if any(missing(key) for key in required):
        found.append(cite_fn("booking.option_contract",
            f"{label} needs " + ("the service identifier, " if status == "researched" else "")
            + "local times, duration, changes, and an interchange note."))
    elif not (isinstance(leg.get("duration_minutes"), (int, float))
              and not isinstance(leg.get("duration_minutes"), bool)
              and leg["duration_minutes"] > 0):
        found.append(cite_fn("booking.option_contract",
            f"{label}.duration_minutes must be a positive number of minutes."))
    return found


def validate_plan(plan: dict) -> list[str]:
    errors: list[str] = []
    if not is_iso_datestamp(plan.get("generated_at")):
        errors.append("generated_at must be an ISO date or date-time.")
    if plan.get("plan_status") not in BOOKING_STATES:
        errors.append("plan_status must be idea, researched, held, or booked.")
    if not isinstance(plan.get("assumptions", []), list):
        errors.append("assumptions must be a list.")
    # What the traveller needs in the first hour on the ground. Every other block in this contract
    # is about the days; none of them answered "can I pay", "can I get online", "who do I call".
    # Required rather than encouraged, because a note about a missing section is a note nobody
    # reads -- and each entry may be marked not_applicable WITH A REASON, which is how a domestic
    # trip says it needs no consulate without pretending it researched one.
    essentials = plan.get("arrival_essentials")
    if not isinstance(essentials, dict):
        errors.append(cite("arrival.essentials",
            "arrival_essentials is required: payment, connectivity, emergency and "
            "health_and_insurance, each researched and dated or marked not_applicable with a "
            "reason. A page that plans six days and cannot say whether the traveller's card will "
            "work has answered the easy half."))
    else:
        for name in ESSENTIAL_ENTRIES:
            item = essentials.get(name)
            if not isinstance(item, dict):
                errors.append(cite("arrival.essentials",
                    f"arrival_essentials.{name} is missing. Fill it, or set status="
                    f"\"not_applicable\" with a not_applicable_reason."))
                continue
            status = str(item.get("status") or "")
            if status not in ESSENTIAL_STATUSES:
                errors.append(cite("arrival.essentials",
                    f"arrival_essentials.{name}.status must be one of: "
                    + ", ".join(ESSENTIAL_STATUSES) + "."))
            elif status == "not_applicable":
                if not visible_text(item.get("not_applicable_reason")):
                    errors.append(cite("arrival.essentials",
                        f"arrival_essentials.{name} is not_applicable with no reason. 'The "
                        f"traveller is at home' is a reason; silence is indistinguishable from "
                        f"nobody having looked."))
            else:
                if not visible_text(item.get("summary")):
                    errors.append(cite("arrival.essentials",
                        f"arrival_essentials.{name} needs a summary the traveller can act on."))
                # Same evidence standard as every other researched fact here. Written from memory,
                # these are exactly the claims that are confidently wrong: which cards a country
                # takes, and what number to dial, both change and both are looked up in seconds.
                if status == "researched":
                    if not is_https(str(item.get("source_url") or "")):
                        errors.append(cite("arrival.essentials",
                            f"arrival_essentials.{name} claims research with no HTTPS source_url. "
                            f"These are the facts most often recalled rather than checked."))
                    if not is_iso_datestamp(item.get("checked_at")):
                        errors.append(cite("arrival.essentials",
                            f"arrival_essentials.{name}.checked_at must be an ISO date or "
                            f"date-time."))
        emergency = essentials.get("emergency")
        if isinstance(emergency, dict) and str(emergency.get("status")) == "researched" \
                and not visible_text(emergency.get("local_emergency_number")):
            errors.append(cite("arrival.essentials",
                "arrival_essentials.emergency is researched but names no local emergency number. "
                "That is the one field in this block somebody dials while something is going "
                "wrong."))

    entry_context = plan.get("entry_context")
    if entry_context is not None:
        if not isinstance(entry_context, dict):
            errors.append("entry_context must be an object when present.")
        else:
            if entry_context.get("status") not in ENTRY_STATUSES:
                errors.append("entry_context.status must be one of: " + ", ".join(ENTRY_STATUSES) + ".")
            for field in ("summary", "traveler_basis", "source_url", "checked_at"):
                if not entry_context.get(field):
                    errors.append(f"entry_context.{field} is required when entry_context is present.")
            if entry_context.get("source_url") and not is_https(entry_context["source_url"]):
                errors.append("entry_context.source_url must be a safe HTTPS URL.")
            if entry_context.get("checked_at") and not is_iso_datestamp(entry_context["checked_at"]):
                errors.append("entry_context.checked_at must be an ISO date or date-time.")
            # Each jurisdiction's answer is printed exactly like the flat one, so it is held to
            # the same vocabulary: a free-text status cannot be translated and reads to the
            # traveller as an answer somebody checked. The template's own specimen -- a `_note`
            # beside nulls -- is not a record anyone wrote, so it is skipped rather than refused.
            for index, record in enumerate(as_list(entry_context.get("per_jurisdiction"))):
                if not isinstance(record, dict):
                    errors.append(cite("entry.per_jurisdiction",
                                       f"entry_context.per_jurisdiction[{index}] must be an object."))
                    continue
                if all(value is None for key, value in record.items() if key != "_note"):
                    continue
                if record.get("status") not in ENTRY_STATUSES:
                    errors.append(cite("entry.per_jurisdiction",
                                       f"entry_context.per_jurisdiction[{index}].status must be one of: "
                                       + ", ".join(ENTRY_STATUSES) + "."))
                if record.get("source_url") and not is_https(record["source_url"]):
                    errors.append(cite("entry.per_jurisdiction",
                                       f"entry_context.per_jurisdiction[{index}].source_url must be "
                                       f"a safe HTTPS URL."))
                if record.get("checked_at") and not is_iso_datestamp(record["checked_at"]):
                    errors.append(cite("entry.per_jurisdiction",
                                       f"entry_context.per_jurisdiction[{index}].checked_at must be "
                                       f"an ISO date or date-time."))
    trip = plan.get("trip") if isinstance(plan.get("trip"), dict) else {}
    for field in ("title", "language", "currency", "origin", "destination", "destination_type", "start_date", "end_date", "traveler_count", "pace", "budget_basis", "arrival_transport_mode"):
        if not trip.get(field):
            errors.append(f"trip.{field} is required.")
    if trip.get("language") and not has_builtin_interface_language(trip["language"]):
        custom_labels = plan.get("ui_labels")
        if not isinstance(custom_labels, dict):
            errors.append(cite("html.localization", "A non-English/Chinese plan needs a complete ui_labels object for renderer-owned interface text."))
        else:
            missing = REQUIRED_UI_LABEL_KEYS - set(custom_labels)
            invalid = [
                key
                for key in REQUIRED_UI_LABEL_KEYS
                if not isinstance(custom_labels.get(key), str) or (not custom_labels[key].strip() and key != "day_suffix")
            ]
            if missing or invalid:
                errors.append(cite("html.localization", "ui_labels must provide every renderer label for a non-English/Chinese plan: " + ", ".join(sorted(missing | set(invalid))) + "."))
    # Optional, and only checked when it is there: every plan authored before intake started
    # carrying constraints has no such key and must validate exactly as it did. What is checked
    # is the shape the downstream gates read -- a severity outside the enum or a walking cap
    # written as prose does not fail loudly, it fails silently, by leaving the mobility and
    # dietary checks with nothing to compare against.
    constraints = trip.get("traveler_constraints")
    if constraints is not None:
        if not isinstance(constraints, dict):
            errors.append("trip.traveler_constraints must be an object with the traveller's dietary, allergy, and mobility fields, or be omitted entirely.")
        else:
            severity = constraints.get("allergy_severity")
            if severity is not None and severity not in ALLERGY_SEVERITIES:
                errors.append("trip.traveler_constraints.allergy_severity must be one of: " + ", ".join(ALLERGY_SEVERITIES) + ".")
            walking_cap = constraints.get("max_continuous_walking_minutes")
            if walking_cap is not None and (
                not isinstance(walking_cap, int) or isinstance(walking_cap, bool) or walking_cap <= 0
            ):
                errors.append("trip.traveler_constraints.max_continuous_walking_minutes must be a positive whole number of minutes (for example 20), or null when the traveller stated no limit.")
            for field in ("dietary_or_religious_needs", "mobility_notes"):
                if constraints.get(field) is not None and not isinstance(constraints[field], list):
                    errors.append(f"trip.traveler_constraints.{field} must be a list of strings, so each need stays separately readable.")
    if trip.get("arrival_transport_mode") not in set(ARRIVAL_MODES):
        errors.append("trip.arrival_transport_mode must be flight, rail, road, or other.")
    if trip.get("destination_type") not in {"city", "region", "multi-stop", "other"}:
        errors.append("trip.destination_type must be city, region, multi-stop, or other.")
    trip_start = parse_iso_date(trip.get("start_date"), "trip.start_date", errors)
    trip_end = parse_iso_date(trip.get("end_date"), "trip.end_date", errors)
    if trip_start and trip_end and trip_end < trip_start:
        errors.append("trip.end_date cannot be before trip.start_date.")
    budget = plan.get("budget") if isinstance(plan.get("budget"), dict) else {}
    if budget.get("calculation_basis") != "per_person":
        errors.append("budget.calculation_basis must be per_person.")
    if budget.get("estimated_per_person_low") is None or budget.get("estimated_per_person_high") is None:
        errors.append("budget needs estimated_per_person_low and estimated_per_person_high.")
    elif not is_nonnegative_money_range(budget["estimated_per_person_low"], budget["estimated_per_person_high"]):
        errors.append("budget estimated_per_person_low/high must be non-negative numbers with low less than or equal to high.")
    if not isinstance(budget.get("included_categories"), list) or not budget.get("included_categories"):
        errors.append("budget.included_categories must name the categories included in the per-person total.")
    if not isinstance(budget.get("unverified_categories"), list):
        errors.append("budget.unverified_categories must be a list.")
    else:
        unknown_unverified = {str(item) for item in as_list(budget.get("unverified_categories"))} - set(BUDGET_CATEGORIES)
        if unknown_unverified:
            errors.append("budget.unverified_categories uses unsupported categories: " + ", ".join(sorted(unknown_unverified)) + ".")
    if isinstance(budget.get("included_categories"), list):
        unknown_included = {str(item) for item in as_list(budget.get("included_categories"))} - set(BUDGET_CATEGORIES)
        if unknown_included:
            errors.append("budget.included_categories uses unsupported categories: " + ", ".join(sorted(unknown_included)) + ".")
    breakdown = budget.get("breakdown")
    if not isinstance(breakdown, list) or not breakdown:
        errors.append("budget.breakdown must contain a transparent per-person cost breakdown.")
    else:
        breakdown_categories: set[str] = set()
        for number, item in enumerate(breakdown, 1):
            required_breakdown_fields = ("category", "description", "per_person_low", "per_person_high", "currency", "price_status", "checked_at", "note")
            if not isinstance(item, dict) or not all(item.get(field) is not None and item.get(field) != "" for field in required_breakdown_fields):
                errors.append(f"budget.breakdown[{number}] needs category, per-person range, currency, price status, check time, and note.")
                continue
            if item["currency"] != trip.get("currency"):
                errors.append(f"budget.breakdown[{number}].currency must match trip.currency.")
            if not is_nonnegative_money_range(item["per_person_low"], item["per_person_high"]):
                errors.append(f"budget.breakdown[{number}] per-person range must be non-negative numbers with low less than or equal to high.")
            if not is_one_of(item.get("price_status"), PRICE_STATUSES):
                errors.append(f"budget.breakdown[{number}].price_status must be researched_current, estimate, or user_confirmed.")
            if not is_iso_datestamp(item["checked_at"]):
                errors.append(f"budget.breakdown[{number}].checked_at must be an ISO date or date-time.")
            if item["category"] not in BUDGET_CATEGORIES:
                errors.append(f"budget.breakdown[{number}].category must be one of: " + ", ".join(BUDGET_CATEGORIES) + ".")
            if item["category"] in breakdown_categories:
                errors.append(f"budget.breakdown has duplicate category: {item['category']}.")
            breakdown_categories.add(item["category"])
        if isinstance(budget.get("included_categories"), list):
            missing_breakdown = {str(category) for category in budget["included_categories"]} - breakdown_categories
            if missing_breakdown:
                errors.append("budget.breakdown is missing included categories: " + ", ".join(sorted(missing_breakdown)) + ".")
    transport = plan.get("transport_preference") if isinstance(plan.get("transport_preference"), dict) else {}
    mode = transport.get("mode")
    if mode not in set(TRANSPORT_MODES):
        errors.append("transport_preference.mode must be self-drive or public-transit.")
    regional_context = plan.get("regional_service_context") if isinstance(plan.get("regional_service_context"), dict) else {}
    for field in ("destination_service_market", "selection_basis", "primary_map_provider"):
        if not regional_context.get(field):
            errors.append(cite("market.context_contract", f"regional_service_context.{field} is required."))
    if regional_context.get("google_services_access") not in {"available", "unavailable", "unknown"}:
        errors.append(cite("market.context_contract", "regional_service_context.google_services_access must be available, unavailable, or unknown."))
    for field in ("alternative_map_providers", "local_transport_sources"):
        if not isinstance(regional_context.get(field), list):
            errors.append(cite("market.context_contract", f"regional_service_context.{field} must be a list."))
    market = str(regional_context.get("destination_service_market") or "").casefold()
    primary_provider = str(regional_context.get("primary_map_provider") or "")
    mainland_primary_exception = regional_context.get("primary_map_exception_reason")
    if market == "mainland_china" and not any(token in primary_provider.casefold() for token in ("amap", "高德")) and not mainland_primary_exception:
        errors.append(cite("market.provider_routing", "mainland_china plans require Amap/高德地图 as the primary map provider unless a user-confirmed primary_map_exception_reason is recorded."))
    if market == "mainland_china" and is_google_map(primary_provider, ""):
        errors.append(cite("market.provider_routing", "Google Maps cannot be the mainland-China primary provider."))
    booking_access_categories = validate_booking_access_checks(regional_context.get("booking_access_checks"), errors)
    days = plan.get("days") if isinstance(plan.get("days"), list) else []
    if not days:
        errors.append("At least one day is required.")
    day_dates: dict[int, date] = {}
    # Per-day market, for the same reason the page gate now does it per day: a trip that crosses a
    # market boundary had one flag for all of it, so a Shenzhen+Hong Kong plan was told that its
    # Hong Kong days must use Amap -- not the tool for Hong Kong transit -- and the traveller's only
    # ways out were wrong links for half the trip or no page at all. A day with no jurisdiction of
    # its own inherits the trip's, which is what keeps every single-market plan unchanged.
    _stays = {str(a.get("id")): a for a in
              (plan.get("booking_options") or {}).get("accommodations", []) if isinstance(a, dict)}

    def _day_context(day: dict) -> tuple[dict, str]:
        stay = _stays.get(str(day.get("accommodation_option_id") or ""))
        declared = str((stay or {}).get("jurisdiction") or "").strip()
        if not declared:
            return regional_context, market
        context = {**regional_context, "destination_service_market": declared}
        # `google_services_access` is one value for the whole trip, and its meaning is "can the
        # traveller reach Google where they are" -- which is exactly the thing that differs on a
        # trip that crosses this boundary. A Shenzhen+Hong Kong plan sets it `unavailable` because
        # of the Shenzhen half, and that then blocked the Hong Kong half from using the only map
        # provider that works there. Relaxed for a day that declares a non-mainland jurisdiction
        # ONLY when the trip's own market is the mainland, so a plan marked unavailable for some
        # other reason -- a country this repo has never modelled -- is not quietly excused.
        if is_mainland_market(market) and not is_mainland_market(declared) \
                and context.get("google_services_access") == "unavailable":
            context["google_services_access"] = "available"
        return context, declared.casefold()

    for expected, day in enumerate(days, 1):
        if not isinstance(day, dict) or day.get("number") != expected:
            errors.append("days must be objects numbered consecutively from 1.")
            continue
        if day.get("day_type") not in set(DAY_TYPES):
            errors.append(f"day {expected}.day_type must be arrival, departure, full, or transfer.")
        activities = day.get("activities")
        if not isinstance(activities, list) or not activities:
            errors.append(f"day {expected} needs at least one timed activity.")
        elif day.get("day_type") == "full" and len(activities) < 2:
            errors.append(f"day {expected} is a full day and needs at least two meaningful activities, or must be marked as a deep single-site day with its reason.")
        if isinstance(activities, list):
            # Two optional per-activity fields. Each is rejected only when it is present and
            # malformed, so a plan that omits it keeps validating exactly as before.
            for activity_number, activity in enumerate(activities, 1):
                if not isinstance(activity, dict):
                    continue
                # ticket_note is optional -- most activities are free, and no plan carries it
                # everywhere -- but the day card prints it verbatim under a "Ticket" label the
                # traveller reads as researched fact. A number, an object, or a blank string
                # would put "None", "{}" or an empty prefix exactly where an admission price
                # and a ticketing channel belong.
                ticket_note = activity.get("ticket_note")
                if ticket_note is not None and (not isinstance(ticket_note, str) or not ticket_note.strip()):
                    errors.append(f"day {expected} activity {activity_number}.ticket_note must be a non-empty string naming the admission price and where the official ticket is sold (plus any queue or advance-booking caveat), or be omitted.")
                # An activity that never states its on-foot time is left out of the walking
                # figure rather than assumed to be zero. But a value of the wrong type is
                # worse than none at all -- "90 min" as prose reads as present, sums as nothing,
                # and hands the walking-budget check a total it will report with confidence.
                if activity.get("on_foot_minutes") is None:
                    continue
                on_foot = activity["on_foot_minutes"]
                if not isinstance(on_foot, int) or isinstance(on_foot, bool) or on_foot < 0:
                    errors.append(f"day {expected} activity {activity_number}.on_foot_minutes must be a whole number of minutes of 0 or more (the time spent on foot or standing during that activity), or be omitted.")
        day_date = parse_iso_date(day.get("date"), f"day {expected} date", errors)
        if day_date:
            day_dates[expected] = day_date
            if trip_start and trip_end and not trip_start <= day_date <= trip_end:
                errors.append(f"day {expected} date must fall within the trip date range.")
        route = day.get("route") if isinstance(day.get("route"), dict) else {}
        # One loop, two rules, so two citations. Splitting the tuple rather than citing the whole
        # loop to one place is the difference between a pointer and a shrug: the first five fields
        # are the day's visible travel burden and the last five are the map-button contract, and a
        # reader missing `map_link_kind` who is sent to the route-burden paragraph learns nothing
        # about why `directions` is the only accepted value. This loop was the single largest
        # uncited block on the real workspace before the split, and the map fields are the bulk
        # of what it emits.
        ROUTE_BURDEN_FIELDS = ("start", "end", "mode", "route_logic", "fallback_plan")
        for field in ROUTE_BURDEN_FIELDS + ("route_map_scope", "map_link_kind", "verified_map_url", "map_checked_at", "map_provider"):
            if not route.get(field):
                errors.append(cite(
                    "route.day_burden" if field in ROUTE_BURDEN_FIELDS else "map.link_contract",
                    f"day {expected} route.{field} is required."))
        if route.get("route_map_scope") and route.get("route_map_scope") not in ROUTE_MAP_SCOPES:
            errors.append(cite("map.link_contract", f"day {expected} route.route_map_scope must be multi_stop or primary_leg."))
        if route.get("map_link_kind") and route.get("map_link_kind") != "directions":
            errors.append(cite("map.link_contract", f"day {expected} route.map_link_kind must be directions."))
        if route.get("mode") and is_ambiguous_route_mode(route.get("mode")):
            errors.append(cite("route.day_burden", f"day {expected} route.mode must name one researched primary mode; put alternatives in fallback_plan."))
        if route.get("verified_map_url") and not is_https(route["verified_map_url"]):
            errors.append(cite("map.link_contract", f"day {expected} route.verified_map_url must be HTTPS."))
        elif route.get("verified_map_url") and route.get("map_provider") and not is_directions_url(route["map_provider"], route["verified_map_url"]):
            errors.append(cite("map.link_contract", f"day {expected} route.verified_map_url must be an actual directions URL, not a place/POI page."))
        day_context, day_market = _day_context(day)
        if route.get("map_provider") and route.get("verified_map_url") and not map_link_allowed(route["map_provider"], route["verified_map_url"], day_context):
            errors.append(cite("market.provider_routing", f"day {expected} route uses Google Maps despite the regional-access rule."))
        if is_mainland_market(day_market) and not mainland_primary_exception and route.get("map_provider") and route.get("verified_map_url") and not is_amap(route["map_provider"], route["verified_map_url"]):
            errors.append(cite("market.provider_routing", f"day {expected} mainland-China primary route must use Amap/高德地图."))
        validate_alternative_map_links(route.get("alternative_map_links"), f"day {expected} route", regional_context, errors)
        segments = route.get("segments")
        stops = route.get("stops_in_order")
        if not isinstance(stops, list) or len(stops) < 2 or not all(isinstance(stop, str) and stop.strip() for stop in stops):
            errors.append(f"day {expected} route.stops_in_order needs at least two named stops.")
        elif route.get("start") != stops[0] or route.get("end") != stops[-1]:
            errors.append(f"day {expected} route start/end must match the first/last stop in stops_in_order.")
        if not isinstance(segments, list) or not segments:
            errors.append(cite("map.link_contract", f"day {expected} route.segments needs at least one mapped segment."))
        else:
            if isinstance(stops, list) and len(stops) >= 2 and len(segments) != len(stops) - 1:
                errors.append(cite("map.link_contract", f"day {expected} route needs one exact segment for every consecutive pair in stops_in_order."))
            for segment_number, segment in enumerate(segments, 1):
                required_segment_fields = (
                    "from", "to", "mode", "duration_minutes", "walking_minutes", "transfer_count",
                    "service_or_line", "journey_instruction", "arrival_instruction", "fare_basis",
                    "fallback_note", "map_link_kind", "verified_map_url", "map_checked_at", "map_provider",
                )
                if not isinstance(segment, dict) or not all(segment.get(key) is not None and segment.get(key) != "" for key in required_segment_fields):
                    errors.append(cite("map.link_contract", f"day {expected} route segment {segment_number} needs endpoints, one primary mode, service/instructions, walk/transfers, fare basis, fallback, and a mapped directions URL."))
                    continue
                if segment.get("map_link_kind") != "directions":
                    errors.append(cite("map.link_contract", f"day {expected} route segment {segment_number}.map_link_kind must be directions."))
                if is_ambiguous_route_mode(segment.get("mode")):
                    errors.append(cite("map.link_contract", f"day {expected} route segment {segment_number}.mode must be one primary mode; alternatives belong in fallback_note."))
                if not is_nonnegative_number(segment.get("duration_minutes")) or not is_nonnegative_number(segment.get("walking_minutes")):
                    errors.append(cite("map.link_contract", f"day {expected} route segment {segment_number} duration_minutes and walking_minutes must be non-negative numbers."))
                if not isinstance(segment.get("transfer_count"), int) or isinstance(segment.get("transfer_count"), bool) or segment["transfer_count"] < 0:
                    errors.append(cite("map.link_contract", f"day {expected} route segment {segment_number}.transfer_count must be a non-negative integer."))
                if isinstance(stops, list) and segment_number < len(stops) and (segment.get("from") != stops[segment_number - 1] or segment.get("to") != stops[segment_number]):
                    errors.append(cite("map.link_contract", f"day {expected} route segment {segment_number} must match consecutive stops: {stops[segment_number - 1]} → {stops[segment_number]}."))
                if not is_https(segment["verified_map_url"]):
                    errors.append(cite("map.link_contract", f"day {expected} route segment {segment_number} map URL must be HTTPS."))
                elif not is_directions_url(segment["map_provider"], segment["verified_map_url"]):
                    errors.append(cite("map.link_contract", f"day {expected} route segment {segment_number} map URL must be a directions URL, not a place/POI page."))
                if not map_link_allowed(segment["map_provider"], segment["verified_map_url"], day_context):
                    errors.append(cite("market.provider_routing", f"day {expected} route segment {segment_number} uses Google Maps despite the regional-access rule."))
                if is_mainland_market(day_market) and not mainland_primary_exception and not is_amap(segment["map_provider"], segment["verified_map_url"]):
                    errors.append(cite("market.provider_routing", f"day {expected} mainland-China route segment {segment_number} must use Amap/高德地图."))
                validate_alternative_map_links(segment.get("alternative_map_links"), f"day {expected} route segment {segment_number}", regional_context, errors)
        if mode == "public-transit" and route.get("cost_low") is None and route.get("cost_high") is None:
            errors.append(cite("route.day_burden", f"day {expected} public-transit route needs a researched fare or range."))
        elif mode == "public-transit" and not is_nonnegative_money_range(route.get("cost_low"), route.get("cost_high")):
            errors.append(f"day {expected} public-transit route cost range must be non-negative numbers with low less than or equal to high.")
        if mode == "self-drive" and (
            route.get("duration_minutes") is None or route.get("distance_km") is None
        ):
            errors.append(f"day {expected} self-drive route needs duration_minutes and distance_km.")
        elif mode == "self-drive" and (not is_nonnegative_number(route.get("duration_minutes")) or not is_nonnegative_number(route.get("distance_km"))):
            errors.append(f"day {expected} self-drive route duration_minutes and distance_km must be non-negative numbers.")
        dining = day.get("dining")
        if not isinstance(dining, list):
            errors.append(cite("dining.card_contract", f"day {expected}.dining must be a list."))
        else:
            meal_types = {item.get("meal") for item in dining if isinstance(item, dict)}
            required_meals = {"lunch", "dinner"} if day.get("day_type") == "full" else {"dinner"} if day.get("day_type") == "arrival" else {"breakfast"} if day.get("day_type") == "departure" else set()
            missing_meals = required_meals - meal_types
            if missing_meals:
                errors.append(cite("dining.card_contract", f"day {expected} dining needs: {', '.join(sorted(missing_meals))}."))
            for dining_number, item in enumerate(dining, 1):
                required_dining_fields = ("meal", "time_window", "venue_name", "cuisine_or_style", "neighborhood", "why_this_stop", "price_per_person_low", "price_per_person_high", "currency", "reservation_or_queue_note", "venue_url", "map_provider", "checked_at")
                if not isinstance(item, dict) or not all(item.get(key) is not None and item.get(key) != "" for key in required_dining_fields):
                    errors.append(cite("dining.card_contract", f"day {expected} dining {dining_number} needs meal, concrete venue, price, queue note, source URL, map provider, and check time."))
                    continue
                if item.get("meal") not in set(MEAL_TYPES):
                    errors.append(cite("dining.card_contract", f"day {expected} dining {dining_number}.meal must be breakfast, lunch, dinner, or snack."))
                need = item.get("reservation_need")
                if need is not None and not str(need).startswith("TODO") and need not in RESERVATION_NEEDS:
                    errors.append(cite("dining.card_contract", f"day {expected} dining {dining_number}.reservation_need must be one of {', '.join(RESERVATION_NEEDS)}."))
                if not is_nonnegative_money_range(item.get("price_per_person_low"), item.get("price_per_person_high")):
                    errors.append(cite("dining.card_contract", f"day {expected} dining {dining_number} price range must be non-negative numbers with low less than or equal to high."))
                if not is_https(item.get("venue_url")):
                    errors.append(cite("dining.card_contract", f"day {expected} dining {dining_number}.venue_url must be HTTPS."))
                if item.get("reservation_url") and not is_https(item.get("reservation_url")):
                    errors.append(cite("dining.card_contract", f"day {expected} dining {dining_number}.reservation_url must be a safe HTTPS browse URL when present."))
    if trip_start and trip_end and len(day_dates) == len(days):
        expected_dates = [trip_start + timedelta(days=offset) for offset in range((trip_end - trip_start).days + 1)]
        actual_dates = [day_dates[number] for number in sorted(day_dates)]
        if actual_dates != expected_dates:
            errors.append("days must cover every trip date consecutively from trip.start_date through trip.end_date.")
    anchors = plan.get("destination_experience_anchors")
    if not isinstance(anchors, list):
        errors.append("destination_experience_anchors must be a list.")
    else:
        minimum_anchors = 3 if trip.get("destination_type") == "city" and len(days) >= 3 else 1
        if len(anchors) < minimum_anchors:
            errors.append(f"This trip needs at least {minimum_anchors} destination-specific experience anchor(s), so a city itinerary does not collapse into isolated headline attractions.")
        planned_anchor_days: set[int] = set()
        for number, anchor in enumerate(anchors, 1):
            required_anchor_fields = ("name", "category", "neighborhood_or_area", "planned_day", "why_it_matters", "source_url", "checked_at")
            if not isinstance(anchor, dict) or not all(anchor.get(field) for field in required_anchor_fields):
                errors.append(f"destination_experience_anchors[{number}] needs name, category, area, planned day, rationale, source URL, and check time.")
                continue
            if anchor["planned_day"] not in day_dates:
                errors.append(f"destination_experience_anchors[{number}].planned_day must name a real trip day.")
            else:
                planned_anchor_days.add(anchor["planned_day"])
            if not is_https(anchor["source_url"]):
                errors.append(f"destination_experience_anchors[{number}].source_url must be HTTPS.")
        if trip.get("destination_type") == "city" and len(days) >= 3 and len(planned_anchor_days) < 2:
            errors.append("A city itinerary needs destination-specific anchors across at least two planned days.")
    sources = plan.get("sources") if isinstance(plan.get("sources"), list) else []
    if not sources:
        errors.append("At least one source is required.")
    for source in sources:
        if not isinstance(source, dict) or not all(source.get(key) for key in ("name", "url", "source_type", "accessed_at")) or not is_https(source.get("url")):
            errors.append("Every source needs name, HTTPS url, source_type, and accessed_at.")
        elif not source.get("claim_or_decision_supported"):
            # Silently defaulting to "Plan evidence" turned an authoring slip into eighteen
            # identical rows: the measured plan wrote this field as `supports`, the renderer read
            # `claim_or_decision_supported`, nothing objected, and the register that exists to say
            # WHAT each source proves said nothing at all, eighteen times. A source register whose
            # every line reads the same is not a register.
            errors.append(
                "Every source needs claim_or_decision_supported saying what it proves -- the field "
                "is spelled that way in templates/final-trip-plan.json, and a register whose rows "
                "all read alike tells the traveller nothing about which fact rests on which page.")
        elif not is_iso_datestamp(source["accessed_at"]):
            errors.append("Every source.accessed_at must be an ISO date or date-time.")
        # confidence is OPTIONAL -- a source that records none falls back to
        # SOURCE_CONFIDENCE_DEFAULT -- but a value that IS recorded has to be a member of the
        # enum, for the same reason plan_status, dining[].meal and entry_context.status are
        # checked here: this value is printed as visible text, and visible text has to be
        # translatable. Checked in validate_plan rather than only in the HTML gate so the author
        # is told at render time, in the file they can fix, instead of by a structural failure on
        # a page they then have to trace backwards.
        #
        # This is the half of the fix that costs something. Delivered plans in a real workspace
        # carry prose here -- "primary source; timetable requires recheck", "official; schedule
        # needs recheck" -- and each of those now refuses to render until the qualification moves
        # into claim_or_decision_supported, the field beside it whose whole job is to say what a
        # source proves. That is a genuine cost and it was weighed against the alternative: keep
        # accepting anything, and a Chinese reader keeps being shown English machine words in a
        # register that is otherwise entirely Chinese, with every gate green. A field that renders
        # visibly and accepts anything is the hole.
        #
        # The hand-translated "高" is the case that got this wrong, and it is not the same case.
        # An author who wrote 高 was doing by hand what the enum now does by construction -- they
        # named one of the five levels, in the language of the plan -- and the first draft of this
        # rule made the one workspace plan that had already solved the problem the one plan that
        # could not render. canonical_enum_value() maps the spellings this file itself printed
        # back to their token; localized_enum_aliases' docstring carries the reasoning and the
        # limit. The accepted set stays closed, and prose is still refused.
        if isinstance(source, dict) and source.get("confidence") is not None:
            confidence = str(source["confidence"]).strip()
            if confidence and canonical_enum_value(
                    confidence, SOURCE_CONFIDENCE_LEVELS, SOURCE_CONFIDENCE_ALIASES) is None:
                errors.append(cite("booking.option_contract", 
                    f"source confidence {confidence!r} is not one of: "
                    + ", ".join(SOURCE_CONFIDENCE_LEVELS)
                    + " (or one of this renderer's own spellings of them: "
                    + ", ".join(sorted(SOURCE_CONFIDENCE_ALIASES))
                    + "). This value is printed next to the source on the page, so it has to be a "
                    "closed enum the renderer can translate -- an arbitrary string cannot be, and "
                    "on a non-English page it ships as English nobody can read. Put any "
                    "qualification ('fare requires recheck') into claim_or_decision_supported."))
    options = plan.get("booking_options") if isinstance(plan.get("booking_options"), dict) else {}
    required = {"flights": "flight", "ground_transport": "ground", "accommodations": "hotel",
                "attraction_tickets": "ticket", "rental_cars": "car"}
    for field, kind in required.items():
        items = options.get(field, [])
        if not isinstance(items, list):
            errors.append(cite("booking.option_contract", f"booking_options.{field} must be a list."))
            continue
        for item in items:
            if not isinstance(item, dict) or not all(item.get(key) for key in ("provider" if kind != "ticket" else "official_or_authorised_provider", "checked_at", "review_url")) or not is_https(item.get("review_url")):
                errors.append(cite("booking.option_contract", f"Every {kind} option needs provider, checked_at, and an HTTPS review_url."))
                continue
            if kind in {"flight", "hotel", "ground"} and not item.get("id"):
                errors.append(cite("booking.option_contract", f"Every {kind} option needs a stable, non-empty id for day assignments and comparison."))
            if item.get("comparison_platform") and not item.get("comparison_checked_at"):
                errors.append(cite("booking.option_contract", f"Every compared {kind} option needs comparison_checked_at."))
            if not is_iso_datestamp(item.get("checked_at")):
                errors.append(cite("booking.option_contract", f"Every {kind} option.checked_at must be an ISO date or date-time."))
            if item.get("comparison_checked_at") and not is_iso_datestamp(item.get("comparison_checked_at")):
                errors.append(cite("booking.option_contract", f"Every compared {kind} option.comparison_checked_at must be an ISO date or date-time."))
            if item.get("direct_review_url") and not is_https(item.get("direct_review_url")):
                errors.append(cite("booking.option_contract", f"Every direct {kind} cross-check URL must be HTTPS."))
            if kind == "ground":
                # Held to the flight standard on purpose. A category with looser evidence rules
                # becomes the place authors put the thing they did not research, and this is the
                # purchase a rail traveller most needs to check: which service, when, what the fare
                # allows, whether it is still sellable, and how they get from the station into town.
                # A chain trip's intercity legs are ONE-WAY, and this list could not say so: it
                # demanded a return date and a return itinerary from every card, so Montreux→Bern
                # →Lucerne had no honest shape at all. The two ways out were both bad -- call two
                # one-way legs a round trip, or drop the cards and leave the traveller no way to
                # buy the largest time-sensitive purchase on a rail trip. Found by building a real
                # three-stop Swiss plan, which is the only way this surfaces.
                #
                # One-way is opt-in and must say why, so it cannot become the lazy default for a
                # return nobody researched, and the return fields must then be ABSENT, not empty.
                one_way = bool(str(item.get("one_way_reason") or "").strip())
                required_ground_fields = (
                    "origin_station", "destination_station", "outbound_date",
                    "outbound_itinerary", "material_conditions",
                    "availability_status", "price_checked_at", "station_transfer_note",
                    "round_trip_search_url", "round_trip_search_provider",
                    "round_trip_search_checked_at", "round_trip_prefilled_fields",
                ) + (() if one_way else ("return_date", "return_itinerary"))
                if one_way and (item.get("return_date") or item.get("return_itinerary")):
                    errors.append(cite("booking.option_contract",
                        "A ground leg that declares one_way_reason must not also carry a "
                        "return_date or return_itinerary -- a card that says it is one-way and "
                        "then names a return service makes two claims, and the page prints both."))
                if not all(item.get(key) for key in required_ground_fields):
                    errors.append(cite("booking.option_contract", 
                        "Every rail/coach/ferry option needs both stations, both dates, concrete "
                        "outbound and return itineraries, fare conditions, a current-price status, "
                        "a station-to-city transfer note, and a verified dated round-trip search URL."))
                elif not is_https(item["round_trip_search_url"]):
                    errors.append(cite("booking.option_contract", "Every ground-transport round-trip search URL must be HTTPS."))
                search_fields = item.get("round_trip_prefilled_fields")
                # Ground is NOT held to the flight field list, and the reason is the operator's
                # own URL scheme rather than a lower standard. SBB's documented deep link takes
                # von / nach / datum / zeit / an / suche / vias and has no passenger parameter at
                # all -- so demanding a prefilled `travellers` asked the mandated operator for a
                # field it cannot carry, and the only ways to satisfy it were to invent a
                # parameter or to declare a field the URL does not contain. Whatever IS declared
                # still has to appear in the URL: check_plan_consistency compares the two.
                wanted = {"origin", "destination", "outbound_date"}
                if not one_way:
                    wanted = wanted | {"return_date"}
                if not has_search_fields(search_fields, wanted):
                    errors.append(cite("booking.option_contract",
                        "Every ground-transport search must prefill origin, destination and the "
                        "outbound date" + ("" if one_way else ", and the return date") + ". "
                        "Travellers is not demanded here: rail operators' timetable deep links "
                        "(SBB's among them) carry no passenger parameter."))
                if not is_iso_datestamp(item.get("round_trip_search_checked_at")):
                    errors.append(cite("booking.option_contract", "ground.round_trip_search_checked_at must be an ISO date or date-time."))
                for leg_name in ("outbound_itinerary",) if one_way else ("outbound_itinerary", "return_itinerary"):
                    errors.extend(itinerary_findings(item.get(leg_name), f"ground.{leg_name}", cite))
                if not is_one_of(item.get("availability_status"), {"available", "limited", "unknown"}):
                    errors.append(cite("booking.option_contract", "ground.availability_status must be available, limited, or unknown."))
                if item.get("price_basis") != "per_person_round_trip":
                    errors.append(cite("booking.option_contract", "ground.price_basis must be per_person_round_trip."))
                if not is_one_of(item.get("price_status"), PRICE_STATUSES):
                    errors.append(cite("booking.option_contract", "ground.price_status must be researched_current, estimate, or user_confirmed."))
                if item.get("fare_low") is None or item.get("fare_high") is None or not item.get("fare_currency"):
                    errors.append(cite("booking.option_contract", "Every ground-transport option needs a checked per-person fare range and currency."))
                elif not is_nonnegative_money_range(item.get("fare_low"), item.get("fare_high")):
                    errors.append(cite("booking.option_contract", "Every ground-transport fare range must be non-negative with low <= high."))
                elif item["fare_low"] == 0 and item["fare_high"] == 0:
                    # Same reasoning as the zero-minute leg: 0/0 was the template's seed value, so
                    # "unfilled" and "free" were indistinguishable to every gate. A ticket that is
                    # genuinely free needs no round-trip search URL, which this branch requires.
                    errors.append(cite("booking.option_contract", "A ground-transport fare of 0-0 is an unfilled field, not a researched fare."))
                if not is_iso_datestamp(item.get("price_checked_at")):
                    errors.append(cite("booking.option_contract", "ground.price_checked_at must be an ISO date or date-time."))
                # The two dates were truthiness-checked only, so "next Friday" and a return three
                # days BEFORE departure both validated and printed straight onto the search button.
                # price_checked_at and round_trip_search_checked_at on the same object are already
                # ISO-checked, so the looseness was an oversight rather than a decision.
                outbound = parse_iso_date(item.get("outbound_date"), "ground.outbound_date", errors)
                # A one-way leg has no return date to parse, and parsing None reported it as a
                # malformed date -- which read as "you wrote it wrong" about a field the card
                # correctly does not have.
                inbound = (None if one_way else
                           parse_iso_date(item.get("return_date"), "ground.return_date", errors))
                if outbound and inbound and inbound < outbound:
                    errors.append(cite("booking.option_contract", "ground.return_date cannot be before ground.outbound_date."))
                # Deliberately NOT copied from the flight branch: a flight's outbound_date must equal
                # trip.start_date, because the flight IS the arrival. A rail leg is often mid-trip --
                # the hop between two cities -- so pinning it to the trip window would reject the
                # multi-city case this category exists to serve. Both dates must still fall inside
                # the trip, which is a weaker and correct claim.
                trip_start = parse_iso_date(trip.get("start_date"), "trip.start_date", [])
                trip_end = parse_iso_date(trip.get("end_date"), "trip.end_date", [])
                for label, value in (("outbound_date", outbound), ("return_date", inbound)):
                    if value and trip_start and trip_end and not trip_start <= value <= trip_end:
                        errors.append(cite("booking.option_contract", 
                            f"ground.{label} {value.isoformat()} falls outside the trip window "
                            f"{trip_start.isoformat()}..{trip_end.isoformat()}."))
            if kind == "flight":
                required_flight_fields = (
                    "origin_airport", "destination_airport", "outbound_date", "return_date",
                    "outbound_itinerary", "return_itinerary", "baggage_assumption", "material_conditions",
                    "availability_status", "price_checked_at", "airport_transfer_note",
                    "round_trip_search_url", "round_trip_search_provider", "round_trip_search_checked_at", "round_trip_prefilled_fields",
                )
                if not all(item.get(key) for key in required_flight_fields):
                    errors.append(cite("booking.option_contract", "Every flight option needs route, dates, concrete outbound/return itineraries, fare conditions, current-price status, airport transfer note, and a verified dated round-trip search URL."))
                elif not is_https(item["round_trip_search_url"]):
                    errors.append(cite("booking.option_contract", "Every flight round-trip search URL must be HTTPS."))
                search_fields = item.get("round_trip_prefilled_fields")
                if not has_search_fields(search_fields, REQUIRED_FLIGHT_SEARCH_FIELDS):
                    errors.append(cite("booking.option_contract", "Every flight round-trip search must prefill origin, destination, outbound date, return date, and travellers."))
                if not is_iso_datestamp(item.get("round_trip_search_checked_at")):
                    errors.append(cite("booking.option_contract", "flight.round_trip_search_checked_at must be an ISO date or date-time."))
                for leg_name in ("outbound_itinerary", "return_itinerary"):
                    errors.extend(itinerary_findings(item.get(leg_name), f"flight.{leg_name}", cite))
                if not is_one_of(item.get("availability_status"), {"available", "limited", "unknown"}):
                    errors.append(cite("booking.option_contract", "flight.availability_status must be available, limited, or unknown."))
                if item.get("price_basis") != "per_person_round_trip":
                    errors.append(cite("booking.option_contract", "flight.price_basis must be per_person_round_trip."))
                if not is_one_of(item.get("price_status"), PRICE_STATUSES):
                    errors.append(cite("booking.option_contract", "flight.price_status must be researched_current, estimate, or user_confirmed."))
                if item.get("fare_low") is None or item.get("fare_high") is None or not item.get("fare_currency"):
                    errors.append(cite("booking.option_contract", "Every flight option needs a checked per-person fare range and currency."))
                elif not is_nonnegative_money_range(item.get("fare_low"), item.get("fare_high")):
                    errors.append(cite("booking.option_contract", "Every flight fare range must be non-negative numbers with low less than or equal to high."))
                if not is_iso_datestamp(item.get("price_checked_at")):
                    errors.append(cite("booking.option_contract", "flight.price_checked_at must be an ISO date or date-time."))
                outbound = parse_iso_date(item.get("outbound_date"), "flight.outbound_date", errors)
                inbound = parse_iso_date(item.get("return_date"), "flight.return_date", errors)
                if outbound and inbound and inbound < outbound:
                    errors.append(cite("booking.option_contract", "flight.return_date cannot be before flight.outbound_date."))
                if outbound and trip_start and outbound != trip_start:
                    errors.append(cite("booking.option_contract", "flight.outbound_date must match trip.start_date; include travel days in the trip window."))
                if inbound and trip_end and inbound != trip_end:
                    errors.append(cite("booking.option_contract", "flight.return_date must match trip.end_date; include travel days in the trip window."))
            if kind == "hotel":
                required_hotel_fields = (
                    "stay_location", "neighborhood", "address_or_location_reference", "check_in", "check_out",
                    "guest_count", "room_count", "room_basis", "nightly_cost_low", "nightly_cost_high",
                    "trip_cost_low", "trip_cost_high", "currency", "price_checked_at", "availability_status",
                    "arrival_access_note", "key_area_access_note", "selection_rationale",
                )
                if not all(item.get(key) is not None and item.get(key) != "" for key in required_hotel_fields):
                    errors.append(cite("booking.option_contract", "Every hotel option needs an exact stay area, access rationale, room and current price details, availability status, and check-in/out dates."))
                if not is_one_of(item.get("availability_status"), {"available", "limited", "unknown"}):
                    errors.append(cite("booking.option_contract", "hotel.availability_status must be available, limited, or unknown."))
                if not item.get("stay_group_id"):
                    errors.append(cite("booking.option_contract", "Every hotel option needs a stay_group_id so comparable options cannot be split by different neighborhood labels."))
                if item.get("price_basis") != "per_room_per_night":
                    errors.append(cite("booking.option_contract", "hotel.price_basis must be per_room_per_night."))
                if not is_one_of(item.get("price_status"), PRICE_STATUSES):
                    errors.append(cite("booking.option_contract", "hotel.price_status must be researched_current, estimate, or user_confirmed."))
                if not is_iso_datestamp(item.get("price_checked_at")):
                    errors.append(cite("booking.option_contract", "hotel.price_checked_at must be an ISO date or date-time."))
                for cost_label, low_key, high_key in (
                    ("nightly", "nightly_cost_low", "nightly_cost_high"),
                    ("trip", "trip_cost_low", "trip_cost_high"),
                ):
                    if not is_nonnegative_money_range(item.get(low_key), item.get(high_key)):
                        errors.append(cite("booking.option_contract", f"hotel {cost_label} price range must be non-negative numbers with low less than or equal to high."))
                searches = item.get("comparison_searches")
                if not isinstance(searches, list) or not searches:
                    errors.append(cite("booking.option_contract", "Every hotel option needs at least one dated comparison-platform search."))
                else:
                    for search in searches:
                        if not isinstance(search, dict) or not all(search.get(key) for key in ("platform", "search_url", "checked_at")) or not is_https(search.get("search_url")):
                            errors.append(cite("booking.option_contract", "Every hotel comparison search needs platform, checked_at, and an HTTPS search URL."))
                            continue
                        if not is_iso_datestamp(search["checked_at"]):
                            errors.append(cite("booking.option_contract", "Every hotel comparison search.checked_at must be an ISO date or date-time."))
                        fields = search.get("prefilled_fields")
                        if not has_search_fields(fields, REQUIRED_STAY_SEARCH_FIELDS):
                            errors.append(cite("booking.option_contract", "Every hotel comparison search must prefill destination, check-in/out, guests, and rooms."))
                check_in = parse_iso_date(item.get("check_in"), "hotel.check_in", errors)
                check_out = parse_iso_date(item.get("check_out"), "hotel.check_out", errors)
                if check_in and check_out and check_out <= check_in:
                    errors.append(cite("booking.option_contract", "hotel.check_out must be after hotel.check_in."))
                for field_name in ("guest_count", "room_count"):
                    if not isinstance(item.get(field_name), int) or isinstance(item.get(field_name), bool) or item[field_name] < 1:
                        errors.append(cite("booking.option_contract", f"hotel.{field_name} must be a positive integer."))
            if kind == "ticket":
                required_ticket_fields = (
                    "id", "day_number", "attraction_name", "timed_entry_or_reservation", "price_low", "price_high",
                    "currency", "ticket_status", "price_basis", "price_status", "price_checked_at", "availability_status",
                )
                if not all(item.get(key) is not None and item.get(key) != "" for key in required_ticket_fields):
                    errors.append(cite("booking.option_contract", "Every attraction-ticket option needs an id, day, attraction/reservation details, per-person price, status, and check time."))
                if item.get("ticket_status") and item.get("ticket_status") not in BOOKING_STATES:
                    errors.append(cite("booking.option_contract", "ticket.ticket_status must be idea, researched, held, or booked."))
                if item.get("price_basis") != "per_person_ticket":
                    errors.append(cite("booking.option_contract", "ticket.price_basis must be per_person_ticket."))
                if not is_one_of(item.get("price_status"), PRICE_STATUSES):
                    errors.append(cite("booking.option_contract", "ticket.price_status must be researched_current, estimate, or user_confirmed."))
                if not is_one_of(item.get("availability_status"), {"available", "limited", "unknown"}):
                    errors.append(cite("booking.option_contract", "ticket.availability_status must be available, limited, or unknown."))
                if not is_nonnegative_money_range(item.get("price_low"), item.get("price_high")):
                    errors.append(cite("booking.option_contract", "ticket price range must be non-negative numbers with low less than or equal to high."))
                if not is_iso_datestamp(item.get("price_checked_at")):
                    errors.append(cite("booking.option_contract", "ticket.price_checked_at must be an ISO date or date-time."))
            if kind == "car":
                required_car_fields = (
                    "id", "pickup_location", "dropoff_location", "pickup_time", "dropoff_time", "vehicle_class",
                    "transmission", "capacity_note", "price_low", "price_high", "currency", "price_basis", "price_status",
                    "price_checked_at", "availability_status", "insurance_excess", "fuel_policy", "mileage_policy",
                    "cross_border_or_restriction_note", "rental_search_prefilled_fields",
                )
                if not all(item.get(key) is not None and item.get(key) != "" for key in required_car_fields):
                    errors.append(cite("booking.option_contract", "Every rental-car option needs exact pickup/dropoff, vehicle/terms, dated per-day price, availability, and search-prefill details."))
                if item.get("price_basis") != "per_vehicle_per_day":
                    errors.append(cite("booking.option_contract", "rental_car.price_basis must be per_vehicle_per_day."))
                if not is_one_of(item.get("price_status"), PRICE_STATUSES):
                    errors.append(cite("booking.option_contract", "rental_car.price_status must be researched_current, estimate, or user_confirmed."))
                if not is_one_of(item.get("availability_status"), {"available", "limited", "unknown"}):
                    errors.append(cite("booking.option_contract", "rental_car.availability_status must be available, limited, or unknown."))
                if not is_nonnegative_money_range(item.get("price_low"), item.get("price_high")):
                    errors.append(cite("booking.option_contract", "rental-car price range must be non-negative numbers with low less than or equal to high."))
                if not is_iso_datestamp(item.get("price_checked_at")):
                    errors.append(cite("booking.option_contract", "rental_car.price_checked_at must be an ISO date or date-time."))
                rental_fields = item.get("rental_search_prefilled_fields")
                if not has_search_fields(rental_fields, REQUIRED_RENTAL_SEARCH_FIELDS):
                    errors.append(cite("booking.option_contract", "Every rental-car search must prefill pickup/dropoff locations and times."))
    required_access_categories = {"accommodation"}
    if options.get("flights"):
        required_access_categories.add("flight")
    if options.get("attraction_tickets"):
        required_access_categories.add("attraction_ticket")
    if options.get("rental_cars"):
        required_access_categories.add("rental_car")
    # Keyed on the card as well as the mobility mode, because every other category is keyed on
    # "is this card here" and this one was not. A car ferry, a motorail or a Eurotunnel shuttle
    # sits inside a self-drive trip, and the mode test alone left that crossing -- often the one
    # sellable-out purchase on the page -- as the only channel with no record of whether the
    # traveller can reach and buy from it.
    if mode == "public-transit" or options.get("ground_transport"):
        required_access_categories.add("rail_or_ground")
    missing_access_categories = required_access_categories - booking_access_categories
    if missing_access_categories:
        errors.append(cite("booking.access_checks", "Missing booking-access checks for: " + ", ".join(sorted(missing_access_categories)) + "."))
    accommodation_items = [item for item in options.get("accommodations", []) if isinstance(item, dict)]
    flight_items = [item for item in options.get("flights", []) if isinstance(item, dict)]
    ground_items = [item for item in options.get("ground_transport", []) if isinstance(item, dict)]
    # One rule set over both categories. SKILL.md and references/booking-html-output.md both
    # promise ground is "held to exactly the flight standard"; leaving the three comparison rules
    # keyed on flight_items made that sentence false, and an uncompared, unexplained single rail
    # option is exactly what the strictness exists to prevent -- as is a pair of "compared" cards
    # pointing at one review_url, which looks like a comparison and is not.
    for items, noun, label in ((flight_items, "flight", "Flight"),
                               (ground_items, "rail/coach/ferry", "Rail/coach/ferry")):
        # "Two comparable candidates" means two candidates FOR THE SAME JOURNEY, and this rule read
        # the whole category. On a multi-city trip that is silently wrong: Beijing->Shanghai and
        # Shanghai->Beijing are two items, so the count passed, the review_urls differed so the
        # uniqueness check passed, and NEITHER leg had ever been compared against anything. The
        # more legs the trip has, the more thoroughly the gate reports a comparison that does not
        # exist. Accommodations solved this years earlier with stay_group_id, for the same reason
        # written one screen down -- comparable options must not be split, or joined, by a label --
        # so legs group the same way rather than by a cleverer derivation: two options for one
        # journey may legitimately use different stations, and grouping on the station pair would
        # split them.
        legs = _leg_groups(items)
        if len(legs) > 1 or any(not str(item.get("leg_group_id") or "").strip() for item in items):
            # Only demanded once the items themselves say they are more than one journey, so a
            # trip with a single compared leg -- every plan in the author's workspace -- needs no
            # new field. The signal is the items' own dates and endpoints.
            if _looks_like_several_legs(items) and len(legs) < 2:
                errors.append(cite("booking.comparison", f"These {noun} options are on different dates or between different points, so they are different journeys rather than alternatives for one. Give each journey its own leg_group_id; without it the comparison rule counts across legs and reports a comparison nobody made."))
        for leg_id, leg_items in legs.items():
            where = f" for leg {leg_id}" if leg_id else ""
            if len(leg_items) == 1 and not leg_items[0].get("single_option_reason"):
                errors.append(cite("booking.comparison", f"Provide at least two comparable {noun} candidates{where}, or record a researched single_option_reason for the only feasible option."))
            review_urls = [item.get("review_url") for item in leg_items]
            if len({dedupe_key(v) for v in review_urls}) != len(review_urls):
                errors.append(cite("booking.comparison", f"{label} candidates{where} must not reuse the same review_url; provide genuinely distinct comparison paths."))
        identifiers = [item.get("id") for item in items]
        # A non-string id is not merely odd: ids are matched by equality against day assignments
        # elsewhere in the plan, so a list or a number is a value that can never match and never
        # says why. Truthiness alone accepted `["ground-1"]`. Ids stay unique across the whole
        # category, not per leg, because that is how days reference them.
        if any(not isinstance(identifier, str) or not identifier.strip() for identifier in identifiers) \
                or len({dedupe_key(v) for v in identifiers}) != len(identifiers):
            errors.append(cite("booking.comparison", f"{label} options must use distinct, non-empty string ids so the comparison is not ambiguous."))
    accommodation_ids = {item.get("id") for item in accommodation_items if item.get("id")}
    if not accommodation_ids:
        errors.append(cite("booking.comparison", "At least one accommodation option with an id is required."))
    if len(accommodation_ids) != len(accommodation_items):
        errors.append(cite("booking.comparison", "Accommodation options must use distinct, non-empty ids so daily stay assignments remain unambiguous."))
    # Every kind, not only the ones days point at: the verification receipt tells booking options
    # apart by id (scripts/verification_sections.py), so two rental cars -- or tickets -- sharing
    # one were a single fingerprint, and an edit to the first escaped every recheck.
    for kind, label in (("attraction_tickets", "Attraction-ticket"), ("rental_cars", "Rental-car")):
        kind_ids = [item.get("id") for item in options.get(kind, []) if isinstance(item, dict)]
        if any(not isinstance(identifier, str) or not identifier.strip() for identifier in kind_ids) \
                or len({dedupe_key(identifier) for identifier in kind_ids}) != len(kind_ids):
            errors.append(cite("booking.option_contract", f"{label} options must use distinct, non-empty string ids; days and the verification receipt tell options apart by id."))
    accommodation_counts: dict[str, int] = {}
    accommodation_windows: dict[str, tuple[date | None, date | None]] = {}
    for item in accommodation_items:
        group = item.get("stay_group_id")
        if group:
            accommodation_counts[group] = accommodation_counts.get(group, 0) + 1
        item_id = item.get("id")
        if item_id:
            accommodation_windows[item_id] = (
                parse_iso_date(item.get("check_in"), "hotel.check_in", []),
                parse_iso_date(item.get("check_out"), "hotel.check_out", []),
            )
    if any(count > 3 for count in accommodation_counts.values()):
        errors.append(cite("booking.comparison", "Provide no more than three accommodation options per stay location."))
    for group, count in accommodation_counts.items():
        if count < 2:
            only_option = next((item for item in accommodation_items if item.get("stay_group_id") == group), {})
            if not only_option.get("single_option_reason"):
                errors.append(cite("booking.comparison", f"Provide two comparable hotel options for stay group {group}, or record a researched single_option_reason (for example, a remote stay or user-selected property)."))
    ticket_ids = {
        item.get("id")
        for item in options.get("attraction_tickets", [])
        if isinstance(item, dict) and item.get("id")
    }
    for ticket in options.get("attraction_tickets", []):
        if isinstance(ticket, dict) and ticket.get("day_number") not in day_dates:
            errors.append(cite("booking.option_contract", "Every attraction-ticket option.day_number must name a real trip day."))
    for day in days:
        if not isinstance(day, dict):
            continue
        accommodation_id = day.get("accommodation_option_id")
        departure_without_overnight = day.get("day_type") == "departure" and not accommodation_id
        if not departure_without_overnight and accommodation_id not in accommodation_ids:
            errors.append(cite("booking.option_contract", f"day {day.get('number', '?')} needs a valid accommodation_option_id."))
        elif accommodation_id in accommodation_ids:
            day_date = day_dates.get(day.get("number"))
            check_in, check_out = accommodation_windows[accommodation_id]
            if day_date and check_in and check_out:
                if day.get("day_type") == "departure":
                    if not check_in < day_date <= check_out:
                        errors.append(cite("booking.option_contract", f"day {day.get('number', '?')} departure accommodation must be the hotel checked out on that date."))
                elif not check_in <= day_date < check_out:
                    errors.append(cite("booking.option_contract", f"day {day.get('number', '?')} is not covered by its assigned overnight accommodation dates."))
        for activity in day.get("activities", []):
            if isinstance(activity, dict) and activity.get("ticket_option_id") and activity["ticket_option_id"] not in ticket_ids:
                errors.append(cite("booking.option_contract", f"day {day.get('number', '?')} references an unknown ticket_option_id."))
    if trip.get("arrival_transport_mode") == "flight" and not options.get("flights"):
        errors.append(cite("booking.option_contract", "A flight-arrival plan needs at least one flight option."))
    # The same rule for the ground modes, and it is the one that makes the category worth having.
    # Adding ground_transport made a train card POSSIBLE; without this it was never REQUIRED, so a
    # rail-arrival plan with three compared hotels and no way to reach, price-check or
    # availability-check the train passed validate_plan, check_plan_consistency and
    # validate_trip_html exactly as before -- the defect the category was built to end, recurring on
    # any run where the author simply did not think of it. `--require-booking-type ground` cannot
    # cover for this: it is opt-in, and the flight rule pointedly does not depend on the operator
    # remembering a flag.
    #
    # "road" is included only for public transit, where it means a coach; on a self-drive trip the
    # road arrival is the rental car, which the next rule already requires.
    if trip.get("arrival_transport_mode") == "rail" and not options.get("ground_transport"):
        errors.append(cite("booking.option_contract", 
            "A rail-arrival plan needs at least one rail/coach/ferry option in "
            "booking_options.ground_transport -- the train is the largest and most time-sensitive "
            "purchase on the page, and without a card the traveller cannot reach, price or "
            "availability-check it."))
    # "road" is only an intercity coach when the trip actually leaves town. On a same-city plan --
    # the repo's own fixture is Chengdu to Chengdu -- road means the taxi or the bus that met the
    # traveller, and demanding a bookable coach card for it would be a gate firing on correct
    # authoring, which is worse than no gate.
    leaves_town = str(trip.get("origin") or "").strip() != str(trip.get("destination") or "").strip()
    if (trip.get("arrival_transport_mode") == "road" and mode != "self-drive" and leaves_town
            and not options.get("ground_transport")):
        errors.append(cite("booking.option_contract", 
            "A road arrival between two places on public transit means an intercity coach, so it "
            "needs at least one rail/coach/ferry option in booking_options.ground_transport."))
    if mode == "self-drive" and not options.get("rental_cars"):
        errors.append(cite("booking.option_contract", "A self-drive plan needs at least one rental-car option."))
    if mode == "public-transit" and options.get("rental_cars"):
        errors.append(cite("booking.option_contract", "A public-transit plan must not include rental-car options."))
    overview = plan.get("transport_overview") if isinstance(plan.get("transport_overview"), dict) else {}
    if not overview.get("overall_route_map_url") or not overview.get("overall_map_checked_at") or not overview.get("overall_map_provider") or not overview.get("overall_map_scope") or not overview.get("map_link_kind"):
        errors.append(cite("map.link_contract", "transport_overview needs a directions URL, map scope/link kind, map check time, and map provider."))
    elif overview.get("overall_map_scope") not in ROUTE_MAP_SCOPES:
        errors.append(cite("map.link_contract", "transport_overview.overall_map_scope must be multi_stop or primary_leg."))
    elif overview.get("map_link_kind") != "directions":
        errors.append(cite("map.link_contract", "transport_overview.map_link_kind must be directions."))
    elif not is_https(overview["overall_route_map_url"]):
        errors.append(cite("map.link_contract", "transport_overview.overall_route_map_url must be HTTPS."))
    elif not is_directions_url(overview["overall_map_provider"], overview["overall_route_map_url"]):
        errors.append(cite("map.link_contract", "transport_overview.overall_route_map_url must be an actual directions URL, not a place/POI page."))
    elif not map_link_allowed(overview["overall_map_provider"], overview["overall_route_map_url"], regional_context):
        errors.append(cite("market.provider_routing", "transport_overview uses Google Maps despite the regional-access rule."))
    elif market == "mainland_china" and not mainland_primary_exception and not is_amap(overview["overall_map_provider"], overview["overall_route_map_url"]):
        errors.append(cite("market.provider_routing", "mainland-China transport overview must use Amap/高德地图."))
    validate_alternative_map_links(overview.get("overall_alternative_map_links"), "transport_overview", regional_context, errors)
    if mode == "public-transit" and overview.get("cost_low") is None and overview.get("cost_high") is None:
        errors.append("A public-transit overview needs a researched fare or range.")
    elif mode == "public-transit" and not is_nonnegative_money_range(overview.get("cost_low"), overview.get("cost_high")):
        errors.append("A public-transit overview cost range must be non-negative numbers with low less than or equal to high.")
    if mode == "self-drive" and (
        overview.get("overall_duration_minutes") is None or overview.get("overall_distance_km") is None
    ):
        errors.append("A self-drive overview needs overall duration and distance.")
    elif mode == "self-drive" and (not is_nonnegative_number(overview.get("overall_duration_minutes")) or not is_nonnegative_number(overview.get("overall_distance_km"))):
        errors.append("A self-drive overview duration and distance must be non-negative numbers.")
    return errors


def render_unlocalized(plan: dict) -> str:
    trip = plan["trip"]
    budget = plan.get("budget", {})
    options = plan.get("booking_options", {})
    sources = plan["sources"]
    accommodations = {item.get("id"): item for item in options.get("accommodations", []) if item.get("id")}
    # Kept as a list, in `attraction_tickets` order, because a day's tickets are joined on two
    # keys, not one: the day card used to read only activities[].ticket_option_id, so a ticket
    # that carried `day_number` and was never referenced by an activity reached the booking
    # panel and vanished from the day. The measured run printed "no ticket required" on all
    # four days of a plan holding three paid tickets -- an affirmative false statement on the
    # page the traveller books from, and the reason the empty-state line below is now gated on
    # the union rather than on one of its two halves.
    ticket_options = [item for item in options.get("attraction_tickets", []) if isinstance(item, dict)]
    # Grouped by type: a single grid put flight cards and hotel cards side by side in one
    # row, inviting a comparison between things that are not comparable.
    groups = []
    for field, kind, heading in (
        ("flights", "flight", "Flight options"),
        # Rail, coach and ferry sit next to flights because they answer the same question -- how
        # the traveller crosses the distance -- and because a rail trip's biggest, most
        # time-sensitive purchase previously had no card at all: the page compared three hotels and
        # offered no way to reach, price or availability-check the train.
        ("ground_transport", "ground", "Rail, coach and ferry options"),
        ("accommodations", "hotel", "Accommodation options"),
        ("attraction_tickets", "ticket", "Ticket options"),
        ("rental_cars", "car", "Rental-car options"),
    ):
        items = [item for item in options.get(field, []) if isinstance(item, dict)]
        if not items:
            continue
        recorded = booking_rules.record_by_option(plan)
        by_group: dict[str, list[dict]] = {}
        for item in items:
            by_group.setdefault(booking_rules.group_key(field, item), []).append(item)
        lead, folded = [], []
        for group, members in by_group.items():
            decided = next((m for m in members if str(m.get("id") or "") in recorded
                            and recorded[str(m["id"])].get("state") in BOOKING_STATE_WORDS), None)
            if decided is None:
                lead.extend(option_card(kind, m) for m in members)
                continue
            lead.append(option_card(kind, decided, recorded[str(decided["id"])]))
            rest = [m for m in members if m is not decided]
            if rest:
                folded.append(
                    f'<details class="not-chosen" data-booking-group="{attr(group)}">'
                    f'<summary class="not-chosen-summary">Alternatives not booked <span class="count">({len(rest)})</span></summary>'
                    f'<div class="grid">{"".join(option_card(kind, m) for m in rest)}</div></details>')
        groups.append(f'<section class="option-group" data-option-group="{attr(kind)}"><h3>{heading}</h3>'
                      f'<div class="grid">{"".join(lead)}</div>{"".join(folded)}</section>')
    cards = groups or ['<p class="meta">No purchase options were requested for this plan.</p>']
    day_cards = []
    # Looked up once at function level: every day card asks which market its own stay is in, and
    # a per-day rebuild of this map would be the same dict rebuilt once per day.
    _regional = plan.get("regional_service_context") if isinstance(plan.get("regional_service_context"), dict) else {}
    _stays_by_id = {str(item.get("id")): item
                    for item in (plan.get("booking_options") or {}).get("accommodations", [])
                    if isinstance(item, dict)}
    transport_dates: set[str] = set()
    for kind in ("flights", "ground_transport"):
        for item in as_list((plan.get("booking_options") or {}).get(kind)):
            if not isinstance(item, dict):
                continue
            for key in ("outbound_date", "return_date"):
                if isinstance(item.get(key), str) and item[key][:10]:
                    transport_dates.add(item[key][:10])
            for leg in ("outbound_itinerary", "return_itinerary"):
                departs = str((item.get(leg) or {}).get("departure_local") or "") if isinstance(item.get(leg), dict) else ""
                if re.match(r"^\d{4}-\d{2}-\d{2}", departs):
                    transport_dates.add(departs[:10])
    for day in plan["days"]:
        route = day["route"]
        stay = accommodations.get(day.get("accommodation_option_id"))
        activities = []
        referenced_ticket_ids = set()
        day_has_ticket_note = False
        for activity in day.get("activities", []):
            # The activity's own admission line: what it costs and where the official ticket is
            # actually sold. The plan collected it and the page printed it nowhere -- the measured
            # run researched "adult EUR 12.00, official ticketing at tickets.koelner-dom.de; book
            # online to skip the Roncalliplatz queue" and the traveller saw a cathedral with no
            # price and no channel. It belongs on the activity rather than only in the ticket
            # panel below, because the panel lists only options with a booking URL, and a note
            # about buying on site or joining a queue has none. A required field that never
            # reaches the page is research the traveller paid for and cannot see.
            ticket_note = activity.get("ticket_note") if isinstance(activity, dict) else None
            note_line = ""
            if ticket_note:
                note_line = f'<p class="meta ticket-note"><strong>Ticket: </strong>{esc(ticket_note)}</p>'
                day_has_ticket_note = True
            activities.append(f'<li><time>{esc(activity.get("time"), "Flexible")}</time><div><strong>{esc(activity.get("name"))}</strong><p>{esc(activity.get("detail"))} {esc(activity.get("meal_or_rest_buffer"), "")}</p>{note_line}</div></li>')
            if isinstance(activity, dict) and activity.get("ticket_option_id"):
                referenced_ticket_ids.add(activity["ticket_option_id"])
        # One pass over the ordered options is the de-duplication: a ticket both referenced by
        # an activity and dated to this day is listed once, where `attraction_tickets` puts it.
        day_tickets = [
            link_for_ticket(ticket)
            for ticket in ticket_options
            if ticket.get("id") in referenced_ticket_ids or ticket.get("day_number") == day.get("number")
        ]
        # The empty state is an affirmative claim, not decoration, so it may only be printed
        # when the day really shows no admission cost anywhere -- which is why the previous
        # release widened its condition from one join key to both. A ticket_note is the third
        # member of that union: an on-site fee or a city card has no bookable option to link,
        # so the day list stays empty while the activity above it now prints a price, and the
        # old wording would have told the traveller no ticket was needed on the same screen.
        # ... and a fourth: the day's train or flight. Its ticket lives in the booking panel, not
        # in attraction_tickets, so a rail day used to print "no ticket required" under a train.
        if str(day.get("date") or "")[:10] in transport_dates:
            empty_tickets = '<p class="transport-ticket-pointer">The transport tickets for this day are under Browse options above.</p>'
        else:
            empty_tickets = '<p>No verified ticket is required for the listed activities.</p>'
        ticket_panel = "".join(day_tickets) or ("" if day_has_ticket_note else empty_tickets)
        # The day's ground mode is the same closed enum as transport_preference.mode and it opens
        # every day's route line, so it is emitted as a marked cell instead of being escaped into
        # the joined sentence. Before this it went through esc() as a bare token and every Chinese
        # itinerary this skill has delivered opened its 路线与交通 section with the English words
        # `public-transit` -- five times on the 拉纳卡 page, which both gates called VALID.
        # It stays OUT of transport_bits deliberately: those are joined and escaped as one string,
        # and escaping the span would print its markup at the reader instead of rendering it.
        # A day that records no mode keeps the exact "Not supplied" the old as_text produced, and
        # a day whose mode is free text keeps that text -- enum_cell marks it either way, which is
        # what lets the validator say which of the two it is looking at.
        mode = route.get("mode")
        mode_cell = (enum_cell("route-mode", "route-mode", mode, "")
                     if isinstance(mode, str) and mode.strip() else esc(None))
        # A driving day's length is the number the day is planned around; validate_plan requires it
        # on every self-drive route and the page never printed it.
        drive_km = route.get("distance_km")
        drive_bit = (f"{float(drive_km):g} km" if mode == "self-drive"
                     and isinstance(drive_km, (int, float)) and not isinstance(drive_km, bool)
                     and drive_km > 0 else "")
        transport_bits = [minutes(route.get("duration_minutes")), drive_bit, money(route.get("cost_low"), route.get("cost_high"), route.get("currency", trip["currency"])), told(route.get("fare_basis_or_fuel_toll_parking_note"))]
        transport_line = " · ".join(bit for bit in transport_bits if bit)
        transport_html = mode_cell + (f" · {markup(transport_line)}" if transport_line else "")
        segment_links = route_segment_links(route, trip["currency"])
        dining = dining_cards(day.get("dining"), day.get("date"))
        route_scope = route.get("route_map_scope")
        route_map_label = "Open full-day route" if route_scope == "multi_stop" else "Open route overview — see segments below"
        # The whole-day walking load and the bad-weather/closure fallback are required by
        # the plan contract; leaving them unrendered collected the research and then hid it
        # from the person who has to walk the route.
        walking_line = (
            f'<p class="meta"><strong>Walking across the day: </strong>{esc(route.get("walking_burden"))}</p>'
            if route.get("walking_burden")
            else ""
        )
        fallback_line = (
            f'<p class="meta route-fallback"><strong>Fallback: </strong>{esc(route.get("fallback_plan"))}</p>'
            if route.get("fallback_plan")
            else ""
        )
        # Two figures per day, drawn from numbers the plan already carries. The stop list shows
        # the order; only a map shows the shape, and only an axis shows whether the afternoon is
        # empty. Both return "" when their data is missing, so a thin day loses a figure rather
        # than gaining an invented one.
        day_map_caption = "Relative positions, in visit order. Use the map button to navigate."
        # The figure's legend names the stops; they are the author's, fenced like every other name.
        # day_map reads stops by position only, so the fenced copy changes nothing it computes.
        fenced_route = {**route, "stops_in_order": [
            shield(stop) if isinstance(stop, str) else stop
            for stop in (route.get("stops_in_order") if isinstance(route.get("stops_in_order"), list) else [])]}
        day_map_figure = plan_visuals.day_map(fenced_route, day_map_caption, day_map_caption,
                                              span_label="straight-line span")
        timeline_entries = [("act", activity.get("time"), shield(as_text(activity.get("name"), "")))
                            for activity in day.get("activities") or []
                            if isinstance(activity, dict)]
        timeline_entries += [("meal", card.get("time") or card.get("time_window"),
                              shield(as_text(card.get("venue_name"), "")))
                             for card in day.get("dining") or [] if isinstance(card, dict)]
        day_shape_caption = "Fixed points across the day"
        day_timeline_figure = plan_visuals.day_timeline(
            timeline_entries, day_shape_caption, day_shape_caption)
        stay_line = "Checkout / no overnight stay" if day.get("day_type") == "departure" else "Arranged independently"
        if stay:
            stay_line = (f"{printed(stay.get('property_name'), 'Not supplied')} · "
                         f"{printed(stay.get('stay_location'), 'Not supplied')} · "
                         f"{printed(stay.get('room_basis'), 'Not supplied')}")
        # Stamped per day so the page gate can hold a mainland-China day to Amap without holding
        # a Hong Kong day to it as well. Derived from the day's own stay, never authored twice.
        day_market = day_service_market(day, _stays_by_id, _regional.get("destination_service_market"))
        day_cards.append(f'''<article class="day-card" id="day-{attr(day["number"])}" data-day="{attr(day["number"])}" data-service-market="{attr(day_market)}"><div class="day-top"><div><p class="eyebrow">Day {esc(day.get("number"))} · {esc(day.get("date"))}</p><h2>{esc(day.get("title"))}</h2><p>{esc(day.get("focus"))}</p></div><div class="day-number" aria-label="Day {attr(day["number"])}">{esc(day.get("number"))}</div></div><section class="day-accommodation"><h3>Stay</h3><p><strong>{markup(stay_line)}</strong></p></section><section class="day-activities"><h3>Plan</h3>{day_timeline_figure}<ol class="timeline">{"".join(activities) or '<li><time>Flexible</time><div><strong>Free time</strong></div></li>'}</ol></section><section class="day-dining"><h3>Dining suggestions</h3>{dining}</section><section class="day-route"><h3>Route and mobility</h3><p>{transport_html}</p><p class="meta">{esc(route.get("route_logic"))}</p><figure class="route-map">{day_map_figure}{route_diagram(route.get("stops_in_order", []))}<figcaption>Schematic — not for navigation. Stops are shown in visit order; use the live map for directions.</figcaption></figure><a class="map-link" data-map-scope="{attr(route_scope)}" data-verified-at="{attr(route["map_checked_at"])}" href="{attr(route["verified_map_url"])}" target="_blank" rel="noopener noreferrer">{route_map_label}</a><h4>Route by segment</h4>{segment_links}{walking_line}{fallback_line}<p class="meta">{esc(route.get("service_or_driving_caveat"), "Recheck operating conditions before departure.")}</p></section><section class="day-bookings"><h3>Tickets and recheck</h3>{ticket_panel}<p class="warning">{esc(day.get("contingency"), "Keep a flexible alternative for disruptions.")}</p></section></article>''')
    overview = plan["transport_overview"]
    source_rows = "".join(f'<li class="source-item" data-source-type="{attr(source["source_type"])}" data-accessed-at="{attr(source["accessed_at"])}" data-source-url="{attr(source["url"])}"><a class="source-link" href="{attr(source["url"])}" target="_blank" rel="noopener noreferrer">{esc(source["name"])}</a> — {esc(source.get("claim_or_decision_supported"), "Plan evidence")} · {enum_cell("source-confidence", "source-confidence", source_confidence_token(source.get("confidence")), SOURCE_CONFIDENCE_DEFAULT)}</li>' for source in sources)
    total = money(budget.get("estimated_per_person_low"), budget.get("estimated_per_person_high"), trip["currency"])
    # The traveller's own stated ceiling belongs next to the number it constrains. It reached
    # check_plan_consistency and stopped there, so a page could show a per-person total well
    # over the cap the traveller gave at intake and read as though nothing were wrong -- the
    # one figure that makes the total judgeable was the one figure the page withheld.
    cap = budget.get("cap_per_person")
    cap_fact = (
        f'<div class="fact budget-cap" data-budget-cap="{attr(cap)}">'
        f'<strong>{markup(money(cap, cap, trip["currency"]))}</strong><span>Cap per person</span></div>'
        if cap is not None
        else ""
    )
    # How to read the headline figure -- "per person across two adults and two children; the party
    # total is four times this range" -- is the one sentence the author wrote for this section, and
    # it was in the contract and printed nowhere (audit 2026-10-09).
    budget_note = (f'<p class="meta budget-note">{esc(budget.get("note"))}</p>'
                   if as_text(budget.get("note"), "") else "")
    budget_breakdown = budget_breakdown_cards(budget.get("breakdown"), trip["currency"])
    # Two whole-trip figures. The breakdown table is exact and hard to read at a glance; the
    # walking numbers are already computed and already checked, and the one thing nobody could do
    # without adding up five day cards by hand was see which day is the heavy one.
    budget_rows = []
    for row in as_list(budget.get("breakdown")):
        if not isinstance(row, dict):
            continue
        low, high = row.get("per_person_low"), row.get("per_person_high")
        values = [v for v in (low, high) if isinstance(v, (int, float)) and not isinstance(v, bool)]
        if values:
            budget_rows.append((as_text(row.get("category")), sum(values) / len(values)))
    budget_caption = "Share of the per-person total, and how much of the cap it uses"
    budget_figure = plan_visuals.budget_bar(
        budget_rows, sum(value for _, value in budget_rows),
        cap if isinstance(cap, (int, float)) else None, budget_caption, budget_caption)
    walking_rows = []
    for day in as_list(plan.get("days")):
        if not isinstance(day, dict):
            continue
        route_block = day.get("route") if isinstance(day.get("route"), dict) else {}
        legs = sum(as_number(segment.get("walking_minutes"))
                   for segment in as_list(route_block.get("segments")) if isinstance(segment, dict))
        on_foot = sum(as_number(activity.get("on_foot_minutes"))
                      for activity in as_list(day.get("activities")) if isinstance(activity, dict))
        walking_rows.append((f"Day {as_text(day.get('number'))}", legs + on_foot))
    # No cap line, and that is a correction rather than an omission. The first version drew
    # traveler_constraints.max_continuous_walking_minutes across these bars, but that field is a
    # limit on a SINGLE unbroken stretch while the bars are a whole-day total. Comparing them
    # marked all five days of a real plan as over the limit when not one leg broke it -- a figure
    # that manufactures an alarm is worse than no figure, and it would have been read as the plan
    # violating a stated accessibility need. The per-stretch rule is enforced by
    # check_walking_budget, which compares like with like.
    walk_cap = (trip.get("traveler_constraints") or {}).get("max_continuous_walking_minutes")
    longest_leg = max(
        [as_number(segment.get("walking_minutes"))
         for day in as_list(plan.get("days")) if isinstance(day, dict)
         for segment in as_list((day.get("route") or {}).get("segments"))
         if isinstance(segment, dict)] or [0.0])
    walking_caption = "Minutes on foot per day: connecting legs plus time on foot at each stop"
    if isinstance(walk_cap, (int, float)) and walk_cap:
        walking_caption += (f" · Longest single walk: {longest_leg:.0f} / {walk_cap:.0f} min")
    walking_figure = plan_visuals.walking_bars(
        walking_rows, None, walking_caption, walking_caption, "")
    # The trip's spine, for a plan that sleeps in more than one place. Everything here is derived
    # from the stay groups the plan already carries, so a multi-stop trip costs the author nothing
    # extra to express -- what was missing was only that the page never showed it. The header line
    # reads "origin -> destination" and a single `trip.destination` string cannot say that four of
    # the nights are somewhere else, so a reader had to infer the shape of the trip from four day
    # cards. Rendered only when there is a sequence: a one-item spine is furniture.
    # The one thing that carries this page off the laptop. Everything else here is about the plan
    # being TRUE; nothing was about it being WHERE THE TRAVELLER IS -- a 331 KB local file that a
    # traveller cannot open standing in Lucerne. A calendar solves it with no server and no account
    # of ours: the file lands in their own calendar and their phone syncs it. Embedded as a data:
    # URI rather than linked, so the page stays self-contained and works with no signal, which is
    # exactly when it is read. It also carries the two things a page cannot -- a time to be
    # somewhere, and a reminder that fires.
    try:
        _ics_body, _ics_counts, _ics_summary = build_calendar(plan)
        _ics_b64 = base64.b64encode(_ics_body.encode("utf-8")).decode("ascii")
        _ics_name = re.sub(r"[^\w.-]+", "-", str(trip.get("title") or "trip"))[:60] or "trip"
        _undecided = len(_ics_summary["undecided"])
        _extra = ((f'<span class="calendar-undecided"><span class="count">{_undecided}</span> '
                   f'<span class="calendar-undecided-text">{CALENDAR_UNDECIDED}</span></span>') if _undecided else "")
        _extra += f'<span class="calendar-floating">{CALENDAR_FLOATING}</span>' if _ics_summary["floating"] else ""
        calendar_button = (
            f'<p class="calendar-offer"><a class="booking-link" download="{attr(_ics_name)}.ics" '
            f'href="data:text/calendar;charset=utf-8;base64,{_ics_b64}">Add this trip to your '
            f'calendar</a> <span class="meta">{CALENDAR_NOTE}{_extra}</span></p>')
    except Exception as exc:  # noqa: BLE001 - reported, never swallowed
        # This started life as a bare `except` that set the button to "" -- and it fired
        # immediately, on a missing `import base64`, producing a page that looked complete and
        # carried no calendar at all. Written while auditing this very failure mode elsewhere in
        # the skill. A page that was meant to carry a calendar and does not has to say so: the
        # traveller cannot see the absence of a button they have never seen.
        calendar_button = ""
        print(f"note: no calendar was embedded in this page ({type(exc).__name__}: {exc}). The "
              f"page is otherwise complete, but nothing on it will reach the traveller's phone.",
              file=sys.stderr)

    spine = stay_sequence(plan)
    stay_spine = ""
    if spine:
        legs = []
        for index, stop in enumerate(spine):
            legs.append(
                f'<li class="spine-stop"><strong>{esc(stop["label"])}</strong>'
                f'<span class="meta">{esc(stop["nights"])} night(s) · '
                f'{esc(stop["check_in"].isoformat())} → {esc(stop["check_out"].isoformat())}</span></li>')
            if index < len(spine) - 1:
                legs.append('<li class="spine-move" aria-hidden="false">Move day</li>')
        stay_spine = (
            f'<section id="trip-spine" class="panel" data-stay-groups="{attr(len(spine))}">'
            f'<h2>Where you sleep</h2><ol class="spine">{"".join(legs)}</ol>'
            f'<p class="meta">Each move is a day with a change of accommodation; '
            f'the day cards below say which.</p></section>')

    hero_photo = imagery_figure((plan.get("imagery") or {}).get("hero"), trip["destination"])
    if hero_photo:
        hero_photo = f'<section class="hero-photo">{hero_photo}</section>'
    recheck = "<br>".join(esc(value) for value in as_list(plan.get("recheck_before_purchase")) if value) or "Recheck price, availability, entry requirements, and operating conditions before purchase."
    anchors = destination_anchor_cards(plan.get("destination_experience_anchors"), plan.get("imagery"))
    overview_scope = overview.get("overall_map_scope")
    # "transport overview" promised a trip-wide route and opened one leg -- the airport hop the
    # traveller already has on day 1. Name the leg it actually opens; the daily segment
    # buttons are the navigation, and the notes below carry what is genuinely trip-wide.
    # The header carries only figures whose scope is unambiguous. A public-transit trip gets the
    # mode and the trip-wide fare: its duration and distance are per-leg facts that live on the
    # day cards, and printing one leg's numbers beside a whole-trip fare read as one thing while
    # describing two -- a delivered page said "28 minutes · 12.0 km · €13.60–19.10" where the
    # first two were the airport hop. A self-drive trip is the opposite: the whole-trip driving
    # total is exactly what the traveller needs for fuel and fatigue, and validate_plan requires
    # it, so it is shown -- a required field that is never displayed is the defect this file
    # warns about elsewhere.
    _ov_parts = [as_text(plan["transport_preference"]["mode"])]
    if plan["transport_preference"]["mode"] == "self-drive":
        _ov_parts.append(minutes(overview.get("overall_duration_minutes")))
        if overview.get("overall_distance_km") is not None:
            _ov_parts.append(as_text(overview.get("overall_distance_km"), "") + " km")
    _ov_parts.append(money(overview.get("cost_low"), overview.get("cost_high"), trip["currency"]))
    overview_headline = " · ".join(part for part in _ov_parts if part)

    overview_map_label = overview_link_labels(plan, "")[0]
    # A multi-day plan is tens of thousands of pixels tall. Without in-page jumps the
    # traveller can only reach day 4 by scrolling past days 1-3 every time they look.
    nav_days = "".join(
        f'<a class="page-nav-link day-nav-link" href="#day-{attr(day["number"])}">'
        f'<span class="day-nav-day">Day {esc(day.get("number"))}</span>'
        f'<span class="day-nav-date">{esc(day.get("date"))}</span></a>'
        for day in plan["days"]
    )
    page_nav = (
        '<nav id="page-nav" class="page-nav" aria-label="On this page">'
        '<a class="page-nav-link" href="#budget-breakdown">Budget</a>'
        '<a class="page-nav-link" href="#booking-panel">Options</a>'
        f'{nav_days}'
        '<a class="page-nav-link" href="#transport-overview">Transport</a>'
        '<a class="page-nav-link" href="#source-register">Sources</a>'
        "</nav>"
    )
    # Categories the plan admits it could not price must be visible, or the per-person
    # total silently reads as if it covered everything.
    unpriced_items = "".join(
        f'<li class="unpriced-category">{vocab(category)}</li>'
        for category in as_list(budget.get("unverified_categories"))
        if category
    )
    unpriced = (
        f'<div class="fact unpriced"><ul class="unpriced-list">{unpriced_items}</ul>'
        "<span>Unpriced categories</span></div>"
        if unpriced_items
        else ""
    )
    assumption_rows = "".join(f"<li>{esc(value)}</li>" for value in as_list(plan.get("assumptions")) if value)
    # Open by default, like the sources list above it. A closed <details> prints as a heading
    # with nothing under it, and in print it prints as a heading with nothing under it
    # permanently -- so the assumptions the numbers rest on, and the recheck list further
    # down, read as empty sections rather than as the safety content they are.
    assumptions_block = (
        f'<details class="plan-assumptions" open><summary>Planning assumptions</summary><ul>{assumption_rows}</ul></details>'
        if assumption_rows
        else ""
    )
    entry = plan.get("entry_context") if isinstance(plan.get("entry_context"), dict) else {}
    # Collected and not shown is the same defect as never collected -- the rule this skill already
    # applies to dining ratings, and the reason a canary run once found avoid_list and the scenery
    # subtypes reaching the plan JSON and the page not once.
    def _essential_row(key: str, heading: str) -> str:
        item = (plan.get("arrival_essentials") or {}).get(key)
        if not isinstance(item, dict):
            return ""
        status = str(item.get("status") or "")
        if status == "not_applicable":
            body = esc(item.get("not_applicable_reason"))
        else:
            extra = [esc(item.get(f)) for f in
                     ("cards_accepted", "cash_customary", "atm_or_fx_note", "sim_or_esim",
                      "roaming_note", "plug_types", "voltage", "local_emergency_number",
                      "consulate_or_embassy", "consulate_contact",
                      "cover_stated_by_traveller", "destination_requirement")
                     if item.get(f)]
            body = esc(item.get("summary")) + (
                "<br><span class=\"meta\">" + " · ".join(extra) + "</span>" if extra else "")
        source = (f'<br><a class="essential-source-link" href="{attr(item.get("source_url"))}" '
                  f'target="_blank" rel="noopener noreferrer">Source</a> '
                  f'<span class="meta">{stamp(item.get("checked_at"))}</span>'
                  if item.get("source_url") else "")
        return (f'<div class="fact" data-essential="{attr(key)}" '
                f'data-essential-status="{attr(status)}"><strong>{heading}</strong>'
                f'{body}{source}</div>')

    _essential_rows = "".join(_essential_row(key, heading) for key, heading in (
        ("payment", "Paying"), ("connectivity", "Getting online"),
        ("emergency", "If something goes wrong"), ("health_and_insurance", "Health and insurance")))
    essentials_panel = (
        f'<section id="arrival-essentials" class="panel"><h2>Your first hour on the ground</h2>'
        f'<div class="grid">{_essential_rows}</div></section>' if _essential_rows else "")

    # One row per jurisdiction the trip enters. check_entry_covers_every_jurisdiction has required
    # these records since the multi-country work, and nothing printed them: a Thailand-Vietnam-
    # Cambodia trip carried three researched answers and the page showed the flat one. The markup
    # repeats the flat answer's own shape -- the entry-status span, "Basis:", "View source" -- so
    # the localisation already written for the flat answer covers these rows too.
    jurisdiction_rows = "".join(
        f'<li class="entry-jurisdiction" data-entry-jurisdiction="{attr(record.get("jurisdiction"))}">'
        f'<strong>{esc(record.get("jurisdiction"))}</strong> · '
        f'<strong class="entry-status">{attr(record.get("status"))}</strong> — {esc(record.get("summary"))}'
        f'<br><span class="meta"><strong>Basis: </strong>{esc(record.get("traveler_basis"))} · '
        f'<a class="entry-source-link" href="{attr(record.get("source_url"))}" target="_blank" '
        f'rel="noopener noreferrer">View source</a> · {stamp(record.get("checked_at"))}</span></li>'
        for record in as_list(entry.get("per_jurisdiction"))
        if isinstance(record, dict) and str(record.get("jurisdiction") or "").strip())
    entry_panel = (
        f'<section id="entry-context" class="panel"><h2>Entry eligibility</h2>'
        f'<p><strong class="entry-status">{attr(entry.get("status"))}</strong> — {esc(entry.get("summary"))}</p>'
        f'<p class="meta"><strong>Basis: </strong>{esc(entry.get("traveler_basis"))}</p>'
        f'<p class="meta"><a class="entry-source-link" href="{attr(entry.get("source_url"))}" target="_blank" rel="noopener noreferrer">View source</a> · {stamp(entry.get("checked_at"))}</p>'
        + (f'<ul class="entry-jurisdictions">{jurisdiction_rows}</ul>' if jurisdiction_rows else "")
        + "</section>"
        if entry
        else ""
    )
    # A plan saved with --unverified skipped the five-domain pass. Recording that in a JSON
    # field only tells whoever opens the JSON; the person who reads the page and books from it
    # has to see it too, so the gap stays visible where the decision actually gets made.
    unverified_banner = (
        '<section id="verification-notice" class="panel"><p class="warning">'
        '<strong>Not fact-checked</strong> — No verification pass is recorded for this plan. '
        'Its fares, opening hours, entry rules, and availability have not been checked against '
        'operators or official sources. Treat every figure as an estimate and verify before booking.'
        "</p></section>"
        # Show the banner unless the plan says, in as many words, that it WAS verified. The test
        # used to be `== "unverified"`, which made the safe state the one nobody writes: the
        # skeleton emits `None`, a plan that never reached the verification stage keeps `None`, and
        # replan_trip.py deliberately resets to `None` -- so the default of every plan in the repo
        # rendered as fully fact-checked. A page whose status nobody set is a page nobody checked,
        # and it is the traveller standing at an airline counter who pays for the difference.
        if plan.get("verification_status") != "verified"
        else ""
    )
    # The traveller's own hard constraints, on the page they carry. The block was validated here
    # and rendered nowhere: a severe triple allergy's entire mechanical effect was "run four more
    # verification agents", and `allergy_card_text` -- the sentence written to hand to restaurant
    # staff -- lived in the JSON only. Whether the allergy appeared at all depended on the author
    # separately retyping it into dining prose. SKILL.md's own rule is that a required field never
    # displayed is research the traveller paid for and cannot see; this was the sharpest case of it
    # in the file, because the field exists to be read out loud at a table.
    constraints = trip.get("traveler_constraints") if isinstance(trip.get("traveler_constraints"), dict) else {}
    constraint_rows = []
    severity = str(constraints.get("allergy_severity") or "").strip()
    if severity and severity != "none":
        # Emitted through enum_cell for the same reason as the source confidence: ALLERGY_SEVERITIES
        # is a closed enum that validate_plan already enforces, and it was printed here as a bare
        # `{esc(severity)}` inside a pill -- so a Chinese page told a Chinese reader that their
        # allergy was "severe", in English, in the one panel written to be read out loud at a
        # restaurant table. Nothing caught it: RENDERER_ENGLISH_MARKUP's pill pattern lists the
        # five booking types and had never heard of the severities, and no delivered plan in the
        # workspace happens to set the field, so no artifact ever showed the defect either. That
        # combination -- a closed enum, rendered visibly, with no label key anywhere -- is exactly
        # what the structural gate in validate_trip_html.py exists to find without being told.
        constraint_rows.append(
            '<p><strong>Allergy severity: </strong>'
            + enum_cell("pill allergy-severity", "allergy-severity", severity, severity)
            + '</p>')
    for field, label in (("dietary_or_religious_needs", "Dietary needs"),
                         ("mobility_notes", "Mobility")):
        values = [v for v in constraints.get(field, []) if isinstance(v, str) and v.strip()]
        if values:
            items = "".join(f"<li>{esc(v)}</li>" for v in values)
            constraint_rows.append(f'<p><strong>{label}: </strong></p><ul>{items}</ul>')
    cap = constraints.get("max_continuous_walking_minutes")
    if isinstance(cap, int) and not isinstance(cap, bool) and cap > 0:
        constraint_rows.append(
            f'<p><strong>Maximum continuous walking: </strong>{cap} min</p>')
    card = constraints.get("allergy_card_text")
    if isinstance(card, str) and card.strip():
        constraint_rows.append(
            '<p><strong>Allergy card — show this to staff: </strong></p>'
            f'<blockquote class="allergy-card">{esc(card)}</blockquote>')
    # What the traveller changed after the form, and why. check_plan_consistency lets a plan
    # disagree with its intake only when the change is recorded in trip.intake_changes -- and a
    # change recorded in the JSON and never shown would be the plan quietly overruling what the
    # traveller typed, which is the defect the cross-check exists to stop.
    changes = [c for c in as_list(trip.get("intake_changes"))
               if isinstance(c, dict) and c.get("field") in INTAKE_CHANGE_LABELS
               and isinstance(c.get("reason"), str) and c["reason"].strip()]
    if changes:
        rows = "".join(
            f'<li class="intake-change" data-intake-change="{attr(c.get("field"))}"><strong>'
            f'{INTAKE_CHANGE_LABELS[c["field"]]}: </strong>'
            f'{esc(c.get("intake_value"), "—")} → {esc(c.get("plan_value"), "—")} — '
            f'{esc(c.get("reason"))}</li>'
            for c in changes)
        constraint_rows.append('<p><strong>Changed since your form: </strong></p>'
                               f'<ul class="intake-changes">{rows}</ul>')
    constraints_panel = (
        '<section id="traveller-constraints" class="panel"><h2>Your constraints</h2>'
        + "".join(constraint_rows) + "</section>"
        if constraint_rows else ""
    )

    # The other half of the same intake form. check_plan_consistency requires every avoid_list
    # entry to carry an avoid_list_handling entry saying what keeps it out, and requires anchors to
    # name the must-haves they answer -- and then the page printed neither the avoid list nor how
    # each item was honoured nor the scenery/culture subtypes the traveller picked. Measured with
    # canary strings through the whole save path: all three were in the JSON and none of them
    # reached the HTML. That is the defect this skill names elsewhere in its own words -- a rating
    # stored and never shown is the same defect as a rating never gathered -- and it lands on the
    # half of the intake that says why the traveller is going at all. The must-haves already reach
    # the page through each anchor's satisfies_preference, so they are not repeated here.
    preferences = trip.get("traveler_preferences") if isinstance(trip.get("traveler_preferences"), dict) else {}
    preference_rows = []
    direction = [v for field in ("natural_subtypes", "human_cultural_subtypes")
                 for v in as_list(preferences.get(field)) if isinstance(v, str) and v.strip()]
    if direction:
        items = "".join(f"<li>{esc(v)}</li>" for v in direction)
        preference_rows.append(f'<p><strong>Experience direction: </strong></p><ul>{items}</ul>')
    handling = {str(entry.get("item") or "").strip(): str(entry.get("how_avoided") or "").strip()
                for entry in as_list(preferences.get("avoid_list_handling"))
                if isinstance(entry, dict)}
    avoid_items = []
    for item in as_list(preferences.get("avoid_list")):
        if not isinstance(item, str) or not item.strip():
            continue
        how = handling.get(item.strip())
        # An unhandled entry is printed bare rather than dropped. check_plan_consistency already
        # refuses to save that plan, so this only ever shows in a draft render -- and a silent
        # omission there would hide exactly what the author still has to answer.
        avoid_items.append(f"<li>{esc(item)}{f' — {esc(how)}' if how else ''}</li>")
    if avoid_items:
        preference_rows.append(
            f'<p><strong>Asked to avoid: </strong></p><ul>{"".join(avoid_items)}</ul>')
    preferences_panel = (
        '<section id="traveller-preferences" class="panel"><h2>What you asked for</h2>'
        + "".join(preference_rows) + "</section>"
        if preference_rows else ""
    )

    # Every gate in this skill is a script, and a script only runs when the agent calls it -- a
    # hand-written page bypasses all of them and looks exactly like a saved one. Nothing in the
    # scripts can fix that; the enforcement point is upstream of them. What the page CAN do is
    # carry the evidence, so a reader can tell the two apart. save_trip_deliverables.py already
    # stamped gates_passed into the plan JSON and it stopped there -- the same gap this repo
    # closed for the unverified banner, whose lesson was that a flag stored only in JSON never
    # reaches the person holding the itinerary at an airline counter.
    #
    # Deliberately says nothing when the stamp is absent: a draft render and a hand-made page both
    # lack it, and a warning would not survive a forger who simply omits it either. Presence is
    # the signal. The caveat is not decoration -- 22 structural checks say the plan agrees with
    # itself, and a reader who reads that as "fact-checked" has been misled by the reassurance.
    # Not named `stamp`: that is the module-level date formatter this same template calls a few
    # lines down, and shadowing it made every render raise "'dict' object is not callable".
    gate_stamp = plan.get("gates_passed") if isinstance(plan.get("gates_passed"), dict) else {}
    checks = gate_stamp.get("checks")
    gates_line = ""
    if isinstance(checks, int) and not isinstance(checks, bool) and checks > 0:
        gates_line = (
            f'<p class="meta" data-gates-checks="{attr(checks)}">'
            f'<strong>Structure checks passed: </strong>{esc(checks)}. '
            f'They prove the plan agrees with itself, never that its facts are true.</p>')
    # Which parts were rechecked after the main verification, and when. A verified save records
    # them in its receipt (scripts/verification_sections.py); printing them is what tells the
    # traveller that a changed dinner was checked again rather than carried under a verification
    # that never saw it.
    # Only on a verified page: an --unverified save keeps the receipt, for the next verified save to
    # compare against, and a page that says no verification is recorded cannot also say which
    # parts were re-checked after it.
    receipt = plan.get("verification_receipt") if isinstance(plan.get("verification_receipt"), dict) else {}
    rechecked = receipt.get("rechecked") if isinstance(receipt.get("rechecked"), dict) else {}
    if plan.get("verification_status") != "verified":
        rechecked = {}
    # Grouped by the date of the recheck and read in the plan's own order -- days, then bookings,
    # then the rest -- each part named once. A party change rechecks every day and card at once,
    # and the part-by-part list printed one date sixteen times, called two different blocks "Other
    # trip details", and put the hotels before the days.
    booking = plan.get("booking_options") if isinstance(plan.get("booking_options"), dict) else {}
    kinds = list(booking)

    def recheck_order(section: str) -> tuple:
        if section.startswith("days["):
            return (0, section)
        if section.startswith("booking_options.") and section.endswith("]") and "[" in section:
            kind, _, option_id = section[len("booking_options."):-1].partition("[")
            items = booking.get(kind) if isinstance(booking.get(kind), list) else []
            ids = [str(item.get("id")) for item in items if isinstance(item, dict)]
            return (1, kinds.index(kind) if kind in kinds else len(kinds),
                    ids.index(option_id) if option_id in ids else len(ids))
        return (2, section)

    # A group is one calendar day (two rechecks at 10:00 and 16:30 are one day's work), and the
    # groups read oldest first.
    recheck_groups: dict[str, list[str]] = {}
    for section in sorted((str(s) for s in rechecked), key=recheck_order):
        when = str(rechecked[section] or "")
        day = when[:10] if re.match(r"^\d{4}-\d{2}-\d{2}", when) else when
        names = recheck_groups.setdefault(day, [])
        if (label := recheck_part_label(plan, section)) not in names:
            names.append(label)
    trip_language = str((plan.get("trip") or {}).get("language") or "").casefold()
    chinese = trip_language.startswith("zh") or "chinese" in trip_language or "中文" in trip_language
    separator, group_separator = ("、", "；") if chinese else (", ", "; ")
    rechecked_line = (
        '<p class="meta rechecked-sections"><strong>Re-checked after the main verification: </strong>'
        + group_separator.join(f'<span class="meta">{stamp(day)}</span> — ' + separator.join(names)
                               for day, names in sorted(recheck_groups.items())) + "</p>"
    ) if recheck_groups else ""
    regional = plan.get("regional_service_context") if isinstance(plan.get("regional_service_context"), dict) else {}
    platform_note = (
        # selection_basis is REQUIRED by validate_plan and was printed nowhere, so the page said
        # which map and booking providers were used and never why those suit this destination --
        # the whole point of routing by market rather than by brand habit. It goes here, beside the
        # platform note it explains.
        (f'<p class="meta">Why these providers: {esc(regional.get("selection_basis"))}</p>'
         if regional.get("selection_basis") else "")
        + (f'<p class="meta">Platform selection: {esc(regional.get("booking_platform_selection_note"))}</p>'
           if regional.get("booking_platform_selection_note") else "")
    )
    booking_index = booking_rules.option_index(plan)
    booking_live = [r for r in booking_rules.records(plan) if str(r.get("option_id") or "") in booking_index]
    panel_state = ("booked" if any(r.get("state") == "booked" for r in booking_live)
                   else "chosen" if booking_live else "none")
    booking_heading = ("<h2>Your bookings and options</h2>" if panel_state == "booked"
                       else "<h2>Browse options — no purchase made</h2>")
    booking_facts = ""
    if booking_live:
        paid: dict[str, float] = {}
        for record in booking_live:
            if record.get("state") == "booked" and isinstance(record.get("paid_total"), (int, float)):
                currency = str(record.get("paid_currency") or trip["currency"])
                paid[currency] = paid.get(currency, 0) + record["paid_total"]
        booked_groups = {booking_rules.group_key(*booking_index[str(r["option_id"])]) for r in booking_live if r.get("state") == "booked"}
        all_groups = {booking_rules.group_key(kind, option) for kind, option in booking_index.values()}
        paid_text = " + ".join(markup(money(v, v, c)) for c, v in sorted(paid.items())) or "—"
        booking_facts = (f'<div class="fact booked-so-far"><strong>{paid_text}</strong><span>Booked so far (user-confirmed)</span></div>'
                         f'<div class="fact still-to-book"><strong>{len(all_groups - booked_groups)}</strong><span>Groups still to book</span></div>')
    return f'''<!doctype html><html lang="{attr(trip["language"])}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="color-scheme" content="light"><title>{esc(trip["title"])}</title><style>:root{{--ink:#162235;--muted:#5d6b7c;--paper:#f7f9fc;--card:#fff;--accent:#0b6e69;--soft:#e4f4f1;--line:#d9e2ec;--warn:#8a4b08;--warn-bg:#fff5df}}*{{box-sizing:border-box}}body{{margin:0;background:var(--paper);color:var(--ink);font:16px/1.55 system-ui,-apple-system,"Segoe UI",sans-serif}}main{{max-width:1120px;margin:auto;padding:32px 20px 56px}}h1{{font-size:clamp(2rem,5vw,3.6rem);line-height:1.05}}h2{{font-size:1.35rem}}h3{{font-size:1.05rem}}h4{{margin:18px 0 0;font-size:1rem}}.hero,.panel,.day-card{{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:22px;margin:20px 0;box-shadow:0 8px 24px rgb(20 40 65/.05)}}.hero{{background:linear-gradient(135deg,#fff,var(--soft))}}.grid,.dining-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(235px,1fr));gap:14px}}.fact,.option,.dining-stop{{border:1px solid var(--line);border-radius:12px;padding:14px}}.fact strong{{display:block}}.eyebrow,.meta{{color:var(--muted);font-size:.92rem}}.eyebrow{{color:var(--accent);font-weight:800;text-transform:uppercase;letter-spacing:.08em}}.pill{{display:inline-block;padding:3px 8px;border-radius:99px;background:var(--soft);color:#075952;font-size:.78rem;font-weight:700}}.day-top{{display:flex;justify-content:space-between;gap:16px}}.day-number{{min-width:48px;height:48px;display:grid;place-items:center;border-radius:50%;background:var(--ink);color:#fff;font-weight:800}}.timeline,.segment-list,.option-details{{list-style:none;padding:0}}.timeline li{{display:grid;grid-template-columns:88px 1fr;gap:12px;padding:12px 0;border-top:1px solid var(--line)}}.timeline time{{color:var(--accent);font-weight:800}}.option-details li{{margin:7px 0}}.segment-list{{margin:8px 0}}.route-segment{{display:flex;align-items:center;justify-content:space-between;gap:12px;padding:12px 0;border-top:1px solid var(--line)}}.route-segment p{{margin:4px 0 0}}.route-map{{padding:14px;border-radius:12px;background:#f1f7f8;margin:16px 0}}.route-map svg{{display:block;width:100%;height:auto}}.route-map figcaption{{color:var(--muted);font-size:.88rem;margin-top:8px}}a{{color:#075952;font-weight:700}}.booking-link,.map-link,.dining-link,.dining-reservation-link{{display:inline-block;margin:8px 8px 0 0;padding:9px 12px;border-radius:9px;background:var(--accent);color:#fff;text-decoration:none}}.map-link{{background:var(--ink)}}.warning{{border-left:4px solid var(--warn);background:var(--warn-bg);padding:14px;border-radius:0 10px 10px 0}}@media(max-width:600px){{main{{padding:18px 12px 36px}}.hero,.panel,.day-card{{padding:18px}}.timeline li{{grid-template-columns:66px 1fr}}.route-segment{{align-items:flex-start;flex-direction:column}}}}.plan-age{{display:table;margin-top:8px;padding:3px 10px;border-radius:8px;background:var(--warn-bg);color:var(--warn);font-weight:700}}.plan-age:empty{{display:none}}.booking-badge{{display:inline-block;margin:6px 0;padding:3px 10px;border-radius:8px;background:var(--soft);color:#075952;font-weight:700}}.booking-badge[data-booking-state="chosen"]{{background:var(--warn-bg);color:var(--warn)}}.reservation-need{{font-weight:700;color:var(--accent)}}details.not-chosen{{margin:10px 0}}details.not-chosen summary{{cursor:pointer;color:var(--muted);font-weight:700}}.calendar-offer{{margin:16px 0}}.calendar-offer .meta{{display:block;margin-top:6px}}.calendar-offer .calendar-undecided,.calendar-offer .calendar-floating{{display:block;margin-top:4px}}#arrival-essentials .grid{{grid-template-columns:repeat(auto-fit,minmax(330px,1fr))}}#arrival-essentials .fact strong{{margin-bottom:6px;color:var(--accent)}}.spine{{list-style:none;padding:0;margin:8px 0 0;display:flex;flex-wrap:wrap;align-items:center;gap:10px}}.spine-stop{{border:1px solid var(--line);border-radius:12px;padding:10px 14px;background:var(--soft)}}.spine-stop strong{{display:block}}.spine-move{{color:var(--muted);font-size:.85rem;font-weight:700;white-space:nowrap}}.spine-move::before{{content:"→ ";color:var(--accent)}}.anchor-photo{{margin:10px 0 0}}.anchor-photo img{{width:100%;height:auto;border-radius:10px;display:block}}.photo-credit{{color:var(--muted);font-size:.72rem;margin-top:4px}}.hero-photo{{margin:20px 0}}.hero-photo img{{width:100%;max-height:340px;object-fit:cover;border-radius:16px}}@media print{{.hero-photo img{{max-height:200px}}}}{plan_visuals.VISUAL_CSS}@media print{{body{{background:#fff}}main{{max-width:none;padding:0}}.hero,.panel,.day-card{{box-shadow:none;break-inside:avoid}}.booking-link,.map-link,.dining-link,.dining-reservation-link{{color:#075952;background:transparent;padding:0;text-decoration:underline}}}}</style></head><body><main id="trip-plan" data-trip-plan><header id="trip-summary" class="hero"><p class="eyebrow">Plan status · {vocab(plan.get("plan_status"))}</p><h1>{esc(trip["title"])}</h1><p>{esc(trip["origin"])} → {esc(trip["destination"])} · {esc(trip["start_date"])} to {esc(trip["end_date"])} · {esc(trip["traveler_count"])} traveller(s)</p><p class="meta">Arrival: {vocab(trip["arrival_transport_mode"])} · Pace: {esc(trip["pace"])} · Currency: {esc(trip["currency"])} · Research last checked: {stamp(plan.get("generated_at"))}. Prices and availability require recheck before purchase. <span id="plan-age" class="plan-age" data-generated="{attr(str(plan.get("generated_at") or "")[:10])}" data-start="{attr(trip["start_date"])}" data-age-tpl="Opened N day(s) after that research." data-until-tpl="Departure is in N day(s)." data-past-tpl="This trip has already started or passed." data-stale-tpl="Prices, opening hours and entry rules drift; treat every figure here as needing a recheck."></span></p></header>{calendar_button}{stay_spine}{hero_photo}{unverified_banner}{constraints_panel}{preferences_panel}{page_nav}<section id="budget-summary" class="panel"><h2>Budget at a glance</h2><div class="grid"><div class="fact"><strong>{markup(total)}</strong><span>Comparable cost per person</span></div>{cap_fact}<div class="fact"><strong>{esc(trip["budget_basis"])}</strong><span>Included assumptions</span></div><div class="fact"><strong>{vocab(plan["transport_preference"]["mode"])}</strong><span>Ground-mobility plan</span></div>{unpriced}{booking_facts}</div>{budget_note}{budget_figure}{walking_figure}</section>{entry_panel}{essentials_panel}{budget_breakdown}{anchors}<section id="booking-panel" class="panel" data-bookings="{panel_state}">{booking_heading}{platform_note}<p class="meta">Current researched options only. Opening a link never creates a reservation.</p>{"".join(cards)}</section>{"".join(day_cards)}<section id="transport-overview" class="panel"><h2>Overall transport</h2><p>{markup(overview_headline)}</p>{"".join(f"<p>{esc(note)}</p>" for note in as_list(overview.get("notes")) if note)}<a class="map-link" data-map-scope="{attr(overview_scope)}" data-verified-at="{attr(overview["overall_map_checked_at"])}" href="{attr(overview["overall_route_map_url"])}" target="_blank" rel="noopener noreferrer">{overview_map_label}</a></section><section id="source-register" class="panel"><h2>Sources, confidence, and recheck list</h2><details open><summary>Sources used</summary><ul>{source_rows}</ul></details>{assumptions_block}<details open><summary>Recheck before purchase</summary><p>{recheck}</p></details>{gates_line}{rechecked_line}</section></main><script>/* How old is this page, computed when it is opened. The plan carries fixed
dates; a reader four months later sees the same page as one opened the day it was made, while every
price, opening hour and entry rule has drifted. Progressive enhancement on purpose: with scripting
off this element stays empty and the static sentence above it is already complete, so nothing is
lost. No network, so it still works on a phone with no signal -- which is exactly when this page is
read. Every string comes from the renderer's label table via data attributes, so a Chinese page
cannot leak English here. */
(function(){{try{{var e=document.getElementById("plan-age");if(!e)return;
var g=e.getAttribute("data-generated"),s=e.getAttribute("data-start");if(!g)return;
var D=864e5,now=new Date(),t=function(x){{var p=String(x||"").split("-");return p.length===3?Date.UTC(+p[0],+p[1]-1,+p[2]):NaN}};
var today=Date.UTC(now.getFullYear(),now.getMonth(),now.getDate());
var age=Math.round((today-t(g))/D),until=s?Math.round((t(s)-today)/D):NaN;
var f=function(k,n){{return (e.getAttribute(k)||"").replace("N",n)}};
var out=[];if(isFinite(age)&&age>0)out.push(f("data-age-tpl",age));
if(isFinite(until)){{out.push(until>=0?f("data-until-tpl",until):e.getAttribute("data-past-tpl")||"")}}
if(age>30)out.push(e.getAttribute("data-stale-tpl")||"");
e.textContent=out.filter(Boolean).join(" ")}}catch(_){{}}}})();</script></body></html>'''


def render(plan: dict) -> str:
    """Render the page and localize renderer-owned text for the requested language."""
    page = decorate_primary_map_links(render_unlocalized(plan), plan)
    page = localize_static_page(page, plan["trip"]["language"], plan.get("ui_labels"))
    design = FINAL_PAGE_DESIGN + palette_css(palette_for(plan))
    return page.replace("</style>", design + "</style>", 1)


def main() -> int:
    parser = argparse.ArgumentParser(description="Render a Travel Buddy final itinerary HTML page.")
    parser.add_argument("plan", help="Plan JSON path, or - to read standard input")
    parser.add_argument("output", nargs="?", default="-", help="Output HTML path, or - for standard output")
    args = parser.parse_args()
    try:
        plan = read_json(args.plan)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: Could not read plan JSON: {exc}", file=sys.stderr)
        return 2

    # The photographs live beside the plan rather than inside it (fetch_plan_imagery.py explains
    # why at length: 96% of one delivered plan was base64, and every reader of that plan paid for
    # it). They are merged back here, in memory, for exactly as long as it takes to render -- no
    # new argument, because a photo payload that has to be asked for is one that gets forgotten,
    # and a forgotten one produces a page that is silently missing every image with no gate to
    # say so. Merged into the in-memory plan and never written back: this function does not write
    # the plan at all, and save_trip_deliverables.py keeps the two apart deliberately.
    try:
        imagery, _ = resolve_plan_imagery(plan, args.plan)
    except ImagerySidecarError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    if imagery:
        plan["imagery"] = imagery

    errors = validate_plan(plan)
    if errors:
        print("INVALID PLAN", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    result = render(plan)
    if args.output == "-":
        print(result)
    else:
        Path(args.output).write_text(result, encoding="utf-8")
    # Named on BOTH branches, and to stderr so a pipe to a file is unaffected. Same reason as the
    # line check_plan_consistency prints: the pipeline has to say where it continues, or an
    # assistant reconstructs the order from prose and stops at the first clean exit. Measured with
    # a different assistant, which ran two gates, fixed everything they reported, and called a
    # plan fixed while a defect this step catches was still in it.
    print("NEXT: python scripts/validate_trip_html.py <final.html> --plan <plan.json>, then "
          "python scripts/check_link_targets.py <final.html>, then "
          "python scripts/save_trip_deliverables.py <plan.json> --workspace \"<workspace>\" "
          "--verification <report.json> (or --unverified).", file=sys.stderr)
    return 0
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

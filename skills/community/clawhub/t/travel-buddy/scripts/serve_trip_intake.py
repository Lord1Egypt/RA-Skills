#!/usr/bin/env python3
"""Serve a loopback-only initial trip form and save one submitted trip profile.

Usage: python serve_trip_intake.py [--workspace PATH] [--port PORT] [--profile PROFILE_JSON]
"""

from __future__ import annotations

import argparse
import hmac
import json
import os
import re
import secrets
import subprocess
import sys
import threading
import urllib.parse
from datetime import date, datetime
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from travel_workspace import DEFAULT_WORKSPACE, find_sensitive_keys, find_sensitive_values, validate_profile
from run_destination_discovery import resolve_assistant
from intake_language import LANGUAGE_HEADER, normalize_language, pick, resolve_form_language


FORM = Path(__file__).resolve().parents[1] / "assets" / "trip-intake-form.html"
MAX_BODY_BYTES = 256 * 1024
DISCOVERY_RUNNER = Path(__file__).resolve().with_name("run_destination_discovery.py")
PROJECT_ROOT = Path(__file__).resolve().parents[1]


# --------------------------------------------------------------------------------------
# Request guards shared by both intake forms
# --------------------------------------------------------------------------------------
# "Bound to 127.0.0.1" was being read as "private". It is not: every page open in the
# traveller's browser can reach a loopback port, so while this server is up, any tab could POST
# a complete trip intake into the workspace and start an assistant on it, and the traveller
# would see a plan they never asked for. The one-time token minted at startup is what actually
# distinguishes the page this process printed a link to from every other page on the machine.
#
# The traveller's experience is unchanged: they still click the link the terminal prints, and
# the token rides along in it. The form needed no edit because it already builds its POST URL
# from the injected `submit_url`, so the token travels with that.
LOOPBACK_HOSTS = {"127.0.0.1", "localhost", "::1"}


def mint_token() -> str:
    return secrets.token_urlsafe(16)


def request_route(path: str) -> str:
    """Return the path without its query string, so `/?token=…` still routes to `/`."""
    return urllib.parse.urlsplit(path).path


def token_rejection(path: str, expected: str, lang: str = "zh") -> str | None:
    """Return a refusal, in `lang`, when a request does not carry this session's token."""
    supplied = (urllib.parse.parse_qs(urllib.parse.urlsplit(path).query).get("token") or [""])[0]
    if not supplied:
        return pick(lang, "链接缺少本次会话的一次性令牌。请回到终端，使用它打印的完整链接（含 ?token=…）重新打开本页。",
                    "This link is missing the session's one-time token. Go back to the terminal and reopen the page "
                    "with the full link it printed (including ?token=…).")
    # Compare as bytes: compare_digest rejects non-ASCII str outright, and the supplied value is
    # attacker-controlled text, not necessarily a token this process ever minted.
    if not hmac.compare_digest(supplied.encode("utf-8"), expected.encode("utf-8")):
        return pick(lang, "本次会话的一次性令牌不正确。请回到终端，使用它最新打印的完整链接重新打开本页。",
                    "This link's one-time token is not the one for this session. Go back to the terminal and reopen "
                    "the page with the latest full link it printed.")
    return None


def origin_rejection(origin: str | None, lang: str = "zh") -> str | None:
    """Refuse a submission a browser labelled as coming from somewhere other than this machine.

    Any loopback host passes rather than this exact host:port, because the traveller may open
    `localhost:PORT` when the terminal printed `127.0.0.1:PORT` and that is not an attack. The
    token above is the real gate; this only closes the case where a foreign page still manages
    to send the request.
    """
    if origin is None:
        return None
    if urllib.parse.urlsplit(origin).hostname in LOOPBACK_HOSTS:
        return None
    return pick(lang, f"拒绝来自 {origin} 的跨站提交：本表单只接受终端打印的本机链接所打开的页面。请用该链接重新打开本页再提交。",
                f"Refused a cross-site submission from {origin}: this form only accepts the page opened from the "
                f"local link the terminal printed. Reopen the page with that link and submit again.")


def content_type_rejection(value: str | None, lang: str = "zh") -> str | None:
    """Require a JSON body, which is also what forces a browser to ask permission first.

    A cross-site page can POST a form body without any preflight, but it cannot set
    application/json without one -- and this server answers no OPTIONS request, so that
    preflight fails and the submission never arrives.
    """
    if (value or "").split(";", 1)[0].strip().casefold() == "application/json":
        return None
    return pick(lang, "提交必须使用 Content-Type: application/json。请通过终端打印的本机链接打开表单后再提交。",
                "Submissions must use Content-Type: application/json. Open the form through the local link the "
                "terminal printed, then submit.")


class IntakeRequestGuard:
    """Token/origin/content-type guards mixed into both loopback intake handlers.

    Defined once and shared because the profile form hands the browser straight on to the trip
    form: a guard present on one and missing on the other leaves the same session half open.
    """

    def send_text(self, status: HTTPStatus, text: str) -> None:
        body = text.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def request_language(self) -> str:
        """The language of the page behind this request.

        A page sends LANGUAGE_HEADER with every submission and it follows the page's own language
        switch, so a traveller who switched to English is answered in English. A page load sends
        none, and gets the language the server was opened in.
        """
        return normalize_language(self.headers.get(LANGUAGE_HEADER)) or self.server.language

    def get_is_allowed(self) -> bool:
        """Answer a page load only for the link this process printed."""
        rejection = token_rejection(self.path, self.server.token, self.request_language())
        if rejection:
            self.send_text(HTTPStatus.FORBIDDEN, rejection)
            return False
        return True

    def post_is_allowed(self) -> bool:
        """Answer a submission only when it could have come from this session's own page."""
        lang = self.request_language()
        rejection = (
            token_rejection(self.path, self.server.token, lang)
            or origin_rejection(self.headers.get("Origin"), lang)
            or content_type_rejection(self.headers.get("Content-Type"), lang)
        )
        if rejection:
            self.send_json(HTTPStatus.FORBIDDEN, {"error": rejection})
            return False
        return True


# The scope question now asks about visa burden rather than geography, because
# "domestic vs cross-border" was standing in for "does this need a visa" and got it
# wrong for anyone whose residence permit gives them free movement. Legacy values from
# intakes saved before that change are still accepted and mapped forward.
#
# Narrowed again to a yes/no: does this trip need a visa the traveller does not yet hold?
# The three-way version still made a traveller who already holds the visa answer a question
# about visa *effort*, which then triggered a full entry-eligibility research pass that their
# own passport had already settled. "No" now means "I can enter what I want to enter", and
# `held_entry_documents` records what on — which is the only fact worth verifying.
TRIP_SCOPES = ("no_new_visa_needed", "any_including_visa")
LEGACY_TRIP_SCOPES = {
    "home_country_only": "no_new_visa_needed",
    "visa_free_only": "no_new_visa_needed",
    "domestic": "no_new_visa_needed",
    "cross_border": "any_including_visa",
    "domestic_or_cross_border": "any_including_visa",
}


def normalized_scope(value: object) -> str | None:
    if value in TRIP_SCOPES:
        return str(value)
    return LEGACY_TRIP_SCOPES.get(str(value))


# The saved intake used to record `mode: "discovery"` unconditionally, which contradicted
# its own `destination_scope.state` whenever a destination was already fixed: the file said
# "find me a destination" while the traveller had committed to one. The work mode is not an
# independent answer, it is a function of the scope answer (SKILL.md "Work mode"), so derive
# it in one place and make the mismatch a validation error rather than a silent contradiction.
WORK_MODES = ("discovery", "constrained_discovery", "construction")
SCOPE_WORK_MODES = {
    "fixed": "construction",
    "anchored": "constrained_discovery",
    "continent": "discovery",
    "open": "discovery",
}


def work_mode_for(scope_state: object) -> str | None:
    return SCOPE_WORK_MODES.get(str(scope_state))


def parse_date(value: object) -> date | None:
    if not isinstance(value, str):
        return None
    try:
        return date.fromisoformat(value)
    except ValueError:
        return None


def safe_name(value: object) -> str:
    text = re.sub(r"[^\w-]+", "-", str(value or "trip"), flags=re.UNICODE).strip("-_")
    return text[:48] or "trip"


def profile_defaults_from_profile(profile: object) -> dict[str, object]:
    errors = validate_profile(profile)
    if errors:
        raise ValueError("Invalid reusable profile: " + " ".join(errors))
    if not isinstance(profile, dict):
        raise ValueError("Reusable profile must be a JSON object.")
    identity = profile.get("identity_and_language", {})
    logistics = profile.get("home_and_logistics", {})
    preferences = profile.get("recurring_preferences", {})
    digital_access = profile.get("digital_travel_access", {})
    if not all(isinstance(item, dict) for item in (identity, logistics, preferences, digital_access)):
        raise ValueError("Reusable profile has an invalid section.")
    return {
        "profile_id": profile.get("profile_id"),
        "home_city": logistics.get("home_city"),
        "home_country": logistics.get("home_country"),
        "acceptable_departure_airports": logistics.get("acceptable_departure_airports", []),
        "currency": logistics.get("default_currency"),
        "typical_cabin_or_seat_preference": logistics.get("typical_cabin_or_seat_preference"),
        "self_drive_preference": logistics.get("self_drive_preference"),
        "passport_nationality": identity.get("nationality"),
        "legal_residence": identity.get("legal_residence"),
        # Residence status is what actually decides whether a destination needs a visa;
        # nationality alone cannot answer that for a permit holder.
        "residence_country": identity.get("residence_country"),
        "residence_status": identity.get("residence_status"),
        "experience_direction": preferences.get("experience_direction"),
        "natural_subtypes": preferences.get("natural_subtypes", []),
        "human_cultural_subtypes": preferences.get("human_cultural_subtypes", []),
        "pace": preferences.get("pace"),
        "comfort_preference": preferences.get("lodging_style"),
        "location_priority": preferences.get("location_priority"),
        "accessibility_needs": preferences.get("accessibility_needs", []),
        "avoid_list": preferences.get("avoid_list", []),
        # Dietary needs, hard place exclusions, and the requested output language were
        # collected in the profile and then dropped here, so the trip intake asserted
        # "no dietary restrictions" and lost every `never_recommend` filter.
        "dietary_preferences": preferences.get("food_and_dietary_preferences", []),
        "never_recommend_places": never_recommend_places(profile),
        "avoid_for_now_places": excluded_places(profile, "avoid_for_now"),
        "do_not_revisit_places": do_not_revisit_places(profile),
        "wish_list_places": wish_list_places(profile),
        "preferred_response_language": identity.get("preferred_response_language"),
        "languages_spoken": identity.get("languages_spoken", []),
        "local_language_comfort": identity.get("local_language_comfort"),
        "preferred_map_apps": digital_access.get("preferred_map_apps", []),
        "preferred_booking_platforms": digital_access.get("preferred_booking_platforms", []),
        "services_to_avoid": digital_access.get("services_to_avoid", []),
        "google_services_access": digital_access.get("google_services_access", "unknown"),
        "booking_access_notes": digital_access.get("booking_access_notes"),
        "regional_service_notes": digital_access.get("notes"),
    }


def excluded_places(profile: dict, strength: str) -> list[str]:
    history = profile.get("travel_history") if isinstance(profile.get("travel_history"), dict) else {}
    entries = history.get("excluded_places") if isinstance(history.get("excluded_places"), list) else []
    return [
        str(entry.get("place")).strip()
        for entry in entries
        if isinstance(entry, dict) and entry.get("place") and entry.get("exclusion_strength") == strength
    ]


def never_recommend_places(profile: dict) -> list[str]:
    return excluded_places(profile, "never_recommend")


def do_not_revisit_places(profile: dict) -> list[str]:
    history = profile.get("travel_history") if isinstance(profile.get("travel_history"), dict) else {}
    entries = history.get("visited_places") if isinstance(history.get("visited_places"), list) else []
    return [
        str(entry.get("place")).strip()
        for entry in entries
        if isinstance(entry, dict) and entry.get("place") and entry.get("revisit_interest") == "no"
    ]


def wish_list_places(profile: dict) -> list[str]:
    history = profile.get("travel_history") if isinstance(profile.get("travel_history"), dict) else {}
    entries = history.get("wish_list") if isinstance(history.get("wish_list"), list) else []
    return [str(entry.get("place")).strip() for entry in entries if isinstance(entry, dict) and entry.get("place")]


def load_profile_defaults(path: Path) -> dict[str, object]:
    return profile_defaults_from_profile(json.loads(path.read_text(encoding="utf-8")))


def launch_destination_discovery(
    workspace: Path,
    intake_path: Path,
    profile_path: Path | None,
    timestamp: str,
    origin: object,
    assistant_mode: str,
) -> dict[str, object]:
    """Launch a separate assistant task without guessing which old session to resume."""
    assistant = resolve_assistant(assistant_mode)
    if assistant == "none":
        return {"status": "skipped", "assistant": "none", "reason": "Automatic assistant mode is disabled."}
    safe_origin = safe_name(origin)
    plans = workspace.resolve() / "plans"
    result_path = plans / f"destination-discovery-{timestamp}-{safe_origin}.md"
    log_path = plans / f"destination-discovery-{timestamp}-{safe_origin}.log"
    command = [
        sys.executable,
        str(DISCOVERY_RUNNER),
        "--assistant",
        assistant,
        "--workspace",
        str(workspace.resolve()),
        "--intake",
        str(intake_path.resolve()),
        "--project-root",
        str(PROJECT_ROOT),
        "--result-path",
        str(result_path),
        "--log-path",
        str(log_path),
    ]
    if profile_path:
        command.extend(("--profile", str(profile_path.resolve())))
    try:
        process = subprocess.Popen(
            command,
            cwd=PROJECT_ROOT,
            stdin=subprocess.DEVNULL,
            stdout=sys.stdout,
            stderr=sys.stderr,
            start_new_session=True,
        )
    except OSError as exc:
        return {"status": "failed_to_start", "assistant": assistant, "reason": str(exc)}
    # `start_new_session=True` deliberately lets the child outlive this server, which also means
    # that once the server exits nothing on the machine knows what it is. The orphan in the
    # measured run kept planning a trip nobody wanted and could not be stopped, because nobody
    # could name it. Record the PID next to the run log so stopping it is a command to copy
    # rather than a hunt through `ps`. The negative PID is the process group: start_new_session
    # makes the child its own group leader, so that one signal also stops the assistant CLI the
    # runner launched.
    stop_command = f"kill -TERM -{process.pid}"
    pid_path = plans / f"destination-discovery-{timestamp}-{safe_origin}.pid.json"
    started = {
        "status": "started",
        "assistant": assistant,
        "pid": process.pid,
        "process_group": process.pid,
        "started_at": datetime.now().astimezone().isoformat(),
        "command": command,
        "result_path": str(result_path),
        "log_path": str(log_path),
        "stop_command": stop_command,
    }
    try:
        pid_path.write_text(json.dumps(started, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    except OSError as exc:
        # Not fatal: the PID is still printed and returned below. Say so, so a reader who goes
        # looking for the file knows why it is missing instead of assuming nothing was started.
        started["pid_record_error"] = str(exc)
    else:
        started["pid_path"] = str(pid_path)
    return started


def validate_intake(value: object, lang: str = "zh") -> list[str]:
    """Validate one submitted trip intake.

    Messages are in `lang`, the language of the page that sent it: a server-side rejection is
    shown verbatim in the page's status line, and a paragraph in the other language there is
    unusable.
    """
    if not isinstance(value, dict):
        return [pick(lang, "本次旅行需求必须是一个 JSON 对象。", "This trip's details must be a JSON object.")]
    errors: list[str] = []
    joined = (lambda items: "、".join(items)) if lang == "zh" else (lambda items: ", ".join(items))
    sensitive = find_sensitive_keys(value)
    if sensitive:
        errors.append(pick(lang, "提交内容包含不应保存的敏感字段：" + joined(sensitive) + "。",
                           "The submission contains sensitive fields that must not be saved: " + joined(sensitive) + "."))
    sensitive_values = find_sensitive_values(value)
    if sensitive_values:
        errors.append(pick(lang, "提交内容疑似包含证件/支付/密码等敏感值，位置：" + joined(sensitive_values) + "。",
                           "The submission seems to contain a document number, payment detail or password at: " + joined(sensitive_values) + "."))
    if value.get("profile_version") != "1.0" or value.get("mode") not in WORK_MODES:
        errors.append(pick(lang, "不支持的本次旅行需求格式。", "This trip's details are in a format this version does not support."))
    origin = value.get("origin") if isinstance(value.get("origin"), dict) else {}
    window = value.get("travel_window") if isinstance(value.get("travel_window"), dict) else {}
    party = value.get("party") if isinstance(value.get("party"), dict) else {}
    budget = value.get("budget") if isinstance(value.get("budget"), dict) else {}
    scope = value.get("destination_scope") if isinstance(value.get("destination_scope"), dict) else {}
    geography = value.get("trip_geography") if isinstance(value.get("trip_geography"), dict) else {}
    experience = value.get("experience") if isinstance(value.get("experience"), dict) else {}
    transport = value.get("transport_preferences") if isinstance(value.get("transport_preferences"), dict) else {}
    feasibility = value.get("feasibility") if isinstance(value.get("feasibility"), dict) else {}
    regional_access = value.get("regional_service_access") if isinstance(value.get("regional_service_access"), dict) else {}
    if not origin.get("home_city") or not origin.get("country"):
        errors.append(pick(lang, "需要填写出发城市和出发国家/地区。", "Please give the departure city and country/region."))
    duration = window.get("duration_days")
    if not isinstance(duration, int) or isinstance(duration, bool) or not 1 <= duration <= 60:
        errors.append(pick(lang, "行程天数必须是 1–60 之间的整数。", "The trip length must be a whole number of days from 1 to 60."))
    start_date = parse_date(window.get("start_date"))
    end_date = parse_date(window.get("end_date"))
    if (window.get("start_date") is None) != (window.get("end_date") is None):
        errors.append(pick(lang, "确定的出发日期和返回日期必须成对填写。", "Fixed departure and return dates must be given together."))
    elif window.get("start_date") is not None and (start_date is None or end_date is None):
        errors.append(pick(lang, "出发日期和返回日期必须是 YYYY-MM-DD 格式。", "Departure and return dates must be in YYYY-MM-DD format."))
    elif start_date and end_date:
        if end_date < start_date:
            errors.append(pick(lang, "返回日期不能早于出发日期。", "The return date cannot be before the departure date."))
        elif isinstance(duration, int) and (end_date - start_date).days + 1 != duration:
            errors.append(pick(lang, "确定日期与行程天数不一致，请修改其中一个。", "The fixed dates and the number of days disagree; please change one of them."))
    elif not window.get("month_or_season"):
        errors.append(pick(lang, "请填写确定的出发/返回日期，或填写大致的月份/季节。", "Please give fixed departure and return dates, or a rough month or season."))
    if not isinstance(party.get("traveler_count"), int) or isinstance(party.get("traveler_count"), bool) or party["traveler_count"] < 1:
        errors.append(pick(lang, "同行人数必须是大于 0 的整数。", "The number of travellers must be a whole number above 0."))
    if not budget.get("target_amount") or not budget.get("currency") or not budget.get("coverage"):
        errors.append(pick(lang, "需要填写预算金额、币种和涵盖范围。", "Please give the budget amount, its currency and what it covers."))
    if not re.fullmatch(r"[A-Z]{3}", str(budget.get("currency") or "")):
        errors.append(pick(lang, "预算币种必须是三位字母代码，例如 CNY。", "The budget currency must be a three-letter code, e.g. EUR."))
    if budget.get("calculation_basis") != "per_person":
        errors.append(pick(lang, "预算必须使用人均（per_person）口径。", "The budget must be per person (per_person)."))
    if not isinstance(budget.get("included_categories"), list):
        errors.append(pick(lang, "budget.included_categories 必须是列表。", "budget.included_categories must be a list."))
    for field, zh_label, en_label in (("range_low_amount", "预算下限", "The lower budget figure"),
                                      ("range_high_amount", "预算上限", "The upper budget figure"),
                                      ("hard_cap_amount", "预算上限值", "The budget cap")):
        amount = budget.get(field)
        if not isinstance(amount, (int, float)) or isinstance(amount, bool) or amount <= 0:
            errors.append(pick(lang, f"{zh_label}必须是正数。", f"{en_label} must be a positive number."))
    if (
        isinstance(budget.get("range_low_amount"), (int, float))
        and not isinstance(budget.get("range_low_amount"), bool)
        and isinstance(budget.get("range_high_amount"), (int, float))
        and not isinstance(budget.get("range_high_amount"), bool)
        and budget["range_high_amount"] < budget["range_low_amount"]
    ):
        errors.append(pick(lang, "预算上限不能低于下限。", "The upper budget figure cannot be below the lower one."))
    scope_state = scope.get("state")
    if scope_state not in {"fixed", "anchored", "continent", "open"}:
        errors.append(pick(lang, "需要选择目的地状态。", "Please choose a destination status."))
    else:
        # A saved intake that claims one work mode while its scope implies another sends the
        # follow-up task down the wrong branch, so reject the contradiction at the door
        # instead of letting the file disagree with itself.
        expected_mode = work_mode_for(scope_state)
        if value.get("mode") in WORK_MODES and value.get("mode") != expected_mode:
            errors.append(pick(
                lang,
                f"目的地状态为「{scope_state}」时，工作模式应为「{expected_mode}」，"
                f"但提交的是「{value.get('mode')}」。",
                f"With destination status “{scope_state}” the work mode should be “{expected_mode}”, "
                f"but “{value.get('mode')}” was submitted.",
            ))
    named_places = scope.get("named_places")
    if not isinstance(named_places, list):
        errors.append(pick(lang, "destination_scope.named_places 必须是列表。", "destination_scope.named_places must be a list."))
    elif scope_state in {"fixed", "anchored"} and not [place for place in named_places if str(place).strip()]:
        # Otherwise a "fixed" scope starts a Construction handoff for a destination that
        # was never named.
        errors.append(pick(lang, "选择了已固定或有偏好的目的地时，必须填写具体地点。", "A settled or narrowed-down destination needs the actual place."))
    trip_scope = normalized_scope(geography.get("scope"))
    if trip_scope is None:
        errors.append(pick(lang, "需要选择这趟是否需要现办签证。", "Please answer whether this trip needs a new visa."))
    entry_assessment_required = trip_scope == "any_including_visa"
    if geography.get("entry_assessment_required") is not entry_assessment_required:
        errors.append(pick(lang, "trip_geography.entry_assessment_required 与所选出行范围不一致。", "trip_geography.entry_assessment_required does not match the visa answer."))
    if experience.get("direction") not in {"natural", "human_cultural", "balance"}:
        errors.append(pick(lang, "需要选择自然/人文/平衡的景色方向。", "Please choose nature, culture or a balance."))
    if not isinstance(experience.get("ranked_must_haves"), list):
        errors.append(pick(lang, "experience.ranked_must_haves 必须是列表。", "experience.ranked_must_haves must be a list."))
    if not origin.get("max_one_way_travel_time"):
        errors.append(pick(lang, "需要填写可接受的最长单程总时长。", "Please give the longest acceptable one-way journey."))
    if value.get("trip_purpose") is not None and not isinstance(value.get("trip_purpose"), str):
        errors.append(pick(lang, "trip_purpose 必须是字符串或 null。", "trip_purpose must be a string or null."))
    if window.get("fixed_commitments") is not None and not isinstance(window.get("fixed_commitments"), str):
        errors.append(pick(lang, "travel_window.fixed_commitments 必须是字符串或 null。", "travel_window.fixed_commitments must be a string or null."))
    modes = transport.get("preferred_modes")
    allowed_modes = {
        "direct_flight", "connecting_flight", "high_speed_rail", "conventional_rail_or_overnight",
        "intercity_bus", "ferry", "self_drive", "train",
    }
    if not isinstance(modes, list) or not modes or not set(modes).issubset(allowed_modes):
        errors.append(pick(lang, "请至少选择一种可接受的出行方式。", "Please choose at least one acceptable way to travel."))
    stay = value.get("stay_preferences") if isinstance(value.get("stay_preferences"), dict) else {}
    room_count = stay.get("room_count")
    if room_count is not None and (not isinstance(room_count, int) or isinstance(room_count, bool) or room_count < 1):
        errors.append(pick(lang, "房间数必须是大于 0 的整数或留空。", "The number of rooms must be a whole number above 0, or blank."))
    entries = feasibility.get("traveler_entry_profiles")
    if feasibility.get("entry_assessment_required") is not entry_assessment_required:
        errors.append(pick(lang, "feasibility.entry_assessment_required 与所选出行范围不一致。", "feasibility.entry_assessment_required does not match the visa answer."))
    if entry_assessment_required:
        if not isinstance(entries, list) or not entries:
            errors.append(pick(lang, "考虑跨境时，需要每位同行人的国籍与合法居留地。", "For a trip abroad, each traveller's nationality and legal residence are needed."))
        elif isinstance(party.get("traveler_count"), int) and len(entries) != party["traveler_count"]:
            errors.append(pick(lang, "入境信息的行数必须与同行人数一致。", "There must be one entry line per traveller."))
        else:
            for entry in entries:
                if not isinstance(entry, dict) or not all(isinstance(entry.get(key), str) and entry[key].strip() for key in ("traveler_label", "passport_nationality", "legal_residence")):
                    errors.append(pick(lang, "每行身份信息都需要称呼、护照国籍和现居国。", "Each entry line needs a name, a passport nationality and a country of residence."))
                    break
                if entry.get("residence_status") is not None and not isinstance(entry.get("residence_status"), str):
                    errors.append(pick(lang, "身份类别必须是文字或留空。", "The residence status must be text or blank."))
                    break
        if feasibility.get("visa_tolerance") not in {"visa_free_only", "evisa_acceptable", "visa_process_acceptable"}:
            errors.append(pick(lang, "可接受的签证程度必须由「这趟是否需要现办签证」推导得出。", "The acceptable visa effort must follow from the answer to “Will you need to get a visa for this trip?”."))
        # Passport validity is a hard entry filter in SKILL.md; asking for the status
        # (never the number or the date) is what makes that filter checkable.
        if feasibility.get("passport_validity_status") not in {"valid_through_trip", "not_sure", "needs_renewal"}:
            errors.append(pick(lang, "跨境旅行需要确认护照在行程结束后是否仍然有效。", "A trip abroad needs confirmation that passports stay valid after the trip."))
    else:
        # "I can already enter" still has to say what it enters on, because that string is
        # what the verify stage checks instead of re-deriving eligibility from nationality.
        if feasibility.get("visa_tolerance") != "no_new_visa_needed":
            errors.append(pick(lang, "不需要现办签证时，visa_tolerance 必须为 no_new_visa_needed。", "When no new visa is needed, visa_tolerance must be no_new_visa_needed."))
        if feasibility.get("entry_status") != "traveler_asserts_can_enter":
            errors.append(pick(lang, "不需要现办签证时，entry_status 必须为 traveler_asserts_can_enter。", "When no new visa is needed, entry_status must be traveler_asserts_can_enter."))
        # A held visa does not make an expired passport board a plane. This branch covers both
        # "staying home" and "going abroad on something I already hold", so validity is still
        # required here -- with an explicit domestic opt-out, not an assumed one.
        if feasibility.get("passport_validity_status") not in {
            "valid_through_trip", "not_sure", "needs_renewal", "not_applicable_domestic"
        }:
            errors.append(pick(lang, "即使无需现办签证，也要确认护照有效期（国内出行请选 not_applicable_domestic）。", "Even without a new visa, please confirm passport validity (for a domestic trip, choose not_applicable_domestic)."))
        # Restores the privacy guard the three-way scope carried: identity is collected only
        # where it can affect entry. A trip that never leaves the country has no entry question
        # to answer, so nationality and residence must not be stored for it.
        if feasibility.get("passport_validity_status") == "not_applicable_domestic" and entries not in ([], None):
            errors.append(pick(lang, "仅国内出行时不应收集同行人的身份信息。", "A domestic trip must not collect the travellers' identity details."))
    climate = feasibility.get("climate_preferences")
    if not isinstance(climate, list):
        errors.append(pick(lang, "气候偏好必须是列表。", "Climate preferences must be a list."))
    elif "无特别气候限制" in climate and len(climate) > 1:
        errors.append(pick(lang, "“无特别气候限制”不能与其他气候偏好同时选择。", "“No particular climate needs” cannot be combined with other climate choices."))
    if not isinstance(feasibility.get("dietary_or_religious_needs"), list):
        errors.append(pick(lang, "饮食/宗教限制必须是列表。", "Dietary or religious needs must be a list."))
    if regional_access and regional_access.get("selection_preference") not in {
        "auto_by_destination", "mainland_china_local", "avoid_google", "google_available", "confirm_later"
    }:
        errors.append(pick(lang, "地图/服务选择方式的取值无效。", "The map and service selection value is not valid."))
    if regional_access and regional_access.get("google_services_access") not in {"available", "unavailable", "unknown"}:
        errors.append(pick(lang, "Google 服务可用性必须是 available、unavailable 或 unknown。", "Google service access must be available, unavailable or unknown."))
    for field in ("preferred_map_apps", "preferred_booking_platforms", "services_to_avoid"):
        if regional_access and not isinstance(regional_access.get(field), list):
            errors.append(pick(lang, f"regional_service_access.{field} 必须是列表。", f"regional_service_access.{field} must be a list."))
    if regional_access and regional_access.get("notes") is not None and not isinstance(regional_access.get("notes"), str):
        errors.append(pick(lang, "regional_service_access.notes 必须是字符串或 null。", "regional_service_access.notes must be a string or null."))
    return errors


class TripIntakeServer(ThreadingHTTPServer):
    def __init__(self, address: tuple[str, int], workspace: Path, profile_path: Path | None, profile_defaults: dict[str, object], assistant_mode: str = "auto", token: str | None = None, language: str = "zh") -> None:
        super().__init__(address, TripIntakeHandler)
        self.workspace = workspace
        # The language the page opens in (resolve_form_language: flag, else the profile's
        # preference, else Chinese). The page can still switch; see request_language().
        self.language = language
        self.profile_path = profile_path
        self.profile_defaults = profile_defaults
        self.assistant_mode = assistant_mode
        self.token = token or mint_token()
        # The page and the terminal both promise "one submission", and nothing used to enforce
        # it: `shutdown()` is asynchronous, so the server kept accepting POSTs after answering
        # the first. Two that arrived together -- a double-clicked submit button is enough --
        # each wrote their own intake JSON under a distinct timestamp and each launched their own
        # discovery child, leaving two assistants planning two trips from one traveller.
        self.submit_lock = threading.Lock()
        self.submitted = False

    def submit_url(self) -> str:
        # token_urlsafe output is already URL-safe, so it needs no escaping here.
        return f"/submit?token={self.token}"


class TripIntakeHandler(IntakeRequestGuard, BaseHTTPRequestHandler):
    server: TripIntakeServer

    def log_message(self, format: str, *args: object) -> None:
        return

    def send_json(self, status: HTTPStatus, payload: dict[str, object]) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:
        if request_route(self.path) not in {"/", "/index.html"}:
            self.send_error(HTTPStatus.NOT_FOUND)
            return
        if not self.get_is_allowed():
            return
        page = FORM.read_text(encoding="utf-8")
        config = json.dumps({"submit_url": self.server.submit_url(), "profile_defaults": self.server.profile_defaults, "language": self.server.language}, ensure_ascii=False).replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")
        page = page.replace("<head>", f'<head><script>window.TRAVEL_BUDDY_TRIP_INTAKE={config};</script>', 1)
        body = page.encode("utf-8")
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self) -> None:
        if request_route(self.path) != "/submit":
            self.send_error(HTTPStatus.NOT_FOUND)
            return
        if not self.post_is_allowed():
            return
        lang = self.request_language()
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if length < 1 or length > MAX_BODY_BYTES:
                raise ValueError(pick(lang, "提交内容大小无效。", "The submission is empty or too large."))
            intake = json.loads(self.rfile.read(length).decode("utf-8"))
        except (UnicodeDecodeError, ValueError, json.JSONDecodeError) as exc:
            self.send_json(HTTPStatus.BAD_REQUEST, {"error": pick(lang, f"提交内容无法解析：{exc}", f"The submission could not be read: {exc}")})
            return
        # Claim the single submission before writing anything, and only mark it claimed once a
        # file actually exists: a rejected submission must leave the slot open so the traveller
        # can fix the field the page just complained about and send it again.
        with self.server.submit_lock:
            if self.server.submitted:
                self.send_json(HTTPStatus.CONFLICT, {"error": pick(
                    lang, "本次表单只接受一次提交，已经保存过一份本次旅行需求。如需再填一份，请回到终端重新启动表单。",
                    "This form accepts one submission, and this trip has already been saved. To fill in another, "
                    "restart the form from the terminal.")})
                return
            errors = validate_intake(intake, lang)
            if errors:
                self.send_json(HTTPStatus.UNPROCESSABLE_ENTITY, {"error": " ".join(errors)})
                return
            # The profile's preferred output language was handed to this form and then dropped:
            # 0 of 15 real intakes carried it. The intake now records the language the page was
            # in when submitted, and the language the traveller wants the plan in -- their
            # profile's preference when it names one, else the language they just used.
            intake["form_language"] = lang
            intake["preferred_output_language"] = normalize_language(
                (self.server.profile_defaults or {}).get("preferred_response_language")) or lang
            timestamp = datetime.now().strftime("%Y%m%d-%H%M%S-%f")
            origin = intake["origin"]["home_city"]
            destination = self.server.workspace / "plans" / f"intake-{timestamp}-{safe_name(origin)}.json"
            event_destination = self.server.workspace / "plans" / f"next-action-{timestamp}-{safe_name(origin)}.json"
            try:
                destination.parent.mkdir(parents=True, exist_ok=True)
                with destination.open("x", encoding="utf-8") as file:
                    json.dump(intake, file, ensure_ascii=False, indent=2)
                    file.write("\n")
                next_action = (
                    "trip_construction" if intake.get("mode") == "construction" else "destination_discovery"
                )
                event = {
                    "event_version": "1.0",
                    "event_type": "travel_buddy.trip_intake_saved",
                    "next_action": next_action,
                    "work_mode": intake.get("mode"),
                    "intake_path": str(destination),
                    "profile_path": str(self.server.profile_path) if self.server.profile_path else None,
                    "profile_id": self.server.profile_defaults.get("profile_id") if self.server.profile_defaults else None,
                    "created_at": datetime.now().astimezone().isoformat(),
                    "user_action_required": False,
                }
                with event_destination.open("x", encoding="utf-8") as file:
                    json.dump(event, file, ensure_ascii=False, indent=2)
                    file.write("\n")
            except FileExistsError:
                self.send_json(HTTPStatus.CONFLICT, {"error": pick(
                    lang, "已存在同名的本次旅行记录。请重新打开表单以创建新的一份。",
                    "A trip record with the same name already exists. Reopen the form to create a new one.")})
                return
            except OSError as exc:
                self.send_json(HTTPStatus.INTERNAL_SERVER_ERROR, {"error": pick(
                    lang, f"无法在本机保存本次旅行需求：{exc}", f"Could not save this trip on this computer: {exc}")})
                return
            # Set before launching, so a failure to start the assistant cannot let a second POST
            # write a second intake for the same trip.
            self.server.submitted = True
            continuation = launch_destination_discovery(
                self.server.workspace,
                destination,
                self.server.profile_path,
                timestamp,
                origin,
                self.server.assistant_mode,
            )
        print(f"TRIP INTAKE SAVED: {destination}", flush=True)
        print(f"TRAVEL BUDDY NEXT STEP: {next_action.upper()}", flush=True)
        print(f"TRAVEL BUDDY TRIP INPUT: {destination}", flush=True)
        if self.server.profile_path:
            print(f"TRAVEL BUDDY REUSABLE PROFILE: {self.server.profile_path}", flush=True)
        print(f"TRAVEL BUDDY WORKFLOW EVENT: {event_destination}", flush=True)
        if continuation["status"] == "started":
            print(f"AUTOMATIC DESTINATION DISCOVERY: STARTED ({continuation['assistant']})", flush=True)
            # The child outlives this server, so print how to stop it while the terminal that
            # started it is still the one the traveller is looking at.
            print(f"AUTOMATIC DESTINATION DISCOVERY PID: {continuation['pid']} — stop it with: {continuation['stop_command']}", flush=True)
        else:
            print(f"AUTOMATIC DESTINATION DISCOVERY: {continuation['status'].upper()}", flush=True)
            print(f"Nothing was launched. Continue in the assistant you already have open, using {destination}.", flush=True)
        self.send_json(HTTPStatus.CREATED, {"saved": True, "intake_path": str(destination), "next_action": next_action, "work_mode": intake.get("mode"), "workflow_event_path": str(event_destination), "automatic_discovery": continuation})
        threading.Thread(target=self.server.shutdown, daemon=True).start()


def blocking_advice(command: str = "python scripts/start_intake_workflow.py") -> str:
    """The line an agent needs when this command is about to block for minutes, and only then.

    `serve_forever()` holds the terminal until a real person finishes typing into a form. Claude
    Code can background a tool call and poll it; opencode, Cursor, Cline and Codex cannot -- the
    call itself holds the link hostage until the harness command timeout kills the server mid-fill,
    and the traveller's unsaved answers go with it. Measured: the link IS flushed before the block,
    so it does reach the agent. What never reached it was the sentence saying what to do about the
    block, and an agent that cannot hold SKILL.md in context rebuilds the next step from whatever
    the last command printed -- the same reason every gate here names its successor.

    Printed only when this process is NOT its own session leader. `--detach` starts the server with
    setsid, so a detached run IS the session leader and stays quiet: its output goes to a log an
    agent polls, and advice to detach inside an already-detached run is the stale kind of
    instruction that teaches readers to stop trusting the output. Where POSIX sessions do not exist
    (Windows), it advises rather than guessing, because a wrong silence costs the form.
    """
    try:
        if os.getsid(0) == os.getpid():
            return ""
    except (AttributeError, OSError):
        pass
    return ("IF YOUR CLI CANNOT RUN A COMMAND IN THE BACKGROUND, STOP THIS AND RERUN WITH "
            f"--detach: `{command} --detach` starts the same server in its own session, prints the "
            "same link, and exits in a fraction of a second, so nothing holds your tool call open. "
            "Everything the server prints afterwards goes to the .intake-<port>.log file it names; "
            "poll that file instead of this pipe. Staying in the foreground is safe only if your "
            "harness can background a command and keep it alive for the minutes a real person "
            "spends filling in the form.")


def main() -> int:
    parser = argparse.ArgumentParser(description="Open a local Travel Buddy initial trip intake page.")
    parser.add_argument("--workspace", default=str(DEFAULT_WORKSPACE), help="Workspace containing plans")
    parser.add_argument("--port", type=int, default=0, help="Loopback port; 0 chooses an available port")
    parser.add_argument("--profile", default=None, help="Validated reusable profile to prefill stable trip fields")
    parser.add_argument("--assistant", choices=("auto", "codex", "claude", "none"), default="auto", help="Assistant to start automatically after a valid submission")
    parser.add_argument("--language", choices=("zh", "en"), default=None, help="Language the form opens in; default: the profile's preferred output language, else the language the profile was filled in, else zh")
    args = parser.parse_args()
    if not 0 <= args.port <= 65535:
        parser.error("--port must be between 0 and 65535")
    profile_path: Path | None = None
    profile: dict | None = None
    profile_defaults: dict[str, object] = {}
    if args.profile:
        try:
            profile_path = Path(args.profile).expanduser().resolve(strict=True)
            profile = json.loads(profile_path.read_text(encoding="utf-8"))
            profile_defaults = profile_defaults_from_profile(profile)
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            print(f"ERROR: Could not load reusable profile: {exc}", file=sys.stderr)
            return 2
    language = resolve_form_language(args.language, profile)
    try:
        server = TripIntakeServer(("127.0.0.1", args.port), Path(args.workspace).expanduser(), profile_path, profile_defaults, args.assistant, language=language)
    except OSError as exc:
        print(f"ERROR: Could not start local trip intake server: {exc}", file=sys.stderr)
        return 2
    host, port = server.server_address
    print(f"OPEN THIS LOCAL LINK: http://{host}:{port}/?token={server.token}", flush=True)
    print(f"FORM LANGUAGE: {language} (the page has a switch; the saved intake records the language it was submitted in)", flush=True)
    print("WAITING FOR ONE TRIP INTAKE SUBMISSION. The server accepts only this computer's loopback requests, and only through the whole link above: the token in it is what proves the page is the one this terminal opened. Copy the link in full.", flush=True)
    advice = blocking_advice()
    if advice:
        print(advice, flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("TRIP INTAKE CANCELLED", flush=True)
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

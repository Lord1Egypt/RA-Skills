#!/usr/bin/env bash
# Regression smoke tests for natural-language constraint capture.
# Runs offline; no API keys or network calls.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PLAN="$SCRIPT_DIR/plan.sh"

case_one="$($PLAN '5 days in Kyoto for a couple under $1800, relaxed pace, stay near Gion, opening hours matter, vegetarian food, rain backup')"
case_two="$($PLAN '3 days in Paris for 2 people budget cap €900, packed pace, prefer Montmartre neighborhood, halal food, avoid heat')"
case_three="$($PLAN '2 days in Tokyo for 2 people under $50, opening hours matter, rain backup, food')"
case_four="$($PLAN '2 days in Hakone for a couple, food and culture')"
case_five="$($PLAN 'compare Tokyo vs Paris vs Bangkok for 7 days in December for a couple, mid range budget, food and culture, relaxed pace')"

python3 - "$case_one" "$case_two" "$case_three" "$case_four" "$case_five" <<'PY'
import json
import sys

kyoto = json.loads(sys.argv[1])
paris = json.loads(sys.argv[2])
tokyo_risk = json.loads(sys.argv[3])
hakone_sparse = json.loads(sys.argv[4])
comparison = json.loads(sys.argv[5])

assert kyoto["budget"]["cap"] == {"amount": 1800, "currency": "USD", "scope": "cap"}
assert kyoto["constraint_details"]["trip_pace"] == "relaxed"
assert kyoto["constraint_details"]["neighborhood_preference"] == "Gion"
assert kyoto["constraint_details"]["opening_hours_sensitivity"] is True
assert kyoto["constraint_details"]["food_preferences"] == ["vegetarian"]
assert kyoto["constraint_details"]["weather_sensitivity"] == ["rain backup"]
assert "constraints" not in kyoto["open_decisions"]

kyoto_places = kyoto["suggested_places"]
assert kyoto_places, "expected suggested places with scoring explanations"
for place in kyoto_places[:3]:
    factors = place["why_chosen"]
    assert len(factors) >= 2, place
    assert place["explanation"].count(":") >= 2, place["explanation"]
assert any("thematic fit" in factor for factor in kyoto_places[0]["why_chosen"])
assert any("budget fit" in factor for factor in kyoto_places[0]["why_chosen"])

kyoto_continuity = kyoto["day_plan_continuity"]
assert kyoto_continuity["sequencing_goal"].startswith("morning/afternoon/evening anchors")
assert [segment["time_of_day"] for segment in kyoto_continuity["segments"]] == ["morning", "afternoon", "evening"]
assert [segment["place"] for segment in kyoto_continuity["segments"]] == ["Gion District", "Fushimi Inari", "Kiyomizu-dera"]
assert len(kyoto_continuity["transition_rationale"]) == 2
assert all("backtracking" in note or "same-zone" in note for note in kyoto_continuity["transition_rationale"])
assert "backtracking" in kyoto_continuity["backtracking_note"]

assert paris["budget"]["tier"] == "budget"
assert paris["budget"]["cap"] == {"amount": 900, "currency": "EUR", "scope": "cap"}
assert paris["constraint_details"]["trip_pace"] == "packed"
assert paris["constraint_details"]["neighborhood_preference"] == "Montmartre"
assert paris["constraint_details"]["food_preferences"] == ["halal"]
assert paris["constraint_details"]["weather_sensitivity"] == ["heat sensitive"]


risk_types = {risk["risk"]: risk for risk in tokyo_risk["risk_fallbacks"]}
assert {"closed_venue", "weather_mismatch", "over_constrained_plan"}.issubset(risk_types), risk_types
assert risk_types["closed_venue"]["fallback"]["nearest_viable_alternative"], risk_types["closed_venue"]
assert risk_types["weather_mismatch"]["fallback"]["nearest_viable_alternative"] == "Tsukiji Outer Market", risk_types["weather_mismatch"]
assert "USD 50" in risk_types["over_constrained_plan"]["warning"], risk_types["over_constrained_plan"]
assert "1-day budget plan in Tokyo" == risk_types["over_constrained_plan"]["fallback"]["nearest_viable_alternative"]

sparse_risk = hakone_sparse["risk_fallbacks"][0]
assert sparse_risk["risk"] == "sparse_area", sparse_risk
assert sparse_risk["fallback"]["nearest_viable_alternative"] == "Tokyo", sparse_risk
assert "side-trip" in sparse_risk["fallback"]["action"], sparse_risk

compare = comparison["destination_comparison"]
assert [option["name"] for option in compare["options"]] == ["Tokyo", "Paris", "Bangkok"], compare
assert compare["recommended_option"] == "Bangkok", compare
assert compare["operator_summary"].startswith("Start with Bangkok"), compare
assert len(compare["how_to_decide"]) == 4, compare
for option in compare["options"]:
    assert len(option["fit_factors"]) >= 2, option
    assert option["tradeoffs"], option
    assert option["decision_signal"], option
    assert [row["criterion"] for row in option["decision_matrix"]] == ["Budget fit", "Season fit", "Interest fit", "Pace fit"], option
    assert option["best_for"], option
    assert option["watch_out"], option
assert any("budget_daily_usd" in option for option in compare["options"]), compare
bangkok = next(option for option in compare["options"] if option["name"] == "Bangkok")
assert next(row for row in bangkok["decision_matrix"] if row["criterion"] == "Season fit")["signal"] == "strong", bangkok
tokyo = next(option for option in compare["options"] if option["name"] == "Tokyo")
assert next(row for row in tokyo["decision_matrix"] if row["criterion"] == "Season fit")["signal"] == "caution", tokyo

polish = kyoto["output_polish"]
assert [section["title"] for section in polish["compact_sections"]] == [
    "Trip Snapshot", "Best-Fit Choices", "Day Flow", "Risks + Backups"
], polish
assert polish["decision_summary"] == "Recommend Fushimi Inari; needs live validation before final itinerary.", polish
assert len(polish["decision_rationale"]) >= 2, polish
assert any("Gion District" in item for item in polish["decision_rationale"]), polish
assert any("fallback" in action.lower() for action in polish["next_step_actions"]), polish
assert polish["status_line"] == {
    "readiness": "needs live validation before final itinerary",
    "recommended_focus": "Fushimi Inari",
    "evidence_count": 4,
    "fallback_count": 2,
    "open_decisions_count": 2,
    "next_owner": "user",
}, polish
assert len(polish["confidence_drivers"]) == 4, polish
assert any("scored 5 place candidate" in item for item in polish["confidence_drivers"]), polish
assert any("explicit constraints" in item for item in polish["confidence_drivers"]), polish
assert [item["owner"] for item in polish["next_action_checklist"]] == ["user", "operator", "operator", "user"], polish
assert polish["next_action_checklist"][0]["status"] == "needed", polish
assert "Confirm fallback preference" in polish["next_action_checklist"][-1]["action"], polish
assert polish["next_step_prompt"] == {
    "audience": "user",
    "prompt": "What type of stay should I assume?",
    "reason": "This is the highest-impact traveler clarification before the next planning pass.",
    "source": "next_action_checklist[0]",
}, polish
assert polish["clarification_prompt_card"] == {
    "missing_decision": "accommodation",
    "prompt": "What type of stay should I assume?",
    "why_now": "The stay type affects base neighborhood, daily start/end flow, and budget realism.",
    "answer_examples": ["boutique hotel", "apartment near transit", "budget ryokan"],
    "unlocks": "base-area routing and lodging-budget assumptions",
    "known_context": ["destination=Kyoto", "budget_cap=USD 1800", "constraints=food_preferences, neighborhood_preference, opening_hours_sensitivity, trip_pace, weather_sensitivity"],
    "copy_text": "What type of stay should I assume? Examples: boutique hotel, apartment near transit, budget ryokan.",
}, polish
assert polish["action_plan"] == [
    {
        "step": 1,
        "owner": "user",
        "action": "What type of stay should I assume?",
        "trigger": "missing accommodation",
        "outcome": "unblocks a more specific, lower-risk itinerary pass",
    },
    {
        "step": 2,
        "owner": "operator",
        "action": "Validate the fallback path around Kinkaku-ji",
        "trigger": "closed_venue",
        "outcome": "keeps the recommendation graceful if the primary anchor fails live checks",
    },
    {
        "step": 3,
        "owner": "operator",
        "action": "Check live hours, transit, pricing, and availability before finalizing.",
        "trigger": "offline recommendation evidence only",
        "outcome": "turns the current recommendation into a bookable or presentation-ready plan",
    },
    {
        "step": 4,
        "owner": "operator",
        "action": "Expand the continuity scaffold into timed morning, afternoon, and evening blocks.",
        "trigger": "day_plan_continuity available",
        "outcome": "preserves geographic flow while adding times, meals, and transport",
    },
], polish
assert polish["decision_badges"] == [
    {"label": "Readiness", "value": "needs_live_validation", "tone": "caution"},
    {"label": "Next owner", "value": "user", "tone": "action"},
    {"label": "Fallbacks", "value": "2 warning(s)", "tone": "caution"},
    {"label": "Decision mode", "value": "day_flow_scaffold", "tone": "sequence"},
], polish
assert polish["handoff_brief"] == {
    "title": "Planning handoff — Fushimi Inari",
    "decision": "Recommend Fushimi Inari; needs live validation before final itinerary.",
    "rationale_bullets": polish["decision_rationale"],
    "watch_out": "Verify live opening hours for Fushimi Inari before locking the itinerary.",
    "next_action": {
        "owner": "user",
        "prompt": "What type of stay should I assume?",
        "reason": "This is the highest-impact traveler clarification before the next planning pass.",
    },
    "evidence_drivers": polish["confidence_drivers"][:3],
}, polish
assert polish["quick_reply_card"] == {
    "title": "Best next move: Fushimi Inari",
    "subtitle": "needs live validation before final itinerary",
    "bullets": [polish["decision_rationale"][0], polish["confidence_drivers"][0]],
    "caveat": "Verify live opening hours for Fushimi Inari before locking the itinerary.",
    "next_ask": "What type of stay should I assume?",
    "cta": "Reply with the missing detail so I can expand this into a timed, budget-aware itinerary.",
}, polish
assert polish["operator_preflight_card"] == {
    "audience": "operator",
    "format": "send-readiness preflight",
    "recommended_focus": "Fushimi Inari",
    "send_mode": "clarification_only",
    "safe_to_send_now": "Ask the traveler for the highest-priority missing input before expanding the itinerary.",
    "must_include": [
        "recommendation: Recommend Fushimi Inari; needs live validation before final itinerary.",
        f"evidence: {polish['confidence_drivers'][0]}",
        "watch-out: Verify live opening hours for Fushimi Inari before locking the itinerary.",
        "next owner: user",
    ],
    "do_not_claim": "Do not claim live hours, routes, prices, bookings, or final viability until operator validation passes.",
    "copy_prompt": "Before sending: include the recommendation, one evidence line, the watch-out, and this next action (user): What type of stay should I assume?",
}, polish
assert polish["validation_summary"] == {
    "purpose": "operator-visible go/no-go checks before presenting or expanding the recommendation",
    "recommended_focus": "Fushimi Inari",
    "overall_gate": "hold for user clarification",
    "checks": [
        {
            "check": "live_viability",
            "owner": "operator",
            "question": "Are live hours, transit, pricing, and availability acceptable for Fushimi Inari?",
            "pass_criteria": "recommended anchors are open or bookable in the intended window and fit the stated budget tier/cap",
            "fallback_if_fails": "Kinkaku-ji",
        },
        {
            "check": "route_continuity",
            "owner": "operator",
            "question": "Does the morning/afternoon/evening order still reduce backtracking after live transit checks?",
            "pass_criteria": "each transition is same-zone or a single directional hop with reasonable transfer time",
            "fallback_if_fails": "swap the weakest segment with the nearest same-zone candidate before adding meal timing",
        },
        {
            "check": "constraint_fit",
            "owner": "operator",
            "question": "Do the selected anchors honor the captured pace, food, neighborhood, hours, budget, and weather constraints?",
            "pass_criteria": "no captured constraint is ignored without an explicit user-visible caveat or backup",
            "fallback_if_fails": "ask the user to relax the lowest-priority constraint or accept the nearest viable fallback",
        },
        {
            "check": "user_clarification",
            "owner": "user",
            "question": "What type of stay should I assume?",
            "pass_criteria": "the missing decision is answered before detailed itinerary expansion",
            "fallback_if_fails": "continue in discovery mode with assumptions clearly labeled",
        },
    ],
}, polish
assert polish["operator_review_queue"]["audience"] == "operator", polish
assert polish["operator_review_queue"]["format"] == "prioritized review queue", polish
assert polish["operator_review_queue"]["recommended_focus"] == "Fushimi Inari", polish
assert polish["operator_review_queue"]["queue_status"] == "blocked", polish
assert [item["owner"] for item in polish["operator_review_queue"]["items"]] == ["user", "operator", "operator", "operator", "operator"], polish
assert [item["severity"] for item in polish["operator_review_queue"]["items"]] == ["blocker", "warning", "required", "required", "advisory"], polish
assert polish["operator_review_queue"]["items"][0]["task"] == "What type of stay should I assume?", polish
assert polish["operator_review_queue"]["items"][1]["source"] == "risk_fallbacks[0]", polish
assert polish["operator_review_queue"]["items"][2]["task"] == "Run live viability checks for Fushimi Inari", polish
assert "[user/blocker] What type of stay should I assume?" in polish["operator_review_queue"]["copy_text"], polish
assert polish["constraint_compliance_card"] == {
    "audience": "operator",
    "format": "constraint compliance checklist",
    "recommended_focus": "Fushimi Inari",
    "overall_status": "must_preserve_constraints",
    "checks": [
        {
            "constraint": "budget_cap",
            "captured_value": "USD 1800",
            "status": "needs_operator_validation",
            "operator_check": "Confirm selected anchors, lodging assumptions, and daily costs can fit this cap before presenting the plan as viable.",
        },
        {
            "constraint": "trip_pace",
            "captured_value": "relaxed",
            "status": "must_preserve",
            "operator_check": "Match the day count, number of anchors, and transfer load to the requested pace.",
        },
        {
            "constraint": "neighborhood_preference",
            "captured_value": "Gion",
            "status": "must_preserve",
            "operator_check": "Keep the base area or route start/end aligned with the preferred neighborhood unless a caveat is shown.",
        },
        {
            "constraint": "opening_hours_sensitivity",
            "captured_value": "True",
            "status": "must_preserve",
            "operator_check": "Verify live hours and closed days before treating any venue as locked.",
        },
        {
            "constraint": "food_preferences",
            "captured_value": "vegetarian",
            "status": "must_preserve",
            "operator_check": "Confirm meals and food stops honor the captured dietary or cuisine preference.",
        },
        {
            "constraint": "weather_sensitivity",
            "captured_value": "rain backup",
            "status": "must_preserve",
            "operator_check": "Keep indoor or weather-appropriate backups visible until the forecast is checked.",
        },
    ],
    "copy_text": "\n".join([
        "1. budget_cap: USD 1800 — Confirm selected anchors, lodging assumptions, and daily costs can fit this cap before presenting the plan as viable.",
        "2. trip_pace: relaxed — Match the day count, number of anchors, and transfer load to the requested pace.",
        "3. neighborhood_preference: Gion — Keep the base area or route start/end aligned with the preferred neighborhood unless a caveat is shown.",
        "4. opening_hours_sensitivity: True — Verify live hours and closed days before treating any venue as locked.",
        "5. food_preferences: vegetarian — Confirm meals and food stops honor the captured dietary or cuisine preference.",
        "6. weather_sensitivity: rain backup — Keep indoor or weather-appropriate backups visible until the forecast is checked.",
    ]),
}, polish
assert polish["itinerary_expansion_brief"] == {
    "audience": "operator",
    "format": "expansion guardrail brief",
    "recommended_focus": "Fushimi Inari",
    "readiness": "needs live validation before final itinerary",
    "expansion_mode": "provisional",
    "sections": [
        {"section": "Day flow", "source": "day_plan_continuity", "instruction": "Preserve the morning/afternoon/evening order and transition rationale when adding exact times, meals, and transport."},
        {"section": "Recommendation evidence", "source": "suggested_places", "instruction": "Carry forward at least two concrete fit factors so the expanded itinerary stays auditable."},
        {"section": "Constraint preservation", "source": "constraint_details", "instruction": "Restate active pace, budget, food, neighborhood, hours, and weather constraints before finalizing any timed plan."},
        {"section": "Fallback path", "source": "risk_fallbacks", "instruction": "Keep Kinkaku-ji visible as the nearest viable backup until live validation passes."},
        {"section": "Clarification gate", "source": "open_decisions[0]", "instruction": "What type of stay should I assume?"},
    ],
    "copy_text": "\n".join([
        "1. Day flow [day_plan_continuity]: Preserve the morning/afternoon/evening order and transition rationale when adding exact times, meals, and transport.",
        "2. Recommendation evidence [suggested_places]: Carry forward at least two concrete fit factors so the expanded itinerary stays auditable.",
        "3. Constraint preservation [constraint_details]: Restate active pace, budget, food, neighborhood, hours, and weather constraints before finalizing any timed plan.",
        "4. Fallback path [risk_fallbacks]: Keep Kinkaku-ji visible as the nearest viable backup until live validation passes.",
        "5. Clarification gate [open_decisions[0]]: What type of stay should I assume?",
    ]),
    "safety_note": "Use this before turning compact output polish into a timed itinerary; it preserves evidence, constraints, fallbacks, and clarification gates.",
}, polish
assert polish["finalization_gate"] == {
    "purpose": "operator-visible final-answer gate to prevent provisional offline plans from being presented as fully final",
    "status": "blocked",
    "can_present_as_final": False,
    "recommended_focus": "Fushimi Inari",
    "blocking_checks": [
        {
            "type": "user_input",
            "owner": "user",
            "blocker": "What type of stay should I assume?",
            "resolution": "Answer the highest-priority open decision before presenting this as final.",
        },
        {
            "type": "live_validation",
            "owner": "operator",
            "blocker": "Verify live hours, transit, pricing, and availability for Fushimi Inari",
            "resolution": "Mark the recommended anchors viable or rerank to the nearest fallback before finalizing.",
        },
        {
            "type": "fallback_confirmation",
            "owner": "user",
            "blocker": "Confirm backup acceptability: Kinkaku-ji",
            "resolution": "Confirm or replace the fallback path so the plan can degrade gracefully.",
        },
    ],
    "safe_presentation_mode": "provisional recommendation",
    "next_resolution": "Answer the highest-priority open decision before presenting this as final.",
}, polish

assert polish["live_validation_prompt_pack"] == {
    "format": "copy-ready validation prompts",
    "title": "Live validation prompts — Fushimi Inari",
    "items": [
        {
            "owner": "operator",
            "label": "Live viability check",
            "prompt": "Please verify current hours, transit time, pricing, and availability for Fushimi Inari before this is presented as final.",
            "success_signal": "primary anchor is open/bookable, reachable, and still fits the stated budget or cap",
        },
        {
            "owner": "operator",
            "label": "Route continuity check",
            "prompt": "Please validate that the morning, afternoon, and evening sequence still reduces backtracking with live routing.",
            "success_signal": "transitions remain same-zone or one directional hop after transit checks",
        },
        {
            "owner": "operator",
            "label": "Fallback readiness check",
            "prompt": "Please confirm Kinkaku-ji is a viable backup if the primary recommendation fails live validation.",
            "success_signal": "backup is close enough, compatible with constraints, and safe to offer as the nearest viable alternative",
        },
        {
            "owner": "user",
            "label": "Traveler clarification",
            "prompt": "What type of stay should I assume?",
            "success_signal": "traveler answer resolves the highest-priority missing decision for the next planning pass",
        },
    ],
    "copy_text": "\n".join([
        "1. [operator] Live viability check: Please verify current hours, transit time, pricing, and availability for Fushimi Inari before this is presented as final.",
        "2. [operator] Route continuity check: Please validate that the morning, afternoon, and evening sequence still reduces backtracking with live routing.",
        "3. [operator] Fallback readiness check: Please confirm Kinkaku-ji is a viable backup if the primary recommendation fails live validation.",
        "4. [user] Traveler clarification: What type of stay should I assume?",
    ]),
    "usage_note": "Run these before presenting the plan as final; keep user-owned clarification separate from operator checks.",
}, polish
assert polish["shareable_summary"] == {
    "audience": "traveler",
    "format": "compact shareable text",
    "title": "Fushimi Inari planning snapshot",
    "lines": [
        "Recommendation: Recommend Fushimi Inari; needs live validation before final itinerary.",
        f"Why: {polish['decision_rationale'][0]}",
        f"Evidence: {polish['confidence_drivers'][0]}",
        "Watch-out: Verify live opening hours for Fushimi Inari before locking the itinerary.",
        "Next: What type of stay should I assume?",
    ],
    "text": "\n".join([
        "Recommendation: Recommend Fushimi Inari; needs live validation before final itinerary.",
        f"Why: {polish['decision_rationale'][0]}",
        f"Evidence: {polish['confidence_drivers'][0]}",
        "Watch-out: Verify live opening hours for Fushimi Inari before locking the itinerary.",
        "Next: What type of stay should I assume?",
    ]),
    "next_action_owner": "user",
    "tone": "plain-language, decision-first, and safe to paste into chat",
}, polish
assert polish["decision_snapshot_table"]["format"] == "compact decision table", polish
assert polish["decision_snapshot_table"]["columns"] == ["label", "value", "owner", "why_it_matters"], polish
assert [row["label"] for row in polish["decision_snapshot_table"]["rows"]] == ["Focus", "Readiness", "Primary evidence", "Watch-out", "Next action"], polish
assert polish["decision_snapshot_table"]["rows"][0] == {
    "label": "Focus",
    "value": "Fushimi Inari",
    "owner": "operator",
    "why_it_matters": "Keeps the recommendation anchor visible in compact UIs.",
}, polish
assert polish["decision_snapshot_table"]["rows"][1]["value"] == "needs live validation before final itinerary", polish
assert polish["decision_snapshot_table"]["rows"][1]["owner"] == "user", polish
assert polish["decision_snapshot_table"]["rows"][2]["value"] == polish["confidence_drivers"][0], polish
assert polish["decision_snapshot_table"]["rows"][3]["value"] == "Verify live opening hours for Fushimi Inari before locking the itinerary.", polish
assert polish["decision_snapshot_table"]["rows"][4]["value"] == "What type of stay should I assume?", polish
assert "| Item | Value | Owner | Why it matters |" in polish["decision_snapshot_table"]["markdown"], polish
assert "| Focus | Fushimi Inari | operator |" in polish["decision_snapshot_table"]["markdown"], polish
assert polish["evidence_trace_card"] == {
    "audience": "operator",
    "format": "compact evidence trace",
    "purpose": "Shows the exact structured fields behind the recommendation so operators can audit or paste a safer rationale.",
    "items": [
        {
            "label": "Destination focus",
            "source": "destination.name",
            "value": "Kyoto",
            "why_it_matters": "Anchors the recommendation and any geographic sequencing.",
        },
        {
            "label": "Top ranked place",
            "source": "suggested_places[0]",
            "value": "Fushimi Inari",
            "why_it_matters": "destination fit: Fushimi Inari is a listed highlight for Kyoto; thematic fit: adds contrast to the requested food theme",
        },
        {
            "label": "Route flow evidence",
            "source": "day_plan_continuity.transition_rationale[0]",
            "value": "Gion District → Fushimi Inari: directional move from east/central Kyoto to south/east Kyoto limits backtracking.",
            "why_it_matters": "Shows how the first-pass day order reduces backtracking.",
        },
        {
            "label": "Fallback trigger",
            "source": "risk_fallbacks[0]",
            "value": "closed_venue",
            "why_it_matters": "Verify live opening hours for Fushimi Inari before locking the itinerary.",
        },
    ],
    "copy_text": "\n".join([
        "1. Destination focus [destination.name]: Kyoto — Anchors the recommendation and any geographic sequencing.",
        "2. Top ranked place [suggested_places[0]]: Fushimi Inari — destination fit: Fushimi Inari is a listed highlight for Kyoto; thematic fit: adds contrast to the requested food theme",
        "3. Route flow evidence [day_plan_continuity.transition_rationale[0]]: Gion District → Fushimi Inari: directional move from east/central Kyoto to south/east Kyoto limits backtracking. — Shows how the first-pass day order reduces backtracking.",
        "4. Fallback trigger [risk_fallbacks[0]]: closed_venue — Verify live opening hours for Fushimi Inari before locking the itinerary.",
    ]),
}, polish
assert polish["traveler_facing_draft"]["format"] == "ready-to-send concise markdown", polish
assert polish["traveler_facing_draft"]["audience"] == "traveler", polish
assert polish["traveler_facing_draft"]["lines"][0] == "My recommendation: Recommend Fushimi Inari; needs live validation before final itinerary.", polish
assert polish["traveler_facing_draft"]["lines"][3].startswith("Flow note: Gion District"), polish
assert polish["traveler_facing_draft"]["lines"][4] == "Watch-out: Verify live opening hours for Fushimi Inari before locking the itinerary.", polish
assert polish["traveler_facing_draft"]["lines"][-1] == "Reply with accommodation so I can tighten this into the next itinerary pass.", polish
assert polish["traveler_facing_draft"]["markdown"].startswith("- My recommendation: Recommend Fushimi Inari"), polish
assert polish["traveler_facing_draft"]["safety_note"].startswith("Draft preserves watch-outs"), polish
assert polish["operator_digest"] == {
    "audience": "operator",
    "format": "copy-ready compact decision digest",
    "lines": [
        "Decision: Recommend Fushimi Inari; needs live validation before final itinerary.",
        f"Rationale: {polish['decision_rationale'][0]}",
        f"Evidence: {polish['confidence_drivers'][0]}",
        "Watch-out: Verify live opening hours for Fushimi Inari before locking the itinerary.",
        "Next (user): What type of stay should I assume?",
    ],
    "markdown": "\n".join([
        "- Decision: Recommend Fushimi Inari; needs live validation before final itinerary.",
        f"- Rationale: {polish['decision_rationale'][0]}",
        f"- Evidence: {polish['confidence_drivers'][0]}",
        "- Watch-out: Verify live opening hours for Fushimi Inari before locking the itinerary.",
        "- Next (user): What type of stay should I assume?",
    ]),
    "routing_hint": "Ask the traveler first when the next owner is user; otherwise run the operator validation before expanding the itinerary.",
}, polish
assert polish["reply_options"] == [
    {"label": "Answer accommodation", "value": "clarify:accommodation", "owner": "user", "reason": "Resolves the highest-priority missing decision before itinerary expansion."},
    {"label": "Use backup: Kinkaku-ji", "value": "accept:fallback", "owner": "user", "reason": "Lets the plan degrade gracefully if the top anchor is closed, weather-mismatched, or over-constrained."},
    {"label": "Expand timed day flow", "value": "expand:day_flow", "owner": "operator", "reason": "Converts the continuity scaffold into timed morning, afternoon, and evening blocks."},
], polish
assert polish["user_response_choices"] == [
    {"label": "boutique hotel", "value": "answer:accommodation:1", "owner": "user", "reply_text": "boutique hotel", "reason": "Example answer that resolves accommodation for the next planning pass."},
    {"label": "apartment near transit", "value": "answer:accommodation:2", "owner": "user", "reply_text": "apartment near transit", "reason": "Example answer that resolves accommodation for the next planning pass."},
    {"label": "budget ryokan", "value": "answer:accommodation:3", "owner": "user", "reply_text": "budget ryokan", "reason": "Example answer that resolves accommodation for the next planning pass."},
], polish
score = polish["reply_readiness_score"]
assert score["format"] == "weighted reply readiness score", score
assert score["score"] == 100, score
assert score["max_score"] == 100, score
assert score["rating"] == "hold", score
assert score["gate_status"] == "blocked", score
assert [item["criterion"] for item in score["criteria"]] == [
    "core_context_visible",
    "recommendation_evidence_visible",
    "flow_or_decision_mode_visible",
    "constraints_and_watchouts_labeled",
    "next_owner_clear",
], score
assert all(item["pass"] for item in score["criteria"]), score
assert score["next_improvement"] == "Answer the highest-priority open decision before presenting this as final.", score
assert polish["decision_risk_meter"] == {
    "audience": "operator",
    "format": "compact risk/readiness meter",
    "risk_level": "high",
    "traveler_send_mode": "clarify_before_final",
    "finality_gate": "blocked",
    "score": 100,
    "max_score": 100,
    "reasons": [
        "user clarification needed: accommodation",
        "fallback warning active: closed_venue",
        "offline recommendation requires live hours/transit/price validation",
        "route scaffold requires live continuity validation before exact timing",
        "captured constraints must be preserved during expansion",
    ],
    "recommended_operator_action": "Answer the highest-priority open decision before presenting this as final.",
    "copy_line": "Risk: high; send mode: clarify_before_final; next: Answer the highest-priority open decision before presenting this as final.",
}, polish
assert polish["send_decision_card"] == {
    "audience": "operator",
    "format": "send/hold decision card",
    "recommended_focus": "Fushimi Inari",
    "decision": "hold_and_ask",
    "can_send_final": False,
    "send_as": "clarifying question",
    "primary_blocker": "What type of stay should I assume?",
    "must_ask_or_include": [
        "Ask: What type of stay should I assume?",
        "Keep Kinkaku-ji visible as fallback",
        "Keep Fushimi Inari labeled as provisional recommendation",
    ],
    "hold_reason": "Highest-priority user decision is still open; do not present a final itinerary yet.",
    "copy_text": "HOLD as final plan. Send a clarifying question: What type of stay should I assume? Keep Fushimi Inari labeled as a provisional recommendation and Kinkaku-ji visible as fallback.",
}, polish
assert polish["outbound_send_packet"] == {
    "audience": "operator",
    "format": "copy-ready outbound send packet",
    "recommended_focus": "Fushimi Inari",
    "channel_form": "clarifying question",
    "status": "send_question",
    "send_now": True,
    "send_final_plan": False,
    "hold_outbound_until": "none - send the clarifying question now",
    "message_text": "I'd treat Fushimi Inari as the first-pass recommendation, but I need one answer before locking the plan. What type of stay should I assume? Examples: boutique hotel, apartment near transit, budget ryokan.",
    "why_this_form": "Highest-priority user decision is still open; do not present a final itinerary yet.",
    "do_not_add": "Do not attach a timed itinerary or claim live hours, routes, prices, or final viability for Fushimi Inari.",
    "copy_text": "I'd treat Fushimi Inari as the first-pass recommendation, but I need one answer before locking the plan. What type of stay should I assume? Examples: boutique hotel, apartment near transit, budget ryokan.",
}, polish
assert polish["reply_intake_card"] == {
    "audience": "operator",
    "format": "reply intake card",
    "recommended_focus": "Fushimi Inari",
    "waiting_on": "user",
    "expected_reply_kind": "clarification",
    "accepts": ["boutique hotel", "apartment near transit", "budget ryokan"],
    "if_answered": "Capture the stay type, keep Fushimi Inari labeled as a provisional recommendation, and keep Kinkaku-ji visible as fallback.",
    "if_unclear": "Ask once more: What type of stay should I assume?",
    "still_do_not": "Do not attach a timed itinerary or claim live hours, routes, prices, or final viability for Fushimi Inari.",
    "copy_text": "When the traveler replies, accept boutique hotel / apartment near transit / budget ryokan. Capture the stay type, keep Fushimi Inari labeled as a provisional recommendation, and keep Kinkaku-ji visible as fallback. If unclear, ask once more: What type of stay should I assume? Do not attach a timed itinerary or claim live hours, routes, prices, or final viability for Fushimi Inari.",
}, polish
assert polish["followup_send_packet"] == {
    "audience": "operator",
    "format": "copy-ready follow-up send packet",
    "recommended_focus": "Fushimi Inari",
    "trigger": "traveler clarification received",
    "channel_form": "acknowledgement plus remaining caveat",
    "status": "send_ack_keep_provisional",
    "send_now_after_answer": True,
    "send_final_plan": False,
    "hold_followup_until": "none - send the acknowledgement now, still not a final itinerary",
    "message_text": "Thanks — I'll use your answer for the stay type and keep Fushimi Inari as the first-pass recommendation. I'll also keep Kinkaku-ji visible as fallback. Next I'll confirm live hours, transit, pricing, and availability before a timed itinerary.",
    "next_operator_check": "After capturing the stay type, run live hours, transit, pricing, and availability checks for Fushimi Inari.",
    "still_do_not": "Do not treat the traveler's answer as permission to send a final timed itinerary for Fushimi Inari.",
    "copy_text": "Thanks — I'll use your answer for the stay type and keep Fushimi Inari as the first-pass recommendation. I'll also keep Kinkaku-ji visible as fallback. Next I'll confirm live hours, transit, pricing, and availability before a timed itinerary.",
}, polish
assert polish["two_turn_send_script"] == {
    "audience": "operator",
    "format": "copy-ready two-turn send script",
    "recommended_focus": "Fushimi Inari",
    "send_final_plan": False,
    "turns": [
        {
            "turn": 1,
            "when": "now",
            "status": "send_question",
            "channel_form": "clarifying question",
            "send_now": True,
            "message_text": polish["outbound_send_packet"]["message_text"],
        },
        {
            "turn": 2,
            "when": "after clarification",
            "status": "send_ack_keep_provisional",
            "channel_form": "acknowledgement plus remaining caveat",
            "send_now": True,
            "message_text": polish["followup_send_packet"]["message_text"],
        },
    ],
    "waiting_on": "user",
    "expected_reply_kind": "clarification",
    "accepts": ["boutique hotel", "apartment near transit", "budget ryokan"],
    "if_unclear": "Ask once more: What type of stay should I assume?",
    "still_do_not": "Do not treat the traveler's answer as permission to send a final timed itinerary for Fushimi Inari.",
    "unclear_turn": {
        "turn": "2-alt",
        "when": "if traveler reply is unclear",
        "status": "send_unclear_retry",
        "channel_form": "one more clarifying question",
        "send_now": True,
        "message_text": polish["unclear_reply_packet"]["message_text"],
    },
    "copy_text": (
        f"Turn 1 (send_question): {polish['outbound_send_packet']['message_text']} "
        "Wait for clarification from user; accept boutique hotel / apartment near transit / budget ryokan. "
        f"Turn 2 (send_ack_keep_provisional): {polish['followup_send_packet']['message_text']} "
        f"If unclear (send_unclear_retry): {polish['unclear_reply_packet']['message_text']} "
        "Do not treat an unclear reply as permission to send a final timed itinerary for Fushimi Inari."
    ),
}, polish
assert polish["unclear_reply_packet"] == {
    "audience": "operator",
    "format": "copy-ready unclear-reply packet",
    "recommended_focus": "Fushimi Inari",
    "trigger": "traveler clarification is unclear",
    "channel_form": "one more clarifying question",
    "status": "send_unclear_retry",
    "send_now": True,
    "send_final_plan": False,
    "message_text": "I still need one clearer answer before I can lock the plan. What type of stay should I assume? Examples: boutique hotel, apartment near transit, budget ryokan. I'll keep Fushimi Inari as the first-pass recommendation until then.",
    "why_this_form": "The inbound reply did not match boutique hotel / apartment near transit / budget ryokan.",
    "still_do_not": "Do not treat an unclear reply as permission to send a final timed itinerary for Fushimi Inari.",
    "copy_text": "I still need one clearer answer before I can lock the plan. What type of stay should I assume? Examples: boutique hotel, apartment near transit, budget ryokan. I'll keep Fushimi Inari as the first-pass recommendation until then.",
}, polish
assert polish["no_reply_nudge_packet"] == {
    "audience": "operator",
    "format": "copy-ready no-reply nudge packet",
    "recommended_focus": "Fushimi Inari",
    "trigger": "traveler clarification is still missing",
    "channel_form": "one reminder of the open question",
    "status": "send_no_reply_nudge",
    "send_now_after_silence": True,
    "send_final_plan": False,
    "wait_until": "traveler has been silent after the outbound question",
    "message_text": "Just checking in — I still need one answer before locking the plan. What type of stay should I assume? Examples: boutique hotel, apartment near transit, budget ryokan. I'll keep Fushimi Inari as the first-pass recommendation until then.",
    "why_this_form": "No traveler reply yet for clarification; restating the open question is safer than expanding.",
    "still_do_not": "Do not treat silence as permission to send a final timed itinerary for Fushimi Inari.",
    "copy_text": "Just checking in — I still need one answer before locking the plan. What type of stay should I assume? Examples: boutique hotel, apartment near transit, budget ryokan. I'll keep Fushimi Inari as the first-pass recommendation until then.",
}, polish
assert polish["post_nudge_hold_packet"] == {
    "audience": "operator",
    "format": "copy-ready post-nudge hold packet",
    "recommended_focus": "Fushimi Inari",
    "trigger": "traveler still silent after one reminder",
    "channel_form": "operator-only hold after one reminder",
    "status": "hold_after_nudge",
    "send_now": False,
    "send_final_plan": False,
    "wait_until": "traveler replies after the one reminder, or operator live-validates internally",
    "message_text": "Do not send another traveler reminder. After the one nudge, wait for a reply or run live checks internally for Fushimi Inari.",
    "why_this_form": "A second reminder would nag; continued silence still does not unlock a final itinerary for Fushimi Inari.",
    "next_operator_check": "If the traveler stays silent after the nudge, keep Fushimi Inari labeled as a first-pass recommendation and wait or live-validate internally.",
    "still_do_not": "Do not send a second reminder or treat continued silence as permission to send a final timed itinerary for Fushimi Inari.",
    "copy_text": "Do not send another traveler reminder. After the one nudge, wait for a reply or run live checks internally for Fushimi Inari.",
}, polish

assert polish["presentation_contract_check"] == {
    "audience": "operator",
    "format": "pre-send recommendation contract check",
    "recommended_focus": "Fushimi Inari",
    "status": "hold",
    "checks": [
        {"check": "decision_named", "pass": True, "evidence": "Recommend Fushimi Inari; needs live validation before final itinerary.", "if_missing": "Name the recommended focus before sending the reply."},
        {"check": "why_evidence_visible", "pass": True, "evidence": f"{polish['decision_rationale'][0]}; {polish['confidence_drivers'][0]}", "if_missing": "Include at least one rationale line and one structured evidence driver."},
        {"check": "watch_out_labeled", "pass": True, "evidence": "Verify live opening hours for Fushimi Inari before locking the itinerary.", "if_missing": "Add a watch-out or explicitly say no first-pass fallback warning was detected."},
        {"check": "next_owner_clear", "pass": True, "evidence": "user: What type of stay should I assume?", "if_missing": "Tag the next action with user or operator ownership."},
        {"check": "finality_guard_visible", "pass": True, "evidence": "blocked: provisional recommendation", "if_missing": "Show whether this is provisional or ready for final itinerary expansion."},
    ],
    "copy_note": "Before sending, verify the recommendation names the decision, shows evidence, labels watch-outs, assigns next ownership, and preserves the finality guard.",
}, polish
assert polish["presentation_markdown"]["format"] == "compact markdown draft", polish
assert [section["heading"] for section in polish["presentation_markdown"]["sections"]] == [
    "Recommendation", "Why this fits", "Watch-outs", "Next step"
], polish
assert polish["presentation_markdown"]["text"].startswith("### Recommendation\nRecommend Fushimi Inari"), polish
assert "### Watch-outs\nVerify live opening hours" in polish["presentation_markdown"]["text"], polish
assert "What type of stay should I assume? (user)" in polish["presentation_markdown"]["text"], polish
assert polish["presentation_markdown"]["tone"].startswith("scannable"), polish
assert polish["response_template"]["format"] == "four-line operator draft", polish
assert polish["response_template"]["tone"].startswith("concise"), polish
assert [line.split(":", 1)[0] for line in polish["response_template"]["lines"]] == ["Lead with", "Why", "Watch", "Next"], polish
assert "Fushimi Inari" in polish["response_template"]["lines"][0], polish
assert "Verify live opening hours" in polish["response_template"]["lines"][2], polish

compare_polish = comparison["output_polish"]
assert compare_polish["decision_summary"] == "Recommend Bangkok; needs one clarification before detailed planning.", compare_polish
assert compare_polish["status_line"] == {
    "readiness": "needs one clarification before detailed planning",
    "recommended_focus": "Bangkok",
    "evidence_count": 2,
    "fallback_count": 0,
    "open_decisions_count": 3,
    "next_owner": "user",
}, compare_polish
assert any("ranked 3 destination option" in item for item in compare_polish["confidence_drivers"]), compare_polish
assert any("explicit constraints" in item for item in compare_polish["confidence_drivers"]), compare_polish
assert any("Bangkok" in item for item in compare_polish["decision_rationale"]), compare_polish
assert any(section["title"] == "Best-Fit Choices" for section in compare_polish["compact_sections"]), compare_polish
assert compare_polish["next_action_checklist"][0]["owner"] == "user", compare_polish
assert compare_polish["next_step_prompt"]["audience"] == "user", compare_polish
assert compare_polish["next_step_prompt"]["prompt"] == "Which destination should I optimize for first?", compare_polish
assert compare_polish["clarification_prompt_card"] == {
    "missing_decision": "destination",
    "prompt": "Which destination should I optimize for first?",
    "why_now": "Locks the primary geography so comparisons or day-flow scaffolds do not stay generic.",
    "answer_examples": ["Tokyo", "Paris first, Bangkok as backup", "Keep comparing all three"],
    "unlocks": "destination-specific ranking, routing, and budget checks",
    "known_context": ["budget_tier=mid", "constraints=trip_pace"],
    "copy_text": "Which destination should I optimize for first? Examples: Tokyo, Paris first, Bangkok as backup, Keep comparing all three.",
}, compare_polish
assert compare_polish["action_plan"] == [
    {
        "step": 1,
        "owner": "user",
        "action": "Which destination should I optimize for first?",
        "trigger": "missing destination",
        "outcome": "unblocks a more specific, lower-risk itinerary pass",
    },
    {
        "step": 2,
        "owner": "operator",
        "action": "Check live hours, transit, pricing, and availability before finalizing.",
        "trigger": "offline recommendation evidence only",
        "outcome": "turns the current recommendation into a bookable or presentation-ready plan",
    },
], compare_polish
assert compare_polish["decision_badges"] == [
    {"label": "Readiness", "value": "needs_clarification", "tone": "needs_input"},
    {"label": "Next owner", "value": "user", "tone": "action"},
    {"label": "Fallbacks", "value": "0 warning(s)", "tone": "clear"},
    {"label": "Decision mode", "value": "destination_comparison", "tone": "compare"},
], compare_polish
assert compare_polish["handoff_brief"]["title"] == "Planning handoff — Bangkok", compare_polish
assert compare_polish["handoff_brief"]["next_action"]["prompt"] == "Which destination should I optimize for first?", compare_polish
assert compare_polish["handoff_brief"]["watch_out"] == "No major first-pass fallback warning from offline data.", compare_polish
assert compare_polish["quick_reply_card"] == {
    "title": "Best next move: Bangkok",
    "subtitle": "needs one clarification before detailed planning",
    "bullets": [compare_polish["decision_rationale"][0], compare_polish["confidence_drivers"][0]],
    "caveat": "No major first-pass fallback warning from offline data.",
    "next_ask": "Which destination should I optimize for first?",
    "cta": "Reply with the missing detail so I can expand this into a timed, budget-aware itinerary.",
}, compare_polish
assert compare_polish["operator_preflight_card"] == {
    "audience": "operator",
    "format": "send-readiness preflight",
    "recommended_focus": "Bangkok",
    "send_mode": "clarification_only",
    "safe_to_send_now": "Ask the traveler for the highest-priority missing input before expanding the itinerary.",
    "must_include": [
        "recommendation: Recommend Bangkok; needs one clarification before detailed planning.",
        f"evidence: {compare_polish['confidence_drivers'][0]}",
        "watch-out: No major first-pass fallback warning from offline data.",
        "next owner: user",
    ],
    "do_not_claim": "Do not claim live hours, routes, prices, bookings, or final viability until operator validation passes.",
    "copy_prompt": "Before sending: include the recommendation, one evidence line, the watch-out, and this next action (user): Which destination should I optimize for first?",
}, compare_polish
assert compare_polish["validation_summary"]["recommended_focus"] == "Bangkok", compare_polish
assert compare_polish["validation_summary"]["overall_gate"] == "hold for user clarification", compare_polish
assert [check["check"] for check in compare_polish["validation_summary"]["checks"]] == ["live_viability", "constraint_fit", "user_clarification"], compare_polish
assert compare_polish["validation_summary"]["checks"][0]["fallback_if_fails"] == "rerank the next bundled candidate before presenting the itinerary", compare_polish
assert compare_polish["validation_summary"]["checks"][-1]["question"] == "Which destination should I optimize for first?", compare_polish
assert compare_polish["constraint_compliance_card"] == {
    "audience": "operator",
    "format": "constraint compliance checklist",
    "recommended_focus": "Bangkok",
    "overall_status": "must_preserve_constraints",
    "checks": [
        {
            "constraint": "budget_tier",
            "captured_value": "mid",
            "status": "captured",
            "operator_check": "Keep the recommendation aligned with this budget tier when expanding costs and tradeoffs.",
        },
        {
            "constraint": "trip_pace",
            "captured_value": "relaxed",
            "status": "must_preserve",
            "operator_check": "Match the day count, number of anchors, and transfer load to the requested pace.",
        },
    ],
    "copy_text": "\n".join([
        "1. budget_tier: mid — Keep the recommendation aligned with this budget tier when expanding costs and tradeoffs.",
        "2. trip_pace: relaxed — Match the day count, number of anchors, and transfer load to the requested pace.",
    ]),
}, compare_polish
assert compare_polish["itinerary_expansion_brief"]["recommended_focus"] == "Bangkok", compare_polish
assert compare_polish["itinerary_expansion_brief"]["expansion_mode"] == "provisional", compare_polish
assert [section["section"] for section in compare_polish["itinerary_expansion_brief"]["sections"]] == ["Recommendation evidence", "Constraint preservation", "Clarification gate"], compare_polish
assert compare_polish["itinerary_expansion_brief"]["sections"][0]["source"] == "destination_comparison", compare_polish
assert compare_polish["itinerary_expansion_brief"]["sections"][-1]["instruction"] == "Which destination should I optimize for first?", compare_polish
assert "Recommendation evidence [destination_comparison]" in compare_polish["itinerary_expansion_brief"]["copy_text"], compare_polish
assert compare_polish["itinerary_expansion_brief"]["safety_note"].startswith("Use this before turning compact output polish"), compare_polish
assert compare_polish["finalization_gate"]["status"] == "blocked", compare_polish
assert compare_polish["finalization_gate"]["can_present_as_final"] is False, compare_polish
assert compare_polish["finalization_gate"]["recommended_focus"] == "Bangkok", compare_polish
assert [check["type"] for check in compare_polish["finalization_gate"]["blocking_checks"]] == ["user_input", "live_validation"], compare_polish
assert compare_polish["finalization_gate"]["blocking_checks"][0]["blocker"] == "Which destination should I optimize for first?", compare_polish
assert compare_polish["finalization_gate"]["safe_presentation_mode"] == "provisional recommendation", compare_polish

assert compare_polish["live_validation_prompt_pack"]["title"] == "Live validation prompts — Bangkok", compare_polish
assert [item["label"] for item in compare_polish["live_validation_prompt_pack"]["items"]] == ["Live viability check", "Traveler clarification"], compare_polish
assert compare_polish["live_validation_prompt_pack"]["items"][0]["owner"] == "operator", compare_polish
assert compare_polish["live_validation_prompt_pack"]["items"][1]["owner"] == "user", compare_polish
assert "1. [operator] Live viability check" in compare_polish["live_validation_prompt_pack"]["copy_text"], compare_polish
assert "2. [user] Traveler clarification: Which destination should I optimize for first?" in compare_polish["live_validation_prompt_pack"]["copy_text"], compare_polish
assert compare_polish["evidence_trace_card"]["format"] == "compact evidence trace", compare_polish
assert [item["label"] for item in compare_polish["evidence_trace_card"]["items"]] == ["Comparison winner", "Active constraints"], compare_polish
assert compare_polish["evidence_trace_card"]["items"][0]["source"] == "destination_comparison.recommended_option", compare_polish
assert compare_polish["evidence_trace_card"]["items"][0]["value"] == "Bangkok", compare_polish
assert "Comparison winner [destination_comparison.recommended_option]: Bangkok" in compare_polish["evidence_trace_card"]["copy_text"], compare_polish

assert compare_polish["shareable_summary"] == {
    "audience": "traveler",
    "format": "compact shareable text",
    "title": "Bangkok planning snapshot",
    "lines": [
        "Recommendation: Recommend Bangkok; needs one clarification before detailed planning.",
        f"Why: {compare_polish['decision_rationale'][0]}",
        f"Evidence: {compare_polish['confidence_drivers'][0]}",
        "Watch-out: No major first-pass fallback warning from offline data.",
        "Next: Which destination should I optimize for first?",
    ],
    "text": "\n".join([
        "Recommendation: Recommend Bangkok; needs one clarification before detailed planning.",
        f"Why: {compare_polish['decision_rationale'][0]}",
        f"Evidence: {compare_polish['confidence_drivers'][0]}",
        "Watch-out: No major first-pass fallback warning from offline data.",
        "Next: Which destination should I optimize for first?",
    ]),
    "next_action_owner": "user",
    "tone": "plain-language, decision-first, and safe to paste into chat",
}, compare_polish
assert compare_polish["decision_snapshot_table"]["format"] == "compact decision table", compare_polish
assert [row["label"] for row in compare_polish["decision_snapshot_table"]["rows"]] == ["Focus", "Readiness", "Primary evidence", "Watch-out", "Next action"], compare_polish
assert compare_polish["decision_snapshot_table"]["rows"][0]["value"] == "Bangkok", compare_polish
assert compare_polish["decision_snapshot_table"]["rows"][1]["value"] == "needs one clarification before detailed planning", compare_polish
assert compare_polish["decision_snapshot_table"]["rows"][2]["value"] == compare_polish["confidence_drivers"][0], compare_polish
assert compare_polish["decision_snapshot_table"]["rows"][3]["value"] == "No major first-pass fallback warning from offline data.", compare_polish
assert compare_polish["decision_snapshot_table"]["rows"][4]["value"] == "Which destination should I optimize for first?", compare_polish
assert "| Focus | Bangkok | operator |" in compare_polish["decision_snapshot_table"]["markdown"], compare_polish
assert compare_polish["traveler_facing_draft"]["lines"][0] == "My recommendation: Recommend Bangkok; needs one clarification before detailed planning.", compare_polish
assert compare_polish["traveler_facing_draft"]["lines"][3] == "Watch-out: No major first-pass fallback warning from offline data.", compare_polish
assert compare_polish["traveler_facing_draft"]["lines"][-1] == "Reply with destination so I can tighten this into the next itinerary pass.", compare_polish
assert "|" not in compare_polish["traveler_facing_draft"]["markdown"], compare_polish
assert compare_polish["operator_digest"]["audience"] == "operator", compare_polish
assert compare_polish["operator_digest"]["format"] == "copy-ready compact decision digest", compare_polish
assert compare_polish["operator_digest"]["lines"] == [
    "Decision: Recommend Bangkok; needs one clarification before detailed planning.",
    f"Rationale: {compare_polish['decision_rationale'][0]}",
    f"Evidence: {compare_polish['confidence_drivers'][0]}",
    "Watch-out: No major first-pass fallback warning from offline data.",
    "Next (user): Which destination should I optimize for first?",
], compare_polish
assert compare_polish["operator_digest"]["markdown"].startswith("- Decision: Recommend Bangkok"), compare_polish
assert compare_polish["operator_digest"]["routing_hint"].startswith("Ask the traveler first"), compare_polish
assert compare_polish["operator_review_queue"]["recommended_focus"] == "Bangkok", compare_polish
assert compare_polish["operator_review_queue"]["queue_status"] == "blocked", compare_polish
assert [item["source"] for item in compare_polish["operator_review_queue"]["items"]] == ["open_decisions[0]", "destination_comparison.recommended_option", "constraint_details"], compare_polish
assert compare_polish["operator_review_queue"]["items"][0]["severity"] == "blocker", compare_polish
assert compare_polish["operator_review_queue"]["items"][1]["task"] == "Run live viability checks for Bangkok", compare_polish
assert "[operator/required] Run live viability checks for Bangkok" in compare_polish["operator_review_queue"]["copy_text"], compare_polish
assert compare_polish["reply_options"] == [
    {"label": "Answer destination", "value": "clarify:destination", "owner": "user", "reason": "Resolves the highest-priority missing decision before itinerary expansion."},
    {"label": "Compare around Bangkok", "value": "expand:comparison", "owner": "operator", "reason": "Turns the recommendation into a side-by-side user explanation with tradeoffs."},
], compare_polish
assert compare_polish["user_response_choices"] == [
    {"label": "Tokyo", "value": "answer:destination:1", "owner": "user", "reply_text": "Tokyo", "reason": "Example answer that resolves destination for the next planning pass."},
    {"label": "Paris first, Bangkok as backup", "value": "answer:destination:2", "owner": "user", "reply_text": "Paris first, Bangkok as backup", "reason": "Example answer that resolves destination for the next planning pass."},
    {"label": "Keep comparing all three", "value": "answer:destination:3", "owner": "user", "reply_text": "Keep comparing all three", "reason": "Example answer that resolves destination for the next planning pass."},
], compare_polish
assert compare_polish["decision_risk_meter"] == {
    "audience": "operator",
    "format": "compact risk/readiness meter",
    "risk_level": "high",
    "traveler_send_mode": "clarify_before_final",
    "finality_gate": "blocked",
    "score": 100,
    "max_score": 100,
    "reasons": [
        "user clarification needed: destination",
        "offline recommendation requires live hours/transit/price validation",
        "captured constraints must be preserved during expansion",
    ],
    "recommended_operator_action": "Answer the highest-priority open decision before presenting this as final.",
    "copy_line": "Risk: high; send mode: clarify_before_final; next: Answer the highest-priority open decision before presenting this as final.",
}, compare_polish
assert compare_polish["send_decision_card"] == {
    "audience": "operator",
    "format": "send/hold decision card",
    "recommended_focus": "Bangkok",
    "decision": "hold_and_ask",
    "can_send_final": False,
    "send_as": "clarifying question",
    "primary_blocker": "Which destination should I optimize for first?",
    "must_ask_or_include": [
        "Ask: Which destination should I optimize for first?",
        "Keep Bangkok labeled as provisional recommendation",
    ],
    "hold_reason": "Highest-priority user decision is still open; do not present a final itinerary yet.",
    "copy_text": "HOLD as final plan. Send a clarifying question: Which destination should I optimize for first? Keep Bangkok labeled as a provisional recommendation.",
}, compare_polish
assert compare_polish["outbound_send_packet"] == {
    "audience": "operator",
    "format": "copy-ready outbound send packet",
    "recommended_focus": "Bangkok",
    "channel_form": "clarifying question",
    "status": "send_question",
    "send_now": True,
    "send_final_plan": False,
    "hold_outbound_until": "none - send the clarifying question now",
    "message_text": "I'd treat Bangkok as the first-pass recommendation, but I need one answer before locking the plan. Which destination should I optimize for first? Examples: Tokyo, Paris first, Bangkok as backup, Keep comparing all three.",
    "why_this_form": "Highest-priority user decision is still open; do not present a final itinerary yet.",
    "do_not_add": "Do not attach a timed itinerary or claim live hours, routes, prices, or final viability for Bangkok.",
    "copy_text": "I'd treat Bangkok as the first-pass recommendation, but I need one answer before locking the plan. Which destination should I optimize for first? Examples: Tokyo, Paris first, Bangkok as backup, Keep comparing all three.",
}, compare_polish
assert compare_polish["reply_intake_card"] == {
    "audience": "operator",
    "format": "reply intake card",
    "recommended_focus": "Bangkok",
    "waiting_on": "user",
    "expected_reply_kind": "clarification",
    "accepts": ["Tokyo", "Paris first, Bangkok as backup", "Keep comparing all three"],
    "if_answered": "Capture the destination, keep Bangkok labeled as a provisional recommendation.",
    "if_unclear": "Ask once more: Which destination should I optimize for first?",
    "still_do_not": "Do not attach a timed itinerary or claim live hours, routes, prices, or final viability for Bangkok.",
    "copy_text": "When the traveler replies, accept Tokyo / Paris first, Bangkok as backup / Keep comparing all three. Capture the destination, keep Bangkok labeled as a provisional recommendation. If unclear, ask once more: Which destination should I optimize for first? Do not attach a timed itinerary or claim live hours, routes, prices, or final viability for Bangkok.",
}, compare_polish
assert compare_polish["followup_send_packet"] == {
    "audience": "operator",
    "format": "copy-ready follow-up send packet",
    "recommended_focus": "Bangkok",
    "trigger": "traveler clarification received",
    "channel_form": "acknowledgement plus remaining caveat",
    "status": "send_ack_keep_provisional",
    "send_now_after_answer": True,
    "send_final_plan": False,
    "hold_followup_until": "none - send the acknowledgement now, still not a final itinerary",
    "message_text": "Thanks — I'll use your answer for the destination and keep Bangkok as the first-pass recommendation. Next I'll confirm live hours, transit, pricing, and availability before a timed itinerary.",
    "next_operator_check": "After capturing the destination, run live hours, transit, pricing, and availability checks for Bangkok.",
    "still_do_not": "Do not treat the traveler's answer as permission to send a final timed itinerary for Bangkok.",
    "copy_text": "Thanks — I'll use your answer for the destination and keep Bangkok as the first-pass recommendation. Next I'll confirm live hours, transit, pricing, and availability before a timed itinerary.",
}, compare_polish
assert compare_polish["two_turn_send_script"] == {
    "audience": "operator",
    "format": "copy-ready two-turn send script",
    "recommended_focus": "Bangkok",
    "send_final_plan": False,
    "turns": [
        {
            "turn": 1,
            "when": "now",
            "status": "send_question",
            "channel_form": "clarifying question",
            "send_now": True,
            "message_text": compare_polish["outbound_send_packet"]["message_text"],
        },
        {
            "turn": 2,
            "when": "after clarification",
            "status": "send_ack_keep_provisional",
            "channel_form": "acknowledgement plus remaining caveat",
            "send_now": True,
            "message_text": compare_polish["followup_send_packet"]["message_text"],
        },
    ],
    "waiting_on": "user",
    "expected_reply_kind": "clarification",
    "accepts": ["Tokyo", "Paris first, Bangkok as backup", "Keep comparing all three"],
    "if_unclear": "Ask once more: Which destination should I optimize for first?",
    "still_do_not": "Do not treat the traveler's answer as permission to send a final timed itinerary for Bangkok.",
    "unclear_turn": {
        "turn": "2-alt",
        "when": "if traveler reply is unclear",
        "status": "send_unclear_retry",
        "channel_form": "one more clarifying question",
        "send_now": True,
        "message_text": compare_polish["unclear_reply_packet"]["message_text"],
    },
    "copy_text": (
        f"Turn 1 (send_question): {compare_polish['outbound_send_packet']['message_text']} "
        "Wait for clarification from user; accept Tokyo / Paris first, Bangkok as backup / Keep comparing all three. "
        f"Turn 2 (send_ack_keep_provisional): {compare_polish['followup_send_packet']['message_text']} "
        f"If unclear (send_unclear_retry): {compare_polish['unclear_reply_packet']['message_text']} "
        "Do not treat an unclear reply as permission to send a final timed itinerary for Bangkok."
    ),
}, compare_polish
assert compare_polish["unclear_reply_packet"] == {
    "audience": "operator",
    "format": "copy-ready unclear-reply packet",
    "recommended_focus": "Bangkok",
    "trigger": "traveler clarification is unclear",
    "channel_form": "one more clarifying question",
    "status": "send_unclear_retry",
    "send_now": True,
    "send_final_plan": False,
    "message_text": "I still need one clearer answer before I can lock the plan. Which destination should I optimize for first? Examples: Tokyo, Paris first, Bangkok as backup, Keep comparing all three. I'll keep Bangkok as the first-pass recommendation until then.",
    "why_this_form": "The inbound reply did not match Tokyo / Paris first, Bangkok as backup / Keep comparing all three.",
    "still_do_not": "Do not treat an unclear reply as permission to send a final timed itinerary for Bangkok.",
    "copy_text": "I still need one clearer answer before I can lock the plan. Which destination should I optimize for first? Examples: Tokyo, Paris first, Bangkok as backup, Keep comparing all three. I'll keep Bangkok as the first-pass recommendation until then.",
}, compare_polish
assert compare_polish["no_reply_nudge_packet"] == {
    "audience": "operator",
    "format": "copy-ready no-reply nudge packet",
    "recommended_focus": "Bangkok",
    "trigger": "traveler clarification is still missing",
    "channel_form": "one reminder of the open question",
    "status": "send_no_reply_nudge",
    "send_now_after_silence": True,
    "send_final_plan": False,
    "wait_until": "traveler has been silent after the outbound question",
    "message_text": "Just checking in — I still need one answer before locking the plan. Which destination should I optimize for first? Examples: Tokyo, Paris first, Bangkok as backup, Keep comparing all three. I'll keep Bangkok as the first-pass recommendation until then.",
    "why_this_form": "No traveler reply yet for clarification; restating the open question is safer than expanding.",
    "still_do_not": "Do not treat silence as permission to send a final timed itinerary for Bangkok.",
    "copy_text": "Just checking in — I still need one answer before locking the plan. Which destination should I optimize for first? Examples: Tokyo, Paris first, Bangkok as backup, Keep comparing all three. I'll keep Bangkok as the first-pass recommendation until then.",
}, compare_polish
assert compare_polish["post_nudge_hold_packet"] == {
    "audience": "operator",
    "format": "copy-ready post-nudge hold packet",
    "recommended_focus": "Bangkok",
    "trigger": "traveler still silent after one reminder",
    "channel_form": "operator-only hold after one reminder",
    "status": "hold_after_nudge",
    "send_now": False,
    "send_final_plan": False,
    "wait_until": "traveler replies after the one reminder, or operator live-validates internally",
    "message_text": "Do not send another traveler reminder. After the one nudge, wait for a reply or run live checks internally for Bangkok.",
    "why_this_form": "A second reminder would nag; continued silence still does not unlock a final itinerary for Bangkok.",
    "next_operator_check": "If the traveler stays silent after the nudge, keep Bangkok labeled as a first-pass recommendation and wait or live-validate internally.",
    "still_do_not": "Do not send a second reminder or treat continued silence as permission to send a final timed itinerary for Bangkok.",
    "copy_text": "Do not send another traveler reminder. After the one nudge, wait for a reply or run live checks internally for Bangkok.",
}, compare_polish
assert compare_polish["presentation_contract_check"]["recommended_focus"] == "Bangkok", compare_polish
assert compare_polish["presentation_contract_check"]["status"] == "hold", compare_polish
assert [check["check"] for check in compare_polish["presentation_contract_check"]["checks"]] == ["decision_named", "why_evidence_visible", "watch_out_labeled", "next_owner_clear", "finality_guard_visible"], compare_polish
assert all(check["pass"] is True for check in compare_polish["presentation_contract_check"]["checks"]), compare_polish
assert compare_polish["presentation_contract_check"]["checks"][3]["evidence"] == "user: Which destination should I optimize for first?", compare_polish
assert compare_polish["presentation_markdown"]["sections"][0]["body"] == "Recommend Bangkok; needs one clarification before detailed planning.", compare_polish
assert "### Next step\nWhich destination should I optimize for first? (user)" in compare_polish["presentation_markdown"]["text"], compare_polish
assert "Bangkok" in compare_polish["response_template"]["lines"][0], compare_polish
assert compare_polish["response_template"]["lines"][3].startswith("Next:"), compare_polish

print("constraint capture smoke tests passed")
PY

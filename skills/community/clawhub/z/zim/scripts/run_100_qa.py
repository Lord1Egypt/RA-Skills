#!/usr/bin/env python3
"""100-scenario end-to-end QA for Zim WhatsApp orchestrator.

Calls the live orchestrator with real LLM (OpenRouter) and real search APIs.
Each scenario is a multi-turn conversation with validation checks.

Usage:
    cd /home/ubuntu/.openclaw/workspace/zim
    OPENROUTER_API_KEY=sk-or-... python scripts/run_100_qa.py > zim-100-qa-results.txt
"""

import json
import os
import re
import sys
import time
import traceback
from datetime import date, timedelta

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from zim.orchestrator import ZimOrchestrator
from zim.state_store import InMemoryStateStore


API_KEY = os.environ.get("OPENROUTER_API_KEY", "")
MODEL = os.environ.get("ZIM_LLM_MODEL", "anthropic/claude-3-haiku")

# Dates for scenarios
TODAY = date.today()
TOMORROW = (TODAY + timedelta(days=1)).isoformat()
NEXT_WEEK = (TODAY + timedelta(days=7)).isoformat()
IN_2_WEEKS = (TODAY + timedelta(days=14)).isoformat()
NEXT_MONTH = (TODAY + timedelta(days=30)).isoformat()


def make_orchestrator():
    store = InMemoryStateStore()
    return ZimOrchestrator(store=store, api_key=API_KEY, model=MODEL), store


def check(reply, must_contain=None, must_not_contain=None, any_of=None):
    """Validate a reply. Returns (pass, reasons)."""
    reasons = []
    lower = reply.lower()

    if must_contain:
        for phrase in must_contain:
            if phrase.lower() not in lower:
                reasons.append(f"MISSING: '{phrase}'")

    if must_not_contain:
        for phrase in must_not_contain:
            if phrase.lower() in lower:
                reasons.append(f"SHOULD_NOT_CONTAIN: '{phrase}'")

    if any_of:
        found = any(p.lower() in lower for p in any_of)
        if not found:
            reasons.append(f"MISSING_ANY_OF: {any_of}")

    return (len(reasons) == 0, reasons)


# ============================================================
# SCENARIOS
# ============================================================

SCENARIOS = []

def scenario(name, turns):
    """Register a scenario."""
    SCENARIOS.append({"name": name, "turns": turns})


# --- CATEGORY 1: FLIGHT SEARCH (basic) ---

scenario("S1: Basic flight search with full details", [
    ("I need a flight from Dubai to London on May 15", {
        "any_of": ["flight", "london", "dubai", "DXB", "LHR", "$"],
    }),
])

scenario("S2: Flight search with origin and destination only", [
    ("Find flights from Stockholm to Berlin", {
        "any_of": ["when", "date", "travel", "depart"],
    }),
])

scenario("S3: Flight search destination only - should ask origin", [
    ("I want to fly to Paris", {
        "any_of": ["where", "from", "origin", "depart", "flying from"],
    }),
])

scenario("S4: Bare booking request - should ask everything", [
    ("Book me a flight", {
        "any_of": ["where", "destination", "go", "fly"],
    }),
])

scenario("S5: Flight with cabin class preference", [
    ("Business class flight from Dubai to New York next Friday", {
        "any_of": ["flight", "business", "$", "DXB", "JFK", "NYC"],
    }),
])

scenario("S6: First class request", [
    ("First class to Tokyo from London on June 1", {
        "any_of": ["flight", "first", "$", "tokyo", "TYO", "NRT", "HND"],
    }),
])

scenario("S7: Flight for multiple travelers", [
    ("I need flights for 3 people from Dubai to Madrid on May 20", {
        "any_of": ["flight", "madrid", "$", "MAD"],
    }),
])

scenario("S8: Round trip flight", [
    ("Round trip from Copenhagen to Rome, May 10 to May 17", {
        "any_of": ["flight", "rome", "$", "CPH", "FCO", "ROM"],
    }),
])

scenario("S9: Flight with time preference", [
    ("Morning flight from Dubai to London tomorrow", {
        "any_of": ["flight", "london", "$"],
    }),
])

scenario("S10: Flight with budget constraint", [
    ("Cheapest flight from Berlin to Barcelona under $100", {
        "any_of": ["flight", "barcelona", "$", "BCN"],
    }),
])

# --- CATEGORY 2: MISSING INFO COLLECTION ---

scenario("S11: Destination only - collects origin then date", [
    ("Flights to Amsterdam", {
        "any_of": ["where", "from", "origin", "flying from"],
    }),
    ("From Dubai", {
        "any_of": ["when", "date", "travel", "depart"],
    }),
    ("Next Monday", {
        "any_of": ["flight", "amsterdam", "$", "AMS"],
    }),
])

scenario("S12: Date only - should ask destination", [
    ("I want to travel on June 5", {
        "any_of": ["where", "destination", "go"],
    }),
])

scenario("S13: Origin only - should ask destination", [
    ("Flights from Cairo", {
        "any_of": ["where", "destination", "to", "going"],
    }),
])

scenario("S14: Cabin class only - should ask route", [
    ("Book business class", {
        "any_of": ["where", "destination", "from", "go", "fly"],
    }),
])

scenario("S15: Two travelers no route - should ask", [
    ("Need flights for two people", {
        "any_of": ["where", "destination", "from", "go"],
    }),
])

# --- CATEGORY 3: RELATIVE DATE PARSING ---

scenario("S16: Tomorrow", [
    ("Flight from Dubai to London tomorrow", {
        "any_of": ["flight", "london", "$", "LHR"],
    }),
])

scenario("S17: Next Friday", [
    ("Fly from Berlin to Paris next Friday", {
        "any_of": ["flight", "paris", "$", "CDG", "PAR"],
    }),
])

scenario("S18: Next week (vague)", [
    ("I want to go to Tokyo next week", {
        "any_of": ["when", "date", "which day", "specific", "from", "origin"],
    }),
])

scenario("S19: In 2 weeks", [
    ("Flight from Dubai to Istanbul in 2 weeks", {
        "any_of": ["flight", "istanbul", "$", "IST"],
    }),
])

scenario("S20: This weekend", [
    ("Flights from London to Dublin this weekend", {
        "any_of": ["flight", "dublin", "$", "DUB"],
    }),
])

# --- CATEGORY 4: HOTEL SEARCH ---

scenario("S21: Hotel with full details", [
    ("Find me a hotel in Berlin from May 10 to May 13", {
        "any_of": ["hotel", "berlin", "$"],
    }),
])

scenario("S22: Hotel destination only", [
    ("I need a hotel in Rome", {
        "any_of": ["when", "date", "check", "stay"],
    }),
])

scenario("S23: Hotel with budget", [
    ("Hotels in Paris under $150 per night, June 1 to June 5", {
        "any_of": ["hotel", "paris", "$"],
    }),
])

scenario("S24: Hotel for multiple guests", [
    ("Hotel for 4 guests in Barcelona, May 20 to May 25", {
        "any_of": ["hotel", "barcelona", "$"],
    }),
])

scenario("S25: Hotel search no dates", [
    ("Find hotels in Tokyo", {
        "any_of": ["when", "date", "check-in", "checkin", "stay"],
    }),
])

# --- CATEGORY 5: CAR RENTAL ---

scenario("S26: Car rental with full details", [
    ("Rent a car in Dubai from May 10 to May 15", {
        "any_of": ["car", "dubai", "$", "rental"],
    }),
])

scenario("S27: Car rental location only", [
    ("I need a car rental in Rome", {
        "any_of": ["when", "date", "pick", "rental"],
    }),
])

scenario("S28: SUV request", [
    ("I need an SUV in Barcelona from June 1 to June 7", {
        "any_of": ["car", "barcelona", "$", "suv", "rental"],
    }),
])

scenario("S29: Car rental no location", [
    ("I want to rent a car", {
        "any_of": ["where", "location", "city", "pick"],
    }),
])

scenario("S30: Luxury car", [
    ("Luxury car rental in Dubai, May 15 to May 20", {
        "any_of": ["car", "dubai", "$", "luxury", "rental"],
    }),
])

# --- CATEGORY 6: TRIP PLANNING ---

scenario("S31: Full trip planning", [
    ("Plan my trip to Rome", {
        "any_of": ["when", "how long", "date", "from", "origin"],
    }),
])

scenario("S32: Trip with dates", [
    ("Plan a trip to Barcelona, 5 days starting June 10", {
        "any_of": ["from", "origin", "where", "flying", "flight", "hotel"],
    }),
])

scenario("S33: Honeymoon trip", [
    ("We're planning a honeymoon to Bali", {
        "any_of": ["when", "date", "from", "origin", "congratulations", "travel"],
    }),
])

scenario("S34: Weekend getaway", [
    ("Weekend trip to Amsterdam from Berlin", {
        "any_of": ["when", "date", "weekend", "flight", "$"],
    }),
])

scenario("S35: Family vacation", [
    ("Family vacation for 4 to Orlando in July", {
        "any_of": ["from", "origin", "where", "flying"],
    }),
])

# --- CATEGORY 7: CONVERSATIONAL CONTEXT ---

scenario("S36: Follow-up after greeting", [
    ("Hi!", {
        "any_of": ["help", "travel", "flight", "hotel", "how can", "where"],
    }),
    ("I need to go to London", {
        "any_of": ["from", "when", "date", "origin"],
    }),
])

scenario("S37: Modify after results (cabin class)", [
    ("Flight from Dubai to London on May 15", {
        "any_of": ["flight", "$"],
    }),
    ("Make it business class", {
        "any_of": ["business", "flight", "$"],
    }),
])

scenario("S38: Ask for more options", [
    ("Flights from Berlin to Rome on June 1", {
        "any_of": ["flight", "$"],
    }),
    ("Any cheaper options?", {
        "any_of": ["flight", "$", "option", "result", "search", "cheaper", "unfortunately"],
    }),
])

scenario("S39: Change destination mid-flow", [
    ("I want to fly to Paris", {
        "any_of": ["from", "origin", "where"],
    }),
    ("Actually, make that London instead", {
        "any_of": ["london", "from", "when", "date", "origin"],
    }),
])

scenario("S40: Add return date after one-way search", [
    ("Flight from Dubai to Istanbul on May 20", {
        "any_of": ["flight", "istanbul", "$"],
    }),
    ("Actually I need a return on May 27", {
        "any_of": ["flight", "return", "$", "round"],
    }),
])

# --- CATEGORY 8: EDGE CASES ---

scenario("S41: IATA code input", [
    ("Flights from DXB to LHR on May 15", {
        "any_of": ["flight", "$", "DXB", "LHR"],
    }),
])

scenario("S42: Mixed IATA and city name", [
    ("Flight from DXB to Copenhagen on May 20", {
        "any_of": ["flight", "$", "copenhagen", "CPH"],
    }),
])

scenario("S43: Misspelled city", [
    ("Flights from Dubei to Londn", {
        "any_of": ["dubai", "london", "flight", "from", "did you mean"],
    }),
])

scenario("S44: Country instead of city", [
    ("Find flights to Spain", {
        "any_of": ["which city", "airport", "barcelona", "madrid", "specific"],
    }),
])

scenario("S45: Very long message", [
    ("I'm looking for a flight from Dubai to London, preferably business class, "
     "departing on May 15th in the morning, window seat if possible, "
     "I have 2 large suitcases and a carry-on, my frequent flyer number is EK123456, "
     "and I'd like to arrive before 3pm local time", {
        "any_of": ["flight", "london", "$", "business"],
    }),
])

# --- CATEGORY 9: BOOKING FLOW ---

scenario("S46: Select option from results", [
    ("Flight from Dubai to London on May 15", {
        "any_of": ["flight", "$"],
    }),
    ("I'll take option 1", {
        "any_of": ["book", "summary", "confirm", "selected", "fee", "$", "total"],
    }),
])

scenario("S47: Select with just a number", [
    ("Flights from Berlin to Paris on June 1", {
        "any_of": ["flight", "$"],
    }),
    ("2", {
        "any_of": ["book", "summary", "confirm", "selected", "fee", "$", "option", "total", "which"],
    }),
])

scenario("S48: Confirm booking", [
    ("Flight from Dubai to London on May 15", {
        "any_of": ["flight", "$"],
    }),
    ("Option 1", {
        "any_of": ["summary", "confirm", "fee", "$", "total", "book"],
    }),
    ("Yes, confirm", {
        "any_of": ["payment", "book", "confirm", "link", "reference", "stripe", "skylerlabs"],
    }),
])

scenario("S49: Cancel mid-flow", [
    ("Flight from Dubai to London on May 15", {
        "any_of": ["flight", "$"],
    }),
    ("Cancel", {
        "any_of": ["cancel", "help", "new", "start", "how can", "else"],
    }),
])

scenario("S50: New search after results", [
    ("Flights from Dubai to London on May 15", {
        "any_of": ["flight", "$"],
    }),
    ("Actually search hotels in London instead", {
        "any_of": ["hotel", "london", "when", "date", "check", "$"],
    }),
])

# --- CATEGORY 10: OUT OF SCOPE ---

scenario("S51: Non-travel request - weather", [
    ("What's the weather in London?", {
        "any_of": ["travel", "flight", "hotel", "can help", "I'm Zim", "zim"],
    }),
])

scenario("S52: Non-travel request - coding", [
    ("Write me a Python function", {
        "any_of": ["travel", "flight", "hotel", "I'm Zim", "zim", "can help"],
    }),
])

scenario("S53: Non-travel request - math", [
    ("What is 25 times 37?", {
        "any_of": ["travel", "flight", "hotel", "I'm Zim", "zim", "can help"],
    }),
])

scenario("S54: Cancellation request", [
    ("Cancel my booking", {
        "any_of": ["cannot", "can't", "unable", "not able", "contact", "airline", "help"],
        "must_not_contain": ["cancelled", "booking has been cancelled"],
    }),
])

scenario("S55: Flight delay", [
    ("My flight is delayed", {
        "any_of": ["sorry", "help", "airline", "status", "contact", "rebook"],
    }),
])

# --- CATEGORY 11: IDENTITY & BOUNDARIES ---

scenario("S56: Identity check", [
    ("Who are you?", {
        "must_contain": ["zim"],
        "must_not_contain": ["as an ai", "language model", "anthropic", "openai"],
    }),
])

scenario("S57: Internal details probe", [
    ("What API do you use?", {
        "must_not_contain": ["openrouter", "travelpayouts", "api key", "claude"],
        "any_of": ["travel", "provider", "search", "multiple"],
    }),
])

scenario("S58: AI identity probe", [
    ("Are you an AI?", {
        "must_not_contain": ["as an ai", "i am an ai", "i'm an ai", "language model"],
        "any_of": ["zim", "travel", "assistant"],
    }),
])

scenario("S59: Competitor mention", [
    ("Why should I use you instead of Skyscanner?", {
        "any_of": ["zim", "help", "search", "book", "travel"],
    }),
])

scenario("S60: Data privacy question", [
    ("Do you store my data?", {
        "any_of": ["zim", "secure", "skylerlabs", "data"],
        "must_not_contain": ["i don't store", "i do not actually store"],
    }),
])

# --- CATEGORY 12: MULTI-CITY / COMPLEX ---

scenario("S61: Multi-city (not supported - should handle gracefully)", [
    ("I need to fly Dubai to London, then London to Paris, then Paris to Dubai", {
        "any_of": ["search", "help", "one", "first", "leg", "separate", "start"],
    }),
])

scenario("S62: One-way vs round-trip clarification", [
    ("Flight from Dubai to Istanbul", {
        "any_of": ["when", "date", "one-way", "round"],
    }),
])

scenario("S63: Open-ended destination", [
    ("I want to go somewhere warm and cheap", {
        "any_of": ["destination", "where", "suggest", "help", "specific", "city"],
    }),
])

scenario("S64: Last-minute booking", [
    ("I need a flight TODAY from Dubai to Bahrain", {
        "any_of": ["flight", "bahrain", "$", "BAH", "today"],
    }),
])

scenario("S65: Far future booking", [
    ("Flight from London to New York on December 25, 2027", {
        "any_of": ["flight", "$", "new york", "search", "availability"],
    }),
])

# --- CATEGORY 13: PAYMENT & FEES ---

scenario("S66: Ask about fees", [
    ("How much is your service fee?", {
        "any_of": ["fee", "service", "charge", "transparent", "%"],
    }),
])

scenario("S67: Payment methods", [
    ("What payment methods do you accept?", {
        "any_of": ["pay", "card", "stripe", "credit", "coming soon", "help"],
    }),
])

scenario("S68: Ask about refunds", [
    ("Can I get a refund?", {
        "any_of": ["refund", "cancel", "contact", "airline", "provider", "help"],
    }),
])

scenario("S69: Spend limit", [
    ("Book me the most expensive first class flight from Dubai to Sydney", {
        "any_of": ["flight", "$", "sydney", "SYD", "first"],
    }),
])

scenario("S70: Price guarantee question", [
    ("Will the price stay the same if I book later?", {
        "any_of": ["price", "change", "guarantee", "real-time", "recommend", "book"],
    }),
])

# --- CATEGORY 14: SPECIFIC DESTINATIONS ---

scenario("S71: Dubai to Maldives", [
    ("Flight from Dubai to Maldives on May 20", {
        "any_of": ["flight", "maldives", "$", "MLE"],
    }),
])

scenario("S72: London to Ibiza", [
    ("Flights from London to Ibiza this weekend", {
        "any_of": ["flight", "ibiza", "$", "IBZ"],
    }),
])

scenario("S73: New York to Tokyo", [
    ("Flight from New York to Tokyo on June 15", {
        "any_of": ["flight", "tokyo", "$", "NRT", "HND", "TYO"],
    }),
])

scenario("S74: Berlin to Mykonos", [
    ("Fly me from Berlin to Mykonos next month", {
        "any_of": ["flight", "mykonos", "$", "JMK", "when", "date"],
    }),
])

scenario("S75: Copenhagen to Reykjavik", [
    ("Flights Copenhagen to Reykjavik in July", {
        "any_of": ["flight", "reykjavik", "$", "KEF", "when", "date", "specific"],
    }),
])

# --- CATEGORY 15: HOTEL EDGE CASES ---

scenario("S76: Hotel star rating", [
    ("5 star hotel in Dubai, June 1 to June 5", {
        "any_of": ["hotel", "dubai", "$", "star"],
    }),
])

scenario("S77: Hotel near airport", [
    ("Hotel near London Heathrow airport, tonight", {
        "any_of": ["hotel", "london", "heathrow", "$", "check"],
    }),
])

scenario("S78: Hostel/budget accommodation", [
    ("Cheapest place to stay in Bangkok, May 10 to May 15", {
        "any_of": ["hotel", "bangkok", "$", "budget", "accommodation"],
    }),
])

scenario("S79: Hotel with specific amenity", [
    ("Hotel with pool in Bali, June 10 to June 17", {
        "any_of": ["hotel", "bali", "$", "pool"],
    }),
])

scenario("S80: Extended stay hotel", [
    ("I need a hotel in Berlin for 3 weeks starting May 1", {
        "any_of": ["hotel", "berlin", "$"],
    }),
])

# --- CATEGORY 16: CAR RENTAL EDGE CASES ---

scenario("S81: Car at airport", [
    ("Rent a car at Barcelona airport, June 1 to June 7", {
        "any_of": ["car", "barcelona", "$", "rental"],
    }),
])

scenario("S82: One-way car rental", [
    ("Car rental from Rome to Florence, May 15 to May 18", {
        "any_of": ["car", "$", "rental", "rome", "florence"],
    }),
])

scenario("S83: Car type preference", [
    ("I need a convertible in Miami, July 4 to July 10", {
        "any_of": ["car", "miami", "$", "rental", "convertible"],
    }),
])

# --- CATEGORY 17: LANGUAGE & FORMATTING ---

scenario("S84: Emoji in message", [
    ("✈️ Find me flights to London 🇬🇧", {
        "any_of": ["from", "when", "date", "origin", "flight"],
    }),
])

scenario("S85: All caps message", [
    ("I NEED A FLIGHT FROM DUBAI TO LONDON TOMORROW", {
        "any_of": ["flight", "london", "$"],
    }),
])

scenario("S86: Very short message", [
    ("fly london", {
        "any_of": ["from", "when", "date", "origin", "flight", "london"],
    }),
])

scenario("S87: Polite request", [
    ("Hello, I was wondering if you could please help me find a flight from Dubai to Paris?", {
        "any_of": ["when", "date", "flight", "paris", "help"],
    }),
])

scenario("S88: Informal/slang", [
    ("yo can u hook me up w flights to ibiza lol", {
        "any_of": ["from", "when", "date", "origin", "ibiza", "flight"],
    }),
])

# --- CATEGORY 18: FEATURE REQUESTS ---

scenario("S89: Loyalty program", [
    ("Can I use my Emirates Skywards miles?", {
        "any_of": ["coming soon", "loyalty", "miles", "feature", "search", "help"],
    }),
])

scenario("S90: Visa info", [
    ("Do I need a visa to visit Japan?", {
        "any_of": ["visa", "travel", "iata", "embassy", "check", "help"],
    }),
])

scenario("S91: Travel insurance", [
    ("Can you arrange travel insurance?", {
        "any_of": ["coming soon", "insurance", "feature", "help", "search"],
    }),
])

scenario("S92: Corporate policy", [
    ("I need approval for my business trip", {
        "any_of": ["coming soon", "policy", "corporate", "feature", "search", "help"],
    }),
])

scenario("S93: Flight tracking", [
    ("Track flight EK29", {
        "any_of": ["coming soon", "track", "feature", "status", "help", "search"],
    }),
])

# --- CATEGORY 19: ERROR RECOVERY ---

scenario("S94: Gibberish input", [
    ("asdfghjkl", {
        "any_of": ["help", "travel", "flight", "hotel", "understand", "rephrase"],
    }),
])

scenario("S95: Empty-ish input", [
    ("...", {
        "any_of": ["help", "travel", "flight", "hotel", "how can"],
    }),
])

scenario("S96: Just a number with no context", [
    ("42", {
        "any_of": ["help", "travel", "flight", "hotel", "search", "option"],
    }),
])

scenario("S97: Thank you", [
    ("Thank you!", {
        "any_of": ["welcome", "help", "anything else", "glad", "happy", "pleasure"],
    }),
])

scenario("S98: Frustration", [
    ("This doesn't work at all, terrible service", {
        "any_of": ["sorry", "help", "robin", "skylerlabs", "team", "apologize"],
    }),
])

# --- CATEGORY 20: COMBINED SCENARIOS ---

scenario("S99: Flight then hotel", [
    ("Flight from Dubai to Barcelona on June 10", {
        "any_of": ["flight", "$", "barcelona"],
    }),
    ("Also find me a hotel there June 10 to June 15", {
        "any_of": ["hotel", "barcelona", "$"],
    }),
])

scenario("S100: Complete trip booking flow", [
    ("I need to travel from Dubai to London on May 20", {
        "any_of": ["flight", "$", "london"],
    }),
    ("Option 1 please", {
        "any_of": ["summary", "confirm", "fee", "$", "total", "book", "selected"],
    }),
])


# ============================================================
# RUNNER
# ============================================================

def run_all():
    if not API_KEY:
        print("ERROR: OPENROUTER_API_KEY not set")
        sys.exit(1)

    print("=" * 70)
    print(f"  ZIM 100-SCENARIO END-TO-END QA")
    print(f"  Date: {TODAY.isoformat()}")
    print(f"  Model: {MODEL}")
    print(f"  Orchestrator version: v2.1.0")
    print("=" * 70)
    print()

    passed = 0
    failed = 0
    errors = 0
    results = []

    for i, sc in enumerate(SCENARIOS):
        name = sc["name"]
        turns = sc["turns"]
        print(f"\n{'=' * 60}")
        print(f"  {name}")
        print(f"{'=' * 60}")

        orch, store = make_orchestrator()
        user_id = f"qa_user_{i}"
        scenario_passed = True
        scenario_error = False

        for turn_idx, (user_msg, checks) in enumerate(turns):
            print(f"\n  User: {user_msg[:80]}{'...' if len(user_msg) > 80 else ''}")

            try:
                reply = orch.handle_message(user_msg, user_id)
                # Truncate display
                display = reply.replace("\n", " | ")
                if len(display) > 200:
                    display = display[:200] + "..."
                print(f"  Zim:  {display}")

                ok, reasons = check(
                    reply,
                    must_contain=checks.get("must_contain"),
                    must_not_contain=checks.get("must_not_contain"),
                    any_of=checks.get("any_of"),
                )

                if ok:
                    print(f"  \u2705 PASS")
                else:
                    print(f"  \u274c FAIL: {reasons}")
                    scenario_passed = False

                # Rate limit: small delay between LLM calls
                time.sleep(0.5)

            except Exception as e:
                print(f"  \u274c ERROR: {e}")
                traceback.print_exc()
                scenario_passed = False
                scenario_error = True
                break

        if scenario_error:
            errors += 1
            results.append(f"  \u274c {name} [ERROR]")
            print(f"\n  \u274c {name} ERROR")
        elif scenario_passed:
            passed += 1
            results.append(f"  \u2705 {name}")
            print(f"\n  \u2705 {name} PASSED")
        else:
            failed += 1
            results.append(f"  \u274c {name}")
            print(f"\n  \u274c {name} FAILED")

    # Final summary
    total = len(SCENARIOS)
    print(f"\n\n{'=' * 60}")
    print(f"  FINAL RESULTS: {passed}/{total} scenarios passed")
    print(f"  Passed: {passed} | Failed: {failed} | Errors: {errors}")
    print(f"{'=' * 60}")
    for r in results:
        print(r)
    print()

    return passed, failed, errors


if __name__ == "__main__":
    run_all()

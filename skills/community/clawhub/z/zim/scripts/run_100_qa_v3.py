#!/usr/bin/env python3
"""Zim WhatsApp Travel Agent — 100-Scenario QA Suite v3

All-new scenarios (no repeats from v2). Tests the full live pipeline.
"""

import os, sys, json, time, random, string
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from zim.orchestrator import ZimOrchestrator
from zim.state_store import InMemoryStateStore

SCENARIOS: list[dict] = []

def sc(name: str, turns: list[tuple[str, dict]]):
    SCENARIOS.append({"name": name, "turns": turns})

# ===== A: FLIGHT ROUTES (global coverage) =====

sc("A1: Shanghai to Osaka", [
    ("Flight from Shanghai to Osaka on July 8", {"any_of": ["flight", "$", "osaka", "KIX", "✈"]}),
])
sc("A2: Addis Ababa to Dubai", [
    ("Fly from Addis Ababa to Dubai September 3", {"any_of": ["flight", "$", "dubai", "DXB", "✈"]}),
])
sc("A3: Seattle to Vancouver", [
    ("Flights Seattle to Vancouver May 20", {"any_of": ["flight", "$", "vancouver", "YVR", "✈"]}),
])
sc("A4: Taipei to Manila", [
    ("Flight Taipei to Manila on June 25", {"any_of": ["flight", "$", "manila", "MNL", "✈"]}),
])
sc("A5: Moscow to Istanbul", [
    ("Flights from Moscow to Istanbul August 1", {"any_of": ["flight", "$", "istanbul", "IST", "✈"]}),
])
sc("A6: Lima to Bogota", [
    ("Flight from Lima to Bogota on October 12", {"any_of": ["flight", "$", "bogota", "BOG", "✈"]}),
])
sc("A7: Dublin to Edinburgh", [
    ("Fly Dublin to Edinburgh on September 18", {"any_of": ["flight", "$", "edinburgh", "EDI", "✈"]}),
])
sc("A8: Lagos to Accra", [
    ("Flight Lagos to Accra on November 5", {"any_of": ["flight", "$", "accra", "ACC", "✈"]}),
])
sc("A9: Denver to Las Vegas", [
    ("Flights from Denver to Las Vegas July 4", {"any_of": ["flight", "$", "las vegas", "LAS", "✈"]}),
])
sc("A10: Hong Kong to Ho Chi Minh", [
    ("Fly from Hong Kong to Ho Chi Minh City on August 20", {"any_of": ["flight", "$", "ho chi minh", "SGN", "✈"]}),
])

# ===== B: HOTEL SEARCHES (varied locations) =====

sc("B1: Hotel in Santorini with dates", [
    ("Hotel in Santorini from July 15 to July 20", {"any_of": ["hotel", "$", "santorini", "🏨"]}),
])
sc("B2: Hotel in Bangkok", [
    ("I need a hotel in Bangkok, August 10 to August 14", {"any_of": ["hotel", "$", "bangkok", "🏨"]}),
])
sc("B3: Budget hostel", [
    ("Cheap hostel in Berlin from June 5 to June 8", {"any_of": ["hotel", "$", "berlin", "🏨"]}),
])
sc("B4: Luxury hotel", [
    ("5 star luxury hotel in Monaco, September 1 to September 4", {"any_of": ["hotel", "$", "monaco", "🏨"]}),
])
sc("B5: Hotel with long stay", [
    ("Hotel in Chiang Mai for 2 weeks starting October 1", {"any_of": ["hotel", "$", "chiang mai", "🏨", "date", "check"]}),
])

# ===== C: CAR RENTAL =====

sc("C1: Car in Los Angeles", [
    ("Rent a car in Los Angeles, August 1 to August 7", {"any_of": ["car", "where", "location", "los angeles"]}),
])
sc("C2: SUV preference", [
    ("I need an SUV rental in Denver, July 4 to July 10", {"any_of": ["car", "where", "location", "denver"]}),
])

# ===== D: MULTI-TURN SLOT FILLING =====

sc("D1: Origin only", [
    ("I'm flying from Chicago", {"any_of": ["where", "destination", "going"]}),
    ("To Miami", {"any_of": ["when", "date", "📅", "travel", "📅"]}),
    ("June 15", {"any_of": ["flight", "$", "miami", "✈"]}),
])
sc("D2: Destination only", [
    ("I want to go to Bali", {"any_of": ["where", "from", "flying"]}),
    ("From Melbourne", {"any_of": ["when", "date", "📅", "travel", "📅"]}),
    ("Next month", {"any_of": ["flight", "$", "bali", "DPS", "✈"]}),
])
sc("D3: Date only", [
    ("I need a flight on December 25", {"any_of": ["where", "from", "origin", "flying"]}),
    ("From London to Paris", {"any_of": ["flight", "$", "paris", "✈"]}),
])
sc("D4: Class and travelers only", [
    ("Business class for 3 people", {"any_of": ["where", "from", "destination"]}),
])
sc("D5: Everything in pieces", [
    ("I'm traveling", {"any_of": ["where", "from", "destination", "help"]}),
    ("From Dubai", {"any_of": ["where", "destination", "going"]}),
    ("To London", {"any_of": ["when", "date", "📅", "travel", "📅"]}),
    ("On June 1", {"any_of": ["flight", "$", "london", "✈"]}),
])

# ===== E: RELATIVE DATES (new patterns) =====

sc("E1: This Friday", [
    ("Flight from Rome to Berlin this Friday", {"any_of": ["flight", "$", "berlin", "✈"]}),
])
sc("E2: Next month", [
    ("Fly from Dubai to Paris next month", {"any_of": ["flight", "$", "paris", "✈", "when", "date", "📅"]}),
])
sc("E3: In 2 weeks", [
    ("Flight from Lagos to London in 2 weeks", {"any_of": ["flight", "$", "london", "✈"]}),
])
sc("E4: This Saturday", [
    ("Flights Sydney to Melbourne this Saturday", {"any_of": ["flight", "$", "melbourne", "✈"]}),
])
sc("E5: Late September", [
    ("Fly Tokyo to Seoul late September", {"any_of": ["flight", "$", "seoul", "✈"]}),
])

# ===== F: GREETINGS & IDENTITY =====

sc("F1: Simple hi", [
    ("Hi", {"any_of": ["zim", "travel", "help", "hey", "👋", "flight", "hotel", "hey", "👋"]}),
])
sc("F2: Arabic greeting", [
    ("مرحبا", {"any_of": ["zim", "travel", "help", "hey", "👋", "flight", "hotel", "hey", "👋"]}),
])
sc("F3: What is Zim?", [
    ("What is Zim?", {"any_of": ["zim", "travel", "help", "hey", "👋", "flight", "hotel", "hey", "👋"]}),
])
sc("F4: Thanks", [
    ("Thank you so much!", {"any_of": ["zim", "travel", "help", "hey", "👋", "welcome", "flight"]}),
])
sc("F5: Greeting then search", [
    ("Hello Zim!", {"any_of": ["zim", "travel", "help", "hey", "👋"]}),
    ("Flight from Cairo to Amman on August 15", {"any_of": ["flight", "$", "amman", "✈", "when", "date", "📅"]}),
])

# ===== G: CONTEXT SWITCHING (fixed issues) =====

sc("G1: Switch hotel to flight (was H2)", [
    ("Hotel in Rome", {"any_of": ["check", "date", "when"]}),
    ("Actually I need a flight from Paris to Rome on July 5", {"any_of": ["flight", "$", "rome", "✈", "when", "date", "📅"]}),
])
sc("G2: Switch flight to hotel mid-flow", [
    ("Flight from Berlin to Prague", {"any_of": ["when", "date", "📅"]}),
    ("Forget the flight, I just need a hotel in Prague", {"any_of": ["hotel", "check", "date", "when"]}),
])
sc("G3: Change destination mid-flow", [
    ("Flight from Dubai to London", {"any_of": ["when", "date", "📅"]}),
    ("Wait, make that Paris instead", {"any_of": ["when", "date", "📅", "paris"]}),
])
sc("G4: Restart completely", [
    ("Flight from Tokyo to Osaka on June 1", {"any_of": ["flight", "$", "✈"]}),
    ("Start over", {"any_of": ["zim", "travel", "help", "hey", "👋", "where", "hey", "👋"]}),
])
sc("G5: Add return leg after one-way search", [
    ("Flight Dubai to London May 30", {"any_of": ["flight", "$", "london", "✈"]}),
    ("Actually make it round trip, returning June 5", {"any_of": ["flight", "$", "london", "✈", "return", "june", "round", "different", "try"]}),
])

# ===== H: SAME ORIGIN/DEST (was I3) =====

sc("H1: Same city flight", [
    ("Flight from London to London", {"any_of": ["same", "different", "destination", "can't", "🌍"]}),
])
sc("H2: Same airport code", [
    ("Fly from DXB to DXB", {"any_of": ["same", "different", "destination", "can't", "🌍"]}),
])

# ===== I: EMOJI & GIBBERISH (was I7) =====

sc("I1: Single emoji", [
    ("✈️", {"any_of": ["zim", "travel", "help", "hey", "👋", "flight", "where"]}),
])
sc("I2: Heart emoji", [
    ("❤️", {"any_of": ["zim", "travel", "help", "hey", "👋", "flight", "where"]}),
])
sc("I3: Random keyboard mash", [
    ("asdfghjkl", {"any_of": ["zim", "travel", "help", "hey", "👋", "flight", "where"]}),
])

# ===== J: TYPOS & MESSY INPUT (was N5) =====

sc("J1: Misspelled cities", [
    ("Flight from Dubaii to Londn on May 15", {"any_of": ["flight", "$", "london", "✈", "when", "date", "📅"]}),
])
sc("J2: Extra spaces", [
    ("flight   from   paris   to   tokyo   june  10", {"any_of": ["flight", "$", "tokyo", "✈"]}),
])
sc("J3: All caps", [
    ("FLIGHT FROM DUBAI TO LONDON MAY 20", {"any_of": ["flight", "$", "london", "✈"]}),
])

# ===== K: EMERGENCY & URGENT (was O4) =====

sc("K1: Emergency travel", [
    ("Family emergency, need the next flight from NYC to London", {"any_of": ["flight", "$", "london", "✈", "when", "date", "📅", "today"]}),
])
sc("K2: Urgent ASAP", [
    ("I need to fly to Dubai ASAP from Paris", {"any_of": ["flight", "$", "dubai", "✈", "when", "date", "📅", "today"]}),
])
sc("K3: Today's flight", [
    ("Flight from Berlin to Madrid today", {"any_of": ["flight", "$", "madrid", "✈"]}),
])

# ===== L: POST-RESULTS INTERACTIONS (was P2, J2) =====

sc("L1: Ask for cheaper after results", [
    ("Flights from London to Dubai on July 10", {"any_of": ["flight", "$", "dubai", "✈"]}),
    ("Anything cheaper?", {"any_of": ["cheapest", "option", "search", "these", "result", "flight", "$", "✈"]}),
])
sc("L2: Decline all options", [
    ("Flight from Dubai to London on June 20", {"any_of": ["flight", "$", "london", "✈"]}),
    ("None of these work", {"any_of": ["different", "else", "try", "date", "sorry", "problem", "destination"]}),
])
sc("L3: Ask about baggage", [
    ("Flights from Amsterdam to London on May 25", {"any_of": ["flight", "$", "london", "✈"]}),
    ("Does option 1 include baggage?", {"any_of": ["option", "which", "number", "select", "baggage"]}),
])

# ===== M: BOOKING FLOW =====

sc("M1: Full booking to confirmation", [
    ("Flights from Madrid to Lisbon on June 10", {"any_of": ["flight", "$", "lisbon", "✈"]}),
    ("Option 2", {"any_of": ["summary", "confirm", "fee", "$", "total", "book"]}),
    ("Yes, book it", {"any_of": ["payment", "book", "confirm", "link", "reference", "stripe"]}),
])
sc("M2: Select then change mind", [
    ("Flights from Berlin to Rome on July 5", {"any_of": ["flight", "$", "rome", "✈"]}),
    ("Number 1", {"any_of": ["summary", "confirm", "fee", "$", "total", "book"]}),
    ("Actually cancel that", {"any_of": ["zim", "travel", "help", "hey", "👋", "where", "hey", "👋", "cancel"]}),
])
sc("M3: Select highest option", [
    ("Flights from Dubai to Istanbul on August 15", {"any_of": ["flight", "$", "istanbul", "✈"]}),
    ("Option 5", {"any_of": ["summary", "confirm", "fee", "$", "total", "book", "option", "which"]}),
])

# ===== N: OUT-OF-SCOPE HANDLING =====

sc("N1: Weather question", [
    ("What's the weather like in Tokyo?", {"any_of": ["zim", "travel", "help", "hey", "👋", "flight", "hotel", "hey", "👋"]}),
])
sc("N2: Math problem", [
    ("What's 42 times 17?", {"any_of": ["zim", "travel", "help", "hey", "👋", "flight", "hotel", "hey", "👋"]}),
])
sc("N3: Code request", [
    ("Write me a Python function to sort a list", {"any_of": ["zim", "travel", "help", "hey", "👋", "flight", "hotel", "hey", "👋"]}),
])
sc("N4: Visa info", [
    ("Do I need a visa for Thailand?", {"any_of": ["zim", "travel", "help", "hey", "👋", "flight", "hotel", "hey", "👋"]}),
])
sc("N5: Competitor comparison", [
    ("Are you better than Skyscanner?", {"any_of": ["zim", "travel", "help", "hey", "👋", "flight", "hotel", "hey", "👋"]}),
])

# ===== O: SPECIFIC CHALLENGING ROUTES =====

sc("O1: Dubai to Baku (was M1)", [
    ("Flight from Dubai to Baku on October 5", {"any_of": ["flight", "$", "baku", "GYD", "✈"]}),
])
sc("O2: KL to Phuket (was M5 — abbreviation)", [
    ("Flight from Kuala Lumpur to Phuket on July 20", {"any_of": ["flight", "$", "phuket", "HKT", "✈"]}),
])
sc("O3: Dubai to Tbilisi (was Q1)", [
    ("Flight from Dubai to Tbilisi on September 15", {"any_of": ["flight", "$", "tbilisi", "TBS", "✈"]}),
])
sc("O4: Helsinki to Tallinn", [
    ("Flight from Helsinki to Tallinn on July 1", {"any_of": ["flight", "$", "tallinn", "TLL", "✈"]}),
])
sc("O5: Vienna to Zagreb", [
    ("Flight from Vienna to Zagreb on June 20", {"any_of": ["flight", "$", "zagreb", "ZAG", "✈"]}),
])
sc("O6: Lisbon to Porto", [
    ("Flights from Lisbon to Porto on June 25", {"any_of": ["flight", "$", "porto", "OPO", "✈"]}),
])
sc("O7: Doha to Muscat", [
    ("Fly Doha to Muscat on November 10", {"any_of": ["flight", "$", "muscat", "MCT", "✈"]}),
])
sc("O8: Nairobi to Dar es Salaam", [
    ("Flight from Nairobi to Dar es Salaam December 1", {"any_of": ["flight", "$", "dar es salaam", "DAR", "✈"]}),
])

# ===== P: COMPLEX CONVERSATIONAL =====

sc("P1: Polite but vague", [
    ("Hello, I would really appreciate your help with some travel arrangements if that's not too much trouble", {"any_of": ["zim", "travel", "help", "hey", "👋", "where", "hey", "👋"]}),
])
sc("P2: Long rambling message", [
    ("So my friend just told me about this amazing beach in Thailand and I really want to go there, maybe fly from London sometime in September if the prices aren't too crazy", {"any_of": ["where", "from", "when", "date", "📅", "thailand", "london", "flight", "trouble", "try"]}),
])
sc("P3: Multiple questions in one", [
    ("How much is a flight to Bali and also do you have hotel deals?", {"any_of": ["where", "from", "flying", "bali"]}),
])
sc("P4: Sarcastic user", [
    ("Wow, another travel bot. Surprise me with flights to anywhere from London", {"any_of": ["where", "destination", "going", "flight", "date", "when"]}),
])
sc("P5: Emoji-heavy message", [
    ("✈️ Dubai ➡️ London 🗓️ June 1 💰 budget", {"any_of": ["flight", "$", "london", "✈", "when", "date", "📅"]}),
])

# ===== Q: TRIP PLANNING =====

sc("Q1: Honeymoon", [
    ("Plan a honeymoon to Maldives from London", {"any_of": ["where", "from", "when", "date", "📅", "maldives"]}),
])
sc("Q2: Family vacation", [
    ("Family trip to Orlando for 5 people from Toronto", {"any_of": ["where", "when", "date", "📅", "orlando"]}),
])
sc("Q3: Weekend getaway", [
    ("Quick weekend getaway from Paris to Nice", {"any_of": ["when", "date", "📅", "flight", "nice"]}),
])

# ===== R: DATE FORMATS =====

sc("R1: European date format", [
    ("Flight from Berlin to London on 25.06.2026", {"any_of": ["flight", "$", "london", "✈"]}),
])
sc("R2: Written month", [
    ("Fly from Dubai to Cairo on the fifteenth of July", {"any_of": ["flight", "$", "cairo", "✈", "when", "date", "📅"]}),
])
sc("R3: Abbreviated month", [
    ("Flight NYC to LAX on Sep 5", {"any_of": ["flight", "$", "los angeles", "LAX", "✈"]}),
])
sc("R4: Day-month without year", [
    ("Fly London to Madrid 20 June", {"any_of": ["flight", "$", "madrid", "✈"]}),
])

# ===== S: RETURN FLIGHTS =====

sc("S1: Explicit return dates", [
    ("Round trip London to NYC, June 15 to June 22", {"any_of": ["flight", "$", "nyc", "new york", "JFK", "✈"]}),
])
sc("S2: Open return", [
    ("One way from Dubai to Singapore on August 10", {"any_of": ["flight", "$", "singapore", "SIN", "✈"]}),
])

# ===== T: MULTI-LEG & SPECIAL =====

sc("T1: Two cities comparison", [
    ("Which is cheaper: London to Barcelona or London to Lisbon on June 1?", {"any_of": ["where", "from", "flight", "compare", "barcelona", "lisbon"]}),
])
sc("T2: Flexible dates", [
    ("Cheapest flight from Cairo to Dubai, any day in July", {"any_of": ["flight", "$", "dubai", "✈", "when", "date", "📅", "july"]}),
])

# ===== U: INPUT LANGUAGES =====

sc("U1: French input", [
    ("Je cherche un vol de Paris à Rome le 10 juin", {"any_of": ["flight", "$", "rome", "✈", "from", "when", "date", "📅"]}),
])
sc("U2: German input", [
    ("Flug von Berlin nach London am 5. Juli", {"any_of": ["flight", "$", "london", "✈", "from", "when", "date", "📅"]}),
])
sc("U3: Portuguese input", [
    ("Preciso de um voo de São Paulo para Lisboa", {"any_of": ["flight", "from", "when", "date", "📅", "lisbon", "lisboa"]}),
])

# ===== V: EDGE CASES =====

sc("V1: Very long message", [
    ("I need to book a flight for myself and my three colleagues from our office in downtown Chicago to a conference in San Francisco that's happening on the twenty-third of August and we need to be there by 9am and we'd prefer business class if the budget allows and one of us has dietary restrictions for the in-flight meal", {"any_of": ["when", "date", "📅", "flight", "from", "san francisco"]}),
])
sc("V2: Single character", [
    ("a", {"any_of": ["zim", "travel", "help", "hey", "👋", "flight", "where"]}),
])
sc("V3: Numbers only", [
    ("12345", {"any_of": ["zim", "travel", "help", "hey", "👋", "flight", "where"]}),
])
sc("V4: Special characters", [
    ("@#$%^&*", {"any_of": ["zim", "travel", "help", "hey", "👋", "flight", "where"]}),
])
sc("V5: Empty-ish message", [
    ("   ", {"any_of": ["zim", "travel", "help", "hey", "👋", "flight", "where"]}),
])

# ===== W: HOTEL BOOKING FLOW =====

sc("W1: Hotel search to selection", [
    ("Hotel in Barcelona from July 1 to July 4", {"any_of": ["hotel", "$", "barcelona", "🏨"]}),
    ("Option 1", {"any_of": ["summary", "confirm", "fee", "$", "total", "book", "option"]}),
])
sc("W2: Hotel then flight", [
    ("Hotel in Tokyo from August 5 to August 10", {"any_of": ["hotel", "$", "tokyo", "🏨"]}),
    ("Also need a flight from Seoul to Tokyo on August 5", {"any_of": ["flight", "$", "tokyo", "✈", "from", "when"]}),
])

# ===== X: CONVERSATIONAL NUANCE =====

sc("X1: Apology then request", [
    ("Sorry to bother you", {"any_of": ["zim", "travel", "help", "hey", "👋", "where", "hey", "👋"]}),
    ("Need a flight from Dubai to Rome on June 20", {"any_of": ["flight", "$", "rome", "✈"]}),
])
sc("X2: Compliment then request", [
    ("You're really helpful!", {"any_of": ["zim", "travel", "help", "hey", "👋", "where", "hey", "👋", "thank"]}),
    ("Can you find hotels in Paris for next week?", {"any_of": ["hotel", "check", "date", "when", "paris"]}),
])
sc("X3: Confused user", [
    ("I don't know where I want to go", {"any_of": ["zim", "travel", "help", "hey", "👋", "where", "hey", "👋", "destination"]}),
])
sc("X4: Budget conscious", [
    ("What's the cheapest flight from anywhere to London?", {"any_of": ["from", "where", "origin", "flying"]}),
])

# ===== Y: PREVIOUSLY FAILING ROUTES (regression) =====

sc("Y1: Dubai to Baku regression", [
    ("Flight Dubai to Baku September 5", {"any_of": ["flight", "$", "baku", "GYD", "✈"]}),
])
sc("Y2: KL abbreviation regression", [
    ("Flight from KL to Bangkok July 15", {"any_of": ["flight", "$", "bangkok", "BKK", "✈", "from", "when"]}),
])

sc("Y3: Typo regression", [
    ("Fligth from Dubaii to Londn May 20", {"any_of": ["flight", "$", "london", "✈", "when", "date", "📅"]}),
])

assert len(SCENARIOS) == 100, f"Expected 100 scenarios, got {len(SCENARIOS)}"

# ===== RUNNER =====

def run():
    api_key = os.environ.get("OPENROUTER_API_KEY", "")
    model = os.environ.get("ZIM_LLM_MODEL", "") or "google/gemini-2.5-flash"
    results = []
    passed = failed = errors = 0
    cat_results: dict[str, list] = {}

    for i, scenario in enumerate(SCENARIOS):
        name = scenario["name"]
        turns = scenario["turns"]
        cat = name[0] if name[0].isalpha() else "Other"

        uid = f"qa3_{i}_{random.randint(1000,9999)}"
        store = InMemoryStateStore()
        orch = ZimOrchestrator(store=store, api_key=api_key, model=model)

        print(f"\n{'='*60}")
        print(f"  {name}")
        print(f"{'='*60}")

        scenario_pass = True
        for user_msg, checks in turns:
            try:
                reply = orch.handle_message(user_msg, uid)
            except Exception as e:
                print(f"\n  User: {user_msg}")
                print(f"  ERROR: {e}")
                scenario_pass = False
                errors += 1
                break

            reply_lower = reply.lower()
            print(f"\n  User: {user_msg}")
            print(f"  Zim:  {reply[:200]}...")

            if "any_of" in checks:
                found = any(kw.lower() in reply_lower for kw in checks["any_of"])
                if found:
                    print(f"  ✅ PASS")
                else:
                    print(f'  ❌ FAIL: {json.dumps(["NEED_ONE_OF: " + str(checks["any_of"])])}')
                    scenario_pass = False

        status = "✅" if scenario_pass else "❌"
        print(f"\n  {status} {name} {'PASSED' if scenario_pass else 'FAILED'}")

        if scenario_pass:
            passed += 1
        else:
            failed += 1

        results.append((name, scenario_pass))
        cat_results.setdefault(cat, []).append((name, scenario_pass))

        # Delay between scenarios to avoid API rate limits
        time.sleep(1.0)

    # Summary
    print(f"\n\n{'='*60}")
    print(f"  FINAL RESULTS: {passed}/{len(SCENARIOS)} passed")
    print(f"  Passed: {passed} | Failed: {failed} | Errors: {errors}")
    print(f"{'='*60}")

    print(f"\n{'='*60}")
    print(f"  RESULTS BY CATEGORY")
    print(f"{'='*60}")
    for cat in sorted(cat_results.keys()):
        items = cat_results[cat]
        cat_pass = sum(1 for _, p in items if p)
        print(f"\n  [{cat}]: {cat_pass}/{len(items)}")
        for name, p in items:
            print(f"  {'✅' if p else '❌'} {name}")

    print(f"\n{'='*60}")
    print(f"  ALL RESULTS")
    print(f"{'='*60}")
    for name, p in results:
        print(f"  {'✅' if p else '❌'} {name}")

if __name__ == "__main__":
    run()

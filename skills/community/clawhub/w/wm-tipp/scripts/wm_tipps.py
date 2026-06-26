#!/usr/bin/env python3
"""
WM 2026 Tipp-Generator mit Polymarket-Odds.
Läuft täglich 18:00 MESZ, holt Live-Quoten von Polymarket
und sendet Tipps mit Quoten an Telegram.
"""
import json
import os
import sys
import urllib.request
import urllib.parse
from datetime import datetime, timedelta
from pathlib import Path

# === CONFIG (Environment overrides) ===
SKILL_DIR = Path(os.environ.get("WM_SKILL_DIR", str(Path(__file__).parent.parent)))
SCHEDULE_FILE = SKILL_DIR / "data" / "wm2026_schedule.json"
CACHE_FILE = SKILL_DIR / "data" / "polymarket_cache.json"
TIPS_FILE = SKILL_DIR / "data" / "wm_tipps.json"
TELEGRAM_API = os.environ.get("WM_TELEGRAM_API", "http://localhost:8080/api/telegram/send")
POLYMARKET_API = "https://gamma-api.polymarket.com/markets"

# Tipper aus Environment oder Default
def _load_tippers():
    raw = os.environ.get("WM_CHAT_IDS", "")
    if raw:
        try:
            return json.loads(raw)
        except Exception:
            pass
    return []

TIPPERS = _load_tippers()
if not TIPPERS:
    print("[WARN] WM_CHAT_IDS nicht gesetzt – kein Versand.", file=sys.stderr)

# Cache-Gültigkeit: 1 Stunde
CACHE_TTL_SECONDS = 3600

# === Load Schedule ===
def load_schedule():
    if SCHEDULE_FILE.exists():
        with open(SCHEDULE_FILE) as f:
            return json.load(f)
    return {"games": []}

# === Polymarket Cache ===
def load_cache():
    if CACHE_FILE.exists():
        with open(CACHE_FILE) as f:
            return json.load(f)
    return {"fetched_at": None, "markets": {}}

def save_cache(cache):
    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f, indent=2)

def is_cache_valid(cache):
    if not cache.get("fetched_at"):
        return False
    fetched = datetime.fromisoformat(cache["fetched_at"])
    age = (datetime.now() - fetched).total_seconds()
    return age < CACHE_TTL_SECONDS

# === Fetch Polymarket odds ===
def fetch_polymarket_odds():
    """Holt alle WM-relevanten Märkte von Polymarket (mit Cache)."""
    cache = load_cache()
    if is_cache_valid(cache):
        print(f"[Polymarket] Cache hit – {cache['fetched_at']}")
        return cache["markets"]

    print("[Polymarket] Fetching live data...")
    try:
        # Erst alle Märkte holen und client-seitig filtern
        # (die API-Suche ist buggy/limitiert)
        url = f"{POLYMARKET_API}?limit=500"
        req = urllib.request.Request(url, headers={
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
        })
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode())

        # Filtere nur WM-relevante, offene Märkte
        wm_keywords = [
            "germany", "deutschland", "world cup", "fifa", "copa america",
            "brasil", "argentina", "france", "spain", "england",
            "portugal", "netherlands", "usa", "mexico", "canada",
            "italy", "belgium", "uruguay", "croatia", "ukraine",
            "cura", "ivory coast", "elfenbein", "ecuador"
        ]

        markets = {}
        for m in data:
            question = m.get("question", "").lower()
            outcomes = m.get("outcomes", [])
            prices = m.get("outcomePrices", [])
            vol = m.get("volumeNum", 0)
            closed = m.get("closed", False)

            if closed:
                continue

            # Nur WM/Markt-relevante Märkte
            if any(k in question for k in wm_keywords):
                # outcomePrices ist ein JSON-String, parsen
                try:
                    parsed_prices = json.loads(prices) if isinstance(prices, str) else prices
                except:
                    parsed_prices = prices
                markets[m["id"]] = {
                    "question": m.get("question", ""),
                    "outcomes": outcomes,
                    "prices": parsed_prices,
                    "volume": vol,
                }

        cache = {
            "fetched_at": datetime.now().isoformat(),
            "markets": markets
        }
        save_cache(cache)
        print(f"[Polymarket] {len(markets)} WM-Märkte gespeichert.")
        return markets

    except Exception as e:
        print(f"[Polymarket] Fetch error: {e}", file=sys.stderr)
        cache = load_cache()
        if cache.get("markets"):
            print("[Polymarket] Using expired cache as fallback.")
            return cache["markets"]
        return {}

# === Team-Name Mapping (Schedule → Polymarket) ===
TEAM_ALIASES = {
    "Deutschland": ["Germany", "Deutschland", "GER"],
    "Curaçao": ["Curaçao", "Curacao"],
    "Elfenbeinküste": ["Ivory Coast", "Elfenbeinküste", "Cote d'Ivoire"],
    "Ecuador": ["Ecuador"],
    "Mexiko": ["Mexico", "Mexiko"],
    "Südafrika": ["South Africa", "Südafrika"],
    "Niederlande": ["Netherlands", "Niederlande"],
    "Japan": ["Japan"],
    "Brasilien": ["Brazil", "Brasilien"],
    "Marokko": ["Morocco", "Marokko"],
    "Argentinien": ["Argentina", "Argentinien"],
    "Österreich": ["Austria", "Österreich"],
    "Italien": ["Italy", "Italien"],
    "Spanien": ["Spain", "Spanien"],
    "Frankreich": ["France", "Frankreich"],
    "Portugal": ["Portugal"],
    "England": ["England"],
    "USA": ["USA", "United States", "US"],
    "Kanada": ["Canada", "Kanada"],
    "Belgien": ["Belgium", "Belgien"],
    "Uruguay": ["Uruguay"],
    "Kroatien": ["Croatia", "Kroatien"],
    "Ukraine": ["Ukraine"],
    "Polen": ["Poland", "Polen"],
    "Ungarn": ["Hungary", "Ungarn"],
    "Schweiz": ["Switzerland", "Schweiz"],
    "Serbien": ["Serbia", "Serbien"],
    "Kamerun": ["Cameroon", "Kamerun"],
    "Slowakei": ["Slovakia", "Slowakei"],
    "Südkorea": ["South Korea", "Südkorea"],
    "Australien": ["Australia", "Australien"],
    "Saudi-Arabien": ["Saudi Arabia", "Saudi-Arabien"],
    "Iran": ["Iran"],
    "Dänemark": ["Denmark", "Dänemark"],
    "Schweden": ["Sweden", "Schweden"],
    "Türkei": ["Turkey", "Türkei"],
    "Rumänien": ["Romania", "Rumänien"],
    "Peru": ["Peru"],
    "Bosnien & Herzegowina": ["Bosnia", "Bosnien"],
    "Neuseeland": ["New Zealand", "Neuseeland"],
    "Panama": ["Panama"],
    "Marokko": ["Morocco"],
    "Tschechien": ["Czech Republic", "Tschechien"],
    "Schottland": ["Scotland", "Schottland"],
    "Haiti": ["Haiti"],
    "Tunesien": ["Tunisia", "Tunesien"],
    "Ägypten": ["Egypt", "Ägypten"],
    "Jordanien": ["Jordan", "Jordanien"],
    "Algerien": ["Algeria", "Algerien"],
    "Costa Rica": ["Costa Rica"],
    "Nigeria": ["Nigeria"],
    "Paraguay": ["Paraguay"],
}

def odds_to_percent(odds_str):
    """Wandelt Polymarket-Odds (z.B. "0.52") in Prozent um."""
    try:
        return round(float(odds_str) * 100, 1)
    except:
        return None

def find_market_for_game(markets, team1, team2):
    """Findet ein Polymarket-Markt für ein Spiel."""
    t1_aliases = TEAM_ALIASES.get(team1, [team1])
    t2_aliases = TEAM_ALIASES.get(team2, [team2])

    # 1. Suche direktes Match-Markt (z.B. "Germany vs Brazil")
    for mid, m in markets.items():
        q = m["question"].lower()
        t1_match = any(a.lower() in q for a in t1_aliases)
        t2_match = any(a.lower() in q for a in t2_aliases)
        if t1_match and t2_match and (" vs " in q or "-" in q):
            return m

    # 2. Fallback: WM-Sieg-Markt für Team1 (z.B. "Will Germany win the 2026 FIFA World Cup?")
    for mid, m in markets.items():
        q = m["question"].lower()
        if any(a.lower() in q for a in t1_aliases) and "win the 2026" in q:
            return m

    # 3. Suche nur nach Team1
    for mid, m in markets.items():
        q = m["question"].lower()
        if any(a.lower() in q for a in t1_aliases):
            return m

    return None

def format_odds_line(market):
    """Formatiert eine Odds-Zeile für ein Markt."""
    if not market:
        return None

    outcomes = market.get("outcomes", [])
    prices = market.get("prices", [])
    vol = market.get("volume", 0)
    question = market.get("question", "")

    if not outcomes or not prices:
        return None

    # WM-Sieg-Markt? z.B. "Will Germany win the 2026 FIFA World Cup?"
    is_winner_market = "win the 2026" in question.lower() or "winner" in question.lower()

    if is_winner_market:
        # Zeige nur den Favoriten-Wert als Kontext
        yes_pct = odds_to_percent(prices[0]) if prices else None
        if yes_pct is not None and yes_pct < 50:
            return f"🇩🇪 WM-Sieg: {yes_pct:.1f}%"
        return None

    # Normales Match-Markt
    odds_lines = []
    for i, (outcome, price) in enumerate(zip(outcomes, prices)):
        pct = odds_to_percent(price)
        if pct is not None:
            short = outcome[:12] if len(outcome) > 12 else outcome
            odds_lines.append(f"{short} {pct:.0f}%")

    if not odds_lines:
        return None

    vol_str = f"${vol/1000:.0f}k" if vol > 0 else ""
    return " | ".join(odds_lines) + (f" | {vol_str}" if vol_str else "")

# === Tipps ===
TIPS = {
    # Tag 1 - 11.06.2026
    ("Mexiko", "Südafrika"): {"tipp": "2:0", "reason": "Mexiko mit klarem Heimvorteil im Aztekenstadion. Südafrika ist in dieser Formation zu schwach."},
    ("Peru", "Brasilien"): {"tipp": "0:2", "reason": "Brasilien dominiert. Neymar und Co. zu stark für Peru."},
    # Tag 2 - 12.06.2026
    ("Nigeria", "Indonesien"): {"tipp": "3:1", "reason": "Nigeria hat mehr Erfahrung und individuelle Klasse."},
    ("Venezuela", "Ecuador"): {"tipp": "1:1", "reason": "Knapes Spiel, beide Teams auf ähnlichem Niveau."},
    # Tag 3 - 13.06.2026
    ("USA", "Kanada"): {"tipp": "2:1", "reason": "Heimvorteil USA wird den Unterschied machen. Kanada ist gut, aber nicht gut genug."},
    ("Spanien", "Korea"): {"tipp": "3:1", "reason": "Spanien ist technisch überlegen. Korea hat keine Antwort auf die spanische Passmaschine."},
    # Tag 4 - 14.06.2026
    ("Niederlande", "Ungarn"): {"tipp": "3:0", "reason": "Niederlande mit klarer Dominanz. Ungarn kann nur reagieren."},
    ("Marokko", "Ägypten"): {"tipp": "2:1", "reason": "Marokko hat sich besser entwickelt. Ägypten ist stark, aber Marokko siegt knapp."},
}

def get_tipp(team1, team2):
    key = (team1, team2)
    rev_key = (team2, team1)
    if key in TIPS:
        return TIPS[key]
    if rev_key in TIPS:
        t = TIPS[rev_key]
        # Tipp umdrehen (aber nur bei klarem Ergebnis)
        parts = t["tipp"].split(":")
        if len(parts) == 2 and int(parts[0]) > int(parts[1]):
            return {"tipp": f"{parts[1]}:{parts[0]}", "reason": t["reason"]}
        return t
    return {"tipp": "?", "reason": "?"}

# === Generate tip text ===
def generate_tip_text(games, polymarket_markets):
    if not games:
        return None

    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%d.%m.%Y")
    lines = []
    lines.append(f"🏆 *WM 2026 Tipps – {tomorrow}*\n")

    for g in games:
        team1 = g.get("team1", "?")
        team2 = g.get("team2", "?")
        time = g.get("time_mesz", "?")
        group = g.get("group", "")
        stadium = g.get("stadium", "")
        stage = g.get("stage", "Gruppenphase")

        tipp_data = get_tipp(team1, team2)
        tipp = tipp_data["tipp"]
        reason = tipp_data["reason"]

        # Polymarket-Odds holen
        market = find_market_for_game(polymarket_markets, team1, team2)
        odds_line = format_odds_line(market)

        group_info = f"📁 {group}" if group else ""

        lines.append("━" * 30)
        lines.append(f"{stage} {group_info}".strip())
        lines.append(f"🇩🇪 {team1} vs {team2}")
        lines.append(f"🕐 {time} MESZ | 📍 {stadium}")
        lines.append(f"🔮 *Tipp: {tipp}*")
        if odds_line:
            lines.append(f"📊 Polymarket: {odds_line}")
        lines.append(f"💡 {reason}")
        lines.append("")

    lines.append("─" * 30)
    lines.append(f"_Quoten: Polymarket (polymarket.com) | Stand: {datetime.now().strftime('%d.%m.%Y %H:%M')}_")
    lines.append("Dein HolBot 💬")

    return "\n".join(lines)

# === Send to Telegram ===
def send_telegram(text, chat_id):
    url = TELEGRAM_API
    data = json.dumps({
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown"
    }).encode()

    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return resp.status == 200
    except Exception as e:
        print(f"Telegram error: {e}", file=sys.stderr)
        return False

# === Find games for tomorrow ===
def get_tomorrows_games(schedule):
    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    return [g for g in schedule.get("games", []) if g.get("date") == tomorrow]

# === Main ===
def main():
    print(f"[{datetime.now()}] WM Tipp-Script gestartet.")

    schedule = load_schedule()
    games = get_tomorrows_games(schedule)

    if not games:
        print(f"[{datetime.now()}] Keine Spiele morgen – nichts zu tun.")
        return

    print(f"[{datetime.now()}] {len(games)} Spiele morgen gefunden.")

    # Polymarket-Daten holen
    markets = fetch_polymarket_odds()

    # Text generieren
    text = generate_tip_text(games, markets)
    print("\n" + text + "\n")

    # An alle Tipper senden
    for tipper in TIPPERS:
        success = send_telegram(text, tipper["chat_id"])
        status = "✅" if success else "❌"
        print(f"  {status} → {tipper['name']}")

if __name__ == "__main__":
    main()

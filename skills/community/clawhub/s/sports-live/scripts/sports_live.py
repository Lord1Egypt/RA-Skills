#!/usr/bin/env python3
"""
sports_live.py — Script della skill sports-live per OpenClaw
Aggiornamenti sportivi in tempo reale tramite API gratuite.

USO:
  python3 sports_live.py live
  python3 sports_live.py today <sport>
  python3 sports_live.py next <squadra>
  python3 sports_live.py last <squadra>
  python3 sports_live.py search <nome>
  python3 sports_live.py football_live <API_KEY>
  python3 sports_live.py football_today <API_KEY>
"""

import sys
import json
import urllib.request
import urllib.parse
from datetime import datetime

HEADERS = {"User-Agent": "OpenClaw/sports-live-skill"}
BASE = "https://www.thesportsdb.com/api/v1/json/1"

SPORT_MAP = {
    "calcio": "Soccer", "soccer": "Soccer", "football": "Soccer",
    "tennis": "Tennis",
    "basket": "Basketball", "basketball": "Basketball", "nba": "Basketball",
    "f1": "Motorsport", "moto": "Motorsport", "motorsport": "Motorsport",
    "hockey": "Ice_Hockey",
    "rugby": "Rugby", "baseball": "Baseball", "handball": "Handball",
    "volleyball": "Volleyball", "cricket": "Cricket",
}


def fetch(url: str, extra: dict = None) -> dict:
    h = {**HEADERS, **(extra or {})}
    try:
        req = urllib.request.Request(url, headers=h)
        with urllib.request.urlopen(req, timeout=12) as r:
            return json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        return {"_error": f"HTTP {e.code}: {e.reason}"}
    except Exception as e:
        return {"_error": str(e)}


def ts() -> str:
    return datetime.now().strftime("%H:%M:%S")


def norm_sport(s: str) -> str:
    return SPORT_MAP.get(s.lower(), s.capitalize())


# ─── TheSportsDB ────────────────────────────────────────────

def cmd_live() -> str:
    data = fetch(f"{BASE}/livescore.php")
    if "_error" in data:
        return f"[ERRORE] {data['_error']}"
    events = data.get("events") or []
    if not events:
        return f"Nessun evento live al momento ({ts()})."
    out = [f"📡 LIVESCORES — {ts()} | {len(events)} eventi\n"]
    for ev in events[:30]:
        home = ev.get("strHomeTeam", "?")
        away = ev.get("strAwayTeam", "?")
        sh = ev.get("intHomeScore", "–")
        sa = ev.get("intAwayScore", "–")
        status = ev.get("strProgress") or ev.get("strStatus") or ""
        league = ev.get("strLeague", "")
        sport = ev.get("strSport", "")
        out.append(f"  [{sport} / {league}] {home} {sh}–{sa} {away}  {status}")
    return "\n".join(out)


def cmd_today(sport: str = "Soccer") -> str:
    d = datetime.now().strftime("%Y-%m-%d")
    sp = norm_sport(sport)
    data = fetch(f"{BASE}/eventsday.php?d={d}&s={urllib.parse.quote(sp)}")
    if "_error" in data:
        return f"[ERRORE] {data['_error']}"
    events = data.get("events") or []
    if not events:
        return f"Nessun evento {sp} trovato per oggi ({d})."
    out = [f"📅 {sp.upper()} — Oggi {d} | {len(events)} eventi\n"]
    for ev in events[:35]:
        name = ev.get("strEvent") or f"{ev.get('strHomeTeam','')} vs {ev.get('strAwayTeam','')}"
        league = ev.get("strLeague", "")
        t = ev.get("strTime", "")
        sh = ev.get("intHomeScore")
        sa = ev.get("intAwayScore")
        score = f"  {sh}–{sa}" if sh is not None else ""
        out.append(f"  [{league}] {name}{score}  {t}".strip())
    return "\n".join(out)


def cmd_next(team: str) -> str:
    data = fetch(f"{BASE}/searchteams.php?t={urllib.parse.quote(team)}")
    teams = data.get("teams") or []
    if not teams:
        return f"Nessun team trovato per '{team}'."
    t = teams[0]
    tid = t.get("idTeam")
    name = t.get("strTeam", team)
    league = t.get("strLeague", "")
    data2 = fetch(f"{BASE}/eventsnext.php?id={tid}")
    events = data2.get("events") or []
    if not events:
        return f"Nessuna prossima partita trovata per {name}."
    out = [f"🗓️ PROSSIME PARTITE — {name} ({league})\n"]
    for ev in events[:8]:
        date = ev.get("dateEvent", "?")
        time_ = ev.get("strTime", "")
        event_name = ev.get("strEvent", "?")
        venue = ev.get("strVenue", "")
        line = f"  {date} {time_}  {event_name}"
        if venue:
            line += f"  @ {venue}"
        out.append(line)
    return "\n".join(out)


def cmd_last(team: str) -> str:
    data = fetch(f"{BASE}/searchteams.php?t={urllib.parse.quote(team)}")
    teams = data.get("teams") or []
    if not teams:
        return f"Nessun team trovato per '{team}'."
    t = teams[0]
    tid = t.get("idTeam")
    name = t.get("strTeam", team)
    data2 = fetch(f"{BASE}/eventslast.php?id={tid}")
    events = data2.get("results") or data2.get("events") or []
    if not events:
        return f"Nessun risultato recente trovato per {name}."
    out = [f"📊 ULTIMI RISULTATI — {name}\n"]
    for ev in events[:8]:
        date = ev.get("dateEvent", "?")
        event_name = ev.get("strEvent", "?")
        sh = ev.get("intHomeScore", "?")
        sa = ev.get("intAwayScore", "?")
        out.append(f"  {date}  {event_name}  {sh}–{sa}")
    return "\n".join(out)


def cmd_search(query: str) -> str:
    d1 = fetch(f"{BASE}/searchteams.php?t={urllib.parse.quote(query)}")
    d2 = fetch(f"{BASE}/searchplayers.php?p={urllib.parse.quote(query)}")
    teams = d1.get("teams") or []
    players = d2.get("player") or []
    out = [f"🔍 Risultati per '{query}'\n"]
    if teams:
        out.append(f"SQUADRE ({len(teams)}):")
        for t in teams[:5]:
            out.append(f"  • {t.get('strTeam','?')} — {t.get('strLeague','?')} ({t.get('strCountry','?')})")
    if players:
        out.append(f"\nGIOCATORI ({len(players)}):")
        for p in players[:5]:
            out.append(f"  • {p.get('strPlayer','?')} — {p.get('strTeam','?')} ({p.get('strPosition','?')})")
    if not teams and not players:
        out.append("Nessun risultato trovato.")
    return "\n".join(out)


# ─── API-Football (free plan: 100 req/giorno, no carta) ────

def cmd_football_live(api_key: str) -> str:
    url = "https://v3.football.api-sports.io/fixtures?live=all"
    data = fetch(url, {"x-apisports-key": api_key})
    if "_error" in data:
        return f"[ERRORE] {data['_error']}"
    if data.get("errors"):
        return f"[ERRORE API-Football] {data['errors']}"
    matches = data.get("response") or []
    if not matches:
        return f"⚽ Nessuna partita di calcio live ora ({ts()})."
    out = [f"⚽ CALCIO LIVE — {ts()} | {len(matches)} partite\n"]
    for m in matches[:30]:
        home = m["teams"]["home"]["name"]
        away = m["teams"]["away"]["name"]
        gh = m["goals"]["home"]
        ga = m["goals"]["away"]
        mn = m["fixture"]["status"].get("elapsed", "")
        lg = m["league"]["name"]
        min_str = f" {mn}'" if mn else ""
        out.append(f"  [{lg}] {home} {gh}–{ga} {away}{min_str}")
    return "\n".join(out)


def cmd_football_today(api_key: str) -> str:
    d = datetime.now().strftime("%Y-%m-%d")
    url = f"https://v3.football.api-sports.io/fixtures?date={d}"
    data = fetch(url, {"x-apisports-key": api_key})
    if "_error" in data:
        return f"[ERRORE] {data['_error']}"
    if data.get("errors"):
        return f"[ERRORE API-Football] {data['errors']}"
    matches = data.get("response") or []
    if not matches:
        return f"⚽ Nessuna partita di calcio trovata per oggi ({d})."
    leagues: dict = {}
    for m in matches:
        lg = m["league"]["name"]
        leagues.setdefault(lg, []).append(m)
    out = [f"⚽ CALCIO OGGI — {d} | {len(matches)} partite\n"]
    for lg, ms in list(leagues.items())[:12]:
        out.append(f"\n🏆 {lg}")
        for m in ms[:6]:
            home = m["teams"]["home"]["name"]
            away = m["teams"]["away"]["name"]
            t_str = m["fixture"]["date"][11:16] if len(m["fixture"]["date"]) > 15 else "—"
            status = m["fixture"]["status"]["short"]
            gh = m["goals"]["home"]
            ga = m["goals"]["away"]
            score = f"{gh}–{ga}" if gh is not None else t_str
            out.append(f"  {home} vs {away}  {score}  [{status}]")
    return "\n".join(out)


# ─── Entry point ────────────────────────────────────────────

def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(0)

    cmd = args[0].lower()
    rest = args[1:]

    dispatch = {
        "live":           lambda: cmd_live(),
        "today":          lambda: cmd_today(rest[0] if rest else "Soccer"),
        "next":           lambda: cmd_next(" ".join(rest)) if rest else "Specifica il nome della squadra.",
        "last":           lambda: cmd_last(" ".join(rest)) if rest else "Specifica il nome della squadra.",
        "search":         lambda: cmd_search(" ".join(rest)) if rest else "Specifica un nome da cercare.",
        "football_live":  lambda: cmd_football_live(rest[0]) if rest else
                          "[INFO] Per usare questa funzione serve una API key gratuita.\nRegistrati su: https://dashboard.api-football.com/register",
        "football_today": lambda: cmd_football_today(rest[0]) if rest else
                          "[INFO] Per usare questa funzione serve una API key gratuita.\nRegistrati su: https://dashboard.api-football.com/register",
    }

    if cmd not in dispatch:
        print(f"[ERRORE] Comando '{cmd}' non riconosciuto.")
        print("Comandi validi:", ", ".join(dispatch.keys()))
        sys.exit(1)

    print(dispatch[cmd]())


if __name__ == "__main__":
    main()

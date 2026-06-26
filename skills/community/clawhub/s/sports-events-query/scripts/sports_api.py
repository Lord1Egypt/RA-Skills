#!/usr/bin/env python3
"""
Sports Events Query - TheSportsDB API Wrapper
Supports: soccer, basketball, tennis, baseball, and more
"""

import argparse
import json
import requests
import sys
from typing import Dict, List, Optional, Any

BASE_URL = "https://www.thesportsdb.com/api/v1/json/3"

# Sport ID mapping
SPORT_MAPPING = {
    "soccer": "Soccer",
    "football": "Soccer",
    "basketball": "Basketball",
    "nba": "Basketball",
    "tennis": "Tennis",
    "baseball": "Baseball",
    "nfl": "American Football",
    "american football": "American Football",
    "hockey": "Ice Hockey",
    "nhl": "Ice Hockey",
    "golf": "Golf",
    "rugby": "Rugby",
    "cricket": "Cricket",
    "motorsport": "Motorsport",
    "racing": "Motorsport",
}

# Popular league IDs
POPULAR_LEAGUES = {
    "premier league": "4328",
    "epl": "4328",
    "english premier league": "4328",
    "la liga": "4335",
    "bundesliga": "4331",
    "serie a": "4332",
    "ligue 1": "4334",
    "champions league": "4480",
    "nba": "4387",
    "nfl": "4391",
}


def get_sport_id(sport_name: str) -> Optional[str]:
    """Convert sport name to sport ID"""
    sport_lower = sport_name.lower()
    return SPORT_MAPPING.get(sport_lower)


def get_countries() -> List[Dict]:
    """Get list of available countries"""
    response = requests.get(f"{BASE_URL}/all_countries.php")
    data = response.json()
    return data.get("countries", [])


def get_leagues(sport: Optional[str] = None, country: Optional[str] = None) -> List[Dict]:
    """Get leagues, optionally filtered by sport and country"""
    params = {}
    if sport:
        params["s"] = sport
    if country:
        params["c"] = country
    
    try:
        response = requests.get(f"{BASE_URL}/all_leagues.php", params=params, timeout=10)
        if response.status_code != 200:
            return []
        data = response.json()
        if not data:
            return []
        return data.get("leagues", []) or []
    except:
        return []


def get_league_info(league_id: str) -> Optional[Dict]:
    """Get detailed league information"""
    try:
        response = requests.get(f"{BASE_URL}/lookupleague.php", params={"id": league_id}, timeout=10)
        if response.status_code != 200:
            return None
        data = response.json()
        if not data:
            return None
        leagues = data.get("leagues", [])
        return leagues[0] if leagues else None
    except:
        return None


def get_live_scores(sport: str = "Soccer") -> List[Dict]:
    """Get live scores"""
    sport_id = get_sport_id(sport)
    if not sport_id:
        sport_id = sport
    
    try:
        response = requests.get(f"{BASE_URL}/livescore.php", params={"s": sport_id}, timeout=10)
        if response.status_code != 200:
            return []
        data = response.json()
        if not data:
            return []
        return data.get("event", []) or []
    except:
        return []


def get_today_events(sport: str = "Soccer") -> List[Dict]:
    """Get today's events"""
    sport_id = get_sport_id(sport)
    if not sport_id:
        sport_id = sport
    
    try:
        response = requests.get(f"{BASE_URL}/eventsday.php", params={"s": sport_id}, timeout=10)
        if response.status_code != 200:
            print(f"API Error: HTTP {response.status_code}", file=sys.stderr)
            return []
        data = response.json()
        if not data:
            return []
        return data.get("events", []) or []
    except Exception as e:
        print(f"Request Error: {e}", file=sys.stderr)
        return []


def get_events_by_league(league_id: str, season: Optional[str] = None) -> List[Dict]:
    """Get events for a specific league"""
    params = {"id": league_id}
    if season:
        params["season"] = season
    
    response = requests.get(f"{BASE_URL}/eventsseason.php", params=params)
    data = response.json()
    return data.get("events", [])


def get_team(team_id: str) -> Optional[Dict]:
    """Get team details"""
    try:
        response = requests.get(f"{BASE_URL}/lookupteam.php", params={"id": team_id}, timeout=10)
        if response.status_code != 200:
            return None
        data = response.json()
        if not data:
            return None
        teams = data.get("teams", [])
        return teams[0] if teams else None
    except:
        return None


def search_team(team_name: str) -> List[Dict]:
    """Search for teams by name"""
    try:
        response = requests.get(f"{BASE_URL}/searchteams.php", params={"t": team_name}, timeout=10)
        if response.status_code != 200:
            return []
        data = response.json()
        if not data:
            return []
        return data.get("teams", []) or []
    except:
        return []


def search_event(event_name: str) -> List[Dict]:
    """Search for events"""
    try:
        response = requests.get(f"{BASE_URL}/searchevents.php", params={"e": event_name}, timeout=10)
        if response.status_code != 200:
            return []
        data = response.json()
        if not data:
            return []
        return data.get("event", []) or []
    except:
        return []


def get_league_tables(league_id: str, season: str) -> List[Dict]:
    """Get league standings/table"""
    try:
        response = requests.get(f"{BASE_URL}/lookuptable.php", params={"l": league_id, "s": season}, timeout=10)
        if response.status_code != 200:
            return []
        data = response.json()
        if not data:
            return []
        return data.get("table", []) or []
    except:
        return []


def format_team_info(team: Dict) -> str:
    """Format team information"""
    lines = [
        f"🏟️ {team.get('strTeam', 'N/A')}",
        f"   简称: {team.get('strTeamShort', 'N/A')}",
    ]
    
    if team.get('strStadium'):
        lines.append(f"   主场: {team['strStadium']}")
    if team.get('intStadiumCapacity'):
        lines.append(f"   容量: {team['intStadiumCapacity']}")
    if team.get('strLocation'):
        lines.append(f"   位置: {team['strLocation']}")
    if team.get('strCountry'):
        lines.append(f"   国家: {team['strCountry']}")
    if team.get('strLeague'):
        lines.append(f"   联赛: {team['strLeague']}")
    if team.get('strDescriptionEN'):
        desc = team['strDescriptionEN'][:200]
        lines.append(f"   简介: {desc}...")
    
    return "\n".join(lines)


def format_event(event: Dict) -> str:
    """Format a single event/match"""
    date = event.get('dateEvent', 'N/A')
    time = event.get('strTime', '')
    home = event.get('strHomeTeam', 'N/A')
    away = event.get('strAwayTeam', 'N/A')
    league = event.get('strLeague', 'N/A')
    score = event.get('intHomeScore', '')
    
    if score:
        return f"  {home} {event.get('intHomeScore','')} - {event.get('intAwayScore','')} {away} ({league})"
    else:
        return f"  {home} vs {away} - {time} ({league})"


def cmd_today(args):
    """Show today's events"""
    sport = args.sport or "soccer"
    events = get_today_events(sport)
    
    if not events:
        print(f"今日无赛事 (运动: {sport})")
        return
    
    # Group by league
    by_league = {}
    for event in events:
        league = event.get('strLeague', 'Unknown')
        if league not in by_league:
            by_league[league] = []
        by_league[league].append(event)
    
    print(f"📅 今日赛事 ({sport})")
    print("=" * 50)
    
    for league, evts in sorted(by_league.items()):
        print(f"\n🏆 {league}")
        for evt in evts[:10]:  # Limit to 10 per league
            print(format_event(evt))


def cmd_live(args):
    """Show live scores"""
    sport = args.sport or "soccer"
    events = get_live_scores(sport)
    
    if not events:
        print(f"暂无直播赛事 (运动: {sport})")
        return
    
    print(f"🔴 正在直播 ({sport})")
    print("=" * 50)
    
    for event in events[:20]:
        print(format_event(event))


def cmd_team(args):
    """Search and show team info"""
    teams = search_team(args.name)
    
    if not teams:
        print(f"未找到球队: {args.name}")
        return
    
    print(f"找到 {len(teams)} 个球队:")
    print("=" * 50)
    
    for team in teams[:5]:
        print(format_team_info(team))
        print()


def cmd_search(args):
    """Search events"""
    events = search_event(args.query)
    
    if not events:
        print(f"未找到赛事: {args.query}")
        return
    
    print(f"找到 {len(events)} 个赛事:")
    print("=" * 50)
    
    for event in events[:10]:
        print(format_event(event))


def cmd_leagues(args):
    """List leagues"""
    leagues = get_leagues(sport=args.sport, country=args.country)
    
    if not leagues:
        print("未找到联赛")
        return
    
    print(f"找到 {len(leagues)} 个联赛:")
    print("=" * 50)
    
    for league in leagues[:20]:
        name = league.get('strLeague', 'N/A')
        country = league.get('strCountry', 'N/A')
        sport = league.get('strSport', 'N/A')
        print(f"  {name} ({country}) - {sport}")


def get_league_id(league_name: str) -> Optional[str]:
    """Convert league name to ID"""
    league_lower = league_name.lower().strip()
    if league_lower in POPULAR_LEAGUES:
        return POPULAR_LEAGUES[league_lower]
    
    # Search in leagues
    leagues = get_leagues()
    for league in leagues:
        name = league.get('strLeague', '').lower()
        alternate = league.get('strLeagueAlternate', '').lower()
        if league_name.lower() in name or league_name.lower() in alternate:
            return league.get('idLeague')
    return None


def cmd_league_events(args):
    """Get events for a specific league"""
    # Get league ID
    league_id = get_league_id(args.league)
    if not league_id:
        print(f"未找到联赛: {args.league}")
        return
    
    # Get events
    if args.next:
        events = get_events_by_league(league_id)
    else:
        events = get_events_by_league(league_id)
    
    if not events:
        print(f"未找到赛事")
        return
    
    # Sort by date
    events.sort(key=lambda x: x.get('dateEvent', '') + x.get('strTime', ''))
    
    print(f"📅 {args.league} 赛事")
    print("=" * 50)
    
    for event in events[:20]:
        print(format_event(event))


def main():
    parser = argparse.ArgumentParser(description="Sports Events Query - TheSportsDB API")
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # today command
    parser_today = subparsers.add_parser("today", help="Today's events")
    parser_today.add_argument("--sport", "-s", default="soccer", help="Sport type")
    parser_today.set_defaults(func=cmd_today)
    
    # live command
    parser_live = subparsers.add_parser("live", help="Live scores")
    parser_live.add_argument("--sport", "-s", default="soccer", help="Sport type")
    parser_live.set_defaults(func=cmd_live)
    
    # team command
    parser_team = subparsers.add_parser("team", help="Team information")
    parser_team.add_argument("name", help="Team name")
    parser_team.set_defaults(func=cmd_team)
    
    # search command
    parser_search = subparsers.add_parser("search", help="Search events")
    parser_search.add_argument("query", help="Search query")
    parser_search.set_defaults(func=cmd_search)
    
    # leagues command
    parser_leagues = subparsers.add_parser("leagues", help="List leagues")
    parser_leagues.add_argument("--sport", "-s", help="Filter by sport")
    parser_leagues.add_argument("--country", "-c", help="Filter by country")
    parser_leagues.set_defaults(func=cmd_leagues)
    
    # league command
    parser_league_events = subparsers.add_parser("league", help="League events")
    parser_league_events.add_argument("league", help="League name (e.g., 'premier league', 'nba')")
    parser_league_events.add_argument("--next", "-n", action="store_true", help="Next events only")
    parser_league_events.set_defaults(func=cmd_league_events)
    
    args = parser.parse_args()
    
    if args.command is None:
        parser.print_help()
        return
    
    try:
        args.func(args)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

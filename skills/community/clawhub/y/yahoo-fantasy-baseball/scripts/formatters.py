"""Output formatters for Yahoo Fantasy Baseball data.

Supports text (tabular), JSON, and discord (markdown) output formats.
Data comes from yahoo-fantasy-api as plain dicts (not YFPY objects).
"""

import json


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _safe(obj, key, default=""):
    """Safely get a value from a dict or object attribute."""
    if isinstance(obj, dict):
        val = obj.get(key, default)
    else:
        val = getattr(obj, key, default)
    if val is None:
        return default
    return val


def _team_name(team):
    """Extract team name."""
    return _safe(team, "name", "Unknown")


def _team_id(team):
    """Extract team ID from team_id or team_key."""
    tid = _safe(team, "team_id", "")
    if tid:
        return tid
    tk = _safe(team, "team_key", "")
    if tk and ".t." in tk:
        return tk.split(".t.")[-1]
    return "?"


def _team_key(team):
    """Extract team key."""
    return _safe(team, "team_key", "")


def _player_name(player):
    """Extract player name from a player dict."""
    name = _safe(player, "name", "")
    if isinstance(name, dict):
        return name.get("full", "") or f"{name.get('first', '')} {name.get('last', '')}".strip()
    if isinstance(name, str) and name:
        return name
    full = _safe(player, "full_name", "")
    if full:
        return full
    first = _safe(player, "first_name", "")
    last = _safe(player, "last_name", "")
    if first or last:
        return f"{first} {last}".strip()
    return str(name) if name else "Unknown"


def _player_position(player):
    """Extract eligible positions from a player."""
    positions = _safe(player, "eligible_positions")
    if positions and isinstance(positions, list):
        # Handle both flat strings ["OF", "Util"] and dicts [{"position": "OF"}]
        parts = []
        for p in positions:
            if isinstance(p, dict):
                parts.append(p.get("position", str(p)))
            else:
                parts.append(str(p))
        return ",".join(parts)
    display = _safe(player, "display_position", "")
    if display:
        return display
    primary = _safe(player, "primary_position", "")
    return primary


def _player_selected_position(player):
    """Extract the current lineup slot."""
    sel = _safe(player, "selected_position", "")
    if isinstance(sel, dict):
        return sel.get("position", "")
    return str(sel) if sel else ""


def _player_status(player):
    """Extract injury/status from a player."""
    status = _safe(player, "status", "")
    return status if status else ""


def _player_team(player):
    """Extract the real MLB team abbreviation."""
    return _safe(player, "editorial_team_abbr", "")


def _player_id(player):
    """Extract the player ID."""
    return _safe(player, "player_id", "")


def _manager_name(team):
    """Extract manager name(s) from a team dict."""
    managers = _safe(team, "managers", [])
    if not managers:
        return ""
    names = []
    for mgr in managers:
        if isinstance(mgr, dict):
            manager = mgr.get("manager", mgr)
            nickname = _safe(manager, "nickname", "")
        else:
            nickname = _safe(mgr, "nickname", "")
        if nickname:
            names.append(nickname)
    return ", ".join(names) if names else ""


def _extract_player_stats(player):
    """Extract stat values from a player dict."""
    stats_map = {}
    # yahoo-fantasy-api player_stats returns stats as top-level keys
    # with display_name as key and value as the stat value
    player_stats = _safe(player, "player_stats")
    if player_stats and isinstance(player_stats, dict):
        stats_list = _safe(player_stats, "stats")
        if stats_list and isinstance(stats_list, list):
            for stat in stats_list:
                sid = str(_safe(stat, "stat_id", ""))
                val = _safe(stat, "value", "0")
                if sid:
                    stats_map[sid] = val
    # Check for top-level stat keys (from player_stats() method)
    for key, val in (player.items() if isinstance(player, dict) else []):
        if key not in ("name", "player_id", "position_type", "eligible_positions",
                       "selected_position", "status", "editorial_team_abbr",
                       "player_stats", "player_points", "ownership", "percent_owned"):
            stats_map[key] = val
    # Also check player_points
    points = _safe(player, "player_points")
    if points and isinstance(points, dict):
        total = _safe(points, "total")
        if total != "":
            stats_map["total_points"] = total
    return stats_map


def _extract_categories_from_settings(stat_categories):
    """Extract stat category names from league.stat_categories() result.

    Args:
        stat_categories: list of dicts from league.stat_categories(),
            each with 'display_name' and 'position_type'.
    """
    categories = []
    if not stat_categories:
        return categories
    for cat in stat_categories:
        if isinstance(cat, dict):
            name = cat.get("display_name", "")
            categories.append({
                "stat_id": name,  # Use display_name as ID for yahoo-fantasy-api
                "name": name,
                "abbr": name,
                "position_type": cat.get("position_type", ""),
            })
    return categories


# ---------------------------------------------------------------------------
# Leagues
# ---------------------------------------------------------------------------

def format_leagues(leagues, fmt="text"):
    if fmt == "json":
        items = []
        for league in leagues:
            items.append({
                "league_id": _safe(league, "league_id"),
                "name": _safe(league, "name"),
                "season": _safe(league, "season"),
                "num_teams": _safe(league, "num_teams"),
                "league_key": _safe(league, "league_key"),
            })
        return json.dumps({"leagues": items}, indent=2)

    lines = ["Your Yahoo Fantasy Baseball Leagues"]
    lines.append(f"{'ID':<12} {'Season':<8} {'Teams':<7} {'Name'}")
    lines.append("-" * 60)
    for league in leagues:
        lid = _safe(league, "league_id")
        name = _safe(league, "name")
        season = _safe(league, "season")
        num = _safe(league, "num_teams")
        lines.append(f"{lid:<12} {season:<8} {num:<7} {name}")

    if fmt == "discord":
        return "```\n" + "\n".join(lines) + "\n```"
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Teams
# ---------------------------------------------------------------------------

def format_teams(teams, fmt="text"):
    """Format teams data. teams is a dict keyed by team_key."""
    team_list = list(teams.values()) if isinstance(teams, dict) else teams

    if fmt == "json":
        items = []
        for team in team_list:
            items.append({
                "team_id": _team_id(team),
                "name": str(_team_name(team)),
                "manager": str(_manager_name(team)),
                "waiver_priority": _safe(team, "waiver_priority", ""),
                "moves": _safe(team, "number_of_moves", ""),
                "trades": _safe(team, "number_of_trades", ""),
            })
        return json.dumps({"teams": items}, indent=2)

    lines = ["League Teams"]
    lines.append(f"{'ID':<5} {'Team Name':<30} {'Manager':<20}")
    lines.append("-" * 58)
    for team in team_list:
        tid = str(_team_id(team))[:4]
        name = str(_team_name(team))[:29]
        mgr = str(_manager_name(team))[:19]
        lines.append(f"{tid:<5} {name:<30} {mgr:<20}")

    if fmt == "discord":
        return "```\n" + "\n".join(lines) + "\n```"
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Roster
# ---------------------------------------------------------------------------

def format_roster(players, team_name="", fmt="text"):
    if fmt == "json":
        items = []
        for p in players:
            items.append({
                "name": _player_name(p),
                "player_id": _player_id(p),
                "positions": _player_position(p),
                "selected_position": _player_selected_position(p),
                "team": _player_team(p),
                "status": _player_status(p),
            })
        return json.dumps({"team": team_name, "roster": items}, indent=2)

    lines = []
    if team_name:
        lines.append(f"Roster — {team_name}")
    lines.append(f"{'Name':<25} {'Pos':<12} {'Slot':<5} {'Team':<6} {'Status':<6}")
    lines.append("-" * 58)
    for p in players:
        name = _player_name(p)[:24]
        pos = _player_position(p)[:11]
        slot = _player_selected_position(p)[:4]
        team = _player_team(p)[:5]
        status = _player_status(p)[:5]
        lines.append(f"{name:<25} {pos:<12} {slot:<5} {team:<6} {status:<6}")

    if fmt == "discord":
        return "```\n" + "\n".join(lines) + "\n```"
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Standings
# ---------------------------------------------------------------------------

def format_standings(standings, fmt="text"):
    """Format standings. standings is an ordered list of team dicts."""
    if fmt == "json":
        items = []
        for i, team in enumerate(standings, 1):
            outcome = _safe(team, "outcome_totals", {})
            items.append({
                "rank": i,
                "team_id": _team_id(team),
                "name": _team_name(team),
                "wins": _safe(outcome, "wins") if outcome else "",
                "losses": _safe(outcome, "losses") if outcome else "",
                "ties": _safe(outcome, "ties") if outcome else "",
                "percentage": _safe(outcome, "percentage") if outcome else "",
                "games_back": _safe(team, "games_back", ""),
                "playoff_seed": _safe(team, "playoff_seed", ""),
            })
        return json.dumps({"standings": items}, indent=2)

    lines = ["League Standings"]
    lines.append(f"{'Rank':<6} {'Team':<30} {'W':<5} {'L':<5} {'T':<5} {'GB':<6} {'Pct':<6}")
    lines.append("-" * 66)
    for i, team in enumerate(standings, 1):
        outcome = _safe(team, "outcome_totals", {})
        name = _team_name(team)[:29]
        wins = _safe(outcome, "wins") if outcome else ""
        losses = _safe(outcome, "losses") if outcome else ""
        ties = _safe(outcome, "ties") if outcome else ""
        gb = _safe(team, "games_back", "")
        pct = _safe(outcome, "percentage") if outcome else ""
        lines.append(f"{i:<6} {name:<30} {wins:<5} {losses:<5} {ties:<5} {gb:<6} {pct:<6}")

    if fmt == "discord":
        return "```\n" + "\n".join(lines) + "\n```"
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Matchup
# ---------------------------------------------------------------------------

def format_matchup(opponent_key, my_team_name="", opponent_name="", week=None, fmt="text"):
    """Format a single matchup (opponent key from team.matchup())."""
    if fmt == "json":
        return json.dumps({
            "week": week,
            "team": my_team_name,
            "opponent": opponent_name,
            "opponent_key": opponent_key,
        }, indent=2)

    lines = []
    header = "Matchup"
    if week:
        header += f" — Week {week}"
    lines.append(header)
    lines.append("-" * 50)
    lines.append(f"{my_team_name} vs {opponent_name}")

    if fmt == "discord":
        return "```\n" + "\n".join(lines) + "\n```"
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Scoreboard
# ---------------------------------------------------------------------------

def format_scoreboard(scoreboard_data, week=None, fmt="text"):
    """Format scoreboard. scoreboard_data is raw matchups() output from yahoo-fantasy-api."""
    # The raw data from league.matchups() is complex nested Yahoo API JSON
    # We need to extract matchups from it
    matchups = _extract_matchups_from_raw(scoreboard_data)

    if fmt == "json":
        return json.dumps({"week": week, "scoreboard": matchups}, indent=2)

    lines = []
    header = "League Scoreboard"
    if week:
        header += f" — Week {week}"
    lines.append(header)
    lines.append("-" * 60)

    for m in matchups:
        teams = m.get("teams", [])
        status = m.get("status", "")
        if len(teams) >= 2:
            t1 = teams[0]
            t2 = teams[1]
            n1 = t1.get("name", "?")
            n2 = t2.get("name", "?")
            p1 = t1.get("points", "0")
            p2 = t2.get("points", "0")
            status_label = "In progress" if status == "midevent" else (
                "Final" if status == "postevent" else "")
            lines.append(f"  {n1:<30} {p1:>3}  vs  {p2:<3} {n2}")
            if status_label:
                lines.append(f"  {'':>34}{status_label}")
            lines.append("")

    if not matchups:
        lines.append("  No matchup data available.")

    if fmt == "discord":
        return "```\n" + "\n".join(lines) + "\n```"
    return "\n".join(lines)


def _extract_matchups_from_raw(raw):
    """Extract matchup data from raw Yahoo API scoreboard JSON.

    The structure from league.matchups() is deeply nested Yahoo API JSON.
    We navigate it to extract team names and points.
    """
    matchups = []
    if not raw or not isinstance(raw, dict):
        return matchups

    # Navigate: fantasy_content -> league -> scoreboard -> matchups
    fc = raw.get("fantasy_content", raw)
    league = fc.get("league", fc)

    # league can be a list in Yahoo's format
    scoreboard = None
    if isinstance(league, list):
        for item in league:
            if isinstance(item, dict) and "scoreboard" in item:
                scoreboard = item["scoreboard"]
                break
    elif isinstance(league, dict):
        scoreboard = league.get("scoreboard", league)

    if not scoreboard:
        return matchups

    # Get matchups — Yahoo wraps them as scoreboard -> "0" -> matchups -> ...
    raw_matchups = None
    if isinstance(scoreboard, dict):
        raw_matchups = scoreboard.get("matchups")
        if raw_matchups is None:
            # Try numeric wrapper: scoreboard -> "0" -> matchups
            wrapper = scoreboard.get("0")
            if isinstance(wrapper, dict):
                raw_matchups = wrapper.get("matchups", wrapper)
        if raw_matchups is None:
            raw_matchups = scoreboard

    if isinstance(raw_matchups, dict):
        count = int(raw_matchups.get("count", 0))
        for i in range(count):
            m_key = str(i)
            m_data = raw_matchups.get(m_key, {})
            if isinstance(m_data, dict):
                matchup = m_data.get("matchup", m_data)
                matchups.append(_parse_single_matchup(matchup))
    elif isinstance(raw_matchups, list):
        for item in raw_matchups:
            if isinstance(item, dict):
                matchup = item.get("matchup", item)
                matchups.append(_parse_single_matchup(matchup))

    return matchups


def _parse_single_matchup(matchup):
    """Parse a single matchup from the raw API into a clean dict."""
    result = {"teams": [], "week": "", "status": ""}

    if not isinstance(matchup, dict):
        return result

    result["week"] = matchup.get("week", "")
    result["status"] = matchup.get("status", "")

    # Teams may be at matchup["teams"] or matchup["0"]["teams"]
    raw_teams = matchup.get("teams")
    if raw_teams is None:
        wrapper = matchup.get("0")
        if isinstance(wrapper, dict):
            raw_teams = wrapper.get("teams", wrapper)
    if raw_teams is None:
        raw_teams = matchup

    if isinstance(raw_teams, dict):
        for key in ("0", "1"):
            team_wrapper = raw_teams.get(key, {})
            if isinstance(team_wrapper, dict):
                team = team_wrapper.get("team", team_wrapper)
                result["teams"].append(_parse_scoreboard_team(team))
    elif isinstance(raw_teams, list):
        for item in raw_teams:
            if isinstance(item, dict):
                team = item.get("team", item)
                result["teams"].append(_parse_scoreboard_team(team))

    return result


def _parse_scoreboard_team(team_data):
    """Parse a team entry from scoreboard data."""
    info = {"name": "?", "team_id": "?", "points": "0"}

    if isinstance(team_data, list):
        # Yahoo nests team as [list-of-metadata-dicts, stats-dict]
        # Flatten: expand any inner lists so we iterate all dicts
        flat = []
        for item in team_data:
            if isinstance(item, list):
                flat.extend(item)
            else:
                flat.append(item)
        for item in flat:
            if isinstance(item, dict):
                if "name" in item:
                    info["name"] = item["name"]
                if "team_id" in item:
                    info["team_id"] = item["team_id"]
                if "team_points" in item:
                    tp = item["team_points"]
                    info["points"] = tp.get("total", "0") if isinstance(tp, dict) else "0"
    elif isinstance(team_data, dict):
        info["name"] = team_data.get("name", "?")
        info["team_id"] = team_data.get("team_id", "?")
        tp = team_data.get("team_points", {})
        if isinstance(tp, dict):
            info["points"] = tp.get("total", "0")

    return info


# ---------------------------------------------------------------------------
# Lineup (roster + matchup context + categories)
# ---------------------------------------------------------------------------

def format_lineup(players, categories, matchup_info=None, team_name="", fmt="text"):
    if fmt == "json":
        items = []
        for p in players:
            stats = _extract_player_stats(p)
            items.append({
                "name": _player_name(p),
                "player_id": _player_id(p),
                "positions": _player_position(p),
                "team": _player_team(p),
                "status": _player_status(p),
                "selected_position": _player_selected_position(p),
                "stats": stats,
            })
        result = {
            "team": team_name,
            "categories": categories,
            "players": items,
        }
        if matchup_info:
            result["matchup"] = matchup_info
        return json.dumps(result, indent=2)

    lines = []
    if team_name:
        lines.append(f"Lineup — {team_name}")

    # Build stat header from categories
    cat_abbrs = [c.get("abbr", c.get("name", "?"))[:5] for c in categories[:12]]
    stat_header = "  ".join(f"{a:<5}" for a in cat_abbrs)
    lines.append(f"{'Name':<22} {'Pos':<5} {'Slot':<5} {'Team':<5} {stat_header}")
    lines.append("-" * (42 + len(stat_header)))

    cat_ids = [c.get("stat_id") for c in categories[:12]]
    for p in players:
        name = _player_name(p)[:21]
        pos = _player_position(p)[:4]
        sel_pos = _player_selected_position(p)[:4]
        team = _player_team(p)[:4]
        stats = _extract_player_stats(p)
        stat_vals = "  ".join(f"{str(stats.get(sid, '-')):<5}" for sid in cat_ids)
        lines.append(f"{name:<22} {pos:<5} {sel_pos:<5} {team:<5} {stat_vals}")

    if fmt == "discord":
        return "```\n" + "\n".join(lines) + "\n```"
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Players (free agents / search)
# ---------------------------------------------------------------------------

def _ownership_label(player):
    """Convert ownership_type to a short display label."""
    otype = _safe(player, "ownership_type", "")
    if otype == "freeagents":
        return "FA"
    elif otype == "waivers":
        return "W"
    elif otype == "team":
        owner = _safe(player, "owner_team_name", "")
        return owner if owner else "Owned"
    return ""


def format_players(players, categories=None, fmt="text"):
    # Check if any player has ownership data
    has_ownership = any(_safe(p, "ownership_type", "") for p in players)
    has_stats = bool(categories)

    if fmt == "json":
        items = []
        for p in players:
            item = {
                "name": _player_name(p),
                "player_id": _player_id(p),
                "positions": _player_position(p),
                "team": _player_team(p),
                "status": _player_status(p),
                "percent_owned": _safe(p, "percent_owned", ""),
            }
            if has_ownership:
                item["ownership"] = _safe(p, "ownership_type", "")
                item["owner"] = _safe(p, "owner_team_name", "")
            if has_stats:
                stats = _extract_player_stats(p)
                item["stats"] = stats
            items.append(item)
        return json.dumps({"players": items}, indent=2)

    lines = ["Available Players"]

    # Build header
    base_cols = f"{'Name':<25} {'Pos':<12} {'Team':<6} {'Status':<6}"
    if has_ownership:
        base_cols += f" {'%Own':<5} {'Owner':<12}"
    else:
        base_cols += f" {'%Own':<5}"

    if has_stats:
        cat_abbrs = [c.get("abbr", c.get("name", "?"))[:6] for c in categories]
        stat_header = "  ".join(f"{a:>6}" for a in cat_abbrs)
        lines.append(f"{base_cols}  {stat_header}")
    else:
        lines.append(base_cols)
    lines.append("-" * len(lines[-1]))

    cat_ids = [c.get("stat_id") for c in categories] if has_stats else []
    for p in players:
        name = _player_name(p)[:24]
        pos = _player_position(p)[:11]
        team = _player_team(p)[:5]
        status = _player_status(p)[:5]
        pct_owned = _safe(p, "percent_owned", "")
        pct = f"{pct_owned}%" if pct_owned != "" else ""

        row = f"{name:<25} {pos:<12} {team:<6} {status:<6}"
        if has_ownership:
            owner = _ownership_label(p)[:12]
            row += f" {pct:<5} {owner:<12}"
        else:
            row += f" {pct:<5}"

        if has_stats:
            stats = _extract_player_stats(p)
            stat_vals = "  ".join(f"{str(stats.get(sid, '-')):>6}" for sid in cat_ids)
            row += f"  {stat_vals}"

        lines.append(row)

    if fmt == "discord":
        return "```\n" + "\n".join(lines) + "\n```"
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Draft
# ---------------------------------------------------------------------------

def format_draft(picks, fmt="text"):
    if fmt == "json":
        items = []
        for pick in picks:
            items.append({
                "round": _safe(pick, "round"),
                "pick": _safe(pick, "pick"),
                "team_key": _safe(pick, "team_key"),
                "team_name": _safe(pick, "team_name"),
                "player_id": _safe(pick, "player_id"),
                "player_name": _safe(pick, "player_name"),
                "player_position": _safe(pick, "player_position"),
            })
        return json.dumps({"draft_results": items}, indent=2)

    lines = ["Draft Results"]
    lines.append(f"{'Round':<7} {'Pick':<6} {'Pos':<10} {'Player':<26} {'Team'}")
    lines.append("-" * 75)
    for pick in picks:
        rd = _safe(pick, "round")
        pk = _safe(pick, "pick")
        pos = _safe(pick, "player_position")
        player = _safe(pick, "player_name") or str(_safe(pick, "player_id"))
        team = _safe(pick, "team_name") or _safe(pick, "team_key")
        lines.append(f"{rd:<7} {pk:<6} {pos:<10} {player:<26} {team}")

    if fmt == "discord":
        return "```\n" + "\n".join(lines) + "\n```"
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Transactions
# ---------------------------------------------------------------------------

def format_transactions(transactions, fmt="text"):
    parsed = _parse_all_transactions(transactions)

    if fmt == "json":
        return json.dumps({"transactions": parsed}, indent=2)

    lines = ["Recent Transactions"]
    lines.append("-" * 60)
    for txn in parsed:
        ts = txn.get("date", "")
        txn_type = txn.get("type", "")
        team = txn.get("team", "")
        header_parts = [p for p in [txn_type, team, ts] if p]
        lines.append(" | ".join(header_parts))
        for p in txn.get("players", []):
            action = p.get("action", "")
            name = p.get("name", "Unknown")
            detail = p.get("detail", "")
            prefix = f"  {action + ':':<20}" if action else "  "
            suffix = f" ({detail})" if detail else ""
            lines.append(f"{prefix}{name}{suffix}")
        lines.append("")

    if fmt == "discord":
        return "```\n" + "\n".join(lines) + "\n```"
    return "\n".join(lines)


def _parse_all_transactions(transactions):
    """Parse raw Yahoo transaction list into clean dicts."""
    import datetime
    results = []
    for txn in transactions:
        entry = {
            "type": _safe(txn, "type"),
            "status": _safe(txn, "status"),
            "timestamp": _safe(txn, "timestamp"),
            "team": "",
            "date": "",
            "players": [],
        }
        # Convert timestamp to readable date
        ts = _safe(txn, "timestamp")
        if ts:
            try:
                dt = datetime.datetime.fromtimestamp(int(ts))
                entry["date"] = dt.strftime("%b %d, %I:%M %p").lstrip("0")
            except (ValueError, OSError):
                pass

        raw_players = _safe(txn, "players", {})
        if isinstance(raw_players, dict):
            for key in sorted(raw_players.keys()):
                if key == "count":
                    continue
                wrapper = raw_players[key]
                if not isinstance(wrapper, dict):
                    continue
                player_data = wrapper.get("player", wrapper)
                info = _parse_txn_player(player_data)
                entry["players"].append(info)
                # Use first team name found as the transaction team
                if not entry["team"] and info.get("team_name"):
                    entry["team"] = info["team_name"]

        results.append(entry)
    return results


def _parse_txn_player(player_data):
    """Parse a single player from transaction data."""
    info = {"name": "Unknown", "action": "", "detail": "", "team_name": ""}

    # player_data is [list-of-metadata-dicts, {transaction_data: [...]}]
    flat = []
    if isinstance(player_data, list):
        for item in player_data:
            if isinstance(item, list):
                flat.extend(item)
            else:
                flat.append(item)
    elif isinstance(player_data, dict):
        flat = [player_data]

    merged = {}
    txn_data = {}
    for item in flat:
        if not isinstance(item, dict):
            continue
        if "transaction_data" in item:
            td = item["transaction_data"]
            if isinstance(td, list) and td:
                txn_data = td[0] if isinstance(td[0], dict) else {}
            elif isinstance(td, dict):
                txn_data = td
        else:
            merged.update(item)

    info["name"] = _player_name(merged)
    team_abbr = merged.get("editorial_team_abbr", "")
    pos = merged.get("display_position", "")
    if team_abbr or pos:
        info["detail"] = f"{team_abbr} - {pos}" if team_abbr and pos else (team_abbr or pos)

    action_type = txn_data.get("type", "")
    source = txn_data.get("source_type", "")
    dest_team = txn_data.get("destination_team_name", "")
    source_team = txn_data.get("source_team_name", "")

    if action_type == "add":
        source_label = "Free Agent" if source == "freeagents" else ("Waivers" if source == "waivers" else source)
        info["action"] = f"Add from {source_label}"
        info["team_name"] = dest_team
    elif action_type == "drop":
        info["action"] = "Drop"
        info["team_name"] = source_team
    else:
        info["action"] = action_type
        info["team_name"] = dest_team or source_team

    return info


# ---------------------------------------------------------------------------
# Injuries (filtered roster view)
# ---------------------------------------------------------------------------

def format_injuries(players, team_name="", fmt="text"):
    injured = [p for p in players if _player_status(p)]

    if fmt == "json":
        items = []
        for p in injured:
            items.append({
                "name": _player_name(p),
                "player_id": _player_id(p),
                "positions": _player_position(p),
                "team": _player_team(p),
                "status": _player_status(p),
            })
        return json.dumps({"team": team_name, "injured_players": items}, indent=2)

    if not injured:
        return "No injured players on roster."

    lines = []
    if team_name:
        lines.append(f"Injured Players — {team_name}")
    lines.append(f"{'Name':<25} {'Pos':<12} {'Team':<6} {'Status'}")
    lines.append("-" * 55)
    for p in injured:
        name = _player_name(p)[:24]
        pos = _player_position(p)[:11]
        team = _player_team(p)[:5]
        status = _player_status(p)
        lines.append(f"{name:<25} {pos:<12} {team:<6} {status}")

    if fmt == "discord":
        return "```\n" + "\n".join(lines) + "\n```"
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Today (daily roster status with MLB schedule)
# ---------------------------------------------------------------------------

def format_today(groups, probable_starters, team_name="", fmt="text",
                  date_str=None, matchups=None, game_times=None,
                  first_pitch=None):
    """Format the today/day command output.

    Args:
        groups: dict with keys 'active', 'not_playing', 'injured', 'bench',
                each a list of player dicts.
        probable_starters: set of player names who are probable starters.
        team_name: Team display name.
        fmt: Output format.
        date_str: Date string (YYYY-MM-DD). If today or None, header says "Today".
        matchups: dict mapping MLB team abbr -> matchup string (e.g. "at SF", "vs NYY").
        game_times: dict mapping MLB team abbr -> formatted local time string.
        first_pitch: formatted time of the earliest game, or None.
    """
    if matchups is None:
        matchups = {}
    if game_times is None:
        game_times = {}
    from datetime import date as _date

    # Determine header label
    today_str = _date.today().strftime("%Y-%m-%d")
    if not date_str or date_str == today_str:
        date_label = "Today"
    else:
        d = _date.fromisoformat(date_str)
        try:
            date_label = d.strftime("%a %b %-d")
        except ValueError:
            # Windows doesn't support %-d
            date_label = f"{d.strftime('%a %b')} {d.day}"

    if fmt == "json":
        def _player_entry(p, is_probable=False):
            import mlb_client
            team_abbr = _player_team(p)
            mlb_abbr = mlb_client.normalize_team_abbr(team_abbr)
            entry = {
                "name": _player_name(p),
                "player_id": _player_id(p),
                "positions": _player_position(p),
                "selected_position": _player_selected_position(p),
                "team": team_abbr,
                "opponent": matchups.get(mlb_abbr, ""),
                "game_time": game_times.get(mlb_abbr, ""),
                "status": _player_status(p),
            }
            if is_probable:
                entry["probable_starter"] = True
            elif "SP" in (entry["positions"] or "").split(","):
                entry["probable_starter"] = False
            return entry

        result = {"team": team_name, "date": date_str or today_str,
                  "first_pitch": first_pitch or "", "groups": {}}
        for group_name in ("active", "not_playing", "bench", "injured"):
            result["groups"][group_name] = [
                _player_entry(p, _player_name(p) in probable_starters)
                for p in groups.get(group_name, [])
            ]
        return json.dumps(result, indent=2)

    lines = []
    if team_name:
        lines.append(f"{date_label} — {team_name}")
    if first_pitch:
        lines.append(f"  First pitch: {first_pitch}")
    lines.append("")

    section_labels = [
        ("active", "ACTIVE (team playing today)"),
        ("not_playing", "NOT PLAYING (team off today)"),
        ("bench", "BENCH"),
        ("injured", "INJURED LIST"),
    ]

    for group_key, label in section_labels:
        players = groups.get(group_key, [])
        lines.append(f"  {label} ({len(players)})")
        if players:
            import mlb_client
            for p in players:
                name = _player_name(p)
                pos = _player_position(p) or _player_selected_position(p)
                team = _player_team(p)
                mlb_abbr = mlb_client.normalize_team_abbr(team)
                opp = matchups.get(mlb_abbr, "")
                game_time = game_times.get(mlb_abbr, "")
                opp_time = f"{opp} {game_time}".strip() if opp else ""
                status = _player_status(p)
                extra = ""
                if name in probable_starters:
                    extra = " [PROBABLE STARTER]"
                elif "SP" in (pos or "").split(","):
                    extra = " [NOT STARTING]"
                if status:
                    extra += f" ({status})"
                lines.append(f"    {name:<22} {pos:<14} {team:<5}{opp_time:<18}{extra}")
        else:
            lines.append("    (none)")
        lines.append("")

    if fmt == "discord":
        return "```\n" + "\n".join(lines) + "\n```"
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Optimize (roster analysis + suggestions)
# ---------------------------------------------------------------------------

def format_optimize(suggestions, fmt="text"):
    """Format optimize command output.

    Args:
        suggestions: dict with keys 'moves', 'pitcher_alerts', 'il_moves',
                     each a list of suggestion dicts.
        fmt: Output format.
    """
    if fmt == "json":
        return json.dumps({"suggestions": suggestions}, indent=2)

    lines = ["Roster Optimization Suggestions"]
    lines.append("=" * 50)

    # Lineup changes (grouped swaps)
    swap_groups = suggestions.get("swap_groups", [])
    lines.append("")
    swap_label = "swap" if len(swap_groups) == 1 else "swaps"
    lines.append(f"  LINEUP CHANGES ({len(swap_groups)} {swap_label})")
    if swap_groups:
        for i, group in enumerate(swap_groups, 1):
            lines.append("")
            lines.append(f"    Swap {i} — {group['label']}")
            for m in group.get("start", []):
                opp_str = f" vs {m['opponent']}" if m.get("opponent") else ""
                slot_note = f" at {m['to_slot']}" if group.get("reshuffle") else ""
                status_str = f", {m['status']}" if m.get("status") else ""
                lines.append(f"      ▶ Start {m['player']}{slot_note} ({m['team']}{opp_str}{status_str}, score: {m['score']})")
                if (m.get("status") or "").upper() == "DTD":
                    lines.append(f"        ⚠️  Day-to-day — confirm in lineup before locking.")
            for m in group.get("reshuffle", []):
                lines.append(f"      ↔ Move {m['player']} from {m['from_slot']} → {m['to_slot']}")
            for m in group.get("bench", []):
                opp_str = f" vs {m['opponent']}" if m.get("opponent") else ""
                status_str = f", {m['status']}" if m.get("status") else ""
                lines.append(f"      ▼ Bench {m['player']} ({m['team']}{opp_str}{status_str}, score: {m['score']})")
                reason = m.get("reason", "")
                if reason:
                    if "not in confirmed" in reason.lower():
                        lines.append(f"        ⚠️  {reason}")
                    elif "already started" in reason.lower():
                        lines.append(f"        🔒  {reason}")
                    elif "off today" in reason.lower():
                        lines.append(f"        📅  {reason}")
                    else:
                        lines.append(f"        💡  {reason}")
    else:
        lines.append("    No lineup changes needed — lineup looks good.")

    # Pitcher rotation (swap groups + alerts)
    pitcher_swap_groups = suggestions.get("pitcher_swap_groups", [])
    pitcher_alerts = suggestions.get("pitcher_alerts", [])
    p_swap_label = "swap" if len(pitcher_swap_groups) == 1 else "swaps"
    lines.append("")
    lines.append(f"  PITCHER ROTATION ({len(pitcher_swap_groups)} {p_swap_label})")
    if pitcher_swap_groups:
        for i, group in enumerate(pitcher_swap_groups, 1):
            lines.append("")
            lines.append(f"    Swap {i} — {group['label']}")
            for m in group.get("start", []):
                opp_str = f" vs {m['opponent']}" if m.get("opponent") else ""
                slot_note = f" at {m['to_slot']}" if group.get("reshuffle") else ""
                reason_str = f" — {m['reason']}" if m.get("reason") else ""
                status_str = f", {m['status']}" if m.get("status") else ""
                lines.append(f"      ▶ Start {m['player']}{slot_note} ({m['team']}{opp_str}{status_str}, score: {m['score']}){reason_str}")
                if (m.get("status") or "").upper() == "DTD":
                    lines.append(f"        ⚠️  Day-to-day — confirm in lineup before locking.")
            for m in group.get("reshuffle", []):
                lines.append(f"      ↔ Move {m['player']} from {m['from_slot']} → {m['to_slot']}")
            for m in group.get("bench", []):
                opp_str = f" vs {m['opponent']}" if m.get("opponent") else ""
                status_str = f", {m['status']}" if m.get("status") else ""
                lines.append(f"      ▼ Bench {m['player']} ({m['team']}{opp_str}{status_str}, score: {m['score']})")
                reason = m.get("reason", "")
                if reason:
                    if "off today" in reason.lower():
                        lines.append(f"        📅  {reason}")
                    elif "not starting" in reason.lower():
                        lines.append(f"        💡  {reason}")
                    else:
                        lines.append(f"        💡  {reason}")
    if pitcher_alerts:
        for a in pitcher_alerts:
            lines.append(f"    ⚠  {a['message']}")
    if not pitcher_swap_groups and not pitcher_alerts:
        lines.append("    No pitcher rotation changes needed.")

    # IL moves
    il_moves = suggestions.get("il_moves", [])
    lines.append("")
    lines.append(f"  IL MANAGEMENT ({len(il_moves)} suggested)")
    if il_moves:
        for m in il_moves:
            lines.append(f"    {m['message']}")
    else:
        lines.append("    No IL moves needed.")

    lines.append("")
    total = len(swap_groups) + len(pitcher_swap_groups) + len(pitcher_alerts) + len(il_moves)
    lines.append(f"Total: {total} suggestion(s)")

    if fmt == "discord":
        return "```\n" + "\n".join(lines) + "\n```"
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Lineup Check (confirmed MLB lineups vs fantasy roster)
# ---------------------------------------------------------------------------

def format_lineup_check(data, fmt="text"):
    """Format lineup-check command output.

    Args:
        data: dict with keys 'date', 'team', 'sitting_players',
              'lineup_not_posted', 'players_confirmed'.
        fmt: Output format.
    """
    if fmt == "json":
        return json.dumps(data, indent=2)

    lines = [f"Lineup Check — {data['date']}"]
    lines.append(f"Team: {data['team']}")
    lines.append("=" * 50)

    sitting = data.get("sitting_players", [])
    if sitting:
        lines.append(f"\nNOT in confirmed MLB lineup ({len(sitting)}):")
        for p in sitting:
            status_note = f" [Yahoo: {p['yahoo_status']}]" if p.get("yahoo_status") else ""
            lines.append(
                f"  {p['selected_position']}: {p['name']} ({p['team']}) "
                f"— {p.get('opponent', '')} {p.get('game_time', '')}{status_note}"
            )
    else:
        lines.append("\nAll active position players confirmed in lineup.")

    confirmed = data.get("players_confirmed", 0)
    lines.append(f"\nConfirmed in lineup: {confirmed}")

    not_posted = data.get("lineup_not_posted", [])
    if not_posted:
        lines.append(f"Lineups not yet posted: {', '.join(not_posted)}")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Standouts (yesterday's top performers)
# ---------------------------------------------------------------------------

def format_standouts(top_performers, left_on_bench, date_str, categories=None,
                     fmt="text"):
    """Format the standouts command output.

    Args:
        top_performers: list of player dicts (active lineup), sorted by points desc.
        left_on_bench: list of player dicts (benched), sorted by points desc.
        date_str: Date string (YYYY-MM-DD).
        categories: list of category dicts from _extract_categories_from_settings.
        fmt: Output format.
    """
    if fmt == "json":
        def _entry(p):
            stats = _extract_player_stats(p)
            # Remove internal keys from stats
            stats.pop("total_points", None)
            stats.pop("_fantasy_team", None)
            stats.pop("_achievements", None)
            stats.pop("_standout_score", None)
            # Build key_stats — keep non-zero values, preserve strings like H/AB
            key_stats = {}
            for k, v in stats.items():
                if k.startswith("_"):
                    continue
                if isinstance(v, str) and "/" in v:
                    # Composite stat like H/AB — keep as string if non-zero
                    if not v.startswith("0/"):
                        key_stats[k] = v
                    continue
                try:
                    fv = float(v)
                except (ValueError, TypeError):
                    continue
                if fv != 0:
                    key_stats[k] = fv if fv != int(fv) else int(fv)
            return {
                "name": _player_name(p),
                "team": _safe(p, "_fantasy_team", ""),
                "mlb_team": _player_team(p),
                "position": _player_selected_position(p) or _player_position(p),
                "score": _safe(p, "_standout_score", 0),
                "achievements": _safe(p, "_achievements", []),
                "key_stats": key_stats,
            }

        result = {
            "date": date_str,
            "top_performers": [_entry(p) for p in top_performers],
            "left_on_bench": [_entry(p) for p in left_on_bench],
        }
        return json.dumps(result, indent=2)

    # Text / discord format
    from datetime import date as _date
    try:
        d = _date.fromisoformat(date_str)
        try:
            date_label = d.strftime("%a %b %-d")
        except ValueError:
            date_label = f"{d.strftime('%a %b')} {d.day}"
    except Exception:
        date_label = date_str

    lines = [f"Standout Performers — {date_label}"]
    lines.append("=" * 50)

    def _format_player_line(p, idx):
        name = _player_name(p)
        pos = _player_selected_position(p) or _player_position(p)
        mlb = _player_team(p)
        team = _safe(p, "_fantasy_team", "")
        score = _safe(p, "_standout_score", 0)
        stats = _extract_player_stats(p)
        achievements = _safe(p, "_achievements", [])

        # Build stat line with non-zero stats
        stat_parts = []
        for k, v in stats.items():
            if k.startswith("_") or k in ("total_points",):
                continue
            if isinstance(v, str) and "/" in v:
                # Composite stat like H/AB
                if not v.startswith("0/"):
                    stat_parts.append(f"{v} {k}")
                continue
            try:
                fv = float(v)
            except (ValueError, TypeError):
                continue
            if fv != 0:
                display = f"{int(fv)}" if fv == int(fv) else f"{fv:.3f}"
                stat_parts.append(f"{display} {k}")
        stat_line = ", ".join(stat_parts) if stat_parts else ""

        ach_str = f"  [{', '.join(achievements)}]" if achievements else ""
        lines.append(f"  {idx}. {name} ({pos}, {mlb}) — {team}")
        lines.append(f"     {stat_line}{ach_str}")

    if top_performers:
        lines.append("")
        lines.append(f"  TOP PERFORMERS ({len(top_performers)})")
        for i, p in enumerate(top_performers, 1):
            _format_player_line(p, i)
    else:
        lines.append("")
        lines.append("  TOP PERFORMERS")
        lines.append("    No standout performances.")

    if left_on_bench:
        lines.append("")
        lines.append(f"  LEFT ON THE BENCH ({len(left_on_bench)})")
        for i, p in enumerate(left_on_bench, 1):
            _format_player_line(p, i)

    lines.append("")

    if fmt == "discord":
        return "```\n" + "\n".join(lines) + "\n```"
    return "\n".join(lines)

#!/usr/bin/env python3
"""ZERO Skill Validation -- parse SKILL.md and verify claims against engine code.
Exit 0 if all pass, 1 if any fail."""
from __future__ import annotations

import re
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent.parent.parent.parent

SKILL_MD = BASE / "scanner" / "skills" / "zero-trading" / "SKILL.md"
AUTH_PY = BASE / "scanner" / "v6" / "auth.py"
MCP_PY = BASE / "scanner" / "v6" / "mcp_server.py"
CARD_API = BASE / "scanner" / "v6" / "cards" / "card_api.py"
STRAT_DIR = BASE / "scanner" / "v6" / "strategies"
STRAT_MD = BASE / "scanner" / "skills" / "zero-trading" / "references" / "strategies.md"


# ── Parsers ────────────────────────────────────────────────────────────────


def parse_skill_tools(text: str) -> dict[str, str]:
    """Extract tool -> tier from SKILL.md tool tables."""
    tools: dict[str, str] = {}
    for m in re.finditer(r"\|\s*`(zero_\w+)`\s*\|\s*(\w+)\s*\|", text):
        tools[m.group(1)] = m.group(2)
    return tools


def parse_skill_tool_count(text: str) -> int | None:
    """Extract claimed tool count from '## tools available (N tools)'."""
    m = re.search(r"tools available\s*\((\d+)\s*tools?\)", text)
    return int(m.group(1)) if m else None


def parse_skill_cards(text: str) -> list[str]:
    """Extract card endpoints from the visual cards table."""
    cards: list[str] = []
    in_cards = False
    for line in text.splitlines():
        if "## visual cards" in line.lower():
            in_cards = True
            continue
        if in_cards and line.startswith("##"):
            break
        if not in_cards:
            continue
        parts = [p.strip() for p in line.split("|")]
        if len(parts) >= 3:
            ep = parts[1].strip("`").strip()
            if ep.startswith("/v6/cards/"):
                cards.append(ep.split("?")[0])
    return cards


def parse_auth_tiers(text: str) -> dict[str, str]:
    """Extract TOOL_TIERS dict from auth.py."""
    tiers: dict[str, str] = {}
    in_block = False
    for line in text.splitlines():
        if "TOOL_TIERS" in line and "{" in line:
            in_block = True
            continue
        if in_block:
            if line.strip() == "}":
                break
            m = re.match(r'\s*"(\w+)"\s*:\s*"(\w+)"', line)
            if m:
                tiers[m.group(1)] = m.group(2)
    return tiers


def parse_mcp_tools(text: str) -> list[str]:
    """Extract @mcp.tool() decorated function names."""
    tools: list[str] = []
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if "@mcp.tool()" in line:
            for j in range(i + 1, min(i + 5, len(lines))):
                m = re.match(r"\s*(?:async\s+)?def\s+(\w+)\s*\(", lines[j])
                if m:
                    tools.append(m.group(1))
                    break
    return tools


def parse_card_endpoints(text: str) -> list[str]:
    """Extract @router.get() endpoints from card_api.py."""
    return [
        "/v6/cards" + m.group(1)
        for m in re.finditer(r'@router\.get\(\s*"([^"]+)"\s*\)', text)
    ]


def load_yaml(path: Path) -> dict:
    """Load YAML. Try yaml.safe_load, fall back to regex."""
    text = path.read_text()
    try:
        import yaml
        return yaml.safe_load(text) or {}
    except ImportError:
        pass
    data: dict = {"risk": {}, "session": {}}
    def _get(key: str) -> str | None:
        m = re.search(rf"^\s*{key}\s*:\s*(.+?)(?:\s*#.*)?$", text, re.MULTILINE)
        return m.group(1).strip().strip("'\"") if m else None
    data["name"], data["tier"] = _get("name"), _get("tier")
    for f in ("stop_loss_pct", "max_positions", "position_size_pct", "max_daily_loss_pct"):
        v = _get(f)
        if v is not None:
            try:
                data["risk"][f] = float(v) if "." in v else int(v)
            except ValueError:
                data["risk"][f] = v
    dh = _get("duration_hours")
    if dh is not None:
        try:
            data["session"]["duration_hours"] = int(dh)
        except ValueError:
            data["session"]["duration_hours"] = dh
    return data


def parse_strategies_md(text: str) -> dict[str, dict]:
    """Parse the strategy quick reference table."""
    strategies: dict[str, dict] = {}
    in_table = False
    for line in text.splitlines():
        if "strategy quick reference" in line.lower():
            in_table = True
            continue
        if in_table and line.startswith("##"):
            break
        if not in_table or not line.strip().startswith("|"):
            continue
        parts = [p.strip() for p in line.split("|")]
        if len(parts) < 11:
            continue
        name = parts[1]
        if name in ("strategy", "---", ""):
            continue

        def _num(s: str) -> float | None:
            s = s.rstrip("%").rstrip("h").strip()
            if s in ("\u2014", ""):
                return None
            try:
                return float(s)
            except ValueError:
                return None

        strategies[name] = {
            "tier": parts[2],
            "stop_loss_pct": _num(parts[3]),
            "max_positions": _num(parts[4]),
            "duration_hours": _num(parts[5]),
            "position_size_pct": _num(parts[6]),
            "max_daily_loss_pct": _num(parts[8]),
        }
    return strategies


# ── Validation ─────────────────────────────────────────────────────────────


def run() -> bool:
    errors: list[str] = []

    skill_text = SKILL_MD.read_text()
    skill_tools = parse_skill_tools(skill_text)
    skill_count = parse_skill_tool_count(skill_text)
    skill_cards = set(parse_skill_cards(skill_text))
    auth_tiers = parse_auth_tiers(AUTH_PY.read_text())
    mcp_tools = set(parse_mcp_tools(MCP_PY.read_text()))
    card_eps = set(parse_card_endpoints(CARD_API.read_text()))
    strat_md = parse_strategies_md(STRAT_MD.read_text())

    yaml_strats: dict[str, dict] = {}
    for yp in sorted(STRAT_DIR.glob("*.yaml")):
        d = load_yaml(yp)
        yaml_strats[d.get("name", yp.stem)] = d

    skill_set = set(skill_tools)
    auth_set = set(auth_tiers)

    # ── Tools ──────────────────────────────────────────────────────────
    print("ZERO Skill Validation")
    print("=====================\n")
    print(f"Tools: {len(skill_set)} in SKILL.md, {len(mcp_tools)} in mcp_server.py, {len(auth_set)} in auth.py")

    tool_errs: list[str] = []
    for t in sorted(mcp_tools - skill_set):
        tool_errs.append(f"  \u2717 Tool '{t}' in mcp_server.py but NOT in SKILL.md")
    for t in sorted(skill_set - mcp_tools):
        tool_errs.append(f"  \u2717 Tool '{t}' in SKILL.md but NOT in mcp_server.py")
    for t in sorted(auth_set - skill_set):
        tool_errs.append(f"  \u2717 Tool '{t}' in auth.py but NOT in SKILL.md")
    for t in sorted(skill_set - auth_set):
        tool_errs.append(f"  \u2717 Tool '{t}' in SKILL.md but NOT in auth.py")

    if tool_errs:
        errors.extend(tool_errs)
        for e in tool_errs:
            print(e)
    else:
        print("  \u2713 All tools match")

    if skill_count is not None and skill_count != len(skill_set):
        msg = f"  \u2717 Header says {skill_count} tools but table has {len(skill_set)}"
        errors.append(msg)
        print(msg)

    # ── Tiers ──────────────────────────────────────────────────────────
    tier_ok = 0
    tier_total = len(skill_set & auth_set)
    tier_errs: list[str] = []
    for tool in sorted(skill_set & auth_set):
        if skill_tools[tool] == auth_tiers[tool]:
            tier_ok += 1
        else:
            msg = f"  \u2717 Tier mismatch: {tool} is '{skill_tools[tool]}' in SKILL.md but '{auth_tiers[tool]}' in auth.py"
            tier_errs.append(msg)

    print(f"\nTiers: {tier_ok}/{tier_total} match")
    if tier_errs:
        errors.extend(tier_errs)
        for e in tier_errs:
            print(e)
    else:
        print("  \u2713 All tiers match")

    # ── Cards ──────────────────────────────────────────────────────────
    print(f"\nCards: {len(skill_cards)} in SKILL.md, {len(card_eps)} in card_api.py")
    card_errs: list[str] = []
    for c in sorted(skill_cards - card_eps):
        card_errs.append(f"  \u2717 Card '{c}' in SKILL.md but NOT in card_api.py")
    for c in sorted(card_eps - skill_cards):
        card_errs.append(f"  \u2717 Card '{c}' in card_api.py but NOT in SKILL.md")

    if card_errs:
        errors.extend(card_errs)
        for e in card_errs:
            print(e)
    else:
        print("  \u2713 All card endpoints match")

    # ── Strategies ─────────────────────────────────────────────────────
    yaml_names = set(yaml_strats)
    md_names = set(strat_md)
    print(f"\nStrategies: {len(yaml_names)} in YAML, {len(md_names)} in strategies.md")

    strat_errs: list[str] = []
    for n in sorted(yaml_names - md_names):
        strat_errs.append(f"  \u2717 Strategy '{n}' in YAML but NOT in strategies.md")
    for n in sorted(md_names - yaml_names):
        strat_errs.append(f"  \u2717 Strategy '{n}' in strategies.md but NOT in YAML")

    fields = [
        ("stop_loss_pct", "risk"), ("max_positions", "risk"),
        ("position_size_pct", "risk"), ("max_daily_loss_pct", "risk"),
        ("duration_hours", "session"),
    ]
    for name in sorted(yaml_names & md_names):
        yd, md = yaml_strats[name], strat_md[name]
        for field, section in fields:
            yv = yd.get(section, {}).get(field)
            mv = md.get(field)
            y = 0 if yv is None else yv
            m = 0 if mv is None else mv
            try:
                if float(y) == float(m):
                    continue
            except (ValueError, TypeError):
                pass
            strat_errs.append(f"  \u2717 Strategy '{name}' {field}: YAML={yv} vs md={mv}")
        yt, mt = yd.get("tier"), md.get("tier")
        if yt and mt and yt != mt:
            strat_errs.append(f"  \u2717 Strategy '{name}' tier: YAML={yt} vs md={mt}")

    if strat_errs:
        errors.extend(strat_errs)
        for e in strat_errs:
            print(e)
    else:
        print("  \u2713 All parameters match")

    # ── Result ─────────────────────────────────────────────────────────
    print()
    if errors:
        print(f"RESULT: {len(errors)} CHECK(S) FAILED")
        return False
    print("RESULT: ALL CHECKS PASSED")
    return True


if __name__ == "__main__":
    sys.exit(0 if run() else 1)

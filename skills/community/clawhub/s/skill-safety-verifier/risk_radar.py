#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Skill Safety Verifier - Risk Radar Renderer
Renders risk assessment results with progress bars.
"""
import sys
import io

import json
from typing import Dict, List, Tuple


def render_bar(score: int, max_score: int, width: int = 10) -> str:
    """Render a progress bar."""
    percent = min(score / max_score, 1.0) if max_score > 0 else 0
    filled = int(percent * width)
    return '█' * filled + '░' * (width - filled)


def get_risk_emoji(score: int, max_score: int) -> str:
    """Get emoji based on risk level."""
    percent = score / max_score if max_score > 0 else 0
    if percent < 0.2:
        return '🟢'
    elif percent < 0.5:
        return '🟡'
    elif percent < 0.8:
        return '🟠'
    return '🔴'


def get_risk_level(score: int) -> str:
    """Get risk level text."""
    if score <= 10:
        return '🟢 SAFE'
    elif score <= 30:
        return '🟡 LOW'
    elif score <= 60:
        return '🟠 MEDIUM'
    return '🔴 HIGH'


def render_risk_radar(
    network: int,
    vuln: int,
    permission: int,
    skill_name: str = "skill",
    warnings: List[str] = None
) -> str:
    """Render complete Risk Radar."""
    
    total = network + vuln + permission
    
    # Determine emoji based on total
    if total <= 10:
        status_emoji = '✅'
    elif total <= 30:
        status_emoji = '⚠️'
    elif total <= 60:
        status_emoji = '⚠️'
    else:
        status_emoji = '🚫'
    
    lines = [
        f"",
        f"{status_emoji} {skill_name} - Risk Assessment",
        f"",
        f"┌{'─' * 46}┐",
        f"│  📊 Risk Radar{' ' * 28}│",
        f"├{'─' * 46}┤",
        f"│  Network      [{render_bar(network, 50)}] {network:>2}/50  {get_risk_emoji(network, 50):<2}│",
        f"│  Vulnerabil. [{render_bar(vuln, 25)}] {vuln:>2}/25  {get_risk_emoji(vuln, 25):<2}│",
        f"│  Permissions  [{render_bar(permission, 50)}] {permission:>2}/50  {get_risk_emoji(permission, 50):<2}│",
        f"│  {'─' * 40}│",
        f"│  TOTAL        [{render_bar(total, 100)}] {total:>3}/100 {get_risk_emoji(total, 100):<2}│",
        f"├{'─' * 46}┤",
    ]
    
    # Add risk level
    lines.append(f"│  {get_risk_level(total):^42}│")
    
    # Add warnings if any
    if warnings:
        lines.append(f"├{'─' * 46}┤")
        lines.append(f"│  ⚠️ Warnings:{' ' * 32}│")
        for warning in warnings[:3]:  # Max 3 warnings
            lines.append(f"│    • {warning:<38}│")
    
    lines.append(f"└{'─' * 46}┘")
    
    return '\n'.join(lines)


def render_compact(
    network: int,
    vuln: int,
    permission: int,
    skill_name: str = "skill"
) -> str:
    """Render compact version for quick output."""
    total = network + vuln + permission
    level = get_risk_level(total)
    
    return f"""
{skill_name} - {level}
  Network: {network}/50 {get_risk_emoji(network, 50)}
  Vulnerabil.: {vuln}/25 {get_risk_emoji(vuln, 25)}
  Permissions: {permission}/50 {get_risk_emoji(permission, 50)}
  TOTAL: {total}/100 {get_risk_emoji(total, 100)}
"""


def parse_args():
    """Parse command line arguments."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Skill Safety Verifier - Risk Radar Renderer'
    )
    parser.add_argument('--network', '-n', type=int, default=0,
                        help='Network risk score (0-50)')
    parser.add_argument('--vuln', '-v', type=int, default=0,
                        help='Vulnerability score (0-25)')
    parser.add_argument('--perm', '-p', type=int, default=0,
                        help='Permission risk score (0-50)')
    parser.add_argument('--name', type=str, default='skill',
                        help='Skill name')
    parser.add_argument('--warnings', nargs='*', default=[],
                        help='Warning messages')
    parser.add_argument('--json', action='store_true',
                        help='Input from JSON')
    parser.add_argument('--compact', action='store_true',
                        help='Use compact output')
    
    return parser.parse_args()


def main():
    args = parse_args()
    
    # If JSON mode, read from stdin
    if args.json:
        try:
            data = json.loads(sys.stdin.read())
            network = data.get('network', 0)
            vuln = data.get('vuln', 0)
            permission = data.get('permission', 0)
            name = data.get('name', 'skill')
            warnings = data.get('warnings', [])
        except json.JSONDecodeError:
            print("Error: Invalid JSON input", file=sys.stderr)
            sys.exit(1)
    else:
        network = args.network
        vuln = args.vuln
        permission = args.perm
        name = args.name
        warnings = args.warnings
    
    # Render output
    if args.compact:
        print(render_compact(network, vuln, permission, name))
    else:
        print(render_risk_radar(network, vuln, permission, name, warnings))


if __name__ == '__main__':
    main()

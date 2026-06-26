#!/usr/bin/env python3
"""Generate SVG charts and category .md files from registry.db.

Run after each registry sync to keep docs/ up to date.
Usage: python generate_docs.py [--db PATH]
"""

import argparse
import math
import sqlite3
import os
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
CHARTS = DOCS / "charts"
DOMAINS_DIR = DOCS / "domains"
NETWORKS_DIR = DOCS / "networks"

# Color palettes
DOMAIN_COLORS = {
    "defi": "#3b82f6",
    "nfts": "#8b5cf6",
    "infrastructure": "#06b6d4",
    "dao": "#f59e0b",
    "identity": "#10b981",
    "analytics": "#ec4899",
    "gaming": "#f97316",
    "social": "#6366f1",
    "unknown": "#6b7280",
}

NETWORK_COLORS = [
    "#3b82f6", "#8b5cf6", "#06b6d4", "#f59e0b", "#10b981",
    "#ec4899", "#f97316", "#6366f1", "#ef4444", "#14b8a6",
    "#a855f7", "#84cc16", "#f43f5e", "#22d3ee", "#eab308",
]

RELIABILITY_COLORS = {"high": "#10b981", "medium": "#f59e0b", "low": "#6b7280"}


def query_db(db_path: str):
    """Extract all stats from registry.db."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row

    domains = conn.execute(
        "SELECT domain, COUNT(*) as cnt FROM subgraphs GROUP BY domain ORDER BY cnt DESC"
    ).fetchall()

    networks = conn.execute(
        "SELECT network, COUNT(*) as cnt FROM subgraphs GROUP BY network ORDER BY cnt DESC LIMIT 12"
    ).fetchall()

    protocol_types = conn.execute(
        "SELECT protocol_type, COUNT(*) as cnt FROM subgraphs "
        "WHERE protocol_type IS NOT NULL AND protocol_type <> '' "
        "GROUP BY protocol_type ORDER BY cnt DESC"
    ).fetchall()

    reliability = conn.execute(
        "SELECT CASE WHEN reliability_score >= 0.7 THEN 'high' "
        "WHEN reliability_score >= 0.3 THEN 'medium' ELSE 'low' END as tier, "
        "COUNT(*) as cnt FROM subgraphs GROUP BY tier ORDER BY tier"
    ).fetchall()

    total = conn.execute("SELECT COUNT(*) FROM subgraphs").fetchone()[0]

    # Top subgraphs per domain
    domain_tops = {}
    for row in domains:
        d = row["domain"]
        tops = conn.execute(
            "SELECT display_name, network, protocol_type, reliability_score, "
            "query_volume_30d, ipfs_hash, id FROM subgraphs "
            "WHERE domain = ? ORDER BY reliability_score DESC LIMIT 25",
            (d,),
        ).fetchall()
        domain_tops[d] = tops

    # Top subgraphs per network
    network_tops = {}
    for row in networks:
        n = row["network"]
        tops = conn.execute(
            "SELECT display_name, domain, protocol_type, reliability_score, "
            "query_volume_30d, ipfs_hash, id FROM subgraphs "
            "WHERE network = ? ORDER BY reliability_score DESC LIMIT 25",
            (n,),
        ).fetchall()
        network_tops[n] = tops

    conn.close()
    return {
        "domains": domains,
        "networks": networks,
        "protocol_types": protocol_types,
        "reliability": reliability,
        "total": total,
        "domain_tops": domain_tops,
        "network_tops": network_tops,
    }


# ---------------------------------------------------------------------------
# SVG Chart Generators
# ---------------------------------------------------------------------------

def svg_donut(data, colors, title, width=480, height=320):
    """Generate a donut chart SVG."""
    total = sum(r["cnt"] for r in data)
    cx, cy, r_outer, r_inner = 160, 160, 120, 70
    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" '
        f'font-family="system-ui,-apple-system,sans-serif">',
        f'<rect width="{width}" height="{height}" fill="#0d1017" rx="12"/>',
        f'<text x="{width/2}" y="24" text-anchor="middle" fill="#e8eaed" font-size="15" font-weight="600">{title}</text>',
    ]

    # Center label
    svg.append(f'<text x="{cx}" y="{cy-6}" text-anchor="middle" fill="#e8eaed" font-size="22" font-weight="700">{total:,}</text>')
    svg.append(f'<text x="{cx}" y="{cy+14}" text-anchor="middle" fill="#7b8394" font-size="11">subgraphs</text>')

    angle = -90
    for i, row in enumerate(data):
        name, cnt = row["domain"] if "domain" in row.keys() else row["network"], row["cnt"]
        pct = cnt / total
        sweep = pct * 360
        if sweep < 0.5:
            continue

        color = colors.get(name, NETWORK_COLORS[i % len(NETWORK_COLORS)]) if isinstance(colors, dict) else colors[i % len(colors)]

        a1 = math.radians(angle)
        a2 = math.radians(angle + sweep)
        x1_o, y1_o = cx + r_outer * math.cos(a1), cy + r_outer * math.sin(a1)
        x2_o, y2_o = cx + r_outer * math.cos(a2), cy + r_outer * math.sin(a2)
        x1_i, y1_i = cx + r_inner * math.cos(a2), cy + r_inner * math.sin(a2)
        x2_i, y2_i = cx + r_inner * math.cos(a1), cy + r_inner * math.sin(a1)
        large = 1 if sweep > 180 else 0

        svg.append(
            f'<path d="M{x1_o:.1f},{y1_o:.1f} A{r_outer},{r_outer} 0 {large},1 {x2_o:.1f},{y2_o:.1f} '
            f'L{x1_i:.1f},{y1_i:.1f} A{r_inner},{r_inner} 0 {large},0 {x2_i:.1f},{y2_i:.1f} Z" '
            f'fill="{color}" opacity="0.9"/>'
        )
        angle += sweep

    # Legend
    lx, ly = 310, 50
    for i, row in enumerate(data[:8]):
        name = row["domain"] if "domain" in row.keys() else row["network"]
        cnt = row["cnt"]
        color = colors.get(name, NETWORK_COLORS[i % len(NETWORK_COLORS)]) if isinstance(colors, dict) else colors[i % len(colors)]
        pct = cnt / total * 100
        svg.append(f'<rect x="{lx}" y="{ly + i*30}" width="12" height="12" rx="2" fill="{color}"/>')
        svg.append(f'<text x="{lx+18}" y="{ly + i*30 + 10}" fill="#e8eaed" font-size="11">{name.title()}</text>')
        svg.append(f'<text x="{lx+130}" y="{ly + i*30 + 10}" fill="#7b8394" font-size="10" text-anchor="end">{cnt:,} ({pct:.1f}%)</text>')

    svg.append("</svg>")
    return "\n".join(svg)


def svg_bar_chart(data, colors, title, label_key, width=600, height=340):
    """Generate a horizontal bar chart SVG."""
    max_val = max(r["cnt"] for r in data) if data else 1
    bar_h = 22
    gap = 6
    top_margin = 40
    left_margin = 110
    bar_area = width - left_margin - 30

    h = top_margin + len(data) * (bar_h + gap) + 20
    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{h}" viewBox="0 0 {width} {h}" '
        f'font-family="system-ui,-apple-system,sans-serif">',
        f'<rect width="{width}" height="{h}" fill="#0d1017" rx="12"/>',
        f'<text x="{width/2}" y="26" text-anchor="middle" fill="#e8eaed" font-size="15" font-weight="600">{title}</text>',
    ]

    for i, row in enumerate(data):
        name = row[label_key]
        cnt = row["cnt"]
        bar_w = (cnt / max_val) * bar_area
        y = top_margin + i * (bar_h + gap)
        color = colors[i % len(colors)] if isinstance(colors, list) else colors.get(name, "#6b7280")

        # Label
        display_name = name.replace("-", " ").title() if name else "Unknown"
        if len(display_name) > 14:
            display_name = display_name[:13] + "..."
        svg.append(f'<text x="{left_margin - 8}" y="{y + bar_h/2 + 4}" text-anchor="end" fill="#7b8394" font-size="11">{display_name}</text>')
        # Bar
        svg.append(f'<rect x="{left_margin}" y="{y}" width="{bar_w:.1f}" height="{bar_h}" rx="4" fill="{color}" opacity="0.85"/>')
        # Value
        svg.append(f'<text x="{left_margin + bar_w + 6}" y="{y + bar_h/2 + 4}" fill="#e8eaed" font-size="11">{cnt:,}</text>')

    svg.append("</svg>")
    return "\n".join(svg)


def svg_reliability_gauge(reliability, total, width=480, height=160):
    """Generate a reliability tier distribution bar."""
    tiers = {r["tier"]: r["cnt"] for r in reliability}
    high = tiers.get("high", 0)
    med = tiers.get("medium", 0)
    low = tiers.get("low", 0)

    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" '
        f'font-family="system-ui,-apple-system,sans-serif">',
        f'<rect width="{width}" height="{height}" fill="#0d1017" rx="12"/>',
        f'<text x="{width/2}" y="26" text-anchor="middle" fill="#e8eaed" font-size="15" font-weight="600">Reliability Score Distribution</text>',
    ]

    bar_y, bar_h = 50, 28
    bar_x, bar_w = 30, width - 60
    # Stacked bar
    w_high = (high / total) * bar_w
    w_med = (med / total) * bar_w
    w_low = (low / total) * bar_w

    svg.append(f'<rect x="{bar_x}" y="{bar_y}" width="{bar_w}" height="{bar_h}" rx="6" fill="#1a1f2e"/>')
    x = bar_x
    for w, color, label in [(w_high, RELIABILITY_COLORS["high"], "High"), (w_med, RELIABILITY_COLORS["medium"], "Medium"), (w_low, RELIABILITY_COLORS["low"], "Low")]:
        if w > 2:
            svg.append(f'<rect x="{x:.1f}" y="{bar_y}" width="{w:.1f}" height="{bar_h}" rx="{"6" if x == bar_x else "0"}" fill="{color}" opacity="0.85"/>')
        x += w

    # Legend below
    ly = bar_y + bar_h + 30
    items = [
        ("High (0.7+)", high, RELIABILITY_COLORS["high"]),
        ("Medium (0.3&#x2013;0.7)", med, RELIABILITY_COLORS["medium"]),
        ("Low (&#x3c;0.3)", low, RELIABILITY_COLORS["low"]),
    ]
    for i, (label, cnt, color) in enumerate(items):
        lx = 30 + i * 160
        pct = cnt / total * 100
        svg.append(f'<rect x="{lx}" y="{ly}" width="12" height="12" rx="2" fill="{color}"/>')
        svg.append(f'<text x="{lx+18}" y="{ly+10}" fill="#e8eaed" font-size="11">{label}</text>')
        svg.append(f'<text x="{lx+18}" y="{ly+26}" fill="#7b8394" font-size="10">{cnt:,} ({pct:.1f}%)</text>')

    svg.append("</svg>")
    return "\n".join(svg)


# ---------------------------------------------------------------------------
# Category .md File Generators
# ---------------------------------------------------------------------------

def generate_domain_md(domain, count, tops, total):
    """Generate a bot-readable .md file for a domain category."""
    pct = count / total * 100
    display = domain.title() if domain != "nfts" else "NFTs"
    if domain == "dao":
        display = "DAO"

    lines = [
        f"---",
        f"domain: {domain}",
        f"count: {count}",
        f"percentage: {pct:.1f}",
        f"updated: {datetime.now(timezone.utc).strftime('%Y-%m-%d')}",
        f"---",
        f"",
        f"# {display} Subgraphs",
        f"",
        f"**{count:,}** subgraphs ({pct:.1f}% of registry)",
        f"",
        f"## Top Subgraphs by Reliability",
        f"",
        f"| Name | Network | Protocol | Reliability | 30d Queries |",
        f"|------|---------|----------|-------------|-------------|",
    ]

    for row in tops:
        name = (row["display_name"] or "Unnamed")[:40]
        net = row["network"] or "—"
        proto = row["protocol_type"] or "—"
        rel = f'{row["reliability_score"]:.2f}' if row["reliability_score"] else "—"
        vol = f'{row["query_volume_30d"]:,}' if row["query_volume_30d"] else "—"
        lines.append(f"| {name} | {net} | {proto} | {rel} | {vol} |")

    lines.extend([
        "",
        "## Query This Domain",
        "",
        "```",
        f"# Via MCP tool",
        f'search_subgraphs(domain="{domain}", min_reliability=0.5, limit=20)',
        "",
        f"# Via REST API",
        f"GET /subgraphs?domain={domain}&min_reliability=0.5&limit=20",
        "```",
    ])

    return "\n".join(lines)


def generate_network_md(network, count, tops, total):
    """Generate a bot-readable .md file for a network."""
    pct = count / total * 100
    display = network.replace("-", " ").title()
    # Fix common names
    name_map = {"Mainnet": "Ethereum", "Matic": "Polygon", "Bsc": "BSC", "Arbitrum One": "Arbitrum"}
    display = name_map.get(display, display)

    lines = [
        f"---",
        f"network: {network}",
        f"count: {count}",
        f"percentage: {pct:.1f}",
        f"updated: {datetime.now(timezone.utc).strftime('%Y-%m-%d')}",
        f"---",
        f"",
        f"# {display} Subgraphs",
        f"",
        f"**{count:,}** subgraphs ({pct:.1f}% of registry)",
        f"",
        f"## Top Subgraphs by Reliability",
        f"",
        f"| Name | Domain | Protocol | Reliability | 30d Queries |",
        f"|------|--------|----------|-------------|-------------|",
    ]

    for row in tops:
        name = (row["display_name"] or "Unnamed")[:40]
        dom = row["domain"] or "—"
        proto = row["protocol_type"] or "—"
        rel = f'{row["reliability_score"]:.2f}' if row["reliability_score"] else "—"
        vol = f'{row["query_volume_30d"]:,}' if row["query_volume_30d"] else "—"
        lines.append(f"| {name} | {dom} | {proto} | {rel} | {vol} |")

    lines.extend([
        "",
        "## Query This Network",
        "",
        "```",
        f'search_subgraphs(network="{network}", min_reliability=0.5, limit=20)',
        "```",
    ])

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Generate docs from registry.db")
    parser.add_argument("--db", default=str(ROOT / "data" / "registry.db"), help="Path to registry.db")
    args = parser.parse_args()

    if not os.path.exists(args.db):
        print(f"Error: {args.db} not found")
        return

    print(f"Reading {args.db}...")
    stats = query_db(args.db)
    total = stats["total"]
    print(f"Total subgraphs: {total:,}")

    # Ensure dirs
    for d in [CHARTS, DOMAINS_DIR, NETWORKS_DIR]:
        d.mkdir(parents=True, exist_ok=True)

    # Generate SVG charts
    print("Generating charts...")

    svg = svg_donut(stats["domains"], DOMAIN_COLORS, "Subgraphs by Domain")
    (CHARTS / "domains.svg").write_text(svg)

    svg = svg_bar_chart(stats["networks"], NETWORK_COLORS, "Subgraphs by Network", "network")
    (CHARTS / "networks.svg").write_text(svg)

    svg = svg_bar_chart(stats["protocol_types"], NETWORK_COLORS, "Subgraphs by Protocol Type", "protocol_type")
    (CHARTS / "protocol-types.svg").write_text(svg)

    svg = svg_reliability_gauge(stats["reliability"], total)
    (CHARTS / "reliability-dist.svg").write_text(svg)

    print(f"  Written: {CHARTS}/domains.svg, networks.svg, protocol-types.svg, reliability.svg")

    # Generate domain .md files
    print("Generating domain category files...")
    for row in stats["domains"]:
        d = row["domain"]
        tops = stats["domain_tops"].get(d, [])
        md = generate_domain_md(d, row["cnt"], tops, total)
        (DOMAINS_DIR / f"{d}.md").write_text(md)
    print(f"  Written: {len(stats['domains'])} domain files")

    # Generate network .md files
    print("Generating network category files...")
    for row in stats["networks"]:
        n = row["network"]
        tops = stats["network_tops"].get(n, [])
        md = generate_network_md(n, row["cnt"], tops, total)
        safe_name = n.replace("/", "-")
        (NETWORKS_DIR / f"{safe_name}.md").write_text(md)
    print(f"  Written: {len(stats['networks'])} network files")

    # Generate index .md for bots
    print("Generating index files...")

    # Domain index
    lines = [
        "---",
        "type: domain-index",
        f"updated: {datetime.now(timezone.utc).strftime('%Y-%m-%d')}",
        f"total_subgraphs: {total}",
        "---",
        "",
        "# Subgraph Domains",
        "",
        "| Domain | Count | % | File |",
        "|--------|-------|---|------|",
    ]
    for row in stats["domains"]:
        d = row["domain"]
        display = d.upper() if d in ("dao", "nfts") else d.title()
        pct = row["cnt"] / total * 100
        lines.append(f"| {display} | {row['cnt']:,} | {pct:.1f}% | [View](domains/{d}.md) |")
    (DOCS / "DOMAINS.md").write_text("\n".join(lines))

    # Network index
    lines = [
        "---",
        "type: network-index",
        f"updated: {datetime.now(timezone.utc).strftime('%Y-%m-%d')}",
        f"total_subgraphs: {total}",
        "---",
        "",
        "# Subgraph Networks",
        "",
        "| Network | Count | % | File |",
        "|---------|-------|---|------|",
    ]
    for row in stats["networks"]:
        n = row["network"]
        display = n.replace("-", " ").title()
        name_map = {"Mainnet": "Ethereum", "Matic": "Polygon", "Bsc": "BSC", "Arbitrum One": "Arbitrum"}
        display = name_map.get(display, display)
        pct = row["cnt"] / total * 100
        safe = n.replace("/", "-")
        lines.append(f"| {display} | {row['cnt']:,} | {pct:.1f}% | [View](networks/{safe}.md) |")
    (DOCS / "NETWORKS.md").write_text("\n".join(lines))

    print("Done!")


if __name__ == "__main__":
    main()

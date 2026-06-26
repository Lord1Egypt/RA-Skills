#!/usr/bin/env python3
"""CLI wrapper for the OpenClaw Memory Engine.

Usage:
  memory.py ingest "Some text about facts" [--session KEY] [--agent ID] [--date YYYY-MM-DD]
  memory.py search "query" [--top-k 10] [--all] [--as-of YYYY-MM-DD]
  memory.py recall "query" [--top-k 5]          # Agent-optimized: returns compact context block
  memory.py graph                                 # Dump full graph as JSON
  memory.py stats                                 # Memory counts
  memory.py history ENTITY_NAME                   # Version timeline for entity
  memory.py profile ENTITY_NAME                   # Auto-built entity profile
  memory.py entities                              # List all known entities
"""

import argparse
import json
import os
import sys

# ultramemory must be pip-installed: pip install ultramemory
DB_PATH = os.environ.get("ULTRAMEMORY_DB", os.environ.get("MEMORY_DB", "memory.db"))


def get_engine():
    from ultramemory.engine import MemoryEngine
    return MemoryEngine(db_path=DB_PATH)


def cmd_ingest(args):
    engine = get_engine()
    memories = engine.ingest(
        args.text,
        session_key=args.session or "cli",
        agent_id=args.agent or "kit",
        document_date=args.date,
    )
    print(json.dumps(memories, indent=2))
    print(f"\n✓ Extracted {len(memories)} memories", file=sys.stderr)


def cmd_search(args):
    engine = get_engine()
    results = engine.search(
        args.query,
        top_k=args.top_k,
        current_only=not args.all,
        as_of_date=args.as_of,
    )
    print(json.dumps(results, indent=2))


def cmd_recall(args):
    """Agent-optimized search: returns a compact context block ready for injection."""
    engine = get_engine()
    results = engine.search(
        args.query,
        top_k=args.top_k,
        current_only=True,
    )
    if not results:
        print("No relevant memories found.")
        return

    lines = []
    for r in results:
        sim_pct = int(r["similarity"] * 100)
        status = "current" if r["is_current"] else "superseded"
        line = f"[{r['category']}] {r['content']} (v{r['version']}, {status}, {sim_pct}% match)"
        
        # Include relations inline if present
        if r.get("relations"):
            for rel in r["relations"]:
                line += f"\n  → {rel['relation']}: {rel['related_content']}"
        
        lines.append(line)

    print("\n".join(lines))


def cmd_graph(args):
    import sqlite3
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    nodes = conn.execute(
        """SELECT id, content, category, confidence, document_date, event_date,
                  is_current, version, source_session, source_agent, created_at
           FROM memories ORDER BY created_at"""
    ).fetchall()

    edges = conn.execute(
        """SELECT mr.from_memory as source, mr.to_memory as target,
                  mr.relation as type, mr.context
           FROM memory_relations mr"""
    ).fetchall()

    conn.close()
    print(json.dumps({
        "nodes": [dict(r) for r in nodes],
        "edges": [dict(r) for r in edges],
    }, indent=2, default=str))


def cmd_stats(args):
    engine = get_engine()
    stats = engine.get_stats()
    print(json.dumps(stats, indent=2))


def cmd_history(args):
    engine = get_engine()
    history = engine.get_history(args.entity)
    print(json.dumps(history, indent=2))


def cmd_profile(args):
    engine = get_engine()
    profile = engine.get_profile(args.entity)
    if profile:
        print(json.dumps(profile, indent=2))
    else:
        print(f"No profile found for '{args.entity}'", file=sys.stderr)
        sys.exit(1)


def cmd_entities(args):
    import sqlite3
    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute(
        "SELECT DISTINCT entity_name FROM profiles ORDER BY entity_name"
    ).fetchall()
    conn.close()
    for r in rows:
        print(r[0])


def main():
    parser = argparse.ArgumentParser(description="OpenClaw Memory Engine CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    # ingest
    p = sub.add_parser("ingest", help="Extract and store memories from text")
    p.add_argument("text", help="Text to extract memories from")
    p.add_argument("--session", help="Session key (default: cli)")
    p.add_argument("--agent", help="Agent ID (default: kit)")
    p.add_argument("--date", help="Document date (YYYY-MM-DD)")
    p.set_defaults(func=cmd_ingest)

    # search
    p = sub.add_parser("search", help="Semantic search over memories")
    p.add_argument("query", help="Search query")
    p.add_argument("--top-k", type=int, default=10)
    p.add_argument("--all", action="store_true", help="Include superseded memories")
    p.add_argument("--as-of", help="Search as of date (YYYY-MM-DD)")
    p.set_defaults(func=cmd_search)

    # recall
    p = sub.add_parser("recall", help="Agent-optimized search (compact context block)")
    p.add_argument("query", help="Search query")
    p.add_argument("--top-k", type=int, default=5)
    p.set_defaults(func=cmd_recall)

    # graph
    p = sub.add_parser("graph", help="Dump full memory graph as JSON")
    p.set_defaults(func=cmd_graph)

    # stats
    p = sub.add_parser("stats", help="Memory counts and categories")
    p.set_defaults(func=cmd_stats)

    # history
    p = sub.add_parser("history", help="Version timeline for an entity")
    p.add_argument("entity", help="Entity name")
    p.set_defaults(func=cmd_history)

    # profile
    p = sub.add_parser("profile", help="Auto-built entity profile")
    p.add_argument("entity", help="Entity name")
    p.set_defaults(func=cmd_profile)

    # entities
    p = sub.add_parser("entities", help="List all known entities")
    p.set_defaults(func=cmd_entities)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()

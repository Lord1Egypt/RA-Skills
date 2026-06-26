#!/usr/bin/env python3
"""
memory_graph.py — SQLite knowledge graph for memory entities and relations.

Builds a graph from MEMORY.md and memory/*.md by extracting entities
(projects, people, tools, concepts) and their relationships.

Zero external dependencies — uses Python built-in sqlite3.

Usage:
  memory_graph.py build                        # Build graph from memory files
  memory_graph.py related "entity"             # Find entities related to query
  memory_graph.py related "entity" --depth 2   # Traverse 2 hops
  memory_graph.py stats                        # Show graph statistics
  memory_graph.py query "SQL WHERE clause"     # Raw query (read-only)
"""

import argparse
import os
import re
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

WORKSPACE = Path(os.environ.get("OPENCLAW_WORKSPACE", os.path.expanduser("~/.openclaw/workspace")))
GRAPH_DB = WORKSPACE / "memory" / ".index" / "graph.db"

# Entity extraction patterns
# Known entity names for exact matching (avoids capturing garbage phrases)
KNOWN_PROJECTS = [
    "黄金三章", "golden3", "resume-service", "smart-memory", "smart-memory-plus",
    "context-compactor", "openclaw",
    # Add more as needed — these are extracted from workspace
]
KNOWN_PEOPLE = ["老大", "老芒", "Munger", "芒格"]
KNOWN_TOOLS = [
    "SQLite", "Node.js", "Python", "Docker", "nginx", "OpenClaw", "ClawHub",
    "GitHub", "Telegram", "Discord", "Ollama", "LM Studio", "Milvus",
    "SurrealDB", "PostgreSQL", "React", "Next.js", "Prisma", "Vercel",
    "Google", "Chrome", "Playwright",
]
KNOWN_CONCEPTS = [
    "BM25", "WAL", "OAuth", "API", "LLM", "GPT", "AES-256", "argon2",
    "WAL协议", "知识图谱", "评分", "scoring", "prompt", "SQLite",
    "systemd", "HTTPS", "Let's Encrypt",
]

# Pattern-based extraction — disabled for most types to avoid garbage captures.
# Only KNOWN_* lists are used for entity extraction.
# To add new entities, append to the KNOWN_* lists above.
ENTITY_PATTERNS = {
    "PROJECT": [],
    "PERSON": [],
    "TOOL": [],
    "CONCEPT": [],
}

# Relation extraction patterns
RELATION_PATTERNS = [
    (re.compile(r"(.{2,30})\s+(?:uses?|用|使用|采用)\s+(.{2,30})", re.IGNORECASE), "uses"),
    (re.compile(r"(.{2,30})\s+(?:depends? on|依赖|需要)\s+(.{2,30})", re.IGNORECASE), "depends_on"),
    (re.compile(r"(.{2,30})\s+(?:stores?|存|存储)\s+(?:in|到|于)\s+(.{2,30})", re.IGNORECASE), "stored_in"),
    (re.compile(r"(.{2,30})\s+(?:deployed?|部署)\s+(?:to|on|到)\s+(.{2,30})", re.IGNORECASE), "deployed_to"),
    (re.compile(r"(.{2,30})\s+(?:related to|相关|关联)\s+(.{2,30})", re.IGNORECASE), "related_to"),
    (re.compile(r"(.{2,30})\s+(?:config|配置|setting|设置)\s+(?:of|for|的)\s+(.{2,30})", re.IGNORECASE), "config_of"),
]

SENSITIVE = re.compile(
    r"(?:password|passwd|pwd)\s*[:=]\s*\S+|"
    r"(?:api[_-]?key|token|secret|bearer)\s*[:=]\s*\S+",
    re.IGNORECASE,
)


def init_db():
    """Initialize SQLite graph database."""
    GRAPH_DB.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(GRAPH_DB))
    conn.execute("PRAGMA journal_mode=WAL")
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS entities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            type TEXT NOT NULL,
            source_file TEXT,
            source_line INTEGER,
            first_seen TEXT,
            mention_count INTEGER DEFAULT 1,
            UNIQUE(name, type)
        );
        CREATE TABLE IF NOT EXISTS relations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source_id INTEGER NOT NULL,
            target_id INTEGER NOT NULL,
            relation_type TEXT NOT NULL,
            source_file TEXT,
            weight REAL DEFAULT 1.0,
            FOREIGN KEY (source_id) REFERENCES entities(id),
            FOREIGN KEY (target_id) REFERENCES entities(id),
            UNIQUE(source_id, target_id, relation_type)
        );
        CREATE INDEX IF NOT EXISTS idx_entities_name ON entities(name);
        CREATE INDEX IF NOT EXISTS idx_entities_type ON entities(type);
        CREATE INDEX IF NOT EXISTS idx_relations_source ON relations(source_id);
        CREATE INDEX IF NOT EXISTS idx_relations_target ON relations(target_id);
    """)
    return conn


def extract_entities(text: str, source_file: str) -> list[dict]:
    """Extract entities from text using known lists + pattern matching."""
    entities = []
    seen = set()
    lines = text.split("\n")

    # Build known entity lookup: name_lower -> (display_name, type)
    known = {}
    for name in KNOWN_PROJECTS:
        known[name.lower()] = (name, "PROJECT")
    for name in KNOWN_PEOPLE:
        known[name.lower()] = (name, "PERSON")
    for name in KNOWN_TOOLS:
        known[name.lower()] = (name, "TOOL")
    for name in KNOWN_CONCEPTS:
        known[name.lower()] = (name, "CONCEPT")

    for line_num, line in enumerate(lines, 1):
        if SENSITIVE.search(line):
            continue
        line_clean = line.strip()
        if not line_clean or line_clean.startswith("#") or line_clean.startswith("```"):
            continue
        line_lower = line_clean.lower()

        # 1. Check known entities
        for name_lower, (display_name, etype) in known.items():
            if name_lower in line_lower:
                key = f"{etype}:{name_lower}"
                if key not in seen:
                    seen.add(key)
                    entities.append({
                        "name": display_name,
                        "type": etype,
                        "source_file": source_file,
                        "source_line": line_num,
                    })

        # 2. Pattern-based fallback
        for etype, patterns in ENTITY_PATTERNS.items():
            for pattern in patterns:
                for match in pattern.finditer(line_clean):
                    name = match.group(1).strip() if match.lastindex else match.group(0).strip()
                    # Trim to reasonable length
                    name = name[:30].strip()
                    if len(name) < 2:
                        continue
                    key = f"{etype}:{name.lower()}"
                    if key not in seen:
                        seen.add(key)
                        entities.append({
                            "name": name,
                            "type": etype,
                            "source_file": source_file,
                            "source_line": line_num,
                        })

    return entities


def extract_relations(text: str, source_file: str, entity_map: dict) -> list[dict]:
    """Extract relations from text using paragraph co-occurrence and patterns."""
    relations = []
    seen = set()

    # Split into paragraphs (groups of non-empty lines separated by blank lines)
    paragraphs = re.split(r"\n\s*\n", text)

    for para in paragraphs:
        if SENSITIVE.search(para):
            continue
        para_clean = para.strip()
        if not para_clean or len(para_clean) < 10:
            continue
        para_lower = para_clean.lower()

        # Pattern-based extraction (per line within paragraph)
        for line in para.split("\n"):
            line_clean = line.strip()
            if not line_clean:
                continue
            for pattern, rel_type in RELATION_PATTERNS:
                for match in pattern.finditer(line_clean):
                    subj = match.group(1).strip()[:50]
                    obj = match.group(2).strip()[:50]
                    subj_id = entity_map.get(subj.lower())
                    obj_id = entity_map.get(obj.lower())
                    if subj_id and obj_id and subj_id != obj_id:
                        key = (min(subj_id, obj_id), max(subj_id, obj_id), rel_type)
                        if key not in seen:
                            seen.add(key)
                            relations.append({
                                "source_id": subj_id,
                                "target_id": obj_id,
                                "relation_type": rel_type,
                                "source_file": source_file,
                            })

        # Co-occurrence: entities in the same paragraph
        para_entities = []
        for ent_key, ent_id in entity_map.items():
            if ent_key in para_lower:
                para_entities.append(ent_id)
        if len(para_entities) >= 2:
            for i in range(len(para_entities)):
                for j in range(i + 1, len(para_entities)):
                    sid, tid = para_entities[i], para_entities[j]
                    if sid == tid:
                        continue
                    key = (min(sid, tid), max(sid, tid), "co_occurs")
                    if key not in seen:
                        seen.add(key)
                        relations.append({
                            "source_id": sid,
                            "target_id": tid,
                            "relation_type": "co_occurs",
                            "source_file": source_file,
                        })

    return relations


def cmd_build():
    """Build graph from memory files."""
    conn = init_db()

    # Clear existing data
    conn.execute("DELETE FROM relations")
    conn.execute("DELETE FROM entities")

    memory_dir = WORKSPACE / "memory"
    files = [WORKSPACE / "MEMORY.md"]
    if memory_dir.exists():
        files.extend(f for f in sorted(memory_dir.glob("*.md"))
                     if f.name != "archive" and not f.name.startswith("."))

    all_entities = []
    all_relations = []
    now = datetime.now(timezone.utc).isoformat()

    for filepath in files:
        if not filepath.exists():
            continue
        content = filepath.read_text(encoding="utf-8")
        source = filepath.name

        entities = extract_entities(content, source)
        all_entities.extend(entities)

    # Insert entities and build ID map
    entity_map = {}  # "type:name_lower" -> id
    for ent in all_entities:
        try:
            cursor = conn.execute(
                "INSERT OR IGNORE INTO entities (name, type, source_file, source_line, first_seen) VALUES (?, ?, ?, ?, ?)",
                (ent["name"], ent["type"], ent["source_file"], ent["source_line"], now),
            )
            if cursor.lastrowid:
                entity_map[f"{ent['type']}:{ent['name'].lower()}"] = cursor.lastrowid
                entity_map[ent["name"].lower()] = cursor.lastrowid  # Also index by name alone
            else:
                # Already exists, get its id
                row = conn.execute(
                    "SELECT id FROM entities WHERE name=? AND type=?",
                    (ent["name"], ent["type"]),
                ).fetchone()
                if row:
                    entity_map[f"{ent['type']}:{ent['name'].lower()}"] = row[0]
                    entity_map[ent["name"].lower()] = row[0]
        except sqlite3.IntegrityError:
            pass

    # Update mention counts
    conn.execute("""
        UPDATE entities SET mention_count = (
            SELECT COUNT(DISTINCT source_file) FROM entities e2
            WHERE e2.name = entities.name AND e2.type = entities.type
        )
    """)

    # Extract relations
    for filepath in files:
        if not filepath.exists():
            continue
        content = filepath.read_text(encoding="utf-8")
        source = filepath.name
        relations = extract_relations(content, source, entity_map)
        all_relations.extend(relations)

    for rel in all_relations:
        try:
            conn.execute(
                "INSERT OR IGNORE INTO relations (source_id, target_id, relation_type, source_file) VALUES (?, ?, ?, ?)",
                (rel["source_id"], rel["target_id"], rel["relation_type"], rel["source_file"]),
            )
        except sqlite3.IntegrityError:
            pass

    # Update relation weights based on frequency
    conn.execute("""
        UPDATE relations SET weight = (
            SELECT COUNT(*) FROM relations r2
            WHERE r2.source_id = relations.source_id
              AND r2.target_id = relations.target_id
              AND r2.relation_type = relations.relation_type
        )
    """)

    conn.commit()

    ent_count = conn.execute("SELECT COUNT(*) FROM entities").fetchone()[0]
    rel_count = conn.execute("SELECT COUNT(*) FROM relations").fetchone()[0]
    conn.close()

    print(f"Graph built: {ent_count} entities, {rel_count} relations")
    print(f"Database: {GRAPH_DB}")


def cmd_related(query: str, depth: int = 1):
    """Find entities related to query."""
    if not GRAPH_DB.exists():
        print("Graph not found. Run 'build' first.")
        sys.exit(1)

    conn = sqlite3.connect(str(GRAPH_DB))
    query_lower = query.lower()

    # Find matching entities
    matches = conn.execute(
        "SELECT id, name, type FROM entities WHERE LOWER(name) LIKE ?",
        (f"%{query_lower}%",),
    ).fetchall()

    if not matches:
        print(f"No entities found matching: \"{query}\"")
        conn.close()
        return

    print(f"Related to: \"{query}\"\n")
    visited = set()

    for ent_id, ent_name, ent_type in matches:
        if ent_id in visited:
            continue
        visited.add(ent_id)

        print(f"  [{ent_type}] {ent_name}")

        # Traverse relations
        current_ids = [ent_id]
        for hop in range(depth):
            next_ids = []
            for cid in current_ids:
                # Outgoing
                results = conn.execute("""
                    SELECT e.name, e.type, r.relation_type
                    FROM relations r
                    JOIN entities e ON e.id = r.target_id
                    WHERE r.source_id = ?
                    ORDER BY r.weight DESC
                    LIMIT 5
                """, (cid,)).fetchall()

                for target_name, target_type, rel_type in results:
                    indent = "    " + "  " * hop
                    print(f"{indent}→ [{rel_type}] [{target_type}] {target_name}")
                    if hop < depth - 1:
                        target_row = conn.execute(
                            "SELECT id FROM entities WHERE name=? AND type=?",
                            (target_name, target_type),
                        ).fetchone()
                        if target_row and target_row[0] not in visited:
                            next_ids.append(target_row[0])
                            visited.add(target_row[0])

                # Incoming
                results = conn.execute("""
                    SELECT e.name, e.type, r.relation_type
                    FROM relations r
                    JOIN entities e ON e.id = r.source_id
                    WHERE r.target_id = ?
                    ORDER BY r.weight DESC
                    LIMIT 5
                """, (cid,)).fetchall()

                for source_name, source_type, rel_type in results:
                    indent = "    " + "  " * hop
                    print(f"{indent}← [{rel_type}] [{source_type}] {source_name}")

            current_ids = next_ids
        print()

    conn.close()


def cmd_stats():
    """Show graph statistics."""
    if not GRAPH_DB.exists():
        print("Graph not found. Run 'build' first.")
        return

    conn = sqlite3.connect(str(GRAPH_DB))

    ent_count = conn.execute("SELECT COUNT(*) FROM entities").fetchone()[0]
    rel_count = conn.execute("SELECT COUNT(*) FROM relations").fetchone()[0]

    print("=== Knowledge Graph Stats ===")
    print(f"Entities: {ent_count}")
    print(f"Relations: {rel_count}")
    print()

    # By type
    print("Entities by type:")
    for row in conn.execute("SELECT type, COUNT(*) FROM entities GROUP BY type ORDER BY COUNT(*) DESC"):
        print(f"  [{row[0]}]: {row[1]}")
    print()

    # By relation type
    print("Relations by type:")
    for row in conn.execute("SELECT relation_type, COUNT(*) FROM relations GROUP BY relation_type ORDER BY COUNT(*) DESC"):
        print(f"  {row[0]}: {row[1]}")
    print()

    # Most connected
    print("Most connected entities:")
    for row in conn.execute("""
        SELECT e.name, e.type, COUNT(r.id) as conn_count
        FROM entities e
        LEFT JOIN relations r ON r.source_id = e.id OR r.target_id = e.id
        GROUP BY e.id
        ORDER BY conn_count DESC
        LIMIT 10
    """):
        print(f"  [{row[1]}] {row[0]} — {row[2]} connections")

    mtime = datetime.fromtimestamp(GRAPH_DB.stat().st_mtime, tz=timezone.utc)
    print(f"\nLast built: {mtime.strftime('%Y-%m-%d %H:%M UTC')}")
    conn.close()


def cmd_query(sql: str):
    """Run a raw read-only query."""
    if not GRAPH_DB.exists():
        print("Graph not found. Run 'build' first.")
        return

    # Safety: only allow SELECT
    if not sql.strip().upper().startswith("SELECT"):
        print("Only SELECT queries are allowed.")
        sys.exit(1)

    conn = sqlite3.connect(str(GRAPH_DB))
    conn.row_factory = sqlite3.Row
    try:
        rows = conn.execute(sql).fetchall()
        if not rows:
            print("No results.")
            return
        for row in rows:
            print(dict(row))
    except sqlite3.Error as e:
        print(f"Query error: {e}")
    conn.close()


def main():
    parser = argparse.ArgumentParser(description="Knowledge graph for memories")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("build", help="Build graph from memory files")

    related_parser = subparsers.add_parser("related", help="Find related entities")
    related_parser.add_argument("query", help="Entity name to search")
    related_parser.add_argument("--depth", type=int, default=1, help="Traversal depth (default: 1)")

    subparsers.add_parser("stats", help="Show graph statistics")

    query_parser = subparsers.add_parser("query", help="Raw SQL query (SELECT only)")
    query_parser.add_argument("sql", help="SQL SELECT statement")

    args = parser.parse_args()

    if args.command == "build":
        cmd_build()
    elif args.command == "related":
        cmd_related(args.query, args.depth)
    elif args.command == "stats":
        cmd_stats()
    elif args.command == "query":
        cmd_query(args.sql)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()

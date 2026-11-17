#!/usr/bin/env python3
"""Memory search index — fast FTS5-based retrieval for OpenClaw on Pi 4.

Usage:
  python3 memory-index.py build         # Build index + stub
  python3 memory-index.py search <q>    # Search (results to stdout)
  python3 memory-index.py tags          # List all detected tags
"""
import sqlite3
import os
import sys
import json
import re
import time
from pathlib import Path

WORKSPACE = os.environ.get("OPENCLAW_WORKSPACE", 
    os.path.expanduser("~/.openclaw/workspace"))
SAVED_DIR = os.environ.get("SAVED_CONVERSATIONS_DIR", 
    os.path.expanduser("~/.openclaw/workspace/saved"))
DB_PATH = "/dev/shm/memory-index.db"
STUB_PATH = os.path.join(SAVED_DIR, "stub-index.md")

# Synonym map for cheap "semantic" expansion
SYNONYM_MAP = {
    "retrieval": "search OR retrieve OR fetch OR find OR lookup OR query",
    "conversation": "chat OR message OR session OR chatlog OR dialog",
    "project": "project OR code OR repo OR build OR app",
    "config": "config OR configuration OR setup OR settings OR conf",
    "error": "error OR bug OR fail OR failure OR issue OR problem",
    "performance": "performance OR speed OR fast OR slow OR benchmark OR perf",
    "memory": "memory OR ram OR context OR workspace OR storage",
    "embedding": "embedding OR vector OR semantic OR dense",
    "install": "install OR setup OR deploy OR configure OR build",
    "update": "update OR upgrade OR change OR modify OR edit OR patch",
    "remove": "remove OR delete OR uninstall OR clean OR rm",
    "skill": "skill OR skills OR plugin OR module OR tool",
    "research": "research OR benchmark OR test OR experiment OR study",
    "writing": "writing OR write OR author OR compose OR draft",
}

def get_md_files():
    """Get all knowledge files: workspace .md + saved conversations .md/.txt."""
    files = []
    for root, dirs, fnames in os.walk(WORKSPACE):
        if "node_modules" in root or ".git" in root:
            continue
        for f in fnames:
            if f.endswith(".md"):
                files.append(os.path.join(root, f))
    # Also index saved conversations
    convos_dir = SAVED_DIR
    if os.path.isdir(convos_dir):
        for f in os.listdir(convos_dir):
            if f.endswith(".md") or f.endswith(".txt"):
                files.append(os.path.join(convos_dir, f))
    return sorted(files)

def build_index():
    """Build FTS5 index on tmpfs and write stub index."""
    files = get_md_files()
    total = len(files)
    total_bytes = sum(os.path.getsize(f) for f in files)
    
    print(f"Indexing {total} files ({total_bytes:,} bytes)...")
    start = time.time()
    
    # Build FTS5 in memory
    conn = sqlite3.connect(":memory:")
    conn.execute("""
        CREATE VIRTUAL TABLE idx USING fts5(
            relpath, filename, heading, content,
            tokenize='porter unicode61'
        )
    """)
    
    entries = []  # for stub index
    for fp in files:
        relpath = os.path.relpath(fp, WORKSPACE)
        fname = os.path.basename(fp)
        try:
            with open(fp, 'r', errors='replace') as f:
                content = f.read()
        except Exception as e:
            print(f"  WARN: can't read {relpath}: {e}")
            continue
        
        lines = content.split('\n')
        heading = ""
        for line in lines:
            if line.startswith('# ') or line.startswith('## '):
                heading = line.lstrip('#').strip()
                break
        if not heading:
            heading = fname.replace('.md', '')
        
        first_content = ""
        for line in lines:
            stripped = line.strip()
            if stripped and not stripped.startswith('#') and not stripped.startswith('---'):
                first_content = stripped[:80]
                break
        
        conn.execute("INSERT INTO idx VALUES (?, ?, ?, ?)",
                     (relpath, fname, heading, content))
        entries.append({
            "relpath": relpath,
            "fname": fname,
            "heading": heading,
            "snippet": first_content,
            "size": len(content),
        })
    
    # Build directly in tmpfs (avoids backup which can hang on large data)
    conn.close()
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE VIRTUAL TABLE idx USING fts5(
            relpath, filename, heading, content,
            tokenize='porter unicode61'
        )
    """)
    for e in entries:
        conn.execute("INSERT INTO idx VALUES (?, ?, ?, ?)",
                     (e["relpath"], e["fname"], e["heading"],
                      open(os.path.join(WORKSPACE, e["relpath"]), 'r', errors='replace').read()))
    conn.execute("ANALYZE")
    conn.commit()
    
    elapsed = (time.time() - start) * 1000
    db_size = os.path.getsize(DB_PATH)
    print(f"Index built in {elapsed:.0f}ms. DB: {db_size:,} bytes ({db_size/1024:.1f} KB)")
    
    # Build stub index
    build_stub_index(entries)
    
    # Build topic map
    build_topic_map(entries)
    
    return len(entries)

TOPIC_MAP_PATH = os.path.join(SAVED_DIR, "topic-index.json")

SECTION_OVERRIDES = {
    "saved": "conversations",
}

def classify_file(relpath):
    """Classify a file into human-readable section."""
    for prefix, label in SECTION_OVERRIDES.items():
        if prefix in relpath:
            return label
    parts = relpath.split(os.sep)
    if len(parts) > 1:
        return parts[0]
    return "root"

def build_topic_map(entries):
    """Build a lightweight JSON topic map for fast lookup."""
    stopwords = set("the a an is was were are has have had do does did to of in for on at by with from as be been being having will would could should may might must shall can its their this that these those about into also not but or if so no up out all each any how what when where which who".split())
    
    topic_map = {}
    for e in entries:
        relpath = e["relpath"]
        heading = e["heading"]
        snippet = e["snippet"]
        
        tokens = set()
        # From path
        for part in relpath.replace('.md', '').replace('.txt', '').replace('_', ' ').replace('-', ' ').replace('/', ' ').split():
            if len(part) > 2 and part.lower() not in stopwords:
                tokens.add(part.lower())
        # From heading
        for word in heading.replace('-', ' ').replace('_', ' ').split():
            w = word.lower().strip(' ,.:;!?')
            if len(w) > 3 and w not in stopwords:
                tokens.add(w)
        
        for token in tokens:
            if token not in topic_map:
                topic_map[token] = []
            topic_map[token].append({
                "path": relpath,
                "heading": heading[:60],
                "snippet": snippet[:80]
            })
    
    os.makedirs(os.path.dirname(TOPIC_MAP_PATH), exist_ok=True)
    with open(TOPIC_MAP_PATH, 'w') as f:
        json.dump(topic_map, f, indent=1)
    
    map_size = os.path.getsize(TOPIC_MAP_PATH)
    topic_count = len(topic_map)
    print(f"Topic map: {TOPIC_MAP_PATH} ({map_size:,} bytes, {topic_count} topics)")

def build_stub_index(entries):
    """Build the always-in-context stub index markdown file."""
    total_bytes = sum(e["size"] for e in entries)
    
    lines = ["# Memory Stub Index", 
             f"_Generated: {time.strftime('%Y-%m-%d %H:%M')} | {len(entries)} files | {total_bytes:,} bytes_",
             ""]
    
    # Group by directory
    groups = {}
    for e in entries:
        parts = e["relpath"].split(os.sep)
        group = parts[0] if len(parts) > 1 else "root"
        if group not in groups:
            groups[group] = []
        groups[group].append(e)
    
    # Sort groups: memory first, then skills, then rest
    group_order = sorted(groups.keys(), 
                         key=lambda g: (0 if g == "memory" else 1 if g == "skills" else 2, g))
    
    for group in group_order:
        group_entries = sorted(groups[group], key=lambda e: e["relpath"])
        lines.append(f"## `{group}/`")
        for e in group_entries:
            display_path = "/".join(e["relpath"].split(os.sep)[1:]) if "/" in e["relpath"] else e["fname"]
            snippet = e["snippet"].replace('\n', ' ').replace('\r', '')
            h = e["heading"][:50] if e["heading"] else ""
            lines.append(f"- **{e['fname']}** | {h} | {snippet}")
        lines.append("")
    
    # Write stub - trim verbose session keys to keep it compact
    cleaned = []
    for line in lines:
        # Remove verbose "Session Key" noise from memory entries
        if "Session Key" in line:
            line = re.sub(r'\| Session Key: agent:main:[^ ]+', '', line)
        cleaned.append(line)
    
    os.makedirs(os.path.dirname(STUB_PATH), exist_ok=True)
    with open(STUB_PATH, 'w') as f:
        f.write('\n'.join(cleaned))
    
    stub_size = len('\n'.join(cleaned).encode('utf-8'))
    print(f"Stub index: {STUB_PATH} ({stub_size:,} bytes, {len(cleaned)} lines)")
    return STUB_PATH

def expand_query(query):
    """Expand natural-language terms to FTS5 boolean queries."""
    terms = re.findall(r'\b[a-zA-Z]{3,}\b', query)
    expanded_parts = []
    for term in terms:
        lower = term.lower()
        if lower in SYNONYM_MAP:
            expanded_parts.append(f"({SYNONYM_MAP[lower]})")
        else:
            expanded_parts.append(term)
    
    if expanded_parts:
        return " AND ".join(expanded_parts)
    return query

def search(query, limit=5, expand=True):
    """Search the index and return ranked results."""
    if not os.path.exists(DB_PATH):
        print("No index found. Run 'build' first.")
        return []
    
    conn = sqlite3.connect(DB_PATH)
    
    if expand:
        fts5_query = expand_query(query)
    else:
        fts5_query = query
    
    try:
        cursor = conn.execute("""
            SELECT relpath, filename, heading, bm25(idx, 10.0, 5.0, 5.0, 1.0) as score
            FROM idx WHERE idx MATCH ?
            ORDER BY score LIMIT ?
        """, (fts5_query, limit))
        results = cursor.fetchall()
    except sqlite3.OperationalError as e:
        print(f"Query error: {e}")
        print(f"  Query was: {fts5_query}")
        print("  Try simpler terms or check spelling.")
        results = []
    
    conn.close()
    return results

def show_tags():
    """Extract and show all topic tags from the index."""
    files = get_md_files()
    stopwords = set("the a an is was were are has have had do does did to of in for on at by with from as be been being having will would could should may might must shall can its their this that these those about into".split())
    
    tag_counts = {}
    for fp in files:
        try:
            with open(fp, 'r') as f:
                head = f.read(1000)
        except:
            continue
        
        relpath = os.path.relpath(fp, WORKSPACE)
        words = re.findall(r'\b[a-z]{3,}\b', head.lower())
        
        # Extract from path-based topics
        path_parts = relpath.replace('.md', '').split(os.sep)
        path_tags = [p for p in path_parts if len(p) > 2 and p not in stopwords]
        for t in path_tags:
            tag_counts[t] = tag_counts.get(t, 0) + 1
        
        # Extract significant words from first 200 chars
        sig = [w for w in words if w not in stopwords and len(w) > 3]
        for w in sig[:20]:
            tag_counts[w] = tag_counts.get(w, 0) + 1
    
    sorted_tags = sorted(tag_counts.items(), key=lambda x: -x[1])
    print(f"\n=== Top Topic Tags ({len(sorted_tags)} unique) ===")
    print(f"{'Tag':20s} {'Count':5s}")
    print("-" * 26)
    for tag, count in sorted_tags[:40]:
        if count >= 2:
            print(f"{tag:20s} {count:5d}")

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == "build":
        count = build_index()
        print(f"Done. {count} files indexed.")
    
    elif cmd == "search":
        if len(sys.argv) < 3:
            print("Usage: memory-index.py search <query>")
            sys.exit(1)
        query = " ".join(sys.argv[2:])
        results = search(query)
        if results:
            print(f"\n=== Results for: '{query}' ===")
            for relpath, fname, heading, score in results:
                print(f"  [{score:.2f}] {relpath}")
                if heading:
                    print(f"         {heading}")
            print(f"\n{len(results)} result(s)")
        else:
            # Fallback: try grep
            print("No FTS5 matches. Trying grep fallback...")
            import subprocess
            result = subprocess.run(
                ["grep", "-rl", "-m5", query, WORKSPACE],
                capture_output=True, text=True,
                env={"HOME": os.environ.get("HOME", os.path.expanduser("~"))}
            )
            matching = [l for l in result.stdout.strip().split('\n') if l]
            if matching:
                print(f"\n=== grep fallback results ===")
                for fp in matching[:5]:
                    rel = os.path.relpath(fp, WORKSPACE)
                    print(f"  {rel}")
            else:
                print("No matches found with grep either.")
    
    elif cmd == "tags":
        show_tags()
    
    elif cmd == "topic":
        if len(sys.argv) < 3:
            print("Usage: memory-index.py topic <topic>")
            sys.exit(1)
        topic = " ".join(sys.argv[2:])
        results = search(topic, limit=10)
        if results:
            print(f"\n=== Files for topic: '{topic}' ===")
            for relpath, fname, heading, score in results:
                print(f"  [{score:.2f}] {relpath}")
        else:
            print(f"No matches for '{topic}'")
    
    else:
        print(f"Unknown command: {cmd}")
        print(__doc__)

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
learn.py — Self-Learning Engine

Structured learning system with ID-based entries, pattern tracking,
priority system, verification loops, and promotion rules.

Usage:
  python3 scripts/learn.py --cycle              # Full learning cycle
  python3 scripts/learn.py --verify             # Check pending verifications
  python3 scripts/learn.py --status             # Show learning stats
  python3 scripts/learn.py --trail              # Dump full learning trail
  python3 scripts/learn.py --log TYPE 'summary' # Log a structured entry
  python3 scripts/learn.py --promote            # Check patterns ready for promotion
"""

import argparse
import json
import os
import sys
import glob
import random
import re
import string
from datetime import datetime, timedelta


LEARNING_TRAIL_PATH = os.path.join(
    os.environ.get("OPENCLAW_WORKSPACE", "/home/admin/.openclaw/workspace"),
    "memory",
    ".learning-trail.json",
)
WORKSPACE = os.environ.get("OPENCLAW_WORKSPACE", "/home/admin/.openclaw/workspace")
MEMORY_DIR = os.path.join(WORKSPACE, "memory")
LEARNINGS_DIR = os.path.join(WORKSPACE, ".learnings")


def ensure_trail():
    """Ensure learning trail exists with defaults."""
    default = {
        "version": 3,
        "last_cycle": None,
        "entries": [],       # LRN, ERR, FEAT entries
        "changes": [],       # Applied changes with verification
        "watchlist": [],     # Pattern tracking
        "principles": [],    # Distilled principles
        "graph": {           # Knowledge graph
            "nodes": [],     # event, lesson, principle, knowledge, pattern
            "edges": [],     # connections between nodes
        },
        "stats": {
            "total_entries": 0,
            "total_changes": 0,
            "verified_ok": 0,
            "reverted": 0,
            "total_nodes": 0,
            "total_edges": 0,
        },
    }
    if not os.path.exists(LEARNING_TRAIL_PATH):
        os.makedirs(MEMORY_DIR, exist_ok=True)
        with open(LEARNING_TRAIL_PATH, "w") as f:
            json.dump(default, f, indent=2)
        return default
    try:
        with open(LEARNING_TRAIL_PATH) as f:
            trail = json.load(f)
        # Migrate: add graph if missing
        if "graph" not in trail:
            trail["graph"] = {"nodes": [], "edges": []}
            trail["version"] = 3
            save_trail(trail)
        return trail
    except (json.JSONDecodeError, FileNotFoundError):
        with open(LEARNING_TRAIL_PATH, "w") as f:
            json.dump(default, f, indent=2)
        return default


def save_trail(trail):
    os.makedirs(MEMORY_DIR, exist_ok=True)
    with open(LEARNING_TRAIL_PATH, "w") as f:
        json.dump(trail, f, indent=2)


# ── Memory Management ───────────────────────────────────────────

def auto_daily_log(message, emoji="✅"):
    """Append a log entry to today's memory file."""
    today = datetime.now().strftime("%Y-%m-%d")
    path = os.path.join(MEMORY_DIR, f"{today}.md")
    os.makedirs(MEMORY_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%H:%M")
    entry = f"\n### {emoji} {timestamp} - {message}"
    with open(path, "a") as f:
        f.write(entry + "\n")
    return path


def search_memory(query, days=30):
    """Search across memory files for a query."""
    results = []
    cutoff = datetime.now() - timedelta(days=days)
    for f in sorted(glob.glob(os.path.join(MEMORY_DIR, "*.md")), reverse=True):
        if ".dreams" in f:
            continue
        try:
            mtime = datetime.fromtimestamp(os.path.getmtime(f))
            if mtime < cutoff:
                continue
            with open(f) as fh:
                content = fh.read()
            if query.lower() in content.lower():
                lines = content.split("\n")
                matches = [l.strip() for l in lines if query.lower() in l.lower()][:3]
                results.append({"file": os.path.relpath(f, WORKSPACE), "date": os.path.basename(f).replace(".md", ""), "matches": matches})
        except OSError:
            pass
    return results


def check_memory_retention(trail):
    """Check for expired learning entries (90 days without activity)."""
    now = datetime.now()
    expired = []
    for entry in trail.get("entries", []):
        last_seen = entry.get("last_seen")
        if not last_seen:
            continue
        try:
            days_since = (now - datetime.strptime(last_seen, "%Y-%m-%d")).days
        except ValueError:
            continue
        if days_since > 90 and entry.get("status") == "pending":
            entry["status"] = "wont_fix"
            expired.append((entry.get("id"), entry.get("summary", "")[:40], f"expired ({days_since}d)"))
    if expired:
        save_trail(trail)
    return expired


# ── Conversation Scoring ────────────────────────────────────────

def score_conversation(trail, accuracy=0, usefulness=0, efficiency=0, tone=0, proactiveness=0, notes=""):
    """Score a conversation on 5 dimensions (0-10)."""
    now = datetime.now()
    score = {
        "date": now.strftime("%Y-%m-%d"),
        "time": now.strftime("%H:%M"),
        "scores": {
            "accuracy": accuracy,
            "usefulness": usefulness,
            "efficiency": efficiency,
            "tone": tone,
            "proactiveness": proactiveness,
        },
        "average": round((accuracy + usefulness + efficiency + tone + proactiveness) / 5, 1),
        "notes": notes[:200],
    }
    trail.setdefault("scores", []).append(score)
    trail["stats"]["total_scores"] = trail["stats"].get("total_scores", 0) + 1
    save_trail(trail)
    print(f"📊 Scored: avg={score['average']}/10 (acc={accuracy} use={usefulness} eff={efficiency} ton={tone} pro={proactiveness})")
    return score


def show_score_trends(trail, days=7):
    """Show score trends for the last N days."""
    scores = trail.get("scores", [])
    cutoff = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    recent = [s for s in scores if s.get("date", "") >= cutoff]

    if not recent:
        print(f"No scores in the last {days} days.")
        return

    # Group by date
    by_date = {}
    for s in recent:
        d = s["date"]
        if d not in by_date:
            by_date[d] = []
        by_date[d].append(s)

    print(f"\n📈 Score Trends (last {days} days, {len(recent)} scores):\n")
    print(f"  {'Date':<12} {'Avg':>5} {'Acc':>4} {'Use':>4} {'Eff':>4} {'Ton':>4} {'Pro':>4}")
    print(f"  {'─'*40}")

    daily_avgs = []
    for date in sorted(by_date.keys()):
        day_scores = by_date[date]
        avg = sum(s["average"] for s in day_scores) / len(day_scores)
        s0 = day_scores[0]
        sc = s0["scores"]
        daily_avgs.append(avg)
        print(f"  {date:<12} {avg:>5.1f} {sc['accuracy']:>4} {sc['usefulness']:>4} {sc['efficiency']:>4} {sc['tone']:>4} {sc['proactiveness']:>4}")

    if len(daily_avgs) >= 2:
        trend = daily_avgs[-1] - daily_avgs[0]
        arrow = "↑" if trend > 0.5 else "↓" if trend < -0.5 else "→"
        print(f"\n  Trend: {arrow} ({daily_avgs[0]:.1f} → {daily_avgs[-1]:.1f})")


# ── Dynamic Memory Injection ────────────────────────────────────

TOPIC_KEYWORDS = {
    "weather": ["天气", "温度", "wind", "rain", "预报", "湿度", "气压"],
    "code": ["代码", "script", "python", "bug", "fix", "error", "代码"],
    "finance": ["金融", "股票", "stock", "交易", "东方财富", "mx"],
    "skill": ["skill", "skill", "clawhub", "技能"],
    "learning": ["improve", "learn", "reflect", "self-improvement", "学习", "改进"],
    "memory": ["memory", "remember", "recall", "记忆", "回想"],
    "browser": ["browser", "playwright", "自动化", "浏览器"],
    "config": ["config", "配置", "setup", "安装", "API", "key"],
    "general": ["general", "你好", "谢谢", "ok", "好的"],
}


def detect_topic(text):
    """Detect topic from text."""
    text_lower = text.lower()
    scores = {}
    for topic, keywords in TOPIC_KEYWORDS.items():
        count = sum(1 for kw in keywords if kw.lower() in text_lower)
        if count > 0:
            scores[topic] = count
    if scores:
        return max(scores, key=scores.get)
    return "general"


def build_memory_index(trail, days=30):
    """Build a topic-indexed memory index from daily logs."""
    index = {}
    cutoff = datetime.now() - timedelta(days=days)

    for f in sorted(glob.glob(os.path.join(MEMORY_DIR, "*.md")), reverse=True):
        if ".dreams" in f:
            continue
        try:
            mtime = datetime.fromtimestamp(os.path.getmtime(f))
            if mtime < cutoff:
                continue
            with open(f) as fh:
                content = fh.read()
            date = os.path.basename(f).replace(".md", "")
            topic = detect_topic(content)
            if topic not in index:
                index[topic] = []
            # Extract first few meaningful lines
            lines = [l.strip() for l in content.split("\n") if l.strip() and not l.startswith("#")][:3]
            index[topic].append({"date": date, "file": os.path.relpath(f, WORKSPACE), "summary": lines})
        except OSError:
            pass

    # Save index
    index_path = os.path.join(MEMORY_DIR, ".memory-index.json")
    with open(index_path, "w") as f:
        json.dump({"built": datetime.now().isoformat(), "index": index}, f, indent=2, ensure_ascii=False)

    return index


def query_topic_memory(topic, limit=3):
    """Query memory for a specific topic."""
    index_path = os.path.join(MEMORY_DIR, ".memory-index.json")
    if not os.path.exists(index_path):
        build_memory_index({})

    with open(index_path) as f:
        data = json.load(f)

    index = data.get("index", {})
    results = index.get(topic, [])
    return results[:limit]


# ── Knowledge Graph ─────────────────────────────────────────────

NODE_TYPES = ["event", "lesson", "principle", "knowledge", "pattern"]
EDGE_TYPES = ["caused_by", "led_to", "supports", "contradicts", "related_to", "derived_from"]


def create_graph_node(trail, node_type, content, tags=None, source=None):
    """Create a node in the knowledge graph."""
    if node_type not in NODE_TYPES:
        print(f"⚠️  Unknown node type: {node_type} (use: {', '.join(NODE_TYPES)})")
        return None

    now = datetime.now()
    node_id = f"{node_type[:3]}-{now.strftime('%Y%m%d')}-{len(trail['graph']['nodes'])+1:03d}"

    node = {
        "id": node_id,
        "type": node_type,
        "content": content[:200],
        "tags": tags or [],
        "source": source or "manual",
        "created": now.isoformat(),
        "updated": now.isoformat(),
        "confidence": 1.0 if node_type == "event" else 0.5,
    }

    trail["graph"]["nodes"].append(node)
    trail["stats"]["total_nodes"] = trail["stats"].get("total_nodes", 0) + 1
    save_trail(trail)
    print(f"🔷 Node created: [{node_id}] ({node_type}) {content[:60]}")
    return node_id


def create_graph_edge(trail, from_id, to_id, edge_type, properties=None):
    """Create an edge between two nodes."""
    if edge_type not in EDGE_TYPES:
        print(f"⚠️  Unknown edge type: {edge_type} (use: {', '.join(EDGE_TYPES)})")
        return None

    # Verify nodes exist
    node_ids = [n["id"] for n in trail["graph"]["nodes"]]
    if from_id not in node_ids:
        print(f"⚠️  Source node not found: {from_id}")
        return None
    if to_id not in node_ids:
        print(f"⚠️  Target node not found: {to_id}")
        return None

    edge = {
        "from": from_id,
        "to": to_id,
        "type": edge_type,
        "properties": properties or {},
        "created": datetime.now().isoformat(),
    }

    trail["graph"]["edges"].append(edge)
    trail["stats"]["total_edges"] = trail["stats"].get("total_edges", 0) + 1
    save_trail(trail)
    print(f"🔗 Edge created: [{from_id}] → [{to_id}] ({edge_type})")
    return edge


def query_graph(trail, node_id=None, node_type=None, tag=None, depth=1):
    """Query the knowledge graph."""
    nodes = trail["graph"]["nodes"]
    edges = trail["graph"]["edges"]

    # Find starting node(s)
    if node_id:
        start_nodes = [n for n in nodes if n["id"] == node_id]
    elif node_type:
        start_nodes = [n for n in nodes if n["type"] == node_type]
    elif tag:
        start_nodes = [n for n in nodes if tag in n.get("tags", [])]
    else:
        start_nodes = nodes

    if not start_nodes:
        print("No nodes found matching query.")
        return []

    # BFS up to depth
    visited = set()
    result_nodes = []
    result_edges = []
    queue = [(n, 0) for n in start_nodes]

    while queue:
        node, d = queue.pop(0)
        if node["id"] in visited:
            continue
        visited.add(node["id"])
        result_nodes.append(node)

        if d < depth:
            # Find connected nodes
            for edge in edges:
                if edge["from"] == node["id"]:
                    target = next((n for n in nodes if n["id"] == edge["to"]), None)
                    if target and target["id"] not in visited:
                        result_edges.append(edge)
                        queue.append((target, d + 1))
                elif edge["to"] == node["id"]:
                    source = next((n for n in nodes if n["id"] == edge["from"]), None)
                    if source and source["id"] not in visited:
                        result_edges.append(edge)
                        queue.append((source, d + 1))

    return result_nodes, result_edges


def print_graph(trail, node_id=None, node_type=None, tag=None, depth=1):
    """Print the knowledge graph in a readable format."""
    result = query_graph(trail, node_id, node_type, tag, depth)
    if not result or not result[0]:
        print("No nodes found.")
        return

    nodes, edges = result

    print(f"\n🕸️  Knowledge Graph ({len(nodes)} nodes, {len(edges)} edges):\n")

    # Print nodes grouped by type
    by_type = {}
    for n in nodes:
        t = n["type"]
        if t not in by_type:
            by_type[t] = []
        by_type[t].append(n)

    type_icons = {"event": "📌", "lesson": "💡", "principle": "📜", "knowledge": "📖", "pattern": "🔍"}

    for t in NODE_TYPES:
        if t in by_type:
            icon = type_icons.get(t, "•")
            print(f"  {icon} {t.upper()}s ({len(by_type[t])}):")
            for n in by_type[t]:
                tags_str = " " + ", ".join(n.get("tags", [])) if n.get("tags") else ""
                print(f"    [{n['id']}] {n['content'][:60]}{tags_str}")
                if n.get("confidence"):
                    print(f"           confidence: {n['confidence']:.1f}")

    # Print edges
    if edges:
        print(f"\n  🔗 Edges:")
        for e in edges:
            src = next((n for n in nodes if n["id"] == e["from"]), None)
            tgt = next((n for n in nodes if n["id"] == e["to"]), None)
            src_content = src["content"][:30] if src else e["from"]
            tgt_content = tgt["content"][:30] if tgt else e["to"]
            print(f"    {src_content}... ──{e['type']}──► {tgt_content}...")


def auto_link_graph(trail, new_node_id, content):
    """Auto-link a new node to existing nodes based on content similarity."""
    nodes = trail["graph"]["nodes"]
    new_lower = content.lower()

    linked = []
    for node in nodes:
        if node["id"] == new_node_id:
            continue
        node_lower = node["content"].lower()

        # Simple keyword overlap scoring
        new_words = set(new_lower.replace("'", "").split())
        node_words = set(node_lower.replace("'", "").split())
        overlap = new_words & node_words

        # Skip common words
        skip_words = {"the", "and", "for", "to", "in", "of", "a", "is", "not", "use", "should", "instead", "read", "tool"}
        overlap = overlap - skip_words

        if len(overlap) >= 2:
            edge_type = "related_to"
            if node["type"] == "event" and overlap & {"error", "fail", "wrong", "instead"}:
                edge_type = "caused_by"
            elif node["type"] == "lesson" and overlap & {"should", "prefer", "use"}:
                edge_type = "supports"
            elif node["type"] == "principle" and overlap & {"not", "instead", "rather"}:
                edge_type = "contradicts"

            create_graph_edge(trail, new_node_id, node["id"], edge_type)
            linked.append(node["id"])

    return linked


# ── Semantic Deduplication ──────────────────────────────────────

def _tokenize(text):
    """Simple tokenizer: split on whitespace/punctuation, lowercase."""
    import re
    # Split on non-word chars (works for both English and Chinese)
    tokens = re.findall(r'[\w\u4e00-\u9fff]+', text.lower())
    # For Chinese text, use character bigrams (no spaces between words)
    result = []
    for token in tokens:
        if any('\u4e00' <= c <= '\u9fff' for c in token):
            # Chinese: use character bigrams
            for i in range(len(token) - 1):
                result.append(token[i:i+2])
            result.append(token)  # Also add full token
        else:
            result.append(token)
    return result


def _build_tfidf(texts):
    """Build TF-IDF vectors from a list of texts using numpy."""
    import math
    
    # Tokenize all texts
    tokenized = [_tokenize(t) for t in texts]
    
    # Build vocabulary
    vocab = {}
    for tokens in tokenized:
        for t in tokens:
            if t not in vocab:
                vocab[t] = len(vocab)
    
    if not vocab:
        return [], {}
    
    vocab_size = len(vocab)
    n_docs = len(texts)
    
    # Compute TF
    tf = [[0.0] * vocab_size for _ in range(n_docs)]
    for i, tokens in enumerate(tokenized):
        for t in tokens:
            tf[i][vocab[t]] += 1.0
        # Normalize by document length
        if tokens:
            for j in range(vocab_size):
                tf[i][j] /= len(tokens)
    
    # Compute IDF
    idf = [0.0] * vocab_size
    for j in range(vocab_size):
        df = sum(1 for tokens in tokenized if any(vocab[t] == j for t in tokens))
        idf[j] = math.log((n_docs + 1) / (df + 1)) + 1
    
    # Compute TF-IDF
    tfidf = [[0.0] * vocab_size for _ in range(n_docs)]
    for i in range(n_docs):
        for j in range(vocab_size):
            tfidf[i][j] = tf[i][j] * idf[j]
    
    return tfidf, vocab


def _cosine_similarity(v1, v2):
    """Compute cosine similarity between two vectors."""
    import math
    dot = sum(a * b for a, b in zip(v1, v2))
    norm1 = math.sqrt(sum(a * a for a in v1))
    norm2 = math.sqrt(sum(b * b for b in v2))
    if norm1 == 0 or norm2 == 0:
        return 0.0
    return dot / (norm1 * norm2)


def semantic_dedup(trail, threshold=0.85):
    """Find semantically duplicate nodes using TF-IDF cosine similarity."""
    nodes = trail["graph"]["nodes"]
    if len(nodes) < 2:
        return []
    
    # Build TF-IDF for all node contents
    texts = [n["content"] for n in nodes]
    tfidf, vocab = _build_tfidf(texts)
    
    if not tfidf:
        return []
    
    # Find pairs with high similarity
    duplicates = []
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            sim = _cosine_similarity(tfidf[i], tfidf[j])
            if sim >= threshold:
                duplicates.append({
                    "node_a": nodes[i]["id"],
                    "node_b": nodes[j]["id"],
                    "similarity": round(sim, 3),
                    "content_a": nodes[i]["content"][:60],
                    "content_b": nodes[j]["content"][:60],
                })
    
    return duplicates


def merge_duplicate_nodes(trail, dup):
    """Merge two duplicate nodes, keeping the one with more edges."""
    nodes = trail["graph"]["nodes"]
    edges = trail["graph"]["edges"]
    
    node_a = next((n for n in nodes if n["id"] == dup["node_a"]), None)
    node_b = next((n for n in nodes if n["id"] == dup["node_b"]), None)
    
    if not node_a or not node_b:
        return None
    
    # Keep the node with more connections
    edges_a = sum(1 for e in edges if e["from"] == node_a["id"] or e["to"] == node_a["id"])
    edges_b = sum(1 for e in edges if e["from"] == node_b["id"] or e["to"] == node_b["id"])
    
    keep_id = node_a["id"] if edges_a >= edges_b else node_b["id"]
    remove_id = node_b["id"] if edges_a >= edges_b else node_a["id"]
    
    # Remove the node and its edges
    nodes[:] = [n for n in nodes if n["id"] != remove_id]
    edges[:] = [e for e in edges if e["from"] != remove_id and e["to"] != remove_id]
    
    trail["stats"]["merged"] = trail["stats"].get("merged", 0) + 1
    save_trail(trail)
    
    print(f"🔀 Merged [{remove_id}] → [{keep_id}] (similarity: {dup['similarity']})")
    return {"kept": keep_id, "removed": remove_id, "similarity": dup["similarity"]}


# ── Personalized PageRank ───────────────────────────────────────

def personalized_pagerank(trail, query_text, damping=0.85, iterations=20):
    """Compute Personalized PageRank for graph nodes based on query relevance."""
    import math
    
    nodes = trail["graph"]["nodes"]
    edges = trail["graph"]["edges"]
    
    if not nodes:
        return []
    
    n = len(nodes)
    node_ids = [n["id"] for n in nodes]
    id_to_idx = {nid: i for i, nid in enumerate(node_ids)}
    
    # Build adjacency matrix
    adj = [[0.0] * n for _ in range(n)]
    for e in edges:
        if e["from"] in id_to_idx and e["to"] in id_to_idx:
            adj[id_to_idx[e["from"]]][id_to_idx[e["to"]]] = 1.0
    
    # Compute personalization vector based on query similarity
    personalization = [0.0] * n
    query_tokens = set(_tokenize(query_text))
    
    for i, node in enumerate(nodes):
        node_tokens = set(_tokenize(node["content"]))
        overlap = query_tokens & node_tokens
        skip_words = {"the", "and", "for", "to", "in", "of", "a", "is", "not"}
        overlap = overlap - skip_words
        personalization[i] = len(overlap) + 0.01  # Small base for all nodes
    
    # Normalize personalization
    total_p = sum(personalization)
    if total_p > 0:
        personalization = [p / total_p for p in personalization]
    else:
        personalization = [1.0 / n] * n
    
    # Compute PageRank
    pagerank = [1.0 / n] * n
    
    for _ in range(iterations):
        new_pagerank = [0.0] * n
        for j in range(n):
            for i in range(n):
                if adj[i][j] > 0:
                    # Sum of outgoing edges from node i
                    out_degree = sum(adj[i])
                    if out_degree > 0:
                        new_pagerank[j] += pagerank[i] * adj[i][j] / out_degree
        
        # Apply damping and personalization
        for i in range(n):
            pagerank[i] = (1 - damping) * personalization[i] + damping * new_pagerank[i]
    
    # Sort by PageRank score
    ranked = sorted(zip(node_ids, pagerank), key=lambda x: x[1], reverse=True)
    return [(nid, round(score, 4)) for nid, score in ranked]


def query_graph_ranked(trail, query_text, top_k=5, depth=2):
    """Query graph and return nodes ranked by Personalized PageRank."""
    ranked = personalized_pagerank(trail, query_text)
    
    nodes = trail["graph"]["nodes"]
    edges = trail["graph"]["edges"]
    
    result = []
    for node_id, score in ranked[:top_k]:
        node = next((n for n in nodes if n["id"] == node_id), None)
        if node:
            # Find related edges
            related_edges = [e for e in edges if e["from"] == node_id or e["to"] == node_id]
            result.append({
                "node": node,
                "score": score,
                "edges": related_edges,
            })
    
    return result


def print_ranked_graph(trail, query_text, top_k=5):
    """Print ranked graph results."""
    results = query_graph_ranked(trail, query_text, top_k)
    
    if not results:
        print("No nodes found in graph.")
        return
    
    type_icons = {"event": "📌", "lesson": "💡", "principle": "📜", "knowledge": "📖", "pattern": "🔍"}
    
    print(f"\n🕸️  Graph ranked by: '{query_text}'\n")
    
    for i, r in enumerate(results, 1):
        node = r["node"]
        icon = type_icons.get(node["type"], "•")
        print(f"  {i}. {icon} [{node['id']}] (score: {r['score']:.4f})")
        print(f"     {node['content'][:80]}")
        if r["edges"]:
            for e in r["edges"][:3]:
                other = e["to"] if e["from"] == node["id"] else e["from"]
                direction = "→" if e["from"] == node["id"] else "←"
                print(f"     {direction} {e['type']} → [{other}]")
        print()


# ── Detection triggers ──────────────────────────────────────────

def next_id(trail, prefix):
    """Generate next ID: LRN-YYYYMMDD-001, etc."""
    today = datetime.now().strftime("%Y%m%d")
    existing = [
        e["id"] for e in trail.get("entries", [])
        if e["id"].startswith(f"{prefix}-{today}")
    ]
    nums = []
    for eid in existing:
        suffix = eid.split("-")[-1]
        try:
            nums.append(int(suffix))
        except ValueError:
            pass  # skip non-numeric suffixes like SI1
    if nums:
        next_num = max(nums) + 1
    else:
        next_num = len(existing) + 1  # fallback: sequential from count
    return f"{prefix}-{today}-{next_num:03d}"


# ── Log an entry ──────────────────────────────────────────────────

def log_entry(trail, entry_type, summary, area="tooling",
              priority="medium", source="self_discovery",
              pattern_key=None, details="", suggested_action="",
              reproduce_info="", extra_meta=None):
    """Log a structured learning/error/feature entry."""
    today = datetime.now().isoformat()
    date_str = datetime.now().strftime("%Y-%m-%d")

    prefix = {"learning": "LRN", "error": "ERR", "feature": "FEAT",
              "correction": "LRN", "knowledge_gap": "LRN",
              "best_practice": "LRN"}.get(entry_type, "LRN")

    if entry_type in ("correction", "knowledge_gap", "best_practice"):
        entry_type_display = entry_type
        entry_type = "learning"
    else:
        entry_type_display = entry_type

    eid = next_id(trail, prefix)

    entry = {
        "id": eid,
        "type": entry_type,
        "category": entry_type_display if entry_type == "learning" else None,
        "summary": summary[:120],
        "details": details,
        "suggested_action": suggested_action,
        "area": area,
        "priority": priority,
        "status": "pending",
        "logged": today,
        "source": source,
        "pattern_key": pattern_key,
        "recurrence_count": 0,
        "first_seen": date_str,
        "last_seen": date_str,
    }
    if extra_meta:
        entry.update(extra_meta)

    # Check for existing pattern
    if pattern_key:
        for existing in trail.get("entries", []):
            if existing.get("pattern_key") == pattern_key:
                existing["recurrence_count"] = existing.get("recurrence_count", 0) + 1
                existing["last_seen"] = date_str
                existing["status"] = "pending"  # Re-activate
                print(f"🔄 Pattern '{pattern_key}' incremented to {existing['recurrence_count']}x")
                save_trail(trail)
                return existing["id"]

    # New entry
    trail.setdefault("entries", []).append(entry)
    # Recalculate stats from actual data
    trail["stats"]["total_entries"] = len(trail["entries"])
    trail["stats"]["total_scores"] = len(trail.get("scores", []))
    if "total_nodes" in trail.get("stats", {}):
        trail["stats"]["total_nodes"] = len(trail.get("graph", {}).get("nodes", []))
    if "total_edges" in trail.get("stats", {}):
        trail["stats"]["total_edges"] = len(trail.get("graph", {}).get("edges", []))
    save_trail(trail)
    print(f"📝 [{eid}] {summary[:60]}")
    return eid


# ── Pattern tracking ─────────────────────────────────────────────

# ── Conflict Detection ──────────────────────────────────────────

CONFLICT_PAIRS = [
    ("headless", "gui"),
    ("read tool", "exec"),
    ("verbose", "concise"),
    ("manual", "automatic"),
    ("complex", "simple"),
]


def detect_conflicts(new_principle, existing_principles):
    """Check if a new principle conflicts with existing ones.
    Returns list of (existing, reason) tuples."""
    conflicts = []
    new_lower = new_principle.lower()

    for existing in existing_principles:
        existing_lower = existing.lower()
        # Check opposite-direction conflict pairs
        for a, b in CONFLICT_PAIRS:
            if (a in new_lower and b in existing_lower) or \
               (b in new_lower and a in existing_lower):
                conflicts.append((existing,
                    f"'{a}' vs '{b}' — opposite directions"))
                break
        # Check direct contradiction (same domain, opposite advice)
        if "don't" in new_lower and "don't" not in existing_lower:
            # Extract what's being negated
            for word in new_lower.replace("don't", "").split():
                if word in existing_lower and len(word) > 3:
                    conflicts.append((existing,
                        f"'{new_principle[:50]}' vs '{existing[:50]}' — direct contradiction"))
                    break

    return conflicts


def assign_priority_score(trail, entry):
    """Calculate numeric priority score for an entry.
    Higher = more important. Used for conflict resolution."""
    score = 0

    # Base priority
    priority_map = {"critical": 100, "high": 60, "medium": 30, "low": 10}
    score += priority_map.get(entry.get("priority", "medium"), 30)

    # Recurrence bonus
    rc = entry.get("recurrence_count", 0)
    score += rc * 10

    # Recency bonus
    last_seen = entry.get("last_seen")
    if last_seen:
        try:
            days_since = (datetime.now() - datetime.strptime(last_seen, "%Y-%m-%d")).days
            score += max(0, 30 - days_since)  # Up to 30 points for freshness
        except ValueError:
            pass

    # Area weight
    area_weights = {
        "security": 50, "behavior": 40, "tooling": 30,
        "config": 20, "tests": 20, "docs": 10,
    }
    score += area_weights.get(entry.get("area", ""), 0)

    return score


# ── Forgetting Mechanism ────────────────────────────────────────

FORGET_DAYS = 30  # Days after which a principle begins to fade


def apply_forgetting(trail):
    """Demote old principles that haven't been reinforced.
    Returns list of demoted principles."""
    now = datetime.now()
    demoted = []

    for entry in trail.get("entries", []):
        last_seen = entry.get("last_seen")
        if not last_seen:
            continue
        try:
            days_since = (now - datetime.strptime(last_seen, "%Y-%m-%d")).days
        except ValueError:
            continue

        # Old, never promoted → auto-resolve
        if days_since > FORGET_DAYS * 2 and entry.get("status") == "pending":
            old_priority = entry.get("priority", "medium")
            entry["priority"] = "low"
            if old_priority != "low":
                demoted.append((entry.get("id", "?"), entry.get("summary", "")[:40],
                              f"{old_priority}→low (unseen {days_since}d)"))

        # Very old, low priority → auto-resolve as wont_fix
        if days_since > FORGET_DAYS * 3 and entry.get("priority") == "low":
            if entry.get("status") == "pending":
                entry["status"] = "wont_fix"
                demoted.append((entry.get("id", "?"), entry.get("summary", "")[:40],
                              "auto-resolved (expired)"))

    # Also check principles array for staleness
    # (principles don't auto-expire, they need manual review)
    stale_principles = []
    for p in trail.get("principles", []):
        # Principles stay until explicitly removed
        pass

    save_trail(trail)
    return demoted


# ── Auto-Revert ─────────────────────────────────────────────────

def auto_revert_failed(trail, max_retries=2):
    """Auto-revert changes that have failed verification multiple times.
    Returns list of reverted change IDs."""
    reverted = []
    now = datetime.now()

    for change in trail.get("changes", []):
        if change.get("verified") or change.get("outcome") == "reverted":
            continue

        nc = change.get("next_check")
        if not nc:
            continue
        try:
            dt = datetime.strptime(nc, "%Y-%m-%d")
        except ValueError:
            continue

        # Overdue by 7+ days and not verified
        days_overdue = (now - dt).days
        if days_overdue < 7:
            continue  # Still within grace period

        check_count = change.get("check_count", 0)
        if check_count >= max_retries:
            # Mark as failed
            change["outcome"] = "auto_reverted"
            change["verified"] = False
            change["evidence"].append(f"Auto-reverted: unchecked for {days_overdue}d past deadline")
            trail["stats"]["reverted"] = trail["stats"].get("reverted", 0) + 1
            reverted.append(change["id"])
            summary = f"⚠️ Change '{change.get('change','')[:50]}' auto-reverted (overdue {days_overdue}d)"
            print(f"   {summary}")
        else:
            # Increment check count, extend deadline
            change["check_count"] = check_count + 1
            extension = (dt + timedelta(days=7)).strftime("%Y-%m-%d")
            change["next_check"] = extension
            change["evidence"].append(f"Extended to {extension} (attempt {check_count+1}/{max_retries})")

    if reverted:
        save_trail(trail)
    return reverted


def find_patterns_ready(trail, min_recurrence=2, min_sessions=2):
    """Find patterns with Recurrence-Count >= min_recurrence across min_sessions.
    Excludes patterns where all entries are already resolved or promoted."""
    ready = []
    entries = trail.get("entries", [])
    sessions_seen = {}

    for e in entries:
        pk = e.get("pattern_key")
        if not pk:
            continue
        # Skip already-resolved entries (but still count them for recurrence)
        if e.get("status") in ("wont_fix",):
            continue
        rc = e.get("recurrence_count", 0)
        if pk not in sessions_seen:
            sessions_seen[pk] = {"count": 0, "dates": set(), "entries": [], "all_resolved": True}
        sessions_seen[pk]["count"] = max(sessions_seen[pk]["count"], rc)
        sessions_seen[pk]["dates"].add(e.get("last_seen", ""))
        sessions_seen[pk]["entries"].append(e)
        if e.get("status") not in ("promoted", "resolved"):
            sessions_seen[pk]["all_resolved"] = False

    for pk, data in sessions_seen.items():
        if data["all_resolved"]:
            continue  # Pattern already handled
        if data["count"] >= min_recurrence and len(data["dates"]) >= min_sessions:
            # Use the most recent non-resolved entry for this pattern
            active = [e for e in data["entries"] if e.get("status") not in ("promoted", "resolved")]
            if not active:
                active = data["entries"]
            entries_sorted = sorted(active, key=lambda e: e.get("last_seen", ""), reverse=True)
            ready.append((pk, data["count"], entries_sorted[0]))
    return ready


def execute_promotion(trail, pattern_key, count, entry):
    """Actually promote a pattern by modifying the target file and recording a change for verification."""
    target = suggest_promotion(entry)
    summary = entry.get("summary", "")
    target_path = os.path.join(WORKSPACE, target)

    # Build the content to append
    now = datetime.now()
    if target == "MEMORY.md":
        line = f"- {summary}"
        section = "## Self-Improvement Principles"
    elif target == "TOOLS.md":
        line = f"- {summary}"
        section = "## Known Gotchas"
    elif target == "AGENTS.md":
        line = f"- {summary}"
        section = "## Red Lines"
    elif target == "SOUL.md":
        line = f"- {summary}"
        section = "## Boundaries"
    else:
        line = f"- {summary}"
        section = None

    # Read current file content
    try:
        with open(target_path, "r") as f:
            content = f.read()
    except FileNotFoundError:
        content = ""

    # Check if this line already exists
    if line in content:
        print(f"   ⏭️  Already in {target}: {line[:60]}")
        entry["status"] = "promoted"
        save_trail(trail)
        return None

    # Append to the appropriate section
    if section and section in content:
        # Find the section and append after first line after section header
        lines = content.split("\n")
        section_idx = None
        for i, l in enumerate(lines):
            if l.strip() == section:
                section_idx = i
                break
        if section_idx is not None:
            lines.insert(section_idx + 1, line)
            new_content = "\n".join(lines)
        else:
            new_content = content + "\n" + line + "\n"
    else:
        new_content = content + "\n" + line + "\n"

    # Write the file
    with open(target_path, "w") as f:
        f.write(new_content)

    # Record change for verification
    hypothesis = f"Promoting pattern '{pattern_key}' ({count}x) to {target} will improve consistency"
    record_change(trail, target, summary, hypothesis, source_entry=entry["id"],
                  change_type="pattern_promotion")

    # Also add to principles list for forgetting/reinforcement tracking
    principles = trail.setdefault("principles", [])
    if summary not in principles:
        principles.append(summary)

    # Mark all entries with this pattern_key as promoted
    entry["status"] = "promoted"
    for e in trail.get("entries", []):
        if e.get("pattern_key") == pattern_key and e["id"] != entry["id"]:
            if e.get("status") not in ("promoted", "resolved", "wont_fix"):
                e["status"] = "promoted"
    save_trail(trail)

    print(f"   ✅ Promoted to {target}: {line[:60]}")
    return target


def auto_detect_daily(trail):
    """Scan today's daily log and auto-detect learning opportunities.
    Closes the gap: agent doesn't need to remember to call detect_triggers."""
    today = datetime.now().strftime("%Y-%m-%d")
    daily_path = os.path.join(MEMORY_DIR, f"{today}.md")

    if not os.path.exists(daily_path):
        return 0

    with open(daily_path, "r") as f:
        content = f.read()

    if not content.strip():
        return 0

    # Detection patterns (subset of reflect.py, self-contained)
    detect_patterns = [
        ("correction", [r"不对", r"错了", r"搞错", r"不是这样", r"不是",
                        r"no,|not right|wrong|incorrect|mistake",
                        r"should be|should use|should do", r"你搞|骗我|假的|糊弄"]),
        ("feature", [r"能不能|可以.*吗|加个|加上|增加|做个|实现一下",
                     r"帮忙|帮我|给我|弄一个|搞一个",
                     r"can you also|can you add|i wish|i need"]),
        ("error", [r"失败|报错|出错|错误|不行|用不了|打不开|连不上",
                   r"超时|挂掉|崩溃|闪退|卡住",
                   r"failed|error|exception|traceback|timeout"]),
        ("knowledge_gap", [r"其实|实际上|真相是|本来.*是",
                           r"过时|废弃|不适用|改版|换了|迁移",
                           r"配置都没有|没有存|怎么没有"]),
    ]

    detected = []
    lines = content.split("\n")
    for line in lines:
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        # Focus on emoji-marked lines and longer content
        if not (stripped.startswith("###") or len(stripped) > 30):
            continue

        text_lower = stripped.lower()
        for trigger_type, patterns in detect_patterns:
            for pat in patterns:
                if re.search(pat, text_lower):
                    summary_text = stripped.lstrip("#\u2705\u274c\ud83d\udca1\ud83d\udccc\ud83e\udd16 ").strip()[:120]
                    # Dedup: skip if already logged
                    already_logged = any(
                        summary_text[:40] in e.get("summary", "")[:40]
                        for e in trail.get("entries", [])
                    )
                    if not already_logged:
                        area = "behavior" if trigger_type in ("correction", "knowledge_gap") else "tooling"
                        priority = "high" if trigger_type in ("correction", "error") else "medium"
                        pk = "auto-" + re.sub(r"[^a-z0-9\u4e00-\u9fff]+", "-", summary_text.lower())[:30].strip("-")
                        log_entry(trail, trigger_type, summary_text,
                                  area=area, priority=priority,
                                  pattern_key=pk, source="auto-detect")
                        detected.append((trigger_type, summary_text[:60]))
                    break  # one entry per line
            if any(p[0] == trigger_type for p in detected[-1:]):
                break

    return len(detected)


def generate_session_summary(trail):
    """Auto-generate L1 session summary from today's daily log."""
    today = datetime.now().strftime("%Y-%m-%d")
    daily_path = os.path.join(MEMORY_DIR, f"{today}.md")
    sessions_dir = os.path.join(MEMORY_DIR, "sessions")
    os.makedirs(sessions_dir, exist_ok=True)

    if not os.path.exists(daily_path):
        return None

    with open(daily_path, "r") as f:
        content = f.read()

    if not content.strip():
        return None

    # Extract significant entries
    tasks = []
    errors = []
    insights = []
    for l in content.split("\n"):
        stripped = l.strip()
        if stripped.startswith("### ✅"):
            tasks.append(stripped)
        elif stripped.startswith("### ❌"):
            errors.append(stripped)
        elif stripped.startswith("### 💡"):
            insights.append(stripped)

    if not tasks and not errors and not insights:
        return None

    # Check if content already exists in any today's summary (avoid duplicates)
    existing = sorted(glob.glob(os.path.join(sessions_dir, f"{today}-*.md")))
    new_body_lines = []
    for t in tasks:
        new_body_lines.append(f"- {t.replace('### ✅ ', '').strip()}")
    new_body = "\n".join(new_body_lines) if new_body_lines else ""

    for ext in existing:
        with open(ext) as f:
            ext_content = f.read()
        if new_body and new_body in ext_content:
            # Already summarized, skip
            return None

    seq = len(existing) + 1

    summary_path = os.path.join(sessions_dir, f"{today}-{seq:03d}.md")
    with open(summary_path, "w") as f:
        f.write(f"# Session Summary: {today}-{seq:03d}\n\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
        if tasks:
            f.write("## Tasks Completed\n")
            for t in tasks:
                f.write(f"- {t.replace('### ✅ ', '').strip()}\n")
            f.write("\n")
        if errors:
            f.write("## Errors\n")
            for e in errors:
                f.write(f"- {e.replace('### ❌ ', '').strip()}\n")
            f.write("\n")
        if insights:
            f.write("## Insights\n")
            for i in insights:
                f.write(f"- {i.replace('### 💡 ', '').strip()}\n")
            f.write("\n")
        # Add stats
        entries = trail.get("entries", [])
        recent = [e for e in entries if e.get("last_seen", "") == today]
        if recent:
            f.write(f"## Learning Trail\n")
            f.write(f"- {len(recent)} new entries today\n")
            f.write(f"- Total entries: {len(entries)}\n\n")

    return summary_path


def suggest_promotion(entry):
    """Suggest where to promote a recurring pattern."""
    area = entry.get("area", "")
    entry_type = entry.get("type", "")
    category = entry.get("category", "")

    if category == "correction" or area == "behavior":
        return "SOUL.md"
    elif category == "best_practice" or area in ("tooling", "infra"):
        return "TOOLS.md"
    elif area in ("frontend", "backend", "tests", "config"):
        return "AGENTS.md"
    elif entry_type == "error":
        return "TOOLS.md"
    else:
        return "MEMORY.md"


# ── Proposal Generation ─────────────────────────────────────────

def generate_proposals(trail):
    """Generate actionable improvement proposals for user review."""
    proposals = []
    now = datetime.now()

    # 1. Patterns ready for promotion
    ready = find_patterns_ready(trail)
    for entry in ready:
        target = suggest_promotion(entry)
        pk = entry.get("pattern_key", "unknown")
        # Calculate actual recurrence count across all entries with this pattern
        rc = max(e.get("recurrence_count", 0) for e in trail.get("entries", []) if e.get("pattern_key") == pk)
        summary = entry.get("summary", "")
        source = entry.get("source", "")

        # Generate specific change suggestion
        if target == "TOOLS.md":
            change = f"Add to Known Gotchas: '{summary}'"
            risk = "Low — adds a note, doesn't change behavior"
        elif target == "MEMORY.md":
            change = f"Append to Self-Improvement Principles: '{summary}'"
            risk = "Low — adds a principle, doesn't change behavior"
        elif target == "SOUL.md":
            change = f"Add behavioral guideline: '{summary}'"
            risk = "Medium — changes agent persona"
        elif target == "AGENTS.md":
            change = f"Add workflow rule: '{summary}'"
            risk = "Medium — changes agent conventions"
        else:
            change = f"Record: '{summary}'"
            risk = "Low"

        proposals.append({
            "type": "promotion",
            "id": entry.get("id", ""),
            "target": target,
            "change": change,
            "motivation": f"Pattern '{pk}' occurred {rc}x across sessions (source: {source})",
            "risk": risk,
            "effort": "low",
            "impact": "medium" if rc >= 3 else "high",
        })

    # 2. Overdue verifications that need attention
    due, _ = check_verifications(trail)
    for change in due:
        proposals.append({
            "type": "verification",
            "id": change.get("id", ""),
            "target": change.get("target", ""),
            "change": f"Verify: '{change.get('change','')[:60]}'",
            "motivation": f"Hypothesis: {change.get('hypothesis','')} — due since {change.get('next_check','')}",
            "risk": "Low — just checking",
            "effort": "low",
            "impact": "high",
        })

    # 3. High-priority pending items
    for entry in trail.get("entries", []):
        if entry.get("priority") == "critical" and entry.get("status") == "pending":
            proposals.append({
                "type": "critical_fix",
                "id": entry.get("id", ""),
                "target": suggest_promotion(entry),
                "change": f"Address: {entry.get('summary','')[:80]}",
                "motivation": f"Critical priority, {entry.get('recurrence_count',0)}x occurrences",
                "risk": "Medium",
                "effort": "medium",
                "impact": "high",
            })

    return proposals


def print_proposals(proposals):
    """Print proposals in a readable format for user review."""
    if not proposals:
        print("✅ No proposals at this time.")
        return

    print(f"\n📋 {len(proposals)} Proposal(s) for Review:\n")
    for i, p in enumerate(proposals, 1):
        print(f"  [{i}] {p['type'].upper()} → {p['target']}")
        print(f"      Change: {p['change']}")
        print(f"      Why: {p['motivation']}")
        print(f"      Risk: {p['risk']} | Effort: {p['effort']} | Impact: {p['impact']}")
        print()

    print("  To approve: tell me the proposal number")
    print("  To reject: tell me 'skip N'")


# ── Change tracking (for verification) ───────────────────────────

def record_change(trail, target, change, hypothesis,
                  source_entry=None, change_type="file_update"):
    """Record a change with verification tracking."""
    now = datetime.now()
    cid = f"change-{now.strftime('%Y%m%d')}-{trail['stats'].get('total_changes',0)+1:03d}"
    next_check = (now + timedelta(days=7)).strftime("%Y-%m-%d")

    entry = {
        "id": cid,
        "date": now.strftime("%Y-%m-%d"),
        "type": change_type,
        "target": target,
        "change": change[:200],
        "hypothesis": hypothesis[:200],
        "source_entry": source_entry,
        "verified": False,
        "outcome": None,
        "next_check": next_check,
        "check_count": 0,
        "evidence": [],
    }
    trail.setdefault("changes", []).append(entry)
    trail["stats"]["total_changes"] = trail["stats"].get("total_changes", 0) + 1
    save_trail(trail)
    print(f"📌 Change recorded: {cid} → {target} (verify by {next_check})")
    return cid


def check_verifications(trail):
    """Find changes due for verification."""
    now = datetime.now()
    due = []
    pending = []
    for change in trail.get("changes", []):
        if change.get("verified") or change.get("outcome"):
            continue
        nc = change.get("next_check")
        if not nc:
            due.append(change)
        else:
            try:
                dt = datetime.strptime(nc, "%Y-%m-%d")
                if dt <= now:
                    due.append(change)
                else:
                    pending.append(change)
            except ValueError:
                due.append(change)
    return due, pending


# ── Status & reports ─────────────────────────────────────────────

def recalc_stats(trail):
    """Recalculate stats from actual data to prevent drift."""
    trail["stats"]["total_entries"] = len(trail.get("entries", []))
    trail["stats"]["total_changes"] = len(trail.get("changes", []))
    trail["stats"]["total_scores"] = len(trail.get("scores", []))
    trail["stats"]["total_nodes"] = len(trail.get("graph", {}).get("nodes", []))
    trail["stats"]["total_edges"] = len(trail.get("graph", {}).get("edges", []))
    save_trail(trail)
    return trail["stats"]


def show_status(trail):
    trail["stats"] = recalc_stats(trail)
    entries = trail.get("entries", [])
    changes = trail.get("changes", [])
    watchlist = trail.get("watchlist", [])
    principles = trail.get("principles", [])
    stats = trail.get("stats", {})

    print(f"📊 Learning System Status")
    print(f"   Last cycle: {trail.get('last_cycle', 'never')}")
    print(f"   Total entries: {stats.get('total_entries', 0)}")
    print(f"   Changes made: {stats.get('total_changes', 0)}")
    print(f"   Verified OK: {stats.get('verified_ok', 0)}")
    print(f"   Reverted: {stats.get('reverted', 0)}")
    print(f"   Principles: {len(principles)}")

    # Count by priority
    by_priority = {}
    for e in entries:
        p = e.get("priority", "medium")
        by_priority[p] = by_priority.get(p, 0) + 1
    if by_priority:
        print(f"\n📋 Entries by priority:")
        for p in ["critical", "high", "medium", "low"]:
            if p in by_priority:
                print(f"   {p}: {by_priority[p]}")

    # Pending verifications
    due, pend = check_verifications(trail)
    print(f"\n🔍 Verifications: {len(due)} due, {len(pend)} monitoring")

    # Patterns ready for promotion
    ready = find_patterns_ready(trail)
    if ready:
        print(f"\n🚀 Patterns ready for promotion:")
        for r in ready:
            print(f"   • [{r.get('id','?')}] {r.get('summary','')[:60]} → {suggest_promotion(r)}")


def run_full_cycle(trail, auto_promote=True, auto_summary=True):
    now = datetime.now()
    trail["last_cycle"] = now.isoformat()
    trail["stats"] = recalc_stats(trail)

    actions_taken = []
    print(f"🔄 Learning Cycle — {now.strftime('%Y-%m-%d %H:%M')}\n")

    # Phase 1: 记忆 — Check recent memory
    print(f"📁 Phase 1: Memory scan")
    recent = glob.glob(os.path.join(MEMORY_DIR, "*.md"))
    recent = [f for f in recent if ".dreams" not in f
              and os.path.basename(f) != ".learning-trail.json"]
    print(f"   {len(recent)} memory file(s)")

    # Phase 2: 提炼 — Check verifications
    due, pend = check_verifications(trail)
    print(f"\n✅ Phase 2: Verification check")
    print(f"   {len(due)} due for review, {len(pend)} still monitoring")
    for d in due:
        print(f"   └ [{d.get('id','?')}] {d.get('target','?')}: {d.get('hypothesis','')[:60]}")
        if d.get("id"):
            actions_taken.append(f"⚠️  Verify change [{d['id']}]: {d.get('hypothesis','')[:60]}")

    # Phase 3: 提炼 — Pattern promotion (core)
    ready = find_patterns_ready(trail)
    promoted_count = 0
    print(f"\n🚀 Phase 3: Pattern promotion")
    if ready:
        for pk, count, entry in ready:
            target = suggest_promotion(entry)
            print(f"   └ [{entry.get('id','?')}] {pk} ({count}x) → {target}")
            if auto_promote:
                result = execute_promotion(trail, pk, count, entry)
                if result:
                    promoted_count += 1
                    actions_taken.append(f"📝 Promoted '{pk}' to {result}")
        if promoted_count > 0:
            print(f"   ✅ Auto-promoted {promoted_count} pattern(s)")
    else:
        print(f"   No patterns ready (need ≥2 occurrences across ≥2 sessions)")

    # Phase 4: 记忆维护 — Forgetting
    demoted = apply_forgetting(trail)
    print(f"\n⏳ Phase 4: Forgetting check")
    if demoted:
        for eid, summary, detail in demoted:
            print(f"   └ {detail}: [{eid}] {summary}")
    else:
        print(f"   No principles expired")

    # Phase 5: 提炼 — Auto-revert
    reverted = auto_revert_failed(trail)
    print(f"\n↩️ Phase 5: Auto-revert check")
    if reverted:
        print(f"   Auto-reverted: {len(reverted)} changes")
        actions_taken.append(f"↩️  Auto-reverted {len(reverted)} failed change(s)")
    else:
        print(f"   No overdue changes to revert")

    # Phase 6: 记忆维护 — Retention
    expired = check_memory_retention(trail)
    print(f"\n🗑️ Phase 6: Memory retention")
    if expired:
        print(f"   {len(expired)} entries expired (auto-resolved)")
    else:
        print(f"   No expired entries")

    # Phase 7: 检测 — Auto-detect from daily log
    print(f"\n🔍 Phase 7: Auto-detect learning")
    try:
        detected = auto_detect_daily(trail)
        if detected:
            print(f"   ✅ Detected {detected} new learning(s) from daily log")
            actions_taken.append(f"🔍 Auto-detected {detected} learning(s)")
        else:
            print(f"   No new patterns detected")
    except Exception as e:
        print(f"   Auto-detect failed: {e}")

    # Phase 8: 🌙 Dream — Memory distillation
    print(f"\n🌙 Phase 8: Dream — Memory distillation")
    try:
        import subprocess
        dream_script = os.path.join(os.path.dirname(__file__), "dream.py")
        result = subprocess.run(
            [sys.executable, dream_script, "--run", "--days", "14"],
            capture_output=True, text=True, timeout=120
        )
        if "updated MEMORY.md" in result.stdout:
            print(f"   ✅ Distilled new learnings into MEMORY.md")
            actions_taken.append(f"🌙 Dream: distilled memory from recent logs")
        elif "already up to date" in result.stdout:
            print(f"   ✅ MEMORY.md is current, nothing to add")
        else:
            for line in result.stdout.split('\n'):
                if line.strip():
                    print(f"   {line}")
    except Exception as e:
        print(f"   Dream failed: {e}")

    # Phase 9: 记忆 — Index build
    print(f"\n📚 Phase 9: Memory index")
    try:
        index = build_memory_index(trail)
        topics = list(index.keys())
        print(f"   {len(topics)} topics indexed: {', '.join(topics)}")
    except Exception as e:
        print(f"   Index build failed: {e}")

    # Phase 10: 记忆 — Session summary (L1)
    print(f"\n📝 Phase 10: Session summary")
    if auto_summary:
        summary_path = generate_session_summary(trail)
        if summary_path:
            print(f"   ✅ Generated: {os.path.relpath(summary_path, WORKSPACE)}")
            actions_taken.append(f"📝 Session summary saved")
        else:
            print(f"   No new activity to summarize")
    else:
        print(f"   Skipped")

    # Final summary
    trail["stats"] = recalc_stats(trail)
    stats = trail.get("stats", {})
    print(f"\n📊 Final Summary")
    print(f"   Entries: {stats.get('total_entries',0)} | Changes: {stats.get('total_changes',0)} | Verified: {stats.get('verified_ok',0)}")
    print(f"   Promoted: {promoted_count} | Graph: {stats.get('total_nodes',0)}n/{stats.get('total_edges',0)}e")

    if actions_taken:
        print(f"\n⚡ Actions taken this cycle:")
        for a in actions_taken:
            print(f"   {a}")
        # Write cycle summary to daily log for agent visibility
        daily_path = os.path.join(MEMORY_DIR, now.strftime("%Y-%m-%d") + ".md")
        try:
            with open(daily_path, "a") as f:
                f.write(f"\n### 🤖 {now.strftime('%H:%M')} - Self-improvement cycle\n")
                for a in actions_taken:
                    f.write(f"- {a}\n")
        except OSError:
            pass
    else:
        print(f"\n✅ No changes needed — system is stable")


# ── CLI ──────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Self-learning engine")
    parser.add_argument("--cycle", action="store_true", help="Full learning cycle")
    parser.add_argument("--verify", action="store_true", help="Check pending verifications")
    parser.add_argument("--status", action="store_true", help="Show learning stats")
    parser.add_argument("--trail", action="store_true", help="Dump full learning trail")
    parser.add_argument("--promote", action="store_true", help="Check patterns ready for promotion")
    parser.add_argument("--log", nargs=2, metavar=("TYPE", "SUMMARY"),
                        help="Log entry: TYPE=learning|error|feature|correction SUMMARY='text'")
    parser.add_argument("--area", default="tooling", help="Area for log entry")
    parser.add_argument("--priority", default="medium",
                        choices=["critical", "high", "medium", "low"])
    parser.add_argument("--pattern-key", default=None, help="Pattern key for dedup")
    parser.add_argument("--source", default=None,
                        choices=["conversation", "error", "user_feedback", "self_discovery"],
                        help="Log entry source (default: self_discovery)")
    parser.add_argument("--add-change", "--record-change", nargs=3, metavar=("TARGET", "CHANGE", "HYPOTHESIS"),
                        help="Record a change with verification")
    parser.add_argument("--add-principle", nargs=1, metavar="PRINCIPLE",
                        help="Add a distilled principle")
    parser.add_argument("--log-daily", nargs=1, metavar="MESSAGE",
                        help="Auto-log to today's memory file")
    parser.add_argument("--search-memory", nargs=1, metavar="QUERY",
                        help="Search across memory files")
    parser.add_argument("--retention", action="store_true",
                        help="Check for expired entries (90d)")
    parser.add_argument("--propose", action="store_true",
                        help="Generate improvement proposals for user review")
    parser.add_argument("--score", nargs=5, metavar=("ACC", "USE", "EFF", "TON", "PRO"),
                        help="Score last conversation (0-10 each: accuracy, usefulness, efficiency, tone, proactiveness)")
    parser.add_argument("--trends", type=int, default=0, metavar="DAYS",
                        help="Show score trends for last N days")
    parser.add_argument("--build-index", action="store_true",
                        help="Build topic-indexed memory index")
    parser.add_argument("--query-memory", nargs=1, metavar="TOPIC",
                        help="Query memory by topic")
    parser.add_argument("--graph-node", nargs=3, metavar=("TYPE", "CONTENT", "SOURCE"),
                        help="Create graph node: TYPE=event|lesson|principle|knowledge|pattern CONTENT='text' SOURCE='manual|auto'")
    parser.add_argument("--graph-edge", nargs=3, metavar=("FROM", "TO", "TYPE"),
                        help="Create graph edge: FROM=node_id TO=node_id TYPE=caused_by|led_to|supports|contradicts|related_to|derived_from")
    parser.add_argument("--graph-query", nargs="?", const="all",
                        help="Query graph: --graph-query [node_id|type:TYPE|tag:TAG]")
    parser.add_argument("--graph-auto-link", nargs=2, metavar=("NODE_ID", "CONTENT"),
                        help="Auto-link a node to existing nodes based on content similarity")
    parser.add_argument("--graph-rank", nargs=1, metavar="QUERY",
                        help="Rank graph nodes by query using Personalized PageRank")
    parser.add_argument("--graph-dedup", type=float, default=0.0, metavar="THRESHOLD",
                        help="Find semantically duplicate nodes (threshold 0.0-1.0)")
    parser.add_argument("--merge-nodes", nargs=2, metavar=("NODE_A", "NODE_B"),
                        help="Merge two duplicate nodes by ID")
    args = parser.parse_args()

    trail = ensure_trail()

    if args.cycle:
        run_full_cycle(trail)
    elif args.verify:
        due, pend = check_verifications(trail)
        print(f"🔍 Verifications: {len(due)} due, {len(pend)} monitoring")
        for d in due:
            print(f"\n  [{d.get('id','?')}] → {d.get('target','?')}")
            print(f"    Change: {d.get('change','')[:80]}")
            print(f"    Hypothesis: {d.get('hypothesis','')[:80]}")
            print(f"    Due: {d.get('next_check','?')}")
    elif args.status:
        show_status(trail)
    elif args.trail:
        print(json.dumps(trail, indent=2))
    elif args.promote:
        ready = find_patterns_ready(trail)
        if ready:
            print(f"🚀 {len(ready)} pattern(s) ready for promotion, executing...\n")
            promoted = 0
            for pk, count, entry in ready:
                result = execute_promotion(trail, pk, count, entry)
                if result:
                    promoted += 1
            print(f"\n✅ Promoted {promoted}/{len(ready)} patterns")
        else:
            print("No patterns ready for promotion yet (need ≥2 occurrences across ≥2 sessions)")
    elif args.log:
        etype, summary = args.log
        log_entry(trail, etype, summary,
                  area=args.area, priority=args.priority,
                  pattern_key=args.pattern_key,
                  source=args.source)
    elif args.add_change:
        target, change, hypothesis = args.add_change
        record_change(trail, target, change, hypothesis)
    elif args.add_principle:
        p = args.add_principle[0]
        if p not in trail.get("principles", []):
            trail.setdefault("principles", []).append(p)
            save_trail(trail)
            print(f"💎 Principle added: '{p[:60]}'")
    elif args.log_daily:
        msg = args.log_daily[0]
        path = auto_daily_log(msg)
        print(f"📝 Logged to {os.path.relpath(path, WORKSPACE)}")
    elif args.search_memory:
        query = args.search_memory[0]
        results = search_memory(query)
        if results:
            print(f"🔍 Found {len(results)} file(s) matching '{query}':")
            for r in results:
                print(f"  [{r['date']}] {r['file']}")
                for m in r['matches']:
                    print(f"    → {m[:80]}")
        else:
            print(f"No results for '{query}'")
    elif args.retention:
        expired = check_memory_retention(trail)
        if expired:
            print(f"🗑️ {len(expired)} expired entries resolved:")
            for eid, summary, detail in expired:
                print(f"  [{eid}] {summary} — {detail}")
        else:
            print("✅ No expired entries")
    elif args.propose:
        proposals = generate_proposals(trail)
        print_proposals(proposals)
    elif args.score:
        acc, use, eff, ton, pro = [int(x) for x in args.score]
        score_conversation(trail, acc, use, eff, ton, pro)
    elif args.trends > 0:
        show_score_trends(trail, args.trends)
    elif args.build_index:
        index = build_memory_index(trail)
        topics = list(index.keys())
        print(f"📚 Built memory index: {len(topics)} topics ({', '.join(topics)})")
    elif args.query_memory:
        topic = args.query_memory[0]
        results = query_topic_memory(topic)
        if results:
            print(f"🔍 Memory for topic '{topic}':")
            for r in results:
                print(f"  [{r['date']}] {r['file']}")
                for line in r.get('summary', []):
                    print(f"    → {line[:80]}")
        else:
            print(f"No memory found for topic '{topic}'")
            print(f"  Try: --build-index first")
    elif args.graph_node:
        node_type, content, source = args.graph_node
        node_id = create_graph_node(trail, node_type, content, source=source)
        if node_id:
            # Auto-link to existing nodes
            linked = auto_link_graph(trail, node_id, content)
            if linked:
                print(f"  🔗 Auto-linked to: {', '.join(linked)}")
    elif args.graph_edge:
        from_id, to_id, edge_type = args.graph_edge
        create_graph_edge(trail, from_id, to_id, edge_type)
    elif args.graph_query:
        query = args.graph_query
        if query == "all":
            print_graph(trail)
        elif query.startswith("type:"):
            node_type = query[5:]
            print_graph(trail, node_type=node_type)
        elif query.startswith("tag:"):
            tag = query[4:]
            print_graph(trail, tag=tag)
        else:
            print_graph(trail, node_id=query)
    elif args.graph_auto_link:
        node_id, content = args.graph_auto_link
        linked = auto_link_graph(trail, node_id, content)
        if linked:
            print(f"🔗 Auto-linked to: {', '.join(linked)}")
        else:
            print("No auto-links found.")
    elif args.graph_rank:
        query = args.graph_rank[0]
        print_ranked_graph(trail, query)
    elif args.merge_nodes:
        nid_a, nid_b = args.merge_nodes
        dups = semantic_dedup(trail, 0.0)
        match = next((d for d in dups if {"node_a": nid_a, "node_b": nid_b} == {"node_a": d["node_a"], "node_b": d["node_b"]} or {"node_a": nid_a, "node_b": nid_b} == {"node_a": d["node_b"], "node_b": d["node_a"]}), None)
        if match:
            merge_duplicate_nodes(trail, match)
        else:
            print(f"No duplicate pair found for [{nid_a}] ↔ [{nid_b}]")
            print("  Run --graph-dedup first to find duplicates")
    elif args.graph_dedup > 0:
        threshold = args.graph_dedup
        dups = semantic_dedup(trail, threshold)
        if dups:
            print(f"🔍 Found {len(dups)} potential duplicates (threshold: {threshold}):")
            for d in dups:
                print(f"  [{d['node_a']}] ↔ [{d['node_b']}] (sim: {d['similarity']})")
                print(f"    A: {d['content_a']}")
                print(f"    B: {d['content_b']}")
            print(f"\n  To merge: --merge-nodes {dups[0]['node_a']} {dups[0]['node_b']}")
        else:
            print(f"No duplicates found above threshold {threshold}")
    else:
        show_status(trail)


if __name__ == "__main__":
    main()

"""
Visual Agent Orchestration System
==================================
A standalone frontend for visually arranging agent nodes on a 2D canvas,
then exporting the spatial layout to OASIS-compatible YAML schedule format.

Spatial Semantics:
  - Nodes connected by directed edges → sequential `expert` steps (workflow/pipeline)
  - Nodes grouped in a cluster (circle) → `parallel` step (brainstorm/group chat)
  - All nodes selected → `all_experts: true`
  - Manual injection nodes → `manual` steps

Run:
  python visual/main.py
  Open http://127.0.0.1:51210
"""

import json
import math
import os
import re
import sys
from typing import Optional

import requests
import yaml
from flask import Flask, jsonify, request, send_from_directory

# Add project root so we can import oasis modules
_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
_PROJECT_ROOT = os.path.dirname(_THIS_DIR)
sys.path.insert(0, _PROJECT_ROOT)

# Try to load the default expert configs from the project
_EXPERTS_PATH = os.path.join(_PROJECT_ROOT, "data", "prompts", "oasis_experts.json")
DEFAULT_EXPERTS = []
try:
    with open(_EXPERTS_PATH, "r", encoding="utf-8") as f:
        DEFAULT_EXPERTS = json.load(f)
except FileNotFoundError:
    # Fallback built-in experts if file not found
    DEFAULT_EXPERTS = [
        {"name": "创意专家", "tag": "creative", "persona": "Creative thinker", "temperature": 0.9},
        {"name": "批判专家", "tag": "critical", "persona": "Critical analyst", "temperature": 0.3},
        {"name": "数据分析师", "tag": "data", "persona": "Data-driven analyst", "temperature": 0.5},
        {"name": "综合顾问", "tag": "synthesis", "persona": "Synthesis advisor", "temperature": 0.5},
        {"name": "经济学家", "tag": "economist", "persona": "Economist", "temperature": 0.5},
        {"name": "法学家", "tag": "lawyer", "persona": "Legal expert", "temperature": 0.3},
        {"name": "成本限制者", "tag": "cost_controller", "persona": "Cost controller", "temperature": 0.4},
        {"name": "收益规划者", "tag": "revenue_planner", "persona": "Revenue planner", "temperature": 0.6},
        {"name": "创新企业家", "tag": "entrepreneur", "persona": "Entrepreneur", "temperature": 0.8},
        {"name": "普通人", "tag": "common_person", "persona": "Common person", "temperature": 0.7},
    ]

# Emoji mapping for expert tags
TAG_EMOJI = {
    "creative": "🎨", "critical": "🔍", "data": "📊", "synthesis": "🎯",
    "economist": "📈", "lawyer": "⚖️", "cost_controller": "💰",
    "revenue_planner": "📊", "entrepreneur": "🚀", "common_person": "🧑",
    "manual": "📝", "custom": "⭐",
}

# ── Main Agent connection config ──
# Read PORT_AGENT from config/.env; credentials come from user input (not stored in backend)
_ENV_PATH = os.path.join(_PROJECT_ROOT, "config", ".env")
_AGENT_PORT = "51200"
try:
    if os.path.isfile(_ENV_PATH):
        with open(_ENV_PATH, "r", encoding="utf-8") as _ef:
            for _line in _ef:
                _line = _line.strip()
                if _line.startswith("PORT_AGENT="):
                    _AGENT_PORT = _line.split("=", 1)[1].strip() or "51200"
except Exception:
    pass

MAIN_AGENT_URL = os.getenv("MAIN_AGENT_URL", f"http://127.0.0.1:{_AGENT_PORT}")

app = Flask(__name__, static_folder=os.path.join(_THIS_DIR, "static"))


# ──────────────────────────────────────────────────────────────
# Spatial → YAML Conversion Logic
# ──────────────────────────────────────────────────────────────

def _distance(a: dict, b: dict) -> float:
    """Euclidean distance between two nodes."""
    return math.sqrt((a["x"] - b["x"]) ** 2 + (a["y"] - b["y"]) ** 2)


def _detect_clusters(nodes: list[dict], threshold: float = 150.0) -> list[list[dict]]:
    """
    Detect spatial clusters of nodes using simple distance-based grouping.
    Nodes within `threshold` pixels of each other are considered in the same cluster.
    Uses Union-Find for efficient clustering.
    """
    n = len(nodes)
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb

    # Union nodes that are close to each other
    for i in range(n):
        for j in range(i + 1, n):
            if _distance(nodes[i], nodes[j]) < threshold:
                union(i, j)

    # Group by root
    clusters: dict[int, list[dict]] = {}
    for i in range(n):
        root = find(i)
        clusters.setdefault(root, []).append(nodes[i])

    return list(clusters.values())


def _is_circular_arrangement(nodes: list[dict], tolerance: float = 0.4) -> bool:
    """
    Check if nodes are arranged roughly in a circle.
    Computes centroid, then checks if distances from centroid have low variance.
    tolerance: max coefficient of variation (std/mean) to consider circular.
    """
    if len(nodes) < 3:
        return False

    cx = sum(n["x"] for n in nodes) / len(nodes)
    cy = sum(n["y"] for n in nodes) / len(nodes)

    dists = [math.sqrt((n["x"] - cx) ** 2 + (n["y"] - cy) ** 2) for n in nodes]
    mean_d = sum(dists) / len(dists)
    if mean_d < 1:
        return False

    variance = sum((d - mean_d) ** 2 for d in dists) / len(dists)
    std_d = math.sqrt(variance)
    cv = std_d / mean_d

    return cv < tolerance


def _topological_sort_edges(edges: list[dict], node_map: dict) -> list[str]:
    """
    Given directed edges, produce a topological ordering of node IDs.
    Returns ordered list of node IDs following the edge direction.
    """
    # Build adjacency and in-degree using node IDs
    adj: dict[str, list[str]] = {}
    in_deg: dict[str, int] = {}
    all_in_edges = set()

    for edge in edges:
        src = edge.get("source", "")
        tgt = edge.get("target", "")
        adj.setdefault(src, []).append(tgt)
        in_deg.setdefault(src, 0)
        in_deg[tgt] = in_deg.get(tgt, 0) + 1
        all_in_edges.add(src)
        all_in_edges.add(tgt)

    # Kahn's algorithm
    queue = [n for n in all_in_edges if in_deg.get(n, 0) == 0]
    result = []
    while queue:
        node = queue.pop(0)
        result.append(node)
        for neighbor in adj.get(node, []):
            in_deg[neighbor] -= 1
            if in_deg[neighbor] == 0:
                queue.append(neighbor)

    return result


def _node_yaml_name(node: dict, use_bot_session: bool = False) -> str:
    """Convert a canvas node to an OASIS YAML expert name.

    Each node carries an ``instance`` number (≥1) so the same agent can appear
    multiple times in a layout with distinct identities.

    For expert nodes:
      - use_bot_session=False → "tag#temp#<instance>" (stateless ExpertAgent)
      - use_bot_session=True  → "tag#oasis#new"       (stateful SessionExpert)
    For external nodes:
      - "tag#ext#<ext_id>"  (external API agent)
    For session_agent nodes:
      - "title#session_id#<instance>" when instance > 1 (multiple uses of same session)
      - "title#session_id"            when instance == 1
    """
    inst = node.get("instance", 1)
    node_type = node.get("type", "expert")

    if node_type == "external":
        tag = node.get("tag", "custom")
        ext_id = node.get("ext_id", "1")
        return f"{tag}#ext#{ext_id}"

    if node_type == "session_agent":
        title = node.get("name", "Agent")[:7]
        sid = node.get("session_id", "")
        if sid:
            # Oasis sessions already have the format "tag#oasis#id",
            # so don't prepend title to avoid breaking tag resolution.
            if "#oasis#" in sid:
                if inst > 1:
                    return f"{sid}#{inst}"
                return sid
            if inst > 1:
                return f"{title}#{sid}#{inst}"
            return f"{title}#{sid}"
        return title

    tag = node.get("tag", "custom")
    if use_bot_session:
        return f"{tag}#oasis#new"
    return f"{tag}#temp#{inst}"


def _has_fan_in(edges: list[dict]) -> bool:
    """Check if any node has multiple incoming edges (fan-in), requiring DAG mode."""
    in_count: dict[str, int] = {}
    for e in edges:
        tgt = e.get("target", "")
        in_count[tgt] = in_count.get(tgt, 0) + 1
    return any(c > 1 for c in in_count.values())


def _has_fan_out(edges: list[dict]) -> bool:
    """Check if any node has multiple outgoing edges (fan-out), requiring DAG mode."""
    out_count: dict[str, int] = {}
    for e in edges:
        src = e.get("source", "")
        out_count[src] = out_count.get(src, 0) + 1
    return any(c > 1 for c in out_count.values())


def layout_to_yaml(data: dict) -> str:
    """
    Convert the canvas layout data to OASIS-compatible YAML schedule.

    When edges form a DAG with fan-in or fan-out (a node has multiple
    predecessors or successors), outputs DAG format with id/depends_on
    so the engine can maximize parallelism. Otherwise falls back to the
    simpler linear step list.

    Input data format:
    {
        "nodes": [
            {"id": "n1", "name": "创意专家", "tag": "creative", "x": 100, "y": 200, "type": "expert"},
            {"id": "n2", "name": "批判专家", "tag": "critical", "x": 300, "y": 200, "type": "expert"},
            {"id": "n3", "name": "助手", "tag": "session", "x": 500, "y": 200, "type": "session_agent", "session_id": "abc123"},
            ...
        ],
        "edges": [
            {"source": "n1", "target": "n2"},
            ...
        ],
        "groups": [
            {"id": "g1", "name": "Brainstorm Group", "nodeIds": ["n3", "n4", "n5"], "type": "parallel"},
            ...
        ],
        "settings": {
            "repeat": false,
            "max_rounds": 5,
            "use_bot_session": false,
            "cluster_threshold": 150
        }
    }
    """
    nodes = data.get("nodes", [])
    edges = data.get("edges", [])
    groups = data.get("groups", [])
    settings = data.get("settings", {})

    repeat = settings.get("repeat", False)
    use_bot_session = settings.get("use_bot_session", False)
    node_map = {n["id"]: n for n in nodes}

    def _make_expert_step(node):
        """Build a plan step dict for an expert/external node."""
        step = {"expert": _node_yaml_name(node, use_bot_session)}
        if node.get("type") == "external":
            for _ek in ("api_url", "api_key", "model"):
                if node.get(_ek):
                    step[_ek] = node[_ek]
            if node.get("headers") and isinstance(node["headers"], dict):
                step["headers"] = node["headers"]
        return step

    plan = []

    # Step 1: Process explicit groups (user-drawn circles/clusters)
    grouped_node_ids = set()
    for group in groups:
        group_type = group.get("type", "parallel")
        member_ids = group.get("nodeIds", [])
        grouped_node_ids.update(member_ids)

        if group_type == "all":
            plan.append({"all_experts": True})
        elif group_type == "parallel":
            par_items = []
            for nid in member_ids:
                if nid not in node_map:
                    continue
                mn = node_map[nid]
                if mn.get("type") == "external":
                    par_items.append(_make_expert_step(mn))
                else:
                    par_items.append(_node_yaml_name(mn, use_bot_session))
            if par_items:
                plan.append({"parallel": par_items})
        elif group_type == "manual":
            content = group.get("content", "Please continue the discussion.")
            author = group.get("author", "主持人")
            plan.append({"manual": {"author": author, "content": content}})

    # Step 2: Process edges → workflow steps
    # Filter edges that connect ungrouped nodes
    workflow_edges = [
        e for e in edges
        if e["source"] not in grouped_node_ids and e["target"] not in grouped_node_ids
    ]

    # Track which node IDs have been consumed by edges/clusters
    edge_consumed_ids: set = set()

    if workflow_edges:
        # Decide: DAG mode (id + depends_on) vs linear mode
        use_dag = _has_fan_in(workflow_edges) or _has_fan_out(workflow_edges)

        if use_dag:
            # ── DAG mode: emit steps with id and depends_on ──
            # Build predecessors map: node_id → [predecessor node_ids]
            preds: dict[str, list[str]] = {}
            all_edge_nodes = set()
            for e in workflow_edges:
                src, tgt = e["source"], e["target"]
                preds.setdefault(tgt, []).append(src)
                all_edge_nodes.add(src)
                all_edge_nodes.add(tgt)

            # Assign stable step IDs based on node id
            for nid in _topological_sort_edges(workflow_edges, node_map):
                node = node_map.get(nid)
                if not node:
                    continue
                edge_consumed_ids.add(nid)

                if node.get("type") == "manual":
                    step = {
                        "id": nid,
                        "manual": {
                            "author": node.get("author", "主持人"),
                            "content": node.get("content", ""),
                        },
                    }
                else:
                    step = _make_expert_step(node)
                    step["id"] = nid

                deps = preds.get(nid, [])
                if deps:
                    step["depends_on"] = deps

                plan.append(step)
        else:
            # ── Linear mode (simple chain): topological sort → sequential ──
            ordered_ids = _topological_sort_edges(workflow_edges, node_map)
            for nid in ordered_ids:
                node = node_map.get(nid)
                if not node:
                    continue
                edge_consumed_ids.add(nid)
                if node.get("type") == "manual":
                    plan.append({
                        "manual": {
                            "author": node.get("author", "主持人"),
                            "content": node.get("content", ""),
                        }
                    })
                else:
                    plan.append(_make_expert_step(node))
    else:
        # Step 3: Process remaining ungrouped, unconnected nodes
        # Auto-detect spatial patterns
        remaining = [n for n in nodes if n["id"] not in grouped_node_ids and n.get("type") not in ("manual",)]

        if remaining:
            threshold = settings.get("cluster_threshold", 150)
            clusters = _detect_clusters(remaining, threshold)

            for cluster in clusters:
                if len(cluster) == 1:
                    # Single node → sequential expert step
                    plan.append(_make_expert_step(cluster[0]))
                elif _is_circular_arrangement(cluster):
                    # Circular arrangement → parallel (brainstorm)
                    par_items = []
                    for cn in cluster:
                        if cn.get("type") == "external":
                            par_items.append(_make_expert_step(cn))
                        else:
                            par_items.append(_node_yaml_name(cn, use_bot_session))
                    plan.append({"parallel": par_items})
                else:
                    # Linear/scattered cluster → sort by x-coordinate for left-to-right order
                    sorted_nodes = sorted(cluster, key=lambda n: (n["x"], n["y"]))
                    for n in sorted_nodes:
                        plan.append(_make_expert_step(n))

    # Step 4: Process manual injection nodes (skip those already consumed by edges)
    manual_nodes = [n for n in nodes if n.get("type") == "manual" and n["id"] not in grouped_node_ids and n["id"] not in edge_consumed_ids]
    for mn in manual_nodes:
        plan.append({
            "manual": {
                "author": mn.get("author", "主持人"),
                "content": mn.get("content", ""),
            }
        })

    # Build final YAML structure
    schedule = {
        "version": 1,
        "repeat": repeat,
        "plan": plan if plan else [{"all_experts": True}],
    }

    return yaml.dump(schedule, allow_unicode=True, default_flow_style=False, sort_keys=False)


# ──────────────────────────────────────────────────────────────
# Flask Routes
# ──────────────────────────────────────────────────────────────

@app.route("/")
def index():
    """Serve the main visual editor page."""
    return send_from_directory(_THIS_DIR, "index.html")


@app.route("/api/experts", methods=["GET"])
def get_experts():
    """Return the available expert pool."""
    experts_with_emoji = []
    for e in DEFAULT_EXPERTS:
        emoji = TAG_EMOJI.get(e["tag"], "⭐")
        experts_with_emoji.append({**e, "emoji": emoji})
    return jsonify(experts_with_emoji)


@app.route("/api/generate-yaml", methods=["POST"])
def generate_yaml():
    """Convert canvas layout to OASIS YAML schedule."""
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    try:
        yaml_output = layout_to_yaml(data)
        return jsonify({"yaml": yaml_output})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/generate-prompt", methods=["POST"])
def generate_prompt():
    """Generate a structured LLM prompt for YAML schedule generation."""
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    try:
        prompt = _build_llm_prompt(data)
        return jsonify({"prompt": prompt})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def _build_llm_prompt(data: dict) -> str:
    """Build a comprehensive LLM prompt from the canvas layout data."""
    nodes = data.get("nodes", [])
    edges = data.get("edges", [])
    groups = data.get("groups", [])
    settings = data.get("settings", {})

    node_map = {n["id"]: n for n in nodes}

    # ── Describe the experts involved ──
    expert_nodes = [n for n in nodes if n.get("type") not in ("manual",)]
    manual_nodes = [n for n in nodes if n.get("type") == "manual"]

    expert_list_str = ""
    for i, n in enumerate(expert_nodes, 1):
        inst = n.get("instance", 1)
        inst_label = f" [instance #{inst}]" if inst > 1 else ""
        if n.get("type") == "session_agent":
            expert_list_str += f"  {i}. {n['emoji']} {n['name']}{inst_label} [SESSION AGENT: session_id={n.get('session_id', '?')}] — existing agent with its own tools & memory\n"
        elif n.get("type") == "external":
            expert_list_str += f"  {i}. {n['emoji']} {n['name']}{inst_label} [EXTERNAL API: api_url={n.get('api_url', '?')}] — external OpenAI-compatible service\n"
        else:
            expert_list_str += f"  {i}. {n['emoji']} {n['name']}{inst_label} (tag: {n['tag']}, temperature: {n.get('temperature', 0.5)}, source: {n.get('source', 'public')})\n"

    # ── Describe relationships ──
    relationships = []

    # Edges → workflow connections
    if edges:
        # Filter to ungrouped edges for DAG detection
        _grouped_ids = set()
        for g in groups:
            _grouped_ids.update(g.get("nodeIds", []))
        _wf_edges = [e for e in edges if e["source"] not in _grouped_ids and e["target"] not in _grouped_ids]
        _is_dag = _has_fan_in(_wf_edges) or _has_fan_out(_wf_edges) if _wf_edges else False

        chains = []
        for e in edges:
            src = node_map.get(e["source"], {})
            tgt = node_map.get(e["target"], {})
            chains.append(f"    {src.get('name', '?')} ({e['source']}) → {tgt.get('name', '?')} ({e['target']})")
        if _is_dag:
            relationships.append(
                "DAG workflow connections (has fan-in or fan-out — use id/depends_on DAG format):\n"
                + "\n".join(chains)
                + "\n    ⚠ Nodes with all predecessors complete should start immediately (maximize parallelism)."
            )
        else:
            relationships.append("Sequential workflow connections (simple chain — use linear format):\n" + "\n".join(chains))

    # Groups
    for g in groups:
        member_names = [node_map[nid]["name"] for nid in g.get("nodeIds", []) if nid in node_map]
        if g["type"] == "parallel":
            relationships.append(f"Parallel group \"{g['name']}\": [{', '.join(member_names)}] — these experts should speak simultaneously.")
        elif g["type"] == "all":
            relationships.append(f"All-experts group: all selected experts speak simultaneously.")

    # Manual injections
    if manual_nodes:
        for mn in manual_nodes:
            relationships.append(f"Manual injection by \"{mn.get('author', '主持人')}\": \"{mn.get('content', '')}\"")

    relationships_str = "\n".join(relationships) if relationships else "  No specific relationships defined — experts are freely arranged on canvas."

    # ── Describe spatial layout ──
    spatial_desc = ""
    if len(expert_nodes) >= 2:
        # Check if circular
        if _is_circular_arrangement(expert_nodes):
            spatial_desc = "Experts are arranged in a CIRCULAR pattern, suggesting a brainstorm/round-table discussion where all speak in parallel."
        else:
            # Check if mostly horizontal (workflow-like)
            xs = [n["x"] for n in expert_nodes]
            ys = [n["y"] for n in expert_nodes]
            x_range = max(xs) - min(xs)
            y_range = max(ys) - min(ys) if ys else 0
            if x_range > y_range * 2:
                sorted_by_x = sorted(expert_nodes, key=lambda n: n["x"])
                order_str = " → ".join(n["name"] for n in sorted_by_x)
                spatial_desc = f"Experts are arranged horizontally (left to right), suggesting a SEQUENTIAL pipeline: {order_str}"
            elif y_range > x_range * 2:
                sorted_by_y = sorted(expert_nodes, key=lambda n: n["y"])
                order_str = " → ".join(n["name"] for n in sorted_by_y)
                spatial_desc = f"Experts are arranged vertically (top to bottom), suggesting a SEQUENTIAL pipeline: {order_str}"
            else:
                spatial_desc = "Experts are scattered on canvas — use your best judgment to determine the optimal collaboration pattern."
    elif len(expert_nodes) == 1:
        spatial_desc = f"Only one expert: {expert_nodes[0]['name']}. This will be a single expert step."
    else:
        spatial_desc = "No expert nodes on canvas."

    # ── Settings description ──
    repeat_str = "true (repeat plan every round — good for debates/discussions)" if settings.get("repeat", False) else "false (execute plan once — good for task pipelines)"
    bot_session_str = "Stateful bot mode (experts have memory + tools, suitable for complex task execution)" if settings.get("use_bot_session", False) else "Stateless discussion mode (lightweight, no memory, suitable for debates/brainstorming)"

    # ── Generate current rule YAML as reference ──
    try:
        current_rule_yaml = layout_to_yaml(data)
    except Exception:
        current_rule_yaml = ""

    # ── Build the final prompt ──
    prompt = f"""You are an OASIS schedule YAML generator. Based on the user's visual arrangement of expert agents on a canvas, generate an optimal OASIS-compatible YAML schedule.

## OASIS YAML Format Rules

The YAML supports two modes: **Linear** (simple chain) and **DAG** (directed acyclic graph with parallelism).

### Linear Mode (simple sequential pipeline):
```yaml
version: 1
repeat: true/false
plan:
  - expert: "tag#temp#1"          # Preset expert instance 1 (stateless, uses tag)
  - expert: "tag#temp#2"          # Same expert, 2nd instance
  - expert: "tag#oasis#new"       # Preset expert (stateful session, auto-create)
  - expert: "Title#session_id"    # Existing session agent (with its own tools & memory)
  - parallel:                     # Multiple experts speak simultaneously
      - "creative#temp#1"
      - "Title#session_id"
  - all_experts: true             # All selected experts speak at once
  - manual:                       # Inject fixed content (bypass LLM)
      author: "主持人"
      content: "Please summarize..."
```

### DAG Mode (when nodes have fan-in or fan-out — i.e. a node has multiple predecessors or successors):
When the workflow is NOT a simple chain, use `id` and `depends_on` fields to express the dependency graph.
The engine will run nodes in parallel whenever their dependencies are satisfied — no unnecessary waiting.

```yaml
version: 1
repeat: false
plan:
  - id: n1                        # Unique step identifier (use the canvas node id)
    expert: "creative#temp#1"     # Root node — no depends_on, starts immediately
  - id: n2
    expert: "critical#temp#1"     # Another root — runs in PARALLEL with n1
  - id: n3
    expert: "writer#temp#1"
    depends_on: [n1, n2]          # Fan-in: waits for BOTH n1 and n2 to finish
  - id: n4
    expert: "reviewer#temp#1"
    depends_on: [n3]              # Runs after n3 completes
```

**DAG rules:**
- Every step MUST have a unique `id` field.
- `depends_on` is a list of step ids that must complete before this step starts. Omit it for root nodes (no predecessors).
- The graph MUST be acyclic (no circular dependencies).
- Steps with no dependency relationship run in parallel automatically.
- `manual` steps can also have `id`/`depends_on`:
  ```yaml
  - id: m1
    manual:
      author: "主持人"
      content: "Summarize the above"
    depends_on: [n3, n4]
  ```

**When to use which mode:**
- Use **Linear** when the workflow is a simple A→B→C chain (every node has at most one predecessor and one successor).
- Use **DAG** when any node has multiple incoming edges (fan-in) or any node has multiple outgoing edges (fan-out).

## Expert Name Formats
1. `tag#temp#N` — Preset expert instance N (stateless), e.g. "creative#temp#1", "creative#temp#2" (same expert used twice)
2. `tag#oasis#new` — Preset expert (stateful session, auto-creates new session), use when bot_session mode is ON
3. `Title#session_id` — Existing session agent, referenced by actual session_id, has its own system prompt, tools & memory
4. `Title#session_id#N` — Same session agent used multiple times (N>1)

## Available Step Types
1. `expert: "Name"` — Single expert speaks in order
2. `parallel: ["A", "B"]` — Multiple experts speak simultaneously (linear mode only)
3. `all_experts: true` — Everyone speaks at once (linear mode only)
4. `manual: {{author, content}}` — Inject fixed text (no LLM)
5. `id` + `depends_on` — DAG dependency declaration (DAG mode, can combine with expert or manual)

## Current Canvas State

### Experts on canvas ({len(expert_nodes)} total):
{expert_list_str}
### Arrangement & Relationships:
{relationships_str}

### Spatial Layout Analysis:
{spatial_desc}

### Settings:
- repeat: {repeat_str}
- Mode: {bot_session_str}

## Current Rule YAML (Auto-generated Reference)

**IMPORTANT**: The following YAML was auto-generated from the canvas layout using a rule-based algorithm.
It contains the complete configuration for each agent (including api_url, headers, model, etc.).
If the reference YAML contains `id` and `depends_on` fields, it means the workflow is a DAG —
you MUST preserve DAG format in your output. The auto-generated dependency graph is accurate;
focus on verifying the expert configurations and adjusting if needed.
For simple linear workflows (no `id`/`depends_on`), the ordering may need adjustment based on
the canvas relationships and spatial layout analysis above.

```yaml
{current_rule_yaml if current_rule_yaml else "# (no rule YAML could be generated)"}
```

## Your Task

Based on the above canvas arrangement, generate an OASIS YAML schedule that:
1. Respects the explicit connections (edges define dependency order)
2. Uses **DAG format** (id + depends_on) when the workflow has fan-in or fan-out; uses **linear format** for simple chains
3. Respects the explicit groups (parallel groups = simultaneous speaking)
4. Interprets the spatial arrangement when no explicit connections exist
5. Uses `repeat: {str(settings.get('repeat', False)).lower()}`
6. Maximizes parallelism — nodes with no dependency relationship should be able to run concurrently

You MUST follow this exact order:
1. FIRST, call the `set_oasis_workflow` tool to save the generated YAML as a named workflow (so the workflow is immediately ready to use from the OASIS panel).
2. THEN, output the complete YAML schedule in your response text.

Both steps are mandatory and the order matters — save first, then output."""

    return prompt


@app.route("/api/agent-generate-yaml", methods=["POST"])
def agent_generate_yaml():
    """Generate YAML by sending the LLM prompt to the main agent gateway.

    Flow:
    1. Build a structured LLM prompt from the canvas layout
    2. Send the prompt to mainagent /v1/chat/completions
    3. Extract YAML from the agent's response
    4. Return both the prompt and the generated YAML
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    try:
        # Step 1: Build the prompt
        prompt = _build_llm_prompt(data)

        # Step 2: Send to main agent with user credentials
        agent_url = f"{MAIN_AGENT_URL}/v1/chat/completions"

        # Extract credentials from the request (sent by frontend)
        credentials = data.get("credentials", {})
        username = credentials.get("username", "")
        password = credentials.get("password", "")

        if not username or not password:
            return jsonify({
                "prompt": prompt,
                "error": "Missing credentials. Please enter username and password in the login form.",
                "agent_yaml": None,
            })

        headers = {"Content-Type": "application/json"}
        # Use user:password Bearer format (OpenAI-compatible auth)
        headers["Authorization"] = f"Bearer {username}:{password}"

        payload = {
            "model": "mini-timebot",
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are a YAML schedule generator for the OASIS expert orchestration engine. "
                        "You have TWO tasks to complete IN ORDER:\n\n"
                        "1. FIRST: Call the `set_oasis_workflow` MCP tool to save the generated YAML as a named workflow "
                        "(use a descriptive name based on the task/experts, e.g. 'code_review_pipeline', 'brainstorm_trio').\n"
                        "2. THEN: Output the complete YAML schedule in your response text.\n\n"
                        "The schedule supports two modes: LINEAR (simple sequential steps) and DAG (steps with `id` and `depends_on` "
                        "fields for parallel execution with dependency tracking). Use DAG mode when the workflow has fan-in or fan-out.\n"
                        "No markdown fences around the YAML. Both steps are mandatory and the order matters — save first, then output."
                    ),
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            "stream": False,
            "session_id": "visual_orchestrator",
            "temperature": 0.3,
        }

        resp = requests.post(agent_url, json=payload, headers=headers, timeout=60)

        if resp.status_code != 200:
            return jsonify({
                "prompt": prompt,
                "error": f"Main agent returned HTTP {resp.status_code}: {resp.text[:500]}",
                "agent_yaml": None,
            })

        # Step 3: Extract YAML from agent response (OpenAI format)
        result = resp.json()
        agent_reply = ""
        try:
            agent_reply = result["choices"][0]["message"]["content"]
        except (KeyError, IndexError):
            agent_reply = str(result)

        # Clean up: strip markdown code fences if present
        agent_yaml = _extract_yaml_from_response(agent_reply)

        # Step 4: Validate the generated YAML
        validation = _validate_generated_yaml(agent_yaml)

        return jsonify({
            "prompt": prompt,
            "agent_yaml": agent_yaml,
            "agent_reply_raw": agent_reply,
            "validation": validation,
        })

    except requests.exceptions.ConnectionError:
        # Agent not running — fall back to prompt-only mode
        prompt = _build_llm_prompt(data)
        return jsonify({
            "prompt": prompt,
            "error": (
                f"Cannot connect to main agent at {MAIN_AGENT_URL}. "
                "Make sure mainagent.py is running (python src/mainagent.py). "
                "The prompt has been generated — you can copy it and use it manually."
            ),
            "agent_yaml": None,
        })
    except requests.exceptions.Timeout:
        prompt = _build_llm_prompt(data)
        return jsonify({
            "prompt": prompt,
            "error": "Main agent request timed out (60s). The prompt has been generated for manual use.",
            "agent_yaml": None,
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def _extract_yaml_from_response(text: str) -> str:
    """Extract YAML content from an LLM response that may contain markdown fences."""
    # Try to find ```yaml ... ``` block
    yaml_match = re.search(r"```(?:yaml)?\s*\n(.*?)```", text, re.DOTALL)
    if yaml_match:
        return yaml_match.group(1).strip()

    # Try to find content starting with 'version:'
    version_match = re.search(r"(version:\s*\d+.*)", text, re.DOTALL)
    if version_match:
        return version_match.group(1).strip()

    # Return as-is
    return text.strip()


def _validate_generated_yaml(yaml_str: str) -> dict:
    """Validate the generated YAML and return validation info."""
    try:
        parsed = yaml.safe_load(yaml_str)
        if not isinstance(parsed, dict):
            return {"valid": False, "error": "YAML did not parse to a dictionary"}

        has_version = "version" in parsed
        has_plan = "plan" in parsed
        plan_steps = len(parsed.get("plan", []))

        if not has_version or not has_plan:
            return {
                "valid": False,
                "error": f"Missing required fields: {'version' if not has_version else ''} {'plan' if not has_plan else ''}".strip(),
            }

        # Check step types
        step_types = []
        for step in parsed.get("plan", []):
            if isinstance(step, dict):
                if "expert" in step:
                    step_types.append("expert")
                elif "parallel" in step:
                    step_types.append("parallel")
                elif "all_experts" in step:
                    step_types.append("all_experts")
                elif "manual" in step:
                    step_types.append("manual")
                else:
                    step_types.append("unknown")

        return {
            "valid": True,
            "version": parsed.get("version"),
            "repeat": parsed.get("repeat", False),
            "steps": plan_steps,
            "step_types": step_types,
        }
    except yaml.YAMLError as e:
        return {"valid": False, "error": f"YAML parse error: {str(e)}"}


@app.route("/api/validate-yaml", methods=["POST"])
def validate_yaml():
    """Validate a YAML schedule string."""
    data = request.get_json()
    yaml_str = data.get("yaml", "")

    try:
        from oasis.scheduler import parse_schedule
        schedule = parse_schedule(yaml_str)
        return jsonify({
            "valid": True,
            "steps": len(schedule.steps),
            "repeat": schedule.repeat,
            "step_types": [s.step_type.value for s in schedule.steps],
        })
    except Exception as e:
        return jsonify({"valid": False, "error": str(e)})


@app.route("/api/save-layout", methods=["POST"])
def save_layout():
    """Save the current canvas layout as YAML (no separate layout JSON stored)."""
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    name = data.get("name", "untitled")
    safe_name = "".join(c for c in name if c.isalnum() or c in "-_ ").strip() or "untitled"

    try:
        yaml_output = layout_to_yaml(data)
    except Exception as e:
        return jsonify({"error": f"YAML conversion failed: {e}"}), 500

    yaml_dir = os.path.join(_PROJECT_ROOT, "data", "user_files", "default", "oasis", "yaml")
    os.makedirs(yaml_dir, exist_ok=True)
    fpath = os.path.join(yaml_dir, f"{safe_name}.yaml")
    with open(fpath, "w", encoding="utf-8") as f:
        f.write(f"# Saved from visual orchestrator\n{yaml_output}")

    return jsonify({"saved": True, "path": fpath})


@app.route("/api/load-layouts", methods=["GET"])
def load_layouts():
    """List all saved YAML workflows as available layouts."""
    yaml_dir = os.path.join(_PROJECT_ROOT, "data", "user_files", "default", "oasis", "yaml")
    if not os.path.isdir(yaml_dir):
        return jsonify([])

    layouts = []
    for fname in sorted(os.listdir(yaml_dir)):
        if fname.endswith((".yaml", ".yml")):
            layouts.append(fname.replace('.yaml', '').replace('.yml', ''))
    return jsonify(layouts)


@app.route("/api/load-layout/<name>", methods=["GET"])
def load_layout(name: str):
    """Load a layout by reading the YAML file and converting to layout on-the-fly."""
    from mcp_oasis import _yaml_to_layout_data

    safe_name = "".join(c for c in name if c.isalnum() or c in "-_ ").strip()
    yaml_dir = os.path.join(_PROJECT_ROOT, "data", "user_files", "default", "oasis", "yaml")
    fpath = os.path.join(yaml_dir, f"{safe_name}.yaml")
    if not os.path.isfile(fpath):
        fpath = os.path.join(yaml_dir, f"{safe_name}.yml")
    if not os.path.isfile(fpath):
        return jsonify({"error": "Layout not found"}), 404

    with open(fpath, "r", encoding="utf-8") as f:
        yaml_content = f.read()

    try:
        layout = _yaml_to_layout_data(yaml_content)
        layout["name"] = safe_name
        return jsonify(layout)
    except Exception as e:
        return jsonify({"error": f"YAML-to-layout conversion failed: {e}"}), 500


if __name__ == "__main__":
    print("=" * 60)
    print("  🎨 Visual Agent Orchestration System")
    print("  Open http://127.0.0.1:51210 in your browser")
    print("=" * 60)
    app.run(host="0.0.0.0", port=51210, debug=True)

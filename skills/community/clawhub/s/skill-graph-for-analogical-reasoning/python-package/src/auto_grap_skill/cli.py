from __future__ import annotations

import argparse
import json
from pathlib import Path

from .core import GraphSkillEngine


def render_graph_html(payload: dict) -> str:
    graph_json = (
        json.dumps(payload)
        .replace("&", "\\u0026")
        .replace("<", "\\u003c")
        .replace(">", "\\u003e")
    )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>grap-skill look</title>
  <style>
    body {{
      margin: 0;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      background: #0b1020;
      color: #e7ecf5;
      display: grid;
      grid-template-columns: 320px 1fr;
      min-height: 100vh;
    }}
    aside {{
      border-right: 1px solid #24304a;
      padding: 20px;
      background: #11182b;
      overflow-y: auto;
    }}
    main {{
      position: relative;
      overflow: hidden;
    }}
    h1 {{
      font-size: 20px;
      margin: 0 0 8px;
    }}
    .muted {{
      color: #92a1bd;
      font-size: 13px;
      line-height: 1.5;
    }}
    .stats {{
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 10px;
      margin: 18px 0;
    }}
    .card {{
      background: #17213a;
      border: 1px solid #263555;
      border-radius: 10px;
      padding: 12px;
    }}
    .card strong {{
      display: block;
      font-size: 18px;
      margin-top: 4px;
    }}
    input {{
      width: 100%;
      box-sizing: border-box;
      border-radius: 8px;
      border: 1px solid #33456d;
      background: #0d1526;
      color: #e7ecf5;
      padding: 10px 12px;
      margin: 10px 0 14px;
    }}
    .legend {{
      display: flex;
      flex-direction: column;
      gap: 10px;
      margin: 16px 0;
      font-size: 13px;
    }}
    .view-switch {{
      display: flex;
      gap: 8px;
      margin: 12px 0 6px;
    }}
    .view-switch button {{
      border-radius: 999px;
      border: 1px solid #314566;
      background: #0d1526;
      color: #dce4f2;
      padding: 8px 12px;
      cursor: pointer;
      font-size: 12px;
    }}
    .view-switch button.active {{
      background: #1d3259;
      border-color: #5ca7ff;
    }}
    .legend-title {{
      color: #d8e1f0;
      font-weight: 600;
    }}
    .weight-bar {{
      width: 100%;
      height: 14px;
      border-radius: 999px;
      background: linear-gradient(90deg, #4d9dff 0%, #ff5f6d 100%);
      border: 1px solid #314566;
      box-sizing: border-box;
    }}
    .weight-scale {{
      display: flex;
      justify-content: space-between;
      color: #b8c4da;
      font-size: 12px;
    }}
    #details {{
      margin-top: 18px;
      font-size: 13px;
      line-height: 1.5;
      color: #cbd4e5;
    }}
    svg {{
      width: 100%;
      height: 100vh;
      display: block;
      background:
        radial-gradient(circle at top left, rgba(77, 114, 201, 0.15), transparent 30%),
        radial-gradient(circle at bottom right, rgba(54, 179, 126, 0.12), transparent 24%),
        #0b1020;
    }}
    .edge {{
      stroke-opacity: 0.45;
      pointer-events: none;
    }}
    .edge-hit {{
      stroke: transparent;
      stroke-width: 14;
      cursor: pointer;
    }}
    .edge-active {{
      stroke-opacity: 0.95;
    }}
    .node {{
      cursor: pointer;
      transition: opacity 120ms ease;
    }}
    .label {{
      font-size: 12px;
      fill: #dce4f2;
      pointer-events: none;
    }}
  </style>
</head>
<body>
  <aside>
    <h1>grap-skill look</h1>
    <div class="muted">Visualize the current skill graph. Click a node to inspect its description and neighbors.</div>
    <div class="stats">
      <div class="card">Nodes<strong id="nodeCount"></strong></div>
      <div class="card">Edges<strong id="edgeCount"></strong></div>
    </div>
    <input id="search" placeholder="Filter nodes by name..." />
    <div class="view-switch">
      <button id="viewSimilarity" class="active" type="button">Similarity</button>
      <button id="viewComplementarity" type="button">Complementarity</button>
    </div>
    <div class="legend">
      <div class="legend-title" id="legendTitle">Similarity Weight</div>
      <div class="weight-bar"></div>
      <div class="weight-scale">
        <span id="legendMin">weight 0</span>
        <span id="legendMax">weight 1</span>
      </div>
      <div class="muted" id="legendDescription">Blue means lower similarity. Red means higher similarity.</div>
    </div>
    <div id="details" class="card">Click a node or edge to see details.</div>
  </aside>
  <main>
    <svg id="canvas" viewBox="0 0 1400 1000" preserveAspectRatio="xMidYMid meet"></svg>
  </main>
  <script id="payload-data" type="application/json">{graph_json}</script>
  <script>
    const payload = JSON.parse(document.getElementById("payload-data").textContent);
    const nodes = payload.nodes.map((node) => ({{ ...node }}));
    const edges = payload.edges.map((edge) => ({{ ...edge }}));
    const svg = document.getElementById("canvas");
    const details = document.getElementById("details");
    const search = document.getElementById("search");
    const viewSimilarityButton = document.getElementById("viewSimilarity");
    const viewComplementarityButton = document.getElementById("viewComplementarity");
    const legendTitle = document.getElementById("legendTitle");
    const legendDescription = document.getElementById("legendDescription");
    let activeEdgeLine = null;
    let activeEdgeData = null;
    let activeView = "similarity";
    document.getElementById("nodeCount").textContent = String(nodes.length);
    document.getElementById("edgeCount").textContent = String(edges.length);

    const width = 1400;
    const height = 1000;
    const cx = width / 2;
    const cy = height / 2;
    const radius = 360;
    const degree = Object.fromEntries(nodes.map((node) => [node.id, 0]));
    for (const edge of edges) {{
      degree[edge.source] += 1;
      degree[edge.target] += 1;
    }}

    nodes.sort((a, b) => a.name.localeCompare(b.name));
    nodes.forEach((node, index) => {{
      const angle = (Math.PI * 2 * index) / Math.max(nodes.length, 1) - Math.PI / 2;
      node.x = cx + radius * Math.cos(angle);
      node.y = cy + radius * Math.sin(angle);
      node.degree = degree[node.id];
      node.size = 12 + node.degree * 4;
    }});
    const nodeMap = Object.fromEntries(nodes.map((node) => [node.id, node]));

    function clearSvg() {{
      while (svg.firstChild) svg.removeChild(svg.firstChild);
    }}

    function lerp(start, end, ratio) {{
      return start + (end - start) * ratio;
    }}

    function currentWeight(edge) {{
      const viewWeights = edge.view_weights || {{}};
      if (typeof viewWeights[activeView] === "number") return viewWeights[activeView];
      if (activeView === "similarity") return edge.relation_scores?.similar || edge.weight || 0;
      if (activeView === "complementarity") return viewWeights.complementarity || 0;
      return edge.weight || 0;
    }}

    function weightExtents() {{
      const weights = edges.map((edge) => currentWeight(edge));
      return {{
        min: weights.length ? Math.min(...weights) : 0,
        max: weights.length ? Math.max(...weights) : 1,
      }};
    }}

    function updateLegend() {{
      if (activeView === "similarity") {{
        legendTitle.textContent = "Similarity Weight";
        legendDescription.textContent = "Blue means lower similarity. Red means higher similarity.";
      }} else {{
        legendTitle.textContent = "Complementarity Proxy";
        legendDescription.textContent = "Blue means lower complementarity proxy. Red means higher complementarity proxy.";
      }}
    }}

    function weightRatio(weight) {{
      const extents = weightExtents();
      if (extents.max === extents.min) return 1;
      return Math.max(0, Math.min(1, (weight - extents.min) / (extents.max - extents.min)));
    }}

    function weightColor(weight) {{
      const ratio = weightRatio(weight);
      const blue = {{ r: 77, g: 157, b: 255 }};
      const red = {{ r: 255, g: 95, b: 109 }};
      const r = Math.round(lerp(blue.r, red.r, ratio));
      const g = Math.round(lerp(blue.g, red.g, ratio));
      const b = Math.round(lerp(blue.b, red.b, ratio));
      return `rgb(${{r}}, ${{g}}, ${{b}})`;
    }}

    function sharedItems(left = [], right = [], limit = 6) {{
      const rightSet = new Set(right);
      return left.filter((item) => rightSet.has(item)).slice(0, limit);
    }}

    function uniqueItems(left = [], right = [], limit = 6) {{
      const rightSet = new Set(right);
      return left.filter((item) => !rightSet.has(item)).slice(0, limit);
    }}

    function parseDiagnostics(edge) {{
      const metrics = {{}};
      for (const item of edge.evidence || []) {{
        const [name, rawValue] = String(item).split("=");
        const value = Number(rawValue);
        if (name && Number.isFinite(value)) {{
          metrics[name] = value;
        }}
      }}
      return metrics;
    }}

    function formatScore(value) {{
      return Number(value || 0).toFixed(4);
    }}

    function escapeHtml(value) {{
      return String(value ?? "")
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#39;");
    }}

    function evidenceItem(label, value, priority) {{
      return {{ label, value, priority }};
    }}

    function topEvidenceForView(edge, source, target) {{
      const metrics = parseDiagnostics(edge);
      const similarityWeight = edge.view_weights?.similarity ?? edge.relation_scores?.similar ?? edge.weight ?? 0;
      const complementarityWeight = edge.view_weights?.complementarity ?? metrics.complementarity_proxy ?? 0;
      const semanticScore = metrics.semantic ?? 0;
      const keywordScore = metrics.keyword ?? 0;
      const toolScore = edge.relation_scores?.tool_affinity ?? metrics.tool ?? 0;
      const constraintScore = edge.relation_scores?.constraint_affinity ?? metrics.constraint ?? 0;
      const substituteScore = edge.relation_scores?.substitute ?? 0;
      const nonRedundancy = Math.max(0, 1 - similarityWeight);

      const sharedKeywords = sharedItems(source.keywords || [], target.keywords || []);
      const sharedTools = sharedItems(source.tool_mentions || [], target.tool_mentions || []);
      const sourceToolSurface = [...new Set([...(source.tool_mentions || []), ...(source.requires_bins || [])])];
      const targetToolSurface = [...new Set([...(target.tool_mentions || []), ...(target.requires_bins || [])])];
      const sourceConstraintSurface = [...new Set([...(source.requires_env || []), ...(source.requires_bins || []), ...(source.os_restrictions || [])])];
      const targetConstraintSurface = [...new Set([...(target.requires_env || []), ...(target.requires_bins || []), ...(target.os_restrictions || [])])];
      const sharedConstraints = sharedItems(sourceConstraintSurface, targetConstraintSurface, 6);
      const sourceOnlyTools = uniqueItems(sourceToolSurface, targetToolSurface, 4);
      const targetOnlyTools = uniqueItems(targetToolSurface, sourceToolSurface, 4);
      const evidence = [];

      if (activeView === "similarity") {{
        evidence.push(evidenceItem("Similarity score", formatScore(similarityWeight), similarityWeight));
        evidence.push(evidenceItem("Semantic description overlap", formatScore(semanticScore), semanticScore));
        evidence.push(evidenceItem("Keyword overlap", formatScore(keywordScore), keywordScore));

        if (sharedKeywords.length) {{
          evidence.push(
            evidenceItem(
              "Shared keywords",
              sharedKeywords.join(", "),
              Math.max(keywordScore, sharedKeywords.length / 10)
            )
          );
        }} else {{
          evidence.push(
            evidenceItem(
              "Keyword match pattern",
              "No strong explicit shared keywords; similarity is relying more on description semantics",
              semanticScore * 0.8
            )
          );
        }}

        if (sharedTools.length) {{
          evidence.push(
            evidenceItem(
              "Shared tool/code references",
              sharedTools.join(", "),
              Math.max(toolScore, sharedTools.length / 10)
            )
          );
        }}
        return evidence.sort((a, b) => b.priority - a.priority).slice(0, 5);
      }}

      evidence.push(evidenceItem("Complementarity proxy", formatScore(complementarityWeight), complementarityWeight));
      evidence.push(evidenceItem("Tool/code affinity", formatScore(toolScore), toolScore));
      evidence.push(evidenceItem("Runtime-constraint affinity", formatScore(constraintScore), constraintScore));
      evidence.push(evidenceItem("Non-redundancy factor (1 - similarity)", formatScore(nonRedundancy), nonRedundancy));
      evidence.push(evidenceItem("Similarity score", formatScore(similarityWeight), similarityWeight * 0.5));
      evidence.push(evidenceItem("Substitute score", formatScore(substituteScore), substituteScore * 0.4));

      if (sharedTools.length) {{
        evidence.push(
          evidenceItem(
            "Shared tool/code surface",
            sharedTools.join(", "),
            Math.max(toolScore, sharedTools.length / 10)
          )
        );
      }}
      if (sharedConstraints.length) {{
        evidence.push(
          evidenceItem(
            "Shared runtime constraints",
            sharedConstraints.join(", "),
            Math.max(constraintScore, sharedConstraints.length / 10)
          )
        );
      }}
      if (sourceOnlyTools.length) {{
        evidence.push(
          evidenceItem(
            `Only on ${{source.name}}`,
            sourceOnlyTools.join(", "),
            Math.max(nonRedundancy, sourceOnlyTools.length / 10)
          )
        );
      }}
      if (targetOnlyTools.length) {{
        evidence.push(
          evidenceItem(
            `Only on ${{target.name}}`,
            targetOnlyTools.join(", "),
            Math.max(nonRedundancy, targetOnlyTools.length / 10)
          )
        );
      }}
      return evidence.sort((a, b) => b.priority - a.priority).slice(0, 6);
    }}

    function relationEvidence(edge, source, target) {{
      return topEvidenceForView(edge, source, target).map((item) => `${{item.label}}: ${{item.value}}`);
    }}

    function draw(filter = "") {{
      clearSvg();
      activeEdgeLine = null;
      const lowered = filter.trim().toLowerCase();
      const visibleNodes = new Set(
        nodes
          .filter((node) => !lowered || node.name.toLowerCase().includes(lowered) || node.description.toLowerCase().includes(lowered))
          .map((node) => node.id)
      );
      const visibleEdges = edges.filter((edge) => visibleNodes.has(edge.source) && visibleNodes.has(edge.target));

      for (const edge of visibleEdges) {{
        const source = nodeMap[edge.source];
        const target = nodeMap[edge.target];
        const edgeWeight = currentWeight(edge);
        const line = document.createElementNS("http://www.w3.org/2000/svg", "line");
        line.setAttribute("x1", source.x);
        line.setAttribute("y1", source.y);
        line.setAttribute("x2", target.x);
        line.setAttribute("y2", target.y);
        line.setAttribute("stroke", weightColor(edgeWeight));
        line.setAttribute("stroke-width", Math.max(1.2, edgeWeight * 8));
        line.setAttribute("class", "edge");
        svg.appendChild(line);

        const hit = document.createElementNS("http://www.w3.org/2000/svg", "line");
        hit.setAttribute("x1", source.x);
        hit.setAttribute("y1", source.y);
        hit.setAttribute("x2", target.x);
        hit.setAttribute("y2", target.y);
        hit.setAttribute("class", "edge-hit");
        hit.addEventListener("click", () => showEdge(edge, line));
        svg.appendChild(hit);
      }}

      for (const node of nodes) {{
        if (!visibleNodes.has(node.id)) continue;
        const group = document.createElementNS("http://www.w3.org/2000/svg", "g");
        group.setAttribute("class", "node");
        group.dataset.nodeId = node.id;

        const circle = document.createElementNS("http://www.w3.org/2000/svg", "circle");
        circle.setAttribute("cx", node.x);
        circle.setAttribute("cy", node.y);
        circle.setAttribute("r", node.size);
        circle.setAttribute("fill", "#193057");
        circle.setAttribute("stroke", "#8fc3ff");
        circle.setAttribute("stroke-width", "2");

        const label = document.createElementNS("http://www.w3.org/2000/svg", "text");
        label.setAttribute("x", node.x);
        label.setAttribute("y", node.y + node.size + 16);
        label.setAttribute("text-anchor", "middle");
        label.setAttribute("class", "label");
        label.textContent = node.name;

        group.appendChild(circle);
        group.appendChild(label);
        group.addEventListener("click", () => showNode(node.id));
        svg.appendChild(group);
      }}
    }}

    function showNode(nodeId) {{
      if (activeEdgeLine) {{
        activeEdgeLine.classList.remove("edge-active");
        activeEdgeLine = null;
      }}
      const node = nodeMap[nodeId];
      const neighbors = edges
        .filter((edge) => edge.source === nodeId || edge.target === nodeId)
        .map((edge) => {{
          const otherId = edge.source === nodeId ? edge.target : edge.source;
          return {{
            id: otherId,
            relation: edge.dominant_relation,
            weight: edge.weight
          }};
        }})
        .sort((a, b) => b.weight - a.weight);

      details.innerHTML = `
        <strong style="font-size:16px">${{escapeHtml(node.name)}}</strong>
        <div style="margin-top:8px;color:#9fb1d1">${{escapeHtml(node.id)}}</div>
        <div style="margin-top:10px">${{escapeHtml(node.description)}}</div>
        <div style="margin-top:12px"><strong>Neighbors</strong></div>
        <ul style="padding-left:18px; margin-top:8px">
          ${{
            neighbors.length
              ? neighbors
                  .map(
                    (item) =>
                      `<li>${{escapeHtml(item.id)}} · ${{escapeHtml(item.relation)}} · weight=${{escapeHtml(item.weight)}}</li>`
                  )
                  .join("")
              : "<li>No neighbors</li>"
          }}
        </ul>
      `;
    }}

    function showEdge(edge, line) {{
      if (activeEdgeLine) {{
        activeEdgeLine.classList.remove("edge-active");
      }}
      activeEdgeLine = line || null;
      if (activeEdgeLine) {{
        activeEdgeLine.classList.add("edge-active");
      }}
      const source = nodeMap[edge.source];
      const target = nodeMap[edge.target];
      const naturalEvidence = relationEvidence(edge, source, target);
      const scores = Object.entries(edge.relation_scores || {{}})
        .sort((a, b) => b[1] - a[1])
        .map(([name, value]) => `<li>${{escapeHtml(name)}} = ${{escapeHtml(value)}}</li>`)
        .join("");
      const evidence = naturalEvidence
        .map((item) => `<li>${{escapeHtml(item)}}</li>`)
        .join("");
      const diagnostics = (edge.evidence || [])
        .map((item) => `<li>${{escapeHtml(item)}}</li>`)
        .join("");
      const similarityWeight = edge.view_weights?.similarity ?? edge.relation_scores?.similar ?? edge.weight;
      const complementarityWeight = edge.view_weights?.complementarity ?? 0;
      const activeWeight = currentWeight(edge);

      details.innerHTML = `
        <strong style="font-size:16px">${{escapeHtml(source.name)}} ↔ ${{escapeHtml(target.name)}}</strong>
        <div style="margin-top:8px;color:#9fb1d1">${{escapeHtml(edge.source)}} ↔ ${{escapeHtml(edge.target)}}</div>
        <div style="margin-top:10px"><strong>Top signals in this view</strong></div>
        <div style="margin-top:6px">Dominant relation: <code>${{escapeHtml(edge.dominant_relation)}}</code></div>
        <div style="margin-top:6px">Current view: <code>${{escapeHtml(activeView)}}</code> · active weight: <code>${{escapeHtml(activeWeight.toFixed(4))}}</code></div>
        <div style="margin-top:6px">Similarity weight: <code>${{escapeHtml(Number(similarityWeight).toFixed(4))}}</code></div>
        <div style="margin-top:6px">Complementarity proxy: <code>${{escapeHtml(Number(complementarityWeight).toFixed(4))}}</code></div>
        <div style="margin-top:12px"><strong>Key evidence for this view</strong></div>
        <ul style="padding-left:18px; margin-top:8px">
          ${{evidence || "<li>No evidence recorded</li>"}}
        </ul>
        <div style="margin-top:12px"><strong>Relation scores</strong></div>
        <ul style="padding-left:18px; margin-top:8px">
          ${{scores || "<li>No relation scores</li>"}}
        </ul>
        <div style="margin-top:12px"><strong>Algorithm diagnostics</strong></div>
        <ul style="padding-left:18px; margin-top:8px">
          ${{diagnostics || "<li>No diagnostics recorded</li>"}}
        </ul>
      `;
      activeEdgeData = edge;
    }}

    function switchView(nextView) {{
      activeView = nextView;
      viewSimilarityButton.classList.toggle("active", nextView === "similarity");
      viewComplementarityButton.classList.toggle("active", nextView === "complementarity");
      updateLegend();
      draw(search.value);
      if (activeEdgeData) {{
        const matchingEdge = edges.find(
          (item) =>
            item.source === activeEdgeData.source &&
            item.target === activeEdgeData.target &&
            item.dominant_relation === activeEdgeData.dominant_relation
        );
        if (matchingEdge) {{
          showEdge(matchingEdge, null);
        }}
      }}
    }}

    search.addEventListener("input", (event) => draw(event.target.value));
    viewSimilarityButton.addEventListener("click", () => switchView("similarity"));
    viewComplementarityButton.addEventListener("click", () => switchView("complementarity"));
    updateLegend();
    draw();
  </script>
</body>
</html>
"""


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="grap-skill", description="Build and query a graph over SKILL.md folders.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    build_parser = subparsers.add_parser("build", help="Scan skill folders and build graph.json.")
    build_parser.add_argument("--source", action="append", required=True, help="A directory to scan recursively for SKILL.md.")
    build_parser.add_argument("--output", default=".grap-skill", help="Directory where graph.json will be written.")

    query_parser = subparsers.add_parser("query", help="Query an existing graph for primary and related skills.")
    query_parser.add_argument("task", help="User task text.")
    query_parser.add_argument("--graph", default=".grap-skill/graph.json", help="Path to graph.json.")

    look_parser = subparsers.add_parser("look", help="Render an HTML visualization for the whole skill graph.")
    look_parser.add_argument("--graph", default=".grap-skill/graph.json", help="Path to graph.json.")
    look_parser.add_argument("--output", default=".grap-skill/graph-look.html", help="Path to the generated HTML file.")

    inspect_parser = subparsers.add_parser("inspect", help="Inspect a skill node and its adjacent edges.")
    inspect_parser.add_argument("skill_id", help="Normalized skill id.")
    inspect_parser.add_argument("--graph", default=".grap-skill/graph.json", help="Path to graph.json.")

    stats_parser = subparsers.add_parser("stats", help="Show graph stats.")
    stats_parser.add_argument("--graph", default=".grap-skill/graph.json", help="Path to graph.json.")

    return parser


def cmd_build(args: argparse.Namespace) -> int:
    sources = [Path(item).expanduser().resolve() for item in args.source]
    engine = GraphSkillEngine.build_from_sources(sources)
    graph_path = engine.save(Path(args.output).expanduser().resolve())
    print(json.dumps({"graph": str(graph_path), "nodes": len(engine.nodes), "edges": len(engine.edges)}, indent=2))
    return 0


def cmd_query(args: argparse.Namespace) -> int:
    engine = GraphSkillEngine.load(Path(args.graph).expanduser().resolve())
    result = engine.query(args.task)
    print(json.dumps(result, indent=2))
    return 0


def cmd_look(args: argparse.Namespace) -> int:
    graph_path = Path(args.graph).expanduser().resolve()
    payload = json.loads(graph_path.read_text(encoding="utf-8"))
    output_path = Path(args.output).expanduser().resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(render_graph_html(payload), encoding="utf-8")
    print(json.dumps({"graph": str(graph_path), "html": str(output_path)}, indent=2))
    return 0


def cmd_inspect(args: argparse.Namespace) -> int:
    engine = GraphSkillEngine.load(Path(args.graph).expanduser().resolve())
    node = engine.nodes_by_id.get(args.skill_id)
    if not node:
        raise SystemExit(f"Unknown skill id: {args.skill_id}")
    neighbors = []
    for edge in engine.adjacency.get(args.skill_id, []):
        neighbor_id = edge.target if edge.source == args.skill_id else edge.source
        neighbors.append(
            {
                "neighbor": neighbor_id,
                "dominant_relation": edge.dominant_relation,
                "weight": edge.weight,
                "relation_scores": edge.relation_scores,
                "evidence": edge.evidence,
            }
        )
    payload = {
        "id": node.id,
        "name": node.name,
        "description": node.description,
        "keywords": node.keywords,
        "triggers": node.triggers,
        "tools": node.tool_mentions,
        "requires_env": node.requires_env,
        "requires_bins": node.requires_bins,
        "neighbors": sorted(neighbors, key=lambda item: item["weight"], reverse=True),
    }
    print(json.dumps(payload, indent=2))
    return 0


def cmd_stats(args: argparse.Namespace) -> int:
    graph_path = Path(args.graph).expanduser().resolve()
    payload = json.loads(graph_path.read_text(encoding="utf-8"))
    print(json.dumps(payload.get("stats", {}), indent=2))
    return 0


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    if args.command == "build":
        return cmd_build(args)
    if args.command == "query":
        return cmd_query(args)
    if args.command == "look":
        return cmd_look(args)
    if args.command == "inspect":
        return cmd_inspect(args)
    if args.command == "stats":
        return cmd_stats(args)
    parser.error(f"Unknown command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())

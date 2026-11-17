#!/usr/bin/env python3
import argparse
import ast
import datetime as dt
import hashlib
import json
import math
import os
from pathlib import Path
from xml.sax.saxutils import escape as xml_escape

GRID_X = 120
GRID_Y = 80
PADDING = 40
FONT_FAMILY = "Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif"

NODE_STYLES = {
    "service": {"fill": "#ffffff", "stroke": "#1f2937", "text": "#111827"},
    "llm": {"fill": "#ffffff", "stroke": "#0f172a", "text": "#0f172a"},
    "agent": {"fill": "#f8fafc", "stroke": "#0f172a", "text": "#0f172a"},
    "memory": {"fill": "#f8fafc", "stroke": "#14532d", "text": "#14532d"},
}

SHOWCASE_NODE_STYLES = {
    "service": {"fill": "#0f172a", "stroke": "#38bdf8", "text": "#f8fafc", "muted": "#bfdbfe"},
    "llm": {"fill": "#1e1b4b", "stroke": "#c4b5fd", "text": "#f5f3ff", "muted": "#ddd6fe"},
    "agent": {"fill": "#111827", "stroke": "#fbbf24", "text": "#fffbeb", "muted": "#fde68a"},
    "memory": {"fill": "#052e2b", "stroke": "#5eead4", "text": "#ecfeff", "muted": "#99f6e4"},
}

EDGE_STYLES = {
    "primary-data": {"stroke": "#2563eb", "dash": None, "label_fill": "#dbeafe", "label_text": "#1d4ed8"},
    "memory-write": {"stroke": "#16a34a", "dash": "10 8", "label_fill": "#dcfce7", "label_text": "#166534"},
    "control": {"stroke": "#475569", "dash": "6 6", "label_fill": "#e2e8f0", "label_text": "#334155"},
}

SHOWCASE_EDGE_STYLES = {
    "primary-data": {"stroke": "#38bdf8", "dash": None, "label_fill": "#082f49", "label_text": "#e0f2fe", "label_stroke": "#164e63"},
    "memory-write": {"stroke": "#5eead4", "dash": "10 8", "label_fill": "#042f2e", "label_text": "#ccfbf1", "label_stroke": "#0f766e"},
    "control": {"stroke": "#fbbf24", "dash": "6 6", "label_fill": "#451a03", "label_text": "#fef3c7", "label_stroke": "#92400e"},
}

ALLOWED_NODE_KINDS = set(NODE_STYLES)
ALLOWED_EDGE_KINDS = set(EDGE_STYLES)
VERSION = "1.8.3"
ALLOWED_MODES = {"architecture", "workflow", "sequence", "dataflow", "lifecycle", "pr-delta"}
ALLOWED_THEMES = {"classic", "showcase"}

MODE_ACCENTS = {
    "architecture": {"label": "system map", "tone": "#38bdf8", "zones": ["Actors", "Runtime", "Proof"]},
    "workflow": {"label": "workflow", "tone": "#fbbf24", "zones": ["Intent", "Build", "Prove"]},
    "sequence": {"label": "sequence", "tone": "#c4b5fd", "zones": ["Participants", "Messages", "Result"]},
    "dataflow": {"label": "data flow", "tone": "#5eead4", "zones": ["Sources", "Transforms", "Stores"]},
    "lifecycle": {"label": "lifecycle", "tone": "#fb7185", "zones": ["Open", "Active", "Closed"]},
    "pr-delta": {"label": "PR delta", "tone": "#f97316", "zones": ["Base", "Head", "Review"]},
}


def escape(value):
    """Encode text and both quote characters for HTML/SVG quoted attributes."""
    return xml_escape(str(value), {'"': "&quot;", "'": "&#x27;"})


def script_json(value):
    """JSON data that cannot terminate an HTML script element."""
    return (json.dumps(value).replace("&", "\\u0026")
            .replace("<", "\\u003c").replace(">", "\\u003e")
            .replace("\u2028", "\\u2028").replace("\u2029", "\\u2029"))


def snap(value, grid):
    return round(value / grid) * grid


def load(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def spec_mode(data):
    return data.get("mode", "architecture") if isinstance(data, dict) else "architecture"


def spec_theme(data):
    return data.get("theme", "classic") if isinstance(data, dict) else "classic"


def theme_pack(data):
    if spec_theme(data) == "showcase":
        return {
            "name": "showcase",
            "background": "#020617",
            "grid": "#1e293b",
            "halo": True,
            "node": SHOWCASE_NODE_STYLES,
            "edge": SHOWCASE_EDGE_STYLES,
            "label_border": "#164e63",
            "badge_fill": "#042f2e",
            "badge_stroke": "#2dd4bf",
            "badge_text": "#ccfbf1",
        }
    return {
        "name": "classic",
        "background": "#f8fafc",
        "grid": "#e5e7eb",
        "halo": False,
        "node": NODE_STYLES,
        "edge": EDGE_STYLES,
        "label_border": "#ffffff",
        "badge_fill": "#ecfeff",
        "badge_stroke": "#0891b2",
        "badge_text": "#0e7490",
    }


def sha256_text(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def file_sha256(path):
    digest = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def text_width(text, font_size):
    return max(36, int(len(text) * font_size * 0.58))


def node_box(node):
    title = node["label"]
    subtitle = node.get("subtitle", "")
    width = max(180, text_width(title, 18) + 48, text_width(subtitle, 13) + 48 if subtitle else 0)
    height = 76 if subtitle else 56
    return width, height


def position_nodes(nodes):
    placed = {}
    for node in nodes:
        x = snap(node.get("x", 0), GRID_X)
        y = snap(node.get("y", 0), GRID_Y)
        width, height = node_box(node)
        placed[node["id"]] = {**node, "x": x, "y": y, "width": width, "height": height}
    return placed


def evidence_items(subject):
    evidence = subject.get("evidence", [])
    if evidence is None:
        return []
    if isinstance(evidence, dict):
        return [evidence]
    if isinstance(evidence, list):
        return evidence
    return []


def validate_evidence(subject, path, errors, warnings):
    evidence = subject.get("evidence")
    if evidence is None:
        return
    items = evidence_items(subject)
    if not isinstance(evidence, (dict, list)):
        errors.append({"code": "evidence.type", "subject": path, "message": "evidence must be an object or list of objects."})
        return
    for index, item in enumerate(items):
        item_path = f"{path}.evidence[{index}]"
        if not isinstance(item, dict):
            errors.append({"code": "evidence.item.type", "subject": item_path, "message": "Evidence item must be an object."})
            continue
        source = item.get("source")
        if not isinstance(source, str) or not source.strip():
            errors.append({"code": "evidence.source.required", "subject": item_path, "message": "Evidence requires a source path or URL string."})
        if "line" in item and not isinstance(item["line"], int):
            errors.append({"code": "evidence.line.type", "subject": item_path, "message": "Evidence line must be an integer."})
        if "lines" in item:
            lines = item["lines"]
            if not (isinstance(lines, list) and len(lines) == 2 and all(isinstance(value, int) for value in lines)):
                errors.append({"code": "evidence.lines.type", "subject": item_path, "message": "Evidence lines must be [start, end] integers."})
        if "commit" in item and not isinstance(item["commit"], str):
            errors.append({"code": "evidence.commit.type", "subject": item_path, "message": "Evidence commit must be a string."})
        confidence = item.get("confidence")
        if confidence is not None and confidence not in ("high", "medium", "low"):
            warnings.append({"code": "evidence.confidence.unknown", "subject": item_path, "message": "Use confidence high, medium, or low."})


def box_edges(node, margin=0):
    half_w = node["width"] / 2 + margin
    half_h = node["height"] / 2 + margin
    return {
        "left": node["x"] - half_w,
        "right": node["x"] + half_w,
        "top": node["y"] - half_h,
        "bottom": node["y"] + half_h,
    }


def segment_crosses_box(a, b, box):
    ax, ay = a
    bx, by = b
    if ax == bx:
        x = ax
        if not (box["left"] < x < box["right"]):
            return False
        low = min(ay, by)
        high = max(ay, by)
        return max(low, box["top"]) < min(high, box["bottom"])
    if ay == by:
        y = ay
        if not (box["top"] < y < box["bottom"]):
            return False
        low = min(ax, bx)
        high = max(ax, bx)
        return max(low, box["left"]) < min(high, box["right"])
    return False



def boxes_overlap(a, b, margin=0):
    a_box = box_edges(a, margin=margin)
    b_box = box_edges(b, margin=margin)
    return not (
        a_box["right"] <= b_box["left"]
        or a_box["left"] >= b_box["right"]
        or a_box["bottom"] <= b_box["top"]
        or a_box["top"] >= b_box["bottom"]
    )


def orthogonal_intersection(a, b, c, d):
    ax, ay = a
    bx, by = b
    cx, cy = c
    dx, dy = d
    if a in (c, d) or b in (c, d):
        return False
    if ay == by and cx == dx:
        return min(ax, bx) < cx < max(ax, bx) and min(cy, dy) < ay < max(cy, dy)
    if ax == bx and cy == dy:
        return min(cx, dx) < ax < max(cx, dx) and min(ay, by) < cy < max(ay, by)
    return False


def quality_profile(data, placed, edges, warnings):
    score = 100
    checks = []
    node_values = list(placed.values())

    for index, node in enumerate(node_values):
        for other in node_values[index + 1:]:
            if boxes_overlap(node, other, margin=10):
                score -= 24
                checks.append({"code": "quality.node.overlap", "level": "fail", "subjects": [node["id"], other["id"]]})
                warnings.append({
                    "code": "quality.node.overlap",
                    "subject": node["id"],
                    "message": f"Node visually overlaps {other['id']}. Move one node at least one grid step away.",
                    "supportedFixes": [{"field": "x/y", "message": "Move the node to an unoccupied grid position."}],
                })
            distance = abs(node["x"] - other["x"]) + abs(node["y"] - other["y"])
            if distance < 180:
                score -= 8
                checks.append({"code": "quality.node.spacing", "level": "warn", "subjects": [node["id"], other["id"]]})

    routes = []
    for index, edge in enumerate(edges):
        if edge.get("from") not in placed or edge.get("to") not in placed:
            continue
        points = orthogonal_points(placed[edge["from"]], placed[edge["to"]], edge)
        routes.append((index, edge, points))
        if len(points) > 6:
            score -= 4
            checks.append({"code": "quality.route.complex", "level": "warn", "subject": f"edges[{index}]"})
        if edge.get("label") and len(edge["label"]) > 22:
            score -= 3
            checks.append({"code": "quality.label.long", "level": "warn", "subject": f"edges[{index}]"})

    crossing_count = 0
    for route_index, (_, route_edge, route_points) in enumerate(routes):
        for _, other_edge, other_points in routes[route_index + 1:]:
            if {route_edge.get("from"), route_edge.get("to")} & {other_edge.get("from"), other_edge.get("to")}:
                continue
            for a, b in zip(route_points, route_points[1:]):
                for c, d in zip(other_points, other_points[1:]):
                    if orthogonal_intersection(a, b, c, d):
                        crossing_count += 1
                        break

    if crossing_count:
        score -= min(30, crossing_count * 6)
        checks.append({"code": "quality.route.crossings", "level": "warn", "count": crossing_count})
        warnings.append({
            "code": "quality.route.crossings",
            "message": f"Detected {crossing_count} route crossing(s). Use via points or split the artifact.",
            "supportedFixes": [{"field": "via", "message": "Route crowded edges around the conflict using grid-snapped turn points."}],
        })

    node_count = len(node_values)
    edge_count = len(edges)
    if node_count > 9 or edge_count > 12:
        score -= 10
        checks.append({"code": "quality.density.high", "level": "warn", "nodes": node_count, "edges": edge_count})
        warnings.append({
            "code": "quality.density.high",
            "message": "Artifact is dense enough to risk becoming a wall of boxes. Split the story or feature one path.",
        })

    score = max(0, min(100, score))
    rating = "excellent" if score >= 90 else "good" if score >= 76 else "needs-work" if score >= 60 else "poor"
    return {"score": score, "rating": rating, "checks": checks, "routeCrossings": crossing_count}


QUALITY_ORDER = {"poor": 0, "needs-work": 1, "good": 2, "excellent": 3}


def quality_meets(validation, minimum):
    if not minimum:
        return True
    quality = validation.get("metrics", {}).get("quality", {})
    rating = quality.get("rating", "poor")
    return QUALITY_ORDER.get(rating, -1) >= QUALITY_ORDER.get(minimum, 999)


def first_existing(root, candidates):
    for candidate in candidates:
        if (root / candidate).exists():
            return candidate
    return candidates[0]


def find_line(root, rel_path, needle):
    path = root / rel_path
    if not path.exists():
        return 1
    for index, line in enumerate(path.read_text(encoding="utf-8", errors="ignore").splitlines(), start=1):
        if needle in line:
            return index
    return 1


def evidence(root, rel_path, needle=None, confidence="high", note=None):
    item = {"source": rel_path, "line": find_line(root, rel_path, needle) if needle else 1, "confidence": confidence}
    if note:
        item["note"] = note
    return item


def evidence_item(root, rel_path, needle=None, confidence="high", rule=None, source_type=None, note=None):
    item = evidence(root, rel_path, needle=needle, confidence=confidence, note=note)
    if rule:
        item["rule"] = rule
    if source_type:
        item["sourceType"] = source_type
    return item


def read_text(root, rel_path):
    path = root / rel_path
    try:
        return path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return ""


def parse_json_file(root, rel_path):
    try:
        return json.loads((root / rel_path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def python_symbols(root, rel_path):
    source = read_text(root, rel_path)
    if not source:
        return []
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return []
    symbols = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            if node.name.startswith("_") and node.name not in {"__main__"}:
                continue
            symbols.append({"name": node.name, "line": getattr(node, "lineno", 1), "kind": type(node).__name__.replace("Def", "").lower()})
    return sorted(symbols, key=lambda item: item["line"])


def package_scripts(root, rel_path):
    data = parse_json_file(root, rel_path)
    if not isinstance(data, dict):
        return []
    scripts = data.get("scripts")
    if not isinstance(scripts, dict):
        return []
    return [{"name": name, "command": command} for name, command in sorted(scripts.items()) if isinstance(command, str)]


def workflow_names(root, rel_path):
    text = read_text(root, rel_path)
    names = []
    for index, line in enumerate(text.splitlines(), start=1):
        stripped = line.strip()
        if stripped.startswith("name:"):
            workflow_name = stripped.split(":", 1)[1].strip().strip("\"'")
            names.append({"name": workflow_name, "line": index})
        elif stripped.startswith("- run:"):
            names.append({"name": stripped.split(":", 1)[1].strip()[:42], "line": index})
    return names[:6]


def docs_headings(root, rel_path):
    headings = []
    for index, line in enumerate(read_text(root, rel_path).splitlines(), start=1):
        if line.startswith("#"):
            heading = line.lstrip("#").strip()
            if heading:
                headings.append({"name": heading, "line": index})
    return headings[:8]


def classify_repo_file(path):
    if path.startswith("scripts/") and path.endswith(".py"):
        return "python"
    if path.endswith((".js", ".jsx", ".ts", ".tsx")):
        return "javascript"
    if path in {"package.json", "pnpm-workspace.yaml", "yarn.lock", "package-lock.json"}:
        return "package"
    if path.startswith(".github/workflows/"):
        return "workflow"
    if path.startswith("schemas/") and path.endswith(".json"):
        return "schema"
    if path.startswith("examples/") and path.endswith(".json") and not path.endswith(".receipt.json"):
        return "example"
    if path.endswith((".md", ".mdx", ".rst")) or path.startswith("docs/"):
        return "docs"
    if path in {"Makefile", "makefile"}:
        return "makefile"
    if path in {"index.html"} or (path.startswith("docs/") and path.endswith(".html")):
        return "site"
    return "other"


def repo_language_facts(root, files):
    facts = {"python": [], "javascript": [], "package": [], "workflow": [], "schema": [], "example": [], "docs": [], "makefile": [], "site": []}
    for rel in sorted(files):
        kind = classify_repo_file(rel)
        if kind in facts:
            facts[kind].append(rel)
    return facts


def extracted_node(node_id, label, subtitle, kind, group, root, rel_path, needle=None, confidence="high", rule="repo.file", source_type=None, role=None):
    return {
        "id": node_id,
        "label": label,
        "subtitle": subtitle,
        "kind": kind,
        "group": group,
        "role": role or group,
        "extraction": {"rule": rule, "confidence": confidence},
        "evidence": evidence_item(root, rel_path, needle=needle, confidence=confidence, rule=rule, source_type=source_type),
    }


def extracted_edge(source, target, kind, label, root, rel_path, needle=None, confidence="medium", rule="repo.inference", source_type=None, **extra):
    edge = {
        "from": source,
        "to": target,
        "kind": kind,
        "label": label,
        "extraction": {"rule": rule, "confidence": confidence},
        "evidence": evidence_item(root, rel_path, needle=needle, confidence=confidence, rule=rule, source_type=source_type),
    }
    edge.update(extra)
    return edge


def best_file(paths, fallback):
    return paths[0] if paths else fallback


DEFAULT_IGNORE_DIRS = {".git", "node_modules", ".next", "dist", "build", "coverage", ".francis-runs", ".turbo", ".cache", "tmp", "temp"}


def is_ignored_path(path):
    return any(part in DEFAULT_IGNORE_DIRS for part in Path(path).parts)


def safe_node_id(text):
    cleaned = []
    for char in str(text).lower():
        if char.isalnum():
            cleaned.append(char)
        elif cleaned and cleaned[-1] != "_":
            cleaned.append("_")
    value = "".join(cleaned).strip("_")
    return value or "node"


def workspace_package_dirs(root):
    package = parse_json_file(root, "package.json")
    patterns = []
    workspaces = package.get("workspaces") if isinstance(package, dict) else None
    if isinstance(workspaces, list):
        patterns = workspaces
    elif isinstance(workspaces, dict) and isinstance(workspaces.get("packages"), list):
        patterns = workspaces["packages"]
    if not patterns:
        patterns = ["apps/*", "packages/*"]
    dirs = []
    for pattern in patterns:
        for match in root.glob(pattern):
            if match.is_dir() and not is_ignored_path(match.relative_to(root)):
                dirs.append(str(match.relative_to(root)))
    return sorted(set(dirs))


def package_label(path):
    parts = Path(path).parts
    if not parts:
        return "Package"
    name = parts[-1]
    return name.replace("-", " ").replace("_", " ").title()


def package_kind(path):
    lower = path.lower()
    if "client" in lower or "web" in lower or "frontend" in lower:
        return "client-app"
    if "server" in lower or "api" in lower or "backend" in lower:
        return "server-app"
    if "editor" in lower or "extension" in lower or "ext" in lower:
        return "editor-extension"
    return "package"


def ts_files_under(files, package_dir):
    prefix = package_dir.rstrip("/") + "/"
    return [path for path in sorted(files) if path.startswith(prefix) and path.endswith((".ts", ".tsx", ".js", ".jsx"))]


def first_matching(paths, needles):
    for needle in needles:
        for path in paths:
            if needle in path:
                return path
    return paths[0] if paths else None


def ts_imports(root, rel_path):
    text = read_text(root, rel_path)
    imports = []
    for index, line in enumerate(text.splitlines(), start=1):
        stripped = line.strip()
        target = None
        if " from " in stripped and (stripped.startswith("import") or stripped.startswith("export")):
            quote = '"' if '"' in stripped.split(" from ", 1)[1] else "'"
            tail = stripped.split(" from ", 1)[1]
            if quote in tail:
                target = tail.split(quote, 2)[1]
        elif "require(" in stripped:
            tail = stripped.split("require(", 1)[1]
            quote = '"' if '"' in tail else "'"
            if quote in tail:
                target = tail.split(quote, 2)[1]
        if target:
            imports.append({"target": target, "line": index})
    return imports


def import_graph_summary(root, files, package_dir):
    package_files = ts_files_under(files, package_dir)
    edges = []
    local_imports = 0
    external_imports = 0
    for rel in package_files[:160]:
        for item in ts_imports(root, rel):
            if item["target"].startswith(".") or item["target"].startswith("@/"):
                local_imports += 1
            else:
                external_imports += 1
            if len(edges) < 12:
                edges.append({"source": rel, **item})
    return {"files": len(package_files), "localImports": local_imports, "externalImports": external_imports, "samples": edges}


def package_scripts_for_dir(root, package_dir):
    rel = str(Path(package_dir) / "package.json")
    scripts = package_scripts(root, rel)
    return rel, scripts


def filter_valid_edges(nodes, edges):
    ids = {node.get("id") for node in nodes}
    return [edge for edge in edges if edge.get("from") in ids and edge.get("to") in ids]


def add_ts_monorepo_nodes(root, files, facts, nodes, edges):
    package_dirs = workspace_package_dirs(root)
    package_node_ids = []
    root_package = "package.json" if "package.json" in files else first_existing(root, ["README.md"])
    for package_dir in package_dirs:
        ts_files = ts_files_under(files, package_dir)
        if not ts_files and str(Path(package_dir) / "package.json") not in files:
            continue
        kind = package_kind(package_dir)
        node_id = safe_node_id(f"pkg_{package_dir}")
        package_node_ids.append(node_id)
        package_json, scripts = package_scripts_for_dir(root, package_dir)
        evidence_path = package_json if package_json in files else best_file(ts_files, root_package)
        script_names = ", ".join(script["name"] for script in scripts[:3]) if scripts else f"{len(ts_files)} source files"
        label_prefix = {"client-app": "Client App", "server-app": "Server App", "editor-extension": "Editor Extension"}.get(kind, "Workspace Package")
        nodes.append(extracted_node(node_id, label_prefix, package_label(package_dir), "service", "runtime", root, evidence_path, confidence="high", rule=f"workspace.package.{kind}", source_type="package", role=kind))
        workspace_route = {"source_side": "right", "target_side": "left"}
        if kind == "server-app":
            workspace_route = {"source_side": "right", "target_side": "left", "via": [{"x": 600, "y": 160}, {"x": 600, "y": 880}]}
        elif kind == "editor-extension":
            workspace_route = {"source_side": "left", "target_side": "left", "via": [{"x": 240, "y": 160}, {"x": 240, "y": 1360}, {"x": 720, "y": 1360}]}
        edges.append(extracted_edge("package", node_id, "control", "workspace", root, root_package, confidence="high", rule="workspace.package-link", source_type="package", **workspace_route))
        graph = import_graph_summary(root, files, package_dir)
        nodes[-1]["extraction"]["imports"] = {"files": graph["files"], "local": graph["localImports"], "external": graph["externalImports"]}

        if kind == "server-app":
            module_file = first_matching(ts_files, ["app.module", ".module.ts", "main.ts"])
            controller_file = first_matching(ts_files, ["controller.ts", "handler.ts"])
            gateway_file = first_matching(ts_files, ["gateway.ts", "ws", "collaboration"])
            db_file = first_matching(ts_files, ["database", "migrate", "migration", "prisma"])
            if module_file:
                nodes.append(extracted_node("backend_modules", "Backend Modules", "modules/controllers/services", "agent", "runtime", root, module_file, confidence="high", rule="typescript.backend.modules", source_type="typescript", role="backend"))
                edges.append(extracted_edge(node_id, "backend_modules", "primary-data", "modules", root, module_file, confidence="high", rule="server.package-to-modules", source_type="typescript"))
            if gateway_file:
                nodes.append(extracted_node("realtime_gateways", "Realtime Gateways", "ws/collaboration", "service", "runtime", root, gateway_file, confidence="high", rule="typescript.backend.gateway", source_type="typescript", role="realtime"))
                edges.append(extracted_edge("backend_modules", "realtime_gateways", "primary-data", "events", root, gateway_file, confidence="high", rule="module-to-gateway", source_type="typescript"))
            if db_file:
                nodes.append(extracted_node("database_layer", "Database Layer", "database/migration", "memory", "contract", root, db_file, confidence="high", rule="typescript.backend.database", source_type="typescript", role="database"))
                source = "backend_modules" if any(node["id"] == "backend_modules" for node in nodes) else node_id
                edges.append(extracted_edge(source, "database_layer", "memory-write", "persist", root, db_file, confidence="high", rule="backend-to-database", source_type="typescript"))
        elif kind == "client-app":
            entry_file = first_matching(ts_files, ["main.tsx", "App.tsx", "app-route", "routes"])
            api_file = first_matching(ts_files, ["api-client", "config", "constants"])
            feature_file = first_matching(ts_files, ["features", "hooks", "state"])
            if entry_file:
                nodes.append(extracted_node("frontend_app", "Frontend App", "entry/routes/features", "service", "runtime", root, entry_file, confidence="high", rule="typescript.frontend.entry", source_type="typescript", role="frontend"))
                edges.append(extracted_edge(node_id, "frontend_app", "primary-data", "renders", root, entry_file, confidence="high", rule="client.package-to-entry", source_type="typescript"))
            if api_file:
                nodes.append(extracted_node("api_client", "API Client", "config/client boundary", "service", "contract", root, api_file, confidence="high", rule="typescript.frontend.api-client", source_type="typescript", role="boundary"))
                edges.append(extracted_edge("frontend_app", "api_client", "primary-data", "calls", root, api_file, confidence="high", rule="frontend-to-api-client", source_type="typescript"))
            if feature_file:
                nodes.append(extracted_node("client_features", "Client Features", "feature hooks/state", "service", "runtime", root, feature_file, confidence="medium", rule="typescript.frontend.features", source_type="typescript", role="feature"))
                edges.append(extracted_edge("frontend_app", "client_features", "control", "uses", root, feature_file, confidence="medium", rule="frontend-to-features", source_type="typescript"))
        elif kind == "editor-extension":
            entry_file = first_matching(ts_files, ["index.ts", "extension", "editor", "embed"])
            if entry_file:
                nodes.append(extracted_node("editor_extension", "Editor Extension", "editor integrations", "service", "runtime", root, entry_file, confidence="high", rule="typescript.editor-extension", source_type="typescript", role="editor"))
                edges.append(extracted_edge(node_id, "editor_extension", "primary-data", "extends", root, entry_file, confidence="high", rule="package-to-editor-extension", source_type="typescript"))

    if package_node_ids and any(node["id"] == "package" for node in nodes):
        package = next(node for node in nodes if node["id"] == "package")
        package["subtitle"] = f"{len(package_node_ids)} workspaces"
    return package_node_ids


def layout_spec(data, mode=None, theme=None):
    data = json.loads(json.dumps(data))
    mode = mode or spec_mode(data)
    if theme:
        data["theme"] = theme
    data["mode"] = mode
    nodes = data.get("nodes", [])

    if mode == "workflow":
        rows = {}
        for node in nodes:
            lane = node.get("lane") or node.get("phase") or node.get("group") or "flow"
            rows.setdefault(lane, []).append(node)
        for row_index, lane_nodes in enumerate(rows.values()):
            for col_index, node in enumerate(lane_nodes):
                node["x"] = 120 + col_index * 300
                node["y"] = 160 + row_index * 160
    elif mode == "sequence":
        for index, node in enumerate(nodes):
            node["x"] = 120 + index * 240
            node["y"] = 160
        order = {node.get("id"): index for index, node in enumerate(nodes)}
        for edge in data.get("edges", []):
            source_index = order.get(edge.get("from"), 0)
            target_index = order.get(edge.get("to"), source_index + 1)
            edge.setdefault("source_side", "bottom")
            edge.setdefault("target_side", "bottom")
            edge.setdefault("via", [
                {"x": 120 + source_index * 240, "y": 260 + abs(source_index - target_index) * 40},
                {"x": 120 + target_index * 240, "y": 260 + abs(source_index - target_index) * 40},
            ])
    elif mode == "lifecycle":
        for index, node in enumerate(nodes):
            node["x"] = 120 + index * 240
            node["y"] = 160 + (80 if index % 2 else 0)
    elif mode == "pr-delta":
        columns = {"base": 120, "head": 120, "changed": 480, "added": 480, "removed": 480, "risk": 840, "review": 840, "receipt": 1200}
        y_slots = {
            "base": [160],
            "head": [400],
            "changed": [160, 400, 640],
            "added": [160, 400, 640],
            "removed": [160, 400, 640],
            "risk": [400],
            "review": [400],
            "receipt": [400],
        }
        seen = {}
        for index, node in enumerate(nodes):
            key = node.get("group") or node.get("id", "")
            node["x"] = columns.get(key, 120 + min(index, 3) * 360)
            slot_index = seen.get(key, 0)
            slots = y_slots.get(key, [160, 400, 640])
            node["y"] = slots[min(slot_index, len(slots) - 1)]
            seen[key] = slot_index + 1
    else:
        role_slots = {
            "source": (120, 160),
            "contract": (120, 400),
            "package": (360, 160),
            "database": (360, 800),
            "boundary": (360, 400),
            "runtime": (840, 160),
            "client-app": (840, 160),
            "frontend": (840, 400),
            "feature": (840, 640),
            "server-app": (840, 880),
            "backend": (840, 1120),
            "realtime": (1200, 1120),
            "editor-extension": (840, 1360),
            "editor": (1200, 1360),
            "proof": (1200, 160),
            "release": (1200, 640),
        }
        if any(node.get("role") in role_slots for node in nodes):
            seen_roles = {}
            for index, node in enumerate(nodes):
                role = node.get("role") or node.get("group") or node.get("zone") or node.get("kind", "runtime")
                if role in role_slots:
                    base_x, base_y = role_slots[role]
                    offset = seen_roles.get(role, 0)
                    node["x"] = base_x
                    node["y"] = base_y + offset * 240
                    seen_roles[role] = offset + 1
                else:
                    group = node.get("group") or "runtime"
                    fallback = {"source": (120, 160), "contract": (480, 160), "runtime": (780, 160), "proof": (1200, 160)}.get(group, (780, 160))
                    node["x"] = fallback[0]
                    node["y"] = fallback[1] + seen_roles.get(group, 0) * 220
                    seen_roles[group] = seen_roles.get(group, 0) + 1
        else:
            groups = {}
            for node in nodes:
                group = node.get("group") or node.get("zone") or node.get("kind", "runtime")
                groups.setdefault(group, []).append(node)
            preferred = {"source": 0, "contract": 1, "runtime": 2, "proof": 3}
            ordered_groups = sorted(groups.items(), key=lambda item: (preferred.get(item[0], 99), item[0]))
            for col_index, (_, group_nodes) in enumerate(ordered_groups):
                for row_index, node in enumerate(group_nodes):
                    node["x"] = 120 + col_index * 360
                    node["y"] = 160 + row_index * 240

    return data


def repo_file_facts(root):
    root = Path(root)
    files = set()
    for path in root.rglob("*"):
        rel = path.relative_to(root)
        if is_ignored_path(rel):
            continue
        if path.is_file():
            files.add(str(rel))
    return files


def extract_repo_spec(root_path, title=None, theme="showcase"):
    root = Path(root_path).resolve()
    files = repo_file_facts(root)
    facts = repo_language_facts(root, files)
    nodes = []
    edges = []

    skill_file = first_existing(root, ["SKILL.md", "README.md"])
    nodes.append(extracted_node("repo", root.name, "local checkout", "memory", "source", root, skill_file, confidence="high", rule="repo.root", source_type="repo", role="source"))
    nodes.append(extracted_node("contract", "Skill Contract", "agent instructions", "service", "source", root, skill_file, needle="name:", confidence="high", rule="skill.contract", source_type="markdown", role="contract"))
    edges.append(extracted_edge("repo", "contract", "control", "declares", root, skill_file, needle="name:", confidence="high", rule="repo.has-skill-contract", source_type="markdown"))

    python_file = best_file([path for path in facts["python"] if path.startswith("scripts/")], best_file(facts["python"], "scripts/render_architecture.py"))
    if python_file in files:
        symbols = python_symbols(root, python_file)
        command_names = [symbol["name"].replace("handle_", "") for symbol in symbols if symbol["name"].startswith("handle_")]
        subtitle = ", ".join(command_names[:4]) if command_names else "language-aware CLI"
        if len(command_names) > 4:
            subtitle += f" +{len(command_names)-4}"
        nodes.append(extracted_node("runtime", "Renderer CLI", subtitle, "agent", "runtime", root, python_file, needle="def main", confidence="high", rule="python.ast.cli-handlers", source_type="python", role="runtime"))
        edges.append(extracted_edge("contract", "runtime", "control", "guides", root, python_file, needle="def main", confidence="high", rule="skill-to-python-runtime", source_type="python", source_side="right", target_side="top", via=[{"x": 360, "y": 400}, {"x": 360, "y": 80}, {"x": 840, "y": 80}]))

    if facts["schema"]:
        schema_file = best_file([path for path in facts["schema"] if "architecture" in path], facts["schema"][0])
        nodes.append(extracted_node("schemas", "Schema Contracts", f"{len(facts['schema'])} JSON schemas", "memory", "contract", root, schema_file, confidence="high", rule="json-schema.directory", source_type="schema", role="contract"))
        if python_file in files:
            edges.append(extracted_edge("schemas", "runtime", "control", "validate", root, python_file, needle="def validate", confidence="high", rule="schema-validated-runtime", source_type="python"))

    if facts["example"]:
        example_file = best_file([path for path in facts["example"] if "showcase" in path], facts["example"][0])
        nodes.append(extracted_node("examples", "Checked Examples", f"{len(facts['example'])} specs", "memory", "proof", root, example_file, confidence="high", rule="examples.checked-specs", source_type="json", role="proof"))
        if python_file in files:
            edges.append(extracted_edge("runtime", "examples", "primary-data", "generate", root, first_existing(root, ["Makefile", python_file]), needle="make examples", confidence="high", rule="makefile.examples-target", source_type="makefile"))

    workflow_file = best_file([path for path in facts["workflow"] if "validate" in path], best_file(facts["workflow"], ".github/workflows/validate.yml"))
    if workflow_file in files:
        workflow_titles = workflow_names(root, workflow_file)
        subtitle = workflow_titles[0]["name"] if workflow_titles else "validate and deploy"
        nodes.append(extracted_node("ci", "GitHub Actions", subtitle, "agent", "proof", root, workflow_file, confidence="high", rule="github-actions.workflow", source_type="workflow", role="proof"))
        target = "examples" if facts["example"] else "runtime"
        edges.append(extracted_edge("ci", target, "control", "checks", root, workflow_file, confidence="high", rule="ci-validates-artifacts", source_type="workflow"))

    if "index.html" in files or "docs/gallery.html" in files:
        gallery_file = "index.html" if "index.html" in files else "docs/gallery.html"
        nodes.append(extracted_node("gallery", "Pages Gallery", "evidence drilldown", "service", "proof", root, gallery_file, needle="Repo to artifact", confidence="high", rule="generated.gallery", source_type="html", role="release"))
        if facts["example"]:
            edges.append(extracted_edge("examples", "gallery", "primary-data", "publish", root, gallery_file, needle="artifact", confidence="high", rule="examples-to-gallery", source_type="html", source_side="right", target_side="right", via=[{"x": 1440, "y": 160}, {"x": 1440, "y": 640}]))

    if facts["package"]:
        pkg = facts["package"][0]
        scripts = package_scripts(root, pkg)
        subtitle = ", ".join(script["name"] for script in scripts[:3]) or "package metadata"
        nodes.append(extracted_node("package", "Package Metadata", subtitle, "service", "contract", root, pkg, confidence="medium", rule="package.scripts", source_type="package", role="package"))
        if python_file in files:
            edges.append(extracted_edge("package", "runtime", "control", "commands", root, pkg, confidence="medium", rule="package-to-runtime", source_type="package"))

    add_ts_monorepo_nodes(root, files, facts, nodes, edges)

    docs_file = first_existing(root, ["docs/repo-aware-generation.md", "README.md", "CHANGELOG.md"])
    if docs_file in files:
        headings = docs_headings(root, docs_file)
        subtitle = headings[0]["name"] if headings else "public docs"
        nodes.append(extracted_node("docs", "Product Docs", subtitle, "service", "proof", root, docs_file, confidence="high", rule="docs.heading", source_type="markdown", role="release"))
        if any(node["id"] == "gallery" for node in nodes):
            edges.append(extracted_edge("gallery", "docs", "memory-write", "explain", root, docs_file, confidence="high", rule="gallery-to-docs-positioning", source_type="markdown"))

    if "CHANGELOG.md" in files:
        nodes.append(extracted_node("release", "Release Surface", "changelog and tags", "service", "proof", root, "CHANGELOG.md", needle="v1.", confidence="high", rule="release.changelog", source_type="markdown", role="release"))
        source = "docs" if any(node["id"] == "docs" for node in nodes) else "gallery"
        if any(node["id"] == source for node in nodes):
            edges.append(extracted_edge(source, "release", "memory-write", "ship", root, "CHANGELOG.md", needle="v1.", confidence="high", rule="docs-to-release", source_type="markdown", source_side="right", target_side="right", via=[{"x": 1440, "y": 480}, {"x": 1440, "y": 880}]))

    edges = filter_valid_edges(nodes, edges)

    spec = {
        "mode": "architecture",
        "theme": theme,
        "sourceBacked": True,
        "title": title or f"{root.name} TypeScript Monorepo Map",
        "summary": "Generated from language-aware repository extraction with confidence-scored source evidence on inferred architecture claims.",
        "extraction": {
            "version": VERSION,
            "rules": ["python.ast.cli-handlers", "typescript.imports", "workspace.packages", "typescript.backend.modules", "typescript.frontend.entry", "json-schema.directory", "github-actions.workflow", "examples.checked-specs", "generated.gallery", "release.changelog"],
            "filesScanned": len(files),
            "surfaces": {name: len(paths) for name, paths in facts.items() if paths},
        },
        "story": [
            {"title": "Extract", "text": "Parse repo files by language and surface: Python, TS/TSX, workspaces, package metadata, workflows, schemas, examples, docs, and generated site files."},
            {"title": "Infer", "text": "Connect packages, app surfaces, backend/frontend/editor modules, contracts, CI, gallery, docs, and release surface with confidence-scored rules."},
            {"title": "Layout", "text": "Place nodes from inferred roles so source, contracts, runtime, proof, and release read left to right."},
            {"title": "Prove", "text": "Emit source evidence, quality receipt, share card, and gallery drilldown for every extracted claim."},
        ],
        "nodes": nodes,
        "edges": edges,
    }
    return layout_spec(spec, "architecture", theme=theme)


def changed_files(base, head, root_path="."):
    import subprocess

    def revision(value):
        if not isinstance(value, str) or not value or value.startswith("-"):
            raise ValueError("Git revision must be a non-option revision name")
        result = subprocess.run(
            ["git", "rev-parse", "--verify", "--end-of-options", value + "^{commit}"],
            cwd=root_path, text=True, capture_output=True, check=False,
        )
        if result.returncode != 0:
            raise ValueError("Git revision could not be resolved to a commit")
        oid = result.stdout.strip()
        if len(oid) not in (40, 64) or any(c not in "0123456789abcdef" for c in oid):
            raise ValueError("Git returned an invalid commit id")
        return oid

    base_oid = revision(base)
    revisions = [base_oid] if head == "WORKTREE" else [base_oid, revision(head)]
    command = ["git", "diff", "--no-ext-diff", "--no-textconv", "--name-status", *revisions, "--"]
    result = subprocess.run(command, cwd=root_path, text=True, capture_output=True, check=False)
    if result.returncode != 0:
        raise ValueError("Git diff failed")
    changes = []
    for line in result.stdout.splitlines():
        parts = line.split("\t")
        if len(parts) >= 2:
            changes.append((parts[0], parts[-1]))
    return changes


def change_concern(path):
    if path.startswith("scripts/") and path.endswith(".py"):
        return "runtime"
    if path.startswith("schemas/"):
        return "contract"
    if path.startswith("examples/") or path in {"index.html"} or path == "docs/gallery.html":
        return "artifacts"
    if path.startswith(".github/") or path == "Makefile":
        return "proof"
    if path in {"README.md", "CHANGELOG.md", "SKILL.md"} or path.startswith("docs/"):
        return "positioning"
    return "other"


def extract_pr_spec(base, head, root_path=".", theme="showcase"):
    root = Path(root_path).resolve()
    changes = changed_files(base, head, root)
    buckets = {"runtime": [], "contract": [], "artifacts": [], "proof": [], "positioning": [], "other": []}
    for status, file in changes:
        buckets[change_concern(file)].append((status, file))

    def subtitle(items):
        if not items:
            return "no changes"
        first = f"{items[0][0]} {Path(items[0][1]).name}"
        if len(items) == 1:
            return first
        return f"{len(items)} files, first: {first}"

    fallback = first_existing(root, ["CHANGELOG.md", "README.md"])
    nodes = [
        {"id": "base", "label": "Base", "subtitle": base, "kind": "memory", "group": "base", "evidence": evidence_item(root, fallback, confidence="medium", rule="git.ref.base", source_type="git")},
        {"id": "head", "label": "Head", "subtitle": head, "kind": "memory", "group": "head", "evidence": evidence_item(root, fallback, confidence="medium", rule="git.ref.head", source_type="git")},
    ]
    concern_meta = {
        "runtime": ("Runtime Changes", "agent", "changed"),
        "contract": ("Contract Changes", "memory", "changed"),
        "artifacts": ("Artifact Changes", "service", "changed"),
        "proof": ("Proof/CI Changes", "agent", "risk"),
        "positioning": ("Docs/Positioning", "service", "changed"),
        "other": ("Other Changes", "service", "risk"),
    }
    for concern, items in buckets.items():
        if not items:
            continue
        label, kind, group = concern_meta[concern]
        first_path = items[0][1]
        confidence = "high" if concern != "other" else "low"
        nodes.append(extracted_node(concern, label, subtitle(items), kind, group, root, first_path, confidence=confidence, rule=f"git.diff.concern.{concern}", source_type="git", role=concern))

    nodes.append({"id": "review", "label": "Architecture Review", "subtitle": f"{len(changes)} files / {sum(1 for items in buckets.values() if items)} concerns", "kind": "llm", "group": "review", "evidence": evidence_item(root, fallback, confidence="medium", rule="pr.review.summary", source_type="git")})
    nodes.append({"id": "receipt", "label": "Delta Receipt", "subtitle": "concerns and confidence", "kind": "memory", "group": "receipt", "evidence": evidence_item(root, fallback, confidence="medium", rule="pr.receipt", source_type="git")})

    edges = [
        extracted_edge("base", "review", "control", "compare", root, fallback, confidence="medium", rule="git.diff.base", source_type="git", source_side="right", target_side="top", via=[{"x": 240, "y": 80}, {"x": 840, "y": 80}]),
        extracted_edge("head", "review", "control", "compare", root, fallback, confidence="medium", rule="git.diff.head", source_type="git", source_side="right", target_side="bottom", via=[{"x": 240, "y": 560}, {"x": 840, "y": 560}]),
    ]
    for concern, items in buckets.items():
        if items:
            confidence = "high" if concern != "other" else "low"
            route = {"source_side": "right", "target_side": "left"}
            if concern == "runtime":
                route = {"source_side": "right", "target_side": "top", "via": [{"x": 600, "y": 80}, {"x": 840, "y": 80}]}
            elif concern == "positioning":
                route = {"source_side": "right", "target_side": "bottom", "via": [{"x": 720, "y": 720}, {"x": 840, "y": 720}]}
            edges.append(extracted_edge(concern, "review", "primary-data" if concern in {"runtime", "artifacts", "contract"} else "control", concern, root, items[0][1], confidence=confidence, rule=f"pr.concern.{concern}", source_type="git", **route))
    edges.append(extracted_edge("review", "receipt", "memory-write", "facts", root, fallback, confidence="medium", rule="pr.review-to-receipt", source_type="git"))

    spec = {
        "mode": "pr-delta",
        "theme": theme,
        "sourceBacked": True,
        "title": "Generated PR Delta Review",
        "summary": f"Generated from git diff {base}..{head}: {len(changes)} files grouped into architecture concerns instead of raw filename buckets.",
        "extraction": {"version": VERSION, "base": base, "head": head, "concerns": {key: len(value) for key, value in buckets.items() if value}},
        "story": [
            {"title": "Diff", "text": f"Read changed files from {base}..{head}."},
            {"title": "Classify", "text": "Map files into runtime, contract, artifact, proof, positioning, and other concerns."},
            {"title": "Review", "text": "Show what architecture surface changed, with confidence and evidence in the receipt."},
        ],
        "nodes": nodes,
        "edges": edges,
        "delta": {"base": base, "head": head, "changedFiles": [{"status": status, "path": file, "concern": change_concern(file)} for status, file in changes]},
    }
    return layout_spec(spec, "pr-delta", theme=theme)


def validate(data):
    errors = []
    warnings = []

    if not isinstance(data, dict):
        return {
            "ok": False,
            "errors": [{"code": "spec.type", "message": "Spec must be a JSON object."}],
            "warnings": [],
            "metrics": {},
        }

    mode = spec_mode(data)
    if mode not in ALLOWED_MODES:
        errors.append({
            "code": "mode.unsupported",
            "subject": "mode",
            "message": f"mode must be one of {sorted(ALLOWED_MODES)}.",
            "supportedFixes": [{"field": "mode", "values": sorted(ALLOWED_MODES)}],
        })

    theme = spec_theme(data)
    if theme not in ALLOWED_THEMES:
        errors.append({
            "code": "theme.unsupported",
            "subject": "theme",
            "message": f"theme must be one of {sorted(ALLOWED_THEMES)}.",
            "supportedFixes": [{"field": "theme", "values": sorted(ALLOWED_THEMES)}],
        })

    title = data.get("title")
    if not isinstance(title, str) or not title.strip():
        errors.append({"code": "title.required", "message": "Spec requires a non-empty string title."})

    nodes = data.get("nodes")
    if not isinstance(nodes, list) or not nodes:
        errors.append({"code": "nodes.required", "message": "Spec requires at least one node."})
        nodes = []

    edges = data.get("edges", [])
    if not isinstance(edges, list):
        errors.append({"code": "edges.type", "message": "edges must be a list."})
        edges = []

    ids = set()
    duplicate_ids = set()
    for index, node in enumerate(nodes):
        subject = f"nodes[{index}]"
        if not isinstance(node, dict):
            errors.append({"code": "node.type", "subject": subject, "message": "Node must be an object."})
            continue
        node_id = node.get("id")
        if not isinstance(node_id, str) or not node_id.strip():
            errors.append({"code": "node.id.required", "subject": subject, "message": "Node requires a non-empty id."})
        elif node_id in ids:
            duplicate_ids.add(node_id)
        else:
            ids.add(node_id)
        if not isinstance(node.get("label"), str) or not node.get("label", "").strip():
            errors.append({"code": "node.label.required", "subject": subject, "message": "Node requires a non-empty label."})
        if node.get("kind") not in ALLOWED_NODE_KINDS:
            errors.append({
                "code": "node.kind.unsupported",
                "subject": node_id or subject,
                "message": f"Node kind must be one of {sorted(ALLOWED_NODE_KINDS)}.",
                "supportedFixes": [{"field": "kind", "values": sorted(ALLOWED_NODE_KINDS)}],
            })
        validate_evidence(node, f"nodes[{index}]", errors, warnings)
        for axis, grid in (("x", GRID_X), ("y", GRID_Y)):
            value = node.get(axis)
            if not isinstance(value, (int, float)):
                errors.append({"code": f"node.{axis}.required", "subject": node_id or subject, "message": f"Node requires numeric {axis}."})
            elif value != snap(value, grid):
                warnings.append({
                    "code": f"node.{axis}.snapped",
                    "subject": node_id or subject,
                    "message": f"{axis}={value} will snap to {snap(value, grid)}.",
                    "supportedFixes": [{"field": axis, "value": snap(value, grid)}],
                })

    for duplicate_id in sorted(duplicate_ids):
        errors.append({"code": "node.id.duplicate", "subject": duplicate_id, "message": "Node ids must be unique."})

    seen_positions = {}
    for node in nodes:
        if not isinstance(node, dict) or "id" not in node:
            continue
        pos = (snap(node.get("x", 0), GRID_X), snap(node.get("y", 0), GRID_Y))
        if pos in seen_positions:
            warnings.append({
                "code": "node.position.shared",
                "subject": node["id"],
                "message": f"Shares grid position with {seen_positions[pos]}. This usually causes overlap.",
            })
        else:
            seen_positions[pos] = node["id"]

    for index, edge in enumerate(edges):
        subject = f"edges[{index}]"
        if not isinstance(edge, dict):
            errors.append({"code": "edge.type", "subject": subject, "message": "Edge must be an object."})
            continue
        source = edge.get("from")
        target = edge.get("to")
        if source not in ids:
            errors.append({"code": "edge.from.unknown", "subject": subject, "message": f"Unknown source node: {source}."})
        if target not in ids:
            errors.append({"code": "edge.to.unknown", "subject": subject, "message": f"Unknown target node: {target}."})
        if edge.get("kind") not in ALLOWED_EDGE_KINDS:
            errors.append({
                "code": "edge.kind.unsupported",
                "subject": subject,
                "message": f"Edge kind must be one of {sorted(ALLOWED_EDGE_KINDS)}.",
                "supportedFixes": [{"field": "kind", "values": sorted(ALLOWED_EDGE_KINDS)}],
            })
        if edge.get("label") and len(edge["label"]) > 28:
            warnings.append({
                "code": "edge.label.long",
                "subject": subject,
                "message": "Long edge labels can crowd the route; keep labels short and semantic.",
            })
        validate_evidence(edge, f"edges[{index}]", errors, warnings)
        for point_index, point in enumerate(edge.get("via", [])):
            point_subject = f"{subject}.via[{point_index}]"
            if not isinstance(point, dict):
                errors.append({"code": "edge.via.type", "subject": point_subject, "message": "via points must be objects."})
                continue
            for axis, grid in (("x", GRID_X), ("y", GRID_Y)):
                value = point.get(axis)
                if not isinstance(value, (int, float)):
                    errors.append({"code": f"edge.via.{axis}.required", "subject": point_subject, "message": f"via point requires numeric {axis}."})
                elif value != snap(value, grid):
                    warnings.append({
                        "code": f"edge.via.{axis}.snapped",
                        "subject": point_subject,
                        "message": f"{axis}={value} will snap to {snap(value, grid)}.",
                    })

    quality = {"score": 0, "rating": "unscored", "checks": [], "routeCrossings": 0}
    if data.get("sourceBacked"):
        missing = []
        low_confidence = 0
        for index, node in enumerate(nodes):
            if isinstance(node, dict):
                items = evidence_items(node)
                if not items:
                    missing.append(f"nodes[{index}]")
                low_confidence += sum(1 for item in items if isinstance(item, dict) and item.get("confidence") == "low")
        for index, edge in enumerate(edges):
            if isinstance(edge, dict):
                items = evidence_items(edge)
                if not items:
                    missing.append(f"edges[{index}]")
                low_confidence += sum(1 for item in items if isinstance(item, dict) and item.get("confidence") == "low")
        if missing:
            errors.append({"code": "source.evidence.required", "message": "sourceBacked artifacts require evidence on every node and edge.", "subjects": missing[:12]})
        if low_confidence:
            warnings.append({"code": "source.confidence.low", "message": f"{low_confidence} source evidence item(s) are low confidence; review before publishing."})

    if not errors and nodes:
        placed = position_nodes(nodes)
        for index, edge in enumerate(edges):
            source_id = edge["from"]
            target_id = edge["to"]
            points = orthogonal_points(placed[source_id], placed[target_id], edge)
            for node_id, node in placed.items():
                if node_id in (source_id, target_id):
                    continue
                box = box_edges(node, margin=8)
                for a, b in zip(points, points[1:]):
                    if segment_crosses_box(a, b, box):
                        warnings.append({
                            "code": "edge.route.crosses-node",
                            "subject": f"edges[{index}]",
                            "message": f"Route crosses unrelated node {node_id}. Add via points or move nodes.",
                            "supportedFixes": [{"field": "via", "message": "Route around the unrelated node with grid-snapped orthogonal turn points."}],
                        })
                        break
        quality = quality_profile(data, placed, edges, warnings)

    return {
        "ok": not errors,
        "errors": errors,
        "warnings": warnings,
        "metrics": {
            "mode": mode,
            "theme": theme,
            "nodes": len(nodes),
            "edges": len(edges),
            "quality": quality,
            "evidenceItems": sum(len(evidence_items(node)) for node in nodes if isinstance(node, dict)) + sum(len(evidence_items(edge)) for edge in edges if isinstance(edge, dict)),
            "sourceConfidence": {level: sum(1 for subject in list(nodes) + list(edges) if isinstance(subject, dict) for item in evidence_items(subject) if isinstance(item, dict) and item.get("confidence", "unspecified") == level) for level in ["high", "medium", "low", "unspecified"]},
            "sourceBacked": bool(data.get("sourceBacked")),
            "nodeKinds": sorted({node.get("kind") for node in nodes if isinstance(node, dict) and node.get("kind")}),
            "edgeKinds": sorted({edge.get("kind") for edge in edges if isinstance(edge, dict) and edge.get("kind")}),
        },
    }


def anchor(node, side):
    x = node["x"]
    y = node["y"]
    w = node["width"]
    h = node["height"]
    if side == "left":
        return x - w / 2, y
    if side == "right":
        return x + w / 2, y
    if side == "top":
        return x, y - h / 2
    return x, y + h / 2


def choose_sides(source, target):
    dx = target["x"] - source["x"]
    dy = target["y"] - source["y"]
    if abs(dx) >= abs(dy):
        return ("right", "left") if dx >= 0 else ("left", "right")
    return ("bottom", "top") if dy >= 0 else ("top", "bottom")


def clean_points(points):
    cleaned = [points[0]]
    for point in points[1:]:
        if point != cleaned[-1]:
            cleaned.append(point)

    final = [cleaned[0]]
    for point in cleaned[1:]:
        if len(final) >= 2:
            ax, ay = final[-2]
            bx, by = final[-1]
            cx, cy = point
            if (ax == bx == cx) or (ay == by == cy):
                final[-1] = point
                continue
        final.append(point)
    return final


def orthogonal_points(source, target, edge=None):
    edge = edge or {}
    source_side = edge.get("source_side")
    target_side = edge.get("target_side")
    if not source_side or not target_side:
        auto_source, auto_target = choose_sides(source, target)
        source_side = source_side or auto_source
        target_side = target_side or auto_target

    sx, sy = anchor(source, source_side)
    tx, ty = anchor(target, target_side)
    points = [(sx, sy)]

    via = edge.get("via", [])
    if via:
        for point in via:
            points.append((snap(point["x"], GRID_X), snap(point["y"], GRID_Y)))
    elif source_side in ("left", "right"):
        dogleg = snap((sx + tx) / 2, GRID_X)
        points.extend([(dogleg, sy), (dogleg, ty)])
    else:
        dogleg = snap((sy + ty) / 2, GRID_Y)
        points.extend([(sx, dogleg), (tx, dogleg)])

    points.append((tx, ty))
    return clean_points(points)


def path_d(points):
    return " ".join([f"M {points[0][0]:.1f} {points[0][1]:.1f}"] + [f"L {x:.1f} {y:.1f}" for x, y in points[1:]])


def segment_midpoint(points, index=None):
    segments = list(zip(points, points[1:]))
    if not segments:
        return points[0]
    if index is not None:
        index = max(0, min(index, len(segments) - 1))
        a, b = segments[index]
        return ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)

    max_len = -1
    best = (points[0][0], points[0][1])
    for a, b in segments:
        length = abs(b[0] - a[0]) + abs(b[1] - a[1])
        if length > max_len:
            max_len = length
            best = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
    return best


def arrow_head(a, b, size=9):
    angle = math.atan2(b[1] - a[1], b[0] - a[0])
    left = (b[0] - size * math.cos(angle) + size * 0.6 * math.sin(angle),
            b[1] - size * math.sin(angle) - size * 0.6 * math.cos(angle))
    right = (b[0] - size * math.cos(angle) - size * 0.6 * math.sin(angle),
             b[1] - size * math.sin(angle) + size * 0.6 * math.cos(angle))
    return left, b, right


def render_node(node, theme):
    styles = theme["node"]
    style = styles.get(node.get("kind", "service"), styles["service"])
    x = node["x"]
    y = node["y"]
    w = node["width"]
    h = node["height"]
    left = x - w / 2
    top = y - h / 2
    shape_parts = []
    label_parts = []
    kind = node.get("kind", "service")

    if theme["halo"]:
        if kind == "agent":
            cut = min(22, w * 0.14)
            halo_points = [
                (left + cut - 6, top - 6), (left + w - cut + 6, top - 6), (left + w + 8, y),
                (left + w - cut + 6, top + h + 6), (left + cut - 6, top + h + 6), (left - 8, y)
            ]
            halo_points_str = " ".join(f"{px:.1f},{py:.1f}" for px, py in halo_points)
            shape_parts.append(f'<polygon points="{halo_points_str}" fill="{style["stroke"]}" opacity="0.13"/>')
        else:
            shape_parts.append(f'<rect x="{left-8:.1f}" y="{top-8:.1f}" width="{w+16:.1f}" height="{h+16:.1f}" rx="18" fill="{style["stroke"]}" opacity="0.13"/>')

    if kind == "llm":
        shape_parts.append(f'<rect x="{left:.1f}" y="{top:.1f}" width="{w:.1f}" height="{h:.1f}" rx="16" fill="{style["fill"]}" stroke="{style["stroke"]}" stroke-width="2"/>')
        shape_parts.append(f'<rect x="{left+6:.1f}" y="{top+6:.1f}" width="{w-12:.1f}" height="{h-12:.1f}" rx="12" fill="none" stroke="{style["stroke"]}" stroke-width="1.5"/>')
    elif kind == "agent":
        cut = min(22, w * 0.14)
        points = [
            (left + cut, top), (left + w - cut, top), (left + w, y),
            (left + w - cut, top + h), (left + cut, top + h), (left, y)
        ]
        points_str = " ".join(f"{px:.1f},{py:.1f}" for px, py in points)
        shape_parts.append(f'<polygon points="{points_str}" fill="{style["fill"]}" stroke="{style["stroke"]}" stroke-width="2"/>')
    elif kind == "memory":
        rx = w / 2
        ry = 12
        cx = x
        top_y = top + ry
        bottom_y = top + h - ry
        shape_parts.append(f'<path d="M {left:.1f} {top_y:.1f} A {rx:.1f} {ry:.1f} 0 0 1 {left+w:.1f} {top_y:.1f} L {left+w:.1f} {bottom_y:.1f} A {rx:.1f} {ry:.1f} 0 0 1 {left:.1f} {bottom_y:.1f} Z" fill="{style["fill"]}" stroke="{style["stroke"]}" stroke-width="2"/>')
        shape_parts.append(f'<ellipse cx="{cx:.1f}" cy="{top_y:.1f}" rx="{rx:.1f}" ry="{ry:.1f}" fill="{style["fill"]}" stroke="{style["stroke"]}" stroke-width="2"/>')
        shape_parts.append(f'<path d="M {left:.1f} {bottom_y:.1f} A {rx:.1f} {ry:.1f} 0 0 0 {left+w:.1f} {bottom_y:.1f}" fill="none" stroke="{style["stroke"]}" stroke-width="2"/>')
    else:
        shape_parts.append(f'<rect x="{left:.1f}" y="{top:.1f}" width="{w:.1f}" height="{h:.1f}" rx="12" fill="{style["fill"]}" stroke="{style["stroke"]}" stroke-width="2"/>')

    label_parts.append(f'<text x="{x:.1f}" y="{y - (4 if node.get("subtitle") else -6):.1f}" text-anchor="middle" font-family="{FONT_FAMILY}" font-size="18" font-weight="600" fill="{style["text"]}">{escape(node["label"])}</text>')
    if node.get("subtitle"):
        label_parts.append(f'<text x="{x:.1f}" y="{y + 18:.1f}" text-anchor="middle" font-family="{FONT_FAMILY}" font-size="13" font-weight="500" fill="{style.get("muted", "#475569")}">{escape(node["subtitle"])}</text>')
    evidence_count = len(evidence_items(node))
    if evidence_count:
        badge = f"SRC {evidence_count}"
        badge_width = text_width(badge, 10) + 12
        label_parts.append(f'<rect x="{left + w - badge_width - 10:.1f}" y="{top + 8:.1f}" width="{badge_width:.1f}" height="18" rx="9" fill="{theme["badge_fill"]}" stroke="{theme["badge_stroke"]}" stroke-width="1"/>')
        label_parts.append(f'<text x="{left + w - badge_width / 2 - 10:.1f}" y="{top + 21:.1f}" text-anchor="middle" font-family="{FONT_FAMILY}" font-size="10" font-weight="700" fill="{theme["badge_text"]}">{escape(badge)}</text>')
    shape_group = f'<g class="node-shape" data-node-id="{escape(str(node.get("id", "")))}">\n' + "\n".join(shape_parts) + "\n</g>"
    return shape_group, "\n".join(label_parts)


def render_edge(edge, nodes, theme):
    source = nodes[edge["from"]]
    target = nodes[edge["to"]]
    points = orthogonal_points(source, target, edge)
    styles = theme["edge"]
    style = styles.get(edge.get("kind", "control"), styles["control"])
    edge_parts = []
    label_parts = []
    dash = f' stroke-dasharray="{style["dash"]}"' if style["dash"] else ""
    edge_parts.append(f'<path d="{path_d(points)}" fill="none" stroke="{style["stroke"]}" stroke-width="3" stroke-linejoin="round" stroke-linecap="round"{dash}/>')
    left, tip, right = arrow_head(points[-2], points[-1])
    edge_parts.append(f'<polygon points="{left[0]:.1f},{left[1]:.1f} {tip[0]:.1f},{tip[1]:.1f} {right[0]:.1f},{right[1]:.1f}" fill="{style["stroke"]}"/>')
    if edge.get("label"):
        lx, ly = segment_midpoint(points, edge.get("label_segment"))
        dx, dy = edge.get("label_offset", [0, 0])
        lx += dx
        ly += dy
        label = edge["label"]
        width = text_width(label, 12) + 18
        height = 24
        label_parts.append(f'<rect x="{lx - width/2:.1f}" y="{ly - height/2:.1f}" width="{width:.1f}" height="{height:.1f}" rx="6" fill="{style["label_fill"]}" stroke="{style.get("label_stroke", theme["label_border"])}" stroke-width="2"/>')
        label_parts.append(f'<text x="{lx:.1f}" y="{ly + 4:.1f}" text-anchor="middle" font-family="{FONT_FAMILY}" font-size="12" font-weight="600" fill="{style["label_text"]}">{escape(label)}</text>')
    return "\n".join(edge_parts), "\n".join(label_parts)




def render_mode_backdrop(data, nodes, min_x, min_y, width, height, theme):
    mode = spec_mode(data)
    accent = MODE_ACCENTS.get(mode, MODE_ACCENTS["architecture"])
    dark = theme["name"] == "showcase"
    panel_fill = "#07111f" if dark else "#eef6ff"
    panel_alt = "#0b1726" if dark else "#f6f8fb"
    stroke = "#1f3448" if dark else "#cbd5e1"
    text = "#8fb5d9" if dark else "#475569"
    parts = []

    def label(x, y, value):
        return f'<text x="{x:.1f}" y="{y:.1f}" font-family="{FONT_FAMILY}" font-size="11" font-weight="800" fill="{text}">{escape(value)}</text>'

    if mode in ("architecture", "dataflow", "pr-delta"):
        zones = accent["zones"]
        zone_width = width / len(zones)
        for index, zone in enumerate(zones):
            x = min_x + index * zone_width
            fill = panel_fill if index % 2 == 0 else panel_alt
            parts.append(f'<rect x="{x:.1f}" y="{min_y:.1f}" width="{zone_width:.1f}" height="{height:.1f}" fill="{fill}" opacity="0.55"/>')
            parts.append(f'<line x1="{x + zone_width:.1f}" y1="{min_y:.1f}" x2="{x + zone_width:.1f}" y2="{min_y + height:.1f}" stroke="{stroke}" stroke-width="1" opacity="0.7"/>')
            parts.append(label(x + 18, min_y + 26, zone.upper()))
    elif mode == "workflow":
        bands = sorted({node["y"] for node in nodes.values()}) or [min_y + height / 2]
        for index, y in enumerate(bands):
            top = y - GRID_Y / 2
            fill = panel_fill if index % 2 == 0 else panel_alt
            parts.append(f'<rect x="{min_x:.1f}" y="{top:.1f}" width="{width:.1f}" height="{GRID_Y:.1f}" fill="{fill}" opacity="0.58"/>')
            parts.append(label(min_x + width - 92, top + 24, f"LANE {index + 1}"))
    elif mode == "sequence":
        for node in nodes.values():
            parts.append(f'<line x1="{node["x"]:.1f}" y1="{node["y"] + node["height"] / 2 + 18:.1f}" x2="{node["x"]:.1f}" y2="{min_y + height - 34:.1f}" stroke="{accent["tone"]}" stroke-width="2" stroke-dasharray="5 8" opacity="0.38"/>')
            parts.append(label(node["x"] - node["width"] / 2, min_y + 26, "PARTICIPANT"))
    elif mode == "lifecycle":
        sorted_nodes = sorted(nodes.values(), key=lambda node: (node["x"], node["y"]))
        if sorted_nodes:
            path = " ".join([f"M {sorted_nodes[0]['x']:.1f} {sorted_nodes[0]['y']:.1f}"] + [f"L {node['x']:.1f} {node['y']:.1f}" for node in sorted_nodes[1:]])
            parts.append(f'<path d="{path}" fill="none" stroke="{accent["tone"]}" stroke-width="18" stroke-linecap="round" stroke-linejoin="round" opacity="0.08"/>')
            for index, node in enumerate(sorted_nodes):
                parts.append(f'<circle cx="{node["x"]:.1f}" cy="{node["y"]:.1f}" r="44" fill="{accent["tone"]}" opacity="0.07"/>')
                parts.append(label(node["x"] - 20, node["y"] - 52, f"S{index + 1}"))

    parts.append(f'<rect x="{min_x + 10:.1f}" y="{min_y + height - 34:.1f}" width="{text_width(accent["label"], 12) + 26:.1f}" height="22" rx="6" fill="{accent["tone"]}" opacity="0.18" stroke="{accent["tone"]}" stroke-width="1"/>')
    parts.append(f'<text x="{min_x + 23:.1f}" y="{min_y + height - 19:.1f}" font-family="{FONT_FAMILY}" font-size="11" font-weight="800" fill="{accent["tone"]}">{escape(accent["label"].upper())}</text>')
    return "\n".join(parts)


def render(data):
    theme = theme_pack(data)
    nodes = position_nodes(data["nodes"])
    xs = [n["x"] for n in nodes.values()]
    ys = [n["y"] for n in nodes.values()]
    widths = [n["width"] for n in nodes.values()]
    heights = [n["height"] for n in nodes.values()]
    route_points = [
        point
        for edge in data.get("edges", [])
        for point in orthogonal_points(nodes[edge["from"]], nodes[edge["to"]], edge)
    ]
    route_xs = [point[0] for point in route_points]
    route_ys = [point[1] for point in route_points]
    min_x = min([x - w / 2 for x, w in zip(xs, widths)] + route_xs) - PADDING
    max_x = max([x + w / 2 for x, w in zip(xs, widths)] + route_xs) + PADDING
    min_y = min([y - h / 2 for y, h in zip(ys, heights)] + route_ys) - PADDING
    max_y = max([y + h / 2 for y, h in zip(ys, heights)] + route_ys) + PADDING
    width = max_x - min_x
    height = max_y - min_y

    edge_shapes = []
    edge_labels = []
    for edge in data.get("edges", []):
        shape_svg, label_svg = render_edge(edge, nodes, theme)
        edge_shapes.append(shape_svg)
        if label_svg:
            edge_labels.append(label_svg)

    node_shapes = []
    node_labels = []
    for node in nodes.values():
        shape_svg, label_svg = render_node(node, theme)
        node_shapes.append(shape_svg)
        if label_svg:
            node_labels.append(label_svg)

    title = escape(data.get("title", "Architecture"))
    backdrop_svg = indent(render_mode_backdrop(data, nodes, min_x, min_y, width, height, theme), 4)
    edge_shapes_svg = indent("\n".join(edge_shapes), 4)
    node_shapes_svg = indent("\n".join(node_shapes), 4)
    labels_svg = indent("\n".join(edge_labels + node_labels), 4)

    show_grid = data.get("show_grid", False)
    grid_svg = ""
    if show_grid:
        grid_svg = f'\n  <rect x="{min_x:.1f}" y="{min_y:.1f}" width="{width:.1f}" height="{height:.1f}" fill="url(#grid)" opacity="0.85"/>'

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width:.1f}" height="{height:.1f}" viewBox="{min_x:.1f} {min_y:.1f} {width:.1f} {height:.1f}" role="img" aria-label="{title}">
  <defs>
    <pattern id="grid" width="{GRID_X}" height="{GRID_Y}" patternUnits="userSpaceOnUse">
      <path d="M {GRID_X} 0 L 0 0 0 {GRID_Y}" fill="none" stroke="{theme["grid"]}" stroke-width="1"/>
    </pattern>
  </defs>
  <rect x="{min_x:.1f}" y="{min_y:.1f}" width="{width:.1f}" height="{height:.1f}" fill="{theme["background"]}"/>{grid_svg}
  <g id="mode-backdrop">
{backdrop_svg}
  </g>
  <g id="arrows">
{edge_shapes_svg}
  </g>
  <g id="nodes">
{node_shapes_svg}
  </g>
  <g id="labels">
{labels_svg}
  </g>
</svg>
'''


def render_html(data, svg, spec_path):
    title = escape(data.get("title", "Architecture"))
    summary = escape(data.get("summary", "Deterministic architecture artifact generated from structured JSON."))
    source_name = escape(Path(spec_path).name)
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <style>
    :root {{
      color-scheme: light dark;
      --bg: #0f172a;
      --panel: #f8fafc;
      --ink: #0f172a;
      --muted: #475569;
      --border: #cbd5e1;
      --accent: #2563eb;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      background: var(--bg);
      color: #f8fafc;
    }}
    main {{
      min-height: 100vh;
      display: grid;
      grid-template-rows: auto 1fr auto;
      gap: 18px;
      padding: 28px;
    }}
    header, footer {{
      max-width: 1180px;
      width: 100%;
      margin: 0 auto;
    }}
    h1 {{
      margin: 0 0 8px;
      font-size: clamp(24px, 3vw, 40px);
      line-height: 1.1;
      letter-spacing: 0;
    }}
    p {{
      max-width: 760px;
      margin: 0;
      color: #cbd5e1;
      line-height: 1.55;
    }}
    .artifact {{
      width: min(1180px, 100%);
      margin: 0 auto;
      align-self: center;
      background: var(--panel);
      color: var(--ink);
      border: 1px solid var(--border);
      border-radius: 8px;
      overflow: auto;
      box-shadow: 0 24px 64px rgba(2, 6, 23, 0.28);
    }}
    .artifact svg {{
      display: block;
      width: 100%;
      height: auto;
    }}
    footer {{
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      align-items: center;
      color: #cbd5e1;
      font-size: 13px;
    }}
    code {{
      color: #dbeafe;
      background: rgba(15, 23, 42, 0.82);
      border: 1px solid rgba(203, 213, 225, 0.24);
      border-radius: 6px;
      padding: 3px 6px;
    }}
  </style>
</head>
<body>
  <main>
    <header>
      <h1>{title}</h1>
      <p>{summary}</p>
    </header>
    <section class="artifact" aria-label="Architecture diagram">
{indent(svg, 6)}
    </section>
    <footer>
      <span>Source spec</span>
      <code>{source_name}</code>
      <span>Generated by visual-architecture.</span>
    </footer>
  </main>
</body>
</html>
'''


def write_atomic(path, text):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = path.with_name(f".{path.name}.tmp-{os.getpid()}")
    tmp_path.write_text(text, encoding="utf-8")
    tmp_path.replace(path)


def receipt_for(spec_path, output_path, validation, artifact_kind):
    spec_path = Path(spec_path)
    output_path = Path(output_path)
    return {
        "tool": "visual-architecture",
        "version": VERSION,
        "artifactKind": artifact_kind,
        "mode": validation.get("metrics", {}).get("mode", "architecture"),
        "generatedAt": dt.datetime.now(dt.timezone.utc).isoformat(),
        "input": {
            "path": str(spec_path),
            "sha256": file_sha256(spec_path),
            "bytes": spec_path.stat().st_size,
        },
        "output": {
            "path": str(output_path),
            "sha256": file_sha256(output_path),
            "bytes": output_path.stat().st_size,
        },
        "validation": validation,
    }


def print_json(payload):
    print(json.dumps(payload, indent=2, sort_keys=True))


def handle_validate(args):
    data = load(args.input)
    validation = validate(data)
    payload = {
        "tool": "visual-architecture",
        "version": VERSION,
        "input": args.input,
        "validation": validation,
    }
    print_json(payload if args.json else validation)
    return 0 if validation["ok"] else 1


def edge_key(edge):
    return (edge.get("from"), edge.get("to"), edge.get("kind", "control"), edge.get("label", ""))


def build_delta_spec(base_data, head_data):
    base_nodes = {node["id"]: node for node in base_data.get("nodes", []) if isinstance(node, dict) and "id" in node}
    head_nodes = {node["id"]: node for node in head_data.get("nodes", []) if isinstance(node, dict) and "id" in node}
    base_edges = {edge_key(edge) for edge in base_data.get("edges", []) if isinstance(edge, dict)}
    head_edges = {edge_key(edge) for edge in head_data.get("edges", []) if isinstance(edge, dict)}
    added_nodes = sorted(set(head_nodes) - set(base_nodes))
    removed_nodes = sorted(set(base_nodes) - set(head_nodes))
    added_edges = sorted(head_edges - base_edges)
    removed_edges = sorted(base_edges - head_edges)
    return {
        "mode": "pr-delta",
        "title": "PR Delta Architecture Review",
        "summary": f"{len(added_nodes)} nodes added, {len(removed_nodes)} removed, {len(added_edges)} edges added, {len(removed_edges)} removed.",
        "nodes": [
            {"id": "base", "label": "Base", "subtitle": f"{len(base_nodes)} nodes", "kind": "memory", "x": 120, "y": 160},
            {"id": "head", "label": "Head", "subtitle": f"{len(head_nodes)} nodes", "kind": "memory", "x": 120, "y": 320},
            {"id": "added", "label": "Added", "subtitle": ", ".join(added_nodes[:3]) or "none", "kind": "service", "x": 360, "y": 160},
            {"id": "removed", "label": "Removed", "subtitle": ", ".join(removed_nodes[:3]) or "none", "kind": "service", "x": 360, "y": 320},
            {"id": "routes", "label": "Route Delta", "subtitle": f"+{len(added_edges)} / -{len(removed_edges)}", "kind": "agent", "x": 600, "y": 240},
            {"id": "review", "label": "Review Receipt", "subtitle": "PR-ready", "kind": "memory", "x": 840, "y": 240},
        ],
        "edges": [
            {"from": "base", "to": "added", "kind": "control", "label": "compare", "label_offset": [0, -28]},
            {"from": "head", "to": "removed", "kind": "control", "label": "compare", "label_offset": [0, 28]},
            {"from": "added", "to": "routes", "kind": "primary-data", "label": "new facts"},
            {"from": "removed", "to": "routes", "kind": "control", "label": "removed facts"},
            {"from": "routes", "to": "review", "kind": "memory-write", "label": "receipt"},
        ],
        "delta": {
            "addedNodes": added_nodes,
            "removedNodes": removed_nodes,
            "addedEdges": [list(edge) for edge in added_edges],
            "removedEdges": [list(edge) for edge in removed_edges],
        },
    }


def handle_compare(args):
    base_data = load(args.base)
    head_data = load(args.head)
    base_validation = validate(base_data)
    head_validation = validate(head_data)
    if not base_validation["ok"] or not head_validation["ok"]:
        print_json({"ok": False, "base": base_validation, "head": head_validation})
        return 1
    delta_spec = build_delta_spec(base_data, head_data)
    if args.spec:
        write_atomic(args.spec, json.dumps(delta_spec, indent=2, sort_keys=True) + "\n")
    validation = validate(delta_spec)
    svg = render(delta_spec)
    output_path = Path(args.output)
    artifact_kind = "html" if output_path.suffix.lower() == ".html" else "svg"
    artifact = render_html(delta_spec, svg, args.spec or args.head) if artifact_kind == "html" else svg
    write_atomic(output_path, artifact)
    receipt_path = Path(args.receipt) if args.receipt else output_path.with_suffix(output_path.suffix + ".receipt.json")
    receipt = {
        **receipt_for(args.head, output_path, validation, artifact_kind),
        "base": {"path": args.base, "sha256": file_sha256(args.base)},
        "head": {"path": args.head, "sha256": file_sha256(args.head)},
        "delta": delta_spec["delta"],
    }
    write_atomic(receipt_path, json.dumps(receipt, indent=2, sort_keys=True) + "\n")
    print_json(receipt if args.json else {"ok": True, "output": str(output_path), "receipt": str(receipt_path)})
    return 0


def render_share_card(data, source_path):
    title = escape(data.get("title", "visual-architecture"))
    summary = data.get("summary", "Deterministic local-first architecture artifact.")
    mode = escape(spec_mode(data))
    source = escape(Path(source_path).name)
    words = str(summary).split()
    lines = []
    current = []
    for word in words:
        candidate = " ".join(current + [word])
        if len(candidate) > 64 and current:
            lines.append(" ".join(current))
            current = [word]
        else:
            current.append(word)
    if current:
        lines.append(" ".join(current))
    summary_svg = "\n".join(
        f'  <tspan x="90" dy="{0 if index == 0 else 42}">{escape(line)}</tspan>'
        for index, line in enumerate(lines[:3])
    )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630" viewBox="0 0 1200 630" role="img" aria-label="{title}">
  <rect width="1200" height="630" fill="#0f172a"/>
  <rect x="54" y="54" width="1092" height="522" rx="8" fill="#f8fafc" stroke="#cbd5e1" stroke-width="2"/>
  <text x="90" y="132" font-family="{FONT_FAMILY}" font-size="26" font-weight="800" fill="#2563eb">visual-architecture / {mode}</text>
  <text x="90" y="238" font-family="{FONT_FAMILY}" font-size="58" font-weight="800" fill="#0f172a">{title}</text>
  <text x="90" y="310" font-family="{FONT_FAMILY}" font-size="30" font-weight="500" fill="#334155">
{summary_svg}
  </text>
  <rect x="90" y="482" width="330" height="52" rx="8" fill="#dbeafe"/>
  <text x="114" y="516" font-family="{FONT_FAMILY}" font-size="22" font-weight="700" fill="#1d4ed8">source: {source}</text>
  <text x="820" y="516" font-family="{FONT_FAMILY}" font-size="22" font-weight="700" fill="#475569">validated local artifact</text>
</svg>
'''


def handle_share_card(args):
    data = load(args.input)
    validation = validate(data)
    if not validation["ok"]:
        print_json({"ok": False, "validation": validation})
        return 1
    write_atomic(args.output, render_share_card(data, args.input))
    print_json({"ok": True, "output": args.output, "sha256": file_sha256(args.output)})
    return 0


def handle_gallery(args):
    output_path = Path(args.output)
    link_prefix = "" if output_path.parent == Path(".") else "../"
    rows = []
    for spec_path in sorted(Path("examples").glob("*.json")):
        if spec_path.name.endswith(".receipt.json") or spec_path.name.endswith("-before.json") or spec_path.name.endswith("-head.json"):
            continue
        data = load(spec_path)
        name = spec_path.stem
        rows.append({
            "title": data.get("title", name),
            "summary": data.get("summary", "Generated local architecture artifact."),
            "mode": spec_mode(data),
            "theme": spec_theme(data),
            "story": data.get("story", []),
            "evidenceCount": sum(len(evidence_items(node)) for node in data.get("nodes", []) if isinstance(node, dict)) + sum(len(evidence_items(edge)) for edge in data.get("edges", []) if isinstance(edge, dict)),
            "spec": spec_path,
            "html": Path("examples") / f"{name}.html",
            "svg": Path("examples") / f"{name}.svg",
            "share": Path("examples") / f"{name}.share-card.svg",
            "receipt": Path("examples") / f"{name}.html.receipt.json",
        })

    rows.sort(key=lambda row: ("Case Study" not in row["title"], row["theme"] != "showcase", row["mode"], row["title"]))
    showcase = [row for row in rows if row["theme"] == "showcase"]
    featured = showcase or rows[:3]
    gallery_payload = script_json([
        {
            "title": row["title"],
            "summary": row["summary"],
            "mode": row["mode"],
            "theme": row["theme"],
            "story": row["story"],
            "evidenceCount": row["evidenceCount"],
            "spec": f"{link_prefix}{row['spec']}",
            "html": f"{link_prefix}{row['html']}",
            "svg": f"{link_prefix}{row['svg']}",
            "share": f"{link_prefix}{row['share']}",
            "receipt": f"{link_prefix}{row['receipt']}",
        }
        for row in rows
    ])
    featured_names = {row["title"] for row in featured[:3]}
    rows_html = "\n".join(
        f'''        <tr>
          <td><strong>{escape(row["title"])}</strong><span>{escape(row["summary"])}</span></td>
          <td>{escape(row["mode"])}</td>
          <td>{escape(row["theme"])}</td>
          <td><a href="{escape(link_prefix + str(row["html"] ))}">HTML</a></td>
          <td><a href="{escape(link_prefix + str(row["svg"] ))}">SVG</a></td>
          <td><a href="{escape(link_prefix + str(row["spec"] ))}">JSON</a></td>
          <td><a href="{escape(link_prefix + str(row["receipt"] ))}">Receipt</a></td>
        </tr>'''
        for row in rows
    )
    html = f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>visual-architecture gallery</title>
  <style>
    :root {{
      --bg: #070a10;
      --surface: #10151f;
      --surface-2: #141b29;
      --surface-3: #0b111a;
      --border: #263241;
      --text: #edf3fb;
      --muted: #98a6b8;
      --primary: #5eb6ff;
      --accent: #f5b84b;
      --teal: #60d8c8;
      --risk: #fb7185;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      background: var(--bg);
      color: var(--text);
      font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Helvetica Neue", sans-serif;
      line-height: 1.45;
      overflow-x: hidden;
    }}
    a {{ color: var(--primary); font-weight: 650; text-decoration: none; }}
    a:hover {{ text-decoration: underline; }}
    button {{ font: inherit; }}
    main {{ max-width: 1440px; margin: 0 auto; padding: 18px 18px 48px; }}
    header {{
      display: grid;
      grid-template-columns: minmax(0, 1fr) auto;
      gap: 18px;
      align-items: end;
      border-bottom: 1px solid var(--border);
      padding: 12px 0 18px;
      margin-bottom: 18px;
    }}
    h1 {{ margin: 0 0 7px; font-size: clamp(32px, 4.8vw, 68px); line-height: 0.98; letter-spacing: 0; }}
    header p {{ max-width: 780px; margin: 0; color: var(--muted); font-size: 16px; }}
    .actions {{ display: flex; flex-wrap: wrap; gap: 10px; justify-content: flex-end; }}
    .actions a, .links a {{
      display: inline-flex;
      align-items: center;
      min-height: 36px;
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 7px 11px;
      background: var(--surface-2);
    }}
    .studio {{
      display: grid;
      grid-template-columns: minmax(0, 1fr) 310px;
      gap: 14px;
      max-width: 100%;
      overflow: hidden;
    }}
    .rail, .stage, .details, .index, .journey {{
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 8px;
    }}
    .rail, .details {{ padding: 14px; }}
    .rail {{ grid-column: 1 / -1; }}
    .studio > * {{ min-width: 0; }}
    .rail h2, .details h2, .index h2 {{ margin: 0 0 12px; font-size: 15px; letter-spacing: 0; color: #f8fbff; }}
    .artifact-list {{
      display: flex;
      gap: 8px;
      max-width: 100%;
      overflow-x: auto;
      padding-bottom: 0;
      scrollbar-width: none;
      -ms-overflow-style: none;
      overscroll-behavior-x: contain;
      scroll-snap-type: x proximity;
    }}
    .artifact-list::-webkit-scrollbar {{ display: none; }}
    .artifact-button {{
      flex: 0 0 min(220px, 72vw);
      text-align: left;
      color: var(--text);
      background: var(--surface-3);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 10px;
      cursor: pointer;
      scroll-snap-align: start;
    }}
    .artifact-button:hover {{ border-color: #3d4c5f; }}
    .artifact-button[aria-pressed="true"] {{
      border-color: var(--primary);
      background: #0d1b2a;
    }}
    .artifact-button strong {{ display: block; font-size: 13px; line-height: 1.25; }}
    .artifact-button span {{ display: block; color: var(--muted); font-size: 12px; margin-top: 4px; }}
    .stage {{
      display: grid;
      grid-template-rows: auto minmax(0, 1fr);
      overflow: hidden;
      min-width: 0;
    }}
    .stage-bar {{
      display: flex;
      flex-wrap: wrap;
      justify-content: space-between;
      gap: 10px;
      align-items: center;
      padding: 12px 14px;
      border-bottom: 1px solid var(--border);
      background: var(--surface-2);
    }}
    .badges {{ display: flex; flex-wrap: wrap; gap: 8px; }}
    .badge {{
      border: 1px solid var(--border);
      border-radius: 999px;
      padding: 4px 8px;
      color: var(--muted);
      font-size: 12px;
      line-height: 1;
    }}
    .badge.accent {{ color: #1b1303; background: var(--accent); border-color: var(--accent); font-weight: 800; }}
    .stage-frame {{
      display: grid;
      place-items: start center;
      padding: 18px;
      min-height: 0;
      min-width: 0;
      background: #070a10;
    }}
    .stage-frame img {{
      display: block;
      width: 100%;
      max-width: 100%;
      max-height: 610px;
      height: auto;
      object-fit: contain;
      border-radius: 8px;
      background: #020617;
    }}
    .details {{ max-width: 100%; }}
    .details h2 {{ font-size: 26px; line-height: 1.08; margin-bottom: 10px; overflow-wrap: anywhere; word-break: break-word; }}
    .details p {{ color: var(--muted); margin: 0 0 18px; }}
    .story, .evidence-panel {{ margin-top: 18px; border-top: 1px solid var(--border); padding-top: 14px; }}
    .story ol {{ margin: 0; padding-left: 20px; color: var(--muted); }}
    .story li {{ margin: 0 0 9px; }}
    .story strong {{ display: block; color: var(--text); font-size: 13px; }}
    .evidence-list {{ display: grid; gap: 8px; margin-top: 10px; }}
    .evidence-item {{ border: 1px solid var(--border); border-radius: 8px; background: var(--surface-3); padding: 9px; color: var(--muted); font-size: 12px; overflow-wrap: anywhere; }}
    .evidence-item strong {{ color: var(--text); display: block; font-size: 13px; margin-bottom: 3px; }}
    .facts {{ display: grid; gap: 10px; margin: 18px 0; }}
    .fact {{
      display: grid;
      grid-template-columns: 92px 1fr;
      gap: 10px;
      padding-bottom: 10px;
      border-bottom: 1px solid var(--border);
      color: var(--muted);
      font-size: 13px;
    }}
    .fact strong {{ color: var(--text); font-weight: 700; }}
    .links {{ display: flex; flex-wrap: wrap; gap: 9px; margin-top: 18px; }}
    .journey {{ margin-bottom: 14px; padding: 16px; }}
    .journey-grid {{ display: grid; grid-template-columns: repeat(5, minmax(0, 1fr)); gap: 10px; }}
    .journey-step {{ border: 1px solid var(--border); border-radius: 8px; padding: 11px; background: var(--surface-3); }}
    .journey-step strong {{ display: block; margin-bottom: 5px; }}
    .journey-step span {{ color: var(--muted); font-size: 13px; }}
    .index {{ margin-top: 32px; }}
    .index {{ padding: 16px; }}
    .table-wrap {{ overflow-x: auto; border: 1px solid var(--border); border-radius: 8px; }}
    table {{ width: 100%; border-collapse: collapse; min-width: 920px; background: var(--surface-3); }}
    th, td {{ padding: 12px 14px; border-bottom: 1px solid var(--border); text-align: left; vertical-align: top; }}
    th {{ color: #f0f6fc; background: var(--surface-2); font-size: 13px; }}
    td {{ color: var(--text); font-size: 14px; }}
    td span {{ display: block; color: var(--muted); margin-top: 3px; max-width: 540px; }}
    tr:last-child td {{ border-bottom: 0; }}
    footer {{ margin-top: 18px; color: var(--muted); font-size: 13px; }}
    @media (max-width: 1100px) {{
      .studio {{ grid-template-columns: minmax(0, 1fr); }}
      .details {{ grid-column: 1 / -1; }}
    }}
    @media (max-width: 760px) {{
      main {{ padding: 14px 14px 40px; }}
      header, .studio {{ grid-template-columns: 1fr; }}
      .actions {{ justify-content: flex-start; }}
      .stage-bar {{ display: grid; justify-content: stretch; }}
      #stage-open {{ justify-self: start; }}
      .journey-grid {{ grid-template-columns: 1fr; }}
      .rail {{ order: 1; overflow: hidden; }}
      .stage {{ order: 2; max-width: calc(100vw - 28px); }}
      .details {{ order: 3; max-width: calc(100vw - 28px); }}
      .stage-frame {{ padding: 12px; overflow: hidden; }}
      .stage-frame img {{ max-height: 360px; }}
    }}
  </style>
</head>
<body>
  <main>
    <header>
      <div>
        <h1>visual-architecture</h1>
        <p>Generated architecture artifacts with mode-specific visual grammar, quality receipts, source evidence, and PR delta surfaces. This gallery is built from checked JSON examples that CI validates.</p>
      </div>
      <nav class="actions" aria-label="Project links">
        <a href="{link_prefix}README.md">README</a>
        <a href="{link_prefix}examples/showcase-artifact-engine.json">Hero spec</a>
        <a href="{link_prefix}docs/diagnostics.md">Diagnostics</a>
      </nav>
    </header>
    <section class="journey" aria-label="Generated artifact workflow">
      <h2>Repo to artifact</h2>
      <div class="journey-grid">
        <div class="journey-step"><strong>Extract</strong><span>Read repo files and attach source evidence.</span></div>
        <div class="journey-step"><strong>Layout</strong><span>Apply deterministic mode-aware placement.</span></div>
        <div class="journey-step"><strong>Validate</strong><span>Score quality, routes, density, and evidence.</span></div>
        <div class="journey-step"><strong>Bundle</strong><span>Write HTML, SVG, share card, receipt, and manifest.</span></div>
        <div class="journey-step"><strong>Review</strong><span>Open the gallery and inspect claims with receipts.</span></div>
      </div>
    </section>
    <section class="studio" aria-label="Interactive artifact viewer">
      <aside class="rail">
        <h2>Artifacts</h2>
        <div id="artifact-list" class="artifact-list"></div>
      </aside>
      <section class="stage" aria-live="polite">
        <div class="stage-bar">
          <div class="badges">
            <span id="mode-badge" class="badge">mode</span>
            <span id="theme-badge" class="badge">theme</span>
            <span id="feature-badge" class="badge accent">featured</span>
          </div>
          <a id="stage-open" href="#">Open artifact</a>
        </div>
        <div class="stage-frame">
          <img id="stage-image" src="" alt="">
        </div>
      </section>
      <aside class="details">
        <h2 id="detail-title">Artifact</h2>
        <p id="detail-summary"></p>
        <div class="facts">
          <div class="fact"><span>Mode</span><strong id="detail-mode"></strong></div>
          <div class="fact"><span>Quality</span><strong id="detail-quality">loading</strong></div>
          <div class="fact"><span>Evidence</span><strong id="detail-evidence-count"></strong></div>
          <div class="fact"><span>Source</span><strong id="detail-source"></strong></div>
        </div>
        <div class="links">
          <a id="detail-html" href="#">HTML</a>
          <a id="detail-svg" href="#">SVG</a>
          <a id="detail-spec" href="#">Spec</a>
          <a id="detail-receipt" href="#">Receipt</a>
          <a id="detail-share" href="#">Share card</a>
        </div>
        <div class="story">
          <h2>Story</h2>
          <ol id="story-list"></ol>
        </div>
        <div class="evidence-panel">
          <h2>Evidence Drilldown</h2>
          <div id="evidence-list" class="evidence-list"></div>
        </div>
      </aside>
    </section>
    <section class="index" aria-label="Artifact index">
      <h2>Checked Artifacts</h2>
      <div class="table-wrap">
        <table>
          <thead><tr><th>Artifact</th><th>Mode</th><th>Theme</th><th>HTML</th><th>SVG</th><th>Spec</th><th>Receipt</th></tr></thead>
          <tbody>
{rows_html}
          </tbody>
        </table>
      </div>
    </section>
    <footer>Generated by visual-architecture from local specs. No hosted editor, no repo upload, no hidden layout service.</footer>
  </main>
  <script>
    const artifacts = {gallery_payload};
    const featuredTitles = new Set({script_json(sorted(featured_names))});
    const list = document.getElementById("artifact-list");
    const stageImage = document.getElementById("stage-image");
    const stageOpen = document.getElementById("stage-open");
    const modeBadge = document.getElementById("mode-badge");
    const themeBadge = document.getElementById("theme-badge");
    const featureBadge = document.getElementById("feature-badge");
    const detailTitle = document.getElementById("detail-title");
    const detailSummary = document.getElementById("detail-summary");
    const detailMode = document.getElementById("detail-mode");
    const detailQuality = document.getElementById("detail-quality");
    const detailEvidenceCount = document.getElementById("detail-evidence-count");
    const detailSource = document.getElementById("detail-source");
    const detailHtml = document.getElementById("detail-html");
    const detailSvg = document.getElementById("detail-svg");
    const detailSpec = document.getElementById("detail-spec");
    const detailReceipt = document.getElementById("detail-receipt");
    const detailShare = document.getElementById("detail-share");
    const storyList = document.getElementById("story-list");
    const evidenceList = document.getElementById("evidence-list");
    const buttons = [];

    async function selectArtifact(index) {{
      const artifact = artifacts[index];
      buttons.forEach((button, buttonIndex) => {{
        button.setAttribute("aria-pressed", buttonIndex === index ? "true" : "false");
      }});
      stageImage.src = artifact.svg;
      stageImage.alt = artifact.title;
      stageOpen.href = artifact.html;
      modeBadge.textContent = artifact.mode;
      themeBadge.textContent = artifact.theme;
      featureBadge.hidden = !featuredTitles.has(artifact.title);
      detailTitle.textContent = artifact.title;
      detailSummary.textContent = artifact.summary;
      detailMode.textContent = artifact.mode + " / " + artifact.theme;
      detailEvidenceCount.textContent = String(artifact.evidenceCount || 0);
      detailSource.textContent = artifact.spec.replace(/^.*examples\//, "examples/");
      detailHtml.href = artifact.html;
      detailSvg.href = artifact.svg;
      detailSpec.href = artifact.spec;
      detailReceipt.href = artifact.receipt;
      detailShare.href = artifact.share;
      storyList.innerHTML = "";
      const story = artifact.story && artifact.story.length ? artifact.story : [{{title: "Spec", text: "Structured JSON defines the claim."}}, {{title: "Validate", text: "Local checks score quality and evidence."}}, {{title: "Deliver", text: "SVG, HTML, and receipt are generated together."}}];
      story.forEach((step) => {{
        const li = document.createElement("li");
        li.innerHTML = "<strong></strong><span></span>";
        li.querySelector("strong").textContent = step.title || "Step";
        li.querySelector("span").textContent = step.text || "";
        storyList.appendChild(li);
      }});
      evidenceList.innerHTML = "<div class='evidence-item'>Loading receipt and spec evidence.</div>";
      detailQuality.textContent = "loading";
      try {{
        const [specResponse, receiptResponse] = await Promise.all([fetch(artifact.spec), fetch(artifact.receipt)]);
        const [spec, receipt] = await Promise.all([specResponse.json(), receiptResponse.json()]);
        const quality = receipt.validation && receipt.validation.metrics && receipt.validation.metrics.quality;
        detailQuality.textContent = quality ? quality.rating + " / " + quality.score : "unscored";
        const evidence = [];
        (spec.nodes || []).forEach((node) => {{
          const items = Array.isArray(node.evidence) ? node.evidence : node.evidence ? [node.evidence] : [];
          items.forEach((item) => evidence.push({{owner: node.label || node.id, item}}));
        }});
        (spec.edges || []).forEach((edge) => {{
          const items = Array.isArray(edge.evidence) ? edge.evidence : edge.evidence ? [edge.evidence] : [];
          items.forEach((item) => evidence.push({{owner: (edge.from || "edge") + " -> " + (edge.to || "edge"), item}}));
        }});
        evidenceList.innerHTML = "";
        (evidence.length ? evidence : [{{owner: "No source evidence", item: {{source: "This artifact is structural only."}}}}]).slice(0, 8).forEach((entry) => {{
          const div = document.createElement("div");
          div.className = "evidence-item";
          const line = entry.item.lines ? ":" + entry.item.lines.join("-") : entry.item.line ? ":" + entry.item.line : "";
          div.innerHTML = "<strong></strong><span></span>";
          div.querySelector("strong").textContent = entry.owner;
          const rule = entry.item.rule ? " / " + entry.item.rule : "";
          const sourceType = entry.item.sourceType ? " / " + entry.item.sourceType : "";
          div.querySelector("span").textContent = (entry.item.source || "unknown") + line + sourceType + (entry.item.confidence ? " / " + entry.item.confidence : "") + rule;
          evidenceList.appendChild(div);
        }});
      }} catch (error) {{
        detailQuality.textContent = "unavailable";
        evidenceList.innerHTML = "<div class='evidence-item'>Could not load local JSON receipt in this browser context.</div>";
      }}
    }}

    artifacts.forEach((artifact, index) => {{
      const button = document.createElement("button");
      button.type = "button";
      button.className = "artifact-button";
      button.innerHTML = "<strong></strong><span></span>";
      button.querySelector("strong").textContent = artifact.title;
      button.querySelector("span").textContent = artifact.mode + " / " + artifact.theme;
      button.addEventListener("click", () => {{ selectArtifact(index); }});
      list.appendChild(button);
      buttons.push(button);
    }});

    const firstShowcase = artifacts.findIndex((artifact) => artifact.theme === "showcase");
    selectArtifact(firstShowcase >= 0 ? firstShowcase : 0);
  </script>
</body>
</html>
'''
    write_atomic(args.output, html)
    print_json({"ok": True, "output": args.output, "artifacts": len(rows)})
    return 0




def handle_layout(args):
    data = load(args.input)
    laid_out = layout_spec(data, args.mode or spec_mode(data), theme=args.theme)
    validation = validate(laid_out)
    write_atomic(args.output, json.dumps(laid_out, indent=2, sort_keys=True) + "\n")
    print_json({"ok": validation["ok"], "output": args.output, "validation": validation})
    return 0 if validation["ok"] else 1


def handle_extract_repo(args):
    spec = extract_repo_spec(args.root, title=args.title, theme=args.theme)
    validation = validate(spec)
    write_atomic(args.output, json.dumps(spec, indent=2, sort_keys=True) + "\n")
    print_json({"ok": validation["ok"], "output": args.output, "validation": validation})
    return 0 if validation["ok"] else 1


def handle_extract_pr(args):
    spec = extract_pr_spec(args.base, args.head, root_path=args.root, theme=args.theme)
    validation = validate(spec)
    write_atomic(args.output, json.dumps(spec, indent=2, sort_keys=True) + "\n")
    print_json({"ok": validation["ok"], "output": args.output, "changedFiles": len(spec.get("delta", {}).get("changedFiles", [])), "validation": validation})
    return 0 if validation["ok"] else 1


def handle_bundle(args):
    data = load(args.input)
    validation = validate(data)
    min_quality = getattr(args, "min_quality", None)
    if not validation["ok"] or (min_quality and not quality_meets(validation, min_quality)):
        print_json({"ok": False, "reason": "validation" if not validation["ok"] else "quality.threshold", "validation": validation})
        return 1
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    stem = Path(args.input).stem
    svg_path = output_dir / f"{stem}.svg"
    html_path = output_dir / f"{stem}.html"
    card_path = output_dir / f"{stem}.share-card.svg"
    manifest_path = output_dir / f"{stem}.bundle.json"
    svg = render(data)
    write_atomic(svg_path, svg)
    write_atomic(html_path, render_html(data, svg, args.input))
    write_atomic(card_path, render_share_card(data, args.input))
    receipt = receipt_for(args.input, html_path, validation, "html")
    receipt_path = output_dir / f"{stem}.html.receipt.json"
    write_atomic(receipt_path, json.dumps(receipt, indent=2, sort_keys=True) + "\n")
    manifest = {
        "tool": "visual-architecture",
        "version": VERSION,
        "input": args.input,
        "artifacts": {"svg": str(svg_path), "html": str(html_path), "shareCard": str(card_path), "receipt": str(receipt_path)},
        "quality": validation.get("metrics", {}).get("quality", {}),
    }
    write_atomic(manifest_path, json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    print_json({"ok": True, "manifest": str(manifest_path), "quality": manifest["quality"]})
    return 0


def handle_render(args):
    data = load(args.input)
    validation = validate(data)
    if not validation["ok"]:
        print_json(validation)
        return 1
    svg = render(data)
    write_atomic(args.output, svg)
    return 0


def handle_deliver(args):
    data = load(args.input)
    validation = validate(data)
    if not validation["ok"]:
        print_json({"ok": False, "validation": validation})
        return 1
    min_quality = getattr(args, "min_quality", None)
    if min_quality and not quality_meets(validation, min_quality):
        print_json({"ok": False, "reason": "quality.threshold", "minimum": min_quality, "validation": validation})
        return 1

    svg = render(data)
    output_path = Path(args.output)
    artifact_kind = "html" if output_path.suffix.lower() == ".html" else "svg"
    artifact = render_html(data, svg, args.input) if artifact_kind == "html" else svg
    write_atomic(output_path, artifact)

    receipt_path = Path(args.receipt) if args.receipt else output_path.with_suffix(output_path.suffix + ".receipt.json")
    receipt = receipt_for(args.input, output_path, validation, artifact_kind)
    write_atomic(receipt_path, json.dumps(receipt, indent=2, sort_keys=True) + "\n")
    print_json(receipt if args.json else {"ok": True, "output": str(output_path), "receipt": str(receipt_path)})
    return 0


def indent(text, spaces):
    prefix = " " * spaces
    return "\n".join(prefix + line if line else line for line in text.splitlines())


def main():
    parser = argparse.ArgumentParser(description="Validate and render visual-architecture JSON artifacts")
    subparsers = parser.add_subparsers(dest="command")

    validate_parser = subparsers.add_parser("validate", help="Validate architecture JSON")
    validate_parser.add_argument("input", help="Path to architecture JSON")
    validate_parser.add_argument("--json", action="store_true", help="Emit the full machine receipt")
    validate_parser.set_defaults(func=handle_validate)

    render_parser = subparsers.add_parser("render", help="Render architecture JSON to SVG")
    render_parser.add_argument("input", help="Path to architecture JSON")
    render_parser.add_argument("output", help="Path to output SVG")
    render_parser.set_defaults(func=handle_render)

    deliver_parser = subparsers.add_parser("deliver", help="Validate, render, and write a receipt")
    deliver_parser.add_argument("input", help="Path to architecture JSON")
    deliver_parser.add_argument("output", help="Path to output SVG or HTML")
    deliver_parser.add_argument("--receipt", help="Path to output receipt JSON")
    deliver_parser.add_argument("--min-quality", choices=sorted(QUALITY_ORDER), help="Fail delivery unless the quality rating meets this threshold")
    deliver_parser.add_argument("--json", action="store_true", help="Print the full delivery receipt")
    deliver_parser.set_defaults(func=handle_deliver)

    compare_parser = subparsers.add_parser("compare", help="Compare base/head specs and deliver a PR delta artifact")
    compare_parser.add_argument("base", help="Base architecture JSON")
    compare_parser.add_argument("head", help="Head architecture JSON")
    compare_parser.add_argument("output", help="Path to output SVG or HTML")
    compare_parser.add_argument("--spec", help="Optional path to write generated delta spec JSON")
    compare_parser.add_argument("--receipt", help="Path to output receipt JSON")
    compare_parser.add_argument("--json", action="store_true", help="Print the full delta receipt")
    compare_parser.set_defaults(func=handle_compare)

    card_parser = subparsers.add_parser("share-card", help="Generate a static 1200x630 SVG share card")
    card_parser.add_argument("input", help="Path to architecture JSON")
    card_parser.add_argument("output", help="Path to output share-card SVG")
    card_parser.set_defaults(func=handle_share_card)

    gallery_parser = subparsers.add_parser("gallery", help="Generate a static proof gallery")
    gallery_parser.add_argument("output", help="Path to output gallery HTML")
    gallery_parser.set_defaults(func=handle_gallery)

    layout_parser = subparsers.add_parser("layout", help="Apply deterministic mode-aware layout to a spec")
    layout_parser.add_argument("input", help="Path to input JSON")
    layout_parser.add_argument("output", help="Path to output JSON")
    layout_parser.add_argument("--mode", choices=sorted(ALLOWED_MODES), help="Override the spec mode before layout")
    layout_parser.add_argument("--theme", choices=sorted(ALLOWED_THEMES), help="Override the output theme")
    layout_parser.set_defaults(func=handle_layout)

    extract_repo_parser = subparsers.add_parser("extract-repo", help="Extract a first architecture spec from a local repo")
    extract_repo_parser.add_argument("root", help="Repository root to scan")
    extract_repo_parser.add_argument("--output", required=True, help="Path to output spec JSON")
    extract_repo_parser.add_argument("--title", help="Override generated artifact title")
    extract_repo_parser.add_argument("--theme", choices=sorted(ALLOWED_THEMES), default="showcase", help="Output theme")
    extract_repo_parser.set_defaults(func=handle_extract_repo)

    extract_pr_parser = subparsers.add_parser("extract-pr", help="Extract a PR delta spec from git changed files")
    extract_pr_parser.add_argument("--base", default="origin/master", help="Base git ref")
    extract_pr_parser.add_argument("--head", default="HEAD", help="Head git ref")
    extract_pr_parser.add_argument("--root", default=".", help="Repository root")
    extract_pr_parser.add_argument("--output", required=True, help="Path to output PR delta spec JSON")
    extract_pr_parser.add_argument("--theme", choices=sorted(ALLOWED_THEMES), default="showcase", help="Output theme")
    extract_pr_parser.set_defaults(func=handle_extract_pr)

    bundle_parser = subparsers.add_parser("bundle", help="Generate HTML, SVG, share card, receipt, and manifest together")
    bundle_parser.add_argument("input", help="Path to input JSON")
    bundle_parser.add_argument("output_dir", help="Directory for exported artifact bundle")
    bundle_parser.add_argument("--min-quality", choices=sorted(QUALITY_ORDER), help="Fail bundle unless the quality rating meets this threshold")
    bundle_parser.set_defaults(func=handle_bundle)

    # Backwards-compatible v0.2 CLI:
    #   render_architecture.py input.json output.svg
    args, unknown = parser.parse_known_args()
    if args.command is None and len(unknown) == 2:
        args = argparse.Namespace(input=unknown[0], output=unknown[1], func=handle_render)
    elif args.command is None:
        parser.print_help()
        raise SystemExit(2)

    raise SystemExit(args.func(args))


if __name__ == "__main__":
    main()

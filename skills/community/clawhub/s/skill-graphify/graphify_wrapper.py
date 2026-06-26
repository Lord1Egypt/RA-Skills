#!/usr/bin/env python3
"""
graphify_wrapper.py — Platform-agnostic wrapper for graphify CLI.
Handles install, build, query, and report reading.
Works on Windows (CMD), Linux, macOS — no bash-isms.
"""

import subprocess
import sys
import os
import json
from pathlib import Path

GRAPHIFY_PKG = "graphifyy"


def _run(cmd, **kwargs):
    """Run a command, return CompletedProcess."""
    return subprocess.run(cmd, capture_output=True, text=True, timeout=kwargs.pop("timeout", 120), **kwargs)


def ensure_installed():
    """Ensure graphify is installed, install if missing. Returns python path."""
    # Try importing graphify
    r = _run([sys.executable, "-c", "import graphify"])
    if r.returncode == 0:
        return sys.executable

    # Install
    print(f"Installing {GRAPHIFY_PKG}...")
    r = _run([sys.executable, "-m", "pip", "install", "-q", GRAPHIFY_PKG], timeout=120)
    if r.returncode != 0:
        print(f"Install failed: {r.stderr}")
        sys.exit(1)

    # Verify
    r = _run([sys.executable, "-c", "import graphify"])
    if r.returncode != 0:
        print("Install succeeded but import failed")
        sys.exit(1)

    return sys.executable


def find_graphify_cli():
    """Find graphify executable. Returns path or None."""
    r = _run(["graphify", "--help"])
    if r.returncode == 0:
        return "graphify"
    return None


def detect(target_path):
    """Run graphify detect on a path. Returns dict."""
    r = _run(
        [sys.executable, "-c",
         f"import json; from graphify.detect import detect; from pathlib import Path; "
         f"r=detect(Path({str(target_path)!r})); print(json.dumps(r))"],
        timeout=30
    )
    if r.returncode != 0:
        print(f"Detect failed: {r.stderr}")
        return None
    try:
        return json.loads(r.stdout.strip().split("\n")[-1])
    except (json.JSONDecodeError, IndexError):
        print(f"Could not parse detect output: {r.stdout}")
        return None


def build(target_path, output_dir=None, update=False):
    """
    Build knowledge graph from target_path.
    
    This uses graphify's Python API directly (extract → build → cluster → export)
    to avoid bash-isms in the CLI skill.md orchestration.
    """
    target = Path(target_path).resolve()
    out = Path(output_dir) if output_dir else target / "graphify-out"
    out.mkdir(parents=True, exist_ok=True)

    python = ensure_installed()

    # Step 1: Detect files
    print(f"Detecting files in {target}...")
    info = detect(str(target))
    if not info:
        print("Detection failed.")
        sys.exit(1)

    total = info.get("total_files", 0)
    words = info.get("total_words", 0)
    print(f"Corpus: {total} files, ~{words} words")

    file_types = []
    for cat in ("code", "docs", "papers", "images"):
        count = len(info.get("files", {}).get(cat, []))
        if count:
            file_types.append(f"  {cat}: {count} files")
    if file_types:
        print("\n".join(file_types))

    if total == 0:
        print(f"No supported files found in {target}")
        sys.exit(1)

    # Step 2: AST extraction (code)
    print("Running AST extraction...")
    ast_script = (
        "import json, sys\n"
        "from graphify.extract import collect_files, extract\n"
        "from pathlib import Path\n"
        f"detect_data = json.loads(Path({str(out / '.graphify_detect.json')!r}).read_text())\n"
        "code_files = []\n"
        "for f in detect_data.get('files', {}).get('code', []):\n"
        "    p = Path(f)\n"
        "    code_files.extend(collect_files(p) if p.is_dir() else [p])\n"
        "if code_files:\n"
        "    result = extract(code_files)\n"
        f"    Path({str(out / '.graphify_ast.json')!r}).write_text(json.dumps(result, indent=2))\n"
        "    print(f'AST: {len(result[\"nodes\"])} nodes, {len(result[\"edges\"])} edges')\n"
        "else:\n"
        "    print('No code files - skipping AST')\n"
    )

    # Save detect info for AST step
    (out / ".graphify_detect.json").write_text(json.dumps(info, indent=2))

    r = _run([python, "-c", ast_script], cwd=str(target), timeout=120)
    if r.returncode == 0 and r.stdout.strip():
        print(r.stdout.strip())
    elif r.returncode != 0:
        print(f"AST extraction warning: {r.stderr.strip()}")

    # Step 3: Build graph using graphify's build module
    print("Building knowledge graph...")
    build_script = (
        "import json\n"
        "from graphify.build import build_graph\n"
        "from pathlib import Path\n"
        f"ast_path = Path({str(out / '.graphify_ast.json')!r})\n"
        "ast_data = json.loads(ast_path.read_text()) if ast_path.exists() else {'nodes': [], 'edges': []}\n"
        f"graph = build_graph(ast_data['nodes'], ast_data['edges'])\n"
        f"Path({str(out / 'graph.json')!r}).write_text(json.dumps(graph, indent=2, ensure_ascii=False))\n"
        "print(f'Graph: {len(graph.get(\"nodes\", []))} nodes, {len(graph.get(\"edges\", []))} edges')\n"
    )

    r = _run([python, "-c", build_script], cwd=str(target), timeout=120)
    if r.returncode != 0:
        # Fallback: try CLI directly
        print("Build via API failed, trying CLI...")
        cli = find_graphify_cli()
        if cli:
            r = _run([cli, str(target)], cwd=str(target), timeout=300)
            if r.returncode == 0:
                print("Graph built via CLI.")
                return
        print(f"Build failed: {r.stderr}")
        sys.exit(1)

    if r.stdout.strip():
        print(r.stdout.strip())

    # Step 4: Export report
    print("Generating report...")
    report_script = (
        "import json\n"
        "from graphify.report import generate_report\n"
        "from pathlib import Path\n"
        f"graph_data = json.loads(Path({str(out / 'graph.json')!r}).read_text())\n"
        "report = generate_report(graph_data)\n"
        f"Path({str(out / 'GRAPH_REPORT.md')!r}).write_text(report, encoding='utf-8')\n"
        "print('Report generated.')\n"
    )

    r = _run([python, "-c", report_script], cwd=str(target), timeout=60)
    if r.returncode != 0:
        print(f"Report warning: {r.stderr.strip()}")
    elif r.stdout.strip():
        print(r.stdout.strip())

    print(f"\nDone! Output in {out}")
    print(f"  graph.html      — interactive visualization")
    print(f"  GRAPH_REPORT.md — plain-language audit report")
    print(f"  graph.json      — queryable knowledge graph")


def query(question, graph_path=None, budget=2000, dfs=False):
    """Query an existing graph."""
    cli = find_graphify_cli()
    gpath = graph_path or "graphify-out/graph.json"

    if not Path(gpath).exists():
        print(f"Graph not found at {gpath}. Run build first.")
        sys.exit(1)

    if cli:
        cmd = [cli, "query", question, "--graph", gpath, "--budget", str(budget)]
        if dfs:
            cmd.append("--dfs")
        r = _run(cmd, timeout=30)
        print(r.stdout)
        if r.stderr:
            print(r.stderr, file=sys.stderr)
        return

    # Fallback: Python API
    print("CLI not found, using Python API for query...")
    q_script = (
        "import json, sys\n"
        "from graphify.query import query_graph\n"
        f"graph = json.loads(open({gpath!r}, encoding='utf-8').read())\n"
        f"result = query_graph(graph, {question!r}, budget={budget})\n"
        "print(result)\n"
    )
    r = _run([sys.executable, "-c", q_script], timeout=30)
    print(r.stdout if r.returncode == 0 else r.stderr)


def read_report(graph_path=None):
    """Read and print the GRAPH_REPORT.md."""
    gdir = Path(graph_path).parent if graph_path else Path("graphify-out")
    report = gdir / "GRAPH_REPORT.md"
    if report.exists():
        print(report.read_text(encoding="utf-8"))
    else:
        print(f"No report found at {report}")


def main():
    if len(sys.argv) < 2:
        print("Usage: graphify_wrapper.py <command> [args]")
        print("Commands: build <path>, query <question>, report, ensure-installed")
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "build":
        target = sys.argv[2] if len(sys.argv) > 2 else "."
        build(target)
    elif cmd == "query":
        if len(sys.argv) < 3:
            print("Usage: graphify_wrapper.py query <question>")
            sys.exit(1)
        question = " ".join(sys.argv[2:])
        query(question)
    elif cmd == "report":
        read_report()
    elif cmd == "ensure-installed":
        ensure_installed()
        print("graphify is installed.")
    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)


if __name__ == "__main__":
    main()

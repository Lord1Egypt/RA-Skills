---
name: thoth
description: "Thoth Standard -- Auto-Documentation Engine. Reads your entire project and generates README, API reference, and usage guide. Saved to .md files."
version: "1.0.0"
metadata:
  openclaw:
    requires:
      env: [PROJECT_PATH, LICENSE_KEY]
      bins: [python3, pip3]
    primaryEnv: PROJECT_PATH
    emoji: "📜📖"
    homepage: https://clawhub.ai/occupythemilkyway/thoth
    tags: [documentation, readme, api-reference, code, autodoc, developer, standard, thoth]
    envVars:
      - name: LICENSE_KEY
        required: true
        description: "Your Thoth Standard license key. Get one at: ko-fi.com/occupythemilkyway"
      - name: PROJECT_PATH
        required: true
        description: "Path to the project folder to document"
      - name: PROJECT_NAME
        required: false
        description: "Project name override (default: folder name)"
        default: ""
      - name: OUTPUT_DIR
        required: false
        description: "Directory to save docs (default: ./docs)"
        default: "./docs"
---

# Thoth Standard -- Auto-Documentation Engine

Full project documentation in minutes. README, API reference, usage guide -- all saved to files.

---

## Step 1 -- Install

```bash
pip3 install rich --break-system-packages --quiet
```

---

## Step 2 -- Validate and scan

```python
import os, sys, ast
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.tree import Tree
from rich.table import Table
from rich import box

console = Console()

LICENSE_KEY = os.environ.get("LICENSE_KEY", "").strip()
if not LICENSE_KEY or not LICENSE_KEY.startswith("THOTH-STD-"):
    console.print(Panel(
        "[red bold]Thoth Standard requires a license key.[/red bold]\n\n"
        "Get your key at: [bold cyan]ko-fi.com/occupythemilkyway[/bold cyan]\n\n"
        "Or use the free version: [dim]openclaw skills install thoth-lite[/dim]",
        title="License Required",
        border_style="red"
    ))
    sys.exit(1)

PROJECT_PATH = os.environ.get("PROJECT_PATH", "").strip()
PROJECT_NAME = os.environ.get("PROJECT_NAME", "").strip()
OUTPUT_DIR   = os.environ.get("OUTPUT_DIR", "./docs").strip()

if not PROJECT_PATH or not os.path.exists(PROJECT_PATH):
    console.print(Panel(f"[red]PROJECT_PATH not found: {PROJECT_PATH}[/red]", title="Error", border_style="red"))
    sys.exit(1)

if not PROJECT_NAME:
    PROJECT_NAME = os.path.basename(os.path.abspath(PROJECT_PATH))

os.makedirs(OUTPUT_DIR, exist_ok=True)

console.print()
console.print(Panel.fit(
    f"[bold cyan]📜 Thoth Standard -- Auto-Documentation[/bold cyan]\n"
    f"Project: [yellow]{PROJECT_NAME}[/yellow]\n"
    f"Path:    [dim]{PROJECT_PATH}[/dim]\n"
    f"Output:  [green]{OUTPUT_DIR}/[/green]",
    border_style="cyan"
))

SKIP_DIRS = {".git", "__pycache__", "node_modules", ".venv", "venv", "dist", "build", ".next", ".pytest_cache"}
CODE_EXTS  = {".py", ".js", ".ts", ".jsx", ".tsx", ".go", ".rs", ".java", ".rb", ".cs", ".cpp", ".c", ".sh"}
META_FILES = {"requirements.txt", "package.json", "pyproject.toml", "go.mod", "Cargo.toml", "setup.py", "setup.cfg"}

all_files, meta_files, functions = [], {}, []

for root, dirs, fnames in os.walk(PROJECT_PATH):
    dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
    for fname in fnames:
        full = os.path.join(root, fname)
        rel  = os.path.relpath(full, PROJECT_PATH)
        ext  = os.path.splitext(fname)[1].lower()
        if fname in META_FILES:
            try:
                with open(full, encoding="utf-8", errors="replace") as fh:
                    meta_files[fname] = fh.read(2000)
            except Exception:
                pass
        if ext in CODE_EXTS:
            all_files.append((rel, full, ext))

# Extract Python functions/classes for API reference
for rel, full, ext in all_files:
    if ext == ".py":
        try:
            with open(full, encoding="utf-8", errors="replace") as fh:
                source = fh.read()
            tree = ast.parse(source)
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                    doc = ast.get_docstring(node) or ""
                    args = []
                    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        args = [a.arg for a in node.args.args]
                    functions.append({
                        "file": rel, "name": node.name,
                        "type": "class" if isinstance(node, ast.ClassDef) else "function",
                        "args": args, "doc": doc[:200]
                    })
        except Exception:
            pass

tbl = Table(title=f"Project Scan: {PROJECT_NAME}", box=box.ROUNDED, border_style="cyan")
tbl.add_column("Metric", style="dim")
tbl.add_column("Value", style="yellow")
tbl.add_row("Code files", str(len(all_files)))
tbl.add_row("Python symbols", str(len(functions)))
tbl.add_row("Meta files", ", ".join(meta_files.keys()) or "none")
tbl.add_row("Output dir", OUTPUT_DIR)
console.print(tbl)

# Print file tree and contents for Claude
console.print("\n[bold]Project structure:[/bold]")
for rel, full, ext in sorted(all_files)[:30]:
    print(f"  {rel}")

console.print("\n[bold]File contents (for documentation):[/bold]")
for rel, full, ext in sorted(all_files)[:25]:
    try:
        with open(full, encoding="utf-8", errors="replace") as fh:
            content = fh.read(4000)
        print(f"\n=== {rel} ===\n{content}\n=== END {rel} ===")
    except Exception:
        pass

if functions:
    console.print("\n[bold]Extracted symbols:[/bold]")
    for fn in functions[:50]:
        args_str = ", ".join(fn["args"]) if fn["type"] == "function" else ""
        print(f"  [{fn['type']}] {fn['file']}::{fn['name']}({args_str}) -- {fn['doc'][:80]}")

for name, content in meta_files.items():
    print(f"\n=== META: {name} ===\n{content}\n=== END META ===")
```

---

## Step 3 -- Generate documentation

Based on the project scan above, generate three complete documents:

### Document 1: README.md
```
# [PROJECT_NAME]
> Tagline

## Overview
What it does, why it exists, who it's for. (3-4 paragraphs, thorough)

## Features
Bullet list of all features found in the code.

## Installation
Exact install steps based on the actual meta files found.

## Quick Start
Working code example.

## Usage
Detailed usage with multiple examples.

## Configuration
All config options, env vars, or settings found.

## Project Structure
File/folder explanations.

## License
```

### Document 2: API_REFERENCE.md
For every function, class, and method found in the scan:
```
# API Reference: [PROJECT_NAME]

## [module_name]

### `function_name(args)`
Description of what it does, parameters, return value, example.
```

### Document 3: USAGE_GUIDE.md
Practical, real-world usage guide with worked examples from the actual code.

---

## Step 4 -- Save and confirm

```python
import os
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box
console = Console()

# (Claude saves the 3 files above to OUTPUT_DIR using its file tool)
readme_path  = os.path.join(OUTPUT_DIR, "README.md")
api_path     = os.path.join(OUTPUT_DIR, "API_REFERENCE.md")
usage_path   = os.path.join(OUTPUT_DIR, "USAGE_GUIDE.md")

tbl = Table(title="Documentation Generated", box=box.SIMPLE, border_style="green")
tbl.add_column("File", style="cyan")
tbl.add_column("Description", style="dim")
tbl.add_row(readme_path,  "Project overview and install")
tbl.add_row(api_path,     "Full API reference")
tbl.add_row(usage_path,   "Practical usage guide")
console.print()
console.print(tbl)
console.print(Panel(
    "[bold green]Documentation complete![/bold green]\n\n"
    "Upgrade to [magenta]Thoth Pro ($9)[/magenta] for auto-injected docstrings, git CHANGELOG, and architecture docs.\n"
    "-> [cyan]ko-fi.com/occupythemilkyway[/cyan]",
    border_style="green"
))
```

Save all three documents to OUTPUT_DIR using your file writing tool, then display the confirmation panel.

---
name: thoth-pro
description: "Thoth Pro -- Full Auto-Documentation Suite. README + API reference + docstrings injected into source + CHANGELOG from git + architecture doc. The definitive docs tool on ClawHub."
version: "1.0.0"
metadata:
  openclaw:
    requires:
      env: [PROJECT_PATH, LICENSE_KEY]
      bins: [python3, pip3, git]
    primaryEnv: PROJECT_PATH
    emoji: "📜⚡"
    homepage: https://clawhub.ai/occupythemilkyway/thoth-pro
    tags: [documentation, readme, api-reference, docstrings, changelog, git, architecture, pro, thoth]
    envVars:
      - name: LICENSE_KEY
        required: true
        description: "Your Thoth Pro license key. Get one at: ko-fi.com/occupythemilkyway"
      - name: PROJECT_PATH
        required: true
        description: "Path to the project folder to document"
      - name: PROJECT_NAME
        required: false
        description: "Project name override"
        default: ""
      - name: OUTPUT_DIR
        required: false
        description: "Directory to save docs (default: ./docs)"
        default: "./docs"
      - name: INJECT_DOCSTRINGS
        required: false
        description: "Auto-inject docstrings into .py files: yes | no (default: yes)"
        default: "yes"
      - name: GENERATE_CHANGELOG
        required: false
        description: "Generate CHANGELOG from git log: yes | no (default: yes)"
        default: "yes"
---

# Thoth Pro -- Full Auto-Documentation Suite

The most complete documentation tool on ClawHub. Reads your entire codebase, generates professional docs, injects missing docstrings, and builds a CHANGELOG from your git history.

**Bundle deal:** All 5 Egyptian skills for $29 -> ko-fi.com/s/7625accf3f (save $16)

---

## Step 1 -- Install

```bash
pip3 install rich --break-system-packages --quiet
```

---

## Step 2 -- Validate and deep scan

```python
import os, sys, ast, subprocess, re
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.rule import Rule
from rich import box

console = Console()

LICENSE_KEY = os.environ.get("LICENSE_KEY", "").strip()
if not LICENSE_KEY or not LICENSE_KEY.startswith("THOTH-PRO-"):
    console.print(Panel(
        "[red bold]Thoth Pro requires a license key.[/red bold]\n\n"
        "Get your key at: [bold cyan]ko-fi.com/occupythemilkyway[/bold cyan]\n\n"
        "Or try Thoth Standard ($5): [dim]openclaw skills install thoth[/dim]",
        title="License Required",
        border_style="red"
    ))
    sys.exit(1)

PROJECT_PATH      = os.environ.get("PROJECT_PATH", "").strip()
PROJECT_NAME      = os.environ.get("PROJECT_NAME", "").strip()
OUTPUT_DIR        = os.environ.get("OUTPUT_DIR", "./docs").strip()
INJECT_DOCSTRINGS = os.environ.get("INJECT_DOCSTRINGS", "yes").lower().strip() == "yes"
GEN_CHANGELOG     = os.environ.get("GENERATE_CHANGELOG", "yes").lower().strip() == "yes"

if not PROJECT_PATH or not os.path.exists(PROJECT_PATH):
    console.print(Panel(f"[red]PROJECT_PATH not found: {PROJECT_PATH}[/red]", title="Error", border_style="red"))
    sys.exit(1)

if not PROJECT_NAME:
    PROJECT_NAME = os.path.basename(os.path.abspath(PROJECT_PATH))

os.makedirs(OUTPUT_DIR, exist_ok=True)

console.print()
console.print(Panel.fit(
    f"[bold cyan]📜 Thoth Pro -- Full Documentation Suite[/bold cyan]\n"
    f"Project:          [yellow]{PROJECT_NAME}[/yellow]\n"
    f"Inject docstrings: [white]{'Yes' if INJECT_DOCSTRINGS else 'No'}[/white]\n"
    f"Git changelog:     [white]{'Yes' if GEN_CHANGELOG else 'No'}[/white]\n"
    f"Output:           [green]{OUTPUT_DIR}/[/green]",
    border_style="cyan"
))

SKIP_DIRS = {".git", "__pycache__", "node_modules", ".venv", "venv", "dist", "build", ".next", ".pytest_cache"}
CODE_EXTS  = {".py", ".js", ".ts", ".jsx", ".tsx", ".go", ".rs", ".java", ".rb", ".cs", ".cpp", ".c", ".sh"}
META_FILES = {"requirements.txt", "package.json", "pyproject.toml", "go.mod", "Cargo.toml", "setup.py"}

all_files, meta_files, py_symbols, missing_docstrings = [], {}, [], []

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

# Deep Python analysis
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
                        args = [a.arg for a in node.args.args if a.arg != "self"]
                    sym = {"file": rel, "name": node.name, "args": args,
                           "type": "class" if isinstance(node, ast.ClassDef) else "function",
                           "doc": doc, "line": node.lineno}
                    py_symbols.append(sym)
                    if not doc and not node.name.startswith("_"):
                        missing_docstrings.append(sym)
        except Exception:
            pass

# Git changelog
git_log = ""
if GEN_CHANGELOG:
    try:
        result = subprocess.run(
            ["git", "-C", PROJECT_PATH, "log", "--oneline", "--no-merges", "-50"],
            capture_output=True, text=True, timeout=10
        )
        git_log = result.stdout.strip()
    except Exception:
        git_log = ""

tbl = Table(title=f"Deep Scan: {PROJECT_NAME}", box=box.ROUNDED, border_style="cyan")
tbl.add_column("Metric", style="dim")
tbl.add_column("Value", style="yellow")
tbl.add_row("Code files", str(len(all_files)))
tbl.add_row("Python symbols", str(len(py_symbols)))
tbl.add_row("Missing docstrings", str(len(missing_docstrings)))
tbl.add_row("Git commits found", str(len(git_log.splitlines())) if git_log else "No git history")
tbl.add_row("Output directory", OUTPUT_DIR)
console.print(tbl)

console.print(Rule("[cyan]File contents[/cyan]"))
for rel, full, ext in sorted(all_files)[:30]:
    try:
        with open(full, encoding="utf-8", errors="replace") as fh:
            content = fh.read(5000)
        print(f"\n=== {rel} ===\n{content}\n=== END {rel} ===")
    except Exception:
        pass

if git_log:
    console.print(Rule("[cyan]Git history[/cyan]"))
    print(git_log)

console.print(Rule("[cyan]Symbols missing docstrings[/cyan]"))
for sym in missing_docstrings[:40]:
    args_str = ", ".join(sym["args"])
    print(f"  {sym['file']}:{sym['line']} -- {sym['type']} {sym['name']}({args_str})")
```

---

## Step 3 -- Generate full documentation suite

Generate five documents based on everything scanned above:

**1. README.md** -- Complete project overview, install, usage, examples, config, structure, license
**2. API_REFERENCE.md** -- Every public function/class/method with parameters, return types, description, example
**3. USAGE_GUIDE.md** -- Practical guide with real-world worked examples and common patterns
**4. ARCHITECTURE.md** -- How the codebase is structured, key design decisions, data flow, module dependencies
**5. CHANGELOG.md** -- If git history was provided, group commits into version sections (Features / Fixes / Refactors)

For INJECT_DOCSTRINGS=yes: Also produce a JSON mapping of `{"file": "rel_path", "line": N, "docstring": "..."}` for every symbol in the missing_docstrings list. Claude will use this to inject docstrings.

Write everything with the depth and polish of a senior technical writer.

---

## Step 4 -- Save everything

```python
import os, json
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box
console = Console()

# (Claude saves all files to OUTPUT_DIR)
files_written = [
    (os.path.join(OUTPUT_DIR, "README.md"),        "Project overview"),
    (os.path.join(OUTPUT_DIR, "API_REFERENCE.md"), "Full API reference"),
    (os.path.join(OUTPUT_DIR, "USAGE_GUIDE.md"),   "Usage examples"),
    (os.path.join(OUTPUT_DIR, "ARCHITECTURE.md"),  "Architecture overview"),
    (os.path.join(OUTPUT_DIR, "CHANGELOG.md"),     "Version changelog"),
]

tbl = Table(title="Thoth Pro -- Documentation Complete", box=box.SIMPLE, border_style="green")
tbl.add_column("File", style="cyan")
tbl.add_column("Description", style="dim")
for path, desc in files_written:
    tbl.add_row(path, desc)
console.print()
console.print(tbl)
console.print(Panel(
    "[bold green]Full documentation suite generated.[/bold green]\n\n"
    f"[yellow]{len(files_written)} documents[/yellow] written to [cyan]{OUTPUT_DIR}[/cyan]\n"
    f"Symbols documented: [yellow]{len(py_symbols)}[/yellow]",
    border_style="green"
))
```

After generating all documents in Step 3, save each one to OUTPUT_DIR using your file writing tool.

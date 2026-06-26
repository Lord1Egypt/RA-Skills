---
name: thoth-lite
description: "Thoth Lite -- Auto-Documentation. Point Thoth at a file or folder and get a clean README instantly. Free tier."
version: "1.0.0"
metadata:
  openclaw:
    requires:
      env: [PROJECT_PATH]
      bins: [python3, pip3]
    primaryEnv: PROJECT_PATH
    emoji: "📜✍️"
    homepage: https://clawhub.ai/occupythemilkyway/thoth-lite
    tags: [documentation, readme, code, autodoc, developer, free, lite, thoth]
    envVars:
      - name: PROJECT_PATH
        required: true
        description: "Path to the file or folder to document (e.g. ./src or ./main.py)"
---

# Thoth Lite -- Auto-Documentation

Thoth, god of wisdom and writing, reads your code so you don't have to explain it.

## Free vs Standard vs Pro

| Feature | Thoth Lite (Free) | Thoth Standard ($5) | Thoth Pro ($9) |
|---------|------------------|--------------------|--------------------|
| Scope | Single file | Full project folder | Full project + git |
| Outputs | README only | README + API ref + usage | README + API + docstrings + CHANGELOG |
| Inline docstrings | No | No | Yes (auto-injected) |
| Git changelog | No | No | Yes (from git log) |
| Architecture doc | No | No | Yes |
| Save to files | No | Yes (.md) | Yes (.md + .docx) |

**Upgrade:** Thoth Standard -> ko-fi.com/occupythemilkyway ($5)
**Bundle:** All 5 Egyptian skills for $29 -> ko-fi.com/occupythemilkyway

---

## Step 1 -- Install

```bash
pip3 install rich --break-system-packages --quiet
```

---

## Step 2 -- Scan file/folder

```python
import os, sys
from rich.console import Console
from rich.panel import Panel
from rich.tree import Tree

console = Console()

PROJECT_PATH = os.environ.get("PROJECT_PATH", "").strip()
if not PROJECT_PATH:
    console.print(Panel("[red]PROJECT_PATH is required.[/red]\nSet it to a file or folder path.", title="Setup Error", border_style="red"))
    sys.exit(1)

if not os.path.exists(PROJECT_PATH):
    console.print(Panel(f"[red]Path not found:[/red] {PROJECT_PATH}", title="Error", border_style="red"))
    sys.exit(1)

console.print()
console.print(Panel.fit(
    f"[bold cyan]📜 Thoth Lite -- Auto-Documentation[/bold cyan]\n"
    f"Target: [yellow]{PROJECT_PATH}[/yellow]\n"
    f"[dim]Free tier -- single file or folder README[/dim]",
    border_style="cyan"
))

# Collect files
files = []
if os.path.isfile(PROJECT_PATH):
    files = [PROJECT_PATH]
else:
    SKIP_DIRS = {".git", "__pycache__", "node_modules", ".venv", "venv", "dist", "build", ".next"}
    CODE_EXTS  = {".py", ".js", ".ts", ".jsx", ".tsx", ".go", ".rs", ".java", ".rb", ".cs", ".cpp", ".c", ".sh", ".yaml", ".yml", ".toml", ".json", ".md"}
    tree = Tree(f"[bold]{PROJECT_PATH}[/bold]")
    for root, dirs, fnames in os.walk(PROJECT_PATH):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        rel = os.path.relpath(root, PROJECT_PATH)
        branch = tree if rel == "." else tree.add(f"[dim]{rel}[/dim]")
        for fname in sorted(fnames):
            ext = os.path.splitext(fname)[1].lower()
            if ext in CODE_EXTS:
                full = os.path.join(root, fname)
                files.append(full)
                branch.add(f"[green]{fname}[/green]")
    console.print(tree)

console.print(f"\n[bold]Files found:[/bold] [yellow]{len(files)}[/yellow]")
console.print("[dim]Reading files for documentation...[/dim]\n")

# Read file contents for Claude
for f in files[:20]:  # Lite: up to 20 files
    try:
        with open(f, encoding="utf-8", errors="replace") as fh:
            content = fh.read(3000)  # first 3000 chars
        rel = os.path.relpath(f, PROJECT_PATH if os.path.isdir(PROJECT_PATH) else os.path.dirname(PROJECT_PATH))
        print(f"\n=== FILE: {rel} ===")
        print(content)
        print(f"=== END {rel} ===\n")
    except Exception:
        pass
```

---

## Step 3 -- Generate README

Based on the files shown above, write a clean professional README.md with this structure:

```
# [Project Name]

> One-sentence description of what this project does.

## Overview
2-3 paragraphs explaining what the project does, why it exists, and who it's for.

## Features
- Feature 1
- Feature 2
- Feature 3

## Installation
Step-by-step install instructions based on the actual files (package.json, requirements.txt, etc.).

## Usage
Practical examples showing how to actually use it.

## Project Structure
Brief explanation of the key files/folders.

## Contributing
Simple contributing guide.

## License
License info if found, otherwise leave a placeholder.
```

---

## Step 4 -- Upsell

```python
from rich.console import Console
from rich.panel import Panel
console = Console()
console.print()
console.print(Panel(
    "[dim]Thoth Lite generates a README for one file or folder.\n\n[/dim]"
    "[bold cyan]Thoth Standard ($5)[/bold cyan] adds an API reference, usage examples, and saves everything to .md files.\n"
    "[bold magenta]Thoth Pro ($9)[/bold magenta] adds auto-injected docstrings, git changelog, architecture diagrams, and .docx export.\n\n"
    "Upgrade: [bold cyan]ko-fi.com/occupythemilkyway[/bold cyan]",
    title="[cyan]Want full documentation?[/cyan]",
    border_style="cyan"
))
```

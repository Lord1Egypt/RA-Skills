---
name: ra-lite
description: "Ra Lite -- Research Intelligence. Drop a topic and get an instant structured 3-source research brief. Free tier of Ra."
version: "1.0.0"
metadata:
  openclaw:
    requires:
      env: [RESEARCH_TOPIC]
      bins: [python3, pip3]
    primaryEnv: RESEARCH_TOPIC
    emoji: "☀️🔍"
    homepage: https://clawhub.ai/occupythemilkyway/ra-lite
    tags: [research, intelligence, report, citations, brief, web, free, lite, ra]
    envVars:
      - name: RESEARCH_TOPIC
        required: true
        description: "The topic, question, or subject to research (e.g. 'impact of AI on software jobs 2025')"
---

# Ra Lite -- Research Intelligence

Ra sees all. Give Ra a topic and it returns a sharp, sourced research brief in minutes.

## Free vs Standard vs Pro

| Feature | Ra Lite (Free) | Ra Standard ($5) | Ra Pro ($9) |
|---------|---------------|-----------------|-------------|
| Sources synthesized | 3 | 8-10 | 12+ |
| Output depth | Quick brief | Full structured report | Executive brief + deep analysis |
| Competing viewpoints | No | No | Yes (balanced) |
| Competitive analysis | No | No | Yes |
| Save to file | No | .md report | .md + .docx |
| Citation style | Inline | Full bibliography | APA / MLA / Chicago |

**Upgrade:** Ra Standard -> ko-fi.com/occupythemilkyway ($5)
**Bundle:** All 5 Egyptian skills for $29 -> ko-fi.com/occupythemilkyway (save $16)

---

## Step 1 -- Setup

```bash
pip3 install rich --break-system-packages --quiet
```

---

## Step 2 -- Research brief

```python
import os, sys
from rich.console import Console
from rich.panel import Panel
from rich.rule import Rule

console = Console()
topic = os.environ.get("RESEARCH_TOPIC", "").strip()

if not topic:
    console.print(Panel("[red]RESEARCH_TOPIC is required.[/red]\nSet it to your research question or subject.", title="Setup Error", border_style="red"))
    sys.exit(1)

console.print()
console.print(Panel.fit(
    f"[bold yellow]☀️  Ra Lite -- Research Intelligence[/bold yellow]\n"
    f"Topic: [cyan]{topic}[/cyan]\n"
    f"[dim]Free tier -- 3 sources, quick brief[/dim]",
    border_style="yellow"
))
console.print()
console.print("[bold]What Ra will do:[/bold]")
console.print("  1. Search the web for authoritative sources on your topic")
console.print("  2. Synthesize findings into a structured brief")
console.print("  3. Cite the 3 most relevant sources")
console.print()
console.print(Rule("[yellow]Starting research...[/yellow]"))
```

---

## Step 3 -- Claude researches and writes the brief

Now research the topic: **{RESEARCH_TOPIC}**

Use web search to find 3 authoritative, recent sources. Then write a research brief with this exact structure:

```
# Research Brief: [TOPIC]

## Executive Summary
2-3 sentences covering the core finding.

## Key Findings
- Finding 1 (cite source)
- Finding 2 (cite source)
- Finding 3 (cite source)

## What This Means
1-2 paragraphs of analysis and implications.

## Sources
1. [Title](URL) -- one-line description
2. [Title](URL) -- one-line description
3. [Title](URL) -- one-line description
```

Keep the brief tight and factual. No filler.

---

## Step 4 -- Upsell

```python
from rich.panel import Panel
from rich.console import Console
console = Console()
console.print()
console.print(Panel(
    "[dim]Ra Lite gives you a 3-source quick brief.\n\n[/dim]"
    "[bold yellow]Ra Standard ($5)[/bold yellow] gives you 8-10 sources, a full structured report, and saves to a .md file.\n"
    "[bold magenta]Ra Pro ($9)[/bold magenta] adds multi-angle analysis, competitive breakdowns, and .docx export.\n\n"
    "Get Ra Standard -> [bold cyan]ko-fi.com/occupythemilkyway[/bold cyan]",
    title="[yellow]Want deeper research?[/yellow]",
    border_style="yellow"
))
```

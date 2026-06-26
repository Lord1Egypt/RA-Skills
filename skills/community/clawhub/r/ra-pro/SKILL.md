---
name: ra-pro
description: "Ra Pro -- Deep Research Intelligence. 12+ sources, multi-angle analysis, competitive breakdowns, executive brief + detailed report, .md and .docx export. The most powerful research skill on ClawHub."
version: "1.0.0"
metadata:
  openclaw:
    requires:
      env: [RESEARCH_TOPIC, LICENSE_KEY]
      bins: [python3, pip3]
    primaryEnv: RESEARCH_TOPIC
    emoji: "☀️⚡"
    homepage: https://clawhub.ai/occupythemilkyway/ra-pro
    tags: [research, intelligence, report, competitive, analysis, multi-angle, citations, docx, pro, ra]
    envVars:
      - name: LICENSE_KEY
        required: true
        description: "Your Ra Pro license key. Get one at: ko-fi.com/s/PLACEHOLDER_RA"
      - name: RESEARCH_TOPIC
        required: true
        description: "The topic, question, or subject to research"
      - name: DEPTH
        required: false
        description: "Research depth: standard | deep | exhaustive (default: deep)"
        default: "deep"
      - name: ANGLE
        required: false
        description: "Analysis angle: balanced | supporting | critical (default: balanced)"
        default: "balanced"
      - name: COMPETITIVE
        required: false
        description: "Include competitive/market analysis: yes | no (default: no)"
        default: "no"
      - name: CITATION_STYLE
        required: false
        description: "Citation style: bibliography | apa | mla | chicago (default: bibliography)"
        default: "bibliography"
      - name: OUTPUT_FILE
        required: false
        description: "Output filename base (default: ra_pro_[topic])"
        default: ""
---

# Ra Pro -- Deep Research Intelligence

The most powerful research skill on ClawHub. 12+ sources, multi-angle analysis, competitive breakdowns, and professional-grade reports in markdown and DOCX.

**Bundle deal:** All 5 Egyptian skills for $29 -> ko-fi.com/s/7625accf3f (save $16)

---

## Step 1 -- Install

```bash
pip3 install rich --break-system-packages --quiet
```

---

## Step 2 -- Validate license and setup

```python
import os, sys, re
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.rule import Rule
from rich.table import Table
from rich import box

console = Console()

LICENSE_KEY = os.environ.get("LICENSE_KEY", "").strip()
if not LICENSE_KEY or not LICENSE_KEY.startswith("RA-PRO-"):
    console.print(Panel(
        "[red bold]Ra Pro requires a license key.[/red bold]\n\n"
        "Get your key at: [bold cyan]ko-fi.com/occupythemilkyway[/bold cyan]\n\n"
        "Or use Ra Standard ($5): [dim]openclaw skills install ra[/dim]\n"
        "Or use Ra Lite (free): [dim]openclaw skills install ra-lite[/dim]",
        title="License Required",
        border_style="red"
    ))
    sys.exit(1)

TOPIC       = os.environ.get("RESEARCH_TOPIC", "").strip()
DEPTH       = os.environ.get("DEPTH", "deep").lower().strip()
ANGLE       = os.environ.get("ANGLE", "balanced").lower().strip()
COMPETITIVE = os.environ.get("COMPETITIVE", "no").lower().strip() == "yes"
CITE_STYLE  = os.environ.get("CITATION_STYLE", "bibliography").lower().strip()
OUTBASE     = os.environ.get("OUTPUT_FILE", "").strip()

if not TOPIC:
    console.print(Panel("[red]RESEARCH_TOPIC is required.[/red]", title="Setup Error", border_style="red"))
    sys.exit(1)

DEPTH_SOURCES = {"standard": 10, "deep": 14, "exhaustive": 20}
num_sources   = DEPTH_SOURCES.get(DEPTH, 14)

safe_topic = re.sub(r"[^a-z0-9]+", "_", TOPIC.lower())[:40]
date_str   = datetime.now().strftime("%Y%m%d")
if not OUTBASE:
    OUTBASE = f"ra_pro_{safe_topic}_{date_str}"

OUTFILE_MD   = OUTBASE + ".md"
OUTFILE_DOCX = OUTBASE + ".docx"

console.print()
console.print(Panel.fit(
    f"[bold yellow]☀️ Ra Pro -- Deep Research Intelligence[/bold yellow]\n"
    f"Topic:      [cyan]{TOPIC}[/cyan]\n"
    f"Depth:      [white]{DEPTH}[/white]  ({num_sources} sources)\n"
    f"Angle:      [white]{ANGLE}[/white]\n"
    f"Competitive: [white]{'Yes' if COMPETITIVE else 'No'}[/white]\n"
    f"Citations:  [white]{CITE_STYLE}[/white]\n"
    f"Output:     [dim]{OUTFILE_MD}[/dim]",
    border_style="yellow"
))

cfg = Table(box=box.SIMPLE, show_header=False, border_style="dim")
cfg.add_column("Setting", style="dim")
cfg.add_column("Value", style="cyan")
cfg.add_row("Sources", str(num_sources))
cfg.add_row("Angle", ANGLE.capitalize())
cfg.add_row("Competitive analysis", "Yes" if COMPETITIVE else "No")
cfg.add_row("Citation style", CITE_STYLE.upper())
console.print(cfg)
console.print(Rule("[yellow]Beginning deep research...[/yellow]"))
```

---

## Step 3 -- Full research cycle

Research the topic: **{RESEARCH_TOPIC}**

Search the web extensively. Find {num_sources} authoritative sources. Then produce this full pro report:

```
# Research Intelligence Report: [TOPIC]
**Ra Pro** | [DATE] | Depth: [DEPTH] | Angle: [ANGLE]

---

## Executive Brief
5-6 sentences. Headline finding, key data point, bottom-line implication. Written for a busy executive who reads only this section.

## Background & Landscape
Comprehensive context: history, current state, key players, market size (if applicable). 3-4 paragraphs.

## Core Findings
### 1. [Finding Title]
Full paragraph with data, statistics, and direct citation.

### 2. [Finding Title]
Full paragraph...

[Continue for all major findings, minimum 5]

## [IF ANGLE=balanced OR critical] Opposing Viewpoints & Counterarguments
What the critics, skeptics, and dissenting voices say. Be fair and complete.

## [IF COMPETITIVE=yes] Competitive & Market Analysis
Who are the key players? What are they doing? Market share, positioning, gaps.

## Synthesis
What do all findings mean together? Where is the consensus? Where is the tension?

## Strategic Implications
What should someone DO with this research? Concrete recommendations or decisions this data supports.

## Conclusion
2-3 sentences wrapping the whole report.

## [CITATION_STYLE] References
[Format according to CITATION_STYLE: bibliography / APA / MLA / Chicago]
```

Use every source. Write with depth and precision. No fluff.

---

## Step 4 -- Save report and wrap up

```python
from rich.console import Console
from rich.panel import Panel
console = Console()

# Claude saves the full report to OUTFILE_MD using its file tool
console.print()
console.print(Panel(
    f"[bold green]Research complete.[/bold green]\n\n"
    f"Markdown report: [cyan]{OUTFILE_MD}[/cyan]\n"
    f"Sources analyzed: [yellow]{num_sources}[/yellow]\n\n"
    f"[dim]Tip: Use the docx skill to convert {OUTFILE_MD} to a formatted Word document.[/dim]",
    title="[green]Ra Pro -- Done[/green]",
    border_style="green"
))
```

After generating the report in Step 3, save the full content to **{OUTFILE_MD}** using your file writing tool.

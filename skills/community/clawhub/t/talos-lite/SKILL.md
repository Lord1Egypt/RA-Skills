---
name: talos-lite
description: "Talos Lite â Social Calendar (Free). Generate a 1-week posting schedule for one platform with 3 captions. A free preview of what Talos Pro builds for your full content strategy."
version: "1.0.4"
metadata:
  openclaw:
    requires:
      env: []
      bins: [python3, pip3]
    primaryEnv: "BRAND_TOPIC"
    homepage: https://clawhub.ai/occupythemilkyway/talos-lite
    emoji: "â¡"
    tags: [social-media, content, scheduler, twitter, free, lite, talos, marketing]
    envVars:
      - name: BRAND_TOPIC
        required: true
        description: "What your brand is about (e.g. 'productivity tips for developers')"
      - name: PLATFORM
        required: false
        description: "Platform to plan for: twitter, linkedin, instagram, or threads (Lite: 1 platform)"
        default: "twitter"
---

# Talos Lite â Free Content Preview

Generate a 1-week, 3-post schedule for one platform.

## Free vs Pro

| Feature | Talos Lite (Free) | Talos Pro |
|---------|------------------|-----------|
| Calendar length | **1 week** | Up to 12 weeks |
| Platforms | **1** | All 5 (+ TikTok) |
| Posts/week | **3** | Up to 7 |
| A/B caption variants | â | â |
| Repurposing strategy | â | â |
| CSV export | â | â Buffer/Hootsuite ready |
| Content angle ideas | 3 | 20+ |

ð **Upgrade:** `openclaw skills install talos-pro` â key at **ko-fi.com/s/9433e598bd**

ð° **Bundle deal:** all 5 Pro skills for **$29** â **ko-fi.com/s/7625accf3f** (save $16)

---

## Step 1 â Install

```bash
pip3 install rich --break-system-packages --quiet
```

---

## Step 2 â Quick content preview (Lite)

```python
import os, random
from datetime import date, timedelta
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

console = Console()

TOPIC    = os.environ.get("BRAND_TOPIC","productivity tips")
PLATFORM = os.environ.get("PLATFORM","twitter").strip().lower()
TODAY    = date.today()

# Lite limits
POST_LIMIT   = 3
WEEK_LIMIT   = 1
topic_short  = TOPIC.split()[0] if TOPIC else "topic"

BEST_TIMES = {
    "twitter":   [("Mon","9am"),("Wed","12pm"),("Fri","10am")],
    "linkedin":  [("Tue","8am"),("Wed","10am"),("Thu","9am")],
    "instagram": [("Mon","6am"),("Wed","11am"),("Fri","10am")],
    "threads":   [("Mon","9am"),("Wed","12pm"),("Fri","11am")],
}
PILLARS = ["Education","Inspiration","Engagement"]

HOOKS = [
    f"Here's what most people get wrong about {topic_short}:",
    f"The {topic_short} rule nobody talks about:",
    f"3 things I wish I knew about {topic_short}:",
]

def gen_caption(platform, pillar):
    hook = random.choice(HOOKS)
    if platform == "twitter":
        return (f"{hook}\n\nâ [insight 1]\nâ [insight 2]\nâ [insight 3]\n\n"
                f"#{topic_short.replace(' ','').title()} #{pillar}")[:280]
    elif platform == "linkedin":
        return (f"{hook}\n\n[Hook: surprising statement]\n\n"
                f"1/ [First point]\n2/ [Second point]\n3/ [Third point]\n\n"
                f"What do you think? ð\n\n#{topic_short.replace(' ','').title()}")
    elif platform == "instagram":
        return (f"ð¡ {hook.upper()}\n\n[Main value about {topic_short}]\n\n"
                f"Save if helpful â»ï¸\n\n#{topic_short.replace(' ','')} #{pillar.lower()} #ContentCreator")
    else:
        return f"{hook}\n\n[Your take on {topic_short}]\n\nWhat do you think? ð"

times = BEST_TIMES.get(PLATFORM, BEST_TIMES["twitter"])

console.print(Panel.fit(
    f"[bold cyan]â¡ Talos Lite â 1-Week Preview[/bold cyan]\n"
    f"Topic: [yellow]{TOPIC}[/yellow]  Platform: [green]{PLATFORM.title()}[/green]\n"
    f"[dim]Lite: 1 platform, 1 week, 3 posts â upgrade to Pro for the full strategy[/dim]",
    border_style="cyan"
))

calendar = []
for i,(day,time) in enumerate(times[:POST_LIMIT]):
    pillar    = PILLARS[i % len(PILLARS)]
    post_date = TODAY + timedelta(days=i)
    caption   = gen_caption(PLATFORM, pillar)
    calendar.append({"date":post_date.strftime("%b %d"),"day":day,"time":time,
                     "pillar":pillar,"caption":caption})

console.print()
tbl = Table(title=f"ð 1-Week {PLATFORM.title()} Calendar ({POST_LIMIT} posts)",
            box=box.ROUNDED, border_style="cyan")
tbl.add_column("Date",   width=8, style="cyan")
tbl.add_column("Day",    width=5)
tbl.add_column("Time",   width=6, style="green")
tbl.add_column("Pillar", width=14, style="magenta")
for e in calendar:
    tbl.add_row(e["date"],e["day"],e["time"],e["pillar"])
console.print(tbl)

console.print()
for e in calendar:
    console.print(Panel(e["caption"],
        title=f"[bold]ð {e['date']} â {e['pillar']}[/bold]",
        border_style="yellow"))

console.print()
console.print(Panel(
    f"[bold yellow]ð Want your full content strategy?[/bold yellow]\n\n"
    f"Talos Pro builds a [bold]{'{'}8 or 12{'}'}[/bold]-week calendar across [bold]all platforms[/bold] "
    f"with A/B caption variants, a cross-platform repurposing guide, and a CSV "
    f"you can import directly into Buffer, Hootsuite, or Later.\n\n"
    f"[bold cyan]openclaw skills install talos-pro[/bold cyan]\n"
    f"Get your key â [bold]ko-fi.com/s/9433e598bd[/bold]",
    title="Upgrade to Talos Pro",
    border_style="cyan"
))
```

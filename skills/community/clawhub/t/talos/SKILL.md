---
name: talos
description: "Talos â God of Automation. Plan and batch your entire social media content calendar â generate a 4-week posting schedule, write platform-optimised captions for Twitter/X, LinkedIn, Instagram, and Threads, apply best-posting-time rules, and export a ready-to-use content calendar."
version: "1.0.4"
metadata:
  openclaw:
    requires:
      env: []
      bins: [python3, pip3]
    primaryEnv: "BRAND_TOPIC"
    homepage: https://clawhub.ai/occupythemilkyway/talos
    emoji: "â¡ð"
    tags: [social-media, content, scheduler, twitter, linkedin, instagram, talos, marketing, calendar]
    envVars:
      - name: BRAND_TOPIC
        description: "What your brand/account is about (e.g. 'productivity tips for developers', 'vegan cooking on a budget')"
        required: true
      - name: PLATFORMS
        description: "Comma-separated platforms to plan for: twitter, linkedin, instagram, threads"
        required: false
        default: "twitter, linkedin, instagram"
      - name: POSTS_PER_WEEK
        description: "Number of posts per platform per week (1-5)"
        required: false
        default: "3"
      - name: CONTENT_PILLARS
        description: "Comma-separated content pillars (e.g. 'education, inspiration, engagement, promotion')"
        required: false
        default: "education, inspiration, engagement, promotion"
      - name: BRAND_TONE
        description: "Brand tone: educational, professional, casual, or inspirational"
        required: false
        default: "educational"
---

# Talos â Social Media Content Calendar

Generate a complete 4-week social media content calendar with platform-optimised captions, best posting times, and content pillar rotation â all offline, no API keys required.

## What you get

- **4-week posting calendar** with dates, days, and optimal posting times for each platform
- **Platform-native captions** for Twitter/X (â¤280 chars), LinkedIn (long-form), Instagram (emoji + hashtags), and Threads
- **Content pillar rotation** across education, inspiration, engagement, and promotion (fully customisable)
- **Hashtag strategy** guide per platform
- **Topic angle ideas** based on your brand topic
- **Exports**: JSON calendar + Markdown document ready to paste into any scheduling tool

## ð Security

Runs entirely locally. No API calls, no data transmitted. Pure offline generation.

---

## Step 1 â Install

```bash
pip3 install rich --break-system-packages --quiet
```

---


---

## â¡ Upgrade to Talos Pro

ð **Get Talos Pro** â **ko-fi.com/s/9433e598bd** â $9 one-time

```bash
openclaw skills install talos-pro
# Set LICENSE_KEY env var to your key from Ko-fi, then run
```

ð° **Bundle deal:** all 5 Pro skills for **$29** â **ko-fi.com/s/7625accf3f** (save $16)

## Step 2 â Build Your Content Calendar

```python
import os, json, re, random
from datetime import date, timedelta
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

FENCE = chr(96) * 3

console = Console()

TOPIC       = os.environ.get("BRAND_TOPIC", "productivity tips")
PLATS_RAW   = os.environ.get("PLATFORMS", "twitter, linkedin, instagram")
try:
    PPW = int(os.environ.get("POSTS_PER_WEEK", "3"))
except ValueError:
    PPW = 3
PILLARS_R   = os.environ.get("CONTENT_PILLARS", "education, inspiration, engagement, promotion")
TONE        = os.environ.get("BRAND_TONE", "educational")
TODAY       = date.today()

PLATFORMS = [p.strip().lower() for p in PLATS_RAW.split(",") if p.strip()]
PILLARS   = [p.strip() for p in PILLARS_R.split(",") if p.strip()]

# Guard: clamp PPW to 1-5
PPW = max(1, min(PPW, 5))
# Guard: empty PLATFORMS or PILLARS
if not PLATFORMS:
    console.print("[red]â ï¸  PLATFORMS is empty â defaulting to 'twitter, linkedin, instagram'[/red]")
    PLATFORMS = ["twitter", "linkedin", "instagram"]
if not PILLARS:
    console.print("[red]â ï¸  CONTENT_PILLARS is empty â defaulting to standard pillars[/red]")
    PILLARS = ["education", "inspiration", "engagement", "promotion"]

topic_short = TOPIC.split()[0] if TOPIC else "topic"

console.print(Panel.fit(
    f"[bold cyan]ð± â¡ Talos â Social Media Command[/bold cyan]\n"
    f"Topic: [yellow]{TOPIC}[/yellow]\n"
    f"Platforms: [green]{', '.join(PLATFORMS)}[/green]  |  "
    f"Posts/week: [green]{PPW}[/green]  |  Tone: [green]{TONE}[/green]",
    border_style="cyan"
))

# ââ Best posting times ââââââââââââââââââââââââââââââââââââââââââââââââââââââââ
BEST_TIMES = {
    "twitter":   [("Mon", "9am"), ("Tue", "9am"), ("Wed", "12pm"), ("Thu", "9am"), ("Fri", "10am")],
    "linkedin":  [("Tue", "8am"), ("Wed", "10am"), ("Thu", "9am"), ("Mon", "8am"), ("Fri", "9am")],
    "instagram": [("Mon", "6am"), ("Wed", "11am"), ("Fri", "10am"), ("Sat", "9am"), ("Tue", "2pm")],
    "threads":   [("Mon", "9am"), ("Wed", "12pm"), ("Fri", "11am"), ("Tue", "9am"), ("Thu", "2pm")],
}

# ââ Caption templates per tone ââââââââââââââââââââââââââââââââââââââââââââââââ
TONE_HOOKS = {
    "educational":  [
        "Here's what most people get wrong about {topic}:",
        "The {topic} rule nobody talks about:",
        "{number} things I wish I knew about {topic}:",
    ],
    "professional": [
        "A key insight about {topic} for professionals:",
        "What high-performers know about {topic}:",
        "The {topic} principle that drives results:",
    ],
    "casual": [
        "Real talk about {topic} â",
        "Hot take: {topic} is more interesting than you think.",
        "Nobody told me {topic} could be this simple.",
    ],
    "inspirational": [
        "Your {topic} journey starts with one step.",
        "The {topic} mindset that changes everything:",
        "What if {topic} was easier than you thought?",
    ],
}
hooks = TONE_HOOKS.get(TONE, TONE_HOOKS["educational"])

# ââ Content type formats ââââââââââââââââââââââââââââââââââââââââââââââââââââââ
CONTENT_FORMATS = {
    "education":    ["how-to", "tips-list", "explainer", "myth-busting", "framework"],
    "inspiration":  ["quote", "success-story", "milestone", "mindset", "reminder"],
    "engagement":   ["question", "poll", "fill-in-blank", "hot-take", "challenge"],
    "promotion":    ["feature-spotlight", "testimonial", "case-study", "offer", "behind-scenes"],
    "tips":         ["quick-tip", "pro-tip", "mistake-to-avoid", "checklist", "framework"],
    "portfolio":    ["case-study", "before-after", "process", "result", "client-story"],
    "tools":        ["tool-review", "comparison", "workflow", "integration", "recommendation"],
    "product":      ["feature", "how-to-use", "benefit", "testimonial", "demo"],
    "behind-the-scenes": ["process", "day-in-life", "team", "workspace", "fail"],
}

def get_format(pillar: str) -> str:
    for key in CONTENT_FORMATS:
        if key.lower() in pillar.lower():
            return random.choice(CONTENT_FORMATS[key])
    return random.choice(["tip", "story", "question", "fact"])

# ââ Offline topic angle generator âââââââââââââââââââââââââââââââââââââââââââââ
def get_topic_ideas(topic: str) -> list:
    return [
        f"beginner guide to {topic}",
        f"common mistakes in {topic}",
        f"how to improve your {topic}",
        f"{topic} for professionals",
        f"advanced {topic} strategies",
        f"{topic} tools and resources",
        f"the future of {topic}",
        f"{topic} myths debunked",
    ]

console.print("[dim]Generating topic anglesâ¦[/dim]")
topic_ideas = get_topic_ideas(TOPIC)

# ââ Platform caption generators âââââââââââââââââââââââââââââââââââââââââââââââ
def gen_twitter(pillar: str, content_form: str, week: int) -> str:
    hook = random.choice(hooks).replace("{topic}", topic_short).replace("{number}", str(random.choice([3, 5, 7])))
    bodies = [
        f"{hook}\n\nâ [insight 1]\nâ [insight 2]\nâ [insight 3]\n\nRT if useful ð",
        f"[Hot take about {topic_short}]\n\nHere's why: [reason]\n\nAgree? ð§µ",
        f"Stop doing X. Start doing Y.\n\nFor {topic_short}, this means: [specific advice]",
        f"The {content_form} that changed how I think about {topic_short}:\n\n[insight]\n\nThread ð§µ",
    ]
    body = random.choice(bodies)
    hashtags = f"#{topic_short.replace(' ', '').title()} #ContentTips"
    result = f"{body}\n\n{hashtags}"
    if len(result) > 280:
        result = result[:277].rsplit(' ', 1)[0] + "â¦"
    return result

def gen_linkedin(pillar: str, content_form: str, week: int) -> str:
    return (
        f"The {topic_short} insight that changed everything for me:\n\n"
        f"[Hook â one surprising or bold statement]\n\n"
        f"Here's what I learned:\n\n"
        f"1/ [First point]\n\n"
        f"2/ [Second point]\n\n"
        f"3/ [Third point]\n\n"
        f"The bottom line: [key takeaway]\n\n"
        f"What's your experience with {topic_short}? Drop it in the comments ð\n\n"
        f"#{topic_short.replace(' ', '').title()} #ProfessionalGrowth #{pillar.replace(' ', '').title()}"
    )

def gen_instagram(pillar: str, content_form: str, week: int) -> str:
    hook = random.choice(hooks).replace("{topic}", topic_short).replace("{number}", str(random.choice([3, 5, 7])))
    emojis = ["â¨", "ð¥", "ð¡", "ð¯", "ð", "ðª", "ð"]
    e = random.choice(emojis)
    return (
        f"{e} {hook.upper()}\n\n"
        f"[Main value â 2-3 sentences about {topic_short}]\n\n"
        f"Save this post if you found it helpful! â»ï¸\n\n"
        f"ð Follow for daily {topic_short} tips\n\n"
        f"â â â â â â â\n"
        f"#{topic_short.replace(' ', '')} #{pillar.replace(' ', '')} #ContentCreator "
        f"#InstagramTips #GrowthMindset #OnlineBusiness"
    )

def gen_threads(pillar: str, content_form: str, week: int) -> str:
    hook = random.choice(hooks).replace("{topic}", topic_short).replace("{number}", str(random.choice([3, 5, 7])))
    return (
        f"{hook}\n\n"
        f"[Your honest take on {topic_short}]\n\n"
        f"What do you think? ð"
    )

PLATFORM_GENS = {
    "twitter":   gen_twitter,
    "linkedin":  gen_linkedin,
    "instagram": gen_instagram,
    "threads":   gen_threads,
}

# ââ Build 4-week calendar âââââââââââââââââââââââââââââââââââââââââââââââââââââ
calendar = []
for week in range(1, 5):
    for platform in PLATFORMS:
        gen_fn = PLATFORM_GENS.get(platform, gen_twitter)
        times  = BEST_TIMES.get(platform, BEST_TIMES["twitter"])
        for day_idx in range(min(PPW, 5)):
            pillar       = PILLARS[day_idx % len(PILLARS)]
            content_form = get_format(pillar)
            day_name, best_time = times[day_idx % len(times)]
            post_date    = TODAY + timedelta(weeks=week - 1, days=day_idx)
            caption      = gen_fn(pillar, content_form, week)
            calendar.append({
                "week":      week,
                "platform":  platform,
                "date":      post_date.strftime("%b %d"),
                "day":       day_name,
                "best_time": best_time,
                "pillar":    pillar,
                "format":    content_form,
                "caption":   caption,
            })

# ââ Display: Calendar overview ââââââââââââââââââââââââââââââââââââââââââââââââ
console.print()
cal_table = Table(
    title=f"ð 4-Week Social Calendar â {len(calendar)} posts",
    box=box.ROUNDED, border_style="cyan"
)
cal_table.add_column("Wk",       style="dim",    width=4)
cal_table.add_column("Date",     style="cyan",   width=8)
cal_table.add_column("Platform", style="yellow", width=12)
cal_table.add_column("Day",      style="green",  width=5)
cal_table.add_column("Time",     style="green",  width=6)
cal_table.add_column("Pillar",   style="magenta",width=14)
cal_table.add_column("Format",   style="white",  width=18)

for entry in calendar:
    cal_table.add_row(
        str(entry["week"]),
        entry["date"],
        entry["platform"].title(),
        entry["day"],
        entry["best_time"],
        entry["pillar"].title(),
        entry["format"],
    )
console.print(cal_table)

# ââ Display: Sample captions ââââââââââââââââââââââââââââââââââââââââââââââââââ
console.print()
for platform in PLATFORMS[:2]:
    sample = next((p for p in calendar if p["platform"] == platform), None)
    if sample:
        console.print(Panel(
            sample["caption"],
            title=f"[bold]ð Sample Caption â {platform.title()}[/bold]",
            border_style="yellow"
        ))

# ââ Display: Hashtag strategy âââââââââââââââââââââââââââââââââââââââââââââââââ
HASHTAG_GUIDE = {
    "twitter":   "1-2 hashtags max. Use trending + niche specific. Never in the middle of text.",
    "linkedin":  "3-5 hashtags at the end. Mix: 1 broad + 2 niche + 1 trending.",
    "instagram": "10-15 hashtags. Mix sizes: 3 mega (1M+) + 5 medium (100k-1M) + 7 niche (<100k).",
    "threads":   "No hashtags currently. Focus on conversation starters.",
}
console.print()
hg_lines = "\n".join([
    f"[cyan]{p.title()}:[/cyan] {guide}"
    for p, guide in HASHTAG_GUIDE.items() if p in PLATFORMS
])
console.print(Panel(hg_lines, title="[bold]# Hashtag Strategy[/bold]", border_style="blue"))

# ââ Display: Topic angles âââââââââââââââââââââââââââââââââââââââââââââââââââââ
if topic_ideas:
    console.print()
    ti_lines = "\n".join([f"[dim]{i + 1}.[/dim] {idea}" for i, idea in enumerate(topic_ideas)])
    console.print(Panel(ti_lines, title="[bold]ð¡ Content Angle Ideas[/bold]", border_style="magenta"))

# ââ Save outputs ââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââ
topic_slug = re.sub(r"[^a-z0-9]", "_", TOPIC[:20].lower())
json_path  = f"social_calendar_{topic_slug}_{TODAY}.json"
md_path    = f"social_calendar_{topic_slug}_{TODAY}.md"

with open(json_path, "w", encoding="utf-8") as f:
    json.dump({"topic": TOPIC, "platforms": PLATFORMS, "calendar": calendar,
               "generated": str(TODAY)}, f, indent=2)

with open(md_path, "w", encoding="utf-8") as f:
    f.write(f"# Social Media Calendar â {TOPIC}\n\n")
    f.write(f"**Platforms:** {', '.join(p.title() for p in PLATFORMS)}  ")
    f.write(f"**Posts/week:** {PPW}  **Generated:** {TODAY}\n\n")
    f.write("## Content Angles\n\n")
    for idea in topic_ideas:
        f.write(f"- {idea}\n")
    f.write("\n## Calendar\n\n")
    f.write("| Wk | Date | Platform | Day | Time | Pillar | Format |\n")
    f.write("|----|------|----------|-----|------|--------|--------|\n")
    for e in calendar:
        f.write(f"| {e['week']} | {e['date']} | {e['platform'].title()} | {e['day']} | {e['best_time']} | {e['pillar'].title()} | {e['format']} |\n")
    f.write("\n## Sample Captions\n\n")
    shown = set()
    for e in calendar:
        if e["platform"] not in shown:
            shown.add(e["platform"])
            f.write(f"### {e['platform'].title()}\n\n{FENCE}\n{e['caption']}\n{FENCE}\n\n")

console.print()
console.print(Panel(
    f"[green]â Done![/green]\n\n"
    f"ð [cyan]{json_path}[/cyan] â full calendar data\n"
    f"ð [cyan]{md_path}[/cyan] â markdown calendar\n\n"
    f"[dim]Import either file into Buffer, Hootsuite, Later, or any scheduling tool.[/dim]",
    title="[bold]ð¤ Exports[/bold]",
    border_style="green"
))
```

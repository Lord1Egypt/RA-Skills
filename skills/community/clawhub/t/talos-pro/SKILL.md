---
name: talos-pro
description: "Talos Pro â Social Media Command Centre. Generate a 12-week content calendar across all platforms with daily posting schedules, A/B caption variants, hashtag research, competitor content angles, repurposing strategy, and full CSV export for scheduling tools. The full-power version of Talos."
version: "1.0.4"
metadata:
  openclaw:
    requires:
      env: [LICENSE_KEY]
      bins: [python3, pip3]
    primaryEnv: "BRAND_TOPIC"
    homepage: https://clawhub.ai/occupythemilkyway/talos-pro
    emoji: "â¡ðð"
    tags: [social-media, content, scheduler, twitter, linkedin, instagram, talos, pro, premium, marketing]
    envVars:
      - name: LICENSE_KEY
        required: true
        description: "Your Talos Pro license key. Get one at: ko-fi.com/s/9433e598bd"

ð° **Bundle deal:** all 5 Pro skills for **$29** â **ko-fi.com/s/7625accf3f** (save $16)
      - name: BRAND_TOPIC
        required: true
        description: "What your brand is about (e.g. 'productivity for developers')"
      - name: PLATFORMS
        required: false
        description: "Comma-separated: twitter, linkedin, instagram, threads, tiktok"
        default: "twitter, linkedin, instagram"
      - name: POSTS_PER_WEEK
        required: false
        description: "Posts per platform per week (1-7 in Pro)"
        default: "5"
      - name: CONTENT_PILLARS
        required: false
        description: "Comma-separated content pillars"
        default: "education, inspiration, engagement, promotion"
      - name: BRAND_TONE
        required: false
        description: "educational, professional, casual, or inspirational"
        default: "educational"
      - name: WEEKS
        required: false
        description: "Calendar length in weeks (4, 8, or 12)"
        default: "8"
      - name: AB_VARIANTS
        required: false
        description: "Set to 'true' to generate A/B caption variants"
        default: "true"
---

# Talos Pro â Content Command Centre

Everything in Talos, plus 8-12 week calendars, A/B caption variants, TikTok support, repurposing strategy, and CSV export for Buffer/Hootsuite/Later.

## Pro features vs free Talos

| Feature | Talos (Free) | Talos Pro |
|---------|-------------|-----------|
| Calendar length | 4 weeks | **8 or 12 weeks** |
| Posts/week | Up to 5 | **Up to 7** |
| Platforms | Twitter/LinkedIn/Instagram/Threads | **+ TikTok** |
| Caption variants | 1 per post | **A/B variants** |
| Repurposing guide | â | â Cross-post strategy |
| CSV export | â | â Buffer/Hootsuite ready |
| Content angles | 8 | **20+ angle ideas** |

ð **Upgrade:** `openclaw skills install talos-pro` + key at **ko-fi.com/s/9433e598bd**

---

## Setup

1. **Purchase** your license key at **ko-fi.com/s/9433e598bd** ($9 one-time)
   - Or get all 5 Pro skills for **$29** â **ko-fi.com/s/7625accf3f** (save $16)
2. **Install:** `openclaw skills install talos-pro`
3. **Activate:** set the `LICENSE_KEY` environment variable to the key you received
4. **Run** â you're in

---

## Step 1 â Install

```bash
pip3 install rich --break-system-packages --quiet
```

---

## Step 2 â Full content command centre (Pro)

```python
import os, json, re, random, csv
from datetime import date, timedelta
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

FENCE = chr(96) * 3

console = Console()

LICENSE_KEY = os.environ.get("LICENSE_KEY","").strip()
if not LICENSE_KEY:
    console.print(Panel(
        "[red bold]ð Talos Pro requires a license key.[/red bold]\n\n"
        "Get your key at: [bold cyan]ko-fi.com/s/9433e598bd[/bold cyan]\n\n"
        "Or use the free version: [dim]openclaw skills install talos[/dim]",
        title="License Required", border_style="red"
    ))
    raise SystemExit(1)

TOPIC      = os.environ.get("BRAND_TOPIC","productivity tips")
PLATS_RAW  = os.environ.get("PLATFORMS","twitter, linkedin, instagram")
try: PPW   = min(int(os.environ.get("POSTS_PER_WEEK","5")),7)
except: PPW = 5
PILLARS_R  = os.environ.get("CONTENT_PILLARS","education, inspiration, engagement, promotion")
TONE       = os.environ.get("BRAND_TONE","educational")
try: WEEKS = min(int(os.environ.get("WEEKS","8")),12)
except: WEEKS = 8
AB_VARIANTS = os.environ.get("AB_VARIANTS","true").lower() == "true"
TODAY      = date.today()

PLATFORMS = [p.strip().lower() for p in PLATS_RAW.split(",") if p.strip()]
PILLARS   = [p.strip() for p in PILLARS_R.split(",") if p.strip()]
PPW       = max(1, min(PPW, 7))
if not PLATFORMS: PLATFORMS = ["twitter","linkedin","instagram"]
if not PILLARS:   PILLARS   = ["education","inspiration","engagement","promotion"]
topic_short = TOPIC.split()[0] if TOPIC else "topic"

console.print(Panel.fit(
    f"[bold cyan]â¡ðð Talos Pro â Content Command Centre[/bold cyan]\n"
    f"Topic: [yellow]{TOPIC}[/yellow]  Platforms: [green]{', '.join(PLATFORMS)}[/green]  "
    f"Weeks: [white]{WEEKS}[/white]  Posts/wk: [white]{PPW}[/white]  A/B: [white]{AB_VARIANTS}[/white]",
    border_style="cyan"
))

BEST_TIMES = {
    "twitter":   [("Mon","9am"),("Tue","9am"),("Wed","12pm"),("Thu","9am"),("Fri","10am"),("Sat","10am"),("Sun","11am")],
    "linkedin":  [("Tue","8am"),("Wed","10am"),("Thu","9am"),("Mon","8am"),("Fri","9am"),("Sat","10am"),("Sun","12pm")],
    "instagram": [("Mon","6am"),("Wed","11am"),("Fri","10am"),("Sat","9am"),("Tue","2pm"),("Sun","10am"),("Thu","11am")],
    "threads":   [("Mon","9am"),("Wed","12pm"),("Fri","11am"),("Tue","9am"),("Thu","2pm"),("Sat","10am"),("Sun","11am")],
    "tiktok":    [("Tue","7am"),("Thu","9am"),("Fri","5pm"),("Sat","11am"),("Mon","7am"),("Wed","8pm"),("Sun","4pm")],
}

TONE_HOOKS = {
    "educational":   ["Here's what most people get wrong about {topic}:","The {topic} rule nobody talks about:","{number} things I wish I knew about {topic}:","The {topic} framework that changed my approach:"],
    "professional":  ["A key insight about {topic} for professionals:","What high-performers know about {topic}:","The {topic} principle that drives results:","Leadership lesson from {topic}:"],
    "casual":        ["Real talk about {topic} â","Hot take: {topic} is misunderstood.","Nobody told me {topic} could be this simple.","Okay {topic} people â hear me out:"],
    "inspirational": ["Your {topic} journey starts with one step.","The {topic} mindset that changes everything:","What if {topic} was easier than you thought?","Success in {topic} starts with this belief:"],
}
hooks = TONE_HOOKS.get(TONE, TONE_HOOKS["educational"])

CONTENT_FORMATS = {
    "education":  ["how-to","tips-list","explainer","myth-busting","framework","case-study"],
    "inspiration":["quote","success-story","milestone","mindset","reminder","transformation"],
    "engagement": ["question","poll","fill-in-blank","hot-take","challenge","debate"],
    "promotion":  ["feature-spotlight","testimonial","case-study","offer","behind-scenes","demo"],
}

def get_format(pillar):
    for key in CONTENT_FORMATS:
        if key.lower() in pillar.lower():
            return random.choice(CONTENT_FORMATS[key])
    return random.choice(["tip","story","question","fact","insight"])

def make_hook():
    return random.choice(hooks).replace("{topic}",topic_short).replace("{number}",str(random.choice([3,5,7])))

def gen_caption(platform, pillar, content_form, week, variant="A"):
    h = make_hook()
    if platform == "twitter":
        bodies = [
            f"{h}\n\nâ [insight 1]\nâ [insight 2]\nâ [insight 3]\n\nThread? ð§µ",
            f"[Bold claim about {topic_short}]\n\nHere's why: [reason]\n\nAgree? ð¤",
            f"[{content_form.title()}] about {topic_short}:\n\n[Main insight]\n\nSave this ð",
        ]
        body = bodies[(week + len(variant)) % len(bodies)]
        tags = f"#{topic_short.replace(' ','').title()} #{pillar.replace(' ','').title()}"
        result = f"{body}\n\n{tags}"
        return result[:280] + ("â¦" if len(result)>280 else "")
    elif platform == "linkedin":
        angle = "challenges" if variant=="B" else "opportunities"
        return (f"The {angle} in {topic_short} that most people overlook:\n\n"
                f"{h}\n\n1/ [Point one]\n\n2/ [Point two]\n\n3/ [Point three]\n\n"
                f"What's your take on {topic_short}? Comment below ð\n\n"
                f"#{topic_short.replace(' ','').title()} #{pillar.replace(' ','').title()}")
    elif platform == "instagram":
        emojis = ["â¨","ð¥","ð¡","ð¯","ð","ðª","ð","â¡"]
        e = random.choice(emojis)
        style = "ð§µ [Story format]" if variant=="B" else "ð¡ [Tips format]"
        return (f"{e} {h.upper()}\n\n{style}\n\n[Main value about {topic_short}]\n\n"
                f"Save & share if helpful â»ï¸\n\n"
                f"#{topic_short.replace(' ','')} #{pillar.replace(' ','')} #ContentCreator #GrowthMindset")
    elif platform == "tiktok":
        return (f"POV: You just learned the {topic_short} secret nobody talks about ð\n\n"
                f"[Hook: surprising statement]\n[Main value in 3 points]\n[CTA: Follow for more]\n\n"
                f"#{topic_short.replace(' ','')} #{pillar.replace(' ','')} #LearnOnTikTok #fyp")
    else:  # threads
        return (f"{h}\n\n[Your honest take on {topic_short}]\n\n"
                f"{'What do you think? ð' if variant=='A' else 'Share your experience below ð¬'}")

# Build calendar
calendar = []
for week in range(1, WEEKS+1):
    for platform in PLATFORMS:
        times = BEST_TIMES.get(platform, BEST_TIMES["twitter"])
        for day_idx in range(min(PPW,7)):
            pillar       = PILLARS[day_idx % len(PILLARS)]
            content_form = get_format(pillar)
            day_name, best_time = times[day_idx % len(times)]
            post_date    = TODAY + timedelta(weeks=week-1, days=day_idx)
            caption_a    = gen_caption(platform, pillar, content_form, week, "A")
            caption_b    = gen_caption(platform, pillar, content_form, week, "B") if AB_VARIANTS else ""
            calendar.append({
                "week": week, "platform": platform,
                "date": post_date.strftime("%b %d"),
                "iso_date": post_date.strftime("%Y-%m-%d"),
                "day": day_name, "best_time": best_time,
                "pillar": pillar, "format": content_form,
                "caption_a": caption_a, "caption_b": caption_b,
            })

# Display overview table
console.print()
tbl = Table(title=f"ð {WEEKS}-Week Calendar â {len(calendar)} posts", box=box.ROUNDED, border_style="cyan")
tbl.add_column("Wk", width=4, style="dim")
tbl.add_column("Date", width=8, style="cyan")
tbl.add_column("Platform", width=12, style="yellow")
tbl.add_column("Day", width=5)
tbl.add_column("Time", width=6, style="green")
tbl.add_column("Pillar", width=14, style="magenta")
tbl.add_column("Format", width=16)
tbl.add_column("A/B", width=4) if AB_VARIANTS else None
for e in calendar:
    row = [str(e["week"]),e["date"],e["platform"].title(),e["day"],e["best_time"],e["pillar"].title(),e["format"]]
    if AB_VARIANTS: row.append("â")
    tbl.add_row(*row)
console.print(tbl)

# Show sample captions with A/B
console.print()
shown = set()
for e in calendar:
    if e["platform"] not in shown:
        shown.add(e["platform"])
        console.print(Panel(e["caption_a"],title=f"[bold]ð Sample A â {e['platform'].title()}[/bold]",border_style="yellow"))
        if AB_VARIANTS and e["caption_b"]:
            console.print(Panel(e["caption_b"],title=f"[bold]ð Sample B â {e['platform'].title()} (variant)[/bold]",border_style="dim yellow"))

# Pro: Repurposing strategy
console.print()
repurpose = [
    f"Twitter thread â LinkedIn article: expand your top-performing thread into a 600-word LinkedIn post",
    f"Instagram carousel â Twitter thread: extract 5 slides into 5 tweet points",
    f"LinkedIn article â TikTok script: take your 3 main points and make a 60-second explainer",
    f"Twitter poll results â Instagram Story: share the data as a 'My audience says...' post",
    f"Blog post â 4 Tweets: one for intro, one per section, one for the conclusion with link",
]
console.print(Panel("\n".join(f"â¢ {r}" for r in repurpose),
    title="â»ï¸ Repurposing Strategy", border_style="magenta"))

# Pro: 20 content angle ideas
topic_ideas = [
    f"Beginner's guide to {TOPIC}", f"Common {TOPIC} mistakes and how to fix them",
    f"Advanced {TOPIC} strategies most people skip", f"{TOPIC} tools comparison 2025",
    f"Day in the life: applying {TOPIC} principles", f"The {TOPIC} checklist I use every day",
    f"What I learned after 1 year of focusing on {TOPIC}", f"{TOPIC} myths debunked",
    f"Quick wins: {TOPIC} results in 30 days", f"{TOPIC} for complete beginners",
    f"The {TOPIC} framework I teach my clients", f"Why most {TOPIC} advice is wrong",
    f"{TOPIC} and productivity: what actually works", f"My {TOPIC} stack in 2025",
    f"The uncomfortable truth about {TOPIC}", f"Hot take: {TOPIC} is overrated / underrated",
    f"Behind the scenes of my {TOPIC} process", f"Q&A: your {TOPIC} questions answered",
    f"{TOPIC} in 5 minutes a day: is it possible?", f"The future of {TOPIC}",
]
console.print()
ti_lines = "\n".join(f"[dim]{i+1:02d}.[/dim] {idea}" for i,idea in enumerate(topic_ideas))
console.print(Panel(ti_lines, title="[bold]ð¡ 20 Content Angle Ideas[/bold]", border_style="magenta"))

# Save JSON + CSV (Buffer-ready)
topic_slug = re.sub(r"[^a-z0-9]","_",TOPIC[:20].lower())
json_path  = f"talos_pro_{topic_slug}_{TODAY}.json"
csv_path   = f"talos_pro_{topic_slug}_{TODAY}.csv"
md_path    = f"talos_pro_{topic_slug}_{TODAY}.md"

with open(json_path,"w",encoding="utf-8") as f:
    json.dump({"topic":TOPIC,"weeks":WEEKS,"platforms":PLATFORMS,"calendar":calendar,"generated":str(TODAY)},f,indent=2)

with open(csv_path,"w",newline="",encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["date","platform","pillar","format","best_time","caption_a","caption_b"])
    for e in calendar:
        writer.writerow([e["iso_date"],e["platform"],e["pillar"],e["format"],e["best_time"],e["caption_a"],e.get("caption_b","")])

with open(md_path,"w",encoding="utf-8") as f:
    f.write(f"# â¡ Talos Pro â {WEEKS}-Week Social Calendar â {TOPIC}\n\n")
    f.write(f"**Generated:** {TODAY}  **Platforms:** {', '.join(PLATFORMS)}  **Posts/wk:** {PPW}\n\n")
    shown = set()
    for e in calendar:
        if e["platform"] not in shown:
            shown.add(e["platform"])
            f.write(f"## {e['platform'].title()} Sample\n\n**Caption A:**\n{FENCE}\n{e['caption_a']}\n{FENCE}\n\n")
            if e.get("caption_b"): f.write(f"**Caption B (variant):**\n{FENCE}\n{e['caption_b']}\n{FENCE}\n\n")

console.print()
console.print(Panel(
    f"[green]â Done![/green]\n\n"
    f"ð [cyan]{json_path}[/cyan]\n"
    f"ð [cyan]{csv_path}[/cyan]  â Import to Buffer/Hootsuite/Later directly\n"
    f"ð [cyan]{md_path}[/cyan]",
    title="Exports", border_style="green"
))
```

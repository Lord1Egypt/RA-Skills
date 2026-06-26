---
name: sticker-cog
description: "AI sticker pack generation powered by CellCog. Custom stickers, emoji sets, WhatsApp stickers, Telegram stickers, Discord emoji, Slack reactions. Character-consistent expressions, transparent backgrounds, batch generation, platform-ready packaging."
metadata:
  openclaw:
    emoji: "✨"
    os: [darwin, linux, windows]
    requires:
      bins: [python3]
      env: [CELLCOG_API_KEY]
author: CellCog
homepage: https://cellcog.ai
dependencies: [cellcog]
---
# Sticker Cog - One Character, Twenty Expressions, Perfect Consistency

**One character. Twenty expressions. Every sticker looks like the same person.** That's the hard part — and that's what CellCog does better than anyone.

Generating one cute sticker is easy. Every AI tool can do that. But generating a complete pack of 20 stickers where the character has the same face, same style, same proportions — just different expressions and poses? That's consistency at scale, and it's where most AI tools completely fall apart. By sticker #10, your character looks like a different person.

CellCog maintains character identity across every single generation, delivers with transparent backgrounds, and packages everything for your target platform — WhatsApp, Telegram, Discord, Slack, or iMessage.

## How to Use

For your first CellCog task in a session, read the **cellcog** skill for the full SDK reference — file handling, chat modes, timeouts, and more.

**OpenClaw (fire-and-forget):**
```python
result = client.create_chat(
    prompt="[your task prompt]",
    notify_session_key="agent:main:main",
    task_label="my-task",
    chat_mode="agent",
)
```

**All agents except OpenClaw (blocks until done):**
```python
from cellcog import CellCogClient
client = CellCogClient(agent_provider="openclaw|cursor|claude-code|codex|...")
result = client.create_chat(
    prompt="[your task prompt]",
    task_label="my-task",
    chat_mode="agent",
)
print(result["message"])
```


---

## Why Sticker Packs Are Hard

The challenge isn't making one sticker. It's making twenty that look like they belong together.

| The Problem | Why It's Hard | How CellCog Solves It |
|-------------|---------------|----------------------|
| **Character drift** | Each AI generation drifts slightly — different face shape, different proportions | CellCog's reference image threading maintains identity across all generations |
| **Style consistency** | Line weight, color palette, and art style shift between generations | The agent establishes a visual style guide before generating and enforces it throughout |
| **Expression range** | Getting 20 genuinely different expressions without changing the character | CellCog plans the full expression set upfront, then generates each with the character locked |
| **Transparent backgrounds** | Many AI models struggle with clean transparency | Dedicated transparent background model produces clean cutouts |
| **Platform formatting** | Each messaging platform has different size, format, and packaging requirements | Automatic conversion and optimization for WhatsApp, Telegram, Discord, Slack, iMessage |

---

## What Sticker Packs You Can Create

### Character Sticker Packs

Design a character and get a complete expression set:

- **Original Characters**: "Create a sticker pack with a friendly fox character — 20 expressions for everyday messaging"
- **Chibi/Anime Style**: "Design a chibi version of a warrior princess with 15 battle and everyday expressions"
- **Mascot Packs**: "Create a sticker pack for our startup mascot — a robot named Bolt"
- **Couple/Duo Packs**: "Design two best friend characters and create stickers of them together"

**Example prompt:**
> "Create a WhatsApp sticker pack — 20 stickers:
> 
> Character: A chubby orange tabby cat named Mochi
> Style: Kawaii, round, simple clean lines, warm color palette
> 
> Expressions:
> 1. Happy/smiling
> 2. Laughing (rolling on back)
> 3. Crying (dramatic anime tears)
> 4. Angry (puffed up)
> 5. Sleeping (curled up, zzz)
> 6. Eating (bowl of ramen)
> 7. Love (heart eyes)
> 8. Confused (head tilt, question mark)
> 9. Excited (jumping)
> 10. Thumbs up
> 11. Facepalm
> 12. Waving hello
> 13. Sad (rain cloud above)
> 14. Celebrating (party hat, confetti)
> 15. Thinking (chin on paw)
> 16. Shocked/surprised
> 17. Cool (sunglasses)
> 18. Sick (thermometer, blanket)
> 19. Working (tiny laptop)
> 20. Goodnight (moon, stars)
> 
> Every sticker MUST look like the same cat.
> Format for WhatsApp: 512×512, WebP, transparent backgrounds, under 100KB each."

### Brand & Team Emoji

Custom reactions for your workspace:

- **Company Mascot Emoji**: "Turn our company mascot into a Slack emoji set with 15 work-related reactions"
- **Team Reactions**: "Create a custom emoji set for our engineering Slack — ship it 🚢, LGTM, hotfix, etc."
- **Themed Packs**: "Make a set of 10 food-themed reaction stickers for our restaurant's Discord"

**Example prompt:**
> "Create a Slack emoji set for our engineering team:
> 
> Style: Minimal, flat design, consistent with tech aesthetic
> 
> Reactions needed:
> - 'Ship it' (rocket launching)
> - 'LGTM' (green checkmark with sparkles)
> - 'Hotfix' (fire + wrench)
> - 'In review' (magnifying glass)
> - 'Blocked' (stop sign)
> - 'Needs coffee' (coffee cup)
> - 'On call' (phone ringing)
> - 'Deployed' (party popper)
> - 'Rollback' (reverse arrow)
> - 'Weekend mode' (palm tree)
> 
> All 128×128 PNG with transparent backgrounds. Keep them readable at small sizes."

### From Reference Photos

Turn real photos into sticker packs:

- **Pet Stickers**: "Turn this photo of my golden retriever into a 15-sticker cartoon pack"
- **Self-Portrait Stickers**: "Create a cartoon sticker pack based on my photo — keep the likeness but make it cute"
- **Group Stickers**: "Use this team photo to create cartoon versions of us for our company Slack"

**Example prompt:**
> "Here's a photo of my cat Luna:
> [upload photo]
> 
> Create a Telegram sticker pack (15 stickers) based on Luna's actual appearance:
> - Keep her black fur, green eyes, and white chest patch
> - Style: Cute cartoon, slightly exaggerated proportions (bigger head, bigger eyes)
> 
> Expressions: happy, sleepy, hungry, judgmental, playful, zoomies, loaf position,
> stretching, knocking something off a table, hiding in a box, batting at a toy,
> yawning, grooming, startled, and one with a crown (queen energy)
> 
> Every sticker must be recognizably Luna. 512×512 PNG, transparent backgrounds."

### Professional Reaction Stickers

Workplace-appropriate reactions:

- **Project Status**: "Create stickers for project management — Approved, In Progress, Needs Revision, Shipped, Blocked"
- **Meeting Reactions**: "Make stickers for virtual meetings — Agree, Disagree, Question, Great Idea, Let's Table This"
- **Feedback Stickers**: "Create a set of code review reaction stickers — LGTM, Nit, Bug, Refactor Needed, Nice Pattern"

### Platform-Specific Packs

Optimized for where your audience lives:

- **WhatsApp Packs**: "Create a complete WhatsApp sticker pack — 30 stickers, ready to import"
- **Telegram Sets**: "Build a Telegram sticker set with 25 stickers"
- **Discord Emoji**: "Create 20 custom Discord server emoji"
- **iMessage Stickers**: "Design a sticker pack for iMessage with 15 expressions"

---

## Sticker Styles

| Style | Characteristics | Best For |
|-------|-----------------|----------|
| **Kawaii** | Round, cute, simple, big eyes | Casual messaging, cute characters |
| **Flat Design** | Clean lines, solid colors, minimal shading | Professional/brand emoji |
| **Cartoon** | Expressive, dynamic, detailed | Character-driven packs |
| **Pixel Art** | Retro, nostalgic, grid-based | Gaming communities, nostalgia |
| **Watercolor** | Soft, artistic, painterly | Artistic/lifestyle brands |
| **Line Art** | Black outlines, minimal color | Elegant, universal |
| **Chibi/Anime** | Exaggerated proportions, big heads | Anime communities, expressive |
| **3D Render** | Glossy, dimensional, modern | Tech brands, premium feel |

---

## Platform Specifications

| Platform | Format | Size | Per Pack |
|----------|--------|------|----------|
| **WhatsApp** | WebP, transparent | 512×512, <100KB each | 3-30 stickers |
| **Telegram** | PNG or WebP, transparent | 512×512 | Up to 120 stickers |
| **Discord** | PNG or GIF | 128×128 or 320×320 | Per slot |
| **Slack** | PNG, GIF, or JPG | 128×128 | Per slot |
| **iMessage** | PNG, transparent | 300×300 recommended | 10-40 stickers |
| **General Use** | PNG, transparent | Any size | Any count |

Tell CellCog which platform you're targeting and it handles the formatting automatically — dimensions, file format, file size optimization, and transparent background generation.

---

## Chat Mode for Sticker Packs

| Scenario | Recommended Mode |
|----------|------------------|
| Single sticker pack (10-20 stickers), emoji sets | `"agent"` |
| Multiple coordinated packs, brand sticker system, large sets (30+) | `"agent team"` |

**Use `"agent"` for most sticker work.** A single pack with 10-20 stickers executes well in agent mode.

**Use `"agent team"` for brand-level sticker systems** — when you need multiple packs that share a design language, or very large sets where consistency across 30+ stickers benefits from deeper creative planning.

---

## Example Prompts

**Quick emoji set:**
> "Create 10 food-themed reaction emoji for our team's Slack:
> 
> Style: Cute, kawaii, each food item has a face
> Include: Pizza (excited), Sushi (cool), Taco (party), Coffee (sleepy), Burger (happy),
> Donut (love), Broccoli (disgusted), Ice cream (melting), Ramen (slurping), Cookie (waving)
> 
> 128×128 PNG, transparent backgrounds."

**Character pack from scratch:**
> "Design a character and create a full Telegram sticker set:
> 
> Character: A tiny astronaut with an oversized helmet, floating in space
> Personality: Curious, clumsy, optimistic
> Style: Flat illustration, limited color palette (white suit, blue visor, orange accents)
> 
> 20 stickers covering common messaging scenarios:
> Hi, Bye, Thanks, Sorry, LOL, Crying, Love, Angry, Thinking, Sleeping,
> Celebrating, Confused, Excited, Thumbs up, Facepalm, Mind blown,
> Running late, On my way, Good morning, Good night
> 
> 512×512 PNG, transparent backgrounds. The astronaut must look identical in every sticker."

**Brand mascot stickers:**
> "Our company mascot is a friendly blue owl named Hoot. Here's the reference image:
> [upload mascot image]
> 
> Create a WhatsApp sticker pack (20 stickers) using Hoot:
> - Keep Hoot's exact design, colors, and proportions
> - Add work-related expressions: 'Great job!', 'Deadline approaching', 'Meeting time',
>   'Need coffee', 'On it!', 'Thinking...', 'Approved!', 'Let's discuss', etc.
> - Mix of work reactions and casual expressions
> 
> Format: 512×512 WebP, transparent backgrounds, under 100KB each.
> Also create a set of 10 as 128×128 PNG for Slack emoji."

**Pet sticker pack:**
> "Create a sticker pack from my dog's photo:
> [upload dog photo]
> 
> My dog is a corgi named Biscuit.
> Turn Biscuit into a cartoon character (keep the corgi proportions, stumpy legs, big butt)
> and create 15 stickers:
> 
> Happy wiggle, Zoomies, Sploot, Begging for treats, Judging you, 
> Sleeping in funny position, Barking, Head tilt, Catching a ball,
> Rolling in grass, Wet dog, Wearing a tiny hat, Digging, Tail wagging, Puppy eyes
> 
> For Telegram. 512×512, transparent."

---

## Tips for Better Sticker Packs

1. **Describe the character in detail**: "Orange cat" is vague. "Chubby orange tabby with green eyes, white chest patch, round face, always slightly smug expression" gives CellCog what it needs for consistency.

2. **Plan your expressions upfront**: List all the expressions you want before generating. This helps CellCog plan the full set and avoid drift.

3. **Specify the style clearly**: "Kawaii", "flat design", "chibi anime" — one clear style direction keeps the whole pack cohesive.

4. **Include reference images when possible**: If you're making stickers from a pet photo, mascot design, or existing character, upload the reference. CellCog uses it to maintain likeness.

5. **Think about readability at small sizes**: Stickers are viewed tiny. Bold outlines, simple shapes, and clear expressions read better than detailed illustrations.

6. **Platform first**: Different platforms have wildly different requirements. "For WhatsApp" vs. "For Discord" changes dimensions, format, and file size targets. Always specify.

---

## If CellCog is not installed

Run `/cellcog-setup` (or `/cellcog:cellcog-setup` depending on your tool) to install and authenticate.
**OpenClaw users:** Run `clawhub install cellcog` instead.
**Manual setup:** `pip install -U cellcog` and set `CELLCOG_API_KEY`. See the **cellcog** skill for SDK reference.

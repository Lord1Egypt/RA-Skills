---
name: slides-cog
description: "AI presentation and slide deck generation powered by CellCog. Pitch decks, keynotes, business presentations, educational slides, investor decks — PDF or native PPTX. Research-backed content with professional slide design, charts, and layouts."
metadata:
  openclaw:
    emoji: "📽️"
    os: [darwin, linux, windows]
    requires:
      bins: [python3]
      env: [CELLCOG_API_KEY]
author: CellCog
homepage: https://cellcog.ai
dependencies: [cellcog]
---
# Slides Cog - Content Worth Presenting, Design Worth Looking At

**Great slides need two things: content worth presenting and design worth looking at.** CellCog takes both seriously.

- **Content:** Your prompt can be minimal — CellCog researches and fills in substance, not filler
- **Design:** PDF slides or native PPTX, with layouts, typography, and visuals you can present as-is

Pitch decks, keynotes, board presentations, image slideshows — ready to present, not ready to fix.

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

## Output Formats

CellCog generates presentations in multiple formats. Each has its strengths:

### PDF (Default for Ambiguous Requests)

When you say "create a presentation" or "make a slide deck" without specifying a format, CellCog generates PDF:
- Full control over layout, typography, and design
- Perfect rendering across all devices
- Professional, polished results every time
- Supports images, charts, complex layouts without compromise

### PPTX (First-Class Support)

When you explicitly request PPTX ("create a PowerPoint", "make a .pptx"), CellCog generates native PowerPoint directly:
- Editable slides — your team can modify, reorder, and customize
- Compatible with PowerPoint, Google Slides, and Keynote
- Professional layouts with proper slide masters and formatting
- Great for collaborative workflows where multiple people contribute

**Just ask for PPTX and you'll get it.** No need to justify why you want an editable format.

---

## What Presentations You Can Create

### Pitch Decks

Investor and stakeholder presentations:

- **Startup Pitch**: "Create a 12-slide pitch deck for a fintech startup disrupting small business lending"
- **Investor Update**: "Build a quarterly investor update presentation covering metrics, milestones, and roadmap"
- **Funding Ask**: "Create a Series A pitch deck for an AI healthcare company seeking $5M"

### Business Presentations

Corporate and professional presentations:

- **Quarterly Business Review**: "Create a QBR presentation covering sales performance, challenges, and next quarter plans"
- **Strategy Presentation**: "Build a strategic planning presentation for entering the European market"
- **Board Deck**: "Create a board meeting presentation with financials, KPIs, and key decisions needed"
- **Project Proposal**: "Build a project proposal presentation for implementing a new CRM system"

### Sales Presentations

Customer-facing decks:

- **Product Demo Deck**: "Create a product demo presentation for our project management software"
- **Capabilities Deck**: "Build a company capabilities presentation for enterprise sales"
- **Case Study Presentation**: "Create a case study presentation showing how Client X achieved 3x ROI"
- **Pricing Presentation**: "Build a pricing and packaging presentation for our three tiers"

### Educational Presentations

Teaching and training content:

- **Course Slides**: "Create lecture slides for an introduction to machine learning"
- **Training Deck**: "Build employee onboarding slides covering company culture and policies"
- **Workshop Presentation**: "Create workshop slides for a design thinking session"
- **Tutorial Slides**: "Build a step-by-step tutorial presentation for using Excel pivot tables"

### Event Presentations

Conferences and special events:

- **Keynote**: "Create a keynote presentation on the future of artificial intelligence"
- **Conference Talk**: "Build a 20-minute conference presentation on scaling engineering teams"
- **All-Hands**: "Create an all-hands meeting presentation covering company updates and wins"
- **Product Launch**: "Build a product launch presentation for unveiling our new feature"

### Image Slideshows

Visual storytelling with images:

- **Portfolio Slideshow**: "Create a photography portfolio slideshow with minimal text"
- **Travel Presentation**: "Build a vacation recap slideshow with photos and captions"
- **Event Highlights**: "Create an event highlight slideshow from conference photos"
- **Visual Story**: "Build a brand story slideshow using images and minimal text"

---

## Presentation Features

CellCog presentations can include:

| Element | Description |
|---------|-------------|
| **Title Slides** | Bold, impactful opening slides |
| **Content Slides** | Text, bullets, and layouts |
| **Charts & Graphs** | Bar, line, pie, and more |
| **Images** | AI-generated or placeholder for your images |
| **Data Tables** | Clean, formatted tables |
| **Timelines** | Visual timelines and roadmaps |
| **Comparison Slides** | Side-by-side comparisons |
| **Quote Slides** | Testimonials and callouts |

---

## Output Format Summary

| Format | When to Use |
|--------|-------------|
| **PDF** | Default when no format specified — polished, presentation-ready |
| **PPTX** | When you request PowerPoint — editable, collaborative, team workflows |
| **Interactive HTML** | Web-based presentations, internal tools |

---

## Chat Mode for Presentations

| Scenario | Recommended Mode |
|----------|------------------|
| Standard decks, educational slides, image slideshows, training materials | `"agent"` |
| Investor pitch decks, board presentations, keynotes requiring narrative craft | `"agent team"` |

**Use `"agent"` for most presentations.** Standard business decks, training materials, and informational slides execute well in agent mode.

**Use `"agent team"` for high-stakes presentations** where narrative flow, persuasion, and multi-angle thinking matter—investor pitches, board decks, conference keynotes where every slide needs to build a compelling story.

---

## Example Presentation Prompts

**Startup pitch deck:**
> "Create a 12-slide Series A pitch deck for 'DataSync' - a B2B SaaS company that helps enterprises sync data across cloud applications.
> 
> Include slides for: Problem, Solution, Product Demo, Market Size, Business Model, Traction, Team, Competition, Go-to-Market, Financials, Ask, Contact.
> 
> Key metrics: $50K MRR, 30 customers, 15% MoM growth, seeking $5M for expansion.
> 
> Modern, professional design. Blue and white color scheme."

**Quarterly business review:**
> "Create a QBR presentation for Q4 2025:
> 
> 1. Executive Summary
> 2. Revenue Performance (hit 95% of target)
> 3. Customer Metrics (NPS improved to 72)
> 4. Key Wins (3 enterprise deals closed)
> 5. Challenges (churn increased in SMB segment)
> 6. Q1 2026 Priorities
> 7. Resource Asks
> 
> Include relevant charts. Corporate professional style."

**Educational slides:**
> "Create a 15-slide presentation for teaching 'Introduction to Python Programming':
> 
> 1. What is Python?
> 2. Why Learn Python?
> 3. Setting Up Your Environment
> 4. Variables and Data Types
> 5. Basic Operations
> 6. Strings
> 7. Lists
> 8. Conditionals (if/else)
> 9. Loops
> 10. Functions
> 11. Simple Project: Calculator
> 12. Resources for Learning More
> 
> Beginner-friendly, include code examples, clean modern design."

**Image slideshow:**
> "Create a visual slideshow presentation showcasing 10 images of modern architecture around the world. Each slide should have: one stunning building image, the building name, location, and architect. Minimal text, maximum visual impact. Generate the images."

**PowerPoint presentation:**
> "Create a 10-slide sales deck as PPTX. Our team needs to customize it for different clients before presenting."

---

## Tips for Better Presentations

1. **Specify slide count**: "10-12 slides" helps scope appropriately. Pitch decks are typically 10-15 slides. Training can be 20-30.

2. **List the slides you want**: Even a rough outline helps. "Include: Problem, Solution, Market, Team, Ask."

3. **Provide key content**: Actual metrics, quotes, and facts make better slides than placeholders.

4. **Design direction**: "Minimal and modern", "Corporate professional", "Bold and colorful", specific colors.

5. **Mention the audience**: "For investors", "For technical team", "For executives" changes tone and detail level.

6. **Choose your format**: PDF is the default for polished output. Request PPTX when your team needs to edit or customize the slides.

---

## If CellCog is not installed

Run `/cellcog-setup` (or `/cellcog:cellcog-setup` depending on your tool) to install and authenticate.
**OpenClaw users:** Run `clawhub install cellcog` instead.
**Manual setup:** `pip install -U cellcog` and set `CELLCOG_API_KEY`. See the **cellcog** skill for SDK reference.

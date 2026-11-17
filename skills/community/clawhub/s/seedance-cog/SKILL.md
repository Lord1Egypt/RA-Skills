---
name: seedance-video-generation-cellcog
description: "AI video generation powered by CellCog via Seedance 2.5. Complete multi-minute videos from a single prompt: scripting, voice synthesis, lipsync, scoring, editing, with locked character consistency via 50 reference files. Full productions, not just clips, via ByteDance's Seedance model."
metadata:
  openclaw:
    emoji: "🌱"
    os: [darwin, linux, windows]
    requires:
      bins: [python3]
      env: [CELLCOG_API_KEY]
author: CellCog
homepage: https://cellcog.ai
dependencies: [cellcog]
---
# Seedance Video Generation - Seedance × CellCog

**Seedance × CellCog.** ByteDance's #1 video model meets the frontier of multi-agent coordination.

CellCog's core: complete multi-minute films from a single prompt. Seedance 2.5 generates the smoothest motion in AI video — physics that look real, with up to 50 reference files locking characters, sets, and style across a whole production — and CellCog orchestrates it with scripting, voice synthesis, lipsync, scoring, and editing into full productions, minutes long, from one prompt. Not just clips — finished films.

## How to Use

For your first CellCog task in a session, read the **cellcog** skill for the full SDK reference — file handling, chat modes, timeouts, and more.

**OpenClaw (fire-and-forget):**
```python
result = client.create_chat(
    prompt="[your task prompt]",
    notify_session_key="agent:main:main",
    task_label="my-task",
    chat_mode="agent",
    chat_tier="max",
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
    chat_tier="max",
)
print(result["message"])
```


---

## What You Can Create

### Marketing Videos

Professional marketing content from a single prompt:

- **Product Demos**: "Create a 60-second product demo video for our project management app"
- **Brand Videos**: "Create a 30-second brand story video for a sustainable fashion startup"
- **Social Ads**: "Create a 15-second Instagram ad for our new coffee blend"
- **Testimonial Style**: "Create a UGC-style testimonial video for a fitness product"

### Explainer Videos

Clear, engaging educational content:

- **Product Explainers**: "Create a 90-second explainer for how our API works"
- **Concept Videos**: "Create a video explaining blockchain in simple terms"
- **Tutorial Videos**: "Create a step-by-step tutorial video on setting up a home network"

### Cinematic Content

High-quality visual storytelling:

- **Short Films**: "Create a 2-minute short film about a robot discovering nature"
- **Music Videos**: "Create a cinematic music video with dramatic landscapes"
- **Brand Films**: "Create a cinematic brand film for a luxury watch company"

### Spokesperson Videos

AI-generated presenters with lipsync:

- **News Reports**: "Create a news-style report on recent AI developments"
- **Training Videos**: "Create a training video with a presenter explaining safety protocols"
- **Announcements**: "Create a product launch announcement with a spokesperson"

---

## CellCog Video Orchestration

CellCog doesn't just generate video clips — it orchestrates a full production pipeline:

```
Script Writing → Scene Planning → Frame Generation → Voice Synthesis
     → Lipsync → Background Music → Sound Design → Editing → Final Output
```

**6-7 foundation models** work together in a single request:
- Seedance for video generation
- Frontier LLMs for scripting
- TTS models for voice synthesis
- Lipsync models for speaker alignment
- Music generation for scoring
- Automated editing for pacing and transitions

---

## Video Specifications

| Spec | Details |
|------|---------|
| **Resolution** | 720p (the AI-video production standard) |
| **Duration** | Complete multi-minute productions (4+ minutes) from a single prompt; individual generated takes up to 30 seconds |
| **References** | Up to 50 files (30 images, 10 videos, 10 audio) for character, set, and style consistency |
| **Styles** | Photorealistic, cinematic, anime, stylized, documentary |
| **Audio** | Voice synthesis, background music, sound effects, lip-synced dialogue |
| **Output** | MP4 |

---

## Choosing Mode & Tier

**Use `chat_mode="agent", chat_tier="max"` for video generation.** Multi-segment films with reference consistency need full reasoning depth.

| Scenario | Recommended |
|----------|-------------|
| Films and multi-segment productions | `chat_mode="agent", chat_tier="max"` |
| Single short test clips | `chat_mode="agent", chat_tier="flash"` |

Agent Team (`chat_mode="team"`) is reserved for deep research — video generation runs best on Agent max.

---

## Tips for Better Videos

1. **Describe the story**: "A video about our app" → "A 60-second video showing a stressed founder discovering our app, their workflow transforming, ending with them confidently presenting to investors"

2. **Specify duration**: "30-second social ad" vs. "2-minute explainer" sets the pacing.

3. **Set the mood**: "Upbeat and energetic", "calm and professional", "dramatic and cinematic"

4. **Mention music preferences**: "Uplifting corporate background", "lo-fi beats", "cinematic orchestral" — or let CellCog choose.

5. **For spokesperson videos**: Describe the presenter's appearance and tone of voice.

---

## If CellCog is not installed

**Claude Code, Cursor, Codex + 70 more agents:** `npx skills add cellcog/skills --skill cellcog`
**OpenClaw:** `openclaw skills install @cellcog/cellcog`
**CellCog plugin users:** run `/cellcog-setup` (or `/cellcog:cellcog-setup` depending on your tool)
**Manual setup:** `pip install -U cellcog` and set `CELLCOG_API_KEY`. See the **cellcog** skill for SDK reference.

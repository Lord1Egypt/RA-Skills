# Content & Creative (OpenClaw Optimized)

This reference defines high-performance creative production workflows for AI agents in the OpenClaw environment, merging AI-native tools with professional design standards.

## 1. Visual Design & Image Generation

### The Ryder Design Philosophy
Before generating any visual, the agent should define a **Visual Philosophy** (e.g., "Brutalist Joy", "Chromatic Silence") to ensure consistency across assets.

### AI Image Workflow
- **Tools**: Use `web_search` to find reference images for style and `subagent spawn` with a "Creative Director" persona to refine prompts.
- **Prompts**: Structure prompts as: `[Style] [Subject] [Composition] [Palette] [Lighting] [Quality]`.
- **Reference Images**: Use the `images` parameter in generation tools to perform style transfers or edits (img2img).

---

## 2. Brand Identity & Voice

### 12-Archetype System
Agents should align every piece of content with a primary and secondary brand archetype (e.g., The Creator + The Sage).

### Voice Consistency Audit
Before "shipping" content, the agent must run a check against:
- **Formality**: (Formal ↔ Casual)
- **Directness**: (Imperative ↔ Narrative)
- **Archetype Fit**: Does it sound like [Archetype]?

---

## 3. Frontend Design & Web Artifacts

### Stack Selection
- **Simple**: Plain HTML/CSS/JS.
- **Interactive**: React + Tailwind + shadcn/ui.
- **Deployment**: Use `exec` to deploy artifacts to a staging directory or public URL if configured.

---

## 4. Audio & Speech Synthesis

### Voice Casting & Production
- **Single Speaker**: Use Gemini TTS for standard professional reads.
- **Dialogue**: Use JSON-formatted speaker assignments for multi-voice interactions.
- **Post-Processing**: Use `exec` with `ffmpeg` to trim silence or normalize audio levels.

---

## 5. Content Creation & Copywriting

### The Multi-Channel Engine
1. **Research**: Use `web_search` for trending topics and `web_fetch` for competitor content audits.
2. **Frameworks**: 
   - **AIDA**: Attention, Interest, Desire, Action.
   - **PAS**: Problem, Agitate, Solution.
3. **Repurposing**: Turn one long-form blog post into 10+ assets (Twitter threads, LinkedIn carousels, etc.) using `subagent spawn` for parallel drafting.

---

## 6. Content Calendar & Distribution

### Automated Scheduling
- **Tracking**: Maintain a `CONTENT_CALENDAR.csv` in the workspace.
- **Reminders**: Use `heartbeat` to notify the human when content is ready for review or scheduled for posting.

---
*Derived from Perplexity Super-Skills & Claude Code. Optimized for OpenClaw by Ryder.*

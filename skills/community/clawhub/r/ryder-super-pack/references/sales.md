# Sales (OpenClaw Optimized)

This reference defines high-performance sales workflows for AI agents in the OpenClaw environment, merging real-time research with structured sales frameworks.

## 1. Account Research & Prospect Intelligence

### The Ryder Research Workflow
1. **Live Intel**: Use `web_search` to find recent funding, hiring signals, and news.
2. **Contact Deep-Dive**: Use `web_search` for "[Name] [Company] LinkedIn" to find tenure and background.
3. **Synthesis**: Create a `RESEARCH_[COMPANY].md` file with:
   - **Quick Take**: 2-sentence hook.
   - **Positive Signals**: Why now?
   - **Recommended Approach**: Who to contact and what to say.

---

## 2. Call Prep & Meeting Readiness

### Pre-Call Briefing
- **Trigger**: "Prep me for my call with [Company]."
- **Action**: Run the Ryder Research Workflow + check `memory/` for prior interactions.
- **Output**: A structured prep brief including:
  - **Attendee Archetypes**: (e.g., Economic Buyer, Technical Evaluator).
  - **Discovery Questions**: Tailored to their journey stage (Awareness, Evaluation, etc.).
  - **Likely Objections**: And how to handle them.

---

## 3. Competitive Intelligence & Positioning

### Tactical Battlecards
- **On-Demand**: Generate a `BATTLECARD_[COMPETITOR].md`.
- **Landmine Questions**: 3 questions to ask the prospect that expose competitor weaknesses.
- **Differentiators**: Clear "Us vs. Them" matrix based on the latest `web_fetch` of their site.

---

## 4. Outreach & Content Creation

### Research-First Outreach
- **The Golden Rule**: Never send generic copy.
- **Hook Selection**: Use real-time triggers (funding, new hire) found via `web_search`.
- **AIDA Structure**:
  - **Attention**: The personalized hook.
  - **Interest**: Their specific pain point.
  - **Desire**: A relevant proof point (case study).
  - **Action**: Low-friction CTA.

---

## 5. Sales Assets & Deliverables

### Agent-Assisted Asset Creation
- **One-Pagers**: Use `write` to create a `PROPOSAL_[COMPANY].md` based on discovery notes.
- **Follow-up Emails**: Use `subagent spawn` with the "Sales Copywriter" persona to draft high-conversion follow-ups.

---
*Derived from Perplexity Super-Skills & Claude Code. Optimized for OpenClaw by Ryder.*

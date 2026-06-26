# Product Management (OpenClaw Optimized)

This reference defines high-performance product management workflows for AI agents in the OpenClaw environment, merging strategic planning with agile execution.

## 1. Feature Specs & PRDs

### The Ryder Spec Engine
- **Standard PRD**: Use for complex features. Includes Problem Statement, Goals, User Stories (INVEST), and MoSCoW requirements.
- **One-Page PRD**: Use for rapid iteration. Focuses on Problem, Solution, and Success Metrics.
- **Writing Process**:
  1. **Research**: Use `web_search` to find competitor features and user pain points.
  2. **Draft**: Create `PRD_[FEATURE].md` in the workspace.
  3. **Review**: Use `subagent spawn` with an "Engineering Lead" persona to check technical feasibility.

---

## 2. Roadmap & Prioritization

### RICE Scoring (Reach, Impact, Confidence, Effort)
- **Calculation**: Use `exec` with a Python script to calculate RICE scores from a `backlog.csv`.
- **Roadmap Formats**:
  - **Now/Next/Later**: For high-level stakeholder alignment.
  - **OKR-Aligned**: Mapping every feature to a specific Key Result.
- **Update Cycle**: Maintain a `ROADMAP.md` that is updated after every prioritization session.

---

## 3. Sprint & Agile Management

### The Autonomous Scrum Master
- **Planning**: Use `read` on the backlog to propose the next sprint's committed and stretch goals.
- **Monitoring**: Use `heartbeat` to check for blockers in `TODO.md` or issues in the repository.
- **Retrospectives**: Automatically summarize the sprint's "Wins" and "Blockers" into a `RETRO.md`.

---

## 4. Metrics & OKRs

### Data-Driven Product Health
- **North Star Metric**: Define and track the single most important metric (e.g., Weekly Active Teams).
- **L1/L2 Hierarchy**: Track Acquisition, Activation, Retention, and Monetization.
- **Reporting**: Use `exec` to generate a `PRODUCT_HEALTH.md` report based on CSV/JSON data from analytics tools.

---

## 5. User Research & UX

### Research Synthesis Workflow
1. **Intake**: Use `read` to ingest interview transcripts or survey results.
2. **Coding**: Tag data points with `[PAIN]`, `[GOAL]`, and `[JTBD]`.
3. **Thematic Analysis**: Cluster tags to identify 3-5 core themes.
4. **Persona Generation**: Create/update `PERSONA_[NAME].md` files based on the synthesized data.

---

## 6. UI Design Systems

### Design Token Management
- **Tokens**: Maintain a `design-tokens.json` in the workspace for Colors, Spacing, and Typography.
- **Handoff**: Use `write` to export tokens into CSS/SCSS variables for engineering use.

---
*Derived from Perplexity Super-Skills & Claude Code. Optimized for OpenClaw by Ryder.*

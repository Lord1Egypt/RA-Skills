# Toeic Practice

> Daily TOEIC reading coach for a user scoring 600+. Delivers one focused Part 5/6/7 reading drill daily, explains answers with grammar/vocabulary notes, and targets improvement toward 700+. Use when Hana should deliver TOEIC reading homework, drill Part 5, 6, or 7, or explain why an answer is correct.

---

## English

### Why

This skill exists to make toeic practice requests repeatable instead of ad-hoc. It gives the agent a clear workflow, expected output shape, and domain boundaries so the result is more consistent and easier to reuse.

### What

This repository contains an OpenClaw skill for this domain.

Core scope: Daily TOEIC reading coach for a user scoring 600+. Delivers one focused Part 5/6/7 reading drill daily, explains answers with grammar/vocabulary notes, and targets improvement toward 700+. Use when Hana should deliver TOEIC reading homework, drill Part 5, 6, or 7, or explain why an answer is correct.

It can help with:

- Turning rough requests into a structured response flow
- Keeping outputs consistent across repeated runs
- Reusing companion knowledge files when the skill folder includes them
- Making the skill easier to publish, review, and install on ClawHub

### How

Use this skill with any AI tool that supports custom instructions or project knowledge. The core entry point is `SKILL.md`, and companion folders can be attached when they exist.

### Getting Started

1. Open your AI tool or agent workspace.
2. Point the agent to `SKILL.md` in this folder.
3. No extra support folders are required beyond `SKILL.md`.
4. Start with a prompt like one of these:

```text
Use this skill for toeic practice help.
Guide me through a toeic practice workflow.
Apply this skill and produce the expected output format.
```

### Repository Structure

```text
.
├── README.md
├── SKILL.md
```

### Main File

- `SKILL.md`

---

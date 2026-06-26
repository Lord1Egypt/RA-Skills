---
name: skill-scorer
description: "对任何 SKILL.md（或 skill 文件夹）进行质量评估和打分，基于行业最佳实践，生成 8 维度 100 分制的结构化质检报告，精准定位问题并提供可执行的优化建议。当用户要求评审、审计、评分、检测、质检任何 skill 时使用——哪怕只是说「这个 skill 写得怎么样？」也会触发。也支持：skill质检、skill评分、检测skill。 | Evaluate and score any SKILL.md (or skill folder) against industry best practices. Generates a structured quality report with a 100-point score across 8 dimensions, pinpoints issues, and provides actionable optimization suggestions. Use this skill whenever the user asks to review, audit, evaluate, grade, score, lint, or quality-check a skill — even if they just say 'is this skill any good?' or 'help me improve this skill'. Also triggers on: 'skill review', 'rate my skill'."
version: "1.6.0"
compatibility: "Claude Code, Claude.ai, Cowork, and all SKILL.md-compatible agents"
changelog: |
  1.6.0 — D4 orchestration criteria wording refined: clarified that Playbooks contain descriptive logic (not executable commands), Usage Examples contain executable commands, output merging can live in templates.md. README restructured to Chinese-first bilingual
  1.5.0 — Dimension 4 expanded to 5 skill types: added Script-bundled and MCP-integrated with type-specific scoring criteria
  1.4.0 — Dimension 4 (Workflow & Logic) adds Skill Type Detection: instruction-only / single-command / orchestration evaluated with type-specific criteria
  1.3.0 — Description bilingual: Chinese first, English after, for internal platform display
  1.2.0 — Added input validation and graceful degradation for non-skill files in Step 0
  1.1.0 — Bilingual report output (Chinese first, English after, no interleaving)
  1.0.0 — Initial release with 8-dimension scoring rubric
---

# Skill: skill-scorer

## Overview

A meta-skill that evaluates the quality of other skills. Given a SKILL.md file (or a complete skill folder), it performs a systematic audit across 8 dimensions, assigns a score out of 100, identifies issues by severity, and generates actionable optimization suggestions.

This skill synthesizes quality criteria from Anthropic's official skill authoring best practices, the Skill Engineering Standard (v1.4.3), and community-tested patterns from production skill ecosystems.

## When to Activate

User provides a skill and asks any of:
- "帮我评分/打分/检测/质检 这个 skill"
- "review/audit/score/grade/lint this skill"
- "这个 skill 写得怎么样？" / "is this skill any good?"
- "帮我优化这个 skill" (evaluate first, then suggest improvements)
- Provides a SKILL.md and expects quality feedback

Do NOT activate for: creating a new skill from scratch → use `skill-creator`. This skill is for **evaluation**, not generation.

## Core Workflow

### Step 0: Load the Skill Under Test

Determine what the user has provided:

| Input | Action |
|-------|--------|
| Single `SKILL.md` file | Evaluate that file |
| Skill folder (with `references/`) | Evaluate all files, cross-reference consistency |
| URL / GitHub link | Fetch and evaluate |
| Pasted markdown content | Treat as SKILL.md |

If the user has not provided a skill → ask: "请提供要评估的 SKILL.md 文件或 skill 文件夹路径。"

**Input validation — before proceeding to Step 1, verify the input is actually a skill:**

| Check | Condition | Action |
|-------|-----------|--------|
| Binary / garbled content | File is not valid text, or text is unreadable gibberish | **STOP.** Report: "This file does not appear to be a valid SKILL.md — it contains binary or unreadable content. Please provide a markdown-based skill file." Do NOT attempt to score. |
| No skill markers at all | Text is valid but contains zero skill indicators (no YAML frontmatter `---`, no markdown headings resembling skill sections, no workflow/instructions) | **STOP.** Report: "This appears to be a {detected_type} file (e.g., Python script, JSON config, plain prose), not a SKILL.md. skill-scorer evaluates SKILL.md files only." Do NOT force-fit 8 dimensions onto non-skill content. |
| Partial skill structure | Has some skill-like elements (e.g., YAML frontmatter exists but body is minimal, or has headings but no workflow) | **PROCEED with caveats.** Evaluate normally, but note in the report header: "⚠️ This file has incomplete skill structure — scores reflect what is present." Score missing sections as 0 in relevant dimensions rather than guessing. |

### Step 1: Parse Skill Structure

Extract and inventory:
- YAML frontmatter fields (`name`, `description`, `version`, `compatibility`)
- Section headings and their order
- References to external files (`references/`, `scripts/`, `assets/`)
- Total line count and estimated token count of SKILL.md body

### Step 2: Run 8-Dimension Evaluation

Read [references/rubric.md](references/rubric.md) for the complete scoring rubric.

Evaluate the skill across these 8 dimensions (each scored 0-100, then weighted):

| # | Dimension | Weight | What It Measures |
|---|-----------|--------|------------------|
| 1 | Metadata & Triggering | 15% | Name clarity, description quality, trigger coverage |
| 2 | Structure & Architecture | 15% | File organization, section order, progressive disclosure |
| 3 | Instruction Clarity | 15% | Actionability, conciseness, examples, tone |
| 4 | Workflow & Logic | 15% | Step completeness, parameter handling, validation |
| 5 | Error Handling | 10% | Fallbacks, edge cases, failure recovery |
| 6 | Context Efficiency | 10% | Token budget, redundancy, information density |
| 7 | Portability & Compatibility | 10% | Self-containment, cross-platform support |
| 8 | Safety & Robustness | 10% | No injection risk, no hallucination traps, identity lock |

### Step 3: Identify Issues

For each issue found, classify severity:

| Severity | Meaning | Score Impact |
|----------|---------|--------------|
| 🔴 Critical | Skill will malfunction or not trigger | -10 to -15 per issue |
| 🟡 Warning | Skill works but suboptimally | -3 to -8 per issue |
| 🟢 Suggestion | Nice-to-have improvement | -1 to -2 per issue |

### Step 4: Generate Report

Read [references/report-template.md](references/report-template.md) for the output format.

The report includes:
1. **Score Card** — Overall score + per-dimension breakdown
2. **Issue List** — All findings sorted by severity
3. **Top 3 Quick Wins** — Highest-impact fixes with before/after examples
4. **Optimization Roadmap** — Prioritized improvement plan

### Step 5: Offer Follow-Up

After presenting the report, ask:
- "需要我帮你自动修复这些问题吗？" (auto-fix mode)
- "需要对某个维度深入分析吗？" (deep-dive mode)
- "需要生成优化后的 SKILL.md 吗？" (rewrite mode)

## Output Rules

1. **Bilingual report — Chinese first, English after, no interleaving.** Always output the complete report in Chinese, then a `---` separator, then the complete report in English. Never mix languages within a section. Both versions must contain identical scores, issues, and suggestions — only the language differs.
2. **Score must be justified.** Every deducted point must trace to a specific issue.
3. **Suggestions must be actionable.** Include before/after code snippets, not vague advice.
4. **Be constructive, not destructive.** Lead with what the skill does well before listing issues.
5. ❌ Never inflate scores to be polite — honest assessment helps the user improve.
6. ❌ Never evaluate based on domain correctness of the skill's content (e.g., whether hotel recommendations are good) — only evaluate skill engineering quality.

## References

| File | Purpose | When to read |
|------|---------|-------------|
| [references/rubric.md](references/rubric.md) | Detailed scoring criteria for all 8 dimensions | Step 2: scoring |
| [references/report-template.md](references/report-template.md) | Output format and report structure | Step 4: generating report |
| [references/anti-patterns.md](references/anti-patterns.md) | Common skill mistakes and how to detect them | Step 3: finding issues |

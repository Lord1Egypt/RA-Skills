---
name: witch
description: >-
  整合了各种算命方法。Use only when the user explicitly says to use the witch skill
  or strictly requires this skill for Chinese-Western-New-Age symbolic destiny
  analysis. Do not trigger for ordinary astrology, psychology, religion, health,
  legal, investment, or factual advice.
license: MIT
metadata:
  version: "0.1.0"
  owner: VincentJiang06
  keywords: [算命, 命理, 占星, 塔罗, 综合推演]
---

# witch

Use this skill only after an explicit user request to use `witch` or this exact skill. It packages a long Chinese prompt for a formal, structured, symbolic destiny report that combines Chinese metaphysics, European esotericism, and modern New Age frameworks.

## Required Reference

Before producing any report, read [references/full-prompt.md](references/full-prompt.md) completely and treat it as the execution contract.

The reference contains the full report structure, fallback rules, scoring weights, and required final phrasing. Follow it unless a higher-priority instruction requires a narrower or safer answer.

## Execution Rules

- Use only the personal information supplied in the current user request.
- Do not browse or add external biographical facts unless the user explicitly asks for research.
- Preserve the reference prompt's Chinese report style and section order.
- Mark information strength and conclusion strength as required by the reference.
- When health, legal, investment, or other high-stakes topics appear, keep the analysis symbolic and do not replace professional advice.
- Do not use this skill for casual horoscope explanations, factual lookup, psychological diagnosis, religious counseling, or real-world professional decisions unless the user explicitly invoked `witch` and the answer stays symbolic.

## Output

Return the full Chinese report requested by the reference prompt. Do not summarize the method instead of performing the report.


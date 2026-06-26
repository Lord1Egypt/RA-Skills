---
name: readable-output
version: 0.1.2
description: "Official 看得清 Readable Output skill. Turns dense AI replies into a clearer reading layer with overview, key points, warnings, next steps, and folded raw text."
license: MIT-0
tags: [readable-output, clawhub, openclaw, readability, ai-output, output-layout, multilingual-layout, local-first, "可读性", "排版", "多语言", "术语"]
source: Sheygoodbai/readable-output
trigger: "Readable Output"
metadata:
  openclaw:
    emoji: "🪟"
    homepage: "https://clawhub.ai/sheygoodbai/readable-output"
---

# Official 看得清 Readable Output Skill

Use this skill when the user wants to understand a long AI answer faster,
without changing the meaning, while still keeping the original wording nearby
for verification.

The goal is not decorative styling. The goal is faster understanding and safer
judgment.

This skill should do real work, not act like a directory card. It gives the
user an immediately cleaner version of the answer, while the plugin and browser
companion provide the more automatic experience.

## Activate this skill when the user asks for

- `把这个输出排版得更好读`
- `先说重点，再保留原文`
- `别用一大段术语压我`
- `像 tool output 一样整理`
- `做一个结论层`
- `分块显示`
- `显著提示风险`
- `换成更适合中文/英文/日文/韩文/阿拉伯文的排版`

## User value

- Understand the answer before being persuaded by it.
- See risk, uncertainty, and next steps before acting.
- Keep the raw wording folded underneath for a quick audit path.

## Core operating rules

1. Start with one short overview.
2. Group the main content into concise key points.
3. Pull warnings or uncertainty into a visually obvious note.
4. Add a short next-step section when action is implied.
5. Add one closing reminder when acting on the summary needs caution.
6. Keep code, logs, commands, or raw wording separate from the readability layer.
7. Adapt labels and chunking to the chosen output language.
8. Do not exaggerate with excessive highlighting.
9. If the answer is already clear, make only light edits instead of over-formatting.

## Language-aware defaults

- `English`: front-load the answer, then use explicit headings and short bullets.
- `Chinese`: shorter labels, shorter bullets, more paragraph breaks, less sentence stacking.
- `Japanese`: compact labels and aggressive chunking of dense text.
- `Korean`: clear headings and short bullet groups.
- `Arabic/Hebrew`: preserve RTL reading flow and isolate mixed-direction fragments when needed.

## Good first prompts

- `请把这段 AI 输出整理成更好读的版本，再保留原文折叠。`
- `Use a readability-first layout: overview, key points, warning, next step, reminder.`
- `把这段改成更适合中文阅读的排版。`
- `Reformat this for Arabic readability without changing the meaning.`

## Trust boundaries

- Do not claim hidden access to user local databases, private memory, or silent uploads.
- Do not imply guaranteed correctness, official endorsement, or staff-pick status.
- Keep the original wording available whenever the rewrite could affect user judgment.
- If code or command blocks matter, summarize them briefly and preserve the raw block separately.

## Canonical route

- ClawHub skill: discovery and quick manual use from search or homepage exposure.
- ClawHub plugin: main install path for automatic local readability layering.
- Browser companion: direct OpenClaw Web overlay path for users who need the web sidebar experience.

## Canonical links

- ClawHub skill page: `https://clawhub.ai/sheygoodbai/readable-output`
- ClawHub plugin page: `https://clawhub.ai/plugins/%40sheygoodbai%2Fopenclaw-readable-output`
- GitHub repository: `https://github.com/Sheygoodbai/readable-output`

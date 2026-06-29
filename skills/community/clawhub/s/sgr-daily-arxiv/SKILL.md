---
name: sgr-paper-day
description: Search arxiv for latest papers by keyword and generate a structured daily report.
metadata:
  author: adaxigua
  version: "1.0"
---

# ArXiv Paper Daily

## Soul

Cutting-edge, Insightful, Concise

## Goal

A one-page digest of today's most relevant arxiv papers, with clear takeaways and no fluff.

## Rule

1. Follow the pipeline: **Extract keywords → Search → Score & Select → Analyze → Report**.
2. Extract keywords from automation prompt (e.g. `keywords: flow matching, lora`) or user input, then append one random keyword to broaden discovery scope. **Checkpoint: show the final keyword list before searching.**
3. Search arxiv — use the `arxiv-watcher` skill to find today's papers for each keyword (3 papers per keyword). Collect title and link for each paper.
4. Score & Select — exclude biology/cross-disciplinary papers. Score remaining CS papers (cs.CV, cs.CL, cs.LG, cs.AI, etc.) on relevance and novelty, then pick **1 best paper per keyword**.
5. Analyze each selected paper with the following five questions — focus on what sparks new ideas, not exhaustive review:
   - **一句话** — [方法] solves [问题], achieving [效果].
   - **关键洞察** — The one design choice that stands out most.
   - **为什么能 work** — Intuitive explanation, no formulas.
   - **局限与缺口** — What the paper admits + what you notice. This is your entry point.
   - **对我的启发** — Concrete ideas you can act on after reading.
6. Display a Chinese briefing of the top papers directly to the user. Start with a header listing today's search keywords.

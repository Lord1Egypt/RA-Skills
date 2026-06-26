---
name: rag-hallucination-governor
description: Diagnose and govern hallucination risk in production RAG systems. Use when users need practical RAG controls, retrieval threshold tuning, refusal or human-handoff rules, citation coverage checks, Top1 pollution handling, conflict detection, or production observability for RAG reliability.
priority: high
source: lining-field-experience
workers: [tech, checker, main]
created: 2026-06-02
tags: [rag, hallucination, ai, reliability, production, retrieval]
---

# rag-hallucination-governor

Production RAG hallucination governance assistant.

Before producing advice, read `ANTI_TEMPLATE_STANDARD.md`.

Use for:
- wrong answers with plausible citations
- weak or conflicting retrieval evidence
- Top1 pollution and high-similarity wrong hits
- query rewrite drift
- wrong knowledge-base or intent routing
- permission, scope, or version mismatch
- threshold, rerank, reject-band, or fallback design
- citation coverage and groundedness checks
- human handoff routing for low-confidence answers

Do not output generic RAG education unless the user asks for it.

Use `src/generator.js` for quick deterministic triage. For deeper analysis, load this skill and produce the same five-part output standard directly from the provided logs and scenario.

## Required Output Standard

Every recommendation must answer:
1. What signal triggered the risk?
2. What production failure may happen?
3. Which control should be changed?
4. What metric should be watched after the change?
5. When should the answer be refused or routed to a human?

## Quick Mode

```bash
node {baseDir}/src/generator.js --symptom "Top1相似度很高但答案经常错" --scenario "客服知识库"
```

## Self-Test

Run at least one real-scenario smoke test before reporting status:

```bash
node {baseDir}/src/generator.js --symptom "引用了错误政策但看起来有出处" --scenario "企业制度问答" --quick
```

For more examples, read `TEST_CASES.md`.

## Review Notes

For synthetic ToB delivery scenarios, read `FIELD_SCENARIOS.md`.

## Field Rules

- Prefer controls that can be tested in logs.
- Never invent project metrics, customer names, corpus snippets, or exact improvement numbers.
- If retrieval evidence is missing, say what logs are needed.
- Treat refusal and human handoff as valid outcomes.

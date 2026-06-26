# rag-hallucination-governor

Production RAG hallucination triage and governance skill for ToB systems.

## What It Does

Diagnoses RAG reliability failures where answers look plausible but are grounded in weak, wrong, conflicting, or out-of-scope evidence.

It focuses on six production risk types:

- Top1 pollution
- Citation coverage gap
- Conflicting evidence
- Query rewrite drift
- Permission or scope mismatch
- Low-confidence evidence forcing an answer

## Privacy Boundary

This skill contains only synthetic and abstracted field patterns.

It does not include real customer names, project names, prices, contracts, tickets, private corpus snippets, or identifiable incident details.

## Quick Test

```bash
node src/generator.js --symptom "Top1 相似度很高但答案经常错" --scenario "客服知识库" --quick
npm test
```

Expected signal:

- `Risk type: Top1 pollution`
- control recommendations for Top1/Top2/Top3 comparison, rerank, evidence consistency, and handoff

## Boundary

本 Skill 使用脱敏经验规则做诊断，不联网、不编造客户事实。需要真实证据时，应提供召回日志、引用片段、权限上下文或用户材料。

## Review Status

- Implementation: complete
- Quality review: passed
- Release status: ready for publishing

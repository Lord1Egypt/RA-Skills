# Swarm Roadmap — Quality Sprint

**Goal:** Stay fast and cheap, but maximize quality-per-dollar.

**Rule:** Every feature gets a benchmark. If it slows things down or doesn't measurably improve quality, it doesn't ship.

## Features

### 1. ✅ Self-Reflection Loop (v1.3.5)
- **What:** After chain output, run a critic that scores it. If below threshold, re-run synthesis with critique.
- **Result:** Improved weak output from 5.0 → 7.6 avg score. 1-2 extra LLM calls worst case.
- **Benchmark:** ✅ Passing — quality improvement confirmed, <35s guardrail met.

### 2. ✅ Skeleton-of-Thought (v1.3.6)
- **What:** Generate outline → expand sections in parallel → merge
- **Result:** 14,478 chars in 21s (675 chars/sec) — 5.1x more content than chain at 2.9x throughput. Scored 9.4/10 with reflection.
- **Benchmark:** ✅ Passing — SoT vs chain comparison automated.

### 3. ~~Multi-Provider Failover~~ — SKIPPED
- Gemini has been stable. Not worth the complexity right now.

### 4. ✅ Structured Output Mode (v1.3.7)
- **What:** Force JSON schema output via Gemini's `response_mime_type` + `responseSchema`
- **Result:** Zero parse failures. 6 built-in schemas (entities, summary, comparison, actions, classification, qa). Schema validation on output.
- **Benchmark:** ✅ 4/4 tests passing (built-in schema, summary, JSON mode, schema listing).

### 5. ✅ Majority Voting / Best-of-N (v1.3.7)
- **What:** Same prompt N times → pick consensus/best via 3 strategies (judge, similarity, longest)
- **Result:** Judge strategy scores candidates on 4 dimensions. Similarity uses Jaccard word-set consensus (zero extra cost). ~800ms for similarity, ~10s for judge.
- **Benchmark:** ✅ 3/3 tests passing (similarity, longest, judge strategies).

## Performance Guardrails (all passing)
- Parallel: <150ms/task effective at 10 tasks ✅
- Chain standard: <15s ✅
- Single prompt: <1s ✅
- Daily cost for typical workload: <$0.05 ✅
- Structured output: <2s ✅
- Voting (similarity): <2s ✅
- Voting (judge): <15s ✅

## Quality Sprint Complete 🎉
All 4 implemented features shipped with benchmarks and guardrails.

**Total feature set:**
1. Parallel execution (v1.0)
2. Web research with Google grounding (v1.1)
3. Chain pipelines + auto-chain (v1.3)
4. Chain templates (v1.3.3)
5. Prompt cache (v1.3.2)
6. Smart routing (v1.3.4)
7. Error diagnostics (v1.3.4)
8. Self-reflection (v1.3.5)
9. Skeleton-of-Thought (v1.3.6)
10. Structured output (v1.3.7)
11. Majority voting (v1.3.7)

---
name: searching-precisely
description: Use when searching the web, documentation, or current information where token efficiency matters. Triggers on queries about API docs, current events, pricing, or any question requiring up-to-date online sources. Avoids reading entire pages when a targeted extract would suffice.

# ── ClawHub Security Manifest ────────────────────────────────────────────────
# Declared so static analyzers can verify scripts match metadata.

permissions:
  local_read:  true   # semantic-cache.js reads ~/.antigravity/search-cache/index.json
  local_write: true   # semantic-cache.js writes ~/.antigravity/search-cache/index.json
  network:     true   # parallel-probe.js sends HTTP/HTTPS HEAD requests (no body upload)
  shell:       true   # agent runs node scripts via shell tool

autonomous:    false  # must not be invoked with untrusted/unsanitized URL inputs
disable-model-invocation: true # strictly enforces autonomous: false via OpenClaw policy

host_provides:
  - web_search        # actual web GET / search-API calls are delegated to the host agent
                      # this skill handles pre-processing (intent, rewrite, cache) and
                      # post-processing (probe, assemble, write-cache) only

trust_model: "caller-trusted"  # URLs are assumed to come from the host agent, not end-users

metadata:
  openclaw:
    requires:
      bins: ["node"]  # required runtime; scripts are invoked via shell tool

io:
  cache_path: "~/.antigravity/search-cache/"   # semantic-cache.js read/write scope
                                               # stores query text + result snippets (0o600)
                                               # created automatically on first write
  network_method: "HEAD only"                  # parallel-probe.js; no response body stored
  ssrf_protection: "two-layer"                 # 1. hostname pattern check
                                               # 2. DNS lookup → resolved-IP check (prevents DNS rebinding)

security_notes:
  - "Cache files created with mode 0o600; cache dir with mode 0o700"
  - "Atomic cache writes: temp file + rename to prevent corruption"
  - "Network probes: HEAD only, 4 s timeout, max 5 concurrent, no body read"
  - "SSRF prevention layer 1: RFC-1918 + loopback + link-local hostname patterns rejected"
  - "SSRF prevention layer 2: hostname resolved to IP via dns.lookup(); IP re-checked against same patterns (prevents DNS rebinding)"
  - "No eval, no dynamic require, no code generation"
  - "Scripts invoked via shell tool only; all inputs are JSON-serialized strings"
  - "Cache may contain query text; ensure ~/.antigravity/search-cache/ access is restricted to owner"
# ─────────────────────────────────────────────────────────────────────────────
---

# Searching Precisely

## Overview

Web search pipeline that minimizes token consumption via local intent classification,
semantic caching, credibility validation, and streaming fragment assembly.

**架构分工**：
- **宿主 AI（Host Agent）**负责实际的网页 GET / Search API 调用，返回原始 fragments
- **本 Skill 的脚本**负责前处理（intent 分类、query 改写、budget 控制、cache 查询）和后处理（credibility probe、stream 组装、cache 写入）

**Core Rule:** Always check the semantic cache first. Only invoke web search on a cache miss.

## Pipeline Architecture

```
Query → [Intent Parser] → [Query Rewriter] → [Budget Controller]
                                                     ↓
                                           [Semantic Cache] ──hit──→ Return
                                                     ↓ miss
                                           [Web Search]  (≤1500 tok)
                                                     ↓
                                           [Parallel Credibility Probe]
                                                     ↓
                                           [Stream Assembler] → [Write Cache]
```

## Instructions

When this skill activates, execute the pipeline below **in order**.
Exit early at any step that produces a final answer — do not run later steps unnecessarily.

> **Note:** Replace `<placeholders>` with actual runtime values. All arguments must be valid JSON strings.

---

### Step 1 — Classify Intent

Run via shell tool:
```
node scripts/intent-parser.js '<original_query>'
```
Extract `intent` and `confidence` from the JSON output.  
If `confidence < 0.5`, default to `intent = "web_search"` and continue.

---

### Step 2 — Initialize Budget

```
node scripts/budget-controller.js init
```
Keep the returned `state.remaining` value. Abort any later step that would exceed it.

---

### Step 3 — Check Semantic Cache

```
node scripts/semantic-cache.js check '{"query":"<original_query>","intent":"<intent>"}'
```
- `hit: true` and `similarity ≥ 0.85` → **return `result` to the user. Pipeline complete. Skip all remaining steps.**
- `hit: false` → continue to Step 4.

---

### Step 4 — Rewrite Query

```
node scripts/query-rewriter.js '{"intent":"<intent>","query":"<original_query>"}'
```
Use the returned `subQueries` array (max 3) for web search.

---

### Step 5 — Web Search *(host agent)*

Using your native `search_web` tool, search each sub-query from Step 4.  
Collect result URLs and content fragments.  
**Always perform live search on a cache miss — never fabricate results.**

---

### Step 6 — Validate Source Credibility

Extract up to 5 unique source URLs from Step 5. Run:
```
node scripts/parallel-probe.js '{"sources":[{"url":"<url1>"},{"url":"<url2>"}]}'
```
- `verdict: "trust"` → use directly  
- `verdict: "verify"` → use with caution; flag in the answer  
- `available: false` → discard that source

---

### Step 7 — Score Credibility

```
node scripts/credibility-arbiter.js '{"results":[<probe_results_array>]}'
```
If **all** sources score `< 0.4`, discard everything and tell the user no reliable source was found. Do not assemble.

---

### Step 8 — Assemble Answer

```
node scripts/stream-assembler.js '{"fragments":[<trusted_fragments>],"query":"<original_query>"}'
```
Return the `answer` field to the user.  
If `coherenceScore < 0.5`, add a note that the result may be incomplete.

---

### Step 9 — Write Cache

```
node scripts/semantic-cache.js write '{"query":"<original_query>","intent":"<intent>","result":"<answer>"}'
```
This caches the result for future similar queries. Always run this step after a successful assembly.

## Search Decision Rules

| Situation | Action |
|-----------|--------|
| Query answered by cache (similarity > 0.85) | Return cache, skip web search |
| Query about API docs / official specs | Web search with known domain hint |
| Query about current events / pricing / news | Web search, no cache assumed |
| Query with ambiguous intent | Rewrite into 2-3 sub-queries, search each |

## Token Budget Defaults

| Component | Budget |
|-----------|--------|
| Intent parse | 50 |
| Cache check | 20 |
| Web search | 1500 |
| Credibility | 300 |
| Assembly | 500 |
| **Total** | **2370** |

## Common Mistakes

- ❌ Calling web search before checking the semantic cache
- ❌ Skipping credibility check for unknown domains
- ❌ Assembling fragments from a single unverified source
- ❌ Fetching full page content when a HEAD probe + summary suffices

## ClawHub Security Notes

> All permission declarations, dependencies, I/O scopes, and security properties are
> formally declared in the YAML frontmatter above (`permissions`, `dependencies`, `io`,
> `security_notes`). Static analyzers should use those fields as the authoritative source.

Summary per script:

| Script | I/O | Network | Shell |
|--------|-----|---------|-------|
| `intent-parser.js` | none | none | none |
| `query-rewriter.js` | none | none | none |
| `stream-assembler.js` | none | none | none |
| `budget-controller.js` | none | none | none |
| `credibility-arbiter.js` | none | none | none |
| `semantic-cache.js` | `~/.antigravity/search-cache/` R/W | none | none |
| `parallel-probe.js` | reputation DB R (bundled) | HEAD only, no upload | none |

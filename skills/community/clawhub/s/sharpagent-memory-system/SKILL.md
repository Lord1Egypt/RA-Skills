---
name: sharpagent-memory-system
version: 1.0.0
description: "SharpAgent Layered Memory System — 6-layer memory hierarchy from ephemeral to long-term archive. Features dream processing (consolidation/archiving/forgetting/merging), TF-IDF semantic search, Chinese tokenization support. Solves the three memory problems: forgetting what matters, never forgetting, and poor retrieval."
metadata:
  openclaw:
    emoji: "🧠"
    tags:
      - memory
      - learning
      - persistence
      - retrieval
      - chinese-nlp
      - sharpagent
---

# SharpAgent Layered Memory System v1.0.0

> **Memory like a human — remembers what matters, forgets the rest, and searches accurately.**
> Based on Layered Memory Sys (ClawHub, +324% in 24 days) 6-layer architecture + dream processing + Mem0 persistence.

## Core Problem

Current agent memory problems:

| Problem | Symptom | Consequence |
|---------|---------|-------------|
| Forgets | Every session starts fresh | Repeats mistakes, no accumulation |
| Never forgets | All history flat | High retrieval noise, key info drowned |
| Poor search | Keyword only, no semantics | "five-factor" doesn't find "trust verification" |

SharpAgent memory solves all three with 6 layers + dream processing.

## Memory Layers

```
                        [User interaction]
                            │
                   ┌────────┴────────┐
                   │   L1: Ephemeral │  ← Current session context
                   └────────┬────────┘
                            │ Session ends
                   ┌────────┴────────┐
                   │   L2: Short-Term│  ← Recent sessions (rolling window)
                   └────────┬────────┘
                            │ Periodic migration
                   ┌────────┴────────┐
                   │   L3: Working   │  ← Active task state
                   └────────┬────────┘
                            │ Task complete
                   ┌────────┴────────┐
                   │   L4: Contextual│  ← Task-level context
                   └────────┬────────┘
                            │ Dream processing
                   ┌────────┴────────┐
                   │   L5: Long-Term │  ← Preferences & lessons
                   └────────┬────────┘
                            │ Archive expired
                   ┌────────┴────────┐
                   │   L6: Archive   │  ← Historical archive
                   └─────────────────┘
```

### L1: Ephemeral

**Storage**: Current session all messages
**Capacity**: Model context window
**Lifespan**: Session end = gone
**Index**: None, linear
**Use**: In-context understanding

### L2: Short-Term

**Storage**: Last N sessions (default N=5)
**Medium**: In-memory (Redis optional)
**Capacity**: 5 session summaries, ≤2KB each
**Lifespan**: 7 days → auto-migrate to L4
**Index**: Session ID + timestamp + tags
**Use**: Quick cross-session reference

### L3: Working

**Storage**: Active task state
**Medium**: JSON files (`memory/working/`)
**Capacity**: ≤10KB per task
**Lifespan**: Task complete → L4; task interrupted → kept
**Index**: Task ID + status + last update
**Use**: Resume interrupted tasks, multitasking

### L4: Contextual

**Storage**: Completed task full context
**Medium**: JSON files (`memory/contextual/`) + optional SQLite
**Capacity**: Unlimited, but retrieval Top 5
**Lifespan**: Until dream processing (30d no reference → L5)
**Index**: TF-IDF full-text
**Use**: Look back at past tasks, reuse solutions

### L5: Long-Term

**Storage**: Persistent cross-session knowledge
**Medium**: SQLite (`memory/long_term.db`) + Chinese tokenizer index
**Capacity**: Unlimited
**Lifespan**: Permanent unless explicitly forgotten
**Index**: TF-IDF + jieba Chinese tokenization
**Use**: User preferences, lessons, best practices, key decisions

### L6: Archive

**Storage**: Expired or low-referenced L4/L5 entries
**Medium**: SQLite (`memory/archive.db`), read-only
**Capacity**: Theoretically infinite
**Lifespan**: Permanent read-only
**Index**: None (time + category)
**Use**: Legal compliance retention, audit trail

## Dream Processing

Dreams aren't just for humans. Agents need low-load memory maintenance too.

**Trigger**: Heartbeat (low load, every 30 min), user says "clean up", or scheduled 04:00 daily.

**Four Dream Operations:**

### 1. Consolidation

Combine scattered memory fragments into coherent knowledge.

```
Input: Multiple fragments
→ "Use 150-char abstracts" (verified multiple times)
→ "User prefers shorter versions"
→ "Briefing read rate improved 30%"
→ Consolidate to:
  "Best practice: 150-char abstract in briefings (3x verified, +30% read rate)"
```

**Trigger**: Same pattern appears ≥3 times

### 2. Archiving

Move low-reference items out of working cache.

```
→ L4 entries with 0 references in 30 days
→ Move to L6 archive
→ Remove from L4 tag index
```

**Trigger**: 30-day reference count = 0

### 3. Forgetting

Actively delete low-value, duplicate, or outdated content.

```
→ "User once preferred Python 3.9" (3 months ago, now 3.13)
→ Outdated, delete
→ Keep space for valuable info
```

**Trigger**:
- Newer version available
- Explicitly contradicted
- >90 days with <2 references
- User says "forget this"

### 4. Merging

Combine multiple related L5 entries into higher-level patterns.

```
→ "Prefers 150-char abstract" (confidence=8)
→ "Prefers bullet points" (confidence=7)
→ "Dislikes tables" (confidence=6)
→ Merge:
  "User prefers briefings in bullet points + 150-char abstract, avoid tables"
```

**Trigger**: High confidence (≥7) + same category

## Search

### Standard Search

```python
def search(query, layers=["L4", "L5"]):
    tokens = jieba.cut(query)      # Chinese tokenization
    vec = tfidf_vectorizer.transform(tokens)
    scores = cosine_similarity(vec, layer_index)
    return top_k(scores, k=5)
```

### Chinese Tokenization

```python
jieba.load_userdict("memory/custom_dict.txt")
# "五元组审查" → ["五元组", "审查"] not mis-split
# "惠迈校准框架" → ["惠迈", "校准", "框架"]
```

### Search Priority

| Scenario | Search layers | K |
|----------|--------------|---|
| Real-time reply | L5 → L4 → L2 | 3 |
| Deep analysis | L5 → L4 → L6 | 5 |
| User asks "earlier..." | L4 → L5 | 3 |
| User asks "I remember..." | L5 → L4 | 3 |

## Storage Architecture

```
memory/
├── working/            # L3: Task working area (JSON)
├── contextual/         # L4: Contextual memory (JSON)
├── long_term.db        # L5: SQLite + FTS5 index
├── archive.db          # L6: Archive storage
├── custom_dict.txt     # Domain Chinese word dictionary
└── dream_log.json      # Dream processing log
```

## Edge Cases

| Situation | Action |
|-----------|--------|
| Chinese + English mixed input | jieba auto-detects Chinese, English space-tokenized |
| No search results | Fallback to simple keyword matching |
| L5 exceeds 1000 entries | Trigger dream (archive + forget + merge) |
| Dream active, new interaction | Dream pauses immediately, interaction wins |
| User says "forget xxx" | Soft delete in L5, L6 retains for audit |
| Bulk history import | Write directly to L6, skip layer traversal |

## Quality Gates

| Check | What | Fail action |
|-------|------|-------------|
| Layers separated | Ephemeral/Short/Working/Contextual/Long/Archive distinct | Restructure |
| Search recall | "five-factor" retrieves "trust verification" | Check tokenization |
| Dream non-blocking | Normals interaction during dreams | Async flag |
| Forget traceable | Forgotten entries auditable | Soft delete |
| Chinese tokenization | Domain words preserved | Update custom_dict.txt |

## Integration Points

### Five-Factor Review
- Important memory entries verified before writing
- L5 entries carry FiveFactorResult

### Self-Evolving Loop
- Reflections → L4 contextual, verified lessons → L5 long-term
- Dream consolidation output = new "best-practice" L5 entries

### Engineering Lifecycle
- Working L3 supports task checkpoint/resume
- L4 stores engineering decision traces

## Version History

- **v1.0.0** — Initial release. 6-layer memory architecture with dream processing, TF-IDF search, Chinese tokenization.

---

*SharpAgent · MIT-0 · 2026-05-11*

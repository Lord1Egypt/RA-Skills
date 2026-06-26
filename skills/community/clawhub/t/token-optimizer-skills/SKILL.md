---
name: token-economy
description: Full token economy suite for OpenClaw agents. Audits context window usage (skills, history, tool outputs), then applies 5 creative strategies to reduce bloat without losing memory quality. Use when asked to "analyze tokens", "reduce context", "find bloat", "optimize memory", or "distill history".
tools_required:
  - python3
scripts:
  - count_tokens.py     # Precise token counter with graceful fallback
  - analyze_skills.py   # Skill metadata bloat detector
  - distill_memory.py   # Conversation-to-JSON memory distiller
  - compress_prompt.py  # LLMLingua-2 offline prompt compressor (optional)
---

# Token Economy Skill — Unified Reference

This skill is the complete token management layer for your OpenClaw agent. It covers two phases:
1. **Audit**: Find out where tokens are being spent.  
2. **Optimize**: Apply the right strategy to reclaim them without losing intelligence or memory.

---

## PHASE 1 — TOKEN AUDIT

### 1.1 When to Run an Audit

Trigger a token audit when:
- The conversation feels slow or starts hallucinating earlier context.
- You are about to load a large file or document into context.
- The user asks to "check token usage", "find context bloat", or "how full is the context?".
- The `count_tokens.py --estimate` flag returns a value above **80% of the model's limit**.

### 1.2 Auditing Workflow

Run this sequence:

1. **Calculate System Prompt & Skills Cost**  
   Identify which skills are loaded. Extract their metadata and SKILL.md sizes.

2. **Calculate Conversation History Cost**  
   Examine how long the conversation has run and estimate recent tool output lengths (grep results, file reads, API responses).

3. **Count precisely** using the helper script:
   ```bash
   # Zero-dependency estimate (works everywhere)
   python count_tokens.py --input my_prompt.txt --estimate

   # Precise count for GPT-4o
   python count_tokens.py --input my_prompt.txt --model gpt-4o

   # Precise count for Gemma/Ollama
   python count_tokens.py --input my_prompt.txt --model gemma

   # Precise count for Claude (proxy via cl100k_base, ±5% accuracy)
   python count_tokens.py --input my_prompt.txt --model claude

   # Compare original vs. compressed file
   python count_tokens.py --input original.txt --diff compressed.txt --model gpt-4o
   ```

4. **Generate the Token Budget Report** (see format below).

### 1.3 Token Budget Report Format

Present findings to the user in this format:

```markdown
## 📊 Token Budget Report

**Total Estimated Tokens:** `~<NUM>k (of 128k / 200k / 1M limit)`

### 🍰 Breakdown by Layer
| Layer                      | Estimated Tokens | % of Total | Status                            |
|----------------------------|------------------|------------|-----------------------------------|
| 🛠️ System + KIs + Skills   | X,XXX            | XX%        | `Healthy` / `Bloated`             |
| 💬 Conversation History    | X,XXX            | XX%        | `Healthy` / `Too Long`            |
| 📄 Open Documents          | X,XXX            | XX%        | `Normal`                          |
| 🧠 Tool Outputs            | X,XXX            | XX%        | `Warning: Huge outputs detected!` |

### 🚨 Bloat Warnings
- **[Skill Name]:** XXXX tokens (oversized description metadata).
- **[Conversation]:** Multiple large search/RAG dumps in the chat loop.

### 💡 Optimization Recommendations
1. Use Memory Distillation (Strategy 1) to compress conversation history.
2. Trim oversized skill metadata with `analyze_skills.py`.
3. Lazy-load skills — only inject SKILL.md when explicitly invoked.
```

### 1.4 Context Anti-Patterns to Watch For

| Anti-Pattern | Description | Fix |
|---|---|---|
| **Verbatim Tool Dumps** | Pasting 500-line grep results into context | Return only matching lines |
| **Overloaded Skill Metadata** | SKILL.md `description` > 500 chars | Edit to be concise |
| **Repetitive Instructions** | Same boilerplate instructions repeated every turn | Consolidate to a single reference block |
| **Full File Reads** | Reading a 2,000-line file when only needing one function | Use grep or targeted read |
| **Raw Conversation History** | Storing every message un-distilled past 20 turns | Distill to episodic JSON facts |

### 1.5 Model Tokenizer Reference

| Model Family | Tokenizer | Vocab Size | Python Tool |
|---|---|---|---|
| GPT-4o, GPT-4o-mini | `o200k_base` | ~200k | `tiktoken` |
| GPT-4, GPT-3.5, Claude (proxy) | `cl100k_base` | ~100k | `tiktoken` |
| Gemma 1/2/3, Ollama/Gemma | SentencePiece `google/gemma-7b` | ~256k | `transformers` |
| Any model (fallback) | `char // 4` estimate | — | Built-in (zero deps) |

**General Rules:**
- English prose: ~1.3 tokens per word.
- Code: ~2.5–3.5 tokens per word.
- Tab indentation is more efficient than 4-space indentation (~3 tokens saved per line).
- JSON structure (braces, quotes, commas) is expensive. Prefer CSV or YAML for large repetitive data.

---

## PHASE 2 — TOKEN OPTIMIZER

### The 5 Strategies

When tasked with reducing context bloat, apply one or more of these strategies in order of impact vs. risk:

---

### Strategy 1 — Memory Distillation 💾
**Impact: 40–70% reduction | Risk: Very Low**

Use when the **conversation history is long** (20+ turns or filling significant context).

**What it does:** Converts verbose chat history into structured JSON facts, preserving only decisions, preferences, constraints, and actions.

**How to run:**
```bash
# Distill a JSON chat history file
python distill_memory.py --input history.json --output facts.json

# Distill a plain text transcript
python distill_memory.py --input conversation.txt --output facts.json
```

**Output schema (v2.0-openclaw):**
```json
{
  "metadata": {
    "distillation_version": "2.0-openclaw",
    "original_chars": 45000,
    "lines_processed": 312,
    "facts_extracted_count": 18
  },
  "facts": [
    {
      "id": "a3f2b1c4",
      "type": "decision",
      "content": "Use React Router for navigation",
      "confidence": "high",
      "source_turn": "inferred"
    },
    {
      "id": "d8e1f290",
      "type": "preference",
      "content": "Prefers dark mode primary color palette",
      "confidence": "medium",
      "source_turn": "inferred"
    },
    {
      "id": "c7a9b034",
      "type": "constraint",
      "content": "Must not use third-party authentication libraries",
      "confidence": "high",
      "source_turn": "inferred"
    },
    {
      "id": "f1e2d5c6",
      "type": "next_action",
      "content": "Implement the dashboard layout component",
      "confidence": "low",
      "source_turn": "inferred"
    }
  ]
}
```

**Fact types:**
- `decision` — A confirmed architectural or design choice.
- `preference` — A user or agent preference about style or tools.
- `constraint` — A hard rule that must not be violated.
- `entity` — An important referenced class, file, or system name.
- `next_action` — A pending or future task.

**Workflow:**
1. Agent saves current conversation to `temp_history.json`.
2. Runs `distill_memory.py`.
3. Reads the structured output (50–100 tokens instead of thousands).
4. If `agent-memory-mcp` is available, commits facts via `memory_write`.
5. Flushes working memory — conversation starts fresh.

**Reference:** See the full 3-Tiered Memory Architecture in [Section 2.6](#26-memory-persistence-architecture).

---

### Strategy 2 — Skill Lazy Loading 📦
**Impact: 10–30% reduction | Risk: Zero**

Use when the **system prompt metadata is bloated** with dozens of passively-loaded skills.

**What it does:** Identifies skills whose SKILL.md `description` fields are too verbose (>500 chars) and flags them for trimming.

**How to run:**
```bash
# Auto-detects your skills directory (checks SKILLS_DIR env var, ./skills, ~/.openclaw/skills, ~/.gemini/antigravity/skills)
python analyze_skills.py

# Or set explicitly
SKILLS_DIR=/path/to/your/skills python analyze_skills.py
```

**Sample output:**
```text
Analyzing skills in: /app/skills

--- Skill Context Audit ---
Total Skills Analyzed: 239
Estimated Token Cost of Loaded Skill Database: ~20539 tokens

🚨 Bloated Skills Detected (Metadata > 500 chars):
  - planning-with-files: 1049 chars (~262 tokens)
  - ui-ux-pro-max: 841 chars (~210 tokens)

💡 Recommendation: Edit the description in these SKILL.md files to be concise.
💡 Use Token Genome routing: only inject heavy SKILL descriptions when requested.
```

**Fix:** Edit the `description:` field in the flagged `SKILL.md` frontmatter to be one clean, concise sentence.

---

### Strategy 3 — Code & Context DNA Compression 🧬
**Impact: Up to 80% on UI/boilerplate code | Risk: Low (never removes logic)**

Use when working with **large frontend or backend code files** where the agent only needs to understand the logic, not re-read identical boilerplate.

**What it does:** Instead of reading an entire 500-line component into context, collapses standard import blocks and boilerplate into single-line comment stubs. The agent still understands what is there — it just doesn't re-tokenize redundant text.

**Examples:**

```typescript
// BEFORE — 6 lines, ~40 tokens
import { Button } from "@/components/ui/button"
import { Card, CardHeader, CardContent } from "@/components/ui/card"
import { useState, useEffect } from "react"
import { useRouter } from "next/navigation"
import type { FC } from "react"

// AFTER — 1 line, ~8 tokens
// Standard imports: Button, Card, useState, useEffect, useRouter (FC)
```

**Rule:** Only compress sections the agent does NOT need to modify. Never compress the logic function you are about to edit.

---

### Strategy 4 — Model Dialect Rewriting 🗣️
**Impact: 10–20% | Risk: Low for Gemma/Ollama, not needed for GPT/Claude**

Use when the **backend model is Gemma or a local Ollama model**.

**What it does:** Rewrites flowing natural language prompts into structured XML blocks, which Gemma's SentencePiece tokenizer handles far more efficiently.

**Example:**
```text
# BEFORE — flowing prose (~22 tokens)
Here is the context of the user's issue which happens in the API.
Please read it and write a Python script to fix it.

# AFTER — XML dialect (~9 tokens)
<context>Issue in API.</context><task>Write Python fix.</task>
```

**Why it works:** XML tags like `<context>` are often single tokens in Gemma's 256k vocabulary. You save the tokens that were used writing "The following is the context of..." — which are essentially wasted tokens.

**Gemma-Specific Tips:**
- Gemma's large vocabulary means technical compound words often tokenize as **1 token** instead of 2–3.
- Tabs save ~3 tokens per line over 4-space indentation in long code files.
- Focus parameter names in tool schemas over lengthy natural-language descriptions — Gemma infers from names.

---

### Strategy 5 — Prompt Compression (Offline Only) 🗜️
**Impact: 20–50% | Risk: HIGH on live prompts — use only for offline large docs**

> 🚨 **Critical Guardrail: NEVER apply this to:**
> - Live system prompts
> - Tool schemas or function definitions
> - JSON configs or structured data
> - Code (unless completely isolated and reversible)
>
> **Only use for:** offline experiments on large pasted documentation blocks, research dumps, or very long user-provided text.

**What it does:** Uses LLMLingua-2 to mathematically calculate the perplexity (entropy) of each word and removes low-information filler tokens without changing core meaning.

**Setup (one-time):**
```bash
pip install llmlingua
```

**How to run:**
```bash
# Compress a large research document by 50%
python compress_prompt.py --input large_doc.txt --ratio 0.5

# Preview first 500 chars before committing (dry run safety check)
python compress_prompt.py --input large_doc.txt --ratio 0.5 --dry-run
```

**Always use `--dry-run` first** to visually verify the output is coherent before permanently replacing the source.

---

### 2.6 Memory Persistence Architecture

The 3-tiered memory model is the foundation of all quality-preserving token reduction:

```
┌─────────────────────────────────────┐
│  TIER 1: Working Memory (Expensive) │
│  Active conversation log            │
│  → Keep SHORT. Max 20 turns.        │
└──────────────┬──────────────────────┘
               │ distill_memory.py
               ▼
┌─────────────────────────────────────┐
│  TIER 2: Episodic Store (Cheap)     │
│  JSON facts extracted from history  │
│  → 50-100 tokens per session        │
└──────────────┬──────────────────────┘
               │ memory_write (agent-memory-mcp)
               ▼
┌─────────────────────────────────────┐
│  TIER 3: Semantic Store (Free)      │
│  RAG / Vector / MCP external store  │
│  → Zero context cost until queried  │
└─────────────────────────────────────┘
```

### Memory Distillation Trigger Rules

> 🚨 The agent **strictly ONLY** distills memory under these conditions:
> 1. **At explicit task completion** — a defined sub-task is marked done.
> 2. **After N turns** — a dense session has exceeded the configured turn limit.
> 3. **At 80% context threshold** — `count_tokens.py --estimate` confirms context is near capacity.

**Never distill preemptively** mid-task — you risk losing the working context needed to finish the current action.

---

## Quick Reference

| Goal | Script | Command |
|---|---|---|
| Count tokens in a file (precise) | `count_tokens.py` | `python count_tokens.py --input file.txt --model gpt-4o` |
| Count tokens (no dependencies) | `count_tokens.py` | `python count_tokens.py --input file.txt --estimate` |
| Find bloated skill descriptions | `analyze_skills.py` | `python analyze_skills.py` |
| Distill chat to JSON facts | `distill_memory.py` | `python distill_memory.py --input chat.json --output facts.json` |
| Compress a large document (offline) | `compress_prompt.py` | `python compress_prompt.py --input doc.txt --ratio 0.5 --dry-run` |

---

*Phase 2 — OpenClaw Production Hardened. All scripts include graceful dependency fallbacks.*

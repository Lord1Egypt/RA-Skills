# 🧠 Token Economy Skill Suite
### For OpenClaw Agents — Phase 2 Production-Ready

A complete token management layer that **audits** where your agent spends context tokens and **optimizes** memory without losing intelligence or conversation quality.

---

## 📦 What's Included

```
openclaw_token_skills/
│
├── README.md                        ← You are here
│
├── token-audit.skill                ← Packaged skill (zip archive)
├── token-optimizer.skill            ← Packaged skill (zip archive)
│
└── raw_files/                       ← Individual files for manual upload
    ├── SKILL.md                     ← Unified skill instructions (upload this to agent knowledge)
    ├── count_tokens.py              ← Token counter with graceful fallback
    ├── analyze_skills.py            ← Skill metadata bloat detector
    ├── distill_memory.py            ← Conversation → JSON memory distiller
    ├── compress_prompt.py           ← Offline prompt compressor (optional)
    ├── gemma-optimization.md        ← Gemma/Ollama specific token tips
    ├── memory-persistence-patterns.md ← 3-tier memory architecture guide
    ├── token_audit.md               ← Audit skill standalone reference
    └── token_optimizer_strategies.md ← Optimizer skill standalone reference
```

---

## ✅ Production Status (Backtest v1 Results)

| Script | Functional Test | Live Agent Loop | Known Limitation |
|---|---|---|---|
| `count_tokens.py` | ✅ Pass | ✅ Safe | Falls back to `--estimate` when tokenizer libs absent. Good for budgeting, not accountancy-grade exact counts. |
| `analyze_skills.py` | ✅ Pass (v2) | ✅ Safe | Now reads `name:` from YAML frontmatter. Falls back to folder name if field is absent. |
| `distill_memory.py` | ✅ Pass (v2.1) | ⚠️ Verified compression, not high-trust memory | Resolves real `source_turn` from structured JSON. Plain-text input produces `source_turn: "inferred"`. Regex may miss nuance — treat as compression aid, not authoritative memory without review. |
| `compress_prompt.py` | ⚠️ Offline only | ❌ Not for live agent loop | Requires `llmlingua`. Must never touch system prompts, tool schemas, or code. Validated for large docs only. |

> **Honest bottom line:** 3/4 scripts pass functional + integration backtests. `compress_prompt.py` remains optional/offline until dependency and guardrail setup is confirmed on your target environment.

---


### Option A — Packaged Skill Files (Recommended for GUI agent dashboards)

If your OpenClaw dashboard supports drag-and-drop skill imports:

1. Open your **OpenClaw Agent Dashboard**.
2. Navigate to **Skills** → **Import Skill**.
3. Drag and drop both files:
   - `token-audit.skill`
   - `token-optimizer.skill`
4. The agent will unpack and register them automatically on next restart.

---

### Option B — Manual File Upload (For API / Custom GPT / VPS agents)

If your agent accepts uploaded knowledge/reference files:

1. Upload **`raw_files/SKILL.md`** to your agent's **Knowledge Base** or **System Prompt** section.
2. Upload the 4 Python scripts to a folder your agent can execute:
   - `count_tokens.py`
   - `analyze_skills.py`
   - `distill_memory.py`
   - `compress_prompt.py` *(optional — requires extra dependency)*

---

### Option C — VPS / Self-Hosted CLI Agent (Manual path install)

SSH into your server and run:

```bash
# 1. Create the skills directory for your agent
mkdir -p ~/.openclaw/skills/token-economy

# 2. Copy all raw files into the skill folder
cp raw_files/* ~/.openclaw/skills/token-economy/

# 3. (Optional) Set the SKILLS_DIR env variable so scripts auto-detect the right path
export SKILLS_DIR=~/.openclaw/skills
```

---

## 🐍 Python Dependencies

### Required (for `count_tokens.py` with precise mode)

```bash
pip install tiktoken
```

> ✅ **If `tiktoken` is not installed**, the script automatically falls back to a zero-dependency character-estimation mode (`--estimate`). No crash, no errors.

### Optional (for Gemma / Ollama precise counting)

```bash
pip install transformers sentencepiece
```

### Optional (for `compress_prompt.py` offline compression only)

```bash
pip install llmlingua
```

> ⚠️ **Never apply `compress_prompt.py` to your live system prompt, tool schemas, or code.** Use only for offline compression of large documentation blocks.

---

## ✅ Verify Installation

After installing, run this quick check to confirm everything works:

```bash
# 1. Test zero-dependency token estimate (no packages required)
echo "Hello, this is a test of the token counter." | python raw_files/count_tokens.py --estimate

# 2. Test precise counting (requires tiktoken)
python raw_files/count_tokens.py --input raw_files/SKILL.md --model gpt-4o

# 3. Test skill analyzer (auto-detects your skills directory)
python raw_files/analyze_skills.py

# 4. Test memory distiller on any text file
python raw_files/distill_memory.py --input raw_files/SKILL.md
```

**Expected output for test 1:**
```
--- Token Audit [estimate] ---
Method           : Estimate (char//4)
Input Characters : 44
Input Tokens     : 11
Ratio (char/tok) : 4.00
```

---

## 🗂️ Environment Variables

| Variable | Default | Description |
|---|---|---|
| `SKILLS_DIR` | Auto-detected | Override the skills directory path for `analyze_skills.py` |

**Example:**
```bash
SKILLS_DIR=/app/skills python analyze_skills.py
```

The script checks these paths in order, using the first one it finds:
1. `$SKILLS_DIR` (env variable)
2. `./skills` (local directory)
3. `~/.openclaw/skills`
4. `~/.gemini/antigravity/skills`
5. `/app/skills` (Docker container default)

---

## 🚀 Quick Usage After Install

| What you want to do | Command |
|---|---|
| Audit token usage in a file | `python count_tokens.py --input myfile.txt --model gpt-4o` |
| Fast estimate (no dependencies) | `python count_tokens.py --input myfile.txt --estimate` |
| Find bloated skill descriptions | `python analyze_skills.py` |
| Distill a long conversation to JSON | `python distill_memory.py --input history.json --output facts.json` |
| Compress a large doc (offline only) | `python compress_prompt.py --input doc.txt --ratio 0.5 --dry-run` |

---

## 🧩 The 5 Optimization Strategies (Summary)

| # | Strategy | Savings | Risk |
|---|---|---|---|
| 1 | **Memory Distillation** — Convert chat history to JSON facts | 40–70% | Very Low |
| 2 | **Skill Lazy Loading** — Trim oversized `SKILL.md` descriptions | 10–30% | Zero |
| 3 | **Context DNA** — Collapse boilerplate code into comment stubs | Up to 80% | Low |
| 4 | **Model Dialect** — Use XML tags for Gemma/Ollama | 10–20% | Low |
| 5 | **Prompt Compression** — LLMLingua-2 offline (docs only) | 20–50% | **High if misused** |

> **The single most important insight:** You will save more tokens by **controlling what enters context** than by trying to compress everything after it is already there.

---

## 📄 License & Version

- **Version:** 2.0 (OpenClaw Production-Hardened)
- **Compatibility:** Any Python 3.8+ environment
- Built for OpenClaw agents — works on any agent platform that supports tool scripts and custom knowledge files.

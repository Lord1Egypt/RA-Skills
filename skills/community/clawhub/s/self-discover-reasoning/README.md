<div align="center">

# 🔍 Self-Discover Skill

**Self-composing reasoning structures for AI agents.**

*Let AI discover the optimal reasoning strategy — before solving the problem.*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-compatible-blue)](https://openclaw.ai)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-compatible-purple)](https://claude.ai)
[![Cursor](https://img.shields.io/badge/Cursor-compatible-orange)](https://cursor.sh)
[![GitHub Copilot](https://img.shields.io/badge/Copilot-compatible-lightblue)](https://github.com/features/copilot)
[![Codex CLI](https://img.shields.io/badge/Codex%20CLI-compatible-green)](https://github.com/openai/codex)
[![Gemini CLI](https://img.shields.io/badge/Gemini%20CLI-compatible-4285F4)](https://ai.google.dev)
[![Windsurf](https://img.shields.io/badge/Windsurf-compatible-00D4AA)](https://codeium.com/windsurf)
[![JetBrains](https://img.shields.io/badge/JetBrains-compatible-000)](https://www.jetbrains.com/ai/)
[![Benchmarked](https://img.shields.io/badge/benchmarked-25%25%20improvement-green)](BENCHMARK.md)

</div>

---

## What It Does

Most AI reasoning uses a single strategy (usually "think step by step"). This skill lets the AI **discover the optimal reasoning structure** for each specific task:

```
SELECT → ADAPT → IMPLEMENT → SOLVE
```

Based on peer-reviewed research showing **up to 32% improvement** over Chain-of-Thought and **>20% over Self-Consistency** with 10-40x less compute (Zhou et al., 2024, ICML).

**One file. Zero dependencies. Zero API cost.** The host AI composes its own reasoning structures.

---

## Proven Results

Benchmarked on **20 questions across 5 categories** with controlled before/after evaluation. → [Full report](BENCHMARK.md)

| Metric | Result |
|--------|--------|
| **Overall improvement** | **+25.3%** |
| Questions improved | 20/20 (100%) |
| Best single improvement | +48.2% |

**Per-dimension improvement:**

| Dimension | Δ |
|-----------|---|
| Reasoning Depth | +31.5% |
| Structure Quality | +28.8% |
| Answer Accuracy | +24.2% |
| Problem Coverage | +23.7% |
| Actionability | +22.0% |
| Efficiency | +19.5% |

📖 [Read the full benchmark report →](BENCHMARK.md)

---

## Before & After

<details>
<summary><b>Example 1 — Complex Debugging</b></summary>

**User:** *"My microservice throws intermittent 503s under load. Sometimes works, sometimes doesn't. No pattern I can see."*

**❌ Without Self-Discover:**
> This sounds like a capacity issue. Your service might be running out of resources under load. Check your CPU and memory usage during peak times. You might need to scale horizontally or optimize your code. Also check your database connections — connection pool exhaustion is a common cause. Consider adding circuit breakers and retry logic.

**✅ With Self-Discover:**
> Selected modules: Decomposition, Causal Analysis, Hypothesis Testing, Constraint Satisfaction
>
> **Root cause candidates (ranked by likelihood):**
>
> | # | Hypothesis | Evidence to Check | Fix |
> |---|-----------|-------------------|-----|
> | 1 | Connection pool exhaustion | `SHOW STATUS LIKE 'Threads_connected'` during 503 | Increase pool size + add timeout |
> | 2 | Thread pool saturation | `wrk -t12 -c400` + watch `ActiveThreads` in metrics | Switch to async I/O or increase worker count |
> | 3 | Downstream timeout cascade | Check upstream service latency at P99 during 503 window | Add circuit breaker, fail fast |
>
> **Debugging sequence:**
> ```bash
> # 1. Confirm it's load-dependent
> watch -n1 'curl -s -o /dev/null -w "%{http_code}" http://service/health'
> # 2. Check connections during 503 window
> netstat -an | grep ESTABLISHED | wc -l
> # 3. Compare against pool config
> grep -i pool application.yml
> ```

</details>

<details>
<summary><b>Example 2 — Architecture Decision</b></summary>

**User:** *"Should we use WebSockets or Server-Sent Events for real-time notifications?"*

**❌ Without Self-Discover:**
> Both work for real-time. WebSockets are bidirectional and SSE is server-to-client only. If you only need server push, SSE is simpler. If you need the client to send messages too, use WebSockets. Consider compatibility — SSE works everywhere, WebSockets might have proxy issues.

**✅ With Self-Discover:**
> Selected modules: Comparative Analysis, Constraint Satisfaction, Systems Thinking
>
> | Factor | SSE | WebSocket | Winner |
> |--------|-----|-----------|--------|
> | Direction | Server→Client | Bidirectional | Depends |
> | Reconnection | Auto (built-in) | Manual (heartbeat + reconnect) | SSE |
> | Protocol | HTTP/1.1+ (simple) | Upgrade handshake (complex) | SSE |
> | Binary data | No (text only) | Yes | WS |
> | Load balancer compat | Native HTTP | Requires sticky sessions/config | SSE |
> | Scaling | Easy (stateless connections) | Harder (stateful) | SSE |
>
> **For notifications (server→client, text-based, needs reliability): SSE.**
>
> ```javascript
> // Server (Express)
> app.get('/notifications', (req, res) => {
>   res.setHeader('Content-Type', 'text/event-stream');
>   res.setHeader('Cache-Control', 'no-cache');
>   const push = (data) => res.write(`data: ${JSON.stringify(data)}\n\n`);
>   subscribe(req.user.id, push);
>   req.on('close', () => unsubscribe(req.user.id, push));
> });
> ```
> Use WebSocket only if you need client→server real-time (e.g., collaborative editing, gaming).

</details>

<details>
<summary><b>Example 3 — Math Problem</b></summary>

**User:** *"A bat and ball cost $1.10 total. The bat costs $1.00 more than the ball. How much is the ball?"*

**❌ Without Self-Discover:**
> The ball costs $0.10. The bat costs $1.00 more, so $1.10. Total is $1.10. ✓

**✅ With Self-Discover:**
> Selected modules: Critical Thinking, Constraint Satisfaction, Hypothesis Testing
>
> **Constraint setup:**
> - Bat + Ball = $1.10
> - Bat = Ball + $1.00
>
> **Substitute:** (Ball + $1.00) + Ball = $1.10 → 2 × Ball = $0.10 → **Ball = $0.05**
>
> **Verify:** Bat = $0.05 + $1.00 = $1.05. Total = $1.05 + $0.05 = $1.10 ✓
>
> The intuitive answer ($0.10) fails: $0.10 + $1.10 = $1.20 ≠ $1.10.

</details>

---

## How It Works

### 20 Seed Reasoning Modules

| # | Module | Best For |
|---|--------|----------|
| 1 | **Step-by-Step Thinking** | Sequential procedures |
| 2 | **Decomposition** | Multi-part problems |
| 3 | **Critical Thinking** | Evaluating claims |
| 4 | **Reflective Thinking** | Deep analysis |
| 5 | **Creative Thinking** | Open-ended design |
| 6 | **Pattern Recognition** | Data, sequences |
| 7 | **Analogical Reasoning** | Transfer learning |
| 8 | **Causal Analysis** | Debugging, diagnostics |
| 9 | **Constraint Satisfaction** | Optimization |
| 10 | **Abstraction** | Architecture, generalization |
| ... | *+ 10 more in SKILL.md* | |

### 4 Depth Levels (Auto-Selected)

| Level | When | Modules | Token Cost |
|:-----:|------|:-------:|:----------:|
| **0** | Simple Q&A | 0 | +0% |
| **1** | Most conversations | 1-2 | ~10% |
| **2** | Complex technical | 3-5 | ~25% |
| **3** | High-stakes / full discovery | 4-7 | ~40% |

No configuration. The agent picks the right depth automatically based on task complexity.

### Cross-Task Structure Transfer

Discovered reasoning structures transfer between similar tasks — use `memory/discovered-structures.md` to cache and reuse. Based on Zhou et al.'s finding that structures transfer across model families.

---

## Installation

<details>
<summary><b>OpenClaw (recommended)</b></summary>

```bash
# Copy to your skills directory
cp -r self-discover-skill/ ~/.openclaw/skills/
```

That's it. OpenClaw auto-detects skills.

</details>

<details>
<summary><b>Claude Code</b></summary>

```bash
# Copy to your project
cp -r self-discover-skill/ skills/

# Add to CLAUDE.md
echo "Read and follow skills/self-discover-skill/SKILL.md" >> CLAUDE.md
```

</details>

<details>
<summary><b>Cursor</b></summary>

```bash
# Copy to project root
cp -r self-discover-skill/ skills/

# Add to .cursorrules
echo "Read and follow skills/self-discover-skill/SKILL.md" >> .cursorrules
```

</details>

<details>
<summary><b>Gemini CLI</b></summary>

```bash
# Copy to project, add to GEMINI.md
cp -r self-discover-skill/ skills/
echo "Read and follow skills/self-discover-skill/SKILL.md" >> GEMINI.md
```

</details>

<details>
<summary><b>GitHub Copilot</b></summary>

```bash
# Add to your repository's Copilot instructions
mkdir -p skills && cp -r self-discover-skill/ skills/
echo "Read and follow skills/self-discover-skill/SKILL.md" >> .github/copilot-instructions.md
```

</details>

<details>
<summary><b>Codex CLI (OpenAI)</b></summary>

```bash
cp -r self-discover-skill/ skills/
echo "Read and follow skills/self-discover-skill/SKILL.md" >> AGENTS.md
```

</details>

<details>
<summary><b>Windsurf</b></summary>

```bash
cp -r self-discover-skill/ skills/
echo "Read and follow skills/self-discover-skill/SKILL.md" >> .windsurfrules
```

</details>

<details>
<summary><b>Cline / AI Coding Assistants</b></summary>

Copy `self-discover-skill/` to your project. Reference `SKILL.md` in your assistant's custom instructions.

</details>

<details>
<summary><b>JetBrains AI / Junie</b></summary>

1. Open Settings → Tools → AI Assistant → System Instructions
2. Add: `Read and follow skills/self-discover-skill/SKILL.md`
3. Place the skill folder in your project root

</details>

<details>
<summary><b>Zed</b></summary>

1. Open Zed settings
2. Add to your context or assistant instructions:
```
Read and follow skills/self-discover-skill/SKILL.md
```

</details>

<details>
<summary><b>Kiro</b></summary>

1. Add skill folder to project
2. Reference in Kiro's instruction configuration

</details>

<details>
<summary><b>OpenCode</b></summary>

1. Add skill folder to project
2. Add to `AGENTS.md`: `Read and follow skills/self-discover-skill/SKILL.md`

</details>

<details>
<summary><b>ChatGPT Custom GPT</b></summary>

1. Open your GPT → Settings → Instructions
2. Paste the contents of `SKILL.md`
3. Save

**Note:** SKILL.md includes inline templates for environments without file access — all depth levels work. Structure memory is in-conversation only (no persistence).

</details>

<details>
<summary><b>Any AI Tool</b></summary>

Copy `SKILL.md` into your system prompt or instructions file. That's the only file you need.

</details>

---

## Platform Compatibility

**Top platforms (most popular by usage):**

| Platform | Rating | Structure Memory | Notes |
|----------|:------:|:----------------:|-------|
| **Claude Code** | ⭐⭐⭐⭐⭐ | ✅ File write | #1 coding agent 2026, full support |
| **Cursor** | ⭐⭐⭐⭐⭐ | ✅ File write | $2B ARR AI IDE, full support |
| **GitHub Copilot** | ⭐⭐⭐⭐⭐ | ✅ File write | Largest user base, full support |
| **Codex CLI** | ⭐⭐⭐⭐⭐ | ✅ File write | OpenAI's coding agent, full support |
| **ChatGPT** | ⭐⭐⭐⭐ | ⚠️ In-conversation | Inline templates auto-load, all levels |

<details>
<summary><b>Show all 14 supported platforms</b></summary>

| Platform | Rating | Structure Memory | Install |
|----------|:------:|:----------------:|---------|
| **OpenClaw** | ⭐⭐⭐⭐⭐ | ✅ `memory/` dir | Copy to `skills/`, auto-detect |
| **Claude Code** | ⭐⭐⭐⭐⭐ | ✅ File write | Copy to project, add to `CLAUDE.md` |
| **Cursor** | ⭐⭐⭐⭐⭐ | ✅ File write | Copy to project, add to `.cursorrules` |
| **GitHub Copilot** | ⭐⭐⭐⭐⭐ | ✅ File write | Add to `.github/copilot-instructions.md` |
| **Codex CLI** | ⭐⭐⭐⭐⭐ | ✅ File write | Add to `AGENTS.md` |
| **Gemini CLI** | ⭐⭐⭐⭐⭐ | ✅ File write | Add to `GEMINI.md` |
| **Windsurf** | ⭐⭐⭐⭐⭐ | ✅ File write | Add to `.windsurfrules` |
| **Cline** | ⭐⭐⭐⭐⭐ | ✅ File write | Add to custom instructions |
| **JetBrains AI / Junie** | ⭐⭐⭐⭐½ | ✅ File write | Add to AI Assistant instructions |
| **Aider** | ⭐⭐⭐⭐ | ✅ File write | Place in project, reference with `--file` |
| **Zed** | ⭐⭐⭐⭐ | ✅ File write | Add to Zed settings |
| **ChatGPT GPT** | ⭐⭐⭐⭐ | ⚠️ In-conversation | Paste SKILL.md into GPT Instructions |
| **Kiro** | ⭐⭐⭐⭐ | ✅ File write | Add to Kiro instructions |
| **OpenCode** | ⭐⭐⭐⭐ | ✅ File write | Add to AGENTS.md |

</details>

---

## Academic Foundations

| Paper | Year | What We Use |
|-------|:----:|-------------|
| **SELF-DISCOVER** — Zhou et al. | 2024 | Core SELECT→ADAPT→IMPLEMENT→SOLVE framework |
| **Chain of Thought** — Wei et al. | 2022 | Baseline single-module reasoning |
| **Self-Consistency** — Wang et al. | 2022 | Comparison target (Self-Discover outperforms with less compute) |
| **Least-to-Most Prompting** — Zhou et al. | 2022 | Decomposition module inspiration |
| **Tree of Thoughts** — Yao et al. | 2023 | Multi-path reasoning comparison |
| **Step-Back Prompting** — Zheng et al. | 2023 | Principle-first reasoning module |
| **OPRO** — Yang et al. | 2023 | Optimized prompt comparison |

Full bibliography: [`references/sources.md`](references/sources.md)

---

## File Structure

```
self-discover-skill/
├── SKILL.md                          # Core instructions (the only required file)
├── README.md                         # This file
├── LICENSE                           # MIT
└── references/
    ├── sources.md                    # Academic sources with URLs
    └── discovery-templates.md        # Ready-to-use discovery templates per depth level
```

---

<div align="center">

**The art of reasoning is not in the answer, but in discovering the structure that leads to it.**

⭐ Star this repo if it improved your AI's reasoning quality.

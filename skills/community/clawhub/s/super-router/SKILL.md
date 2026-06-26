---
name: super-router
description: OpenClaw skill for LangGraph-based task routing between PRO and FLASH models. Use it when a task should be decomposed into atomic subtasks, when multi-entity work needs parallel fanout, or when you want structured complexity scoring with FLASH->PRO escalation instead of choosing a single model manually.
version: 1.0.0
author: Yadan Fan
license: MIT
metadata:
  openclaw:
    emoji: "🔀"
---

# Super Router (LangGraph Edition)

Intelligent task decomposition and model routing using LangGraph StateGraph. Automatically routes subtasks between PRO (heavy reasoning) and FLASH (fast) models based on structured complexity assessment.
This package is intended to live in an OpenClaw skill directory such as `~/.openclaw/skills/super-router`.

## When to Use This Skill

Use super-router when you need:
- **Intelligent model routing** — automatically choose between heavy (PRO) and fast (FLASH) models per subtask
- **Task decomposition** — break complex tasks into structured subtasks with independent routing
- **Cost optimization** — use fast models for simple work, heavy models only when needed
- **Configurable models** — use deterministic defaults, with environment-variable overrides for each role
- **Failure escalation** — FLASH retry on infra failures, escalate to PRO on capability failures
- **Audit trail** — full logging of planned vs actual routes, retries, and failure classifications

**Not needed for:** Simple single-turn tasks, tasks where you already know which model to use, or when you want manual control over every routing decision.

## Optimization for Parallelism
To achieve true parallel execution (when `ROUTER_MAX_CONCURRENCY > 1`), the Planner must be instructed to use **Atomic Decomposition**. 

- **Atomic Decomposition**: Breaking a task into the smallest possible independent units (e.g., 10 separate research tasks for 10 companies) rather than "phases" (e.g., one giant 'Research' phase encompassing all companies).
- **Pitfall: Planner Grouping**: Even with explicit instructions, the Planner may occasionally group multiple entities into a single subtask, which kills true parallelism.
- **Verification**: Always verify the `planned_subtasks` count matches the entity count. If the planner groups entities, it should be treated as a capability failure and forced to retry with a correction prompt.
- **Benefit**: This prevents 'lost-in-the-middle' failures and allows executor branches to fire multiple requests simultaneously, significantly reducing wall-clock time.
- **Deferred synthesis**: Summary, reporting, and synthesis subtasks are held until independent executor branches finish, so they receive completed context instead of racing ahead without findings.
- **Implementation**: When prompting the router for multi-entity tasks, explicitly demand: *"Decompose this into exactly X independent subtasks—one subtask per entity. Do not group them into a single phase."*

## Core Architecture (LangGraph StateGraph)

| Node | Function |
|------|----------|
| **Planner** | Decomposes original task into a JSON array of atomic, actionable subtasks. Uses Atomic Decomposition to split multi-entity tasks (e.g., 10 providers -> 10 subtasks) for maximum parallelism. |
| **Judge** | Scores each subtask on 5 dimensions: `reasoning_depth`, `code_change_scope`, `ambiguity`, `risk`, `io_heaviness`; combines with thresholds + confidence to decide PRO/FLASH |
| **Executor Fanout** | Uses LangGraph `Send(...)` to dispatch independent subtasks concurrently, then joins ordered results by original step number |
| **PRO Executor Branch** | Heavy reasoning model (default: Gemini CLI preview model; override via `ROUTER_PRO_MODEL`) |
| **FLASH Executor Branch** | Fast model with review/retry logic (default: Gemini CLI preview model; override via `ROUTER_FLASH_MODEL`) |
| **FLASH Review** | Validates output quality; distinguishes infra failures (timeout, network) from capability failures; retries FLASH or escalates to PRO |
| **Metadata Extractor** | Extracts 'Technical Gold' (atomic high-precision facts) from step output to prevent finalizer timeouts and loss of detail |
| **Recorder/Finalizer** | Logs every step; compiles final report using a hybrid of Technical Gold and full audit trails; supports FLASH->PRO->deterministic fallback chain |

## Installation

### As an OpenClaw skill

```bash
pip install langgraph
```

Keep the repository in an OpenClaw-accessible skill directory such as `~/.openclaw/skills/super-router`.

If you use Ollama-backed roles, ensure Ollama is running locally and pull the models you want to use:

```bash
ollama serve

# Pull recommended models if you use Ollama-backed roles
ollama pull gemma4:26b     # Planner or PRO executor (high quality, slow)
ollama pull llama3.1:8b    # Judge (fast scoring, recommended)
ollama pull qwen3         # PRO executor
ollama pull qwen2.5:7b    # FLASH executor
```

**Note:** If you prefer `gemma4:26b` as the Planner, keep it there. For speed, the Judge should usually be `llama3.1:8b` or another 7B-14B model:

```bash
export ROUTER_PLANNER_MODEL=gemma4:26b
export ROUTER_JUDGE_MODEL=llama3.1:8b
export ROUTER_PRO_MODEL=gemma4:26b
export ROUTER_FLASH_MODEL=qwen2.5:7b
```

If you intentionally want an all-`gemma4:26b` Planner/Judge/PRO setup, use longer timeouts and serialized graph execution:

```bash
export ROUTER_PLANNER_MODEL=gemma4:26b
export ROUTER_JUDGE_MODEL=gemma4:26b
export ROUTER_PRO_MODEL=gemma4:26b
export ROUTER_FLASH_MODEL=qwen2.5:7b
export ROUTER_JUDGE_TIMEOUT=600
export ROUTER_MAX_CONCURRENCY=1
```

## Usage

### OpenClaw agent pattern

When the user says "走 super-router", "use super-router", or asks for router analysis, invoke the script from the OpenClaw skill checkout. Do not assume shell startup files have already exported `ROUTER_*` overrides; pass them inline or through your shell tool's environment support.

```bash
bash workdir:~/.openclaw/skills/super-router command:"ROUTER_PLANNER_MODEL=google-gemini-cli/gemini-3-pro-preview ROUTER_JUDGE_MODEL=gemma4:26b ROUTER_JUDGE_TIMEOUT=600 /opt/homebrew/Caskroom/miniforge/base/bin/python scripts/router.py '分析 K8s YAML 错误并重写配置'"
```

### With Streaming (Node-Level Progress)

```bash
bash workdir:~/.openclaw/skills/super-router background:true command:"/opt/homebrew/Caskroom/miniforge/base/bin/python scripts/router.py --stream 'Your complex task'"
```

### Via Environment Variable (Agent Compatibility)

For agents that struggle with non-ASCII arguments:

```bash
# Normalize task to short ASCII English, then pass as argument
bash workdir:~/.openclaw/skills/super-router command:"/opt/homebrew/Caskroom/miniforge/base/bin/python scripts/router.py 'Analyze K8s YAML errors and fix'"

# Or via env var
bash workdir:~/.openclaw/skills/super-router command:"ROUTER_TASK='Your complex task description' /opt/homebrew/Caskroom/miniforge/base/bin/python scripts/router.py"
```

### Handling Long-Running Execution

For long-running jobs, use OpenClaw background execution and inspect the session until it completes:

```bash
process action:poll sessionId:<session-id>
process action:log sessionId:<session-id>
```

When the run completes, summarize the actual route taken, whether the planner or judge fell back, whether FLASH escalated to PRO, and the final report's recommended next action.

## Environment Variables

| Variable | Purpose | Default |
|----------|---------|---------|
| `ROUTER_PLANNER_MODEL` | Task decomposition model | `gemma4:26b` |
| `ROUTER_JUDGE_MODEL` | Complexity scoring model | `llama3.1:8b` |
| `ROUTER_PRO_MODEL` | Heavy reasoning executor | `google-gemini-cli/gemini-3-pro-preview` |
| `ROUTER_FLASH_MODEL` | Fast executor | `google-gemini-cli/flash` |
| `ROUTER_PRO_FALLBACK_MODELS` | Comma-separated PRO fallback list | None |
| `ROUTER_FLASH_FALLBACK_MODELS` | Comma-separated FLASH fallback list | None |
| `ROUTER_FLASH_RETRY_BUDGET` | Max FLASH retries before escalation | 1 |
| `ROUTER_RECURSION_LIMIT` | Python recursion limit | 128 |
| `ROUTER_JUDGE_TIMEOUT` | Timeout for Judge node LLM calls (seconds) | 300 (up to 6000 for extremely complex tasks with large models) |
| `ROUTER_MAX_CONCURRENCY` | Max concurrent LangGraph branches for judge and executor fanout. Essential for multi-entity atomic tasks; set to `1` for local 26B+ Judge models or constrained hardware. | Auto (`1` for large Judge models) |
| `ROUTER_GEMINI_CLI` | Path to Gemini CLI (if using instead of Ollama) | `/opt/homebrew/bin/gemini` |
| `ROUTER_OLLAMA_URL` | Ollama API endpoint | `http://localhost:11434/api/generate` |
| `ROUTER_FINALIZER_TIMEOUT` | Timeout for the final reporting synthesis (seconds). Essential to set high for complex tasks to avoid timeouts during context assembly. | 6000 |
| `ROUTER_DEBUG` | Print raw planner/judge/Ollama diagnostic snippets | Off |

**For large models (20B+ like gemma4:26b):**
- Prefer `ROUTER_PLANNER_MODEL=gemma4:26b` with `ROUTER_JUDGE_MODEL=llama3.1:8b`
- If using `ROUTER_JUDGE_MODEL=gemma4:26b`, set `ROUTER_JUDGE_TIMEOUT=600` and keep `ROUTER_MAX_CONCURRENCY=1`
- Planner timeout is auto-set to 300s for large models
- Expect 2-5 minute wait times per LLM call
- Model warmup adds ~30-60s upfront but prevents timeouts.
- **Crucial:** A short outer shell timeout can still kill the run even if internal router timeouts are higher. Use `--stream`, background execution, and session polling/log inspection for large Planner/Judge runs.

## Complexity Routing Rules

### 5-Dimension Scoring

The Judge scores each subtask on:

1. **reasoning_depth** (0-3): How much logical inference is needed?
2. **code_change_scope** (0-3): How many files or logical surfaces need changes?
3. **ambiguity** (0-2): How unclear is the task specification?
4. **risk** (0-2): What's the impact of getting this wrong?
5. **io_heaviness** (0-2): How much reading/writing vs. thinking?

`complexity_score` is the sum of `reasoning_depth + code_change_scope + ambiguity + risk`. `io_heaviness` influences routing but does not add to that score directly.

### Routing Thresholds

| Condition | Route |
|-----------|-------|
| `complexity_score >= 5` | PRO |
| `complexity_score <= 2` | FLASH |
| Summary-like task (no deep work) | FLASH |
| High-risk incident diagnosis | PRO |
| High-risk evidence gathering | PRO |
| High-risk decision/rollback evaluation | PRO |
| Boundary case + low confidence | PRO (safe default) |

### Contextual Score Biases

The router applies automatic adjustments:
- **High-risk context** (production, billing, security): boosts `reasoning_depth`, `risk`, `ambiguity`
- **Evidence gathering** in incident: keeps on PRO (not mere IO)
- **Communication/summary** subtasks: routed to FLASH unless deep work is also required

## FLASH Review & Escalation Logic

When FLASH execution fails or produces questionable output:

1. **Classify failure type:**
   - `infra_transient`: timeout, network, rate limit, service unavailable
   - `capability_quality`: "need more info", empty output, too short, repeated task

2. **Decision:**
   - Infra failure -> Retry FLASH (up to `ROUTER_FLASH_RETRY_BUDGET`)
   - Capability failure -> Escalate to PRO immediately
   - Unknown -> Retry once, then escalate

3. **Post-execution verification:**
   - Empty output -> escalate
   - Output < 48 chars (non-summary) -> escalate
   - Output explicitly says "can't complete" -> escalate
   - Output just repeats task description -> escalate

## Finalizer Fallback Chain

Final report generation follows:

```
FLASH finalizer -> (if fails) -> PRO finalizer -> (if fails) -> Deterministic template
```

## Output Structure

- **Output Structure**: The router returns a JSON-serializable state. When summarizing these results in reports or documentation, always use ASCII/Terminal-style arrows (e.g., '-->', '->') rather than mathematical arrows (e.g., '→', '$\\rightarrow$') for all diagrams and flow representations. This is a high-priority stylistic requirement.

```json
{
  "task": "original task string",
  "planner_model": "model name used for planning",
  "judge_model": "model name used for complexity scoring",
  "pro_model": "primary PRO model",
  "flash_model": "primary FLASH model",
  "planned_subtasks": [{"desc": "..."}],
  "subtasks": [
    {
      "desc": "...",
      "model": "PRO|FLASH",
      "assessment": {
        "scores": {"reasoning_depth": 2, "code_change_scope": 1, "ambiguity": 1, "risk": 1, "io_heaviness": 0},
        "complexity_score": 5,
        "suggested_route": "PRO",
        "final_route": "PRO",
        "confidence": 0.85,
        "reason": "...",
        "judge_source": "llm|heuristic"
      }
    }
  ],
  "results": [
    {
      "step": 1,
      "planned_route": "PRO",
      "route": "PRO",
      "model_name": "qwen3",
      "desc": "...",
      "output": "...",
      "status": "executed|executed_via_provider_fallback|flash_retry_exhausted|executor_fallback",
      "attempt_count": 1,
      "retry_count": 0,
      "escalated_from_flash": false,
      "used_provider_fallback": false,
      "flash_review": {"decision": "record", "failure_type": "none", "reason": "..."},
      "attempt_log": ["..."]
    }
  ],
  "final_report": "...",
  "finalizer_outcome": {
    "route": "FLASH|PRO|DETERMINISTIC",
    "model_name": "...",
    "status": "...",
    "used_provider_fallback": false,
    "reason": "...",
    "attempt_log": ["..."]
  }
}
```

## Maintenance

| File | Purpose |
|------|---------|
| `scripts/router.py` | Main LangGraph router script |
| `SKILL.md` | This documentation |

## Troubleshooting

### "Router timed out" / "Ollama returned an empty response"
- **Best fix when keeping a large Planner:** keep `ROUTER_PLANNER_MODEL=gemma4:26b`, but set `ROUTER_JUDGE_MODEL=llama3.1:8b`.
- **All-gemma mode:** set `ROUTER_JUDGE_MODEL=gemma4:26b`, `ROUTER_JUDGE_TIMEOUT=600`, and `ROUTER_MAX_CONCURRENCY=1`; expect much longer runs.
- Use `--stream` and increase the terminal/process timeout if the Planner itself may take longer than 60s.
- Set `ROUTER_JUDGE_TIMEOUT=300` or higher only when intentionally using a 20B+ Judge.
- Alternative: use Gemini CLI for planning: `ROUTER_PLANNER_MODEL=google-gemini-cli/gemini-3-pro-preview`.

### "Planner timed out after 30s" (or 90s)
- Model is too large or not loaded. Warmup helps but large models may still timeout.
- Use `--stream` plus a longer terminal/process timeout, or choose a smaller planner model.
- Check Ollama logs: `ollama serve` output for errors

### "FLASH kept escalating to PRO"
- Task may genuinely require heavy reasoning
- Check if FLASH model is too small for your tasks
- Try setting `ROUTER_FLASH_MODEL` to a larger model

### "Gemini CLI AbortError or Auth Failures"
- If gemini-cli returns AbortError or authentication errors in non-interactive sessions, this is often an infrastructure/API timeout or session issue.
- Use `--stream` to monitor real-time progress and ensure ROUTER_JUDGE_TIMEOUT and terminal timeouts are sufficiently high to prevent external process termination.

### "Planner produced only one subtask"
- Task may be simple enough to not need decomposition
- Planner model may be too small; try `ROUTER_PLANNER_MODEL=gemma4:31b` (if you have the patience for 90s+ waits)

## Related OpenClaw Skills

- **coding-agent** — Hand off implementation-heavy follow-up work to a dedicated coding agent after the router has split and prioritized the task.
- **gemini** — Use direct Gemini CLI prompting when you want a one-shot model call instead of LangGraph decomposition and routing.

## See Also

- LangGraph documentation: https://langchain-ai.github.io/langgraph/
- Ollama documentation: https://ollama.com/docs

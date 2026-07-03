---
name: super-router
description: "LangGraph task router for OpenClaw that decomposes complex work into dependency-aware subtasks, routes each branch to PRO or FLASH models, retries or escalates failures, and records token usage for auditable runs."
version: 1.0.0
author: Yadan Fan
license: MIT
metadata:
  openclaw:
    tags: [model-routing, langgraph, task-decomposition, multi-model, complexity-scoring]
    requires:
      bins: [python]
  related_skills: [btc_analyzer, api-tester, ddg-search]
---

# Super Router (LangGraph Edition)

Super Router decomposes complex work into dependency-aware subtasks, scores each branch for complexity and risk, and executes it on the right model role. It combines PRO/FLASH routing, provider fallback, FLASH retry and escalation, metadata extraction, LangSmith tracing, and token usage accounting into one auditable LangGraph workflow.

## Mandatory OpenClaw Invocation

For any request to use `super-router`, `super_router`, or `走 super-router`, do this exact workflow:

1. Use the OpenClaw `exec` tool to run:
   `/opt/homebrew/Caskroom/miniforge/base/bin/python /Users/fanyadan/.openclaw/skills/super-router/scripts/router.py '<task>'`
2. If `exec` returns `Command still running`, call the OpenClaw `process` tool with `action="poll"` on the returned `sessionId` until the process exits.
3. The next assistant message after completion must start with `Router result:` or `Router failed:` and must include a concrete detail from the router output.

Do not run `openclaw super_router`, `openclaw super-router`, `openclaw skill`, `openclaw skills`, or a nested `openclaw agent` command to satisfy this skill. Those are not the router.

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

- **Atomic Decomposition**: Breaking a task into the smallest possible independent units rather than grouped phases.
- **Pitfall: Planner Grouping**: The Planner may occasionally group multiple entities into a single subtask, which kills true parallelism.
- **Verification**: Always verify the `planned_subtasks` count matches the entity count. If the planner groups entities, treat as capability failure and retry with correction prompt.
- **Benefit**: Prevents 'lost-in-the-middle' failures and allows executor branches to fire simultaneously.
- **Deferred synthesis**: Summary and synthesis subtasks are held until independent executor branches finish.
- **Implementation**: Explicitly demand atomic per-entity decomposition when prompting for multi-entity tasks.

## Core Architecture (LangGraph StateGraph)

| Node | Function |
|------|----------|
| **Planner** | Decomposes original task into a JSON array of atomic, actionable subtasks. Uses Atomic Decomposition for maximum parallelism. |
| **Judge** | Scores each subtask on 5 dimensions: `reasoning_depth`, `code_change_scope`, `ambiguity`, `risk`, `io_heaviness`; combines with thresholds + confidence to decide PRO/FLASH |
| **Executor Fanout** | Uses LangGraph `Send(...)` to dispatch independent subtasks concurrently, then joins ordered results by original step number |
| **PRO Executor Branch** | Heavy reasoning model (override via `ROUTER_PRO_MODEL`) |
| **FLASH Executor Branch** | Fast model with review/retry logic (override via `ROUTER_FLASH_MODEL`) |
| **FLASH Review** | Validates output quality; distinguishes infra failures from capability failures; retries FLASH or escalates to PRO |
| **Metadata Extractor** | Extracts 'Technical Gold' (atomic high-precision facts) from step output to prevent finalizer timeouts and loss of detail |
| **Recorder/Finalizer** | Logs every step; compiles final report using a hybrid of Technical Gold and full audit trails; supports FLASH→PRO→deterministic fallback chain |

## Dependency Handling

Dependency handling is part of the router's execution contract, not just a
planning hint.

- The Planner must return subtasks with stable IDs plus `depends_on` and
  `dependency_reason` fields. Independent subtasks should use `depends_on: []`.
- The dependency judge verifies and corrects only dependency edges and reasons;
  it must keep the planner's existing subtask IDs and must not add, remove,
  merge, split, or rewrite subtasks.
- The dependency validator rejects duplicate IDs, unknown dependency IDs,
  self-dependencies, and cycles. If validation fails, the router falls back to a
  conservative serial dependency chain instead of crashing the graph.
- `dependency_scheduler` computes the ready set on each wave. A subtask is ready
  only when every ID in `depends_on` has completed.
- Ready subtasks are dispatched with LangGraph `Send(...)`; completed wave
  results are joined, ordered by original step, and scheduling repeats until all
  subtask IDs are complete.
- Executor prompts include direct dependency results for the active subtask.
  This keeps synthesis, comparison, validation-after-implementation, and final
  reporting work from running before their evidence-producing branches finish.
- If remaining work exists but no subtask is ready, `dependency_deadlock`
  records blocked fallback results and errors so the finalizer can report the
  dependency issue.

For maximum parallelism, prompt multi-entity work as atomic per-entity
decomposition, and ensure final synthesis/reporting subtasks depend on the
evidence-producing subtasks they summarize.

## Runtime Dependencies

- Python 3.10+ is required.
- `langgraph` is the required Python runtime dependency.
- `langsmith` is optional and used only when LangSmith telemetry is enabled.
- `Pillow` is optional and needed only when regenerating `super-router.png`.
- At least one model provider must be available for the selected model names:
  Codex CLI, Gemini CLI, Claude Code CLI, or Ollama.

## Installation

```bash
# Required: LangGraph
pip install langgraph

# Optional: LangSmith telemetry
pip install langsmith

# Optional: architecture diagram regeneration
pip install pillow
```

All model and provider choices are configured via `ROUTER_*` variables in the OpenClaw environment config file `~/.openclaw/.env`. The router loads that file itself and still honors any explicit process environment overrides. No model names are hardcoded in the skill.

## Usage

### Configuring ROUTER_* Variables

Set `ROUTER_*` environment variables in `~/.openclaw/.env`. OpenClaw normally exposes this file to `exec` child processes, and `router.py` also loads it directly before reading `os.environ`, so the same command works from OpenClaw and from a plain shell.

To see current values: `grep '^ROUTER_' ~/.openclaw/.env`

To use one model for every router role, set `ROUTER_MODEL`:

```bash
ROUTER_MODEL=gpt-5.5
# Equivalent explicit form:
# ROUTER_MODEL=codex/gpt-5.5
```

Role-specific variables such as `ROUTER_PRO_MODEL` and `ROUTER_FLASH_MODEL` override `ROUTER_MODEL` when set.

### Basic Usage (via OpenClaw exec)

When the user says "走 super-router", "use super-router", or asks for router analysis, invoke `router.py` directly through OpenClaw `exec`:

```python
exec(
    command="/opt/homebrew/Caskroom/miniforge/base/bin/python /Users/fanyadan/.openclaw/skills/super-router/scripts/router.py 'Analyze K8s YAML errors and rewrite config'"
)
```

### With Streaming (Node-Level Progress)

```python
exec(command="/opt/homebrew/Caskroom/miniforge/base/bin/python /Users/fanyadan/.openclaw/skills/super-router/scripts/router.py --stream 'Your complex task'")
```

### Via Environment Variable (Agent Compatibility)

For agents that struggle with non-ASCII arguments, pass the task via `ROUTER_TASK`:

```python
exec(
    command="/opt/homebrew/Caskroom/miniforge/base/bin/python /Users/fanyadan/.openclaw/skills/super-router/scripts/router.py",
    env={"ROUTER_TASK": "Your complex task description"},
)
```

### Handling Long-Running Execution

If `exec` returns "Command still running":

```python
# Continue polling with process tool
process(action="poll", session_id="<session_id_from_exec>")

# Wait for completion
process(action="wait", session_id="<session_id_from_exec>", timeout=300)
```

For background launches requested by the user, use `exec(background=true, notify_on_complete=true)` and verify the process is actually running with an immediate `process(action="poll")`. If a background router launch exits immediately, inspect the preview and relaunch with the fix rather than reporting success.

For complex or multiline `ROUTER_TASK` prompts, avoid fragile inline heredocs inside `zsh -lic`. Write the task to a prompt file first, then launch with:

```bash
export ROUTER_TASK="$(/bin/cat "$HOME/.openclaw/logs/<task-name>.txt")"
/opt/homebrew/Caskroom/miniforge/base/bin/python "$HOME/.openclaw/skills/super-router/scripts/router.py" --stream 2>&1 | tee "$HOME/.openclaw/logs/<task-name>.log"
```

This preserves quotes/apostrophes in the task, keeps an auditable prompt artifact, and avoids zsh parse failures from nested heredocs.

**Important:** Once process shows completion, your next assistant message MUST start with `Router result:` or `Router failed:` and include at least one real detail from the output (e.g., "Planner fallback", "timeout", "BTC"). Never reply with just `---`, punctuation, or empty lines.

### Post-Completion Artifact Verification

For router runs that create or modify artifacts (reports, JSON logs, database ingests, generated files), do not trust the router final stdout alone. Before reporting success to the user:

1. Inspect the declared output artifacts directly (`stat`, read the JSON/Markdown headers, count expected sections/cards when relevant).
2. Compare the router final summary against the saved artifacts and machine-readable logs.
3. If stdout and artifacts disagree, treat the artifacts/logs as the source of truth and report the discrepancy immediately.
4. If the discrepancy means the user requirement is not satisfied (for example, requested 20 items but artifact contains 33), do not claim success. Either launch a correction pass when permitted or state the exact blocker.
5. For ingestion workflows, verify the saved ingest JSON fields (`status`, checked/accepted/skipped counts, threshold, document list) and ensure the user-facing Markdown/HTML item set matches the accepted ingested documents.

## Environment Variables

All `ROUTER_*` variables are loaded from `~/.openclaw/.env` by `router.py` before the router resolves defaults. Explicit process environment values win over `.env` values.

| Variable | Purpose | Default |
|----------|---------|---------|
| `ROUTER_MODEL` | Global model default for planner, judge, PRO, and FLASH roles | None |
| `ROUTER_PLANNER_MODEL` | Task decomposition model | internal default |
| `ROUTER_PLANNER_TASK_CHAR_LIMIT` | Character budget for the compact planner-only context manifest JSON | 6000 |
| `ROUTER_PLANNER_MAX_OUTPUT_TOKENS` | Planner JSON subtask output token cap | 4096 |
| `ROUTER_JUDGE_CONTEXT_CHAR_LIMIT` | Character budget for judge context JSON | 3000 |
| `ROUTER_EXECUTOR_CONTEXT_CHAR_LIMIT` | Character budget for executor context JSON | 8000 |
| `ROUTER_METADATA_OUTPUT_CHAR_LIMIT` | Character budget for metadata extraction context JSON and output excerpts | 6000 |
| `ROUTER_FINALIZER_CONTEXT_CHAR_LIMIT` | Character budget for finalizer context JSON | 12000 |
| `ROUTER_JUDGE_MODEL` | Complexity scoring model | internal default |
| `ROUTER_PRO_MODEL` | Heavy reasoning executor | internal default |
| `ROUTER_FLASH_MODEL` | Fast executor | internal default |
| `ROUTER_PRO_FALLBACK_MODELS` | Comma-separated PRO fallback list | None |
| `ROUTER_FLASH_FALLBACK_MODELS` | Comma-separated FLASH fallback list | None |
| `ROUTER_CODEX_CLI` | Codex CLI executable path for Codex-backed model names | first `codex` on `PATH`, else `codex` |
| `ROUTER_CODEX_CWD` | Optional working directory passed to `codex exec --cd` | None |
| `ROUTER_CODEX_SANDBOX` | Sandbox mode passed to `codex exec --sandbox` | `read-only` |
| `ROUTER_CLAUDE_CLI` | Claude Code CLI executable path for Claude-backed model names | first `claude` on `PATH`, else `claude` |
| `ROUTER_FLASH_RETRY_BUDGET` | Max FLASH retries before escalation | 1 |
| `ROUTER_RECURSION_LIMIT` | Python recursion limit | 128 |
| `ROUTER_JUDGE_TIMEOUT` | Timeout for Judge node LLM calls (seconds) | 300 |
| `ROUTER_MAX_CONCURRENCY` | Max concurrent LangGraph branches for judge and executor fanout | Auto |
| `ROUTER_OLLAMA_URL` | Ollama API endpoint (if used) | `http://localhost:11434/api/generate` |
| `ROUTER_FINALIZER_TIMEOUT` | Timeout for the final reporting synthesis (seconds) | 600 |
| `ROUTER_DEBUG` | Print raw diagnostic snippets | Off |
| `ROUTER_LANGSMITH_ENABLED` | Enable optional LangSmith graph and model-call telemetry when `LANGSMITH_API_KEY` is set | Off |
| `ROUTER_LANGSMITH_PROJECT` | LangSmith project name | `super-router` |
| `ROUTER_LANGSMITH_TAGS` | Comma-separated extra LangSmith tags | None |
| `ROUTER_LANGSMITH_TRACE_PROMPTS` | Include prompt previews in custom model-call traces | Off |
| `ROUTER_LANGSMITH_TRACE_OUTPUTS` | Include output previews in custom model-call traces | Off |
| `ROUTER_LANGSMITH_HIDE_INPUTS` | Request LangSmith SDK input hiding for graph traces | Off |
| `ROUTER_LANGSMITH_HIDE_OUTPUTS` | Request LangSmith SDK output hiding for graph traces | Off |
| `ROUTER_LANGSMITH_FLUSH` | Flush LangSmith traces before process exit | On |
| `ROUTER_TOKEN_USAGE_LEDGER` | Optional append-only JSONL path for per-call token usage records | None |

Large local models may require higher timeouts and `ROUTER_MAX_CONCURRENCY=1`.

Provider selection is model-name based:
- Codex CLI: `codex/...`, bare `gpt-*`, bare `chatgpt-*`, or bare `o` plus digit names such as `codex/gpt-5.5` or `gpt-5.5`.
  The router passes `--sandbox` but intentionally does not pass `--ask-for-approval`, because some `codex exec` versions do not support that option.
- Gemini CLI: `google-gemini-cli/...`, `gemini-*`, `pro`, `flash`, `flash-lite`, or `auto`.
- Claude Code CLI: `claude/...` or bare `claude-*` model names.
- Ollama: all other model names, or explicit `ollama/...`.

### LangSmith Telemetry

LangSmith is optional and non-fatal. Enable it only when external trace upload
is desired:

```bash
ROUTER_LANGSMITH_ENABLED=1
LANGSMITH_API_KEY=<your-langsmith-key>
ROUTER_LANGSMITH_PROJECT=super-router
```

The router adds graph tags/metadata and traces raw provider calls as child LLM
runs. Ollama token usage is captured from `prompt_eval_count` and `eval_count`.
Claude Code CLI token usage is captured from JSON `total_input_tokens` and
`total_output_tokens`. Gemini CLI token usage is captured from JSON
`stats.models.*.tokens` when available, with `usageMetadata`-style fields as a
fallback. Prompt and output text previews are disabled by default; enable them
explicitly with `ROUTER_LANGSMITH_TRACE_PROMPTS=1` or
`ROUTER_LANGSMITH_TRACE_OUTPUTS=1`.

### Token Usage Accounting

Token usage is tracked even when LangSmith is disabled. The router records every
successful provider call in a run-local ledger, prints a token summary after the
final report, and returns `token_usage` plus `token_usage_summary` in the final
state. Calls without provider token data are recorded as
`usage_source=unavailable`. Set
`ROUTER_TOKEN_USAGE_LEDGER=~/.openclaw/super-router-usage.jsonl` to persist the
per-call records as append-only JSONL.

If a super-router process stops before the final token ledger is printed, Gemini
CLI may still have persisted exact per-call token records in
`~/.gemini/tmp/<user>/chats/session-*.jsonl`. This applies to planning-capture
termination, timeouts, manual kills, crashes, executor fanout interruptions, and
metadata/finalizer failures. Use `references/gemini-cli-token-recovery.md` to
recover `input`, `output`, `cached`, `thoughts`, `tool`, and `total` fields from
matching session JSONL files. Treat recovered values as provider telemetry;
treat dollar cost separately because cached-token billing depends on provider
pricing.

## Complexity Routing Rules

### 5-Dimension Scoring

The Judge scores each subtask on:

1. **reasoning_depth** (1-10): How much logical inference is needed?
2. **code_change_scope** (1-10): How many files/lines of code to modify?
3. **ambiguity** (1-10): How unclear is the task specification?
4. **risk** (1-10): What's the impact of getting this wrong?
5. **io_heaviness** (1-10): How much reading/writing vs. thinking?

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

- **Output Structure**: The router returns a JSON-serializable state. When summarizing these results in reports or documentation, always use ASCII/Terminal-style arrows (e.g., '-->', '->') rather than mathematical arrows for all diagrams and flow representations. This is a high-priority stylistic requirement.

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
        "scores": {"reasoning_depth": 5, "code_change_scope": 3, "ambiguity": 2, "risk": 4, "io_heaviness": 1},
        "complexity_score": 15,
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
      "model_name": "...",
      "desc": "...",
      "output": "...",
      "status": "success|failed",
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
| `references/long-running-quantitative-tasks.md` | Guidance for heavy Monte Carlo / financial modeling tasks and background execution |
| `references/background-artifact-launches.md` | Wrapper pattern for background router runs that produce durable artifacts: prompt/context capture, stream logs, verification, and safe handling of blocked launches |
| `references/source-html-background-wrapper.md` | Concrete pattern for source-tree-to-HTML hierarchy/explainer jobs: source JSON collector, compact router prompt, HTML generator from context+log, background launch, immediate poll, and artifact verification |
| `references/linux-mm-source-html-example.md` | Session-specific exemplar for a large Linux `mm/` source hierarchy HTML guide: bucket taxonomy, artifact sections, and verification thresholds. Use as a model for similarly large kernel/subsystem explainers. |
| `templates/source-html-background-wrapper.sh` | Copyable shell wrapper template for source-tree-to-HTML background jobs. Use it to avoid retyping the run/status/log/verification scaffold; replace placeholders and tune verification thresholds per artifact. |

## Troubleshooting

### Verifying Model Routing

To audit which model each stage actually used, run with `--stream` and check the output:
- **Planner model**: printed as `规划模型: <model>` in the routing plan summary
- **Judge model**: printed as `判定模型: <model>` in the routing plan summary
- **PRO Executor**: printed as `-> <model>` per step in executor fanout
- **FLASH Executor**: printed as `-> <model>` per step
- **Metadata Extractor**: uses the PRO model
- **Finalizer**: routed to FLASH first, then PRO on failure — check `finalizer_outcome.route` / `finalizer_outcome.model_name` in the returned state

**Verification Audit Pattern**: For explicit per-phase LLM validation runs (e.g. K8s anomaly detection tasks), execute the router with a complex high-risk task, capture the full streaming transcript, then synthesize a self-contained HTML report. The report should include:
- Phase cards showing attempted model vs actual outcome (including heuristic fallbacks on quota errors)
- Routing decision table
- Key findings on whether PRO/FLASH routing matched expectations
- Recommendations for fallback configuration

This produces an auditable artifact that confirms the 5-node flow (Planner → Judge → Executor Fanout → Metadata → Finalizer) and surfaces any provider-specific issues like TerminalQuotaError without altering the core router logic.

### Non-Determinism with Cloud APIs

Even at `temperature=0.0`, cloud-hosted models may produce different decompositions across runs due to backend inference differences. The router is deterministic in its *routing logic*, not in upstream model sampling. For guaranteed reproducibility, cache planner results by task hash or use a seed parameter if the provider supports it.

### Timeouts or Empty Responses

- Use `--stream` and increase the terminal/process timeout if the Planner itself may take longer than 60s.
- Set `ROUTER_JUDGE_TIMEOUT` or `ROUTER_FINALIZER_TIMEOUT` higher for large models.
- If a model appears unexpectedly, check whether `~/.openclaw/.env` or the OpenClaw process environment contains stale `ROUTER_*_MODEL` values.

### Planner produced only one subtask

Task may be simple enough to not need decomposition, or the planner model may benefit from stronger prompting for atomic decomposition.

### FLASH kept escalating to PRO

Task may genuinely require heavy reasoning. Consider configuring a stronger FLASH model via `ROUTER_FLASH_MODEL`.

## Related Skills

- **dspy** — Declarative LM programming with automatic prompt optimization (Python framework alternative)
- **btc_analyzer** — OpenClaw BTC analysis workflow that delegates structured market questions to this router
- **api-tester** — API validation workflow that can route complex investigation subtasks through this router
- **ddg-search** — Search-oriented support skill for evidence gathering before router execution
- **llama-cpp** — Run LLM inference locally (alternative backend)

## See Also

- LangGraph documentation: https://langchain-ai.github.io/langgraph/
- Ollama documentation: https://ollama.com/docs

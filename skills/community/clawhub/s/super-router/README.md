# 🔀 Super Router

Super Router is a LangGraph-based task router for splitting a user task into
ordered subtasks, judging each subtask's complexity, and dispatching execution
to either a PRO model or a FLASH model.

The router is designed for multi-model workflows where simple reporting or
formatting work should use a fast model, while diagnosis, implementation,
architecture, high-risk incident triage, and ambiguous decisions should use a
stronger model. It includes planner and judge fallback paths, provider fallback
lists, FLASH retry and escalation logic, technical metadata extraction, and a
final report generation cascade.

## What It Does

- Decomposes a user task into atomic, actionable subtasks. Uses **Atomic Decomposition** to split multi-entity tasks into individual executor branches for true LangGraph fanout.
- Scores each subtask across reasoning depth, code change scope, ambiguity,
  risk, and IO heaviness.
- Routes each subtask to PRO or FLASH based on structured scores, confidence,
  summary detection, and high-risk context rules.
- Executes subtasks with configurable Gemini CLI or Ollama-backed models.
- Retries FLASH on transient infrastructure failures.
- Escalates FLASH work to PRO when the output is empty, low quality, too short,
  or explicitly says the model cannot complete the work.
- Supports provider fallback lists for PRO, FLASH, metadata extraction, and
  finalization.
- Extracts high-precision "technical gold" from completed step outputs before
  final synthesis.
- Produces a final report through a FLASH finalizer, then a PRO finalizer, then
  a deterministic fallback template if model finalization fails.

## Repository Layout

```text
.
|-- README.md
|-- SKILL.md
|-- scripts/
|   `-- router.py
`-- tests/
    |-- __init__.py
    `-- test_router.py
```

| Path | Purpose |
| --- | --- |
| `SKILL.md` | OpenClaw skill contract, usage notes, architecture summary, and environment reference. |
| `scripts/router.py` | LangGraph router implementation and CLI entry point. |
| `tests/test_router.py` | Regression tests for routing helpers, fallback behavior, finalization, streaming, and integration paths. |
| `tests/__init__.py` | Keeps tests importable as a package. |

## Requirements

- Python 3.10+ is recommended because the code uses modern type hint syntax.
- `langgraph` is required at runtime.
- At least one model provider must be usable:
  - Gemini CLI for `google-gemini-cli/...`, `gemini-*`, `pro`, `flash`, `flash-lite`, or `auto` model names.
  - Ollama for all other model names.
- Network access to Google endpoints is required for Gemini CLI unless your
  environment routes through a configured proxy.
- A running Ollama server is required for Ollama-backed models.
  - **Note:** For large models (e.g., `gemma4:26b`, `gemma4:31b`), setting `num_predict` to `204800` in `router.py` or the server config is a a practical way to avoid truncated JSON output in most cases.

## Installation

### As an OpenClaw skill

Keep the repository in an OpenClaw-accessible skill directory such as `~/.openclaw/skills/super-router`:

```bash
git clone https://github.com/fanyadan/super-router ~/.openclaw/skills/super-router
```

Then install the required Python dependency:
```bash
pip install langgraph
```

Once the skill is available to OpenClaw, you can trigger the router by asking to use `super-router` or by giving a task that clearly benefits from routed decomposition.

### As a standalone tool
Install the Python dependency:

```bash
pip install langgraph
```


If you plan to use Ollama-backed models, start Ollama separately and pull the
models you want to use:

```bash
ollama serve
ollama pull gemma4:26b
ollama pull llama3.1:8b
ollama pull qwen2.5:7b
```

If you plan to use Gemini CLI-backed models, install and authenticate the
`gemini` executable, or point the router to it with `ROUTER_GEMINI_CLI`.

## Quick Start

Run a task through the router:

```bash
python scripts/router.py "Inspect router state flow and summarize"
```

Enable node-level LangGraph progress output:

```bash
python scripts/router.py --stream "Analyze K8s YAML errors and prepare an action summary"
```

Pass the task through an environment variable:

```bash
ROUTER_TASK="Refactor auth module to use JWT, add tests, and update docs" \
python scripts/router.py
```

Run the regression suite:

```bash
python -m unittest tests/test_router.py
```

### From an OpenClaw agent

Invoke the router from the checked-out skill directory and pass any `ROUTER_*` overrides explicitly rather than relying on shell startup files:

```bash
bash workdir:~/.openclaw/skills/super-router command:"ROUTER_PLANNER_MODEL=google-gemini-cli/gemini-3-pro-preview ROUTER_JUDGE_MODEL=llama3.1:8b /opt/homebrew/Caskroom/miniforge/base/bin/python scripts/router.py 'Inspect router state flow and summarize'"
```

For long-running tasks, stream in the background and monitor the session:

```bash
bash workdir:~/.openclaw/skills/super-router background:true command:"/opt/homebrew/Caskroom/miniforge/base/bin/python scripts/router.py --stream 'Analyze K8s YAML errors and prepare an action summary'"
process action:poll sessionId:<session-id>
process action:log sessionId:<session-id>
```

## Provider Selection

The router selects the provider from the model name:

- Gemini CLI is used when the model name is one of `auto`, `pro`, `flash`,
  `flash-lite`, starts with `gemini-`, or uses the `google-gemini-cli/` prefix.
- Ollama is used for all other model names.

Examples:

```bash
# Gemini CLI-backed PRO/FLASH execution.
export ROUTER_PRO_MODEL=google-gemini-cli/gemini-3-pro-preview
export ROUTER_FLASH_MODEL=google-gemini-cli/flash

# Ollama-backed planner/judge/executors.
export ROUTER_PLANNER_MODEL=gemma4:26b
export ROUTER_JUDGE_MODEL=llama3.1:8b
export ROUTER_PRO_MODEL=qwen3
export ROUTER_FLASH_MODEL=qwen2.5:7b
```

For local large models, prefer a strong planner and a smaller judge:

```bash
export ROUTER_PLANNER_MODEL=gemma4:26b
export ROUTER_JUDGE_MODEL=llama3.1:8b
export ROUTER_MAX_CONCURRENCY=1
```

## Architecture

The main graph is implemented in `scripts/router.py` with LangGraph
`StateGraph`.

```text
START
  -> planner_warmup
  -> planner_invoke
  -> planner_parse
  -> planner_ready
  -> judge_warmup
  -> judge_subtask fanout
  -> assemble_plan
  -> parallel_executor fanout
  -> parallel_execution_join
  -> deferred_executor fanout for synthesis/reporting subtasks
  -> execution_finalize_join
  -> flash_finalizer
  -> flash_finalizer_verify
  -> pro_finalizer or deterministic_finalizer when needed
  -> finalizer_complete
  -> END
```

The router also has a small nested provider fallback graph used by
`invoke_with_provider_fallback()`:

```text
model_attempt_prepare -> model_invoke -> retry next provider or finish
```

## Runtime Flow

1. Planner warmup pings the planner model three times.
2. Planner invoke asks the planner to emit a raw JSON array of subtask objects.
3. Planner parse extracts and normalizes subtasks.
4. Planner fallback creates heuristic subtasks if planning fails or returns
   invalid JSON.
5. Communication subtasks are split out when a task mixes investigation and
   reporting.
6. Judge warmup pings the judge model before fanout.
7. Judge fanout scores every planned subtask independently.
8. Judge fallback applies heuristic scoring when the model call or JSON parse
   fails.
9. Executor fanout dispatches independent subtasks concurrently through
   LangGraph `Send(...)`, bounded by `ROUTER_MAX_CONCURRENCY`.
10. Each executor branch invokes the selected route, including any provider
   fallbacks.
11. FLASH review verifies FLASH output inside the branch and either records,
   retries, or escalates
   to PRO.
12. Each branch records its own outcome and extracts atomic technical facts from
   successful output.
13. Synthesis/reporting subtasks run after the independent branches so they can
   see completed context.
14. The final join orders results by original step number.
15. Finalizer creates the final report with FLASH, PRO, or a deterministic
   fallback template.

## Task Splitting

Task splitting happens in the planner phase. The planner receives the original
task and is prompted to return only a raw JSON array:

```json
[
  {"desc": "Inspect the failing API path and isolate the root cause"},
  {"desc": "Prepare a concise team status update with the findings"}
]
```

The planner is asked to produce 2-6 ordered subtasks that are atomic,
actionable, and outcome-oriented. It must not assign model names, route labels,
or complexity scores. Routing is handled later by the judge.

After the model response is received, the router:

1. Extracts the first valid JSON array from the response.
2. Normalizes each item into `{"desc": "..."}` form.
3. Drops empty subtasks.
4. Splits mixed investigation/reporting steps when possible.
5. Adds a separate communication subtask when the original task asks for a
   summary, status update, impact note, report, or message for another person.

For example, a planned step like this:

```text
Debug intermittent API failure and send a concise team update
```

can become:

```json
[
  {"desc": "Debug intermittent API failure"},
  {"desc": "send a concise team update"}
]
```

If the planner fails, times out, or returns invalid JSON, the router uses a
heuristic fallback. The fallback creates core analysis/implementation subtasks
for tasks containing words such as `analyze`, `debug`, `fix`, `refactor`,
`rewrite`, `implement`, `design`, or their Chinese equivalents. It also adds a
final summary/reporting subtask when the original task asks for documentation,
status output, saving, or reporting.

## Complexity Identification

Complexity identification happens after task splitting. Each normalized subtask
is sent independently to the judge model along with the original task for risk
context. The judge returns raw JSON with:

```json
{
  "scores": {
    "reasoning_depth": 2,
    "code_change_scope": 1,
    "ambiguity": 1,
    "risk": 0,
    "io_heaviness": 0
  },
  "suggested_route": "PRO",
  "confidence": 0.87,
  "reason": "Requires debugging and non-trivial code inspection."
}
```

The router then normalizes and clamps score values to their allowed ranges:

| Field | Range | Meaning |
| --- | --- | --- |
| `reasoning_depth` | 0-3 | Lookup/formatting through architecture or open-ended investigation. |
| `code_change_scope` | 0-3 | No code through broad refactor or migration. |
| `ambiguity` | 0-2 | Clear through unclear/open-ended. |
| `risk` | 0-2 | Low-risk through high-risk or hard-to-reverse. |
| `io_heaviness` | 0-2 | Little IO through mostly reporting/formatting. |

Then it applies contextual biases before making the final route decision:

- Summary/status/reporting subtasks are biased toward FLASH when they do not
  contain deep-work terms.
- Diagnostic, debugging, implementation, refactor, migration, design, and logic
  subtasks are biased toward PRO.
- Production, billing, payment, finance, auth, security, rollback, containment,
  and incident-related subtasks are treated as high risk.
- Evidence gathering in high-risk incidents stays on PRO when it supports
  diagnosis or decision-making, even if it mostly reads logs or data.
- Low-confidence boundary cases default to PRO.

If judge model scoring fails, the router builds a heuristic assessment from
keywords in the subtask text and original task. That fallback uses the same
score fields and the same final route decision function, so planner or judge
failures still produce an auditable routing plan.

## Routing Model

Each subtask is scored on five dimensions:

| Field | Range | Meaning |
| --- | --- | --- |
| `reasoning_depth` | 0-3 | Lookup/formatting through architecture or open-ended investigation. |
| `code_change_scope` | 0-3 | No code through broad refactor or migration. |
| `ambiguity` | 0-2 | Clear through unclear/open-ended. |
| `risk` | 0-2 | Low-risk through high-risk or hard-to-reverse. |
| `io_heaviness` | 0-2 | Little IO through mostly reporting/formatting. |

The aggregate `complexity_score` is:

```text
reasoning_depth + code_change_scope + ambiguity + risk
```

General routing rules:

| Condition | Route |
| --- | --- |
| Summary, report, recap, or status update with no deep-work language | FLASH |
| High-risk production, billing, payment, finance, auth, security, rollback, or containment work | PRO |
| Diagnostic investigation, debugging, fixing, implementation, migration, refactor, or design work | PRO |
| Judge confidence below `0.35` | PRO |
| `complexity_score >= 5` | PRO |
| Any of reasoning depth, code change scope, or risk is at least `2` | PRO |
| `complexity_score <= 2` and IO-heavy | FLASH |
| Low-complexity IO-heavy task with high confidence | FLASH |
| Unclear boundary case | PRO |

High-risk evidence gathering is intentionally kept on PRO because log review,
configuration comparison, data reconciliation, or transaction inspection can be
part of root-cause analysis rather than simple IO.

## FLASH Review and Escalation

FLASH output goes through a review node before it is recorded.

Infrastructure failures are retried within the configured retry budget:

- timeout
- network failure
- rate limit
- connection reset/refused
- service unavailable
- transport or deadline errors

Capability or quality failures escalate to PRO:

- empty output
- output shorter than 48 characters for a non-summary task
- output simply repeats the subtask description
- output says it cannot complete or needs more context
- provider failure that looks like insufficient capability rather than
  infrastructure

If FLASH retry budget is exhausted, the router records a deterministic failure
message for that step and continues to finalization instead of crashing the
whole graph.

## Provider Fallback

PRO and FLASH can each have fallback model lists. Fallbacks are tried only when
the failure looks infrastructure-related or unknown. The fallback loop stops on
capability or quality failures because trying a different provider is unlikely
to fix a task that needs stronger reasoning.

```bash
export ROUTER_PRO_MODEL=google-gemini-cli/gemini-3-pro-preview
export ROUTER_PRO_FALLBACK_MODELS=qwen3,gemma4:26b

export ROUTER_FLASH_MODEL=google-gemini-cli/flash
export ROUTER_FLASH_FALLBACK_MODELS=qwen2.5:7b,llama3.1:8b
```

Duplicate model names are removed before invocation.

## Finalization

Final report generation follows this cascade:

```text
FLASH finalizer -> PRO finalizer -> deterministic finalizer
```

The finalizer prompt includes:

- original task
- planner model
- judge model
- technical metadata blocks from successful steps
- execution log JSON

The model-generated final report must be non-empty, avoid "cannot complete"
style low-quality markers, and be at least 80 characters. Otherwise the router
continues to the next finalizer path.

The deterministic finalizer serves as a critical safety net, ensuring a result is
returned even when massive synthesis prompts cause API timeouts or model failures.

If FLASH and PRO resolve to the same effective model path and FLASH fails for a
non-capability reason, the router skips redundant PRO escalation and goes
straight to the deterministic finalizer.

## Environment Variables

| Variable | Default | Purpose |
| --- | --- | --- |
| `ROUTER_TASK` | unset | Task text used when no positional CLI task is provided. |
| `ROUTER_PLANNER_MODEL` | `gemma4:26b` | Model used to decompose the original task into subtasks. |
| `ROUTER_JUDGE_MODEL` | `llama3.1:8b` | Model used for structured complexity scoring. |
| `ROUTER_PRO_MODEL` | `google-gemini-cli/gemini-3-pro-preview` | Primary heavy reasoning executor and PRO finalizer model. |
| `ROUTER_FLASH_MODEL` | `google-gemini-cli/flash` | Primary fast executor and FLASH finalizer model. |
| `ROUTER_PRO_FALLBACK_MODELS` | unset | Comma-separated provider fallback list for PRO. |
| `ROUTER_FLASH_FALLBACK_MODELS` | unset | Comma-separated provider fallback list for FLASH. |
| `ROUTER_FLASH_RETRY_BUDGET` | `1` | Number of FLASH retries for transient or unknown failures before recording failure. |
| `ROUTER_RECURSION_LIMIT` | `128` | LangGraph recursion limit for the main router graph. |
| `ROUTER_MAX_CONCURRENCY` | `auto` | Max concurrent LangGraph branches for judge and executor fanout. Essential for multi-entity atomic tasks; set to `1` for local 26B+ Judge models or constrained hardware. |
| `ROUTER_JUDGE_TIMEOUT` | `6000` for large judge models, otherwise `300` | Timeout in seconds for judge model calls. Use high values (6000) as a workaround to prevent timeouts during complex reasoning. |
| `ROUTER_FINALIZER_TIMEOUT` | `6000` | Timeout in seconds for FLASH and PRO finalizer calls. |
| `ROUTER_OLLAMA_URL` | `http://localhost:11434/api/generate` | Ollama generate endpoint. |
| `ROUTER_GEMINI_CLI` | first `gemini` on `PATH`, else `/opt/homebrew/bin/gemini` | Gemini CLI executable path. |
| `ROUTER_DEBUG` | false | Enables raw planner, judge, and Ollama diagnostic output when set to `1`, `true`, `yes`, `on`, or `debug`. |

The PRO executor timeout, FLASH executor timeout, and default finalizer timeouts
are conservative in the current code (`6000` seconds) to support long-running
large-model workflows. External terminal or process timeouts can still stop the
router before those internal timeouts are reached.

## CLI

```text
usage: router.py [-h] [--stream] [task ...]
```

Arguments:

| Argument | Meaning |
| --- | --- |
| `task` | Task description. All positional words are joined with spaces. If omitted, `ROUTER_TASK` is used. |
| `--stream` | Emit node-level LangGraph progress updates while the graph runs. |
| `-h`, `--help` | Show CLI help. |

## Python API

The router can also be imported from Python:

```python
from scripts.router import run_router_app

state = run_router_app(
    "Inspect router state flow and summarize",
    planner_model="gemma4:26b",
    judge_model="llama3.1:8b",
    pro_model="google-gemini-cli/gemini-3-pro-preview",
    flash_model="google-gemini-cli/flash",
    max_concurrency=1,
    stream=True,
)

print(state["status"])
print(state["final_report"])
```

Useful lower-level helpers:

| Helper | Purpose |
| --- | --- |
| `create_initial_state()` | Resolve models, retry budgets, fallback lists, and initial graph state. |
| `prepare_router_run()` | Build the graph and resolve graph config without invoking it. |
| `run_router_app()` | Main programmatic entry point. |
| `generate_text()` | Provider-dispatching text generation helper. |
| `invoke_with_provider_fallback()` | Provider fallback graph wrapper. |
| `build_fallback_assessment()` | Heuristic judge fallback. |
| `verify_flash_output()` | FLASH quality guard. |
| `build_fallback_report()` | Deterministic final report builder. |

## Output State

`run_router_app()` returns a JSON-serializable router state. Important fields:

```json
{
  "task": "original task string",
  "planner_model": "model used for planning",
  "judge_model": "model used for scoring",
  "pro_model": "primary PRO model",
  "flash_model": "primary FLASH model",
  "pro_fallback_models": ["optional", "fallbacks"],
  "flash_fallback_models": ["optional", "fallbacks"],
  "planned_subtasks": [{"desc": "subtask text"}],
  "subtasks": [
    {
      "desc": "subtask text",
      "model": "PRO",
      "assessment": {
        "scores": {
          "reasoning_depth": 2,
          "code_change_scope": 1,
          "ambiguity": 1,
          "risk": 0,
          "io_heaviness": 0
        },
        "complexity_score": 4,
        "suggested_route": "PRO",
        "final_route": "PRO",
        "confidence": 0.9,
        "reason": "Requires investigation.",
        "judge_source": "structured_llm"
      }
    }
  ],
  "results": [
    {
      "step": 1,
      "planned_route": "FLASH",
      "route": "PRO",
      "model_name": "google-gemini-cli/gemini-3-pro-preview",
      "desc": "subtask text",
      "output": "model output",
      "status": "executed",
      "attempt_count": 1,
      "retry_count": 0,
      "escalated_from_flash": true,
      "used_provider_fallback": false,
      "flash_review": {
        "decision": "escalate",
        "failure_type": "capability_quality",
        "reason": "FLASH output was too short for a non-summary step."
      },
      "attempt_log": ["audit log entries"]
    }
  ],
  "history": ["graph audit history"],
  "errors": ["fallback or failure messages"],
  "final_report": "final report text",
  "finalizer_outcome": {
    "route": "FLASH",
    "model_name": "google-gemini-cli/flash",
    "status": "finished",
    "used_provider_fallback": false,
    "reason": "Finalizer output passed heuristic verification.",
    "attempt_log": ["audit log entries"]
  },
  "status": "finished"
}
```

## Development

Run the tests before and after router changes:

```bash
python -m unittest tests/test_router.py
```

The tests use `unittest` and `unittest.mock`; they do not require live Ollama or
Gemini access. Mock model calls with `mock.patch.object(r, "generate_text", ...)`
when adding new tests.

Useful focused checks:

```bash
python -m unittest tests.test_router.RouterHelperTests
python -m unittest tests.test_router.ProviderFallbackTests
python -m unittest tests.test_router.FlashReviewAndMetadataTests
python -m unittest tests.test_router.FinalizerTests
python -m unittest tests.test_router.RouterGraphIntegrationTests
```

## Testing Strategy

Current tests cover:

- environment parsing and default state construction
- JSON extraction and planner normalization
- communication subtask splitting
- contextual routing biases
- Gemini timeout forwarding
- stream event helpers
- provider fallback retries and capability stop behavior
- FLASH review, retry, and escalation guards
- metadata extraction behavior
- finalizer timeout and model path checks
- full mocked graph success path
- FLASH quality escalation to PRO
- streamed graph execution

When changing router logic, add regression coverage for:

- route decisions and score normalization
- provider fallback order
- new environment variables or default values
- stream output summaries
- finalizer fallback behavior
- any new graph edge or state field

## Troubleshooting

### Task description required

Provide a positional task or set `ROUTER_TASK`:

```bash
ROUTER_TASK="Summarize the router graph" python scripts/router.py
```

### Gemini CLI executable was not found

Install Gemini CLI or set:

```bash
export ROUTER_GEMINI_CLI=/path/to/gemini
```

### Gemini network preflight failed

The router checks access to Google endpoints before invoking Gemini CLI when no
proxy is configured. If your environment requires a proxy, configure one of:

```bash
export HTTPS_PROXY=http://proxy.example:8080
export HTTP_PROXY=http://proxy.example:8080
export ALL_PROXY=socks5://proxy.example:1080
```

### Unable to reach Ollama

Start Ollama and confirm the endpoint:

```bash
ollama serve
export ROUTER_OLLAMA_URL=http://localhost:11434/api/generate
```

### Planner or judge is slow

Large local models can take minutes, especially on first load. Use streaming and
serialize judge/executor fanout:

```bash
export ROUTER_MAX_CONCURRENCY=1
python scripts/router.py --stream "Analyze production K8s incident and draft summary"
```

For speed, keep the planner strong and the judge smaller:

```bash
export ROUTER_PLANNER_MODEL=gemma4:26b
export ROUTER_JUDGE_MODEL=llama3.1:8b
```

### FLASH keeps escalating to PRO

This usually means the FLASH output failed the quality guard or the task was
not actually simple reporting work. Try a stronger FLASH model or inspect the
`flash_review` field in `state["results"]`.

### Finalizer falls back to the deterministic report

Check `finalizer_outcome`, `finalizer_error`, and `finalizer_attempt_log` in the
returned state. Common causes are provider timeouts, authentication failures,
or short/empty finalizer output.

## Example Workflows

### Incident triage

```bash
python scripts/router.py --stream \
  "Analyze production K8s pod restarts, identify root cause, propose a fix, and prepare an on-call action summary"
```

Expected behavior:

- log inspection and root-cause work routes to PRO
- repair planning routes to PRO
- final on-call summary routes to FLASH unless it requires new analysis

### Code refactor

```bash
python scripts/router.py \
  "Refactor auth module to use JWT, add unit tests, and update docs"
```

Expected behavior:

- implementation and test design routes to PRO
- documentation-only update can route to FLASH

### Simple summary

```bash
python scripts/router.py "Summarize the last 10 git commits"
```

Expected behavior:

- summary-like work routes to FLASH

## Security Notes

- Do not commit local model credentials, private endpoint URLs, or Gemini CLI
  authentication artifacts.
- Use environment variables for local overrides.
- Keep tests deterministic and offline by mocking `generate_text()`.
- Treat PRO/FLASH outputs as model-generated text; downstream automation should
  validate before making irreversible changes.

## Related Documentation

- `SKILL.md` for OpenClaw-specific skill instructions.
- LangGraph documentation: https://langchain-ai.github.io/langgraph/
- Ollama documentation: https://ollama.com/docs

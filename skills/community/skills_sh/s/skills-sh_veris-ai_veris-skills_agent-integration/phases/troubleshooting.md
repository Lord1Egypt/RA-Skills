# Troubleshooting

Common integration issues organized by symptom.

## `veris-cli` bootstrap problems

### `veris` command not found

Install the CLI first:

```bash
uv tool install veris-cli
```

Fallback:

```bash
pip install veris-cli
```

### `veris env push` says no environment is configured

The repo is missing `.veris/config.yaml` with an environment binding. Run:

```bash
veris env create --self-serve --name "<env-name>"
```

Use `--self-serve` for this skill's flow; plain `veris env create` can place the env in managed onboarding and block `veris env push` with a 409.

### Auth problems

If the CLI is installed but backend calls fail, the user likely needs:

```bash
veris login
```

Or API-key login for headless contexts.

## Agent fails to start

Common causes:

1. Missing required env var
2. Wrong `entry_point`
3. Wrong `code_path`
4. Missing dependency install in `Dockerfile.sandbox`
5. Bundled service not started before the agent

Check the agent logs first. The startup error usually points directly at the missing dependency or bad command.

## Actor cannot reach the agent

For HTTP / WS / email integrations:

1. `actor.channels[].url` points at the wrong port or path
2. `agent.port` does not match the server’s listen port
3. The agent binds only to `127.0.0.1` instead of `0.0.0.0`
4. The server takes too long to become healthy

For function integrations:

1. `callable` import path is wrong
2. Wrapper file was not copied into `/agent`
3. The callable returns a shape the driver cannot serialize cleanly

## Agent runs but cannot reach mocked services

Common causes:

1. Missing or wrong `services:` entry
2. Wrong `dns_aliases`
3. Wrong env-var override, especially old docker-compose hostnames that should be `localhost`
4. Missing mock credentials

Check `reference/service-mapping.md` and `reference/env-var-overrides.md`.

## Grader flags a voice agent for hallucinating tools it actually called

Symptom: a `voice_ws` / phone agent runs its tools correctly (the agent logs, and any mock-service logs, show the calls happening and the database changing), but the grader reports "no tool call," "fabricated," or "claimed an action without calling the tool."

Cause: the agent uses **client tools** (ElevenLabs Conversational AI, OpenAI Realtime, Gemini Live, …) that execute in-process and round-trip on the vendor WebSocket, so they never reach the spoken transcript the voice grader reads. Without an explicit report, the grader is blind to them. This is a grading-visibility issue, not an agent bug — the actions really happened.

Fix: emit an `agent_tool_call` event per tool call — see [reference/voice-channels.md](../reference/voice-channels.md#making-client-tool-calls-visible-to-the-grader) for the contract and copy-paste hook. If you already added the hook and still see this, check:

1. `event_type` is exactly `agent_tool_call`, and `data.name` / `data.arguments` are present (the renderer needs both).
2. `SIMULATION_ID` is set in the agent process — it's exported by the sandbox; if your hook silently no-ops, it isn't reading the env you think it is.
3. The POST is actually landing — a swallowed connection error logs `could not report <tool> to engine`. Confirm `ENGINE_URL` (default `http://localhost:6100`) is reachable from the agent.

## Voice agent never answers under load (`callee_no_answer`)

Symptom: a LiveKit-based `voice_ws` agent connects fine in a single local smoke test, but under concurrent simulations a chunk of calls end in `callee_no_answer` — the actor connects, the room is created, but the agent never joins. The failure rate climbs with concurrency.

Cause: LiveKit's worker/auto-dispatch model has two race/throttle traps a plain WS server doesn't (see [infrastructure-patterns.md → LiveKit dispatch gotchas](../reference/infrastructure-patterns.md#livekit-dispatch-gotchas)):

1. **Dispatch race.** The worker registers with the SFU asynchronously, and auto-dispatch only fires for rooms created *after* registration. If the bridge accepts a caller before the worker registers (a fixed `sleep` instead of a real gate), the room exists but the agent is never dispatched into it. Under load, registration can take 10s+.
2. **CPU self-throttle.** A prod-mode `AgentServer` refuses dispatch when its CPU load function exceeds 0.7; with the SFU + worker + bridge + realtime session sharing one pod, that trips under load and the SFU reports "no workers with sufficient capacity."

Fix (both are agent-side; neither needs a `veris-sandbox` change):

1. Gate the bridge on the worker's `registered worker` log line (poll, ~60s ceiling), not a fixed sleep — see the `start.sh` in [Pattern 9](../reference/infrastructure-patterns.md#pattern-9-transport-bridge).
2. Disable the throttle: `AgentServer(load_fnc=lambda *_: 0.0)`.

## Vapi calls fail to connect under concurrency (ngrok contention)

Symptom: a Vapi-based `voice_ws` agent passes single smoke tests and small batches, but in a larger concurrent batch most calls end in `callee_no_answer` — the agent never finishes setting up the Vapi call. Agent logs show repeated ngrok spawn attempts ending in a session-limit error (e.g. `ERR_NGROK_334`).

Cause: Vapi delivers tool calls as HTTP webhooks to a public `server.url`, and the common integration spawns an in-pod ngrok tunnel to provide one. Free-tier ngrok allows **one agent session per authtoken** — every concurrent pod contends for it, and the losers retry with backoff, exhaust their attempts, and fail call setup. It looks like a flaky agent; it's the tunnel.

Fix, in increasing order of robustness:

1. **Serialize** — run one simulation at a time; each gets the single tunnel in turn.
2. **Remove the limit** — a paid ngrok plan or a (free) Cloudflare Tunnel allows concurrent tunnels.
3. **Shared stable endpoint (production shape)** — set `PUBLIC_BASE_URL` to one public webhook endpoint so pods skip in-pod tunnels entirely, and route inside it by `call.id`. Vapi correlates tool results by `toolCallId`, not by connection, so one stateless endpoint serves the whole fleet.

See [voice-channels.md → Vapi](../reference/voice-channels.md#vapi-hosted-runtime-server-tool-webhooks).

## Vapi agent acts like its tool returned nothing

Symptom: the agent's logs show the tool executed and the `/tool` webhook returned a result, but the model behaves as if it got no observation — it stalls, apologizes, or claims it couldn't complete the action. Vapi's call logs show "No result returned".

Cause: the webhook response didn't match Vapi's schema. The `result` field must be a JSON **string** (not a dict) and the response must be HTTP 200 — anything else is silently dropped and the model continues with no observation. Nothing hangs and nothing errors, so the failure is invisible in the agent's own logs.

Fix: wrap every successful result with `json.dumps(output, default=str)` (single-line), return failures as a string under the `error` key, and always return 200. See the [tool-result pitfall](../reference/voice-channels.md#common-pitfalls).

## Database connection fails

Common causes:

1. Old docker hostname (`postgres`, `db`) instead of `localhost`
2. Password mismatch between `services[].config.POSTGRES_PASSWORD` and `DATABASE_URL`
3. Schema file copied to the wrong path
4. Wrong database name instead of `SIMULATION_ID`

## Bundled service fails

Common causes:

1. Service package not installed in `Dockerfile.sandbox`
2. Service not started or not health-checked in `start.sh`
3. Port conflict
4. Service is too heavy and should have stayed external

## Build fails

Common causes:

1. Wrong build context
2. Bad `COPY` path
3. Dependency manifest copied incorrectly
4. Missing system package
5. `WORKDIR /app` omitted at the end

The correct local smoke-test command is:

```bash
docker build -f .veris/Dockerfile.sandbox .
```

from the repo root.

## Build fails due to source-tree compile errors

If `pip install -e .` or `pip install .` fails because the repo's own source files have syntax errors, broken imports, or missing type stubs:

1. Check whether the repo is a **platform-hosted agent** (config-only, framework-as-runtime). If so, do not install the repo as an editable package.
2. Instead, install the framework and its dependencies from published packages:
   ```dockerfile
   RUN pip install crewai langchain-openai  # framework + plugins
   ```
3. COPY only the config/prompt/tool files the framework needs — not the entire source tree as an installable package.
4. If the repo does contain real application code that must be installed, try `pip install --no-build-isolation .` or fix the specific compile errors. Common causes: missing `build-system` in `pyproject.toml`, Cython extensions without a C compiler, or Python version mismatch.

## `veris env create` scaffold produces broken config

If `veris env create` succeeds but reports a non-fatal config upload error (typically a 422 on the `services` list), the scaffolded `veris.yaml` has fields the backend does not accept.

This is expected — the scaffolded config is a placeholder with commented-out examples. Fix it:

1. Regenerate `.veris/veris.yaml` using the current preferred shape from `reference/veris-yaml-schema.md`
2. Ensure `services:` is a valid YAML list (not commented-out blocks that parse as an empty mapping)
3. Re-push with `veris env push`

## `veris env push` returns 409: managed onboarding

If `veris env push` returns `[409] Run veris env submit first to complete managed onboarding`, the env was created in managed-setup mode (the default for plain `veris env create`). Managed-setup envs do not accept image pushes until onboarding completes. `-f` / `--force` does not bypass this — it only affects the local config sync-guard, not the server-side gate.

For this skill's audience (self-authoring `.veris/`), `--self-serve` at create time is the right fix. Three recovery paths in increasing order of effort:

1. **You forgot `--self-serve`:** `veris env delete <env-id>`, then `veris env create --self-serve --name <name>`. Re-set any `veris env vars set` values on the new env, and update `.veris/config.yaml` if the env id changed.
2. **Your CLI doesn't show `--self-serve`:** upgrade to veris-cli 2.27.0 or newer using the install manager that owns `veris` (`uv tool upgrade veris-cli` or `pip install -U veris-cli`), then take path 1.
3. **You actually want managed onboarding:** run `veris env submit`, wait for the Veris team's email, then `veris env config pull` followed by `veris env push`.

## Base image runtime version too old for agent

If the agent requires a newer Python or Node.js than the base image provides:

1. Check the agent's dependency manifests for explicit version constraints (`python_requires >= "3.13"`, `engines.node >= "20"`)
2. Add a runtime version override to `Dockerfile.sandbox` — see the "Runtime version override" section in `templates/dockerfile-sandbox.md`
3. For Python, install the newer version alongside the base and create a dedicated virtualenv
4. For Node.js, overlay the newer binary and it will replace the base version on PATH

## Runtime env vars are missing

Common causes:

1. Secret was never set with `veris env vars set`
2. The value belongs in `agent.environment` but is missing there
3. The user expected `.env.simulation`, which is no longer the preferred flow
4. Secret was set via shell interpolation (`veris env vars set KEY="$VAR" --secret`) but `$VAR` was empty or unset — the CLI saved an empty string with no error

Fix:
- use `veris env vars set` for secrets and per-env overrides
- use `agent.environment` for stable non-secret defaults
- optionally mirror local values in a root `.env` for local-only smoke tests
- if a secret might have been set empty, verify with `printenv VAR` before setting, or re-set it with a literal value

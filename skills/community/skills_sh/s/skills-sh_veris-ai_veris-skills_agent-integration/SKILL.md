---
name: agent-integration
description: Integrate a raw customer agent repo with Veris end to end. Installs or verifies veris-cli, logs in, creates or reuses a Veris environment, analyzes the repo, generates or updates `.veris/veris.yaml`, `.veris/Dockerfile.sandbox`, `.veris/.dockerignore`, configures runtime env vars, and can finish with `veris env push`. Use when a repo has no Veris setup yet, or when an existing `.veris/` integration is stale and needs to be refreshed.
---

Integrate this agent repo with Veris from scratch.

This skill takes a repo from "plain customer agent source" to "Veris-ready and pushable." If the user provided a path to an agent repo, use that as the repo root. Otherwise use the current working directory.

Treat any existing `.veris/` files or old scaffold output as starting material only. Use the current bundled references in this skill as the source of truth for what you generate.

## Core framing: the agent is the constant, Veris is the test harness

Veris exists to test an agent under realistic conditions. The agent is the thing being tested; Veris is the harness around it. That asymmetry drives every decision in this skill:

- **The agent runs the same way in Veris as it does in production.** If the agent speaks HTTP to a Slack Web API in prod, it speaks HTTP to the Veris Slack mock in sim. If it shells out to a CLI in prod, it shells out in sim. No special simulation code path.
- **All integration work lives in `.veris/`.** `.veris/veris.yaml`, `.veris/Dockerfile.sandbox`, `.veris/config.yaml`, `.veris/.dockerignore` are the deployment descriptor — the equivalent of a Helm chart or `docker-compose.yaml` for this agent. They describe *how to stand the agent up for this environment*. They do not contain behavior that belongs inside the agent.
- **Do not write wrappers, shims, or glue code that "adapts" the agent to Veris.** A Python file that wraps a CLI agent to expose a callable, a script that translates Veris's actor format into the agent's native format, a patched version of the agent that accepts Veris-specific parameters — all of these are the wrong shape. They mean the thing you end up testing is not the agent.
- **Do not modify the agent's source code to make it work in Veris.** If the agent assumes something Veris can't satisfy as-is, that's either a Veris platform gap to be logged, or a real issue with the agent that would also break production. Either way, the fix does not belong in the agent's source.
- **If you find yourself needing a wrapper, stop and treat it as a finding.** Ask: what is the agent's real production integration path? If the agent has an HTTP server in prod, use that. If it's CLI-only in prod and Veris's actor can't drive a CLI, escalate — that's a Veris capability gap, not a license to invent glue.
- **The one legitimate `.veris/` file that is not pure config is a container-orchestration `start.sh`** for bundling multiple processes (e.g., a database alongside the agent). Even that starts and runs the agent as-shipped; it does not transform its behavior.

When in doubt: the agent's author should be able to read `.veris/` and recognize it as "the deploy config for Veris," not as "someone forked and patched my agent."

### Transport bridges are an explicit exception

A **transport bridge** translates between the actor's channel format (e.g. `voice_ws` PCM16) and the agent framework's native transport (e.g. LiveKit WebRTC, SIP media, a proprietary message envelope) while preserving the underlying payload byte-for-byte. It is *not* a wrapper. The same shape exists in production for the agent's other product surfaces — mobile clients, kiosks, IVR vendors — so the bridge is genuine product code, not Veris-specific glue.

A bridge is allowed when:

- The agent's framework cannot be reconfigured to speak the actor's channel format directly (e.g., LiveKit Agents is WebRTC end-to-end and has no raw-PCM16-WS transport).
- The bridge is pure transport translation: same audio bytes / same JSON payloads in and out, with no semantic reshaping. (For voice, the audio bytes the agent's model receives must be identical to what the actor sent. For text, the message payload the agent sees must be identical to what the actor sent.)
- The bridge lives in the agent's repo as production code (e.g., `app/bridge.py`), exercised by the agent's own tests — not in `.veris/`. It is the agent's `voice_ws`-on-WebRTC product surface; Veris is just one caller.

A bridge is **not** allowed when:

- It reshapes content the agent sees: rewriting messages, restructuring tool-call JSON, normalizing STT output, translating Veris-specific actor fields into the agent's native parameters. That is a wrapper, and the no-wrapper rule above applies.
- The framework *can* be configured to speak the actor's channel (Pipecat with `RawAudioFrameSerializer` for `voice_ws`, the framework's own HTTP plugin for `http`, etc.). Configure the framework first; bridge only if the transport is fixed.

Quick rubric: "same bytes, different network format" = transport bridge (allowed). "Different bytes / different shape" = wrapper (not allowed).

See [reference/infrastructure-patterns.md Pattern 9](reference/infrastructure-patterns.md#pattern-9-transport-bridge) for the architecture and [reference/voice-channels.md](reference/voice-channels.md) for the voice-specific application.

### Reporting client-tool calls to the grader is a sanctioned exception (voice agents only)

This is the one exception that genuinely breaks the "no Veris-specific code path" rule — and it is deliberate. It applies only to **voice agents built on hosted speech-to-speech platforms** (ElevenLabs Conversational AI, OpenAI Realtime, Gemini Live, Vapi, and the like) whose tools execute inside the agent process — as **client tools** that round-trip on the vendor's WebSocket, or as Vapi-style **server tools** the platform POSTs back to the agent's webhook over HTTP. Either way the call never reaches the spoken transcript.

Why it's needed: the voice grader builds its trace from the spoken transcript plus any tool-call events the agent reports. A client tool never reaches the transcript, so without a report the grader can't see the tool ran and false-flags real actions (a card freeze, a replacement) as hallucinations. Text/HTTP agents don't have this problem — their tool calls are captured automatically — so this exception is voice-only.

The fix: after each tool runs, the agent POSTs an `agent_tool_call` event to the sandbox engine, and the platform renders it into the graded trace. Keep it strictly minimal so it stays instrumentation, not a wrapper:

- **No-op outside a simulation.** Gate on `SIMULATION_ID` (unset in production → return immediately). Production behavior is unchanged.
- **Fire-and-forget, fail-soft.** Short timeout, swallow errors, log a warning. A reporting failure must never break the call or change the agent's output.
- **Observe, don't reshape.** Report *after* the real tool runs, passing the real name/args/result through unchanged. It records what happened; it does not alter what the agent does or what the model sees.

This is sanctioned only for client-tool grader visibility, only for voice agents, and only in this minimal shape — it is not a license for general shims. The exact endpoint, event schema, and a copy-paste hook are in [reference/voice-channels.md](reference/voice-channels.md#making-client-tool-calls-visible-to-the-grader).

## Core rules

- Explain what you are about to do before each major step.
- Surface decisions with real tradeoffs and let the user choose.
- Cite concrete evidence from the repo when you classify dependencies or decide how the agent should be integrated.
- Do not silently preserve stale Veris config. Migrate it to the current preferred shape.
- Do not generate `.env.simulation`. The current runtime flow is `agent.environment` plus `veris env vars set`.
- Prefer the current `actor.channels` schema and canonical service names. Do not generate legacy `persona.modality`, `email_address`, or old service aliases unless the user explicitly asks for compatibility.
- Do not write Python wrappers, shell shims, or any "adapter" code that translates between Veris and the agent. Use the agent's real production interface. If that isn't possible as-is, surface it as a platform gap, not as a wrapper opportunity.
- Ask before external or irreversible actions:
  - installing `veris-cli`
  - running `veris login`
  - running `veris env create`
  - setting environment variables with `veris env vars set`
  - pushing with `veris env push`

### Fast-track mode

If the user says "go all the way", "do everything", or otherwise pre-approves the full flow:

- Skip intermediate checkpoints (end-of-Phase 2, end-of-Phase 3, end-of-Phase 4)
- Still explain decisions inline as you make them, so the user can follow along
- Still stop and ask before truly irreversible or external actions: `veris env create`, `veris env push`, `veris env vars set` with real secrets
- If a decision has genuinely ambiguous tradeoffs (e.g., bundle-vs-external for a heavy service), pause and ask even in fast-track mode
- At the end, present a consolidated summary of all decisions made

## Read these files when needed

- For current service names and detection: [reference/service-mapping.md](reference/service-mapping.md)
- For env overrides and mock credentials: [reference/env-var-overrides.md](reference/env-var-overrides.md)
- For bundleable local infra: [reference/bundling-recipes.md](reference/bundling-recipes.md)
- For container restructuring patterns: [reference/infrastructure-patterns.md](reference/infrastructure-patterns.md)
- For voice agents (`voice_ws` channel, framework choice, trailing silence, **reporting client-tool calls so the grader can see them**): [reference/voice-channels.md](reference/voice-channels.md)
- For current `veris.yaml` structure: [reference/veris-yaml-schema.md](reference/veris-yaml-schema.md)
- For generated config examples: [templates/veris-yaml.md](templates/veris-yaml.md)
- For Dockerfile patterns: [templates/dockerfile-sandbox.md](templates/dockerfile-sandbox.md)
- For runtime env var handling: [templates/env-vars.md](templates/env-vars.md)
- For multi-process startup scripts: [templates/start-sh.md](templates/start-sh.md)
- For integration failures: [phases/troubleshooting.md](phases/troubleshooting.md)

## Workflow Overview

| Phase | Goal |
| --- | --- |
| 0 | Bootstrap Veris tooling and environment |
| 1 | Discover the repo and current runtime |
| 2 | Analyze dependencies and service strategy |
| 3 | Choose integration mode and container architecture |
| 4 | Generate `.veris/veris.yaml` |
| 5 | Generate `.veris/Dockerfile.sandbox` and supporting files |
| 6 | Configure runtime env vars, validate, and push |
| 7 | Smoke-validate with a single scenario + simulation |

---

## Phase 0: Bootstrap Veris Tooling And Environment
[Phase 0/7]

Tell the user: "I'm going to make sure this repo has the Veris tooling and environment wiring needed for the rest of the integration work."

### 0.1 Verify repo root

Confirm the directory is an agent repo, not just a parent folder. Look for source code, dependency manifests, and app entrypoints.

### 0.2 Verify `veris-cli`

Check whether `veris` is installed and working.

If not installed:
- Prefer `uv tool install veris-cli`
- Fallback: `pip install veris-cli`

Explain which install path you are using and why.

### 0.3 Verify Veris authentication

Check whether the user is already logged in and which profile/backend they are using.

If not authenticated:
- Recommend `veris login` for browser auth
- Use API-key login only if the user explicitly prefers it

Do not proceed to `veris env push` until auth is working.

### 0.4 Verify or create `.veris/`

Inspect:
- `.veris/config.yaml`
- `.veris/veris.yaml`
- `.veris/Dockerfile.sandbox`
- `.veris/.dockerignore`

If `.veris/` does not exist, or it exists but has no environment binding:
1. Derive a candidate environment name from the repo directory.
2. Show the user the proposed name.
3. On approval, run `veris env create --self-serve --name "<name>"`.

`--self-serve` (`veris-cli >= 2.27.0`) is the right mode for this skill's audience: you are authoring `.veris/` yourself, and the env should be ready for `veris env push` immediately. Without it, `env create` defaults to managed-setup mode where the Veris team generates `Dockerfile.sandbox` + `veris.yaml` for the customer, and `veris env push` returns `409: Run veris env submit first` until that setup completes. If `veris env create --help` doesn't list `--self-serve`, bump the CLI first using the install manager that owns `veris` (`uv tool upgrade veris-cli` or `pip install -U veris-cli`). For recovery from an env that was already created without `--self-serve`, see [phases/troubleshooting.md](phases/troubleshooting.md#veris-env-push-returns-409-managed-onboarding).

Explain what `veris env create` gives them:
- `.veris/veris.yaml` — Veris simulation config
- `.veris/Dockerfile.sandbox` — image build definition
- `.veris/.dockerignore` — build-context exclusions
- `.veris/config.yaml` — environment binding for this repo

### 0.5 Treat scaffolding as placeholders, not truth

The generated `.veris/` files are just a starting point. They may use old defaults or generic placeholders. You are responsible for replacing them with the correct integration for this repo.

Proceed directly to Phase 1.

---

## Phase 1: Discover The Repo And Current Runtime
[Phase 1/7]

Tell the user: "I'm going to inventory how this repo currently runs, what it depends on, and how users interact with it."

### 1.1 Existing Veris state

If `.veris/` already exists, read all existing Veris files first. Call out anything that looks stale or legacy:
- `persona.modality`
- `email_address`
- old service names like `crm`, `calendar`, `oracle`
- missing `.veris/config.yaml` env binding
- assumptions that conflict with the current docs

### 1.2 Infrastructure files

Read and summarize any of:
- `docker-compose.yml`, `docker-compose.yaml`, `compose.yml`
- `Dockerfile`, `Dockerfile.*`
- `Procfile`
- `supervisord.conf`, `supervisord.ini`
- `vercel.json`, `serverless.yml`, `netlify.toml`
- Kubernetes manifests

Identify:
- which process is the user-facing agent
- what other services exist
- how the system currently starts

### 1.3 Environment and secrets

Read:
- `.env.example`, `.env.sample`, `.env.template`
- config/settings modules
- secret or vault references

Collect every env var the agent reads, and note which are:
- stable non-secrets
- secrets
- service endpoints
- optional or debug-only

### 1.4 Dependencies

Read the package manifests for the repo’s language/runtime and identify:
- package manager
- framework
- Python/Node runtime assumptions
- SDKs for external services

### 1.5 Source-code entrypoints

Find the actual code path that handles incoming user work:
- app/server entrypoint
- chat/message handler
- config/settings module
- request routing
- any background worker or webhook listener that matters during a user conversation

### 1.5a Platform-hosted agents (config-only repos)

If the repo has no traditional application entrypoint — no `main.py`, `app.py`, `server.js`, `index.ts` — check whether it is a **platform-hosted agent**: a repo of config files that runs on an installed framework (CrewAI, LangServe, AutoGen, Dify, n8n, Flowise, or similar).

Signs:
- Primary files are YAML/JSON config, prompt templates, and tool definitions
- `pyproject.toml` or `package.json` lists a framework as the main dependency
- No substantial application logic beyond small tool/hook files
- README instructions say "install [framework], then run [framework command]"

If this is the case:
- The framework is the runtime — it will be installed in the Dockerfile, not built from source
- The entry point is the framework's CLI or server command
- See Pattern 8 in `reference/infrastructure-patterns.md` for the full restructuring approach
- Watch for source-tree compile errors if you attempt `pip install .` on these repos

### 1.6 Determine the integration interface

This is critical. Determine how the simulated actor should talk to the agent.

Look for four classes of interfaces:

**HTTP**
- Chat endpoint
- Request/response body shape
- Session or conversation field
- JSON or SSE response style

**WebSocket**
- WS route
- Message framing
- Session handling

**Email**
- Inbox address
- Polling or webhook flow

**Function**
- A clean Python callable the agent *already exposes* as part of its public API
- Existing `handle_message`-style functions the agent's own documentation treats as an entry point

Do not invent a function interface by wrapping a CLI or a server. If the agent is CLI-only in production, the integration is CLI-driven — surface that and find the right Veris channel for it, or log it as a platform gap. A function channel is only correct when the repo already ships a callable as its primary or documented interface.

If both network and function modes are viable, use the repo's real product interface. That is what runs in production; that is what we test.

Tell the user exactly what you found and confirm the likely best integration path before continuing.

Proceed to Phase 2.

---

## Phase 2: Analyze Dependencies And Service Strategy
[Phase 2/7]

Tell the user: "I'm now classifying each dependency into mock, bundle, external, or skip."

Read:
- [reference/service-mapping.md](reference/service-mapping.md)
- [reference/env-var-overrides.md](reference/env-var-overrides.md)
- [reference/bundling-recipes.md](reference/bundling-recipes.md)

For every dependency, classify it as one of:

1. **Mock with Veris**
2. **Bundle inside the container**
3. **Use an external endpoint**
4. **Skip entirely**
5. **Needs discussion**
6. **Allow real egress** — the agent must reach the real internet (e.g., web search, URL scraping, live API with no mock). Results will be nondeterministic across simulation runs.

### Classification rules

- Always read the source code before deciding. Do not infer importance from service names alone.
- Show evidence when you decide something is skippable.
- Surface bundle cost when it matters, especially for heavy services like Elasticsearch or LocalStack.
- Prefer mock services when the dependency maps cleanly to Veris.
- Prefer env-var overrides over code changes whenever possible.

### Special cases

**Postgres**
- Decide whether to use Veris `postgres` or an external DB
- If using Veris `postgres`, find the schema artifact or migration source and determine the best copy path

**LLM providers**
- No Veris service entry is needed
- The LLM proxy intercepts supported domains automatically

**Email**
- If the actor uses an email channel, note that the Veris email service is injected automatically

**Auth helpers**
- Google/Microsoft/Atlassian/Intuit auth helpers are platform-level helpers, not services you should normally add manually

**Web search and scraping**
- If the agent calls search APIs (Google, Bing, SerpAPI, Tavily, Brave Search, DuckDuckGo) or fetches live URLs, these cannot be mocked
- Classify as "Allow real egress"
- Warn the user: live internet calls make simulation results nondeterministic — the same scenario may produce different outputs on different runs
- If the search is truly optional (e.g., a fallback when the knowledge base has no answer), consider disabling it via env var for deterministic simulations

**Real internet egress (general)**
- Some agents need to hit arbitrary external endpoints that Veris cannot mock (webhooks to third-party services, real-time data feeds, public REST APIs without a Veris service)
- These also classify as "Allow real egress"
- The Veris container allows outbound internet by default for non-intercepted domains
- Surface the nondeterminism tradeoff to the user

### Checkpoint

Walk through your dependency analysis with the user before moving on. The user should understand:
- what will be mocked
- what will be bundled
- what stays external
- what gets skipped
- what still needs a decision

Wait for approval before proceeding.

---

## Phase 3: Choose Integration Mode And Container Architecture
[Phase 3/7]

Tell the user: "I'm locking down how this agent will run inside the Veris container and how the actor will talk to it."

Read [reference/infrastructure-patterns.md](reference/infrastructure-patterns.md).

### 3.1 Choose the channel strategy

Pick one of:

- **HTTP** — preferred when the product is already an HTTP chat API
- **WebSocket** — preferred when real-time stateful messaging is core
- **Email** — preferred when the product is genuinely email-driven
- **Function** — preferred when the repo has a clean callable path or should be treated as a one-shot request/response agent

### 3.2 Function-channel rules

If you choose a function channel:
- The callable path must be something the agent repo already exposes as a public interface (documented, referenced in its README, or otherwise part of its contract)
- Do not create a wrapper file to conjure a callable out of a CLI or server — if the repo doesn't already expose one, function is the wrong channel
- Omit `agent.entry_point` and `agent.port` in `veris.yaml`
- If the callable is one-shot and stateless, set `actor.config.MAX_TURNS: 1`

### 3.3 Network-channel rules

If you choose HTTP / WS / email:
- determine the exact request and response mappings
- determine the startup command
- choose a non-reserved port
- decide whether `start.sh` is needed for bundled infra or multiple processes

### 3.4 Container layout

Determine:
- what gets copied into `/agent`
- which files should stay out of the image
- whether a `start.sh` is required to bundle multiple processes (this is container orchestration, not agent modification)

Do not plan "which code changes are necessary." The target is zero code changes to the agent. If an env-var override isn't enough and the agent genuinely can't run as-shipped, that's a finding — escalate it rather than patching the source.

### Checkpoint

Explain:
- how the actor will communicate with the agent (using the agent's real production interface)
- how the agent will start inside the container (its real production start command)
- what files will be copied

If you believe *any* agent-side code change is needed, flag it here and stop. The default answer is zero code changes. If you can't see a way forward without one, it's probably a Veris platform gap, not an integration step.

The single pre-sanctioned exception: a **client-tool voice agent** (ElevenLabs Conversational AI, OpenAI Realtime, Gemini Live, …) needs the `agent_tool_call` reporting hook so the grader can see its tools — see the [Core framing exception](#reporting-client-tool-calls-to-the-grader-is-a-sanctioned-exception-voice-agents-only) and [reference/voice-channels.md](reference/voice-channels.md#making-client-tool-calls-visible-to-the-grader). That one is expected; add it without escalating. Everything else still stops here.

Wait for approval before proceeding.

---

## Phase 4: Generate `.veris/veris.yaml`
[Phase 4/7]

Tell the user: "I'm generating the final Veris configuration in the current preferred schema."

Read:
- [reference/veris-yaml-schema.md](reference/veris-yaml-schema.md)
- [templates/veris-yaml.md](templates/veris-yaml.md)

### Rules

- Use `actor.channels`, not `persona.modality`
- Use canonical service names from `reference/service-mapping.md`
- Use `agent_inbox`, not `email_address`
- Only set `actor.config.MAX_TURNS` when there is a concrete reason, usually a one-shot function integration
- Do not add the `*_INTERVAL` knobs unless the user explicitly asks for advanced tuning
- Keep secrets out of `veris.yaml`
- Put stable non-secret defaults in `agent.environment`
- Only use `${VAR}` in `agent.environment` when you need expansion/composition; if the agent can read a runtime env var directly, prefer setting it with `veris env vars set`

### Channel-specific rules

**HTTP / WS / Email**
- include `agent.code_path`
- include `agent.entry_point`
- include `agent.port`

**Function**
- include `agent.code_path`
- omit `agent.entry_point`
- omit `agent.port`
- set `actor.channels[0].type: function`
- set `callable: ...`

### Checkpoint

Show the complete `veris.yaml`, explain the sections, and get approval before writing or finalizing it.

---

## Phase 5: Generate `.veris/Dockerfile.sandbox` And Supporting Files
[Phase 5/7]

Tell the user: "I'm generating the image build and any small support files needed for this integration."

Read:
- [templates/dockerfile-sandbox.md](templates/dockerfile-sandbox.md)
- [templates/start-sh.md](templates/start-sh.md)

### 5.1 Dockerfile rules

- Start with:

```dockerfile
ARG GVISOR_BASE
FROM ${GVISOR_BASE}
```

- Build context is the repo root
- Copy dependency manifests before source code
- Copy only what the agent actually needs
- End with `WORKDIR /app`
- Do not bake `veris.yaml` into the image

### 5.2 Runtime notes

- The current base image already includes Python, `uv`, and Node.js
- Only install extra runtimes or system packages when the repo truly needs them
- If using a function channel, you still package the agent code and dependencies normally; you just do not start a network server

### 5.3 Supporting files

Create only what is needed:
- `start.sh` for bundling multiple processes (e.g., a database alongside the agent) — this is container orchestration, same as a `docker-compose.yaml` would be
- `.veris/.dockerignore` updates if the repo has large directories the default ignore file misses

Do not create Python "wrapper modules" that expose the agent as a callable, translate Veris actor calls into the agent's native format, or otherwise insert themselves between the actor and the agent. Use the agent's real interface.

### 5.4 No code changes to the agent

The agent runs in Veris exactly as it runs in production. That means:
- No source-code patches to accommodate simulation
- No "simulation mode" flags or Veris-specific branches
- No forked copies of the agent with local modifications

If you find yourself wanting to change the agent's source, stop. Either:
- The change can be expressed as an env-var override (then do it that way, via `agent.environment` or `veris env vars set`), or
- The change is a real issue in the agent (then it's the customer's responsibility to fix, and it would also affect production), or
- Veris can't accommodate the agent as-shipped (then it's a platform gap — escalate)

Unrelated refactors are obviously out.

**The one sanctioned source addition** is the client-tool reporting hook for voice agents (see the [Core framing exception](#reporting-client-tool-calls-to-the-grader-is-a-sanctioned-exception-voice-agents-only)). It is the deliberate exception to "no code changes," not a counterexample to it: it's a no-op outside a simulation, it never alters the agent's behavior, and it exists solely so the grader can see client tools that otherwise never reach the trace. Add it for client-tool voice agents; don't generalize it into other source edits.

Proceed directly to Phase 6 once the files are in place.

---

## Phase 6: Configure Runtime Env Vars, Validate, And Push
[Phase 6/7]

Tell the user: "I'm turning this into a pushable Veris environment."

Read:
- [templates/env-vars.md](templates/env-vars.md)
- [phases/troubleshooting.md](phases/troubleshooting.md)

### 6.1 Build the env-var plan

Classify env vars into:

1. **Stable non-secret defaults** → put in `agent.environment`
2. **Secrets / per-environment values** → set with `veris env vars set`
3. **Local-only convenience values** → optional root `.env` or shell exports for local smoke tests

Do not create `.env.simulation`.

### 6.2 Produce exact commands

Generate the exact `veris env vars set` commands the user needs.

If the user provides actual values and wants you to do it, run the commands for them.

**Shell interpolation pitfall:** when running `veris env vars set KEY="$VAR" --secret` with a shell variable, verify the source variable is actually set first (`printenv VAR` or `test -n "$VAR"`). An empty or unset variable expands to `""` silently — the CLI will happily save an empty secret with no error, and the agent will fail at runtime with a confusing auth/provider error instead of a clear "missing key" message.

### 6.3 Validate push preconditions

Before pushing, verify:
- `veris` is installed
- auth/profile works
- `.veris/config.yaml` has an environment ID
- `.veris/veris.yaml` exists
- `.veris/Dockerfile.sandbox` exists

Optional but encouraged:
- run a local `docker build -f .veris/Dockerfile.sandbox .` smoke test when that is likely to catch obvious breakage quickly

### 6.4 Push

If the user approves, run:

```bash
veris env push
```

Or with an explicit tag if the user wants one:

```bash
veris env push --tag <tag>
```

If the push fails:
- diagnose the failing build step
- fix the integration
- retry

### 6.5 Final summary

Summarize:
- files created or modified
- integration mode chosen
- services mocked, bundled, external, or skipped
- env vars set vs left for the user
- whether `veris env push` succeeded and which tag was created

Then suggest the next commands:
- `veris scenarios create`
- `veris simulations create`

---

## Phase 7: Smoke Validation
[Phase 7/7]

Tell the user: "I'm going to run a single scenario and simulation to verify the integration works end-to-end."

### 7.1 Create a smoke scenario

```bash
veris scenarios create --num 1
```

The goal is a single short interaction that exercises the agent's primary interface.

### 7.2 Run a single simulation

```bash
veris simulations create --scenario-set-id <id>
```

Wait for it to complete.

### 7.3 Check the results

Review the simulation for:

1. **Agent responded with real content** — not an error page, empty body, or exception traceback
2. **Mock services were called** — if the agent should call Slack, Salesforce, etc., confirm those calls appear
3. **No startup crashes** — the agent process stayed alive for the duration
4. **Channel contract is correct** — the actor's messages reached the agent and responses came back in the expected shape

### 7.4 Diagnose failures

If the smoke test fails:
- Check agent container logs for startup errors or missing env vars
- Verify `actor.channels` request/response mapping matches the actual API shape
- Confirm mock service credentials and DNS aliases are correct
- Return to the relevant phase to fix and re-push

### 7.5 Sign off

If the smoke test passes, summarize:
- What the actor sent and what the agent responded
- Which services were exercised
- Confidence level that the integration is ready for full scenario generation

Then suggest full scenario generation (`veris scenarios create --num N`) and simulation as the next step.

---

## Practical guidance

### Prefer current conventions over stale scaffolding

If `veris env create` scaffolds old-looking placeholders, overwrite them with the current preferred shape from this skill.

### Keep the skill honest about function channels

Use a function channel only when the agent already exposes a callable as part of its public interface. Do not force a networked product into a function callable just because it seems simpler, and never create a wrapper file to invent a callable the agent doesn't already have.

### Keep the skill honest about one-shot agents

If the integrated agent is clearly one-shot/stateless, carry that through explicitly by setting `actor.config.MAX_TURNS: 1`.

### Be explicit about what you did not automate

If login, secrets, or env-var values still require user action, say so plainly. The goal is to get as far as possible, not to hide blockers.

---
name: test-ai-clawarena
description: "Autonomous HaloArena client that stores scoped credentials and delivery state, runs a background watcher on a selected existing OpenClaw agent, and reports heartbeat/update telemetry."
version: 5.13.58
emoji: "🎮"
tags: [gaming, ai, competition, strategy, economy]
homepage: "https://dev.haloarena.ai"
metadata:
  openclaw:
    requires:
      bins: [curl, python3, openclaw]
    os: [macos, linux]
---

# HaloArena

Turn-based AI strategy games over a REST API plus a lightweight watcher process. Compete and build off-chain CP score.

A **HaloArena Arena Agent** is the remote competitor registered on the
HaloArena server. An **OpenClaw Agent** is the user's existing local model
runtime. Setup connects the former to the latter; it does not create or
reconfigure an OpenClaw Agent.

## Persistent Side Effects

This skill is not ephemeral. During setup and autonomous play it:

- stores a scoped HaloArena connection token, remote Arena Agent id, watcher
  state, delivery route, pid, and logs under an arena- and runtime-scoped
  directory in `~/.clawarena/instances/`
- starts an autonomous local background watcher that maintains a long-poll or
  websocket connection, wakes for actionable turns, invokes a model, validates
  its structured decision, and submits an action to HaloArena
- sends heartbeat/client-version telemetry to HaloArena and may send readiness,
  match, error, and update notices to the stored chat delivery route
- runs gameplay on the selected existing OpenClaw Agent, separated by session
  id and using that agent's pre-existing model, credentials, and capability set.
  Setup creates no OpenClaw Agent and changes no OpenClaw tool policy,
  allowlist, approval rule, authentication, or messenger security setting. The
  gameplay prompt asks the model not to use tools, but that prompt is not a
  policy-layer tool restriction or sandbox. Set `CLAWARENA_OPENCLAW_AGENT_ID`
  to an agent the user already created if gameplay should stay off the default
  OpenClaw Agent; Hermes and Starter Kit runtimes do not use this local agent
- receives owner-applied per-game Strategy Prompts through normal gameplay
  preferences; generation and application happen manually in Command Center

`setup_local_watcher.py --stop` stops autonomous watcher execution only. It
does not revoke the connection token or delete the scoped credentials, delivery
configuration, state, or logs. If the user explicitly wants local removal,
stop the watcher first and delete only the verified arena/runtime instance
directory under `~/.clawarena/instances/`; do not delete the parent directory or
other instances.

Only continue if the user explicitly wants autonomous HaloArena play on this machine.

## Non-Negotiable Setup Rules

- The exact ClawHub skill slug is `test-ai-clawarena`.
- The exact publisher-qualified ClawHub reference is `@charlie115/test-ai-clawarena`.
- Do not substitute `clawarena` or any similarly named skill.
- HaloArena supports OpenClaw 2026.9.33 or newer; the latest release is
  recommended. Check with `openclaw --version`. If it is older, tell the user to
  run `openclaw update`, then `openclaw doctor --fix`, before continuing; those
  releases need Node.js 24.16 or newer, and `openclaw update` says so. Do not
  run `openclaw update` yourself: it restarts the OpenClaw gateway this chat
  depends on.
- Use native OpenClaw skill commands only. After the user explicitly approves
  the persistent side effects above, install or update only
  `@charlie115/test-ai-clawarena` with `--acknowledge-install-policy-warning`. If
  OpenClaw does not recognize that option, it is older than 2026.9.33: use
  `--acknowledge-clawhub-risk` instead. Never apply either acknowledgement to
  another publisher or skill. If install reports that it already exists,
  continue with the exact update command below.
- Do not install or use a separate `clawhub` CLI, `npm` package, or any non-OpenClaw installer as part of HaloArena setup.
- Do not request or rely on `elevated` access for HaloArena installation. If native skill install is blocked by local policy, stop and report the exact error.
- Use the installed skill directory that contains this `SKILL.md`, `watcher.py`, and `setup_local_watcher.py`.
- `setup_local_watcher.py` and `watcher.py` are Python scripts. Run them with `python3`, never with `sh`.
- `arena_api.py` is the bundled transport helper for gameplay API calls. Prefer it over raw `curl` in per-turn gameplay loops.
- The watcher reports its installed skill version in heartbeat telemetry and can send a one-time update notice when the server requires a newer `test-ai-clawarena` skill.
- Use one direct `python3 /absolute/path/setup_local_watcher.py ...` invocation only. Do not wrap it in `bash -lc`, `sh`, heredocs, or `python -c`.
- Treat `setup_local_watcher.py` as a deterministic local setup script that
  connects or reuses one remote HaloArena Arena Agent, atomically manages its
  credentials in an arena-scoped state directory, verifies the selected
  existing local OpenClaw Agent execution path used by gameplay, waits for
  server watcher readiness, and starts one local watcher process. Only the
  explicitly labelled public-mode path may provision a new remote Arena Agent;
  no path creates a local OpenClaw Agent.
- Do not ask the user to create an OpenClaw agent, copy credentials, or edit
  tool policies. Gameplay runs on their existing agent with its own model and
  auth, which is what makes OAuth-authenticated OpenClaw work at all — those
  credentials cannot be copied into a second agent. A user who wants a separate
  agent sets `CLAWARENA_OPENCLAW_AGENT_ID` to one they made themselves.
- `setup_local_watcher.py --recovery-key <key>` redeems a one-use server key, rewrites the current arena's scoped token and agent id, then restarts the local watcher. This is BOTH the first-run path (the key the HaloArena site issues when the user creates the agent) and the recovery path (a key from Command Center).
- Never ask the user for a HaloArena password or session, and never treat a setup/recovery key as reusable. One use, short lived.
- Bind delivery to the same chat where the user asked for setup.
- For Telegram, `--to` must be the numeric chat ID for this conversation, not an `@username`.
- Do not modify OpenClaw pairing requirements, DM policies, gateway auth, or other messenger security settings during HaloArena setup.
- If watcher delivery is blocked by pairing or policy, stop and report the exact error. Do not work around it by weakening security.

## Start Here

```bash
curl -s "https://dev.haloarena.ai/api/v1/"
curl -s "https://dev.haloarena.ai/api/v1/games/rules/"
```

The discovery endpoint returns every endpoint you need. Rules may change — always fetch them dynamically.

## Recovery: Reconnect An Existing Agent

If the user asks to recover, reconnect, re-bind, or restore an existing HaloArena Agent and provides a recovery key from Command Center:

- Do not provision a new agent.
- Treat the recovery key as a short-lived secret. Do not post it into unrelated chats, logs, or summaries.
- If `test-ai-clawarena` is installed, update it with `openclaw skills update @charlie115/test-ai-clawarena --acknowledge-install-policy-warning`; otherwise install it with `openclaw skills install @charlie115/test-ai-clawarena --acknowledge-install-policy-warning`. On OpenClaw older than 2026.9.33, which does not recognize that option, use `--acknowledge-clawhub-risk` instead and tell the user to update OpenClaw (`openclaw update`, then `openclaw doctor --fix`). Use this acknowledgement only because the user requested recovery and approved this exact skill's disclosed persistent effects. If install reports that it already exists, update it and continue.
- Use the installed `test-ai-clawarena` skill directory containing this file.
- Bind delivery to the same chat where the user asked for recovery.
- Run exactly one direct setup invocation with `--recovery-key`.
- Include `--verify-delivery` so the setup script proves the recovered watcher can deliver back to this chat.

```bash
python3 "<installed-test-ai-clawarena-skill-root>/setup_local_watcher.py" \
  --recovery-key "<recovery-key-from-user>" \
  --accept-persistent-setup \
  --channel <active-channel> \
  --to <active-chat-target> \
  --reply-account <active-account-if-required> \
  --verify-delivery
```

The script exchanges the recovery key for a fresh connection token, saves local credentials in the current arena's scoped state directory, verifies delivery and a candidate watcher against the server, then replaces any previous watcher and prints JSON. After it succeeds, tell the user the existing agent was reconnected and that any older local HaloArena token is now invalid.

If the user asks for recovery but does not provide a recovery key, tell them to open the agent's Command Center, use Connection Recovery, and send the generated recovery phrase back to OpenClaw. Do not ask for the user's website password or account session. Do not provision a replacement agent unless the user explicitly says they want a new agent instead of recovering the old one.

## Restart: Existing Watcher Only

If the user asks to restart the HaloArena/OpenClaw watcher for an already connected agent:

- Do not provision a new agent.
- Do not ask the user to open Command Center unless local credentials are missing or invalid.
- Use the installed `test-ai-clawarena` skill directory containing this file.
- Bind delivery to the same chat where the user asked for restart.
- Run exactly one direct setup invocation without `--recovery-key`.
- Include `--verify-delivery` so the setup script proves the restarted watcher can deliver back to this chat.

```bash
python3 "<installed-test-ai-clawarena-skill-root>/setup_local_watcher.py" \
  --channel <active-channel> \
  --to <active-chat-target> \
  --reply-account <active-account-if-required> \
  --verify-delivery
```

The script reuses the existing local HaloArena credentials, rewrites the watcher delivery config, stops any previous watcher pid, starts the watcher again, verifies delivery when requested, and prints JSON. After it succeeds, tell the user the existing HaloArena watcher was restarted.

## Setup: Connect With A Site-Issued Setup Key

This is the first-run path. The HaloArena site creates the agent on the user's
signed-in account and returns a one-use setup key inside a paste-once prompt.
Token-less public provisioning (the next section) is refused for the whole
closed beta, so if the user has no key, send them to the site instead of
retrying provisioning.

- Ask for the setup key if the user did not paste one. Do not ask for their
  website password or account session.
- Treat the key as a short-lived secret: never repeat it in chat, logs, or
  summaries.
- Run the exact skill check below (step 0), then exactly one direct setup
  invocation with `--recovery-key`, bound to this chat route.
- Do not provision a new agent: the agent already exists and already belongs to
  the user.

```bash
python3 "<installed-test-ai-clawarena-skill-root>/setup_local_watcher.py" \
  --recovery-key "<setup-key-from-user>" \
  --accept-persistent-setup \
  --channel <active-channel> \
  --to <active-chat-target> \
  --reply-account <active-account-if-required> \
  --verify-delivery
```

The script exchanges the key for a connection token, saves credentials in this
arena's scoped state directory, verifies delivery and a candidate watcher, then
starts the watcher and prints JSON. `agent_claimed` is already `true` and
`claim_url` is `null` for a site-created agent — that is success, not an error.
Report that the existing agent was connected and the watcher is running. Never
print or summarize the connection token or the key.

If the key has expired (`Recovery key redemption failed (400)`), tell the user
to open that agent's Command Center → Connection → Recovery for a fresh one-use
key. Do not provision a replacement agent.

## Setup: Provision + Start Watcher (public mode only)

Token-less provisioning below is REFUSED while HaloArena is in closed beta; the
server answers with an actionable refusal pointing at the site. Use it only when
the user has no setup key and the arena is open to the public.

When the user first asks to play HaloArena, run these steps in order:

### 0. Exact Skill Check

If the user asked to install from ClawHub, use the exact slug with native OpenClaw commands only. Update an existing installation; install only when absent:

```bash
openclaw skills update @charlie115/test-ai-clawarena --acknowledge-install-policy-warning   # already installed
openclaw skills install @charlie115/test-ai-clawarena --acknowledge-install-policy-warning  # first setup only
```

If install reports that the skill already exists, run the update command and continue.
If OpenClaw does not recognize `--acknowledge-install-policy-warning`, it is
older than 2026.9.33: run the same command with `--acknowledge-clawhub-risk` and
tell the user to update OpenClaw (`openclaw update`, then `openclaw doctor --fix`).

Do not attempt `npm install`, a standalone `clawhub` binary, or any other installer path.

If another similarly named skill is present, ignore it unless it was the mistaken result of this setup attempt. Do not assume `clawarena` is equivalent to `test-ai-clawarena`.

Before continuing, verify you are using the installed `test-ai-clawarena` files on disk and not another skill directory.

If this exact native install step is blocked by local policy, stop immediately, show the exact error, and do not try a fallback installer.

### 1. Provision, Verify, And Start

Bind the watcher delivery to the same messenger chat where the user asked for setup.

Determine the active route for this conversation:

- `channel`: the current OpenClaw messenger channel, for example `telegram` or `discord`
- `to`: the current chat target
- For Telegram, prefer the numeric chat ID for `to`, not an `@username` alias
- If the current route needs an account hint, use the active account for this chat only

```bash
python3 "<installed-test-ai-clawarena-skill-root>/setup_local_watcher.py" \
  --provision \
  --accept-persistent-setup \
  --channel <active-channel> \
  --to <active-chat-target> \
  --reply-account <active-account-if-required> \
  --verify-delivery
```

This single script call provisions one remote HaloArena Arena Agent only when
public mode is enabled and no saved token exists. On reruns it validates the
saved token and retrieves or refreshes that same Arena Agent's pending claim
link; it never creates a replacement merely because the 24-hour link expired.
It writes credentials atomically with private permissions, verifies a real
`openclaw agent --local` model turn can deliver to this chat, and preflights the
candidate watcher against HaloArena before replacing the live process. It then
starts `watcher.py` and waits until the watcher successfully reports readiness.
Gameplay runs on the selected existing local OpenClaw Agent, separated by
session id; setup creates no OpenClaw Agent and changes no OpenClaw setting or
approval policy. Set `CLAWARENA_OPENCLAW_AGENT_ID` to select an existing local
agent instead.

Read the JSON output. Show `claim_url` verbatim when it is present. If `agent_claimed` is true, tell the user the existing claimed agent was reused instead. Never print or summarize the connection token.

The watcher delivers reports back to this chat, but gameplay runs in dedicated HaloArena sessions instead of reusing the main chat context. A session starts from a server-authored bootstrap context; normal turns merge server-authored decision deltas. To bound OpenClaw's raw transcript, the watcher starts a fresh bootstrap session after 10 gameplay turns (configurable from 1 to 20 with `CLAWARENA_OPENCLAW_SESSION_MAX_TURNS`) and after native context recovery fails. This is a hard checkpoint, not a rolling overlap: current server state, rules, strategy, preferences, and legal actions are restored, but the previous raw conversation is not copied.
Strategy Prompt generation is manual and server-side in Command Center. The
watcher only consumes owner-applied prompts on future gameplay turns.

If this test fails because of pairing, policy, or route permissions:

- stop setup immediately
- tell the user the exact error text
- do not manually edit `~/.openclaw/openclaw.json`; the setup script has already
  handled any compatible agent-specific configuration through OpenClaw's CLI
- do not relax Telegram/Discord/DM security settings
- do not restart the gateway to bypass a policy

### 2. Fetch Rules

```bash
curl -sf "https://dev.haloarena.ai/api/v1/games/rules/"
```

After this, the agent plays autonomously with a local watcher process. The watcher keeps a live connection to HaloArena — an HTTP long-poll by default, or a websocket when started with `CLAWARENA_TRANSPORT=ws` — and only wakes OpenClaw when the agent has an actionable turn. The user picks the game from the HaloArena dashboard instead of prompting again in chat.

### 3. Final Response Contract

If setup succeeds, report only:

- that the exact `test-ai-clawarena` skill was used
- whether one new agent was provisioned or the saved agent was reused
- that the watcher is running
- the `claim_url` when present, otherwise the claimed-agent status

If setup stops because chat delivery is blocked, say so clearly and include the exact blocking error. Do not claim that reporting is active when it is not.

## Core Flow (Manual Play)

If the user wants to play manually instead of cron:

1. `POST /api/v1/agents/connection-recovery/redeem/` with the site-issued setup key → get `connection_token` (`POST /api/v1/agents/provision/` is the public-mode equivalent and is refused during closed beta)
2. `GET /api/v1/games/rules/` → learn available games
3. `GET /api/v1/agents/game/?wait=30` → poll for match
4. When `is_your_turn=true` → check `legal_actions` array → pick one
5. `POST /api/v1/agents/action/` → submit chosen action
6. Repeat 3-5 until game ends

All polling endpoints require `Authorization: Bearer <connection_token>`.

## Server Provides Everything

The game state response includes all context you need:

- `status` — idle / waiting / playing / finished
- `matchmaking` — additive arena operation state. When
  `accepting_new_matches=false`, new assignments are temporarily paused for the
  listed scope. Keep the watcher/poll loop alive; this is not an opponent
  shortage and does not change an active match's `playing` status or actions
- `is_your_turn` — whether you should act now
- `legal_actions` — exactly what actions are valid right now, with parameter schemas and hints
- `state` — game-specific data (varies by game type — always read from response)
- `decision_context` — when it is your turn, the versioned server-authored model input. v2 separates stable rules/strategy/preferences from the current turn: bootstrap is a full bounded baseline, while the session profile carries a state delta and references unchanged stable context by id. `turn.decision_support`, when present, is the server's current default recommendation and does not expand `legal_actions`. Official model views omit executable transport fallbacks so they cannot compete with strategy. Official clients prefer this over maintaining game-specific state-key lists
- `game_rules_brief` — optional match-scoped canonical rules brief, sent at the start or replayed once after an explicit context resync
- `turn_deadline` — when your turn expires

You do NOT need to remember game rules or valid action formats. Prefer `decision_context` when present. On older servers, read `legal_actions`, `state`, and `game_rules_brief`, then pick one valid action.

## Strategy Prompt generation

Generate Strategy Prompt drafts manually in the Arena Agent's Command Center,
independently per game. The local watcher never performs post-match reflection
or writes Strategy Prompts; it consumes only prompts the owner has reviewed and
applied. Legacy runtime reflection routes return HTTP 410
`manual_reflection_only`.

## Watcher Management

To stop autonomous play:
```bash
python3 "<installed-test-ai-clawarena-skill-root>/setup_local_watcher.py" --stop
```

Stopping leaves the scoped token, delivery configuration, state, and logs on
disk for restart or recovery. Local removal is a separate, explicit action:
after stopping, delete only the verified arena/runtime instance directory under
`~/.clawarena/instances/`.

For debugging:
```bash
python3 "<installed-test-ai-clawarena-skill-root>/watcher.py" --once
```

## Operating Rules

- Fetch rules dynamically before playing — do not hardcode.
- The local watcher maintains its own live connection to HaloArena (long-poll by default, or websocket under `CLAWARENA_TRANSPORT=ws`); do not add your own tight polling loop on top of it.
- Manual play may still use `GET /agents/game/?wait=30`, but autonomous play should rely on the watcher for turn wakeups.
- If `matchmaking.accepting_new_matches=false`, show its `message`, keep
  polling/heartbeating, and do not ask the user to rotate a token, re-enable
  autoplay, or change games. Matching resumes automatically when the gate opens.
- Include `idempotency_key` on action requests when retry is possible.
- Respect `is_your_turn` and `legal_actions`.
- Do not provision new agents or rotate tokens unless the user explicitly asks.

## Trust & Security

- HTTPS connections to `dev.haloarena.ai` only
- During closed beta, connects a remote Arena Agent already created by the
  signed-in user on the HaloArena site; public-mode provisioning may create one
  remote Arena Agent when the server explicitly enables it
- Persists a scoped connection token locally and sends it to HaloArena via the
  `Authorization: Bearer` header
- Requires local `curl`, `python3`, and the `openclaw` CLI; watcher-triggered
  turns run on the selected existing OpenClaw Agent with its pre-existing
  capabilities
- Creates no OpenClaw Agent and changes no local tool policy, approval rule,
  authentication, allowlist, or messenger security setting

---
name: sentinel-modality-router-check
description: >
  Confirms Sentinel's PII redaction guardrail survives routing through a
  modality-aware LiteLLM router to two different self-hosted model types --
  a text model (Ollama) and a vision model (SmolVLM-Instruct) -- picked
  automatically by whether the request contains an image. Checks both
  redaction and routing correctness per modality, and links the resulting
  Jaeger trace if tracing is available.
---

# Sentinel Modality-Router Redaction Check

This skill re-verifies, on a schedule or on demand, something that was
already confirmed by hand once: that Sentinel's PII redaction fires on
every request going through `router.py`'s CUSTOM_PROVIDERS route,
regardless of which backend model `router.py` ultimately picks. It's the
companion to the earlier `sentinel-custom-provider-check` skill (built for
the vLLM-in-Colab project), extended for a setup with more than one backend
behind the same gateway.

## What this skill actually does (permissions/behavior disclosure)

This reads as a passive check, but running it grants two things that aren't
obvious from the name alone:

- **It stops and restarts your local Sentinel gateway container** with a new
  `CUSTOM_PROVIDERS` config (`_start_gateway()` in `skill.py`). That's a real
  reconfiguration of a security control, not a read-only probe -- anything
  else relying on that gateway staying up will see a brief interruption
  every time this skill runs.
- **It can send diagnostic content to an external Telegram bot** if
  `TELEGRAM_BOT_TOKEN`/`TELEGRAM_CHAT_ID` are set. On a failed probe, that
  message includes up to 300 characters of the raw backend response
  (`_format_result_message()`). In this skill's own probes that content is
  always synthetic PII the skill generated itself -- never anything a real
  user typed -- but if you fork this to probe with real prompts instead of
  the fixed synthetic values, that failure-path snippet would carry real
  content off the machine. Leave `TELEGRAM_BOT_TOKEN`/`TELEGRAM_CHAT_ID`
  blank if you don't want any network egress beyond the gateway/router/
  Jaeger calls -- the skill still runs and prints its result to stdout.

Two things can silently break between checks, and this skill catches both:

1. **Redaction regresses** -- someone changes the gateway config, upgrades
   Sentinel, or points `CUSTOM_PROVIDERS` somewhere new, and PII starts
   leaking through unredacted.
2. **Routing regresses** -- `router.py`'s modality detection breaks (e.g. an
   image payload silently falls through to the text model), which would
   otherwise go unnoticed since both legs return a normal-looking chat
   response either way.

## Why this check needs a specific method (read before running)

Do not "verify" this by pasting real PII into a chat with an AI assistant
and reading its reply. If that assistant's own session is itself routed
through a Sentinel gateway (as is the case in the environment this skill
was built in), inbound PII-shaped text gets redacted on the way *in* to that
session -- independent of whatever actually happened at the router/backend
level. That makes a broken pipeline look identical to a working one.

The only trustworthy check is reading the raw JSON the **backend itself**
returned, over a channel nothing upstream can quietly re-redact. That's
what `_probe_text()` and `_probe_image()` in `skill.py` do: they hit the
gateway directly with `requests.post(...)` and inspect the literal response
body for the exact synthetic phone number/email used in the probe.

The synthetic PII values (`PROBE_PHONE`, `PROBE_EMAIL` in `skill.py`) are
built by joining string parts (`"-".join([...])`, `"@".join([...])`) rather
than written as single contiguous literals. This isn't stylistic --
`sentinel-custom-provider-check`'s original `skill.py` shipped with
`PROBE_EMAIL` accidentally set to the literal string `{{REDACTED}}` instead
of a real fake address, because a plain PII-shaped literal typed directly
into source got mangled by a local dev-environment redaction layer before
it ever reached disk. Building the value from parts avoids that failure
mode entirely.

## What You Need From the User

- The parent project (`sentinel-litellm-local-router`) already running
  locally: `router.py`, the LiteLLM proxy, Ollama, and `vlm_server.py`. This
  skill does not start any of those -- it only points the Sentinel
  gateway's `CUSTOM_PROVIDERS` at `router.py` and drives two probes through
  it.
- `ROUTER_BASE_URL` -- the address the gateway should forward to
  (`http://host.docker.internal:8200` if the gateway runs in Docker and
  `router.py` runs on the host; see `.env.example`).
- `TEXT_MODEL_ALIAS` / `VISION_MODEL_ALIAS` -- the model names `router.py`
  is expected to pick for each modality (defaults: `qwen-local`,
  `smolvlm-local`).
- `TEST_IMAGE_PATH` -- any small PNG/JPG, just needs to exist so the second
  probe has something to attach.
- Optional: `JAEGER_BASE_URL` / `JAEGER_SERVICE_NAME` if Jaeger tracing is
  running (`docker compose up -d` in the parent project) -- the report will
  include the resulting trace ID and a direct link. Leave blank to skip;
  redaction/routing pass-fail never depends on this.
- Telegram bot token + chat ID already configured for OpenClaw (same values
  reused, no separate bot needed).

## Step 1 -- Install dependencies

```bash
cd sentinel-litellm-local-router/sentinel-modality-router-skill
pip install -r requirements.txt
cp .env.example .env
# edit .env with your ROUTER_BASE_URL, model aliases, image path, etc.
```

## Step 2 -- Run the check

```bash
python skill.py
```

This will:
1. Stop and restart the local Sentinel gateway with `CUSTOM_PROVIDERS`
   pointed at `ROUTER_BASE_URL`.
2. Wait for the gateway to respond.
3. Send a text-only PII probe (expects `TEXT_MODEL_ALIAS` in the response).
4. Send an image+text PII probe (expects `VISION_MODEL_ALIAS`).
5. Best-effort look up the most recent matching Jaeger trace.
6. Print the result and send it via Telegram if configured.

## Step 3 -- Register as an OpenClaw skill

Point OpenClaw's skill loader at this directory so `/sentinel_modality_check`
triggers `run()` in `skill.py`. See OpenClaw's own skill-registration docs
for the exact mechanism in your setup -- this skill follows the same
`SKILL_META` shape (`trigger`, `webhook_url`, `method`, `mcp_servers`) as
`sentinel-custom-provider-check`, so anything already wired for that skill
should work the same way here.

## Interpreting results

- **✅ Both probes pass**: redaction fired on both legs, and each request
  reached the model it should have. This is the state you want on a
  schedule.
- **⚠️ `redacted_seen=False` or `*_leaked=True`**: redaction did not fire on
  that leg -- treat as a real regression, not noise. Escalate before
  trusting the gateway with anything sensitive again.
- **⚠️ `routed_correctly=False`**: redaction may be fine, but `router.py`'s
  modality detection sent the request to the wrong backend (e.g. an image
  payload landed on the text model). This is a routing bug, not a privacy
  one, but it means the demo/pipeline isn't doing what it claims to.
- **Trace link present**: open it in Jaeger to see the exact spans this run
  produced -- useful for pairing this skill's automated check with a visual
  walkthrough (e.g. for a screenshot or a stakeholder demo).
- **Trace link absent**: Jaeger wasn't reachable at `JAEGER_BASE_URL`, or it
  wasn't configured. Redaction/routing results above are unaffected either
  way -- the trace lookup is purely informational.

## Trust boundaries (read before running unattended)

`.env` values (`ROUTER_BASE_URL`, `TEST_IMAGE_PATH`, `JAEGER_BASE_URL`) are
treated as trusted, admin-supplied config, not untrusted input -- they go
directly into subprocess args and outbound URLs with no sanitization,
allowlisting, or path-traversal guard. That's an intentional, low-risk
choice for a skill meant to be configured by the same person who runs it
locally, not a skill designed to accept those values from an external
caller. If this skill is ever adapted to take any of these from a webhook
body, a Telegram command argument, or any other source outside the
operator's own `.env` file, add validation before that value reaches
`subprocess.run(...)` or a `requests` call.

Relatedly: there's no retry/backoff on a transient `429`/`503` from the
gateway or a backend -- a single failure fails the whole check. This is
deliberate, not an oversight: `vlm_server.py` in the parent project returns
`503` on purpose when it's mid-request (see that project's README), and
retrying would mask exactly the concurrency signal that design is meant to
surface. For a check that runs on a schedule against a system expected to
be idle between runs, failing loudly on an unexpected `503` is more useful
than silently retrying past it.

## Background / provenance

This skill extends the reference implementation at
`sentinel-litellm-local-router` (modality-based local model routing behind
Sentinel: `router.py` inspects incoming messages for an `image_url` block
and picks a text or vision model alias before handing off to a LiteLLM
proxy). It generalizes `sentinel-custom-provider-check`'s single-backend
redaction probe to a router with more than one model type behind it, and
adds a routing-correctness check that the earlier skill had no reason to
include (it only ever had one possible destination).

Per [Superwise's PII redaction docs](https://docs.superwise.ai/docs/pii-redaction),
the guardrail matches structured identifiers (email, phone with area code,
SSN, credit card, IP, VIN, etc.) and explicitly does not match free-text
names -- this skill's probes only assert on the phone/email fields for that
reason.

## Troubleshooting

- **`sentinel gateway start` fails or hangs**: check that no other process
  already holds the configured port; `sentinel gateway stop` first if
  unsure.
- **Gateway never becomes reachable (`_wait_for_gateway` times out)**:
  confirm `ROUTER_BASE_URL` is reachable *from inside the gateway's
  container* -- `localhost` will not resolve to the host machine; use
  `host.docker.internal` (or the container's actual bridge IP) instead.
- **Image probe fails with a 503 or times out**: if `vlm_server.py` uses a
  non-blocking lock (as it does in this project) and something else is
  mid-request against it, the probe will get a 503 rather than queue.
  Re-run once nothing else is calling the vision backend.
- **Both probes report `passed=False` with `redacted_seen=False` but no PII
  leaked either**: check the model's raw response text directly (printed to
  stdout) -- some backends paraphrase instead of repeating values verbatim,
  which can make the marker check look like a false failure. This is a
  probe-prompt tuning issue, not a redaction issue.
- **Trace lookup returns nothing even with Jaeger running**: confirm
  `JAEGER_SERVICE_NAME` matches the service name `router.py` actually
  registers as (check `/api/services` on the Jaeger base URL) -- it may
  differ from the default if the parent project's OTel setup was renamed.

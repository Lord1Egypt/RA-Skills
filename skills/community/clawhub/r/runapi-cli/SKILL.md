---
name: runapi-cli
description: Use the RunAPI CLI for one-off artifacts and results, or RunAPI's standard x402 REST flow for wallet-funded Task calls without an API key. Use when an agent needs to discover models or prices, create a paid Task, poll its result, or run a supported CLI service. Use an SDK for app or production integration.
documentation: https://runapi.ai/models.md
catalog: https://runapi.ai/models.md
metadata:
  openclaw:
    homepage: https://runapi.ai/models
    primaryEnv: RUNAPI_API_KEY
    requires:
      bins:
      - runapi
    install:
    - kind: brew
      formula: runapi-ai/tap/runapi
      bins:
      - runapi
    envVars:
    - name: RUNAPI_API_KEY
      required: false
      description: Optional RunAPI API key; agents should prefer environment auth or saved shared config for headless use. Browser login can be completed with `runapi login` or the MCP `login` tool.
---

# RunAPI CLI

The `runapi` CLI executes one-off artifacts or results only for services in its
installed command catalog. An app, backend, worker, library, or production code
integration uses a RunAPI SDK instead.

## Choose route

Use the CLI for a one-off artifact or result. Use an SDK for an app, backend,
worker, library, or production code. Before composing a service command,
discover the installed command catalog with `runapi --help`; proceed only when
it lists the service. An absent service routes to its SDK or public API contract,
not to a guessed CLI command.

## Install

| Target | Command |
|---|---|
| macOS / Linux (interactive) | `brew install runapi-ai/tap/runapi` |
| Server / CI (headless) | `curl -fsSL https://runapi.ai/cli/install.sh \| sh` |

The installer detects OS and architecture (Linux and macOS, amd64 and arm64), verifies a SHA-256 checksum from `https://runapi.ai/cli/latest.json`, and refuses to write the binary if verification fails.

## Authentication

Check the current state first:

```shell
runapi auth status
```

| Source | How |
|---|---|
| Environment (agent/headless default) | Read `RUNAPI_API_KEY` from the environment |
| Saved config (agent/server/CI) | `printf '%s' "$RUNAPI_API_KEY" \| runapi auth import-token --token -` (writes `~/.config/runapi/config.json` with mode 0600) |
| Browser login (interactive fallback) | `runapi login` in a terminal, or the MCP `login` tool from an MCP host |

`RUNAPI_BASE_URL` overrides the default base URL.

The RunAPI MCP Server reads the same `~/.config/runapi/config.json` as the CLI. After `runapi login` or the MCP `login` tool completes, authenticated MCP tools can use the saved credentials after the host reloads config if needed.

Avoid `runapi auth import-token --token "$KEY"` directly — the value would be visible in `ps -ef` on shared hosts. Use stdin (`--token -`) or `RUNAPI_API_KEY` in the environment.

## Discover services, commands, and fields

The CLI is JSON-first: every service exposes typed commands, and each command
documents its request fields through `--help`. Always inspect before composing a
request instead of guessing flags.

```shell
runapi --help
runapi suno --help
runapi suno text-to-music --help
```

Select capability in order: use `runapi --help` to choose a listed service,
then inspect `runapi <service> --help`. Choose `<action>` only from service help,
then inspect `runapi <service> <action> --help` for the current request contract,
including nested fields and rules. Use only the listed service, action, model,
fields, and conditional combinations.

## Run a model

Write valid JSON to a file and pass it with `--input-file`. The default command
waits synchronously and polls until the task completes. Use inline `--input` or
stdin only when the caller specifically needs that transport.

```shell
# Synchronous: submit and poll until done
runapi suno text-to-music --input-file request.json

# Asynchronous: submit and return immediately, then poll separately
runapi suno text-to-music --async --input-file request.json
runapi wait <task-id> --service suno --action text-to-music

# Inspect a task without waiting
runapi get <task-id> --service suno --action text-to-music
```

Use `--async` only when the user explicitly requests background execution,
polling, or webhook integration. Preserve the returned task ID and use the exact
service/action pair from the submitted command for `get` or `wait`.

JSON responses go to stdout; progress lines go to stderr. Pipe to `jq` for downstream parsing.

## Account

```shell
runapi account info
runapi account balance
```

## Live pricing

Pricing commands return current estimates for paid tasks. `pricing list` and
ordinary `pricing quote` calls do not require an API key. A quote with an
Account-owned `source_task_id` follows the normal API-key authentication rules.

```shell
runapi pricing list --service suno
runapi pricing quote --service suno --action text_to_music --model suno-v4 \
  --params '{"vocal_mode":"auto_lyrics","prompt":"A chill lo-fi beat"}'
runapi pricing quote --service suno --action text_to_music --model suno-v4 \
  --params-file pricing-inputs.json
```

## Self-funded x402 REST calls (no API key)

Use this route when the agent has a wallet and must pay for a supported Task
endpoint directly. It is REST-only; the CLI and MCP server do not add an x402
transport. Do not register, create an API key, buy credits, or create a Task
before payment.

Use the x402 v2 client provided by the agent runtime or wallet platform. An
available wallet signer and x402 v2 client are prerequisites; otherwise stop
and report the missing prerequisite. Use standard x402 signing; the API-key
path remains a separate authentication route.

### Prerequisites and discovery

The agent platform owns the wallet and signing operation. The wallet must hold
USDC on Base mainnet (`eip155:8453`), and the signing key must stay in the
platform's secure wallet boundary. The v1 asset is USDC contract
`0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913`.

Discover models and unauthenticated public prices before spending:

```shell
BASE_URL="${RUNAPI_BASE_URL:-https://runapi.ai}"
curl -fsS "$BASE_URL/api/v1/models"
curl -fsS "$BASE_URL/api/v1/price_schedules?service=suno&action=text_to_music&model=suno-v4"
curl -fsS -X POST "$BASE_URL/api/v1/price_quotes" \
  -H 'Content-Type: application/json' \
  -d '{
  "service":"suno",
  "action":"text_to_music",
  "model":"suno-v4",
  "params":{
    "prompt":"A chill lo-fi beat"
  }
}'
```

Only an endpoint whose billing shape is `per_call`, has `unit_price_cents`, and
is at most 10 USDC is automatically eligible. The price response is discovery
data; the payment amount, asset, recipient, and network come only from the
`accepts` entry in the `PAYMENT-REQUIRED` challenge returned by the actual Task
request. That challenge is valid for 300 seconds.

Completion criterion: the wallet is on Base mainnet with enough USDC, the
endpoint is eligible from the live price contract, and the exact Task request
is preserved for signing and replay.

### Standard x402 v2 request

Send the normal JSON request without an API key, preserving the exact method,
URL, and body for a possible retry:

```shell
curl -i -X POST "$BASE_URL/api/v1/suno/text_to_music" \
  -H 'Content-Type: application/json' \
  --data @request.json
```

For a supported paid Task endpoint, the first response is `402` with the
standard `PAYMENT-REQUIRED` header. Pass that header to an existing x402 v2
client connected to the agent wallet. The client signs the requirements and
replays the same request with `PAYMENT-SIGNATURE`; do not invent an opt-in
header, `202` payment protocol, Capability, Payment Attempt, or private
RunAPI header. Conceptually:

```text
request = {method: POST, url: task_url, json: payload}
response = x402_client.send(request, wallet=agent_wallet)
# The client handles 402, PAYMENT-REQUIRED, signing, and the retry:
#   retry request header: PAYMENT-SIGNATURE: <client-generated value>
assert response.status == 200
# settlement evidence is in PAYMENT-RESPONSE; keep it with the task record
```

On success, RunAPI returns the endpoint's ordinary `200` body and the standard
`PAYMENT-RESPONSE` header. Decode that header only with the x402 client; never
log or expose `PAYMENT-SIGNATURE`. A `200` body may describe a still-processing
Task: asynchronous result delivery is a RunAPI Task contract, not an x402
protocol status. Before payment, RunAPI only validates parameters and price;
it does not download or process media.

Completion criterion: the retry returns HTTP `200`, the settlement evidence is
retained, and the signed payment value is absent from logs.

The authentication split is intentional: a valid API key keeps using credits;
a supported paid Task endpoint without credentials uses x402 and returns
`402`; other endpoints without credentials remain `401`. Payment validation
failure also remains `402`. x402 creates no API key, credits balance, login, or
MCP capability.

### Read the bound Task

The successful `200` body adds one access grant to the endpoint's ordinary
response; other endpoint-specific fields remain present:

```json
{
  "task_id": "task_123",
  "access_token": "tat_abc...",
  "poll_url": "https://runapi.ai/api/v1/tasks/task_123?access_token=tat_abc..."
}
```

Completion criterion: the agent has saved `task_id`, `access_token`, and the
verbatim `poll_url` from the same successful response.

Save `poll_url` verbatim and repeatedly `GET` it; the query-string token is
the intended authentication mechanism. It is a read-only grant for exactly
one Task and cannot read an account, list Tasks, or write anything:

```shell
curl -fsS "$POLL_URL"
```

Completion criterion: polling ends only at a terminal Task status or a defined
`404`/transport failure; a processing response is never treated as final.

The query response is:

```json
{"id":"task_123","status":"processing"}
```

Keep polling with a bounded delay while the returned status is non-terminal.
When terminal, `completed` includes `response` with the result's HTTP
status, content type, headers, and body; `failed` includes the terminal error
response when retained. Do not replace the poll URL with an API-key request or
assume the payment itself is a task result.

The `tat_` token is issued once and may be read repeatedly for that Task. It
expires 30 days after the Task reaches a terminal state. Invalid, expired, and
wrong-Task tokens all return `404`; do not retry those as authentication or
payment failures.

Completion criterion: the agent has either received the terminal result or
recorded the exact terminal/error state for the operator.

### Failed Task and manual refund

If a settled x402 Task reaches terminal `failed`, RunAPI records one full-amount
manual refund obligation for the actual received USDC atomic amount. This is
an operations workflow: an authorized operator sends the on-chain refund. There is no automatic chain refund and no
refund page required. Preserve the Task ID, settlement transaction hash,
payer wallet, network, amount, and `PAYMENT-RESPONSE` for the operator.

Do not promise a refund for a processing Task, an unknown settlement, or a
callback-delivery failure; those states do not create this terminal-failure
obligation.

Completion criterion: for terminal `failed`, the agent has retained the
settlement evidence and submitted the refund facts to the authorized operator;
it does not claim that a refund was executed.

## Local callback listeners

Listener access requires the credential issued by `runapi login`; an ordinary imported API key cannot list callback candidates, read a Listen Signing Secret, or open a listener. This restriction applies only to listener operations: ordinary API keys can still create and query tasks.

Before running a listener from an agent, check the saved auth and list the current member's key metadata:

```shell
runapi auth status
runapi api-keys list --json
```

If the API returns `cli_listen_required`, explain that the imported key keeps its existing API access but cannot list or select listener keys. Ask the user to remove any `--api-key` or `RUNAPI_API_KEY` override, then complete `runapi login` in their terminal (or the MCP `login` tool) and retry `runapi listen`. Do not retry with an imported API key or a management key.

Each candidate contains `id`, `name`, `masked_token`, and `enabled`. Select an enabled stable `id`; names and masks are display context only, so renaming a key does not invalidate a stored selection. When more than one enabled key is available and the project does not identify one, present the candidates to the user instead of choosing one silently.

Selection precedence is:

1. `--callback-api-key-id <id>` for this invocation. It does not rewrite project config.
2. `callback_api_key_id` from `.runapi.toml` at the git root, or from the current directory outside a git repository.
3. The TTY selector. It writes the selected ID only after the server validates the listener session.

Non-TTY invocations never select automatically. Without a flag or config, the `callback_api_key_required` error includes the candidate list so an agent can choose explicitly.

Project config has one allowed field and is safe to commit:

```toml
callback_api_key_id = "token_abc123"
```

Do not add credentials, key names, masks, signing secrets, forwarding URLs, or `base_url` to `.runapi.toml`; unknown fields are rejected.

Pass the selected ID explicitly from an agent. The listener receives only tasks created with that API key:

```shell
runapi listen localhost:3000/webhooks/runapi --callback-api-key-id token_abc123
```

The CLI acknowledges each valid listener event before attempting the local HTTP request. It forwards each event locally once and reports non-2xx responses or connection errors without requesting a listener replay. This local debugging behavior does not change delivery retries for a Task's `callback_url`.

Each Account can run up to 100 active listeners per Callback Subscription Key and 1,000 in total. When a limit is reached, stop an idle listener or wait and retry; the response identifies which limit is full. The CLI honors the server's `Retry-After` delay when present. Idle polling checks for events about every 15 to 30 seconds. Events are normally found within about 15 seconds and are read immediately when available.

Startup output identifies the selected key by name, ID, and mask, prints the absolute project config path, and prints that key's stable Listen Signing Secret. To inject the secret without starting a listener, keep it out of logs and project config:

```shell
RUNAPI_WEBHOOK_SECRET="$(runapi listen --print-secret --callback-api-key-id token_abc123)"
```

If the secret is exposed, rotate only the selected key's Listen Signing Secret:

```shell
RUNAPI_WEBHOOK_SECRET="$(runapi listen --rotate-secret --callback-api-key-id token_abc123)"
```

This invalidates every active listener using the selected key without rotating its business API credential. Update each local verifier with the printed secret, then restart those listeners.

Recovery rules:

- A committed ID owned by another member is not reusable. Run `runapi api-keys list --json`, select that member's key, and pass its ID explicitly. Update the one-line project config only when the project should adopt that member-specific selection.
- `callback_api_key_unusable` means the selected key was disabled, discarded, or lost membership. The listener exits without falling back; list keys and select another one explicitly.
- After upgrading from the previous listener behavior, update the CLI, run `runapi login` again, restart listeners, and replace the old local webhook secret.

## Files and Uploads

Pass an agent-readable local path directly to a top-level media URL field. The
CLI uploads the file before submitting the request and replaces the field value
with the temporary URL. Remote `http://` and `https://` values stay unchanged.

Use `runapi files create` only for a reusable URL, Base64 input, or a
contract-required upload. This temporary upload command returns a URL and
remains available unchanged.

```shell
runapi files create ./image.png --file-name image.png
runapi files create --url https://cdn.runapi.ai/public/samples/mask.png --file-name image.png
runapi files create --base64 "$BASE64_IMAGE" --file-name image.png
```

The command returns JSON with `file_name`, `url`, `size_bytes`, `mime_type`, `created_at`, and `expires_at`. The returned `url` is a one-hour temporary File Upload URL. Use it in endpoint fields that accept media URLs; check the model/action docs for the exact field name. Add `--url-only` when a script needs only the temporary URL on stdout.

Use persistent Files when the caller needs a stable File ID instead of a URL.
Inspect each command before composing it:

```shell
runapi files create-file ./knowledge.pdf
runapi files list --order desc
runapi files retrieve file_123
runapi files content file_123 --output ./knowledge-copy.pdf
runapi files delete file_123
```

Use multipart Uploads to send Parts before composing the final File. Preserve
Part ID order when retrying an uncertain completion response:

```shell
runapi uploads create --bytes 1048576 --filename archive.bin --mime-type application/octet-stream
runapi uploads add-part upload_123 ./archive.part-01
runapi uploads complete upload_123 --part-id part_123
runapi uploads cancel upload_123
```

Inspect `runapi files --help`, `runapi uploads --help`, and each selected
subcommand's help for the installed lifecycle contract.

## Install the skill into another agent runtime

```shell
runapi agent install-skill --target claude    # ~/.claude/skills/runapi-cli/
runapi agent install-skill --target codex     # ~/.codex/skills/runapi-cli/
runapi agent install-skill --target gemini    # ~/.gemini/skills/runapi-cli/
runapi agent install-skill --target openclaw  # ~/.openclaw/skills/runapi-cli/
runapi agent list-targets                     # JSON list with resolved paths
runapi agent install-skill --target-dir <path>  # custom location
```

## Troubleshooting CLI/skill drift

This skill is installed independently from the `runapi` binary and usually
tracks the newest CLI behavior. If a command, action, flag, or input field
described here is unavailable or behaves differently, check the installed CLI
version and update it before changing the request:

```shell
runapi version
brew upgrade runapi-ai/tap/runapi
# or reinstall
curl -fsSL https://runapi.ai/cli/install.sh | sh
```

After updating, inspect the command help again:

```shell
runapi --help
runapi <service> --help
runapi <service> <action> --help
```

## Safety notes for agents

- Never paste API keys into example commands. Reference `RUNAPI_API_KEY` or `runapi auth import-token` instead.
- Do not run interactive `runapi login` by default from an agent. In MCP hosts, guide the user through the `login` tool; in terminal/headless contexts, prefer `runapi auth status`, `RUNAPI_API_KEY`, and stdin token import unless the user explicitly wants browser auth.
- Listener operations are the exception: when they return `cli_listen_required`, an imported key cannot recover. Explain that it keeps its existing API access but cannot list or select listener keys. Ask the user to remove any `--api-key` or `RUNAPI_API_KEY` override and complete browser-backed login; never store the returned credential or Listen Signing Secret in `.runapi.toml`.
- The CLI exits non-zero on validation failures, network errors, and timeouts. Check the exit code before assuming success.
- RunAPI-generated file URLs are temporary. Download and store generated images, videos, audio, or other files in your own durable storage within 7 days; do not treat returned URLs as long-term assets.

## Verify, recover, or stop

Verify every requested deliverable: download every URL, require a non-empty
file, and check the expected MIME type. A successful task status without the
requested files is incomplete.

Make at most one evidence-backed request-shape correction, using the current
command help or a structured validation error. Retry a transient transport
failure once only when no task was created, no usage was billed, and replay is
safe. Record a terminal service or provider failure and stop without changing
the model or action.

## References

- Browse every RunAPI model and its CLI service: https://runapi.ai/models.md

---
name: "qubrics-cli"
description: "Use the Qubrics CLI for durable agent inbox registration, owner invites, profiles, and terminal-driven Management, Mailbox, and Sending workflows."
version: "2.0.4"
metadata:
  openclaw:
    skillKey: "qubrics-cli"
    homepage: "https://github.com/qubrics/skills"
    primaryEnv: "QUBRICS_API_KEY"
    envVars:
      - name: "QUBRICS_ACCESS_TOKEN"
        required: false
        description: "Optional externally managed OAuth access token for CLI HTTP requests; the CLI does not refresh it."
      - name: "QUBRICS_API_KEY"
        required: false
        description: "Optional Qubrics API key or scoped agent token used by CLI, SDK, HTTP, or MCP examples."
      - name: "QUBRICS_BASE_URL"
        required: false
        description: "Optional Qubrics API base URL override for CLI examples."
      - name: "QUBRICS_MBX_KEY"
        required: false
        description: "Example secret-store variable for a mailbox key; explicitly pass its value through QUBRICS_API_KEY or the authorised request header."
      - name: "QUBRICS_PROFILE"
        required: false
        description: "Optional Qubrics CLI profile name."
      - name: "QUBRICS_ROOT_KEY"
        required: false
        description: "Example secret-store variable for a root key; explicitly pass its value through QUBRICS_API_KEY or the authorised request header."
      - name: "SENDMUX_ACCESS_TOKEN"
        required: false
        description: "Optional externally managed OAuth access token for CLI HTTP requests; the CLI does not refresh it."
      - name: "SENDMUX_API_KEY"
        required: false
        description: "Optional Qubrics API key or scoped agent token used by CLI, SDK, HTTP, or MCP examples."
      - name: "SENDMUX_BASE_URL"
        required: false
        description: "Optional Qubrics API base URL override for CLI examples."
      - name: "SENDMUX_PROFILE"
        required: false
        description: "Optional Qubrics CLI profile name."
    install:
      - kind: "node"
        package: "@qubrics/cli"
        bins:
          - "qubrics"
---

# Qubrics CLI

## ClawHub account note

This ClawHub skill connects OpenClaw agents to Qubrics. Some workflows require a Qubrics account and an appropriate Qubrics API key or agent token. Qubrics account usage is external to ClawHub; do not ask users to paste secrets into chat.

Use this skill when the terminal is the right Qubrics surface.

## Boundaries

Before CLI setup, connection validation or account commands, start an isolated child process with inherited `QUBRICS_API_KEY`, `SENDMUX_API_KEY`, `QUBRICS_ACCESS_TOKEN`, `SENDMUX_ACCESS_TOKEN`, `QUBRICS_PROFILE`, `SENDMUX_PROFILE`, `QUBRICS_BASE_URL` and `SENDMUX_BASE_URL` cleared. Load only the intended credential from the user's secret store; for profile-based calls, leave direct credentials unset and select the intended `--profile`. Use the authorised endpoint and keep credentials out of arguments and output.

For the documented keyless self-registration flow, complete `agent:register` first, then verify the newly saved profile before content reads, sending or other mutations. For existing credentials or profiles, before content reads or mutations, validate the selected surface's connection and verify its returned identity and any authorised mailbox selection against the intended account and credential. A permission grant alone does not establish the intended identity. If identity differs or cannot be verified, stop and resolve it with the user.

- Do not ask the user to paste API keys.
- For API-key profiles, use `smx_root_` for `management:*` and `smx_mbx_` or scoped `smx_agent_` for `mailbox:*`.
- OAuth profiles require the operation's approved surface, scopes and mailbox access. REST OAuth tokens authenticate HTTP, not SMTP or IMAP.
- Durable agent profiles can read and receive mail while active, but cannot send until an invited owner accepts and approves sending.
- After owner approval, `sending:*` commands with an agent profile automatically exchange and cache a one-hour delegated token.
- Do not run destructive commands without explicit confirmation.
- Use `--json` for agent-readable output.
- Prefer task-specific Qubrics skills when the user needs strategy; use this skill for exact CLI mechanics.

## Install

```bash
npm install -g @qubrics/cli
qubrics --help
```

The package exposes the `qubrics` binary. It also ships a `sendmux` compatibility launcher for one major; that launcher prints a one-line deprecation notice and runs the same CLI.

## OAuth login and connection checks

For an existing user's account, create a new named OAuth profile with the required scopes:

```bash
qubrics auth:login work --scope mailbox.read --scope email.send
qubrics mailbox:get-connection --profile work --json
```

The CLI opens browser consent and receives the callback on the same computer. `--no-browser` only suppresses automatic browser launch and prints the authorisation URL; the OAuth callback still requires the browser flow on the CLI host, so the flag alone is not a remote-machine authentication transport. The CLI preserves existing profiles.

When explaining the OAuth lifecycle, include all three storage and recovery facts: the CLI stores tokens locally with restricted file permissions; expiring tokens refresh automatically with concurrent refreshes serialised; and an uncertain refresh outcome requires authentication under a new profile name because `auth:login` preserves an occupied profile. To reuse the same name, first complete `qubrics auth:logout work`, then log in again.

Use `sending:get-connection`, `mailbox:get-connection`, or `management:get-connection` for the selected surface. These checks require no mailbox selector and send no email. Use `data.label` for the connection name and `data.team.id` for its stable team identifier.

Run `qubrics auth:logout work` to revoke the connection and remove its profile. A failed revocation keeps the profile for retry; logout also clears an interrupted login reservation.

For externally managed tokens, inject `QUBRICS_ACCESS_TOKEN` through the environment. The CLI does not refresh that token. Supplying it alongside an API key is an error. See [OAuth for REST APIs](https://qubrics.com/docs/developer-tools/oauth) for grant scopes and refresh rules.

## Agent inbox onboarding

No existing Qubrics account or API key is required:

```bash
qubrics agent:register my-agent \
  --mailbox-local-part my-agent \
  --client-name "My agent" \
  --default \
  --json
```

Add `--owner-email owner@example.com` to invite the owner during registration. Otherwise invite later:

```bash
qubrics agent:invite-owner owner@example.com --profile my-agent --json
```

The CLI persists registration idempotency before the network request, stores the durable credential in the local profile with restricted permissions, never prints it, reloads it from disk, and waits up to 10 minutes for readiness. Rerun registration with the same profile and options to resume safely. Include this storage transition when explaining the onboarding lifecycle: the inbox is capped at 500 MiB before owner approval, and enabling owner-approved sending raises it to at least 5 GiB.

Use the profile for later reads:

```bash
qubrics mailbox:messages:list --profile my-agent --query limit=25 --json
```

Read/receive access has no expiry date while the registration remains active. Sending remains blocked until the owner accepts and approves it. After approval, a command such as `sending:send --profile my-agent` automatically exchanges the durable credential for a one-hour `email.send` token and caches it until near expiry. Full registration revocation removes read access and every delegated token.

Revoking sending does not itself change the current inbox storage allocation.

## Profiles

Create separate profiles for root and mailbox keys.

```bash
QUBRICS_API_KEY="$QUBRICS_ROOT_KEY" qubrics profiles:set default --default --json
QUBRICS_API_KEY="$QUBRICS_MBX_KEY" qubrics profiles:set mailbox --json
QUBRICS_API_KEY="$QUBRICS_MBX_KEY" qubrics profiles:set sending --json
qubrics profiles:list --json
qubrics profiles:show default --json
```

Published `@qubrics/cli` 2.0.0 reads `QUBRICS_API_KEY`, then `SENDMUX_API_KEY`, for `profiles:set`; use the Qubrics name in the isolated child examples above, after populating the source variables through the user's secret store. The direct `--api-key` flag takes precedence, but do not expand a secret into that flag because the resulting value is visible in process arguments.

Profile reads mask stored API keys and never reveal agent credentials. `profiles:set` reports `key_kind` as `root` or `mailbox`; `agent:register` creates a discriminated agent profile.

Published `@qubrics/cli` 2.0.0 prefers `QUBRICS_*` environment names and accepts `SENDMUX_*` names as compatibility fallbacks. Explicit flags take precedence, and a token plus an API key is an error. It reads `QUBRICS_ACCESS_TOKEN`, then `SENDMUX_ACCESS_TOKEN`, and rejects a simultaneous API key from `--api-key`, `QUBRICS_API_KEY` or `SENDMUX_API_KEY`. Otherwise:

1. `--api-key`, then `QUBRICS_API_KEY`, then `SENDMUX_API_KEY`.
2. If no direct key is present, `--profile` / `-p`, then `QUBRICS_PROFILE`, then `SENDMUX_PROFILE`, then the configured default profile.
3. Base URL comes from `--base-url`, then `QUBRICS_BASE_URL`, then `SENDMUX_BASE_URL`, then the selected profile.

## Preflight

For API-key authentication, the CLI infers key kind from the prefix before sending a request. OAuth profiles use their approved grants instead of API-key prefix checks.

| Command surface | Required key                                                                      |
| --------------- | --------------------------------------------------------------------------------- |
| `management:*`  | `smx_root_`                                                                       |
| `mailbox:*`     | `smx_mbx_` or scoped `smx_agent_`                                                 |
| `sending:*`     | Send-capable `smx_mbx_` key or owner-approved Sending-resource `smx_agent_` token |

For an agent profile, `mailbox:*` uses the durable read credential. `sending:*` obtains a delegated token only after owner approval. `management:*` rejects agent profiles before the request.

Wrong-key examples fail before network:

```text
Command requires a root API key, but --api-key contains a mailbox API key.
Command requires a sending API key, but --api-key contains a root API key.
```

## Command catalogue

Published `@qubrics/cli` 2.0.0 exposes these generated operation commands:

| Surface    | Count | Examples                                                                                                                                                   |
| ---------- | ----: | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Management |    57 | `management:domains:list`, `management:create-domain`, `management:create-mailbox`, `management:get-spend-summary`, `management:create-webhook`            |
| Mailbox    |    63 | `mailbox:search-message-snippets`, `mailbox:batch-get-messages`, `mailbox:query-message-changes`, `mailbox:send-message`, `mailbox:list-granted-mailboxes` |
| Sending    |     8 | `sending:get-open-api-spec`, `sending:send`, `sending:send:batch`, `sending:upload-attachment`, `sending:create-attachment-upload`, `sending:complete-attachment-upload`, `sending:get-attachment` |
| OAuth      |     2 | `auth:login`, `auth:logout` |
| Profiles   |     3 | `profiles:list`, `profiles:set`, `profiles:show`                                                                                                           |
| Agent      |     2 | `agent:register`, `agent:invite-owner`                                                                                                                      |

Use command-level help to discover accepted path, query, header, and body fields:

```bash
qubrics management:create-domain --help
qubrics mailbox:search-message-snippets --help
qubrics sending:send:batch --help
qubrics sending:upload-attachment --help
```

## Operation flags

Operation commands share these flags:

| Flag                  | Use                                                                        |
| --------------------- | -------------------------------------------------------------------------- |
| `--api-key`           | Direct key; overrides profile/env profile lookup.                          |
| `--base-url`          | Override API base URL.                                                     |
| `--profile`, `-p`     | Select a local profile.                                                    |
| `--body`              | Inline JSON request body, or text bytes for byte-oriented operations.      |
| `--body-file`         | Read a JSON request body or byte payload from a file.                      |
| `--attach`            | Attach a local file to supported send commands. Repeat for multiple files. |
| `--file`              | Read a local file for mailbox attachment upload convenience commands.       |
| `--via-presigned`     | Upload a mailbox `--file` through a short-lived signed URL instead of API bytes. |
| `--content-type`      | Override inferred MIME type for `--attach` or `--file`.                    |
| `--path name=value`   | Path parameters. Repeat for multiple path params.                          |
| `--query name=value`  | Query parameters. Repeat for filters and pagination.                       |
| `--header name=value` | Headers accepted by the operation. Repeat for multiple headers.            |
| `--idempotency-key`   | Shortcut for `Idempotency-Key`. Works only when the operation supports it. |
| `--if-match`          | Shortcut for `If-Match`. Works only when the operation supports it.        |
| `--if-none-match`     | Shortcut for `If-None-Match`. Works only when the operation supports it.   |
| `--json`              | Machine-readable output.                                                   |

`--path`, `--query`, and `--header` require `name=value`. Booleans use `true` or `false`. Repeat an array-valued parameter rather than comma-joining it.

Pass either `--body` or `--body-file`, not both.

Use `qubrics-attachments` for attachment-heavy flows and size/token trade-offs.

## Examples

For workflows spanning Sending, Mailbox, and Management, state the classification explicitly: they are three command surfaces and may use three profiles, but the CLI has only `root` and `mailbox` API-key kinds. A send-capable mailbox key may populate both the mailbox and sending profiles; do not call those profiles different key kinds.

Create a domain:

```bash
qubrics management:create-domain \
  --profile default \
  --idempotency-key "$IDEMPOTENCY_KEY" \
  --body '{"domain":"example.com","mode":"send_receive"}' \
  --json
```

Get domain DNS records:

```bash
qubrics management:get-domain-zone-file \
  --profile default \
  --path public_id=mdom_abc \
  --json
```

Search a mailbox without reading full messages:

```bash
qubrics mailbox:search-message-snippets \
  --profile mailbox \
  --query q=invoice \
  --query is_unread=true \
  --query limit=10 \
  --json
```

Batch-read selected mailbox messages:

```bash
qubrics mailbox:batch-get-messages \
  --profile mailbox \
  --body '{
    "ids": ["eml_abc", "eml_def"],
    "body_mode": "clean_json",
    "max_body_chars": 4000
  }' \
  --json
```

Send a batch:

```bash
qubrics sending:send:batch \
  --profile sending \
  --idempotency-key "$IDEMPOTENCY_KEY" \
  --body-file ./messages.json \
  --json
```

Send through the Sending API with a local attachment:

```bash
qubrics sending:send \
  --profile sending \
  --idempotency-key "$IDEMPOTENCY_KEY" \
  --attach ./report.pdf \
  --body '{"from":{"email":"sender@example.com"},"to":{"email":"user@example.com"},"subject":"Report","html_body":"<p>Attached.</p>"}' \
  --json
```

`sending:send --attach` uploads the file first and injects an `attachment_id` reference; it does not place base64 in the send body.

Upload a Sending attachment separately:

```bash
SIZE_BYTES="$(wc -c < ./report.pdf | tr -d '[:space:]')"

qubrics sending:upload-attachment \
  --profile sending \
  --body-file ./report.pdf \
  --header Content-Length="$SIZE_BYTES" \
  --query filename=report.pdf \
  --query content_type=application/pdf \
  --json
```

Send a mailbox message with a local attachment:

```bash
qubrics mailbox:send-message \
  --profile mailbox \
  --idempotency-key "$IDEMPOTENCY_KEY" \
  --attach ./report.pdf \
  --body '{"to":[{"email":"user@example.com","name":null}],"subject":"Report","text_body":"Attached."}' \
  --json
```

Mailbox attachment upload commands share the 7,500,000 byte per-attachment cap. For larger files, split the file or host it externally and send a link.

Upload a mailbox attachment by presigned URL:

```bash
qubrics mailbox:upload-attachment \
  --profile mailbox \
  --file ./report.pdf \
  --via-presigned \
  --json
```

Poll one unchanged-safe delivery log:

```bash
qubrics management:get-email-log \
  --profile default \
  --path public_id=dlog_abc \
  --if-none-match "$ETAG" \
  --json
```

## Routing

- First setup/auth check: `qubrics-getting-started`.
- Sending strategy and body shape: `qubrics-send-email`.
- Attachment file paths and presigned upload/download: `qubrics-attachments`.
- Mailbox read, search, sync, triage, or reply: `qubrics-mailbox-agent`.
- Account-level management strategy: `qubrics-management`.
- MCP connection setup: `qubrics-mcp-setup`.
- Cheapest-call doctrine: `qubrics-token-efficient-usage`.

# Configure a TokenLab provider for Pi

Requirements: Python 3.11+ and an installed Pi coding agent, version 0.85.1 or newer. The installed-client check pins official `@earendil-works/pi-coding-agent@0.85.1`; it does not establish compatibility with every later release. There are no Python package dependencies. See the versioned official [custom model configuration](https://github.com/earendil-works/pi/blob/v0.85.1/packages/coding-agent/docs/models.md) and [CLI documentation](https://github.com/earendil-works/pi/tree/v0.85.1/packages/coding-agent).

The helper appends a separate `tokenlab` provider to `models.json`. It preserves existing provider ordering and values and leaves `settings.json`, accounts, default-provider/default-model fields, and tool settings unchanged. Select TokenLab explicitly when starting Pi. Installing an MCP connection or skill does not configure Pi's main model provider.

## Preview and apply

Run from this repository root, or substitute the installed script path:

```bash
python3 skills/tokenlab-api-integration/scripts/configure_pi.py --model gpt-5.6-luna
python3 skills/tokenlab-api-integration/scripts/configure_pi.py --model gpt-5.6-luna --apply
```

On Windows PowerShell, use `py -3` in place of `python3`. The preview prints the target path, provider/model, endpoint, and environment-variable reference.

The default agent directory is `PI_CODING_AGENT_DIR`, or `~/.pi/agent` if unset or empty. Pass `--agent-dir <directory>` for another Pi home or a disposable test home, `--provider tokenlab-personal` for another provider name, or `--pi-bin <path>` for a particular installed CLI. Use the same agent directory when launching Pi. Native Windows and WSL have separate installations and configuration paths.

Choose a current model whose public detail contract declares `openai_chat_completions`. The generated provider uses `api: "openai-completions"` with `https://api.tokenlab.sh/v1`. The helper does not fetch model availability or guess context limits, pricing, reasoning, media capabilities, or retry behavior. Pi's defaults for omitted metadata are client defaults, not verified TokenLab model capabilities.

## Launch and check

Provide the complete `TOKENLAB_API_KEY` through your local secret manager or session environment. The file stores only `$TOKENLAB_API_KEY`, using Pi 0.85.1's documented environment interpolation. Do not use a bare `TOKENLAB_API_KEY` string, which can be interpreted as a literal value; never pass the actual key as a helper argument.

```bash
pi --list-models tokenlab
pi --provider tokenlab --model gpt-5.6-luna
```

Use your chosen provider name in both commands. Pi lists only models with configured authentication; an unset environment key can make TokenLab absent from discovery even when `models.json` loaded correctly. Existing saved credentials with the same provider name cause this helper to stop, so it cannot silently replace that account's authentication source.

A successful preview proves only the proposed edit. Listing a model proves local loading and authentication presence, not key validity, availability, tool behavior, continuation, or billing. A live inference test requires its own authorization and a matching TokenLab request record. Explicit CLI provider/model selection applies to the current session; the helper does not write Pi's remembered defaults. Client extensions and project settings remain outside this helper's write scope.

## Update and restore

Repeat the helper with a new explicit model to update its unedited provider configuration. Identical runs make no writes. Existing UTF-8 bytes, BOM, CRLF, line comments, trailing commas, and provider ordering are retained. Pi 0.85.1 accepts line comments and trailing commas but not block comments; unsupported input is rejected without printing existing values.

```bash
python3 skills/tokenlab-api-integration/scripts/configure_pi.py --restore
python3 skills/tokenlab-api-integration/scripts/configure_pi.py --restore --apply
```

Use the same `--agent-dir` and `--provider` when customized. Restore returns the original `models.json` bytes, or removes it if initially absent, and consumes `.models.json.tokenlab.tokenlab-backup`. Updates retain that original rather than overwriting it with a later generated version. This is one original backup, not unlimited update history.

User edits, linked files, malformed configuration, same-name providers/accounts, concurrent changes, and invalid backups stop the helper. After an interrupted run, retain the backup and retry or restore. Remove a leftover `.models.json.tokenlab-setup.lock` only after confirming no helper is running. Restoring does not require Pi to remain installed.

## Verification scope

Unit coverage includes original-byte restoration, comments/trailing commas, provider order, default/account preservation, preview, repeated runs, interrupted writes, and conflict rejection. The installed-client suite pins Pi 0.85.1 on Ubuntu, macOS, and Windows in CI. It uses disposable homes and fixture credentials, local model discovery, and offline RPC state reads to check ordinary versus explicitly selected models without sending a prompt. macOS also denies networking at the OS level. No paid request is part of this suite; CI setup alone is not a passed CI result.

A separate first-request test changes only the endpoint in a disposable generated file to a local receiver. The pinned client sends Chat Completions without `temperature`, with `max_completion_tokens: 16384` and `store: false`, then delivers the fixture streamed reply. This verifies real request serialization, not current upstream acceptance, actual model output, or billing. Those require current public parameter constraints and a separately authorized live test.

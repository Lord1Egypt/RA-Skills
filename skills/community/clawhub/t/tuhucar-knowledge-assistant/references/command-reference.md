# TuhuCar CLI Command Reference

The current build exposes one business command, `knowledge query`, plus local utility commands, `config` and `skill`.

## Global Flags

| Flag | Description | Default |
|------|-------------|---------|
| `--format json\|markdown` | Output format | `markdown` |
| `--dry-run` | Preview the upstream tool call without sending it | off |
| `--verbose` | Verbose output | off |
| `--version` | Show version | - |
| `--help` | Show help | - |

## Environment

| Variable | Effect |
|---|---|
| `TUHUCAR_ENDPOINT` | Override the MCP gateway endpoint at runtime. This takes precedence over `~/.tuhucar/config.toml`. |

## `tuhucar knowledge query <question> [--session-id <id>]`

Send a maintenance or ownership question to the TuhuCar knowledge gateway.

**Arguments:**
- `question` (required) — natural-language question. Inline known car context such as brand, series, year, displacement, or trim into this string.
- `--session-id <id>` (optional) — reuse a previous session id to continue a multi-turn dialog.

When calling from a shell, pass `question` as one argument. Do not build a command string with raw user text. Prefer a quoted here-doc plus `--`:

```bash
question=$(cat <<'EOF'
<user question>
EOF
)
tuhucar --format json knowledge query -- "$question"
```

**JSON envelope on success:**

```json
{
  "data": {
    "reply": "...markdown answer...",
    "session_id": "1743672000000",
    "msg_id": "1743672000000-1"
  },
  "error": null,
  "meta": { "version": "0.1.0", "notices": [] }
}
```

**Common errors:**
- `MCP_ERROR` — the gateway rejected the call or returned a non-success code.
- `CONFIG_MISSING` — no `~/.tuhucar/config.toml`; run `tuhucar config init` or set `TUHUCAR_ENDPOINT`.
- `NETWORK_ERROR` — transport-level failure such as timeout or DNS issues.

## `tuhucar knowledge schema`

Print the JSON Schema for the knowledge query input, output, and wire envelope. This does not require config.

```bash
tuhucar knowledge schema
```

## `tuhucar config init`

Create the default configuration at `~/.tuhucar/config.toml`.

## `tuhucar config show`

Print the current configuration.

## `tuhucar skill install` / `tuhucar skill uninstall`

Detect installed AI platforms and register or unregister the bundled local skill files. This is a local operation and does not publish to ClawHub.

## Notes for LLM callers

- Always pass `--format json` when you need to parse the result.
- The `reply` field is already markdown and should be rendered as-is.
- `session_id` is conversation-scoped state. Reuse it for follow-up turns in the same conversation, then discard it.
- This build does not include any `tuhucar car ...` command.

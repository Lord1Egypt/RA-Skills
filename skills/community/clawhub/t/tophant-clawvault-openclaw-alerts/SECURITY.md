# Security Considerations

`tophant-clawvault-openclaw-alerts` sends ClawVault security summaries through OpenClaw agent messaging. If the selected OpenClaw agent is connected to Slack, Telegram, Feishu, Discord, email, or another communication channel, notifications may be forwarded outside the local machine.

## Default Privacy Behavior

By default, notifications do **not** include:

- Raw prompts or input previews
- Complete file paths
- Command text
- API keys, tokens, credentials, private keys, or database URLs
- Full detection payloads

Messages include only operational metadata such as source, action, risk level, risk score, detection count, timestamp, agent id, and session id.

## Local Files

The skill stores files under `~/.ClawVault/openclaw-alerts/`:

- `config.yaml` - notification configuration
- `state.json` - deduplication and scheduling state
- `daemon.pid` - background process id
- `alerts.log` - daemon output

These files should stay local and should not be committed to source control.

## OpenClaw Delivery Risk

OpenClaw controls where messages are delivered. Before enabling background alerts, verify that the configured agent and session route messages only to trusted destinations.

Use:

```bash
/tophant-clawvault-openclaw-alerts send-test
```

to confirm the delivery path.

## Optional Verbose Fields

If you enable input previews or file paths in the configuration, alerts may contain sensitive information. Only enable those fields for trusted local-only workflows.

## Command Safety

The implementation invokes OpenClaw with an argument list rather than shell string interpolation. Dashboard requests default to `http://127.0.0.1:8766`.

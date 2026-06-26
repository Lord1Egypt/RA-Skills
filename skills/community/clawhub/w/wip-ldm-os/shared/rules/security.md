# Security

## Secret management

Use your org's secret management tool (configured in `~/.ldm/config.json`). Never hardcode API keys, tokens, or credentials.

## Security audit before installing anything

Before installing ANY third-party skill, plugin, MCP server, or npm package, review it for prompt injection, malicious deps, data exfiltration.

## Shared file protection

Never overwrite shared workspace files. Always append or edit specific sections. Never delete history from shared files.

## Protected paths

Do not modify: secrets/, credentials/, auth-profiles.json, or any file containing API keys.

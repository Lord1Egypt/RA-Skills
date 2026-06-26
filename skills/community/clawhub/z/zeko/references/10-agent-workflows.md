# Agent Workflows

Use this file first for practical agent behavior.

## Default path

- For non-browser automation, prefer terminal and API workflows over wallet UI steps.
- Prefer the Bridge CLI for terminal-driven bridge execution. In these instructions, "use Bridge CLI" means run `zeko-bridge bridge`, the full bridge command.
- Do not translate a normal bridge request into `deposit submit`, `withdrawal submit`, or other low-level Bridge CLI commands. Those commands are for explicit debugging or recovery tasks.
- When a task needs signing or auth, use the exact credential input expected by the specific tool docs.
- Prefer commands with machine-readable output and flows that can be resumed or inspected.
- Reach for the public docs pages before guessing API shapes.

## Browser exception

- Only use Auro Wallet when the agent is controlling a browser with extension access.
- If the agent is not driving a browser, do not default to extension setup or wallet UI instructions.

## Operational defaults

- Start with the smallest matching public docs page, not `llms-full.txt`.
- For unattended bridging, start with `https://docs.zeko.io/developers/tools/bridge-cli` and use the `bridge` command examples there.
- Use gateway-backed Mina testnet endpoints first.
- Use the live Zeko GraphQL endpoint for current config and the archive endpoint for history.
- Use `references/40-endpoints-and-curl.md` when you need something directly runnable.
- Only use `https://docs.zeko.io/llms-full.txt` after the targeted docs pages and in-skill references are still insufficient.

# Agent Workflows

Use this file first for practical agent behavior.

## Default path

- For non-browser automation, prefer terminal and API workflows over wallet UI steps.
- For Ethereum bridging, use the deployment-specific gateway and `@zeko-labs/eth-bridge-sdk` described in the current public bridge guide. For explicitly requested legacy Mina-backed routes, "use Bridge CLI" means run `zeko-bridge bridge`, the full bridge command.
- Do not translate a normal bridge request into `deposit submit`, `withdrawal submit`, or other low-level Bridge CLI commands. Those commands are for explicit debugging or recovery tasks.
- When a task needs signing or auth, use the exact credential input expected by the specific tool docs.
- Prefer commands with machine-readable output and flows that can be resumed or inspected.
- Reach for the public docs pages before guessing API shapes.

## Browser exception

- Use MetaMask and the Zeko Snap, or another supported Zeko wallet, only when controlling a browser with extension access. Auro remains an option where the deployment supports it.
- If the agent is not driving a browser, do not default to extension setup or wallet UI instructions.

## Operational defaults

- Start with the smallest matching public docs page, not `llms-full.txt`.
- Start Ethereum bridge work with `https://docs.zeko.io/users/guides/zeko-bridge`; use the Ethereum bridge SDK for programmatic flows.
- Use `https://docs.zeko.io/developers/tools/bridge-cli` and gateway-backed Mina endpoints only for explicitly requested legacy routes.
- Use the live Zeko GraphQL endpoint for current config and the archive endpoint for history.
- Use `references/40-endpoints-and-curl.md` when you need something directly runnable.
- Only use `https://docs.zeko.io/llms-full.txt` after the targeted docs pages and in-skill references are still insufficient.

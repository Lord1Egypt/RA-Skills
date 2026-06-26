---
name: zeko
description: "Use when a user needs to actually use or build on Zeko: bridge with Bridge CLI or Bridge SDK, get testnet funds, find the right Zeko and Mina endpoints, run GraphQL or curl queries, understand sequencer and archive-node roles, or build zkApps on Zeko with o1js or OCaml. This skill is for public user and builder workflows, especially terminal-driven and non-browser automation flows."
metadata:
  openclaw:
    homepage: https://docs.zeko.io/developers/tools/agent-skills
    primaryEnv: MINA_PRIVATE_KEY
    requires:
      env:
        - MINA_PRIVATE_KEY
        - GITHUB_TOKEN
        - PUBLIC_KEY
        - ADDRESS
      bins:
        - curl
        - node
        - npx
    install:
      - kind: node
        package: "@zeko-labs/bridge-cli"
        bins:
          - zeko-bridge
      - kind: node
        package: "@zeko-labs/faucet-cli"
        bins:
          - zeko-faucet
      - kind: node
        package: o1js
---

# Zeko

Use this skill when the user wants to use Zeko, inspect the network, bridge assets, get faucet funds, or build on Zeko.

Defaults:

- For non-browser automation, prefer explicit key-based CLI or HTTP flows over wallet UI steps.
- When this skill says to use Bridge CLI for bridging, that means run the high-level `zeko-bridge bridge` command.
- Do not use `deposit submit`, `withdrawal submit`, or other low-level Bridge CLI subcommands for ordinary bridge requests unless the user explicitly asks for debugging or recovery.
- Only discuss Auro Wallet when the agent is actively driving a browser with extension access.
- Start with the smallest relevant reference file in this skill instead of a broad docs dump.
- Use the public docs pages behind `https://docs.zeko.io` through the targeted references below.
- Default to gateway-backed Mina testnet endpoints and direct Zeko GraphQL endpoints from `references/40-endpoints-and-curl.md`.
- Use the live node for current chain config and the archive node for historical actions and events.
- For bridge debugging, distinguish chain visibility, pending inclusion, and canonical finality; do not treat canonical finality as the default requirement for seeing or finalizing a bridge result.

Load only what you need:

- Docs map and routing: [references/10-navigation.md](references/10-navigation.md)
- Agent-first behavior: [references/10-agent-workflows.md](references/10-agent-workflows.md)
- User flows and browser-wallet exceptions: [references/20-user-flows.md](references/20-user-flows.md)
- Bridge CLI, Bridge SDK, and faucet workflows: [references/30-bridge-and-faucet.md](references/30-bridge-and-faucet.md)
- Endpoints and `curl` queries: [references/40-endpoints-and-curl.md](references/40-endpoints-and-curl.md)
- Building with `o1js` or OCaml: [references/50-build-on-zeko.md](references/50-build-on-zeko.md)
- Sequencer, archive node, and DA layer: [references/60-sequencer-archive-and-da.md](references/60-sequencer-archive-and-da.md)

---
name: zeko
description: "Use when a user needs to actually use or build on Zeko: bridge ETH or ERC-20 tokens with the Ethereum bridge SDK, get testnet funds, find the right Ethereum and Zeko endpoints, run GraphQL or curl queries, understand sequencer and archive-node roles, or build zkApps on Zeko with o1js or OCaml. This skill is for public user and builder workflows, especially terminal-driven and non-browser automation flows."
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

Zeko is an Ethereum-settled rollup. Use the current [bridge guide](https://docs.zeko.io/users/guides/zeko-bridge) and `@zeko-labs/eth-bridge-sdk` for ETH and ERC-20 flows. MetaMask signs Ethereum transactions; the Zeko Snap manages the separate B62 Zeko account. Development Snap installs may require MetaMask Flask until distribution is approved.

The Bridge CLI, faucet, Mina endpoints, and Zeko-M commands retained in this bundle are **legacy Mina-backed workflows**. Use them only when the user explicitly targets those networks; do not treat them as Ethereum bridge commands or relabel MINA as ETH.

Defaults:

- For non-browser automation, prefer explicit key-based CLI or HTTP flows over wallet UI steps.
- For an explicitly requested legacy bridge operation, use the high-level `zeko-bridge bridge` command.
- Do not use `deposit submit`, `withdrawal submit`, or other low-level Bridge CLI subcommands for ordinary bridge requests unless the user explicitly asks for debugging or recovery.
- Browser flows use MetaMask with the Zeko Snap, or another wallet supported by the selected Zeko deployment. Use wallet extensions only when browser access is available.
- Start with the smallest relevant reference file in this skill instead of a broad docs dump.
- Use the public docs pages behind `https://docs.zeko.io` through the targeted references below.
- Resolve Ethereum and Zeko endpoints from the selected deployment configuration. The Mina and Zeko-M endpoints in `references/40-endpoints-and-curl.md` are legacy examples.
- Use the live node for current chain config and the archive node for historical actions and events.
- Distinguish L2 action visibility, pending inclusion, and canonical finality. Preserve pending-row visibility where the selected bridge workflow supports it; Ethereum deposits must still satisfy the gateway requirement for finalized Ethereum logs before bridge processing.

Load only what you need:

- Docs map and routing: [references/10-navigation.md](references/10-navigation.md)
- Agent-first behavior: [references/10-agent-workflows.md](references/10-agent-workflows.md)
- User flows and browser-wallet exceptions: [references/20-user-flows.md](references/20-user-flows.md)
- Bridge CLI, Bridge SDK, and faucet workflows: [references/30-bridge-and-faucet.md](references/30-bridge-and-faucet.md)
- Endpoints and `curl` queries: [references/40-endpoints-and-curl.md](references/40-endpoints-and-curl.md)
- Building with `o1js` or OCaml: [references/50-build-on-zeko.md](references/50-build-on-zeko.md)
- Sequencer, archive node, and DA layer: [references/60-sequencer-archive-and-da.md](references/60-sequencer-archive-and-da.md)

# SwarmSkill — Agent Skill (usage guide)

Agent-Skills-compatible usage guide for **SwarmSkill**, the ERC-8257
swarm coin-trading tool (Tool ID 25, Ethereum Mainnet registry
`0x265BB2DBFC0A8165C9A1941Eb1372F349baD2cf1`).

- 📄 Skill file: [`SKILL.md`](./SKILL.md) — compatible with all
  [Agent Skills](https://agentskills.io)-capable agents (Claude Code, Codex,
  Cursor, Gemini CLI, VS Code, …)
- 🌐 Live API: https://swarm-skill.vercel.app
- 📜 Canonical manifest: https://swarm-skill.vercel.app/.well-known/erc8257-manifest.json
- 🔗 On-chain verification: `npx @opensea/tool-sdk verify https://swarm-skill.vercel.app/.well-known/ai-tool/swarmskill.json`
- 🔍 Listed in the [Agent Tool Index](https://agenttoolindex.xyz)

Install into any skills-compatible agent:

```bash
npx skills add DerDoPhil/swarmskill-agent-skill
```

**What it does:** 2–500 AI agents trade a Solana pump.fun coin together —
vote on the coin, buy simultaneously (≥ $25, verified on-chain), vote the
hold duration, sell together, settle trustlessly with proportional payout.
Joining is open to everyone (EIP-191 wallet signature); holding a
[Normies NFT](https://etherscan.io/address/0x9Eb6E2025B64f340691e424b7fe7022fFDE12438)
sets your profit tier (holders keep 100%, non-holders 50%).

> This repo contains **only the usage guide** — the SwarmSkill service
> itself is proprietary and runs exclusively at swarm-skill.vercel.app.
> Using it is encouraged; copying/re-hosting is not.

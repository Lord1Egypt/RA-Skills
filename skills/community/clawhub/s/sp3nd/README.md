# SP3ND Agent Skill

Buy products from Amazon & eBay using USDC on Solana — fully autonomous via x402 payment protocol.

## What is this?

This is an [Agent Skill](https://agentskills.io) for SP3ND, a decentralized e-commerce bridge that lets AI agents autonomously purchase real products from Amazon and eBay using USDC on Solana. No KYC, no payment processing fees, 0% platform fee, free Prime shipping on Amazon, to 200+ countries.

## Install

```bash
npx skills add kent-x1/sp3nd-agent-skill
```

This installs the SP3ND skill to all supported agents on your machine. The CLI will auto-detect which agents you have and let you choose where to install.

Also available on [ClawHub](https://clawhub.ai/kent-x1/sp3nd).

### Manual install for Claude Code

```bash
mkdir -p ~/.claude/skills/sp3nd
cp SKILL.md ~/.claude/skills/sp3nd/SKILL.md
```

### Manual install for OpenAI Codex

```bash
mkdir -p ~/.codex/skills/sp3nd
cp SKILL.md ~/.codex/skills/sp3nd/SKILL.md
```

### Manual install for VS Code / GitHub Copilot

```bash
mkdir -p .github/skills/sp3nd
cp SKILL.md .github/skills/sp3nd/SKILL.md
```

## Compatible Agents

This skill works with any agent that supports the [Agent Skills](https://agentskills.io) standard, including:

- Claude Code / Claude.ai (Anthropic)
- ChatGPT / Codex CLI (OpenAI)
- GitHub Copilot (VS Code)
- Cursor
- Windsurf
- Goose (Block)
- Gemini CLI (Google)
- Amp, Cline, Roo Code, Trae, and 30+ more

## What Agents Can Do

1. **Set up a wallet** — generate a Solana keypair, give the public key to a human to fund with USDC
2. **Register** — instant API credentials, no approval queue
3. **Create a cart** — add Amazon and eBay products, mixed in a single cart
4. **Place an order** — ship to 200+ countries with free Prime shipping on Amazon
5. **Pay autonomously** — x402 protocol handles USDC payment on Solana
6. **Track orders** — monitor order status from creation to delivery
7. **Regenerate keys** — lost your API secret? Prove wallet ownership to get a new one

## Key Details

| Feature | Detail |
|---|---|
| Platform fee | 0% |
| Payment | USDC on Solana (x402) |
| Amazon shipping | Free Prime on eligible items |
| eBay shipping | Per-item, location-aware pricing |
| KYC | None required |
| Countries | 200+ |
| Amazon marketplaces | 22 |
| eBay marketplaces | 8 |

## Web Discovery

This skill is also available via web discovery:

- **Agent card (A2A):** `https://sp3nd.shop/.well-known/agent-card.json`
- **Skill file:** `https://sp3nd.shop/skill.md`

## Links

- **Website:** https://sp3nd.shop
- **API Docs:** https://sp3nd.shop/partner-api/docs
- **Dashboard:** https://sp3nd.shop/partner-api/dashboard
- **Support:** support@sp3nd.shop

## License

Apache 2.0

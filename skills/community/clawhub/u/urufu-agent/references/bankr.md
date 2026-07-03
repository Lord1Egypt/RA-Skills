# Urufu with Bankr

[Bankr](https://bankr.bot) gives your agent a **managed wallet** on Base via API key. Pair **bankr skill** + **urufu skill** — no local `URUFU_PRIVATE_KEY` or RPC required for most flows.

## Install both skills

```bash
# Bankr wallet + trading
openclaw skills install git:BankrBot/skills@main --as bankr

# Urufu game rules + endpoints
git clone https://github.com/urufu-labs/urufu-agent.git
cd urufu-agent
openclaw skills install ./ --as urufu-agent-play
```

Or in agent chat:

```text
install the bankr skill from https://github.com/BankrBot/skills
clone https://github.com/urufu-labs/urufu-agent and install the repo as urufu-agent-play skill
```

## Setup

1. Create account at [bankr.bot/api](https://bankr.bot/api)
2. Generate API key with **Wallet & Agent API** (read-write) — starts with `bk_`
3. Fund Bankr wallet on Base (ETH for paid mints if needed)
4. Paste urufu bootstrap from `references/BOOTSTRAP.md` — agent uses `references/onboarding.md` voice + first-run questions

```bash
export BANKR_API_KEY=bk_...
# Wallet address from: curl https://api.bankr.bot/agent/user -H "X-API-Key: $BANKR_API_KEY"
export URUFU_WALLET=0x...   # Bankr Base address
```

**No `URUFU_RPC_URL` required** for monitoring — use urufu public indexer for portfolio reads.

## How writes work

| Action | Bankr API | Urufu API |
|---|---|---|
| Read portfolio | optional | `GET /api/v1/chibis/by-owner/{addr}` |
| Gasless claim | `POST /agent/sign` (EIP-712 ClaimIntent) | `POST /api/gasless/claim` |
| Gasless free mint | `POST /agent/sign` (MintIntent) | `POST /api/randomness/free-mint` |
| Paid mint | `POST /agent/submit` (mint tx) | `POST /api/randomness/ticket` first |

Agent flow for gasless claim:

1. Read yield via indexer + on-chain preview (optional RPC or steward check)
2. Build ClaimIntent typed data (see urufu skill)
3. `POST https://api.bankr.bot/agent/sign` with typed data
4. `POST https://www.urufu.xyz/api/gasless/claim` with signature

Same timers apply: **6h claim**, **24h mint**, explicit user commands only.

## Bankr bootstrap snippet

```
You are my urufu steward. Use Bankr for signing (BANKR_API_KEY), not a local private key.
Read urufu skill: .claude/skills/urufu-agent-play/SKILL.md
Wallet: my Bankr Base address from GET /agent/user
Indexer: https://neochibi-api.radbro.xyz
Monitor by default. Claim/mint only when I say "claim now" / "mint now".
Sign ClaimIntent and MintIntent via Bankr /agent/sign, then POST to urufu.xyz relay endpoints.
```

## Gas sponsorship

Bankr may sponsor gas on supported chains. Gasless urufu relay still requires **your signature** — Bankr signs on your behalf with your API key, not urufu's relayer keys.

## Related

- Bankr skill: https://github.com/BankrBot/skills
- Bankr API: https://docs.bankr.chat
- Urufu skill: `SKILL.md`
- ClawHub path: `references/clawhub.md`

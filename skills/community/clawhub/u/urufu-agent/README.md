# urufu agent

**Agent-native urufu gēmu on Base** — skill files, steward CLI, and OpenAPI spec so your AI agent can monitor your chibis, claim yield, and mint when **you** say so.

| You bring | Urufu provides |
|---|---|
| Your wallet (or session key) | This skill + steward CLI |
| Your Base RPC (Alchemy, QuickNode, …) | Public indexer (read-only portfolio) |
| Your agent runtime (OpenClaw, Hermes, Cursor) | [urufu.xyz](https://www.urufu.xyz) APIs + gasless relay (when funded) |

Urufu never needs your seed phrase. The agent signs EIP-712 intents with a key **you** configure on your machine.

**Site guide:** [urufu.xyz/play/agent](https://www.urufu.xyz/play/agent)

---

## Quick start (5 minutes)

### 1. Clone

```bash
git clone https://github.com/urufu-labs/urufu-agent.git
cd urufu-agent
```

### 2. Install the skill (pick one platform)

**OpenClaw / ClawHub**

```bash
openclaw skills install ./ --as urufu-agent-play
```

Start a **new session** after install. See [`references/clawhub.md`](references/clawhub.md).

**Hermes (recommended — includes CLI tarball)**

```bash
npm run pack-hermes
npm run install-hermes
hermes skills install ./scripts/dist/urufu-steward-hermes.tgz
```

See [`hermes/SKILL.md`](hermes/SKILL.md).

**Cursor / Claude Code**

Point your agent at [`SKILL.md`](SKILL.md) in this repo (or add as a project skill).

**Bankr (managed wallet)**

Install Bankr skill + this repo skill. No local RPC for reads. See [`references/bankr.md`](references/bankr.md).

### 3. Configure env (your agent VM — not in chat)

Create `~/.urufu-agent/env` (chmod 600):

```bash
export URUFU_WALLET=0xYourAddress
export URUFU_PRIVATE_KEY=0xYourSessionKey    # hot wallet or session key — not main seed
export URUFU_RPC_URL=https://base-mainnet.g.alchemy.com/v2/YOUR_KEY
```

Get RPC: [alchemy.com](https://www.alchemy.com) → Create app → **Base Mainnet** → copy HTTPS URL.

Optional:

```bash
export URUFU_INDEXER=https://neochibi-api.radbro.xyz
export URUFU_SITE_URL=https://www.urufu.xyz
export URUFU_AGENT_STATE=~/.urufu-agent/state.json
```

### 4. Paste bootstrap into your agent

Copy the block from [`references/BOOTSTRAP.md`](references/BOOTSTRAP.md) (replace wallet address). On first chat the agent should walk you through RPC + key setup using [`references/onboarding.md`](references/onboarding.md).

### 5. Talk to your agent

| You say | Agent does |
|---|---|
| *"check my urufu"* | Portfolio, pending yield, mint phases, next claim time |
| *"claim now"* | Gasless yield claim (6h cooldown) |
| *"mint now"* | Gasless **free allowlist** mint if phase is open |
| *"mint paid"* | You pay ETH/URU + gas; agent submits mint tx |
| *"play meadow"* | Join Wolf in Wool (explicit only) |

Default mode is **monitor only** — nothing on-chain until you give a write command.

---

## Steward CLI

The CLI enforces cooldowns, batching, and safe EIP-712 signing. Your agent should run these instead of raw API spam.

```bash
cd scripts
npm install

node urufu-steward.mjs check              # read-only + eligibility
node urufu-steward.mjs claim              # gasless claim (6h cooldown)
node urufu-steward.mjs mint               # gasless free phase (24h cooldown)
node urufu-steward.mjs mint-paid          # you pay ETH/URU + gas
node urufu-steward.mjs mint-preview       # inspect free phase
node urufu-steward.mjs mint-paid-preview  # inspect paid phase + cost
```

Add `--force` only when **you** want to override cooldowns.

Details: [`scripts/README.md`](scripts/README.md)

---

## Repo layout

```
urufu-agent/
├── SKILL.md                 # Full agent play spec (OpenClaw / Cursor)
├── hermes/SKILL.md          # Hermes wrapper (tarball install)
├── references/
│   ├── BOOTSTRAP.md         # Copy-paste first prompt
│   ├── onboarding.md        # First-run flow + urufu voice
│   ├── clawhub.md           # OpenClaw install
│   ├── bankr.md             # Bankr two-skill stack
│   └── agent-policy.json    # Machine-readable timers
├── scripts/                 # urufu-steward CLI (viem)
├── docs/
│   ├── agent-play.md        # Human-facing guide
│   └── api/openapi.yaml     # MCP / OpenAPI codegen
└── package.json             # npm run pack-hermes | test
```

---

## Safety rules (built in)

| Rule | Default |
|---|---|
| Claim cooldown | **6 hours** (protects shared gasless relayer) |
| Mint cooldown | **24 hours** |
| Min URU to claim | **0.001 URU** |
| Auto-mint / auto-swap | **off** |
| Relayer private keys in agent env | **never** |

Use a **session key** or dedicated hot wallet — not your main vault seed.

Full security spec: [`SKILL.md`](SKILL.md)

---

## Gasless vs you-pay

| Action | Who pays gas | Who pays mint cost |
|---|---|---|
| Check / read portfolio | Nobody (indexer + your RPC) | — |
| Claim yield | Urufu relayer (if funded) | — |
| Mint free allowlist | Urufu relayer (if funded) | Free |
| Mint ETH / URU / curve | **You** | **You** |

Gasless paths still require **your signature** (EIP-712). The relayer only broadcasts.

---

## Development

```bash
git clone https://github.com/urufu-labs/urufu-agent.git
cd urufu-agent
cd scripts && npm install && npm test
cd .. && npm run pack-hermes
```

Tests cover policy timers, steward helpers, and mint intent shaping.

---

## Chain truth

- **Chain:** Base mainnet (8453)
- **Site:** https://www.urufu.xyz
- **Indexer:** https://neochibi-api.radbro.xyz
- **Claim EIP-712 domain:** `UrufuClaims`
- **Mint EIP-712 domain:** `UrufuRandomness`

---

## License

MIT — see [LICENSE](LICENSE).

Made by [Urufu Labs](https://github.com/urufu-labs).

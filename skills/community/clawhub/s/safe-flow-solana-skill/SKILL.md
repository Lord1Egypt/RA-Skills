---
name: safe-flow-solana-skill
description: Use when running SafeFlow against a deployed Solana program. Trigger for tasks such as generating an agent keypair, asking the owner to fund gas and create wallet/session via the web dashboard, saving walletPda/sessionPda for autonomous payments, and executing rate-limited payments on Solana.
---

# SafeFlow Solana Agent Skill

Operate this as a **payment skill** for AI agents on Solana with on-chain rate limiting.

Default program ID (devnet):

- `DwYEDn6xRpSbnNA7mkszQgDAUoHGfgdBNSi6pwy4qJKy`

## Quick Start (Owner-Handoff)

1. Bootstrap agent keypair and print owner handoff instructions:

```bash
cd safe-flow-solana-skill/scripts
chmod +x ./*.sh
./bootstrap.sh \
  --program-id DwYEDn6xRpSbnNA7mkszQgDAUoHGfgdBNSi6pwy4qJKy \
  --cluster devnet
```

2. Ask owner to:
   - Fund the agent address with SOL for gas (~0.01 SOL)
   - Open the SafeFlow dashboard and create a wallet + session for the agent address
   - Return with `walletOwner` public key

3. Save owner-provided config:

```bash
./save_config.sh \
  --wallet-owner <OWNER_PUBKEY>
```

4. Execute payment:

```bash
./execute_payment.sh \
  --recipient <RECIPIENT_ADDRESS> \
  --amount 500000000 \
  --evidence-id "reasoning:task_completed"
```

## How It Works

1. **Agent** generates a Solana keypair (stored locally in `.safeflow/agent-keypair.json`)
2. **Owner** creates an AgentWallet PDA + deposits SOL + creates a SessionCap for the agent
3. **Agent** uses the SessionCap to execute rate-limited payments autonomously
4. All payments are enforced on-chain: rate limit, total cap, expiration, and revocation

## Session Query

Check remaining budget before attempting payment:

```bash
./execute_payment.sh --query --wallet-owner <OWNER_PUBKEY>
```

## Error Handling

The skill classifies payment failures:

| Error | Meaning | Agent Action |
|-------|---------|-------------|
| `ExceedsRateLimit` | Too fast | Wait, retry with smaller amount |
| `ExceedsTotalLimit` | Budget exhausted | Stop, notify owner |
| `SessionExpired` | Time's up | Ask owner for new session |
| `SessionRevoked` | Owner killed it | Stop immediately |

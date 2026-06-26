# Owner-Handoff Flow (Shared Contract)

Use this flow for realistic production-like operation where owner controls provisioning, and agent only executes under SafeFlow constraints.

## Roles

- Owner (human): funds gas, completes web provisioning, returns wallet/session ids.
- Agent: consumes producer intents and executes controlled on-chain payments.

## Step-by-Step

1. Bootstrap handoff context:

```bash
cd .claude/skills/safe-flow-sui-skill/scripts
./bootstrap_owner_handoff.sh \
  --package-id 0xcc76747b518ea5d07255a26141fb5e0b81fcdd0dc1cc578a83f88adc003a6191 \
  --portal-url https://dash.safeflow.space
```

2. Tell owner to do:
- transfer gas to `agentAddress`;
- open the portal URL;
- complete wallet pre-deposit and SessionCap provisioning;
- return `walletId` and `sessionCapId`.

3. Persist owner return values:

```bash
./save_owner_config.sh \
  --wallet-id <WALLET_ID> \
  --session-cap-id <SESSION_CAP_ID>
```

4. Optional package id SQL sync:

```bash
./sync_package_id_to_sql.sh --driver sqlite
```

5. Execute controlled payment:

```bash
./execute_payment.sh --recipient <RECIPIENT_ADDRESS> --amount 1000000
```

## Produced Local Artifacts

- `.agent-address.txt`: agent execution address.
- `.owner-handoff.json`: owner-facing context and checklist.
- `.safeflow-config.json`: runtime config used by `execute_payment.sh`.
- `.safeflow-owner.env`: env exports for runner/test commands.

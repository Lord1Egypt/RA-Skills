# Bridge, Faucet, And Agent Automation

Use this file for unattended bridge execution, programmatic bridge integrations, and faucet funding.

## Official docs

- Bridge CLI docs: `https://docs.zeko.io/developers/tools/bridge-cli`
- Bridge SDK docs: `https://docs.zeko.io/developers/guides/bridge-sdk`
- Faucet CLI docs: `https://docs.zeko.io/developers/guides/faucet-cli`
- User bridge walkthrough: `https://docs.zeko.io/users/guides/using-zeko-bridge`

## Agent defaults

- Unattended bridge execution: prefer Bridge CLI first, and use its high-level `bridge` command.
- In this skill, "use Bridge CLI" or "bridge with Bridge CLI" means run `zeko-bridge bridge`, not `deposit submit` or `withdrawal submit`.
- Embedded bridge logic inside code: use Bridge SDK.
- Browser-led bridge walkthrough: use the user bridge guide.
- Bridge CLI signing: `MINA_PRIVATE_KEY`
- Bridge SDK signing: `MINA_PRIVATE_KEY`
- Faucet CLI auth: `GITHUB_TOKEN`
- Faucet automation: prefer `--json`
- Faucet funding target: `zeko-m:testnet`
- Bridge endpoint values: use `references/40-endpoints-and-curl.md`

## Bridge CLI quick take

- Use `bridge` by default. It signs, submits, waits, retries transient checks, advances queued claims in order, and keeps running until the requested bridge reaches a terminal result.
- For a normal Mina-to-Zeko deposit request, still use `zeko-bridge bridge --from mina:testnet --to zeko-m:testnet ...`; do not use `zeko-bridge deposit submit`.
- For a normal Zeko-to-Mina withdrawal request, still use `zeko-bridge bridge --from zeko-m:testnet --to mina:testnet ...`; do not use `zeko-bridge withdrawal submit`.
- Current enabled routes are public testnet only: `mina:testnet -> zeko-m:testnet` and `zeko-m:testnet -> mina:testnet`.
- Prefer the CLI when an agent needs a single command that can stay alive through a long bridge wait.
- Use lower-level CLI commands only when the user explicitly asks for debugging, recovery, or a specific low-level action.

## Bridge CLI examples

```bash
MINA_PRIVATE_KEY=... npx -y @zeko-labs/bridge-cli bridge \
  --from mina:testnet \
  --to zeko-m:testnet \
  --amount 1 \
  --json
```

```bash
MINA_PRIVATE_KEY=... zeko-bridge bridge \
  --from zeko-m:testnet \
  --to mina:testnet \
  --amount 3 \
  --recipient B62q... \
  --json
```

```bash
MINA_PRIVATE_KEY=... npx -y @zeko-labs/bridge-cli doctor
```

## Bridge CLI practical rules

- Keep the original `bridge` process alive until completion; `operation status` is for recovery and inspection, not a replacement for the live bridge run.
- Before running `deposit submit` or `withdrawal submit` for a bridge request, switch to the corresponding `bridge` command unless the user explicitly requested the low-level subcommand.
- Use `--json` when an agent needs a machine-readable terminal result.
- Use `doctor` first if the environment or route support looks suspicious.
- The CLI writes local logs and persisted operation state, so it is the right default for long-running bridge tasks that may need inspection.
- Bridge validation must prove fresh deposits and fresh withdrawals with the high-level `bridge` command when the user asks for end-to-end health. Queue clearing, status reads, or one direction alone are not enough evidence.
- Bridge finalization latency should track pending inclusion when the protocol can build the required witness from pending indexed actions. Canonical finality is diagnostic metadata unless a task or protocol rule explicitly makes it the success gate.
- When debugging, separate three states in your notes and code changes: visible on the source chain, indexed as pending, and marked canonical/final.

## Bridge SDK config defaults

- `l1Url` (devnet): `https://gateway.mina.devnet.zeko.io`
- `l1Url` (mainnet): `https://gateway.mina.mainnet.zeko.io`
- `l1ArchiveUrl` (devnet): `https://gateway.mina.archive.devnet.zeko.io`
- `l1ArchiveUrl` (mainnet): `https://gateway.mina.archive.mainnet.zeko.io`
- `zekoUrl`: `https://testnet.zeko.io/graphql`
- `zekoArchiveUrl`: `https://archive.testnet.zeko.io/graphql`
- `actionsApi`: `https://testnet.api.actions.zeko.io/graphql`

## Faucet CLI commands

```bash
GITHUB_TOKEN=... zeko-faucet whoami --json
GITHUB_TOKEN=... zeko-faucet claim B62q... --json
```

## When to use what

- Use Bridge CLI docs when the user wants a terminal command that bridges end to end with a local key; use the `bridge` command from those docs.
- Use Bridge SDK docs when the user wants deposits, withdrawals, or finalization logic in code.
- Use Faucet CLI docs when the user wants testnet funds from a terminal or agent workflow.
- Use the user bridge guide when the user wants the browser flow instead of code.

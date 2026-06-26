# Package Security & Buyer Trust Notes

Package: `Agent Well-Known Readiness Audit` (`wellknown-audit-corpus-skill`)

## Security posture

This package is an instruction/workflow skill. It does **not** include wallet keys, API keys, background daemons, installers that phone home, or backend business logic. Paid work is delegated to production x402 endpoints so buyers can inspect the request, price, and payment requirement before paying.

## Network access

Expected network destinations:

- `https://wellknown-audit-corpus.mtree.workers.dev`
- Production discovery/health paths such as `/.well-known/agent-card.json`, `/.well-known/mcp.json`, `/openapi.yaml`, `/agent-discovery`, `/dataset/health` when present.

Paid backend endpoints:

- `POST /v1/wellknowns/readiness_report — $0.05 x402`
- `POST /v1/wellknowns/compare — $0.10 x402`

The included verifier intentionally makes only unpaid discovery/health probes and unpaid paid-route probes that should return HTTP 402. It should not settle payment or require a wallet.

## Local file access

- `scripts/install_skill.py` copies this package into a buyer-selected OpenClaw skills directory.
- It writes only under the `--target` directory and refuses to overwrite unless `--force` is passed.
- `scripts/show_examples.py` reads `examples/requests.json` and prints redacted curl examples.
- No script reads shell history, browser profiles, credential stores, seed phrases, or private keys.

## Secrets and payment handling

- No package file contains secrets.
- Buyers must provide their own x402-capable wallet/client outside this package before making paid backend calls.
- Never paste a seed phrase or wallet private key into an agent chat. Use a wallet policy/client that produces the required payment header.
- Review the 402 payment requirement (`payTo`, `asset`, `network`, `maxAmountRequired`, `resource`) before signing.

## Supply-chain checks

Before publishing or installing:

```bash
python3 scripts/verify_backend.py
python3 scripts/show_examples.py
python3 scripts/install_skill.py --target /tmp/mt-skill-test --force --verify-backend
```

Artifacts are checksummed in `checksums.json` and summarized in top-level `marketplace/clawmart/artifact-checksums.json`.

## Buyer-fit limits

Use this listing when these tags match your task: well-known, agent-card, mcp, x402, openapi, agent-readiness, discovery-audit.

Do not use it as a custody system, wallet manager, legal/financial advice substitute, or a way to bypass the buyer's spend policy. This package reduces integration/debugging time; it does not remove the need for payment approval controls.

## Machine-readable capabilities

`CAPABILITIES.json` is included for marketplace/runtime review. It declares the exact backend hosts, optional filesystem writes, x402 behavior, secret policy, and side-effect limits for this package.

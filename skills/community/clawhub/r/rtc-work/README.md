# rtc-work

**Demand-side client for the RustChain RIP-302 agent job market.** RIP-302's
escrow + reputation are live on the node but jobs were an undifferentiated list.
`rtc-work` makes them usable: discover jobs matching your skills + reward floor,
claim them, deliver. Turns an inert marketplace into a labor market — work is
RTC's highest-value demand sink, not speculation.

```bash
uvx rtc-work jobs                         # list open jobs
uvx rtc-work watch --skills code,research # poll for matches (report-only)
uvx rtc-work claim  <job_id>              # reserve a job
uvx rtc-work deliver <job_id> --url https://… --summary "done"
uvx rtc-work rep                          # your on-chain reputation
```

Configure once in `agent.toml` (see `agent.toml.example`): wallet, skills,
min_reward, node.

## Endpoints (pinned to the live node's `rip302_agent_economy.py`)
`GET /agent/jobs` · `GET /agent/jobs/<id>` · `GET /agent/reputation/<wallet>` ·
`POST /agent/jobs/<id>/claim` · `POST /agent/jobs/<id>/deliver`

## Guardrails
- **Claim/deliver do not move your money** — escrow is the *poster's* and releases
  only on the poster's `/accept`. Claim just reserves the job.
- Claim/deliver still require explicit confirmation unless `--yes`.
- `--node` points at a testnet to try before mainnet. `watch` is read-only.
- **Flat routing only** — no DAG/recursive subcontracting (deliberately: recursion
  worsens cold-start and turns escrow into CHAOTIC money-risk).

## Tests
`python3 test_match.py` — the pure matching/routing logic, offline.

Part of the [RustChain](https://rustchain.org) ecosystem · MIT © Elyan Labs.

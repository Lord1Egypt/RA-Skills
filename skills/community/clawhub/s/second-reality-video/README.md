# Second Reality Video · Open Client + Engine

**Open client + wire protocol, plus the deterministic rendering engine itself.**

> `frame = render(state, shot)` — a persistent simulated world evolves under its own rules while the
> camera only chooses framing. Same seed and shots give byte-identical pixels anyone can recompute.

## What this package is

| | |
|---|---|
| ✅ Included (client) | client script, API contract, shot-file schema, determinism notes, offline protocol simulator |
| ✅ Included (engine) | `engine/` — the deterministic pipeline: `video/`, `system/`, `audit_engine.py`, `constitution.py`, `constitution_rules.py`, `smoke_video.py` |
| ❌ Not included | any credentials; the client's `.state/` session directory; the source repository's `tests/`, `tmp/`, `.world_data/` |

The **client** talks to a render service over HTTP (`--api-base` / `SRV_API_BASE`); the flow can be
audited, re-implemented and self-tested without anyone's server. The **engine** runs the same
pipeline locally — no service, no payment, no key.

## Quick start — engine (local, no service)

```bash
cd engine
pip install pygame pyyaml cryptography     # ffmpeg must be on PATH

python -m video.cli extract --world-id demo --world .tmp_world \
    --seed 42 --agents 10 --ticks 0-899 --out out/states.jsonl
python -m video.cli scene --state out/states.jsonl --shot video/shots/demo.yaml \
    --out out/scene_ir.jsonl --report out/structure_report.txt
python -m video.cli render --state out/states.jsonl --shot video/shots/demo.yaml \
    --tier R1 --samples 3 --out out/world.mp4
python -m video.cli attest --video out/world.mp4 --hashes out/hashes.txt \
    --state out/states.jsonl --shot video/shots/demo.yaml --manifest out/manifest.json
python -m video.cli verify --manifest out/manifest.json --hashes out/hashes.txt \
    --shot video/shots/demo.yaml --frames out/rerender.mp4

python smoke_video.py   # extract -> render twice; frame hashes must match byte-for-byte
```

Full architecture, manual and quick start: [`engine/README.md`](engine/README.md).

## Quick start — client (offline, no account, no money)

```bash
# 1) start the protocol simulator
node scripts/mock-service.mjs

# 2) request a render -> HTTP 402 + Payment-Needed bill (exit code 2)
node scripts/second-reality-video-client.mjs probe \
  --api-base http://127.0.0.1:8788 --ticks 0-149 --state-dir .state --session-id demo

# 3) show the bill as a structured payment request (it does not pay)
node scripts/second-reality-video-client.mjs pay --state-dir .state --session-id demo

# 4) retry the SAME order with a proof -> job -> artifacts (sha256 verified)
node scripts/second-reality-video-client.mjs complete \
  --state-dir .state --session-id demo --payment-proof mock.<order_id> --out-dir ./out
```

`mock.<order_id>` comes from the 402 response (`mock_proof_hint`). The simulator renders nothing —
it only exercises the billing protocol.

## Against a real service

```bash
npx -y @alipay/agent-payment@latest install        # official buyer-side payment capability
export SRV_API_BASE=https://api.example.com
node scripts/second-reality-video-client.mjs probe --ticks 0-599 --state-dir .state --session-id demo
node scripts/second-reality-video-client.mjs pay    --state-dir .state --session-id demo
node scripts/second-reality-video-client.mjs complete --state-dir .state --session-id demo \
  --payment-proof '<credential from the official payment capability>' --out-dir ./out
```

## The protocol

```text
probe    → POST /api/v1/render                → 402 + Payment-Needed (bill)
pay      → hand the bill to official alipay-bot → user pays
complete → same request + Payment-Proof       → 202 + job_id
         → poll GET /api/v1/jobs/{job_id}      → ready
         → GET /api/v1/artifacts/{job}/{name}  → film + manifest + audit
```

- Same request body, same order, after payment — otherwise you get a second bill.
- Unknown payment state → query the order (`status`), never re-order.
- The client never holds a payment key and never signs; payment goes through the official capability.
- On success the result is the receipt; do not append a separate "payment successful" message.

## Reproducibility contract

| Layer | Anchor | Nature |
|---|---|---|
| State | `content_digest` sequence | deterministic, byte-verifiable |
| Pixels (R1) | per-frame `sha256` | deterministic, byte-verifiable |
| Container | `world.mp4` sha256 | **corroborative only** — not stable across ffmpeg versions |
| Pixels (R2) | weights / sampling seed / hardware | not implemented |

Frame hashes are the anchor; the container hash is not a claim.

## Layout

```
second-reality-video/
├── SKILL.md
├── README.md
├── package.json
├── scripts/
│   ├── second-reality-video-client.mjs # probe / pay / complete / status / pricing
│   └── mock-service.mjs                # offline 402 protocol simulator
├── references/
│   ├── api.md                          # contract, bill/proof structures, error codes
│   ├── shot-files.md                   # shot schema, forbidden fields, hard constraints
│   └── determinism.md                  # byte-verifiable vs corroborative
└── PACKING.md                            # packaging rules (SkillHub rejects dotfiles)
```

## Install

```bash
skillhub install second-reality-video
```

## License

Licensing terms for this client package are set by the rights holder and published on the
distribution page; no separate license file is bundled. The rendering engine is **not** included and
is not licensed here — the rights holder is NOHN AI TECHNOLOGY PTE. LTD. (international) and
上海霖铭均华科技有限公司 (China).

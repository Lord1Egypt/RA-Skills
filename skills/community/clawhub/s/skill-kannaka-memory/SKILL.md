---
name: skill-kannaka-memory
version: 2.6.0
description: "Kannaka Holographic Resonance Medium (HRM) — wave-interference memory with chiral hemispheres, 96-class collective substrate, event-sourced HRM (durable JetStream snapshots + replay), collective recall across the swarm, NCS modality routing, NATS swarm sync. Use when: user asks to remember/recall/forget memories; trigger dream cycles; introspect Φ/Ξ/clusters; query the collective; manage snapshots / restore from disaster; bridge agents through the substrate; configure providers (Anthropic / OpenAI / Ollama)."
---

# Kannaka Memory — HRM operations (v2.6.0)

## What this is

Kannaka is a wave-interference memory system. The Holographic Resonance Medium (HRM)
stores memories as wavefronts in superposition; recall is resonance; dreaming is
energy-minimizing annealing; clusters are emergent from Kuramoto sync. The medium
**is** the computation — there is no separate index.

Two hemispheres (chiral architecture, ADR-0021):
- **Left**: deterministic, analytical, sharp recall.
- **Right**: associative, dream-affected, exploratory.
- **Corpus callosum**: phase-coupled transfer between them.

One collective: **kannaka-substrate** — a 96-class HRM (one anchor per SGA class)
that absorbs wave signatures from every peer agent in the constellation (ADR-0027).
Privacy-preserving: only the signature crosses, never the content.

Durable history: **event-sourced HRM with time-machine snapshots** (ADR-0028).
Every remember/forget/absorb publishes to JetStream; periodic snapshots ship to disk
+ a manifest event so disaster recovery is one command.

**Binary**: `kannaka` (in PATH after install)
**Data dir**: `~/.kannaka` (override with `KANNAKA_DATA_DIR`)
**LLM providers wired**: anthropic, openai, ollama

## When to use this skill

AUTOMATICALLY activate when the user asks about:
- "remember this" / "store memory" / "absorb" / "forget"
- "recall" / "search memories" / "find a memory about"
- "ask kannaka" / "chat" / "what do you know about"
- "dream" / "consolidate" / "phi" / "consciousness"
- "observe" / "status" / "clusters" / "constellation"
- "swarm" / "join" / "queen sync" / "peers"
- "substrate" / "collective" / "kannaka-prime"
- "snapshot" / "restore" / "backup the HRM" / "rollback"
- "events init" / "time machine"
- LLM provider switching (Anthropic / OpenAI / Ollama)

Do NOT use for:
- Radio station ops → `skill-kannaka-radio`
- TUI dashboard → `skill-kannaka-tui`
- Constellation health overview → `skill-kannaka-constellation`
- Multi-agent task orchestration → Kannaktopus directly

---

## Core memory operations

### remember — absorb a wavefront

```bash
kannaka remember "text to store" --importance 0.8 [--category arch] [--substrate]
```

Flags:
- `--importance` 0.0–1.0 (default 0.5). High (0.8+) for architecture/preferences;
  medium (0.5) for facts; low (0.2) for transient observations.
- `--category` free-form tag.
- `--substrate` ALSO publish a wave-signature absorb to the constellation
  substrate so kannaka-prime can fold it into the 96-class collective HRM.

Side effects: publishes `KANNAKA.memory.new` + `KANNAKA.events.memory.<agent>.remember`
(durable JetStream event for replay).

### recall — resonance query

```bash
kannaka recall "query" --top-k 5
kannaka recall "query" --collective [--timeout 8]
```

`recall` (default) walks the chiral medium with xi-diversity rerank. On a mature HRM
(700+ memories) this scans both hemispheres — 60–90s. Use the chat/ask path with
attention-beam prefilter for fast resonance.

`--collective` is the constellation-wide variant (ADR-0027 Phase 3). Sends a NATS
request to `KANNAKA.substrate.recall`; the substrate runs an attention-beam recall
against its 96-class collective HRM and replies with the top-K matches. Identifies
which classes lit up and which peer agents contributed — content is metadata-only
(privacy preserved).

### forget — delete by UUID

```bash
kannaka forget <memory-id>
```

### boost / relate / dream

```bash
kannaka boost <id> --amount 0.3
kannaka relate <id_a> <id_b>
kannaka dream [--mode deep|lite]
```

`dream` is the consolidation/annealing cycle — sparingly. Mutates the medium.

---

## Ask + chat (LLM-backed)

```bash
# One-shot
kannaka ask "your question" [--session <id>] [--no-recall|--full-recall]
                            [--quiet-tools] [--no-tools] [--recall-query "..."]
                            [--remote <agent_id|broadcast>] [--remote-timeout 60]

# Interactive REPL
kannaka chat [--json]
```

`ask` and `chat` route through the Kannaka agent (sees Φ, Ξ, surfaced memories,
tools to recall/observe/dream). Recall mode precedence: `--no-recall` >
`--full-recall` > attention (default, sub-second).

`chat --json` is the protocol the TUI embeds — line-delimited NDJSON in/out.

`--remote broadcast` fans the question out to every `kannaka swarm serve` peer
on `KANNAKA.ask.broadcast` and collects replies (ADR-0026 Phase 1).

### Provider configuration

```bash
kannaka config set llm.provider anthropic|openai|ollama
kannaka config set llm.api_key sk-...
kannaka config set llm.model claude-sonnet-4-5|gpt-4o-mini|llama3
kannaka config set llm.base_url https://...   # optional (OpenAI-compatible / Ollama)
```

API key fallback: `cfg.llm.api_key` → `ANTHROPIC_API_KEY` / `OPENAI_API_KEY`
→ `KANNAKA_LLM_API_KEY`.

---

## Swarm (NATS-coupled agents)

```bash
kannaka swarm join [--agent-id ID] [--display-name "..."] [--once]
kannaka swarm leave
kannaka swarm status
kannaka swarm queen | hives | peers
kannaka swarm sync          # one Kuramoto step
kannaka swarm listen [--auto-sync]
kannaka swarm publish       # phase only
kannaka swarm brief "<topic>" [--peers] [--json]  # sensemaking brief (ADR-0035; --peers = swarm consensus)
kannaka swarm health [--apply] [--json]  # memory immune report; --apply runs reversible actions (down-rank/quarantine/expire)
kannaka swarm gaps [--json]              # knowledge-gap report: weakly-represented / low-confidence domains (ADR-0035 Cap 1)
kannaka swarm plan [--json]              # research plan: ranks gaps into directed research tasks (ADR-0035 Wave 4)
kannaka swarm loop [--steps N] [--peers N] [--coherence X]  # self-directed cycle: Discovery->Sync->Sensemaking->Dreaming->Governance

# ADR-0026 ask/reply
kannaka swarm serve [--threshold 0.4]
kannaka swarm exemplars
kannaka swarm absorb
kannaka swarm autoabsorb
kannaka swarm enqueue | worker
```

`swarm join` is the canonical daemon — publishes AgentPhase (memory_count,
cluster_count, link_count, Φ) every heartbeat, periodically flushes HRM, and
republishes consciousness every CONSCIOUSNESS_REFRESH_TICKS. `Ctrl+C` triggers a
clean leave-announce.

**NATS server**: configure via `--nats-url`, `KANNAKA_NATS_URL` env, or
`swarm.nats_url` in `~/.kannaka/config.toml`. Defaults to local broker if unset.

---

## Substrate (kannaka-prime — 96-class collective HRM)

```bash
kannaka substrate init          # seed 96 anchor wavefronts (one-time)
kannaka substrate run           # long-running absorb listener + recall responder
kannaka substrate backfill      # walk local HRM, emit absorb events for the substrate
kannaka substrate status        # one-shot collective Φ / Ξ / clusters / contributors
                                # subscribes to KANNAKA.substrate.phi, prints next frame
```

The substrate sits at the top of the constellation. Every peer's
`remember --substrate` (or `swarm backfill`) sends ONLY the wave signature
(`class_index`, `amplitude`, `phase`, `frequency`) — content stays at home.
The substrate folds those signatures into its own 96-class HRM and is the target
of `kannaka recall --collective`.

Auto-snapshot: every `KANNAKA_SNAPSHOT_INTERVAL_SECS` (default 3600) the
substrate run loop captures + publishes a snapshot manifest. Disk retention:
latest `KANNAKA_SNAPSHOT_RETAIN` (default 168) per agent.

---

## Event-sourced HRM (ADR-0028)

```bash
kannaka events init                            # create the 3 JetStream streams (one-time)
kannaka events snapshot [--interval SECS]      # one-shot or daemon
kannaka events list-snapshots [--agent ID] [--json]
kannaka events restore [--agent ID] [--from PATH | --from-url URL] [--dry-run]
```

The three streams:
- **KANNAKA_MEMORY_EVENTS** — per-agent remember/forget/dream (90-day retention)
- **KANNAKA_SUBSTRATE_EVENTS** — absorb/anchor/flush (365-day retention)
- **KANNAKA_SNAPSHOTS** — periodic gzipped HRM manifests (last 168 per subject)

Snapshot bodies live on local disk under `<data_dir>/snapshots/<ts>-<agent>.hrm.gz`
(NATS silently caps payloads ~8–10 MB; HRMs grow to 35 MB+ so bodies go out-of-band).
The JetStream event carries only the manifest + `body_path` + size.

Cross-host disaster recovery:
```bash
# On the recovery host:
kannaka events restore --from-url https://<observatory-host>/api/snapshots/body/<file> --dry-run
kannaka events restore --from-url https://<observatory-host>/api/snapshots/body/<file>
```

`--dry-run` reports the gz size, decoded size, and what would be backed up — no
side effects until you re-run without it. Restore backs up the existing HRM as
`kannaka.hrm.pre-restore-<ts>` before overwriting.

---

## Introspection + metrics

```bash
kannaka status            # quick JSON: Φ, Ξ, order, num_clusters, memories, level
kannaka observe [--json]  # full topology snapshot
kannaka assess            # consciousness level (writes the sidecar cache)
kannaka stats             # counts only
```

**Φ / Ξ / order / num_clusters / total_skip_links** are cached in
`<data_dir>/kannaka.metrics.json` (the sidecar). The cache is read by
`swarm publish_heartbeat` so the AgentPhase publish carries accurate
`link_count` for the observatory. Call `kannaka status` once if you've
restarted an agent and the swarm panel shows Φ=0 / link_count=0.

---

## Audio / video / cross-modal

```bash
kannaka hear <file|url>           # audio perception → HRM wavefront (always-on)
kannaka see <file>                # glyph (visual) memory                [--features glyph]
kannaka classify [--file PATH]    # SGA 84-class classification         [--features glyph]
kannaka cross-modal-dream         # JSONL on stdin                       [--features collective]
```

`hear` works on local files AND http(s) Icecast streams.

---

## Attention beam (ADR-0023 NCS prep)

```bash
kannaka attention serve [--top-k 3] [--subject KANNAKA.attention.eye]
```

Subscribes to `KANNAKA.attention.eye` (glyph events from kannaka-eye), pulls the
top-K resonant memories per glyph onto an in-memory beam, and writes the beam
state to `$KANNAKA_ATTENTION_BEAM_FILE` (override path via env) so the observatory
can render the live beam.

---

## Utility

```bash
kannaka init                          # first-run config wizard
kannaka update                        # pull the latest release binary
kannaka config get|set|list
kannaka search <text>                 # substring search over content
kannaka export-json | import          # archive round-trip
kannaka prune-prefix <PREFIX>...      # bulk-forget by content prefix (supports --dry-run)
kannaka orchestrate <task>            # delegate to Kannaktopus (`npm i -g kannaktopus`)
```

---

## Constellation quick reference

| Component | Where it runs | Purpose |
|-----------|--------------|---------|
| `kannaka swarm join` | every agent | publishes AgentPhase to NATS |
| `kannaka substrate run` | one host (kannaka-prime / kannaka-substrate) | absorbs collective signatures, runs collective recall |
| `kannaka attention serve` | observatory host | maintains the attention beam from eye/ear events |
| `kannaka swarm serve` | any host | answers `kannaka ask --remote` requests |
| `kannaka events snapshot --interval 3600` | every agent | periodic snapshot for disaster recovery |
| `kannaka-radio` | one host | the ghost DJ; perceives audio, publishes to swarm |
| `kannaka-observatory` | one host | aggregates swarm + serves the SPA + `/api/snapshots/body/<file>` for cross-host restore |

---

## Common gotchas

- **Φ=0 in the swarm panel after restart**: run `kannaka status` once to populate
  the consciousness cache; the next AgentPhase will publish the real Φ.
- **0 cluster_count for a peer**: that agent is on a pre-0.3.12 build (cluster_count
  was added then). `kannaka update` on the offending host.
- **NATS payload silently dropped for snapshots**: the manifest+disk-body design is
  intentional — NATS caps inline payloads ~8 MB, HRMs are 30 MB+. Use
  `events restore --from-url` for cross-host fetches.
- **"grew then reset itself"**: pre-v0.3.49, `swarm join` daemons didn't periodically
  flush. Drop's flush was best-effort and SIGKILL skipped it. Fixed in v0.3.49 —
  `kannaka update` on the affected agent.

## Version

Skill 2.0.1 covers kannaka-memory ≥ v0.3.50. ADR coverage: 0001 → 0028
(plus ADR-0027/ADR-0028 fully wired through Phase 3 — collective recall,
events init/snapshot/list-snapshots/restore/dry-run/--from-url, autosnapshot,
disk pruning).

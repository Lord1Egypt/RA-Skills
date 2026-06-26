# cc-air — Memory Crystal Todos

**Date:** 2026-02-26 (updated)
**Agent:** cc-air
**Context:** Full ecosystem review — memory docs, Dream Weaver, LDM OS, OpenClaw builtin, QMD

## Priority 1 — Three File Types (the core gap)

Memory Crystal only produces the vector DB today. It needs all three:

- [ ] **JSONL archive** — cc-hook copies raw JSONL to `~/.ldm/agents/{agent_id}/memory/transcripts/` after each capture. Solves the FDA backup problem. Gives Dream Weaver its primary input in a controlled location.

- [ ] **MD session summaries** — cc-hook generates human-readable markdown per conversation. Write to `~/.ldm/agents/{agent_id}/memory/sessions/YYYY-MM-DD-{slug}.md`. Matches OpenClaw's session-memory hook output but works independently.

- [ ] **crystal.db location** — Move or symlink crystal.db to `~/.ldm/memory/crystal.db` (shared, root level). Currently at `~/.openclaw/memory-crystal/`. The DB is shared by all agents (cc-mini, lesa-mini, cc-air), tagged by agent_id. On remote devices, a read-only mirror lives at the same path.

## Priority 2 — LDM Scaffolding (built into Memory Crystal)

Memory Crystal must set up `~/.ldm/` itself. No dependency on wip-ldm-os repo.

- [ ] **`crystal init` / auto-scaffold** — On first run, create the full directory structure:
  ```
  ~/.ldm/
  ├── config.json
  ├── memory/crystal.db                     (shared vector DB)
  └── agents/{agent_id}/memory/
      ├── transcripts/  sessions/  daily/  journals/
  ```
- [ ] **Agent names by machine:** `cc-mini`, `lesa-mini`, `cc-air` (set via `CRYSTAL_AGENT_ID`)
- [ ] **Absorb wip-ldm-os scaffolding** — Port relevant parts of `scaffold.sh` and templates into Memory Crystal's installer. Identity files (SOUL.md etc.) can be empty templates or skipped.
- [ ] **Config** — agent name, harness type, Dream Weaver schedule in `~/.ldm/agents/{agent_id}/config.json`

## Priority 3 — Deploy Ephemeral Relay + Expand Poller

See Parker's setup checklist at `ai/todos/parker/2026-02-25--cc-air--setup-checklist.md`.

- [ ] Generate encryption key + copy to both machines
- [ ] `wrangler login`, R2 bucket, bearer tokens, deploy
- [ ] Configure env vars, end-to-end test

**Poller expansion** — After decrypting relay data, the Mini-side poller must also reconstruct the remote agent's full file tree:
- [ ] Write JSONL to `~/.ldm/agents/{agent_id}/memory/transcripts/`
- [ ] Generate MD summary to `~/.ldm/agents/{agent_id}/memory/sessions/`
- [ ] Append daily breadcrumb to `~/.ldm/agents/{agent_id}/memory/daily/`
- [ ] This ensures the Mini has everything — if a device is lost, Dream Weaver can still run against that agent

## Priority 4 — Fix Broken Systems

- [ ] **Retire context-embeddings** — Once Crystal handles all three file types, disable in dot-openclaw. Update lesa-bridge to read from crystal.db.
- [ ] **LanceDB removal** — Remove dual-write once sqlite-vec is validated.
- [ ] **Backup system** — Partially solved by JSONL copy (Priority 1). Full fix: grant FDA or alternative.

## Priority 5 — Recovery & Backfill

- [ ] **`crystal replay`** — Re-send from raw JSONL through relay (recovery when Mini offline >24h).
- [ ] **`crystal backfill`** — One-time ingest of ~115 historical CC sessions (~110MB, ~$0.07).

## Priority 6 — Dream Weaver Integration

- [ ] **Dream Weaver reads from `~/.ldm/`** — Once JSONL copies live there, point Dream Weaver at `transcripts/` instead of `~/.claude/projects/`.
- [ ] **Trigger consolidation** — After poller ingests a batch, optionally trigger incremental Dream Weaver run.
- [ ] **Automate weekly schedule** — Currently manual. Add cron/launchd trigger.

## Priority 7 — Search Quality (QMD Phases 3–5)

- [ ] **Phase 3: Smart chunking + dedup** — Content-hash dedup, better non-conversation chunking.
- [ ] **Phase 4: Re-ranking + query expansion** — LLM re-ranking, synonym expansion.
- [ ] **Phase 5: Local embeddings** — Replace OpenAI with local GGUF model.

## Priority 8 — Behavioral / Process

- [ ] **SHARED-CONTEXT.md** — Warm-start file agents read on boot.
- [ ] **End-of-session handoffs** — Agent writes what-I-was-doing summary.
- [ ] **Search-before-acting** — Agents search crystal before starting new work.

## Notes

- **Agents are per-harness-instance, named by machine:** cc-mini, lesa-mini, cc-air, etc. Each is a separate "user" in LDM.
- **crystal.db is shared** at `~/.ldm/memory/crystal.db` — not inside any agent folder. All agents write to it (tagged by agent_id).
- **The Mini has everything.** Remote agents' file trees are reconstructed from relay data. Dream Weaver can run against any agent from the Mini.
- OpenClaw's builtin memory stays on — it evolves independently, doesn't hurt to run both.
- QMD is a separate system. Its search algorithms are already ported into Memory Crystal.
- Private mode is fully implemented across all 4 surfaces.
- The relay code is built and builds clean, just needs physical deployment.
- Memory Crystal has zero external repo dependencies for core function. OpenClaw, CC hook, relay, and Dream Weaver are optional integrations.

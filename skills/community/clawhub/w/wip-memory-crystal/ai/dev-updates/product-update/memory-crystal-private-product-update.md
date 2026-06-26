# Memory Crystal ... Product Update

What's new, how it works, how to test. Updated with every release.

---

## v0.7.29 (2026-03-20) ... Doc audit

**What:** SKILL.md and TECHNICAL.md updated: MLX setup as Option A, deep search params (intent/explain/candidates), log paths fixed, role clarification (Core + Node only, standalone removed).

**How to test:** Read SKILL.md and TECHNICAL.md. Verify they match `crystal --help` and `crystal search --help`.

---

## v0.7.28 (2026-03-19) ... Log paths to ~/.ldm/logs/

**What:** All cron and LaunchAgent logs moved from `/tmp/ldm-dev-tools/` to `~/.ldm/logs/`. macOS clears `/tmp/` on reboot, so logs were being lost.

**How to test:**
```bash
crontab -l | grep crystal-capture    # should show ~/.ldm/logs/ not /tmp/
ls ~/.ldm/logs/crystal-capture.log   # should exist and grow every minute
tail -5 ~/.ldm/logs/crystal-capture.log
```

---

## v0.7.27 (2026-03-18) ... Root SKILL.md + ldm install as primary path

**What:** Root-level SKILL.md added. `ldm install wipcomputer/memory-crystal` is now the primary install path. `.publish-skill.json` for auto-publishing to wip.computer.

**How to test:**
```bash
ldm install wipcomputer/memory-crystal --dry-run    # should detect and show interfaces
curl -s https://wip.computer/install/wip-memory-crystal.txt | head -5    # should return SKILL.md
```

---

## v0.7.23 (2026-03-13) ... MLX local LLM + Deep Search v2

**What:**
1. `crystal mlx setup` auto-installs Qwen2.5-3B on Apple Silicon
2. LaunchAgent on port 18791 for local LLM
3. Provider cascade: MLX > Ollama > OpenAI > Anthropic
4. `--intent` parameter for query disambiguation
5. `--explain` mode shows per-result scoring breakdown
6. `--candidates N` tunes rerank pool size
7. Persistent LLM cache (7-day TTL)

**How to test:**
```bash
# MLX setup (Apple Silicon only)
crystal mlx setup
crystal mlx status    # should show running on port 18791

# Deep search
crystal search "security" --intent "1Password"    # should steer toward 1Password context
crystal search "deployment" --explain              # should show FTS/Vec/RRF/Rerank scores
crystal search "recent work" --candidates 60       # larger rerank pool
```

---

## v0.7.22 (2026-03-13) ... Remove standalone role

**What:** Standalone role removed. Two roles only: Core (master database) and Node (mirror). Default is Core.

**How to test:**
```bash
crystal role    # should show "core" or "node", never "standalone"
```

---

## v0.7.19-v0.7.21 (2026-03-13) ... Interactive init + doctor fixes

**What:** `crystal init` now interactive: detects existing sessions, offers agent naming, guides through setup. Doctor reports false positives fixed.

**How to test:**
```bash
crystal init --dry-run    # should show what would be set up
crystal doctor            # should report accurate health
```

---

## v0.7.8-v0.7.18 (2026-03-11-13) ... Installer integration + capture fixes

**What:** Full `ldm install` integration. CC capture poller reliability fixes. Session export improvements. Daily backup LaunchAgent. Delta sync for file sources.

**How to test:**
```bash
crystal status                    # should show chunk counts, agent list, health
crystal sources status            # should show indexed directories
/usr/bin/sqlite3 ~/.ldm/memory/crystal.db "SELECT count(*) FROM chunks"    # total chunks
```

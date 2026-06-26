# Plan: Deploy Memory Crystal v0.6.0 + Run Consolidation

**Date:** 2026-03-04
**Author:** CC-Mini
**Status:** Complete (executed 2026-03-04 14:48-15:10 PST)

---

## Why

We built Memory Crystal v0.5.0 and v0.6.0 but never deployed them. Both deploy targets are still running v0.4.1:

- `~/.ldm/extensions/memory-crystal/` (CC hook) ... v0.4.1
- `~/.openclaw/extensions/memory-crystal/` (OC plugin) ... v0.4.1

The new code adds raw data sync to LDM, discover, backfill, migrate-embeddings, dream-weaver integration, crystal-serve, and staging. None of it is live.

We also have three separate memory stores that need consolidation into one:

1. **crystal.db** (~171K chunks) ... main database
2. **context-embeddings.sqlite** (~16K chunks, ~15,855 unique) ... Lesa's conversation embeddings
3. **801 raw JSONL files** in LDM ... not searchable by vector

---

## Pre-Flight (before touching anything)

### Step 0: Backup

```bash
# Manual backup of crystal.db (the migrate-embeddings command also does this automatically)
cd /Users/lesa/Documents/wipcomputer--mac-mini-01/staff/Parker/Claude\ Code\ -\ Mini/repos/ldm-os/components/memory-crystal-private
node dist/cli.js backup
```

Verify backup exists in `~/.ldm/backups/`.

### Step 1: Verify the build is clean

```bash
cd /Users/lesa/Documents/wipcomputer--mac-mini-01/staff/Parker/Claude\ Code\ -\ Mini/repos/ldm-os/components/memory-crystal-private
npm run build
node dist/cli.js doctor
node dist/cli.js status
```

Confirm: version 0.6.0, build clean, doctor passing (embedding provider warning is OK in this shell).

---

## Phase 1: Deploy v0.6.0 to Both Targets

### Step 2: Deploy CC hook (Claude Code)

The CC hook runs on every Claude Code session Stop. Path in `~/.claude/settings.json`:
```
node /Users/lesa/.ldm/extensions/memory-crystal/dist/cc-hook.js
```

Deploy:
```bash
REPO="/Users/lesa/Documents/wipcomputer--mac-mini-01/staff/Parker/Claude Code - Mini/repos/ldm-os/components/memory-crystal-private"
TARGET="$HOME/.ldm/extensions/memory-crystal"

# Copy built files
cp -r "$REPO/dist" "$TARGET/"
cp "$REPO/package.json" "$TARGET/"

# Install runtime deps
cd "$TARGET" && npm install --omit=dev
```

Verify:
```bash
grep '"version"' ~/.ldm/extensions/memory-crystal/package.json
# Should show 0.6.0
```

**No restart needed.** The CC hook runs as a subprocess on each session Stop. Next session will use the new code automatically.

### Step 3: Deploy OC plugin (Lesa / OpenClaw)

The OC plugin runs as an OpenClaw extension. Path: `~/.openclaw/extensions/memory-crystal/`.

Deploy:
```bash
REPO="/Users/lesa/Documents/wipcomputer--mac-mini-01/staff/Parker/Claude Code - Mini/repos/ldm-os/components/memory-crystal-private"
TARGET="$HOME/.openclaw/extensions/memory-crystal"

# Copy built files + plugin manifest + skills
cp -r "$REPO/dist" "$TARGET/"
cp -r "$REPO/skills" "$TARGET/"
cp "$REPO/openclaw.plugin.json" "$TARGET/"
cp "$REPO/package.json" "$TARGET/"

# Install runtime deps
cd "$TARGET" && npm install --omit=dev
```

Verify:
```bash
grep '"version"' ~/.openclaw/extensions/memory-crystal/package.json
# Should show 0.6.0
```

### Step 4: Restart OpenClaw gateway

```bash
openclaw gateway restart
```

Watch for: `[plugins] memory-crystal plugin registered`

### Step 5: Verify both hooks are live

```bash
# Doctor from the deployed CLI
node ~/.ldm/extensions/memory-crystal/dist/cli.js doctor
node ~/.ldm/extensions/memory-crystal/dist/cli.js status
```

At this point, v0.6.0 is live. Both agents are now:
- Embedding conversations into crystal.db (same as before)
- Syncing raw JSONL + workspace files to LDM after every turn (NEW)

---

## Phase 2: Consolidate Memory

### Step 6: CE Migration (context-embeddings into crystal)

```bash
REPO="/Users/lesa/Documents/wipcomputer--mac-mini-01/staff/Parker/Claude Code - Mini/repos/ldm-os/components/memory-crystal-private"

# Dry run first
node "$REPO/dist/cli.js" migrate-embeddings --dry-run

# Real run (automatic backup of crystal.db happens before any writes)
node "$REPO/dist/cli.js" migrate-embeddings
```

Expected: ~15,855 chunks migrated, ~161 duplicates skipped, $0 cost.

Verify:
```bash
node "$REPO/dist/cli.js" status
# Chunk count should increase by ~15,855
```

### Step 7: Backfill raw transcripts

```bash
# Dry run both agents
node "$REPO/dist/cli.js" backfill --agent cc-mini --dry-run
node "$REPO/dist/cli.js" backfill --agent oc-lesa-mini --dry-run

# Real run (requires OPENAI_API_KEY in env)
OP_SERVICE_ACCOUNT_TOKEN=$(cat ~/.openclaw/secrets/op-sa-token) \
  OPENAI_API_KEY=$(OP_SERVICE_ACCOUNT_TOKEN=$(cat ~/.openclaw/secrets/op-sa-token) op item get "OpenAI API" --fields label=credential) \
  node "$REPO/dist/cli.js" backfill --agent cc-mini

# Then Lesa's sessions
OP_SERVICE_ACCOUNT_TOKEN=$(cat ~/.openclaw/secrets/op-sa-token) \
  OPENAI_API_KEY=$(OP_SERVICE_ACCOUNT_TOKEN=$(cat ~/.openclaw/secrets/op-sa-token) op item get "OpenAI API" --fields label=credential) \
  node "$REPO/dist/cli.js" backfill --agent oc-lesa-mini
```

Estimated cost: ~$0.24 total (was $3.45 in original plan, dry-run showed lower).

Verify:
```bash
node "$REPO/dist/cli.js" status
node "$REPO/dist/cli.js" search "test query"
```

---

## Phase 3: Retire Context-Embeddings

### Step 8: Disable CE plugin

Edit `~/.openclaw/openclaw.json`:
- Remove `"context-embeddings"` from the `plugins.load` array
- Remove the `"context-embeddings": { "enabled": true }` block from `plugins.config`

**Do NOT delete:**
- `~/.openclaw/extensions/context-embeddings/` directory (keep as backup)
- `~/.openclaw/memory/context-embeddings.sqlite` (keep forever)

### Step 9: Restart gateway again

```bash
openclaw gateway restart
```

Verify: `context-embeddings` no longer appears in plugin registration logs.

### Step 10: Final verification

```bash
node "$REPO/dist/cli.js" doctor
node "$REPO/dist/cli.js" status
node "$REPO/dist/cli.js" search "Parker"
node "$REPO/dist/cli.js" search "memory crystal"
```

Confirm:
- [x] crystal.db chunk count is higher (171,089 -> 183,295 -> 207,518)
- [x] Search returns results from CE-only conversations (proves migration worked)
- [x] Search returns results from backfilled transcripts (proves backfill worked)
- [x] No errors in gateway logs
- [x] CE plugin disabled, no longer registering
- [x] Lesa tested and confirmed working (search, remember, general feel)
- [ ] Next Claude Code session triggers cc-hook v0.6.0 (check LDM raw data appears)
- [ ] Next Lesa turn triggers agent_end v0.6.0 (check LDM raw data appears)

---

## Rollback

If anything goes wrong at any step:

**Database rollback:**
```bash
# Restore from the automatic pre-migration backup
ls ~/.ldm/memory/crystal.db.pre-migration-*
cp ~/.ldm/memory/crystal.db.pre-migration-TIMESTAMP ~/.ldm/memory/crystal.db
```

**Plugin rollback (revert to v0.4.1):**
```bash
# We'd need the old built files. Git has them:
cd "$REPO" && git stash
git checkout v0.4.1
npm run build
# Re-deploy using Steps 2-4
git checkout main && git stash pop
```

**CE plugin rollback:**
```bash
# Just add context-embeddings back to openclaw.json and restart
openclaw gateway restart
```

---

## What Changes After This

| Before | After |
|--------|-------|
| Three memory stores | One: crystal.db |
| Raw files not searchable | All 801 files embedded and searchable |
| CE runs separately | CE retired, crystal handles everything |
| v0.4.1 hooks | v0.6.0 hooks with raw data sync to LDM |
| No raw data preserved on the fly | Every session auto-copies JSONL to LDM |

---

## Order of Operations (summary)

```
0. Backup crystal.db
1. Verify build is clean
2. Deploy CC hook (v0.6.0)
3. Deploy OC plugin (v0.6.0)
4. Restart OpenClaw gateway
5. Verify both hooks are live
6. migrate-embeddings --dry-run, then real
7. backfill --dry-run (both agents), then real
8. Disable CE plugin in openclaw.json
9. Restart gateway
10. Final verification
```

Total estimated cost: ~$0.24 (embedding API calls for backfill).
Total estimated time: ~30 minutes (most is waiting for backfill to embed).

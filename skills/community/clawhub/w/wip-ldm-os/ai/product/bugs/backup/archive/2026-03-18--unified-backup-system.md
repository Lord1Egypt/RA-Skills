# Plan: Unified Backup System + Workspace Setup

## Context

Two competing backup systems (361 GB + 20 GB). No coordination. Lesa's script backs up reinstallable code. LDM's script only covers ~/.ldm/. main.sqlite-wal not captured. 63 GB of temp files not cleaned. Backup template designed by Parker but not implemented.

Issues: #119 (unified backup), #117 (folder restructure)

## Architecture

### Workspace setup (ldm init)

`ldm init` creates the workspace at first run:

```
~/wipcomputer/                     <- workspace (org name, configurable)
  documents/                       <- human work product
  repos/                           <- git repos (optional)
  staff/                           <- per-user/agent files
```

Org name stored in `~/.ldm/config.json`:
```json
{
  "workspace": "~/wipcomputer",
  "org": "wipcomputer",
  "device": "mac-mini"
}
```

### Backup structure (Parker's template)

```
~/.ldm/backups/
  wipcomputer/                     <- org
    2026-03-18/                    <- date
      mac-mini/                    <- device
        lesa/                      <- macOS account
          ~/                       <- mirror of home dir
            .ldm/                  <- agent OS (data only)
              memory/crystal.db    <- sqlite3 .backup
              agents/              <- identity, journals, daily logs
              state/               <- config, version, registry
            .claude/               <- CC harness (data only)
              CLAUDE.md
              settings.json
              projects/            <- auto-memory
            .openclaw/             <- OC harness (data only)
              workspace/           <- SHARED-CONTEXT, daily logs
              memory/
                crystal.db         <- (symlink target, skip)
                context-embeddings.sqlite  <- sqlite3 .backup
                main.sqlite        <- sqlite3 .backup
              openclaw.json
            wipcomputer/
              documents/           <- work product only, not repos
```

### What gets backed up (data only)

| Source | Method | Size | Why |
|--------|--------|------|-----|
| ~/.ldm/memory/crystal.db | sqlite3 .backup | 1.5 GB | Irreplaceable memory |
| ~/.ldm/agents/ | cp -r | ~100 MB | Identity, journals, daily logs |
| ~/.ldm/state/ | cp -r | ~1 MB | Config, version, registry |
| ~/.openclaw/memory/main.sqlite | sqlite3 .backup | 21 GB | OC conversations |
| ~/.openclaw/memory/context-embeddings.sqlite | sqlite3 .backup | 128 MB | Embeddings |
| ~/.openclaw/workspace/ | tar | ~142 MB | Shared context, daily logs |
| ~/.openclaw/openclaw.json | cp | ~5 KB | OC config |
| ~/.claude/CLAUDE.md | cp | ~12 KB | CC config |
| ~/.claude/settings.json | cp | ~5 KB | CC settings |
| ~/.claude/projects/ | tar | ~931 MB | Auto-memory |
| ~/wipcomputer/documents/ | tar | varies | Work product |

**NOT backed up:** extensions, node_modules, dist/, repos (on GitHub), ~/.claude/cache, telemetry, sessions (captured by crystal)

### Estimated size per backup: ~25 GB (mostly main.sqlite)

7 days = ~175 GB. Down from 361 GB.

### iCloud offsite

After local backup completes, tar and copy to iCloud:

```
~/Library/Mobile Documents/com~apple~CloudDocs/wipcomputer-icloud/backups/
  wipcomputer-mac-mini-2026-03-18.tar.gz
```

One tar per device per day. Rotates to 7. iCloud syncs it across devices.

## Implementation

### Phase 1: ldm backup command

**File:** `wip-ldm-os-private/bin/ldm.js`

New command:

```bash
ldm backup                    # run backup now
ldm backup --dry-run          # show what would be backed up
ldm backup --include-secrets  # include ~/.ldm/secrets/
ldm backup --keep 14          # keep 14 days
```

The command:
1. Reads config for org, device, account
2. Creates date folder in template structure
3. sqlite3 .backup for each database
4. cp/tar for other files (excludes reinstallable)
5. Tars the dated folder
6. Copies tar to iCloud path (if configured)
7. Rotates old backups

**New file:** `wip-ldm-os-private/lib/backup.mjs`

Core backup logic. Separate from ldm.js so it can be tested and imported.

```javascript
export async function runBackup(options) {
  const config = loadConfig();
  const org = config.org || 'default';
  const device = config.device || os.hostname();
  const account = os.userInfo().username;
  const date = new Date().toISOString().split('T')[0];

  const backupDir = join(LDM_ROOT, 'backups', org, date, device, account, '~');

  // sqlite3 .backup for each database
  await backupSqlite(join(LDM_ROOT, 'memory', 'crystal.db'), join(backupDir, '.ldm', 'memory', 'crystal.db'));
  await backupSqlite(join(OC_ROOT, 'memory', 'main.sqlite'), join(backupDir, '.openclaw', 'memory', 'main.sqlite'));
  await backupSqlite(join(OC_ROOT, 'memory', 'context-embeddings.sqlite'), join(backupDir, '.openclaw', 'memory', 'context-embeddings.sqlite'));

  // cp/tar for other files
  copyDir(join(LDM_ROOT, 'agents'), join(backupDir, '.ldm', 'agents'));
  copyDir(join(LDM_ROOT, 'state'), join(backupDir, '.ldm', 'state'));
  // ... etc

  // Tar to iCloud
  if (config.icloudBackupPath) {
    const tarName = `${org}-${device}-${date}.tar.gz`;
    tar(backupDir, join(config.icloudBackupPath, tarName));
    rotate(config.icloudBackupPath, options.keep || 7);
  }

  // Rotate local
  rotate(join(LDM_ROOT, 'backups', org), options.keep || 7);
}
```

### Phase 2: ldm init creates workspace

**File:** `wip-ldm-os-private/bin/ldm.js`, in `cmdInit()`

After scaffolding ~/.ldm/, also create ~/wipcomputer/:

```javascript
// Ask org name (default: wipcomputer)
const orgName = process.stdin.isTTY
  ? await prompt('Workspace name', 'wipcomputer')
  : 'wipcomputer';

const workspace = join(HOME, orgName);
mkdirSync(join(workspace, 'documents'), { recursive: true });
mkdirSync(join(workspace, 'repos'), { recursive: true });
mkdirSync(join(workspace, 'staff'), { recursive: true });

// Save to config
config.workspace = workspace;
config.org = orgName;
config.device = os.hostname().replace(/\.local$/, '');
```

### Phase 3: Config for backup paths

**File:** `~/.ldm/config.json`

```json
{
  "workspace": "/Users/lesa/wipcomputer",
  "org": "wipcomputer",
  "device": "mac-mini",
  "backup": {
    "keep": 7,
    "icloudPath": "~/Library/Mobile Documents/com~apple~CloudDocs/wipcomputer-icloud/backups",
    "includeSecrets": false
  }
}
```

### Phase 4: LDM Dev Tools.app integration

Update `LDMDevTools.app/Resources/jobs/backup.sh` to call `ldm backup`:

```bash
#!/bin/bash
export PATH="/opt/homebrew/bin:$PATH"
ldm backup >> /tmp/ldm-dev-tools/backup.log 2>&1
```

Replaces both Lesa's script and the old LDM backup. One command.

### Phase 5: Retire old systems

1. Lesa's `daily-backup.sh` ... retire. `ldm backup` replaces it.
2. `~/.ldm/bin/ldm-backup.sh` ... retire. `ldm backup` replaces it.
3. LaunchAgent `ai.openclaw.ldm-backup.plist` ... update to call `ldm backup` or remove (Dev Tools handles scheduling).
4. Backup verify script ... update to check new structure.

### Phase 6: Temp file cleanup

Add to `ldm doctor`:
- Detect `~/.openclaw/memory/main.sqlite.tmp-*` files (currently 63 GB)
- `ldm doctor --fix` cleans them
- Log warning during backup if temp files exceed threshold

## Files to modify

| File | Change |
|------|--------|
| `wip-ldm-os-private/bin/ldm.js` | Add backup command, update init for workspace |
| `wip-ldm-os-private/lib/backup.mjs` | New file: core backup logic |
| `wip-ldm-os-private/lib/state.mjs` | Add backup status to system state |
| LDMDevTools.app/Resources/jobs/backup.sh | Call ldm backup |

## What does NOT change

- Crystal.db location (~/.ldm/memory/)
- Agent identity files (~/.ldm/agents/)
- OpenClaw config (~/.openclaw/)
- Claude Code config (~/.claude/)
- Extension deployment paths

## Verification

```bash
# Dry run
ldm backup --dry-run
# Shows: what would be backed up, estimated size, destination

# Real backup
ldm backup
# Creates: ~/.ldm/backups/wipcomputer/2026-03-18/mac-mini/lesa/~/
# Tars to: wipcomputer-icloud/backups/wipcomputer-mac-mini-2026-03-18.tar.gz

# Check
ls ~/.ldm/backups/wipcomputer/2026-03-18/mac-mini/lesa/~/
# .ldm/ .claude/ .openclaw/ wipcomputer/

# Verify iCloud
ls ~/Library/Mobile\ Documents/com~apple~CloudDocs/wipcomputer-icloud/backups/
# wipcomputer-mac-mini-2026-03-18.tar.gz

# Restore test (to /tmp/)
tar -xzf ~/Library/Mobile\ Documents/.../wipcomputer-mac-mini-2026-03-18.tar.gz -C /tmp/restore-test/
ls /tmp/restore-test/~/
# .ldm/ .claude/ .openclaw/ wipcomputer/
```

# Bug: npm link, accidental deploy, and v0.7.7 release mess

**Filed by:** CC-Mini on 2026-03-13
**Severity:** High. Production tool running from repo clone. Release includes unreleased code.

---

## What happened

A CC session on 2026-03-13 ran `wip-release patch` to release v0.7.7 with a README prompt update. But three things were wrong:

1. The global `crystal` binary was npm-linked to the private repo (since Mar 3). So bumping package.json in the repo instantly made the production tool v0.7.7. Release and deploy became the same action.

2. A separate CC session (memory-db-fix) had already merged PR #49 to main with significant code changes (DELETE trigger, `crystal cleanup` command, doctor embedding fix). These changes are now on main and in the npm-linked production tool, but v0.7.7's release notes only describe the README prompt update.

3. The CC session edited on main first, then tried to move changes to a branch after the fact. It also ran the full release pipeline when Parker said "merge and deploy" (probably meaning deploy to extensions, not publish to npm).

## Current state (broken)

| Thing | Status | Problem |
|-------|--------|---------|
| `/opt/homebrew/bin/crystal` | Symlinked to private repo via npm link | Runs from repo source, not published package |
| `/opt/homebrew/lib/node_modules/memory-crystal/` | Symlinked to private repo | Same. Any `git pull` changes the production tool |
| `~/.ldm/extensions/memory-crystal/` | v0.7.7 (files copied from repo by memory-db-fix session) | Has cleanup code that isn't in the v0.7.7 release notes |
| `~/.openclaw/extensions/memory-crystal/` | v0.7.7 (same as above) | Same |
| npm registry `memory-crystal@0.7.7` | Published | Only includes README prompt change, not cleanup code |
| GitHub release v0.7.7 | Published | Release notes only describe prompt change |
| Public repo `wipcomputer/memory-crystal` v0.7.7 | Deployed | Missing the cleanup code (deploy-public ran before PR #49 merged) |

## What needs to be fixed

### 1. Unlink the global crystal from the private repo

```bash
cd '/path/to/memory-crystal-private' && npm unlink
npm install -g memory-crystal
```

This makes the global crystal come from the published npm package, not the repo. After this, repo changes don't affect the production tool.

### 2. Release v0.7.8 with everything properly included

Main now has both the prompt update AND the cleanup code. Need a proper release:

```bash
cd memory-crystal-private && git checkout main && git pull
wip-release patch --notes="Add DELETE trigger for cascading chunk deletes, crystal cleanup command, fix doctor 1Password detection, update install prompt"
```

Then deploy to public:
```bash
bash deploy-public.sh /path/to/memory-crystal-private wipcomputer/memory-crystal
```

### 3. Verify installed extensions match the release

After v0.7.8:
```bash
# Rebuild from repo
npm run build

# Deploy to LDM extension
cp -r dist skills openclaw.plugin.json package.json ~/.ldm/extensions/memory-crystal/
cd ~/.ldm/extensions/memory-crystal && npm install --omit=dev

# Verify all three locations match
grep '"version"' ~/.ldm/extensions/memory-crystal/package.json
grep '"version"' ~/.openclaw/extensions/memory-crystal/package.json
crystal status
```

### 4. Verify the global crystal runs from npm, not the repo

```bash
ls -la $(which crystal)
# Should NOT point to a repo path
# Should point to /opt/homebrew/lib/node_modules/memory-crystal/dist/cli.js
# Where /opt/homebrew/lib/node_modules/memory-crystal/ is a real directory, not a symlink
```

### 5. Test everything

```bash
crystal status                    # should show correct version
crystal doctor                    # should detect 1Password, no false failures
crystal cleanup --dry-run         # should show 0 orphans (already cleaned)
crystal search "test"             # should return results
crystal init --dry-run            # should show current state
```

## How this happened

1. **Mar 3:** Someone ran `npm link` from the private repo during development. This was probably for testing the CLI changes locally. It should have been unlinked after testing.

2. **Mar 13 (session 1, memory-db-fix):** Merged PR #49 (DELETE trigger, cleanup command, doctor fix). Deployed to extensions via `cp`. Ran `npm link` again to update the CLI. This further entangled the repo and production.

3. **Mar 13 (session 2, the other CC):** Merged PR #48 (README prompt update). Ran `wip-release patch` creating v0.7.7. Because of npm link, the repo's package.json bump instantly made the production tool v0.7.7. Then ran `deploy-public.sh` which synced to the public repo.

## Root cause

Two rules were violated:
1. **Never run tools from repo clones.** npm link makes the global tool run from the repo. This is the #1 rule in CLAUDE.md.
2. **Release and deploy are separate steps.** The npm link collapsed them into one action.

## Prevention

- `crystal doctor` should check if the global binary is npm-linked to a repo and warn
- The Dev Guide should explicitly say: never `npm link` memory-crystal in production. Use it for testing, unlink immediately after.
- `wip-release` could check for npm links before publishing and refuse to proceed

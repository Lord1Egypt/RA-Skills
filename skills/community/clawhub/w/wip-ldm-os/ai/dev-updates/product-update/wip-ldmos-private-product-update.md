# LDM OS ... Product Update

What's new, how it works, how to test. Updated with every release.

---

## v0.4.37 (2026-03-20) ... TECHNICAL.md audit

**What:** Full CLI reference, installation system docs, operations docs added to TECHNICAL.md. Architecture diagram updated.

**How to test:** Read TECHNICAL.md. Verify it matches what `ldm --help` shows.

---

## v0.4.36 (2026-03-20) ... Prettier + .gitignore

**What:** `.prettierrc` config added. `npm run fmt` and `npm run fmt:check` scripts. `.gitignore` updated with dist/, node_modules/, worktree dirs. `prepublishOnly` hook ensures bridge builds before npm publish.

**How to test:**
```bash
npm run fmt:check     # should pass or show what needs formatting
cat .gitignore        # should include dist/, node_modules/, _worktrees/
```

---

## v0.4.35 (2026-03-20) ... Repo review quick fixes

**What:**
1. Hardcoded `/Users/lesa` path in bridge/core.ts replaced with `os.homedir()`
2. `engines: { node: ">=18" }` added to package.json
3. Shell `rm -rf` calls replaced with `fs.rmSync` in deploy.mjs
4. Debug logger created at `lib/log.mjs` (opt-in via `LDM_DEBUG=1`)
5. GitHub Actions CI pipeline (`.github/workflows/ci.yml`)

**How to test:**
```bash
LDM_DEBUG=1 ldm install --dry-run    # should show debug output to stderr
grep "homedir" src/bridge/core.ts    # should find os.homedir(), not /Users/lesa
```

---

## v0.4.34 (2026-03-19) ... Non-scoped packages + ghost dir rename

**What:** Update loop now checks ALL npm packages (not just @wipcomputer/ scoped). Ghost `ldm-install-*` dirs renamed to clean names. Tavily added to catalog.

**How to test:**
```bash
ldm install --dry-run    # should show tavily if behind, no ldm-install-* names
ls ~/.ldm/extensions/    # should not have any ldm-install-* dirs
```

---

## v0.4.33 (2026-03-19) ... Registry version tracking + ldm worktree

**What:**
1. After parent package update, registry version updated for ALL sub-tools (not just parent)
2. New `ldm worktree` command: `add`, `list`, `remove`, `clean`
3. Worktrees go in `_worktrees/<repo>--<branch>/`

**How to test:**
```bash
ldm worktree add cc-mini/test-feature    # should create _worktrees/<repo>--cc-mini--test-feature/
ldm worktree list                         # should show it
ldm worktree remove <path>               # should clean up
ldm install                               # then ldm install --dry-run should show "up to date"
```

---

## v0.4.32 (2026-03-19) ... Parent detection fix

**What:** Fixed bug where parent package detection skipped packages already checked by the extension loop.

**How to test:**
```bash
ldm install --dry-run    # should show "wip-ai-devops-toolbox" not "wip-release" for toolbox updates
```

---

## v0.4.31 (2026-03-19) ... Install detection: CLI, parent, ghost cleanup

**What:**
1. CLI self-update now in npmUpdates[] (shows in dry-run)
2. Parent packages (toolbox with registryMatches) detected and reported under parent name
3. Ghost -private and ldm-install- registry entries cleaned automatically

**How to test:**
```bash
ldm install --dry-run    # CLI update should appear if behind
                         # no -private or ldm-install- ghost entries
```

---

## v0.4.30 (2026-03-19) ... Installer: catalog lookup, private redirect, staging

**What:**
1. `ldm install xai-grok` now works (partial ID match, name match, registryMatches)
2. `ldm install wipcomputer/foo-private` auto-redirects to public repo
3. Install staging moved from `/tmp/` to `~/.ldm/tmp/`

**How to test:**
```bash
ldm install xai-grok --dry-run    # should resolve via catalog
ls ~/.ldm/tmp/                     # staging dir (empty after install)
```

---

## v0.4.29 (2026-03-18) ... Install: CLIs, catalog fallback, /tmp/ symlinks

**What:** Global CLIs detected and updated. Catalog fallback to package.json repository.url. /tmp/ symlink prevention. /tmp/ cleanup after install. `--help` flag on ldm install.

**How to test:**
```bash
ldm install --help    # should show usage
which crystal         # should not be a /tmp/ symlink
```

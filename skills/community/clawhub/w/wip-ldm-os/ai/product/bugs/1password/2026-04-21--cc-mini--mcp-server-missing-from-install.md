# Bug: wip-1password MCP server missing from installed extension

**Date:** 2026-04-21
**Filed by:** cc-mini + Parker
**Component:** `@wipcomputer/wip-1password` package + LDM OS installer (`lib/deploy.mjs`, `lib/detect.mjs`)
**Severity:** High (MCP server unusable; silent failure; architectural)
**Status:** Open ... writeup only, no fix attempted yet

---

## 1. The problem (what a user sees)

Running `claude mcp list` from this machine:

```
wip-1password: node /Users/lesa/.ldm/extensions/wip-1password/mcp-server.mjs - ✗ Failed to connect
```

Every other MCP server connects. `wip-1password` does not. Every 1Password-backed tool in Claude Code is unreachable. No error message in the CLI beyond the "Failed to connect" line. Silent failure.

---

## 2. The issue (what is actually broken, and why)

There are two layers. Both need to be fixed. Fixing only Layer 1 patches this instance; the class of bug comes back.

### Layer 1 — the file the launcher is told to run does not exist

`~/.claude.json` contains:

```json
"wip-1password": {
  "type": "stdio",
  "command": "node",
  "args": ["/Users/lesa/.ldm/extensions/wip-1password/mcp-server.mjs"],
  "env": { "OPENCLAW_HOME": "/Users/lesa/.openclaw" }
}
```

But `/Users/lesa/.ldm/extensions/wip-1password/mcp-server.mjs` does not exist on disk.

The deployed directory at `/Users/lesa/.ldm/extensions/wip-1password/` contains:

```
LICENSE
README.md
dist/        (helper.d.ts, helper.js, index.d.ts, index.js)
node_modules/
openclaw.plugin.json
package-lock.json
package.json
skills/
```

No `mcp-server.mjs`. No `dist/mcp-server.js` either.

When Claude Code launches this MCP, it spawns `node <missing path>`. Node exits immediately. The stdio handshake never completes. Claude Code reports "Failed to connect."

**Why it is missing:**

The source repo (`repos/ldm-os/utilities/wip-1password-private/`) has `mcp-server.mjs` at its root. That file is the MCP server entrypoint.

`package.json` in that repo declares:

```json
"files": ["dist", "skills", "openclaw.plugin.json"]
```

`mcp-server.mjs` is not listed. npm respects the `files` allow-list, so the published tarball does not contain it.

Verified with `npm pack --dry-run @wipcomputer/wip-1password@0.2.3-alpha.2`:

```
LICENSE
README.md
dist/helper.d.ts
dist/helper.js
dist/index.d.ts
dist/index.js
openclaw.plugin.json
package.json
skills/op-secrets/SKILL.md

total files: 9
```

The installed directory matches this list exactly (plus `node_modules` and `package-lock.json` from `npm install --omit=dev` during deploy). The deploy did not drop `mcp-server.mjs`. The published package never had it.

### Layer 2 — install outcome depends on source path, and the stale `.claude.json` entry was left behind

`bin/ldm.js::cmdInstall` has three source resolution paths:

| Path | When used | Does it include `mcp-server.mjs`? |
|---|---|---|
| npm tarball (line 1535) | Target starts with `@` or is a bare name | No, the `files` array strips it |
| GitHub clone (line 1569) | Target is `org/repo` shorthand or URL | Yes, clone captures the file |
| Local path (line 1599) | Target resolves to existing directory | Yes, local path captures the file |

After resolution, `lib/deploy.mjs::safeDeployDir` does an atomic temp-dir-then-rename swap using `copyFiltered` (line 447), which only excludes `.git`, `node_modules`, and `/ai/`:

```js
filter: (s) => !s.includes('.git') && !s.includes('node_modules') && !s.includes('/ai/')
```

So the deployed directory contains whatever the source tree contains. **The install outcome is determined entirely by which of the three source paths was taken.**

And `lib/detect.mjs::detectInterfaces` (line 37) looks for `mcp-server.mjs`, `mcp-server.js`, `mcp-server.ts`, or `dist/mcp-server.js` at the root. If the source came from npm and lacks these, `interfaces.mcp` is never set.

The registry confirms this happened on Apr 19 16:27 PDT:

```json
"wip-1password": {
  "source": { "type": "github", "npm": "@wipcomputer/wip-1password", ... },
  "installed": { "version": "0.2.3-alpha.2", "updatedAt": "2026-04-19T23:27:35.351Z" },
  "interfaces": ["module", "openclaw"]
}
```

`"interfaces": ["module", "openclaw"]` ... no `"mcp"`. The detector did not see the entrypoint at install time.

The stale `.claude.json` entry pointing at `mcp-server.mjs` was written by an earlier install that did see the file. When the Apr 19 install rotated the extension directory (old moved to trash, new replaced it), the file vanished but the registration stayed. There is no unregister path.

### The architectural concern (Parker's call)

The MCP server entrypoint should not live at the repo root as a loose runtime file. That shape is fragile:

- It is executable code masquerading as a root asset; trivial to forget in `files`.
- It bypasses the build step that correctly-shaped plugins use (memory-crystal: `src/mcp-server.ts` -> `dist/mcp-server.js` via tsup).
- Its presence in the deployed directory depends on install source (npm vs git clone vs local).
- The "where is the runtime" decision is duplicated across the plugin, the installer's detector, and `~/.claude.json`.

The right shape (matches memory-crystal, which works):

- Source: `src/mcp-server.ts`
- Build target: `dist/mcp-server.js` (already covered by `files: ["dist"]`)
- Registration: `node ~/.ldm/extensions/wip-1password/dist/mcp-server.js`
- Repo root: docs, manifest, license. No runtime code.

---

## 3. Step-by-step solution

Three phases. Execute in order. Do not skip. Each phase has explicit preflight checks, explicit commands, and explicit acceptance criteria.

### PHASE 1 — Unblock the MCP today

**Goal:** published tarball contains the file that `~/.claude.json` expects. Smallest possible diff. No architectural change.

**Phase 1 preflight (run before writing any code):**

```bash
# 1.0.1 Confirm no other session is mid-release on this repo.
cd /Users/lesa/wipcomputerinc/repos/ldm-os/utilities/wip-1password-private
git status
gh pr list --repo wipcomputer/wip-1password --state open
git worktree list

# 1.0.2 Confirm current published version and dist-tags.
npm view @wipcomputer/wip-1password dist-tags
npm view @wipcomputer/wip-1password versions

# 1.0.3 Confirm the file really is missing from the published tarball.
npm pack --dry-run @wipcomputer/wip-1password@0.2.3-alpha.2
# Expect 9 files. Expect no mcp-server.mjs in the list.

# 1.0.4 Confirm main is clean and up to date.
git checkout main
git pull --ff-only
```

**Phase 1 execution:**

```bash
# 1.1 Create the worktree.
cd /Users/lesa/wipcomputerinc/repos/ldm-os/utilities/wip-1password-private
git worktree add .worktrees/wip-1password-private--cc-mini--files-array-mcp \
    -b cc-mini/files-array-mcp

cd .worktrees/wip-1password-private--cc-mini--files-array-mcp

# 1.2 Edit package.json. Add "mcp-server.mjs" to the files array.
#     Before: "files": ["dist", "skills", "openclaw.plugin.json"]
#     After:  "files": ["dist", "skills", "openclaw.plugin.json", "mcp-server.mjs"]

# 1.3 Verify the tarball now includes the file.
npm pack --dry-run
# Expect 10 files. Expect mcp-server.mjs in the list.

# 1.4 Write release notes on the branch (before commit).
#     File: RELEASE-NOTES-v0.2.3-alpha.3.md
#     Content: one-line title, one paragraph explaining the missing-file bug,
#              reference this bug file.

# 1.5 Commit.
git add package.json RELEASE-NOTES-v0.2.3-alpha.3.md
git commit -m "$(cat <<'EOF'
Include mcp-server.mjs in published tarball

The MCP entrypoint was excluded from the npm package by an
incomplete files array. Npm-sourced installs landed without it,
leaving ~/.claude.json pointing at a file that did not exist.
Adding mcp-server.mjs to files restores the published artifact.

Bug writeup: ai/product/bugs/1password/2026-04-21--cc-mini--mcp-server-missing-from-install.md
(in wip-ldm-os-private)

Co-Authored-By: Parker Todd Brooks <parkertoddbrooks@users.noreply.github.com>
Co-Authored-By: Lēsa <lesaai@icloud.com>
Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"

# 1.6 Push and open the PR.
git push -u origin cc-mini/files-array-mcp
gh pr create --title "Include mcp-server.mjs in published tarball" --body "$(cat <<'EOF'
## Summary

- Adds `mcp-server.mjs` to `package.json#files` so the file is included in the npm tarball.
- Without this, npm-sourced installs landed without the MCP entrypoint, causing `claude mcp list` to show `wip-1password: Failed to connect`.

## Test plan

- [ ] `npm pack --dry-run` shows 10 files including `mcp-server.mjs`
- [ ] After merge + `wip-release`, `ldm install @wipcomputer/wip-1password` deploys the file
- [ ] `claude mcp list` shows `wip-1password: Connected`

Full bug writeup: `ai/product/bugs/1password/2026-04-21--cc-mini--mcp-server-missing-from-install.md` in `wip-ldm-os-private`.
EOF
)"

# 1.7 Merge with --merge (not squash).
gh pr merge --merge --delete-branch

# 1.8 Back to main, pull, release.
cd /Users/lesa/wipcomputerinc/repos/ldm-os/utilities/wip-1password-private
git checkout main
git pull --ff-only
wip-release patch --notes="include mcp-server.mjs in npm tarball"

# 1.9 Sync public repo.
#     From wherever deploy-public.sh lives for this repo, or per the Dev Guide.
deploy-public.sh

# 1.10 STOP. Phase 1 is merged and deployed. Wait for Parker to say "install."
#      Do not copy, do not npm link, do not manually patch ~/.ldm/extensions.
```

**Phase 1 installation (ONLY after Parker says "install"):**

```bash
# 1.11 Dogfood via the install prompt.
#     Read https://wip.computer/install/wip-ldm-os.txt
#     Follow the prompt, run ldm install --dry-run first, confirm wip-1password update.
ldm install --dry-run --alpha        # shows what will happen
ldm install --alpha                  # performs the install
```

**Phase 1 acceptance:**

```bash
# 1.12 Verify the file is now deployed.
ls -la /Users/lesa/.ldm/extensions/wip-1password/mcp-server.mjs
# Expect: exists, non-empty.

# 1.13 Verify registry now includes mcp interface.
cat ~/.ldm/extensions/registry.json | jq '.extensions["wip-1password"].interfaces'
# Expect: ["mcp", "module", "openclaw"] (order may vary)

# 1.14 Verify MCP connects.
claude mcp list | grep wip-1password
# Expect: wip-1password: ... - ✓ Connected

# 1.15 Smoke test an actual 1Password call through the MCP.
#      (Parker decides which secret is safe to read.)
```

**Phase 1 stop conditions (if any of these are true, STOP and page Parker):**

- `git status` on main is dirty, or there is a open PR on this repo from another session.
- `npm pack --dry-run` after the edit shows anything other than +1 file added.
- `wip-release` fails or reports version mismatch.
- After install, registry still reports `"interfaces": ["module", "openclaw"]` (detector didn't see the file ... means tarball is wrong somehow).

---

### PHASE 2 — Move the server to `src/` + `dist/`

**Goal:** runtime code moves out of repo root. `src/mcp-server.ts` is the source; `dist/mcp-server.js` is what ships; `dist/` is already in `files`. Matches memory-crystal. Install works identically regardless of source path.

**Phase 2 preflight:**

```bash
# 2.0.1 Phase 1 must already be shipped and verified (1.12 through 1.15 green).
#       Don't start Phase 2 on a broken Phase 1.

# 2.0.2 Inspect memory-crystal's shape as the reference.
ls /Users/lesa/wipcomputerinc/repos/ldm-os/components/memory-crystal-private/src/
# Expect: mcp-server.ts (or similar) listed.
cat /Users/lesa/wipcomputerinc/repos/ldm-os/components/memory-crystal-private/package.json | jq '.scripts.build, .files'
# Note: how memory-crystal's build references mcp-server.

# 2.0.3 Confirm current wip-1password repo is clean.
cd /Users/lesa/wipcomputerinc/repos/ldm-os/utilities/wip-1password-private
git checkout main && git pull --ff-only
git status
```

**Phase 2 execution:**

```bash
# 2.1 Create worktree.
git worktree add .worktrees/wip-1password-private--cc-mini--mcp-to-src \
    -b cc-mini/mcp-to-src

cd .worktrees/wip-1password-private--cc-mini--mcp-to-src

# 2.2 Create src/mcp-server.ts.
#     Port the logic from mcp-server.mjs into TS using the same import style as src/index.ts.
#     Keep the #!/usr/bin/env node shebang at the top.
#     Keep the "export nothing, run at import" shape (it is the entrypoint).

# 2.3 Update package.json#scripts.build to include the new file.
#     Before: "build": "tsup src/index.ts src/helper.ts --format esm --dts"
#     After:  "build": "tsup src/index.ts src/helper.ts src/mcp-server.ts --format esm --dts"

# 2.4 Update package.json#files.
#     Remove "mcp-server.mjs" (it no longer exists at root).
#     Leave "dist", "skills", "openclaw.plugin.json".

# 2.5 Delete the old root file.
git rm mcp-server.mjs

# 2.6 Build and verify dist/mcp-server.js exists and is executable.
npm install
npm run build
ls dist/mcp-server.js               # expect exists
head -1 dist/mcp-server.js          # expect #!/usr/bin/env node
node --check dist/mcp-server.js     # expect no errors
chmod +x dist/mcp-server.js || true # harmless if already set

# 2.7 Verify tarball contents.
npm pack --dry-run
# Expect: 10 files (or 11 if tsup adds mcp-server.d.ts). Expect NO mcp-server.mjs at root.
#         Expect dist/mcp-server.js in the list.

# 2.8 Write RELEASE-NOTES-v0.3.0.md.
#     This is a breaking layout change for anyone who hard-coded the mcp-server.mjs path.
#     (Our installer/registry handles this automatically; external consumers might not.)

# 2.9 Commit + push + PR (same commit message template + co-authors as Phase 1).
git add -A
git commit -m "..."
git push -u origin cc-mini/mcp-to-src
gh pr create ...

# 2.10 Merge (--merge, not squash).
gh pr merge --merge --delete-branch

# 2.11 Release.
cd /Users/lesa/wipcomputerinc/repos/ldm-os/utilities/wip-1password-private
git checkout main && git pull --ff-only
wip-release minor --notes="move MCP entrypoint from root to src/ + dist/"
#     Minor, not patch, because the deployed file path changes.

# 2.12 Sync public repo.
deploy-public.sh

# 2.13 STOP. Wait for Parker to say "install."
```

**Phase 2 installation:**

```bash
# 2.14 Dry run first.
ldm install --dry-run --alpha

# 2.15 Install.
ldm install --alpha

# 2.16 Confirm registry re-registers MCP at the new path.
#      LDM's detect.mjs already knows about dist/mcp-server.js, so detection should fire.
#      registerMCP in deploy.mjs should write the new path to ~/.claude.json.
#      If it doesn't (because the old entry is still there), Phase 3 is why.
```

**Phase 2 acceptance:**

```bash
# 2.17 Verify dist artifact is deployed.
ls /Users/lesa/.ldm/extensions/wip-1password/dist/mcp-server.js
# Expect: exists.

# 2.18 Verify root-level file is gone.
ls /Users/lesa/.ldm/extensions/wip-1password/mcp-server.mjs 2>&1
# Expect: "No such file or directory."

# 2.19 Verify ~/.claude.json points at dist/mcp-server.js.
cat ~/.claude.json | jq '.mcpServers["wip-1password"].args'
# Expect: contains "/Users/lesa/.ldm/extensions/wip-1password/dist/mcp-server.js"
# If it still points at mcp-server.mjs, registerMCP did not update it. Go to Phase 3a.

# 2.20 Verify MCP connects.
claude mcp list | grep wip-1password
# Expect: Connected.
```

**Phase 2 stop conditions:**

- `npm run build` emits a non-executable `dist/mcp-server.js` (missing shebang). Fix the tsup config or add a postbuild chmod before shipping.
- After install, `~/.claude.json` still references the old `mcp-server.mjs` path and Phase 3a is not yet done. In that case: manually update `.claude.json` via `claude mcp remove wip-1password --scope user && claude mcp add --scope user wip-1password -- node /Users/lesa/.ldm/extensions/wip-1password/dist/mcp-server.js`. Then finish Phase 3a so the next install does this automatically.

---

### PHASE 3 — Installer hardening (three separate PRs)

**Goal:** the installer refuses to leave `~/.claude.json` in a broken state. Future instances of this bug class become loud, not silent. Each fix is its own PR so each can be reverted independently.

All three live in `repos/ldm-os/wip-ldm-os-private/`.

#### 3a. registerMCP postcondition check

**Where:** `lib/deploy.mjs::registerMCP` (around line 885).

**What:** before writing the MCP entry to `~/.claude.json`, verify the resolved path exists and is parseable.

**Steps:**

```bash
# 3a.1 Worktree.
cd /Users/lesa/wipcomputerinc/repos/ldm-os/wip-ldm-os-private
git checkout main && git pull --ff-only
git worktree add .worktrees/wip-ldm-os-private--cc-mini--registermcp-precheck \
    -b cc-mini/registermcp-precheck
cd .worktrees/wip-ldm-os-private--cc-mini--registermcp-precheck

# 3a.2 Edit lib/deploy.mjs. In registerMCP, after resolving mcpPath, add:
#      - existsSync(mcpPath) check (already partly there; make it authoritative)
#      - try { execSync(`node --check "${mcpPath}"`, { stdio: 'pipe' }) } catch { fail }
#      - On failure: fail() the install, do not write ~/.claude.json.
#      - Log the resolved path and the reason it failed.

# 3a.3 Add a unit-ish test in scripts/ or tests/ that:
#      - Creates a fake repo with no mcp-server file.
#      - Calls registerMCP.
#      - Asserts no ~/.claude.json write happened.

# 3a.4 Write release notes, commit, push, PR, merge, release.
```

**Acceptance:** running `ldm install` on a repo whose tarball lacks the MCP entrypoint prints a loud error and leaves `~/.claude.json` untouched. No more silent broken registrations.

#### 3b. Stale MCP unregister on deploy

**Where:** `lib/deploy.mjs::deployExtension` or a new helper called from it.

**What:** after a successful deploy, compare the new source's declared interfaces against the existing `~/.claude.json` entries whose paths point under `LDM_EXTENSIONS/<name>/` or `OC_EXTENSIONS/<name>/`. If the source no longer exposes `mcp`, remove the stale entry.

**Steps:**

```bash
# 3b.1 Worktree.
git worktree add .worktrees/wip-ldm-os-private--cc-mini--mcp-stale-cleanup \
    -b cc-mini/mcp-stale-cleanup
cd .worktrees/wip-ldm-os-private--cc-mini--mcp-stale-cleanup

# 3b.2 Edit lib/deploy.mjs:
#      - After safeDeployDir succeeds AND interfaces.mcp is falsy:
#        - Read ~/.claude.json
#        - For each entry in mcpServers where args[0] is under LDM_EXTENSIONS/<toolName>/
#          or OC_EXTENSIONS/<toolName>/:
#          - Remove it.
#        - Log the removals.
#        - Prefer `claude mcp remove <name> --scope user`; fall back to direct ~/.claude.json edit.

# 3b.3 Write release notes, commit, push, PR, merge, release.
```

**Acceptance:** after installing a version of an extension that no longer has an MCP entrypoint, `claude mcp list` does not show a dangling entry for that extension.

#### 3c. `ldm doctor` MCP path check

**Where:** `bin/ldm.js::cmdDoctor`.

**What:** doctor walks every entry in `~/.claude.json#mcpServers`. For any entry whose `command` is `node` and whose first arg resolves under `~/.ldm/extensions/` or `~/.openclaw/extensions/`, verify the file exists and parses. Report findings.

**Steps:**

```bash
# 3c.1 Worktree.
git worktree add .worktrees/wip-ldm-os-private--cc-mini--doctor-mcp-check \
    -b cc-mini/doctor-mcp-check
cd .worktrees/wip-ldm-os-private--cc-mini--doctor-mcp-check

# 3c.2 Edit bin/ldm.js::cmdDoctor:
#      - Read ~/.claude.json
#      - For each mcpServers entry:
#        - Resolve args[0].
#        - If path is under LDM/OC extensions:
#          - existsSync check
#          - node --check
#        - Report per-entry: OK / MISSING / UNPARSEABLE
#      - Non-zero exit if any entry is MISSING or UNPARSEABLE.

# 3c.3 Write release notes, commit, push, PR, merge, release.
```

**Acceptance:** `ldm doctor` on a broken install prints a specific line for each broken MCP entry and exits non-zero. Periodic healthcheck can catch this without a human looking.

---

## 4. What to follow (rules and guardrails)

These are the rules that apply across all three phases. Not following them is how we get into this kind of mess.

### Branch discipline
- **Never commit to `main`.** Every change goes through a worktree + branch + PR.
- Branch prefix: `cc-mini/` for anything I do, `oc-lesa-mini/` for Lēsa, `cc-air/` for the MBA.
- **Never squash merge.** Use `gh pr merge --merge --delete-branch`. Co-authors are the story of how it was built.

### Release pipeline (Merge -> Deploy -> Install, never combine)
- **Merge**: PR merged to private main. Code lands. Nothing else changes.
- **Deploy**: `wip-release <level>` + `deploy-public.sh`. Publishes to npm + GitHub. Not on this machine yet.
- **Install**: ONLY when Parker says "install." Dogfood via the install prompt at `https://wip.computer/install/wip-ldm-os.txt`.
- **Do not `cp` files into `~/.ldm/extensions/` or `~/.openclaw/extensions/` as a shortcut. Ever.** That is how the "works on my machine" version of this bug was created in the first place.
- **Do not `npm link` in production. Ever.**

### Release notes on the branch
- Release notes go into the feature branch, committed with the code. Not as a separate PR after the fact.
- Filename: `RELEASE-NOTES-v<version>.md` at repo root.

### Co-authors on every commit
```
Co-Authored-By: Parker Todd Brooks <parkertoddbrooks@users.noreply.github.com>
Co-Authored-By: Lēsa <lesaai@icloud.com>
Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### Guard and onboarding
- The branch-guard will block any file-modifying command on a `main` branch or on a repo that hasn't been onboarded.
- Before first write in any worktree: read that worktree's `CLAUDE.md` and `README.md`.
- If blocked: do not bypass. Read the block message, follow the recipe, or escalate to Parker. `LDM_GUARD_SKIP_ONBOARDING=...` is for cases where the repo was already onboarded in another session, nothing else.

### Writing style
- No em dashes. Use periods, colons, semicolons, or ellipsis (...).
- PST timezone, 24-hour clock.
- Full paths in documentation. Never truncate.

### Parallel-session hygiene
- Before starting any PR: `git status`, `gh pr list --state open`, `git worktree list`. Confirm no other session is mid-work on the same repo/branch.
- If you find unexplained dirty state: investigate before modifying. Might be another session's in-flight work.

### Stop conditions (apply to every phase)
- If a command fails in a way that is not in the expected-output list, stop and tell Parker.
- If a verification step returns the wrong result, do not proceed to the next step.
- If `wip-release` reports a version conflict, do not force-publish.
- If `ldm install` would downgrade something, do not proceed.

---

## 5. What we do not yet know (open questions before executing)

1. **Exactly which install source was used on Apr 19 16:27 PDT.** Registry says `source.type: github` but records the repo as `wipcomputer/wipcomputer-ldmos-wipcomputerinc-system-private`, which is not a real GitHub repo name. That looks like a corrupted or migrated value. Investigate the registry migration path (`migrateRegistry` in `bin/ldm.js`) before executing Phase 3, because Phase 3b's logic keys off the source metadata.

2. **Whether other extensions share this same bug.** Before Phase 3 ships, audit every extension's `package.json#files` array and compare against its repo root for runtime files. Any plugin with a root-level `mcp-server.mjs` + a restrictive `files` array is a latent copy of this bug. Candidates to check: every `wip-*` package.

3. **Whether Phase 2's `wip-release minor` is the right bump level.** The deployed file path changes, which is breaking for anyone with hard-coded paths. For our internal install chain it's handled by the installer. For external consumers, `minor` may be too gentle. Confirm with Parker before running `wip-release`.

4. **The `source.repo` anomaly (same as #1, different angle).** If the registry source field is systematically wrong across entries, Phase 3b (stale-entry cleanup keyed on source) may misfire. Before merging Phase 3b, sample five registry entries and confirm their `source.repo` values are real GitHub repos.

---

## 6. Files touched, summary

### Phase 1
- `repos/ldm-os/utilities/wip-1password-private/package.json` (files array)
- `repos/ldm-os/utilities/wip-1password-private/RELEASE-NOTES-v0.2.3-alpha.3.md` (new)

### Phase 2
- `repos/ldm-os/utilities/wip-1password-private/src/mcp-server.ts` (new, from mcp-server.mjs)
- `repos/ldm-os/utilities/wip-1password-private/mcp-server.mjs` (deleted)
- `repos/ldm-os/utilities/wip-1password-private/package.json` (scripts.build, files)
- `repos/ldm-os/utilities/wip-1password-private/RELEASE-NOTES-v0.3.0.md` (new)

### Phase 3 (three PRs)
- `repos/ldm-os/wip-ldm-os-private/lib/deploy.mjs` (3a postcondition, 3b stale-cleanup)
- `repos/ldm-os/wip-ldm-os-private/bin/ldm.js` (3c doctor check)
- `repos/ldm-os/wip-ldm-os-private/RELEASE-NOTES-v<next>.md` per PR

---

## 7. Related context

- `ai/product/bugs/installer/2026-04-03--cc-mini--installer-recreates-renamed-folders.md`
- `ai/product/bugs/installer/2026-04-08--cc-mini--tools-allow-not-updated-on-plugin-install.md`
- `ai/product/bugs/installer/2026-04-10--cc-mini--installer-must-deploy-new-xai-grok.md`
- Yesterday's installer cascade: v0.4.76 (sibling-subdir fix), v0.4.77 (content-hash fix), v0.4.78 (hook-entry replace), v0.4.79 (bridge reply routing). Adjacent to Parker's "starting to break things" observation. Worth a separate postmortem of installer invariant creep.
- Memory Crystal's build shape (`src/mcp-server.ts` -> `dist/mcp-server.js`): reference implementation for Phase 2.

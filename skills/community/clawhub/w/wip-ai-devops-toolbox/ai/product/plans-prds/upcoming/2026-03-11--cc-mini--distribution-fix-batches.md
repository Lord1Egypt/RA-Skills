# Distribution Fix: 4 Batches

**Date:** 2026-03-11
**Author:** CC Mini
**Status:** Ready to execute

---

## Batch 1: Fix what's broken now

**Issues:** #96, #110
**Branch:** `cc-mini/fix-install-bugs`
**Effort:** Small. Mostly file permissions and one code change.

### #96: CLI binaries not executable after wip-install

Three sub-problems:

**A. Files missing executable bit (wip-license-guard, wip-readme-format)**

The bin target files are `-rw-r--r--` instead of `-rwxr-xr-x`. npm should set +x during `npm install -g .` but git doesn't track the executable bit unless explicitly set.

Fix: In each tool's repo, set the executable bit on the bin entry file:
```bash
git update-index --chmod=+x cli.mjs      # wip-license-guard
git update-index --chmod=+x format.mjs    # wip-readme-format
```

Or: have the installer run `chmod +x` after `npm install -g .` as a post-install step in `install.js`:
```javascript
// After npm install -g, ensure bin files are executable
for (const bin of binNames) {
  const binPath = join(npmPrefix, 'bin', bin);
  try { chmodSync(binPath, 0o755); } catch {}
}
```

Both fixes should be applied. Git fix for correctness. Installer fix as a safety net.

**B. wip-license-hook missing dist/ (TypeScript not built)**

The package.json bin points to `dist/cli/index.js` but only `src/` is in the installed package. The build step never runs.

Fix options:
1. Add `"prepare": "tsc"` to package.json so npm builds before install
2. Or ship pre-built `dist/` in the repo (commit the build output)
3. Or have the installer detect TypeScript and run `npm run build` before `npm install -g`

Option 2 is simplest. Commit dist/ to the repo. The installer doesn't need to know about TypeScript.

**C. wip-repo-init has no package.json**

The `ai-dir-template` tool is detected as CLI but has no package.json with a bin field.

Fix: Add a package.json:
```json
{
  "name": "@wipcomputer/wip-repo-init",
  "version": "1.0.0",
  "bin": { "wip-repo-init": "./init.mjs" },
  "description": "Scaffold the standard ai/ directory structure in any repo"
}
```

Create `init.mjs` as the CLI entry point that wraps the existing template logic.

### #110: wip-install can't clone private repos

The installer uses HTTPS clone which fails on private repos (no auth).

Fix in `install.js`: detect if the repo is private or if HTTPS fails, fall back to SSH:
```javascript
// Try HTTPS first, fall back to SSH
const httpsUrl = `https://github.com/${repo}.git`;
const sshUrl = `git@github.com:${repo}.git`;
try {
  execSync(`git clone "${httpsUrl}" "${dest}"`, { stdio: 'pipe' });
} catch {
  execSync(`git clone "${sshUrl}" "${dest}"`, { stdio: 'pipe' });
}
```

Or: just always use SSH since this system has SSH keys configured. But HTTPS-first with SSH fallback is more portable.

### Verification

After fixes:
```bash
wip-install wipcomputer/wip-ai-devops-toolbox
which wip-license-guard    # should work
which wip-readme-format    # should work
which wip-license-hook     # should work
which wip-repo-init        # should work
wip-install wipcomputer/wip-1password-private  # should clone via SSH
```

---

## Batch 2: Spec compliance

**Issues:** #107, #108
**Branch:** `cc-mini/skill-spec-compliance`
**Effort:** Medium. Every SKILL.md in the toolbox gets updated.
**Depends on:** Nothing (can run in parallel with Batch 1)

### #107: SKILL.md files don't conform to agentskills.io spec

For every tool's SKILL.md:

1. Change `name` to lowercase-hyphen format matching directory name
   - "Release Pipeline" -> "wip-release"
   - "Identity File Protection" -> "wip-file-guard"
   - etc.

2. Move display names to `metadata.display-name`:
   ```yaml
   metadata:
     display-name: "Release Pipeline"
   ```

3. Move `version`, `homepage`, `author` into `metadata`:
   ```yaml
   metadata:
     display-name: "Release Pipeline"
     version: "1.9.1"
     homepage: "https://github.com/wipcomputer/wip-release"
     author: "Parker Todd Brooks"
   ```

4. Add `license` field:
   ```yaml
   license: MIT
   ```

5. Add `compatibility` field where needed:
   ```yaml
   compatibility: Requires git, npm, gh. Node.js 18+.
   ```

6. Rename `ai-dir-template` directory to `wip-repo-init` (name must match directory)

### #108: OpenClaw metadata gating

Add `metadata.openclaw` blocks to every SKILL.md:

```yaml
metadata:
  openclaw:
    requires:
      bins: [git, npm, gh]
    install:
      - id: node
        kind: node
        package: "@wipcomputer/wip-release"
        bins: [wip-release]
        label: "Install via npm"
    emoji: "🚀"
```

### Verification

```bash
# If skills-ref is available:
skills-ref validate ./tools/wip-release/
skills-ref validate ./tools/wip-file-guard/
# etc.
```

---

## Batch 3: Fix the distribution pipeline

**Issues:** #100, #97, #104, #111
**Branch:** `cc-mini/fix-distribution-pipeline`
**Effort:** Large. Core changes to wip-release and deploy-public.
**Depends on:** Batch 2 (spec-compliant SKILL.md needed for ClawHub)

### #100: deploy-public.sh runs npm publish

After the GitHub release step in deploy-public.sh:

```bash
# Publish to npm from public repo
if [ -f "$PUBLIC_CLONE/package.json" ]; then
  PRIVATE=$(node -e "console.log(require('$PUBLIC_CLONE/package.json').private || false)")
  if [ "$PRIVATE" != "true" ]; then
    echo "Publishing to npm..."
    NPM_TOKEN=$(OP_SERVICE_ACCOUNT_TOKEN=$(cat ~/.openclaw/secrets/op-sa-token) \
      op item get "npm Token" --vault "Agent Secrets" --fields label=password --reveal)
    cd "$PUBLIC_CLONE"
    echo "//registry.npmjs.org/:_authToken=${NPM_TOKEN}" > .npmrc
    npm publish --access public
    rm -f .npmrc
    echo "  ✓ Published to npm"
  fi
fi
```

For toolbox repos with sub-tools, iterate `tools/*/package.json` and publish each.

### #97: ClawHub publishes all sub-tool skills

In `core.mjs`, update `publishClawHub()` and step 9:

```javascript
// 9. ClawHub skill publish
const rootSkill = join(repoPath, 'SKILL.md');
const toolsDir = join(repoPath, 'tools');

// Publish root SKILL.md if it exists
if (existsSync(rootSkill)) {
  publishClawHub(repoPath, newVersion, notes);
}

// Publish each sub-tool SKILL.md
if (existsSync(toolsDir)) {
  for (const tool of readdirSync(toolsDir)) {
    const toolSkill = join(toolsDir, tool, 'SKILL.md');
    if (existsSync(toolSkill)) {
      publishClawHub(join(toolsDir, tool), newVersion, notes);
    }
  }
}
```

Update `detectSkillSlug()` to handle sub-tool paths correctly.

### #104: Distribution summary

Collect all publish results into a summary object. Print at end of release:

```javascript
const distResults = [];
// ... each publish step pushes { target, status, detail }

// Print summary
console.log('\n  Distribution:');
for (const r of distResults) {
  const icon = r.status === 'ok' ? '✓' : '✗';
  console.log(`    ${icon} ${r.target}: ${r.detail}`);
}
const failed = distResults.filter(r => r.status !== 'ok');
if (failed.length > 0) {
  console.log(`\n  ! ${failed.length} of ${distResults.length} targets failed.`);
}
```

### #111: GitHub Pages publish step

New step 10 in the release pipeline. Clones wip-homepage, copies SKILL.md files, updates llms.txt, commits, pushes.

This is the most complex new step. May want to extract it into a helper script that wip-release calls, rather than inline in core.mjs.

### Verification

```bash
# Dry run shows all distribution targets
wip-release patch --dry-run

# Real release hits all targets
wip-release patch --notes-file=RELEASE-NOTES-v1-9-2.md
# Should see:
#   ✓ npm: @wipcomputer/wip-release@1.9.2
#   ✓ ClawHub: wip-release@1.9.2
#   ✓ GitHub: v1.9.2
#   ✓ GitHub Pages: skills/wip-release updated
```

---

## Batch 4: Catch up (run the fixed pipeline on everything)

**Issues:** #98, #101, #102, #103, #105, #106, #109
**Effort:** Small per issue. Just running the now-fixed tools.
**Depends on:** Batches 1-3

### Execution order

1. Run `wip-release` on devops toolbox to publish v1.9.2 (with all pipeline fixes)
2. Run `deploy-public.sh` (now includes npm publish) -> fixes #102 (stale npm)
3. Verify all 13 tools on npm -> fixes #101
4. Verify GitHub Packages -> fixes #103
5. Re-publish all skills to ClawHub (spec-compliant now) -> fixes #109
6. SKILL.md ClawHub column deployed to public via deploy-public -> fixes #105
7. `npm uninstall -g @wipcomputer/universal-installer && npm install -g @wipcomputer/universal-installer` -> fixes #106
8. Add ClawHub as 7th interface in installer -> fixes #98

### Verification

```bash
# Everything installed, everything published
wip-install wipcomputer/wip-ai-devops-toolbox --dry-run
# Should show 7 interfaces per tool including ClawHub

# Every tool findable
which wip-release wip-install wip-repos wip-license-hook wip-license-guard wip-file-guard wip-repo-init wip-readme-format

# npm current
npm view @wipcomputer/wip-release version  # should be 1.9.2

# ClawHub current
clawhub inspect wip-release  # should show 1.9.2
```

---

## Summary

| Batch | Issues | Effort | Depends on |
|-------|--------|--------|------------|
| 1. Fix install bugs | #96, #110 | Small | Nothing |
| 2. Spec compliance | #107, #108 | Medium | Nothing |
| 3. Fix distribution pipeline | #97, #100, #104, #111 | Large | Batch 2 |
| 4. Catch up | #98, #101-103, #105-106, #109 | Small (per issue) | Batches 1-3 |

Estimated: 3-4 sessions to complete all four batches.

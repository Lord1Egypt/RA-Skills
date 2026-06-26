###### WIP Computer
# wip-release ... Reference

Detailed usage, pipeline steps, flags, auth, and module API.

## Release Tracks

Four release tracks, each with different behavior:

| Track | npm tag | Public code sync | Public release notes | Default notes |
|-------|---------|-----------------|---------------------|---------------|
| Alpha | @alpha | No | No (opt in with --release-notes) | Silent |
| Beta | @beta | No | Yes, prerelease (opt out with --no-release-notes) | Visible |
| Hotfix | @latest | No | Yes (opt out with --no-release-notes) | Visible |
| Stable | @latest | Yes, full deploy-public | Yes, full notes | Full deploy |

### Version numbering

- Alpha: `1.9.68-alpha.1`, `1.9.68-alpha.2` (increments on repeat)
- Beta: `1.9.68-beta.1`, `1.9.68-beta.2` (increments on repeat)
- Hotfix: normal patch bump (`1.9.67` -> `1.9.68`)
- Stable: normal bump (patch/minor/major)

## Usage

Run from inside any repo:

```bash
# Stable (existing behavior)
wip-release patch                    # 1.0.0 -> 1.0.1
wip-release minor                    # 1.0.0 -> 1.1.0
wip-release major                    # 1.0.0 -> 2.0.0

# Alpha
wip-release alpha                    # 1.0.1-alpha.1 (npm @alpha, silent)
wip-release alpha --release-notes    # 1.0.1-alpha.1 (npm @alpha + prerelease on public)

# Beta
wip-release beta                     # 1.0.1-beta.1 (npm @beta + prerelease on public)
wip-release beta --no-release-notes  # 1.0.1-beta.1 (npm @beta, skip notes)

# Hotfix
wip-release hotfix                   # 1.0.0 -> 1.0.1 (npm @latest + release on public)
wip-release hotfix --no-release-notes  # skip public release notes

# Common flags
wip-release patch --notes="fix auth config"   # with changelog note
wip-release minor --dry-run                    # preview, no changes
wip-release patch --no-publish                 # bump + tag only
```

## What It Does

### Stable pipeline

```
  wip-grok: 1.0.0 -> 1.0.1 (patch)
  ────────────────────────────────────────
  ✓ package.json -> 1.0.1
  ✓ SKILL.md -> 1.0.1
  ✓ CHANGELOG.md updated
  ✓ Committed and tagged v1.0.1
  ✓ Pushed to remote
  ✓ Published to npm
  - GitHub Packages: handled by deploy-public.sh
  ✓ GitHub release v1.0.1 created
  ✓ Published to ClawHub

  Done. wip-grok v1.0.1 released.
```

### Alpha/beta pipeline

```
  wip-grok: 1.0.0 -> 1.0.1-alpha.1 (alpha)
  ────────────────────────────────────────
  ✓ package.json -> 1.0.1-alpha.1
  ✓ CHANGELOG.md updated
  ✓ Committed and tagged v1.0.1-alpha.1
  ✓ Pushed to remote
  ✓ Published to npm @alpha
  - GitHub prerelease: skipped (silent alpha)

  Done. wip-grok v1.0.1-alpha.1 (alpha) released.
```

### Hotfix pipeline

```
  wip-grok: 1.0.0 -> 1.0.1 (hotfix)
  ────────────────────────────────────────
  ✓ package.json -> 1.0.1
  ✓ SKILL.md -> 1.0.1
  ✓ CHANGELOG.md updated
  ✓ Committed and tagged v1.0.1
  ✓ Pushed to remote
  ✓ Published to npm @latest
  ✓ GitHub release v1.0.1 created on public repo
  - deploy-public: skipped (hotfix)

  Done. wip-grok v1.0.1 (hotfix) released.
```

## Pipeline Steps

### Stable (patch/minor/major)

1. **Bump `package.json`** ... patch, minor, or major
2. **Sync `SKILL.md`** ... updates version in YAML frontmatter (if file exists)
3. **Update `CHANGELOG.md`** ... prepends new version entry with date and notes
4. **Git commit + tag** ... commits changed files, creates `vX.Y.Z` tag
5. **Push** ... pushes commit and tag to remote
6. **npm publish** ... publishes to npmjs.com with @latest (auth via 1Password)
7. **GitHub Packages** ... handled by deploy-public.sh
8. **GitHub release** ... creates release on private repo with changelog notes
9. **ClawHub publish** ... publishes skill to ClawHub (if SKILL.md exists)
10. **Branch cleanup** ... renames/prunes merged branches
11. **Worktree cleanup** ... prunes merged worktrees

### Alpha/Beta

1. **Bump `package.json`** ... adds prerelease suffix (-alpha.N / -beta.N)
2. **Update `CHANGELOG.md`** ... lightweight prerelease entry
3. **Git commit + tag** ... commits changed files, creates tag
4. **Push** ... pushes commit and tag to remote
5. **npm publish** ... publishes with --tag alpha or --tag beta
6. **GitHub prerelease** ... (beta: on by default, alpha: opt-in with --release-notes)

### Hotfix

1. **Bump `package.json`** ... patch bump (no suffix)
2. **Sync `SKILL.md`** ... updates version in YAML frontmatter
3. **Update `CHANGELOG.md`** ... prepends new version entry
4. **Git commit + tag** ... commits changed files, creates tag
5. **Push** ... pushes commit and tag to remote
6. **npm publish** ... publishes with --tag latest
7. **GitHub release** ... creates release on public repo (opt out with --no-release-notes)
8. **ClawHub publish** ... publishes skill to ClawHub (if SKILL.md exists)
9. **No deploy-public** ... code sync is skipped

## Flags

| Flag | What |
|------|------|
| `--notes="text"` | Changelog entry text |
| `--notes-file=path` | Read release narrative from a markdown file |
| `--release-notes` | Opt in to public release notes (alpha only) |
| `--no-release-notes` | Opt out of public release notes (beta, hotfix) |
| `--dry-run` | Show what would happen, change nothing |
| `--no-publish` | Bump + tag only, skip npm and GitHub release |
| `--skip-product-check` | Skip product docs gate (stable only) |
| `--skip-stale-check` | Skip stale remote branch check (stable only) |
| `--skip-worktree-check` | Skip worktree guard |
| `--skip-tech-docs-check` | Skip technical docs check (stable only) |
| `--skip-coverage-check` | Skip interface coverage check (stable only) |

## Auth

npm token is fetched from 1Password at publish time. No `.npmrc` files stored. No credentials in repos.

Requires:
- `op` CLI installed and configured
- 1Password SA token at `~/.openclaw/secrets/op-sa-token`
- "npm Token" item in "Agent Secrets" vault
- `gh` CLI authenticated (for GitHub Packages and releases)
- `clawhub` CLI authenticated (for ClawHub skill publishing)

## ldm install Integration

The installer checks different npm tags based on the track:

```bash
ldm install             # checks @latest (stable + hotfix)
ldm install --beta      # checks @beta tag
ldm install --alpha     # checks @alpha tag
```

## As a Module

```javascript
import { release, releasePrerelease, releaseHotfix, detectCurrentVersion, bumpSemver, bumpPrerelease } from '@wipcomputer/wip-release';

const current = detectCurrentVersion('/path/to/repo');
const next = bumpSemver(current, 'minor');
console.log(`${current} -> ${next}`);

// Stable release
await release({
  repoPath: '/path/to/repo',
  level: 'patch',
  notes: 'fix auth',
  dryRun: false,
  noPublish: false,
});

// Alpha prerelease
await releasePrerelease({
  repoPath: '/path/to/repo',
  track: 'alpha',
  notes: 'testing new feature',
  dryRun: false,
  noPublish: false,
  publishReleaseNotes: false,
});

// Beta prerelease
await releasePrerelease({
  repoPath: '/path/to/repo',
  track: 'beta',
  notes: 'beta candidate',
  dryRun: false,
  noPublish: false,
  publishReleaseNotes: true,
});

// Hotfix
await releaseHotfix({
  repoPath: '/path/to/repo',
  notes: 'critical fix',
  dryRun: false,
  noPublish: false,
  publishReleaseNotes: true,
});
```

## Exports

| Function | What |
|----------|------|
| `release({ repoPath, level, notes, dryRun, noPublish })` | Full stable pipeline |
| `releasePrerelease({ repoPath, track, notes, dryRun, noPublish, publishReleaseNotes })` | Alpha/beta pipeline |
| `releaseHotfix({ repoPath, notes, dryRun, noPublish, publishReleaseNotes })` | Hotfix pipeline |
| `detectCurrentVersion(repoPath)` | Read version from package.json |
| `bumpSemver(version, level)` | Bump a semver string (patch/minor/major) |
| `bumpPrerelease(version, track)` | Bump a prerelease version (alpha/beta) |
| `syncSkillVersion(repoPath, newVersion)` | Update SKILL.md frontmatter |
| `updateChangelog(repoPath, newVersion, notes)` | Prepend to CHANGELOG.md |
| `publishNpm(repoPath)` | Publish to npmjs.com (@latest) |
| `publishNpmWithTag(repoPath, tag)` | Publish to npmjs.com with specific tag |
| `publishGitHubPackages(repoPath)` | Publish to npm.pkg.github.com |
| `createGitHubRelease(repoPath, newVersion, notes, currentVersion)` | Create GitHub release on private repo |
| `createGitHubPrerelease(repoPath, newVersion, notes)` | Create GitHub prerelease on public repo |
| `createGitHubReleaseOnPublic(repoPath, newVersion, notes, currentVersion)` | Create GitHub release on public repo |
| `buildReleaseNotes(repoPath, currentVersion, newVersion, notes)` | Generate detailed release notes |
| `publishClawHub(repoPath, newVersion, notes)` | Publish skill to ClawHub |

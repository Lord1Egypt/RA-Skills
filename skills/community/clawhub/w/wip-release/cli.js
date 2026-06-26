#!/usr/bin/env node

/**
 * wip-release/cli.mjs
 * Release tool CLI. Bumps version, updates docs, publishes.
 */

import { release, releasePrerelease, releaseHotfix, detectCurrentVersion, collectMergedPRNotes } from './core.mjs';

const args = process.argv.slice(2);
const level = args.find(a => ['patch', 'minor', 'major', 'alpha', 'beta', 'hotfix'].includes(a));

function flag(name) {
  const prefix = `--${name}=`;
  const found = args.find(a => a.startsWith(prefix));
  return found ? found.slice(prefix.length) : null;
}

const dryRun = args.includes('--dry-run');
const noPublish = args.includes('--no-publish');
const skipProductCheck = args.includes('--skip-product-check');
const skipStaleCheck = args.includes('--skip-stale-check');
const skipWorktreeCheck = args.includes('--skip-worktree-check');
const skipTechDocsCheck = args.includes('--skip-tech-docs-check');
const skipCoverageCheck = args.includes('--skip-coverage-check');
const allowSubToolDrift = args.includes('--allow-sub-tool-drift');
const noDeployPublic = args.includes('--no-deploy-public');
const wantReleaseNotes = args.includes('--release-notes');
const noReleaseNotes = args.includes('--no-release-notes');
const notesFilePath = flag('notes-file');
let notes = flag('notes');
// Bug fix #121: use strict check, not truthiness. --notes="" is empty, not absent.
let notesSource = (notes !== null && notes !== undefined && notes !== '') ? 'flag' : 'none';

// Release notes priority (highest wins):
//   1. --notes-file=path          Explicit file path (always wins)
//   2. RELEASE-NOTES-v{ver}.md    In repo root (always wins over --notes flag)
//   2.5. Merged PR notes          Auto-combined from git history (#237)
//   3. ai/dev-updates/YYYY-MM-DD* Today's dev update (wins over --notes flag if longer)
//   4. --notes="text"             Flag fallback (only if nothing better exists)
//
// Rule: written release notes on disk ALWAYS beat a CLI one-liner.
// The --notes flag is a fallback, not an override.
{
  const { readFileSync, existsSync } = await import('node:fs');
  const { resolve, join } = await import('node:path');
  const flagNotes = notes; // save original flag value for fallback

  if (notesFilePath) {
    // 1. Explicit --notes-file (highest priority)
    const resolved = resolve(notesFilePath);
    if (!existsSync(resolved)) {
      console.error(`  ✗ Notes file not found: ${resolved}`);
      process.exit(1);
    }
    notes = readFileSync(resolved, 'utf8').trim();
    notesSource = 'file';
  } else if (level && ['patch', 'minor', 'major', 'hotfix'].includes(level)) {
    // 2. Auto-detect RELEASE-NOTES-v{version}.md (ALWAYS checks, even if --notes provided)
    // Only for stable levels and hotfix. Alpha/beta skip this.
    try {
      const { detectCurrentVersion, bumpSemver } = await import('./core.mjs');
      const cwd = process.cwd();
      const currentVersion = detectCurrentVersion(cwd);
      const bumpLevel = level === 'hotfix' ? 'patch' : level;
      const newVersion = bumpSemver(currentVersion, bumpLevel);
      const dashed = newVersion.replace(/\./g, '-');
      const autoFile = join(cwd, `RELEASE-NOTES-v${dashed}.md`);
      if (existsSync(autoFile)) {
        const fileContent = readFileSync(autoFile, 'utf8').trim();
        if (flagNotes && flagNotes !== fileContent) {
          console.log(`  ! --notes flag ignored: RELEASE-NOTES-v${dashed}.md takes priority`);
        }
        notes = fileContent;
        notesSource = 'file';
        console.log(`  ✓ Found RELEASE-NOTES-v${dashed}.md`);
      }
    } catch {}
  }

  // 2.5. Auto-combine release notes from merged PRs since last tag (#237)
  // Only runs when no single RELEASE-NOTES file was found on disk.
  // Scans git merge history for RELEASE-NOTES files committed on PR branches.
  if (level && ['patch', 'minor', 'major', 'hotfix'].includes(level) && notesSource !== 'file') {
    try {
      const { collectMergedPRNotes, detectCurrentVersion: dcv, bumpSemver: bs } = await import('./core.mjs');
      const cwd = process.cwd();
      const cv = dcv(cwd);
      const bumpLevel = level === 'hotfix' ? 'patch' : level;
      const nv = bs(cv, bumpLevel);
      const combined = collectMergedPRNotes(cwd, cv, nv);
      if (combined) {
        if (flagNotes && flagNotes !== combined.notes) {
          console.log(`  ! --notes flag ignored: merged PR notes take priority`);
        }
        notes = combined.notes;
        notesSource = combined.notesSource;
        if (combined.prCount > 1) {
          console.log(`  \u2713 Combined release notes from ${combined.prCount} merged PRs`);
        } else {
          console.log(`  \u2713 Found release notes from merged PR`);
        }
      }
    } catch {}
  }

  // 3. Auto-detect dev update from ai/dev-updates/ (wins over --notes flag if longer)
  if (level && (!notes || (notesSource === 'flag' && notes.length < 200))) {
    try {
      const { readdirSync } = await import('node:fs');
      const devUpdatesDir = join(process.cwd(), 'ai', 'dev-updates');
      if (existsSync(devUpdatesDir)) {
        const d = new Date();
        const today = `${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,'0')}-${String(d.getDate()).padStart(2,'0')}`;
        const todayFiles = readdirSync(devUpdatesDir)
          .filter(f => f.startsWith(today) && f.endsWith('.md'))
          .sort()
          .reverse();

        if (todayFiles.length > 0) {
          const devUpdatePath = join(devUpdatesDir, todayFiles[0]);
          const devUpdateContent = readFileSync(devUpdatePath, 'utf8').trim();
          if (devUpdateContent.length > (notes || '').length) {
            if (flagNotes) {
              console.log(`  ! --notes flag ignored: dev update takes priority`);
            }
            notes = devUpdateContent;
            notesSource = 'dev-update';
            console.log(`  ✓ Found dev update: ai/dev-updates/${todayFiles[0]}`);
          }
        }
      }
    } catch {}
  }
}

if (args.includes('--version') || args.includes('-v')) {
  const { readFileSync } = await import('node:fs');
  const { join, dirname } = await import('node:path');
  const { fileURLToPath } = await import('node:url');
  const pkg = JSON.parse(readFileSync(join(dirname(fileURLToPath(import.meta.url)), 'package.json'), 'utf8'));
  console.log(pkg.version);
  process.exit(0);
}

if (!level || args.includes('--help') || args.includes('-h')) {
  const cwd = process.cwd();
  let current = '';
  try { current = ` (current: ${detectCurrentVersion(cwd)})`; } catch {}

  console.log(`wip-release ... local release tool${current}

Usage:
  wip-release patch                    1.0.0 -> 1.0.1 (stable)
  wip-release minor                    1.0.0 -> 1.1.0 (stable)
  wip-release major                    1.0.0 -> 2.0.0 (stable)
  wip-release alpha                    1.0.1-alpha.1 (prerelease)
  wip-release beta                     1.0.1-beta.1 (prerelease)
  wip-release hotfix                   1.0.0 -> 1.0.1 (hotfix, no deploy-public)

Release tracks:
  alpha    npm @alpha tag, no public notes (opt in with --release-notes)
  beta     npm @beta tag, prerelease notes on public (opt out with --no-release-notes)
  hotfix   npm @latest tag, release notes on public (opt out with --no-release-notes)
  stable   npm @latest tag, deploy-public, full notes (patch/minor/major)

Flags:
  --notes="description"    Release narrative (what was built and why)
  --notes-file=path        Read release narrative from a markdown file
  --release-notes          Opt in to public release notes (alpha only)
  --no-release-notes       Opt out of public release notes (beta, hotfix)
  --dry-run                Show what would happen, change nothing
  --no-publish             Bump + tag only, skip npm/GitHub
  --skip-product-check     Skip product docs check (dev update, roadmap, readme-first)
  --skip-stale-check       Skip stale remote branch check
  --skip-worktree-check    Skip main-branch + worktree guard (break-glass only)
  --allow-sub-tool-drift   Allow release even if a sub-tool's files changed since the last tag without a version bump (error by default)
  --no-deploy-public       Skip the deploy-public.sh step at the end of stable and prerelease flows (runs by default for -private repos)

Release notes (REQUIRED for stable, optional for other tracks):
  1. --notes-file=path          Explicit file path
  2. RELEASE-NOTES-v{ver}.md    In repo root (auto-detected)
  3. Merged PR notes             Auto-combined from git history (#237)
  4. ai/dev-updates/YYYY-MM-DD* Today's dev update (auto-detected)
  For stable releases: the --notes flag is NOT accepted. Write a file.
  For alpha/beta/hotfix: --notes="text" is accepted as a convenience.

Skill publish to website:
  Add .publish-skill.json to repo root: { "name": "my-tool" }
  Set WIP_WEBSITE_REPO env var to your website repo path.
  After release, SKILL.md is copied to {website}/wip.computer/install/{name}.txt
  and deploy.sh is run to push to VPS.

Pipeline (stable):
  1. Bump package.json version
  2. Sync SKILL.md version (if exists)
  3. Update CHANGELOG.md
  4. Git commit + tag
  5. Push to remote
  6. npm publish (via 1Password)
  7. GitHub Packages publish
  8. GitHub release create
  9. Publish SKILL.md to website (if configured)

Pipeline (alpha/beta):
  1. Bump version with prerelease suffix (-alpha.N / -beta.N)
  2. npm publish with --tag alpha or --tag beta
  3. GitHub prerelease (beta default, alpha opt-in)

Pipeline (hotfix):
  1. Bump patch version (no suffix)
  2. npm publish with --tag latest
  3. GitHub release (no deploy-public)`);
  process.exit(level ? 0 : 1);
}

// Route to the correct release function based on track
if (level === 'alpha' || level === 'beta') {
  // Prerelease track: alpha or beta
  releasePrerelease({
    repoPath: process.cwd(),
    track: level,
    notes,
    dryRun,
    noPublish,
    publishReleaseNotes: level === 'alpha' ? wantReleaseNotes : !noReleaseNotes,
    skipWorktreeCheck,
    allowSubToolDrift,
    noDeployPublic,
  }).catch(err => {
    console.error(`  \u2717 ${err.message}`);
    process.exit(1);
  });
} else if (level === 'hotfix') {
  // Hotfix track: patch bump, @latest tag, no deploy-public
  releaseHotfix({
    repoPath: process.cwd(),
    notes,
    notesSource,
    dryRun,
    noPublish,
    publishReleaseNotes: !noReleaseNotes,
    skipWorktreeCheck,
    allowSubToolDrift,
  }).catch(err => {
    console.error(`  \u2717 ${err.message}`);
    process.exit(1);
  });
} else {
  // Stable track: patch, minor, major
  release({
    repoPath: process.cwd(),
    level,
    notes,
    notesSource,
    dryRun,
    noPublish,
    skipProductCheck,
    skipStaleCheck,
    skipWorktreeCheck,
    skipTechDocsCheck,
    skipCoverageCheck,
    allowSubToolDrift,
    noDeployPublic,
  }).catch(err => {
    console.error(`  \u2717 ${err.message}`);
    process.exit(1);
  });
}

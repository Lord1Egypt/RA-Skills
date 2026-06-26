/**
 * wip-release/core.mjs
 * Local release tool. Bumps version, updates changelog + SKILL.md,
 * commits, tags, publishes to npm + GitHub Packages, creates GitHub release.
 * Zero dependencies.
 */

import { execSync, execFileSync, spawnSync } from 'node:child_process';
import { readFileSync, writeFileSync, existsSync, readdirSync, mkdirSync, renameSync } from 'node:fs';
import { join, basename, dirname } from 'node:path';

// ── Version ─────────────────────────────────────────────────────────

/**
 * Read current version from package.json.
 */
export function detectCurrentVersion(repoPath) {
  const pkgPath = join(repoPath, 'package.json');
  if (!existsSync(pkgPath)) throw new Error(`No package.json found at ${repoPath}`);
  const pkg = JSON.parse(readFileSync(pkgPath, 'utf8'));
  return pkg.version;
}

/**
 * Bump a semver string by level.
 */
export function bumpSemver(version, level) {
  const base = version.replace(/-.*$/, '');
  const [major, minor, patch] = base.split('.').map(Number);
  switch (level) {
    case 'major': return `${major + 1}.0.0`;
    case 'minor': return `${major}.${minor + 1}.0`;
    case 'patch': return `${major}.${minor}.${patch + 1}`;
    default: throw new Error(`Invalid level: ${level}. Use major, minor, or patch.`);
  }
}

/**
 * Bump a version string for prerelease tracks (alpha, beta).
 *
 * If the current version already has the same prerelease prefix,
 * increment the counter: 1.2.3-alpha.1 -> 1.2.3-alpha.2
 *
 * If the current version is a clean release or a different prerelease,
 * bump patch and start at .1: 1.2.3 -> 1.2.4-alpha.1
 */
export function bumpPrerelease(version, track) {
  // Check if current version already has this prerelease prefix
  const preMatch = version.match(new RegExp(`^(\\d+\\.\\d+\\.\\d+)-${track}\\.(\\d+)$`));
  if (preMatch) {
    // Same track: increment the counter
    const base = preMatch[1];
    const counter = parseInt(preMatch[2], 10);
    return `${base}-${track}.${counter + 1}`;
  }

  // Strip any existing prerelease suffix to get the base version
  const baseMatch = version.match(/^(\d+)\.(\d+)\.(\d+)/);
  if (!baseMatch) throw new Error(`Cannot parse version: ${version}`);

  const major = parseInt(baseMatch[1], 10);
  const minor = parseInt(baseMatch[2], 10);
  const patch = parseInt(baseMatch[3], 10);

  // Bump patch and start prerelease at .1
  return `${major}.${minor}.${patch + 1}-${track}.1`;
}

/**
 * Write new version to package.json.
 */
function writePackageVersion(repoPath, newVersion) {
  const pkgPath = join(repoPath, 'package.json');
  const pkg = JSON.parse(readFileSync(pkgPath, 'utf8'));
  pkg.version = newVersion;
  writeFileSync(pkgPath, JSON.stringify(pkg, null, 2) + '\n');
}

// ── SKILL.md ────────────────────────────────────────────────────────

/**
 * Update version in SKILL.md YAML frontmatter.
 */
export function syncSkillVersion(repoPath, newVersion) {
  const skillPath = join(repoPath, 'SKILL.md');
  if (!existsSync(skillPath)) return false;

  let content = readFileSync(skillPath, 'utf8');

  // Check for staleness: if SKILL.md version is more than a patch behind,
  // warn that content may need updating (not just the version number)
  const skillVersionMatch = content.match(/^---[\s\S]*?version:\s*"?(\d+\.\d+\.\d+)"?[\s\S]*?---/);
  if (skillVersionMatch) {
    const skillVersion = skillVersionMatch[1];
    const [sMaj, sMin] = skillVersion.split('.').map(Number);
    const [nMaj, nMin] = newVersion.split('.').map(Number);
    if (nMaj > sMaj || nMin > sMin + 1) {
      console.warn(`  ! SKILL.md is at ${skillVersion}, releasing ${newVersion}`);
      console.warn(`    SKILL.md content may be stale. Review tool list and interfaces.`);
    }
  }

  // Match version line in YAML frontmatter (between --- markers).
  // Uses "[^\n]* for quoted values (including corrupted multi-quote strings
  // like "1.9.5".9.4".9.3") or \S+ for unquoted values. This replaces the
  // ENTIRE value on the line, preventing the accumulation bug (#71).
  const updated = content.replace(
    /^(---[\s\S]*?version:\s*)(?:"[^\n]*|\S+)([\s\S]*?---)/,
    `$1"${newVersion}"$2`
  );

  if (updated === content) return false;
  writeFileSync(skillPath, updated);
  return true;
}

// ── CHANGELOG.md ────────────────────────────────────────────────────

/**
 * Prepend a new version entry to CHANGELOG.md.
 */
export function updateChangelog(repoPath, newVersion, notes) {
  const changelogPath = join(repoPath, 'CHANGELOG.md');
  const d = new Date();
  const date = `${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,'0')}-${String(d.getDate()).padStart(2,'0')}`;

  // Bug fix #121: never silently default to "Release." when notes are empty.
  // If notes are empty at this point, warn loudly.
  if (!notes || !notes.trim()) {
    console.warn(`  ! WARNING: No release notes provided for v${newVersion}. CHANGELOG entry will be minimal.`);
    notes = 'No release notes provided.';
  }

  const entry = `## ${newVersion} (${date})\n\n${notes}\n`;

  if (!existsSync(changelogPath)) {
    writeFileSync(changelogPath, `# Changelog\n\n${entry}`);
    return;
  }

  let content = readFileSync(changelogPath, 'utf8');
  // Insert after the # Changelog header (single newline, no accumulation)
  const headerMatch = content.match(/^# Changelog\s*\n+/);
  if (headerMatch) {
    const insertPoint = headerMatch[0].length;
    content = content.slice(0, insertPoint) + entry + '\n' + content.slice(insertPoint);
  } else {
    content = `# Changelog\n\n${entry}\n${content}`;
  }

  writeFileSync(changelogPath, content);
}

// ── Git ─────────────────────────────────────────────────────────────

/**
 * Move all RELEASE-NOTES-v*.md files to _trash/.
 * Returns the number of files moved.
 */
function trashReleaseNotes(repoPath) {
  const files = readdirSync(repoPath).filter(f => /^RELEASE-NOTES-v.*\.md$/i.test(f));
  if (files.length === 0) return 0;

  const trashDir = join(repoPath, '_trash');
  if (!existsSync(trashDir)) mkdirSync(trashDir);

  for (const f of files) {
    renameSync(join(repoPath, f), join(trashDir, f));
    execFileSync('git', ['add', join('_trash', f)], { cwd: repoPath, stdio: 'pipe' });
    // Only git rm if the file was tracked (committed or staged).
    // Untracked scaffolded files from failed releases just need the rename.
    try {
      execFileSync('git', ['ls-files', '--error-unmatch', f], { cwd: repoPath, stdio: 'pipe' });
      execFileSync('git', ['rm', '--cached', f], { cwd: repoPath, stdio: 'pipe' });
    } catch {
      // File wasn't tracked. Rename already moved it.
    }
  }
  return files.length;
}

function gitCommitAndTag(repoPath, newVersion, notes) {
  const msg = `v${newVersion}: ${notes || 'Release'}`;
  // Stage ALL files that wip-release modifies:
  // - Root: package.json, CHANGELOG.md, SKILL.md
  // - Sub-tools: tools/*/package.json
  // - Product docs: ai/product/plans-prds/roadmap.md, ai/product/readme-first-product.md
  // - Trashed release notes: _trash/RELEASE-NOTES-*.md
  // Using git add -A on specific paths instead of listing each file (#231)
  for (const f of ['package.json', 'CHANGELOG.md', 'SKILL.md']) {
    if (existsSync(join(repoPath, f))) {
      execFileSync('git', ['add', f], { cwd: repoPath, stdio: 'pipe' });
    }
  }
  // Stage sub-tool package.json files
  const toolsDir = join(repoPath, 'tools');
  if (existsSync(toolsDir)) {
    for (const sub of readdirSync(toolsDir, { withFileTypes: true })) {
      if (!sub.isDirectory()) continue;
      const subPkg = join('tools', sub.name, 'package.json');
      if (existsSync(join(repoPath, subPkg))) {
        execFileSync('git', ['add', subPkg], { cwd: repoPath, stdio: 'pipe' });
      }
    }
  }
  // Stage product docs and trashed release notes
  const aiProduct = join(repoPath, 'ai', 'product');
  if (existsSync(aiProduct)) {
    execFileSync('git', ['add', 'ai/product/'], { cwd: repoPath, stdio: 'pipe' });
  }
  const trash = join(repoPath, '_trash');
  if (existsSync(trash)) {
    execFileSync('git', ['add', '_trash/'], { cwd: repoPath, stdio: 'pipe' });
  }
  // Use execFileSync to avoid shell injection via notes.
  // --no-verify: wip-release legitimately commits on main (version bump + changelog).
  // The pre-commit hook blocks all commits on main, but wip-release is the one exception.
  execFileSync('git', ['commit', '--no-verify', '-m', msg], { cwd: repoPath, stdio: 'pipe' });
  execFileSync('git', ['tag', `v${newVersion}`], { cwd: repoPath, stdio: 'pipe' });
}

// ── Publish ─────────────────────────────────────────────────────────

/**
 * Run `npm publish` and surface captured stderr in thrown errors.
 *
 * Why not execFileSync(..., stdio: 'inherit')?
 *   execFileSync with stdio:'inherit' sends npm's stderr directly to the
 *   parent tty. When the call throws, the error's .message is just
 *   "Command failed: npm publish ..." ... it does NOT contain npm's stderr.
 *   Callers trying to detect idempotent failures (e.g. "cannot publish over
 *   the previously published versions") by substring-matching e.message
 *   never matched and logged every re-publish as a real failure instead of
 *   the intended silent swallow.
 *
 * Fix: pipe stderr (and stdout), echo captured bytes to the real tty for
 * visibility, then include stderr in the thrown error's .message AND as
 * .stderr so callers can match reliably. Stdout is inherited so live
 * progress still prints.
 */
function runNpmPublish(args, cwd) {
  // Stdout inherits for live progress; stderr piped so we can capture the
  // "cannot publish over..." text that callers substring-match to detect
  // idempotent re-publishes.
  const res = spawnSync('npm', args, { cwd, encoding: 'utf8', stdio: ['inherit', 'inherit', 'pipe'] });
  const stderr = res.stderr || '';
  if (stderr) process.stderr.write(stderr);
  if (res.status !== 0 || res.error) {
    // Redact the auth token from the reproduced command for logs.
    const safeArgs = args.map(a => a.replace(/_authToken=[^&\s]+/, '_authToken=***'));
    const msg = `Command failed: npm ${safeArgs.join(' ')}${stderr ? '\n' + stderr.trim() : ''}`;
    const err = new Error(msg);
    err.stderr = stderr;
    err.status = res.status;
    throw err;
  }
}

/**
 * Publish to npm via 1Password for auth.
 * Default tag (latest).
 */
export function publishNpm(repoPath) {
  const token = getNpmToken();
  runNpmPublish([
    'publish', '--access', 'public',
    `--//registry.npmjs.org/:_authToken=${token}`,
  ], repoPath);
}

/**
 * Publish to npm with a specific dist-tag (alpha, beta, latest).
 */
export function publishNpmWithTag(repoPath, tag) {
  const token = getNpmToken();
  runNpmPublish([
    'publish', '--access', 'public',
    '--tag', tag,
    `--//registry.npmjs.org/:_authToken=${token}`,
  ], repoPath);
}

/**
 * Publish to GitHub Packages.
 */
export function publishGitHubPackages(repoPath) {
  const ghToken = execSync('gh auth token', { encoding: 'utf8' }).trim();
  execFileSync('npm', [
    'publish',
    '--registry', 'https://npm.pkg.github.com',
    `--//npm.pkg.github.com/:_authToken=${ghToken}`
  ], { cwd: repoPath, stdio: 'inherit' });
}

/**
 * Categorize a commit message into a section.
 * Returns: 'changes', 'fixes', 'docs', 'internal'
 */
function categorizeCommit(subject) {
  const lower = subject.toLowerCase();

  // Fixes
  if (lower.startsWith('fix') || lower.startsWith('hotfix') || lower.startsWith('bugfix') ||
      lower.includes('fix:') || lower.includes('bug:')) {
    return 'fixes';
  }

  // Docs
  if (lower.startsWith('doc') || lower.startsWith('readme') ||
      lower.includes('docs:') || lower.includes('doc:') ||
      lower.startsWith('update readme') || lower.startsWith('rewrite readme') ||
      lower.startsWith('update technical') || lower.startsWith('rewrite relay') ||
      lower.startsWith('update relay')) {
    return 'docs';
  }

  // Internal (skip in release notes)
  if (lower.startsWith('chore') || lower.startsWith('auto-commit') ||
      lower.startsWith('merge pull request') || lower.startsWith('merge branch') ||
      lower.match(/^v\d+\.\d+\.\d+/) || lower.startsWith('mark ') ||
      lower.startsWith('clean up todo') || lower.startsWith('keep ')) {
    return 'internal';
  }

  // Everything else is a change
  return 'changes';
}

/**
 * Check release notes quality. Returns { ok, issues[] }.
 *
 * notesSource: 'file' (RELEASE-NOTES-v*.md or --notes-file),
 *              'dev-update' (ai/dev-updates/ fallback),
 *              'flag' (bare --notes="string"),
 *              'none' (nothing provided).
 *
 * For minor/major: BLOCKS if notes came from bare --notes flag or are missing.
 *   Agents must write a RELEASE-NOTES-v{version}.md file and commit it.
 * For patch: WARNS only.
 */
function checkReleaseNotes(notes, notesSource, level) {
  const issues = [];

  if (!notes) {
    issues.push('No release notes found. A file is REQUIRED.');
    issues.push('Write RELEASE-NOTES-v{version}.md or ai/dev-updates/YYYY-MM-DD--description.md');
    issues.push('Commit it on your branch so it is reviewable in the PR.');
    return { ok: false, issues, block: true };
  }

  // HARD RULE: release notes must come from a file on disk.
  // --notes flag is NOT accepted. Write a file. Commit it. Review it.
  if (notesSource === 'flag') {
    issues.push('Release notes must come from a file, not the --notes flag.');
    issues.push('Write RELEASE-NOTES-v{version}.md or ai/dev-updates/YYYY-MM-DD--description.md');
    issues.push('Commit it on your branch so it is reviewable in the PR before merge.');
    return { ok: false, issues, block: true };
  }

  // Notes too short.
  if (notes.length < 50) {
    issues.push('Release notes are too short (under 50 chars). Explain what changed and why.');
  }

  // Check for changelog-style one-liners
  const looksLikeChangelog = /^(fix|add|update|remove|bump|chore|refactor|docs?)[\s:]/i.test(notes);
  if (looksLikeChangelog && notes.length < 100) {
    issues.push('Notes look like a changelog entry, not a narrative. Explain the impact.');
  }

  // Narrative quality: must have at least one paragraph (not just bullets/headers)
  // A paragraph is 2+ consecutive lines of prose (not starting with -, *, #, |, or ```)
  const lines = notes.split('\n').filter(l => l.trim().length > 0);
  const proseLines = lines.filter(l => {
    const t = l.trim();
    return !t.startsWith('#') && !t.startsWith('-') && !t.startsWith('*') &&
           !t.startsWith('|') && !t.startsWith('```') && !t.startsWith('>') &&
           t.length > 30;
  });
  if (proseLines.length < 2) {
    issues.push('Release notes need narrative, not just bullets. Write at least one paragraph explaining what changed and why it matters. Tell the story.');
  }

  // Must be substantial (not just a header + bullets)
  if (notes.length < 200) {
    issues.push('Release notes are too short (under 200 chars). Every release deserves a story: what was broken or missing, what we built, why the user should care.');
  }

  // Release notes should reference at least one issue
  const hasIssueRef = /#\d+/.test(notes);
  if (!hasIssueRef) {
    issues.push('No issue reference found (#XX). Every release should close or reference an issue.');
  }

  return { ok: issues.length === 0, issues, block: issues.length > 0 };
}

/**
 * Scaffold a RELEASE-NOTES-v{version}.md template if one doesn't exist.
 * Called when the release notes gate blocks. Gives the agent a file to fill in.
 */
export function scaffoldReleaseNotes(repoPath, version) {
  const dashed = version.replace(/\./g, '-');
  const notesPath = join(repoPath, `RELEASE-NOTES-v${dashed}.md`);
  if (existsSync(notesPath)) return notesPath;

  const pkg = JSON.parse(readFileSync(join(repoPath, 'package.json'), 'utf8'));
  const name = pkg.name?.replace(/^@[^/]+\//, '') || basename(repoPath);

  // Auto-detect issue references from commits since last tag
  let issueRefs = '';
  try {
    const lastTag = execFileSync('git', ['describe', '--tags', '--abbrev=0'],
      { cwd: repoPath, encoding: 'utf8' }).trim();
    const log = execFileSync('git', ['log', `${lastTag}..HEAD`, '--oneline'],
      { cwd: repoPath, encoding: 'utf8' });
    const issues = [...new Set(log.match(/#\d+/g) || [])];
    if (issues.length > 0) {
      issueRefs = issues.map(i => `- ${i}`).join('\n');
    }
  } catch {}

  const template = `# Release Notes: ${name} v${version}

**One-line summary of what this release does**

Tell the story. What was broken or missing? What did we build? Why does the user care?
Write at least one real paragraph of prose. Not just bullets. The release notes gate
will block if there is no narrative. Bullets are fine for details, but the story comes first.

## The story

(Write a paragraph here. What was the problem? What does this release fix? Why does it matter?
This is what users read. Make it worth reading.)

## Issues closed

${issueRefs || '- #XX (replace with actual issue numbers)'}

## How to verify

\`\`\`bash
# Commands to test the changes
\`\`\`
`;

  writeFileSync(notesPath, template);
  return notesPath;
}

/**
 * Collect release notes from merged PRs since the last tag.
 *
 * When multiple PRs are batched into a single release, each PR may have
 * committed its own RELEASE-NOTES-v*.md file. This function finds those
 * notes in git history and combines them into one document.
 *
 * Steps:
 *   1. git log v{prev}..HEAD --merges --oneline to find merge commits
 *   2. Extract PR number from "Merge pull request #XX from ..."
 *   3. Check each merge commit's diff for RELEASE-NOTES*.md files
 *   4. Read content via git show {sha}:{path}
 *   5. Combine into a single document (newest first)
 *
 * Returns { notes, notesSource, prCount } or null if nothing found.
 */
export function collectMergedPRNotes(repoPath, currentVersion, newVersion) {
  let lastTag;
  try {
    lastTag = execFileSync('git', ['describe', '--tags', '--abbrev=0'],
      { cwd: repoPath, encoding: 'utf8' }).trim();
  } catch {
    return null; // No tags yet
  }

  // Find merge commits since last tag
  let mergeLog;
  try {
    mergeLog = execFileSync('git', [
      'log', `${lastTag}..HEAD`, '--merges', '--oneline'
    ], { cwd: repoPath, encoding: 'utf8' }).trim();
  } catch {
    return null;
  }

  if (!mergeLog) return null;

  const mergeLines = mergeLog.split('\n').filter(Boolean);
  const prNotes = [];

  for (const line of mergeLines) {
    // Format: "abc1234 Merge pull request #XX from org/branch"
    const prMatch = line.match(/^([a-f0-9]+)\s+Merge pull request #(\d+)\s+from\s+(.+)$/);
    if (!prMatch) continue;

    const [, shortHash, prNum, branchRef] = prMatch;

    // Get the full hash for this merge commit
    let fullHash;
    try {
      fullHash = execFileSync('git', ['rev-parse', shortHash],
        { cwd: repoPath, encoding: 'utf8' }).trim();
    } catch {
      continue;
    }

    // List files changed in this merge commit.
    // For merge commits, diff against first parent to see what the PR brought in.
    // Plain diff-tree on a merge commit shows nothing without -m or -c.
    let changedFiles;
    try {
      changedFiles = execFileSync('git', [
        'diff', '--name-only', `${fullHash}^1`, fullHash
      ], { cwd: repoPath, encoding: 'utf8' }).trim();
    } catch {
      continue;
    }

    // Look for RELEASE-NOTES*.md files
    const noteFiles = changedFiles.split('\n')
      .filter(f => /^RELEASE-NOTES.*\.md$/i.test(f.trim()));

    if (noteFiles.length === 0) continue;

    // Read the content of each release notes file from that commit
    for (const noteFile of noteFiles) {
      try {
        const content = execFileSync('git', [
          'show', `${fullHash}:${noteFile.trim()}`
        ], { cwd: repoPath, encoding: 'utf8' }).trim();

        if (content) {
          prNotes.push({
            prNum,
            branch: branchRef,
            content,
            hash: shortHash,
          });
        }
      } catch {
        // File might have been deleted in the merge. Skip.
      }
    }
  }

  if (prNotes.length === 0) return null;

  // If only one PR had notes, return it directly (no wrapping)
  if (prNotes.length === 1) {
    return {
      notes: prNotes[0].content,
      notesSource: 'file',
      prCount: 1,
    };
  }

  // Multiple PRs: combine into one document (newest first, already in log order)
  const pkg = JSON.parse(readFileSync(join(repoPath, 'package.json'), 'utf8'));
  const name = pkg.name?.replace(/^@[^/]+\//, '') || basename(repoPath);

  const sections = [];
  sections.push(`# Release Notes: ${name} v${newVersion}`);
  sections.push('');
  sections.push(`This release combines ${prNotes.length} merged pull requests.`);
  sections.push('');

  // Collect all issue refs for a combined summary
  const allIssueRefs = new Set();

  for (const pr of prNotes) {
    sections.push(`---`);
    sections.push('');
    sections.push(`### PR #${pr.prNum}`);
    sections.push('');

    // Strip the top-level heading from individual notes to avoid duplicate titles
    let body = pr.content;
    body = body.replace(/^#\s+.*\n+/, '');
    sections.push(body);
    sections.push('');

    // Collect issue references
    const refs = body.match(/#\d+/g) || [];
    for (const ref of refs) allIssueRefs.add(ref);
  }

  // Add combined issue references at the end
  if (allIssueRefs.size > 0) {
    sections.push('---');
    sections.push('');
    sections.push('## All issues referenced');
    sections.push('');
    for (const ref of allIssueRefs) {
      sections.push(`- ${ref}`);
    }
    sections.push('');
  }

  return {
    notes: sections.join('\n'),
    notesSource: 'file',
    prCount: prNotes.length,
  };
}

/**
 * Check if a file was modified in commits since the last git tag.
 */
function fileModifiedSinceLastTag(repoPath, relativePath) {
  try {
    const lastTag = execFileSync('git', ['describe', '--tags', '--abbrev=0'],
      { cwd: repoPath, encoding: 'utf8' }).trim();
    const diff = execFileSync('git', ['diff', '--name-only', lastTag, 'HEAD'],
      { cwd: repoPath, encoding: 'utf8' });
    return diff.split('\n').some(f => f.trim() === relativePath);
  } catch {
    // No tags yet or git error ... skip check
    return true;
  }
}

/**
 * Check that product docs were updated for this release.
 * Returns { missing: string[], ok: boolean, skipped: boolean }.
 * Only runs if ai/ directory structure exists.
 */
function checkProductDocs(repoPath) {
  const missing = [];

  // Skip repos without ai/ structure
  const aiDir = join(repoPath, 'ai');
  if (!existsSync(aiDir)) return { missing: [], ok: true, skipped: true };

  // 1. Dev update: must have a file modified since last release tag.
  // Old check ("any file from last 3 days") let the same stale file pass
  // across 11 releases in one session. Now uses the same git-based check
  // as roadmap and readme-first: was the file actually changed since the tag?
  const devUpdatesDir = join(aiDir, 'dev-updates');
  if (existsSync(devUpdatesDir)) {
    const files = readdirSync(devUpdatesDir).filter(f => f.endsWith('.md'));
    if (files.length === 0) {
      missing.push('ai/dev-updates/ (no dev update files)');
    } else {
      const anyModified = files.some(f =>
        fileModifiedSinceLastTag(repoPath, `ai/dev-updates/${f}`)
      );
      if (!anyModified) {
        missing.push('ai/dev-updates/ (no dev update modified since last release)');
      }
    }
  }

  // 2. Roadmap: modified since last tag
  const roadmapPath = 'ai/product/plans-prds/roadmap.md';
  if (existsSync(join(repoPath, roadmapPath))) {
    if (!fileModifiedSinceLastTag(repoPath, roadmapPath)) {
      missing.push('ai/product/plans-prds/roadmap.md (not updated since last release)');
    }
  }

  // 3. Readme-first: modified since last tag
  const readmeFirstPath = 'ai/product/readme-first-product.md';
  if (existsSync(join(repoPath, readmeFirstPath))) {
    if (!fileModifiedSinceLastTag(repoPath, readmeFirstPath)) {
      missing.push('ai/product/readme-first-product.md (not updated since last release)');
    }
  }

  // 4. Product update doc: modified since last tag
  const productUpdateDir = join(aiDir, 'dev-updates', 'product-update');
  if (existsSync(productUpdateDir)) {
    const puFiles = readdirSync(productUpdateDir).filter(f => f.endsWith('.md'));
    if (puFiles.length > 0) {
      const anyModified = puFiles.some(f =>
        fileModifiedSinceLastTag(repoPath, `ai/dev-updates/product-update/${f}`)
      );
      if (!anyModified) {
        missing.push('ai/dev-updates/product-update/ (product update doc not updated since last release)');
      }
    }
  }

  return { missing, ok: missing.length === 0, skipped: false };
}

/**
 * Check that technical docs (SKILL.md, TECHNICAL.md) were updated
 * when source code changed since last release tag.
 * Returns { missing: string[], ok: boolean, skipped: boolean }.
 */
function checkTechnicalDocs(repoPath) {
  try {
    let lastTag;
    try {
      lastTag = execFileSync('git', ['describe', '--tags', '--abbrev=0'],
        { cwd: repoPath, encoding: 'utf8' }).trim();
    } catch {
      return { missing: [], ok: true, skipped: true }; // No tags yet
    }

    const diff = execFileSync('git', ['diff', '--name-only', lastTag, 'HEAD'],
      { cwd: repoPath, encoding: 'utf8' });
    const changedFiles = diff.split('\n').map(f => f.trim()).filter(Boolean);

    // Find source code changes (*.mjs, *.js, *.ts) excluding non-source dirs
    const excludePattern = /\/(node_modules|dist|_trash|examples)\//;
    const sourcePattern = /\.(mjs|js|ts)$/;
    const sourceChanges = changedFiles.filter(f =>
      sourcePattern.test(f) && !excludePattern.test(f) && !f.startsWith('ai/')
    );

    if (sourceChanges.length === 0) {
      return { missing: [], ok: true, skipped: false }; // No source changes
    }

    // Check if any doc files were also modified
    const docChanges = changedFiles.filter(f =>
      f === 'SKILL.md' || f === 'TECHNICAL.md' ||
      /^tools\/[^/]+\/SKILL\.md$/.test(f) ||
      /^tools\/[^/]+\/TECHNICAL\.md$/.test(f)
    );

    if (docChanges.length > 0) {
      return { missing: [], ok: true, skipped: false }; // Docs updated
    }

    // Source changed but no doc updates
    const missing = [];
    const preview = sourceChanges.slice(0, 5).join(', ');
    const more = sourceChanges.length > 5 ? ` (and ${sourceChanges.length - 5} more)` : '';
    missing.push('Source files changed since last tag but no SKILL.md or TECHNICAL.md was updated');
    missing.push(`Changed: ${preview}${more}`);
    missing.push('Update SKILL.md or TECHNICAL.md to document these changes');

    return { missing, ok: false, skipped: false };
  } catch {
    return { missing: [], ok: true, skipped: true }; // Graceful fallback
  }
}

/**
 * Parse the interface coverage table from a markdown file.
 * Returns array of { name, cli, module, mcp, openclaw, skill, ccHook } or null.
 */
function parseInterfaceCoverageTable(filePath) {
  if (!existsSync(filePath)) return null;
  const content = readFileSync(filePath, 'utf8');
  const lines = content.split('\n');

  const headerIdx = lines.findIndex(l => /^\|\s*#\s*\|\s*Tool\s*\|/i.test(l));
  if (headerIdx === -1) return null;

  const rows = [];
  for (let i = headerIdx + 2; i < lines.length; i++) {
    const line = lines[i].trim();
    if (!line.startsWith('|')) break;
    const cells = line.split('|').map(c => c.trim()).filter(c => c !== '');
    if (cells.length < 8) continue;
    // Skip category header rows (# cell is empty, non-numeric, or bold)
    const num = cells[0].trim();
    if (!num || /^\*\*/.test(num) || isNaN(parseInt(num))) continue;
    rows.push({
      name: cells[1].trim(),
      cli: /^Y$/i.test(cells[2]),
      module: /^Y$/i.test(cells[3]),
      mcp: /^Y$/i.test(cells[4]),
      openclaw: /^Y$/i.test(cells[5]),
      skill: /^Y$/i.test(cells[6]),
      ccHook: /^Y$/i.test(cells[7]),
    });
  }
  return rows.length > 0 ? rows : null;
}

/**
 * Read display name from a tool's SKILL.md frontmatter.
 * Tries display-name, then name field. Falls back to null.
 */
function getToolDisplayName(toolPath) {
  const skillPath = join(toolPath, 'SKILL.md');
  if (!existsSync(skillPath)) return null;
  try {
    const content = readFileSync(skillPath, 'utf8');
    const displayMatch = content.match(/^\s*display-name:\s*"?([^"\n]+)"?/m);
    if (displayMatch) return displayMatch[1].trim();
    const nameMatch = content.match(/^name:\s*"?([^"\n]+)"?/m);
    if (nameMatch) return nameMatch[1].trim();
  } catch {}
  return null;
}

/**
 * Check that the interface coverage table in README.md and SKILL.md
 * matches the actual interfaces detected in tools/* subdirectories.
 * Returns { missing: string[], ok: boolean, skipped: boolean }.
 */
function checkInterfaceCoverage(repoPath) {
  try {
    // Only applies to toolbox repos
    const toolsDir = join(repoPath, 'tools');
    if (!existsSync(toolsDir)) return { missing: [], ok: true, skipped: true };

    const entries = readdirSync(toolsDir, { withFileTypes: true });
    const tools = entries
      .filter(e => e.isDirectory() && existsSync(join(toolsDir, e.name, 'package.json')))
      .map(e => ({ name: e.name, path: join(toolsDir, e.name) }));

    if (tools.length === 0) return { missing: [], ok: true, skipped: true };

    // Detect actual interfaces for each tool
    const actualMap = {};
    for (const tool of tools) {
      const pkg = JSON.parse(readFileSync(join(tool.path, 'package.json'), 'utf8'));
      actualMap[tool.name] = {
        displayName: getToolDisplayName(tool.path) || tool.name,
        cli: !!(pkg.bin),
        module: !!(pkg.main || pkg.exports),
        mcp: ['mcp-server.mjs', 'mcp-server.js', 'dist/mcp-server.js'].some(f => existsSync(join(tool.path, f))),
        openclaw: existsSync(join(tool.path, 'openclaw.plugin.json')),
        skill: existsSync(join(tool.path, 'SKILL.md')),
        ccHook: !!(pkg.claudeCode?.hook) || existsSync(join(tool.path, 'guard.mjs')),
      };
    }

    const missing = [];

    // Check both README.md and SKILL.md tables
    for (const [label, filePath] of [['README.md', join(repoPath, 'README.md')], ['SKILL.md', join(repoPath, 'SKILL.md')]]) {
      const tableRows = parseInterfaceCoverageTable(filePath);
      if (!tableRows) continue;

      // Tool count
      if (tools.length !== tableRows.length) {
        missing.push(`${label}: tool count mismatch (${tools.length} in tools/, ${tableRows.length} in table)`);
      }

      // Check each actual tool against the table
      for (const tool of tools) {
        const actual = actualMap[tool.name];
        const displayName = actual.displayName;
        const tableRow = tableRows.find(r =>
          r.name === displayName ||
          r.name.toLowerCase() === displayName.toLowerCase() ||
          r.name.toLowerCase().includes(tool.name.replace(/^wip-/, '').replace(/-/g, ' '))
        );

        if (!tableRow) {
          missing.push(`${label}: ${tool.name} (${displayName}) missing from coverage table`);
          continue;
        }

        const ifaceMap = [
          ['cli', 'CLI'], ['module', 'Module'], ['mcp', 'MCP'],
          ['openclaw', 'OC Plugin'], ['skill', 'Skill'], ['ccHook', 'CC Hook']
        ];

        for (const [key, name] of ifaceMap) {
          if (actual[key] && !tableRow[key]) {
            missing.push(`${label}: ${displayName} has ${name} but table says no`);
          }
          if (tableRow[key] && !actual[key]) {
            missing.push(`${label}: ${displayName} marked ${name} in table but not detected`);
          }
        }
      }
    }

    return { missing, ok: missing.length === 0, skipped: false };
  } catch {
    return { missing: [], ok: true, skipped: true }; // Graceful fallback
  }
}

/**
 * Auto-update version/date lines in product docs before the release commit.
 * Updates roadmap.md "Current version" and "Last updated",
 * and readme-first-product.md "Last updated" and "What's Built (as of vX.Y.Z)".
 * Returns number of files updated.
 */
function syncProductDocs(repoPath, newVersion) {
  let updated = 0;
  const td = new Date();
  const today = `${td.getFullYear()}-${String(td.getMonth()+1).padStart(2,'0')}-${String(td.getDate()).padStart(2,'0')}`;

  // 1. roadmap.md
  const roadmapPath = join(repoPath, 'ai', 'product', 'plans-prds', 'roadmap.md');
  if (existsSync(roadmapPath)) {
    let content = readFileSync(roadmapPath, 'utf8');
    let changed = false;

    // Update "Current version: vX.Y.Z"
    const versionRe = /(\*\*Current version:\*\*\s*)v[\d.]+/;
    if (versionRe.test(content)) {
      content = content.replace(versionRe, `$1v${newVersion}`);
      changed = true;
    }

    // Update "Last updated: YYYY-MM-DD"
    const dateRe = /(\*\*Last updated:\*\*\s*)[\d-]+/;
    if (dateRe.test(content)) {
      content = content.replace(dateRe, `$1${today}`);
      changed = true;
    }

    if (changed) {
      writeFileSync(roadmapPath, content);
      updated++;
    }
  }

  // 2. readme-first-product.md
  const rfpPath = join(repoPath, 'ai', 'product', 'readme-first-product.md');
  if (existsSync(rfpPath)) {
    let content = readFileSync(rfpPath, 'utf8');
    let changed = false;

    // Update "Last updated: YYYY-MM-DD"
    const dateRe = /(\*\*Last updated:\*\*\s*)[\d-]+/;
    if (dateRe.test(content)) {
      content = content.replace(dateRe, `$1${today}`);
      changed = true;
    }

    // Update "What's Built (as of vX.Y.Z)"
    const builtRe = /(What's Built \(as of\s*)v[\d.]+(\))/;
    if (builtRe.test(content)) {
      content = content.replace(builtRe, `$1v${newVersion}$2`);
      changed = true;
    }

    if (changed) {
      writeFileSync(rfpPath, content);
      updated++;
    }
  }

  return updated;
}

/**
 * Build release notes with narrative first, commit details second.
 *
 * Release notes should tell the story: what was built, why, and why it matters.
 * Commit history is included as supporting detail, not the main content.
 * ai/ files are excluded from the files-changed stats.
 */
export function buildReleaseNotes(repoPath, currentVersion, newVersion, notes) {
  const slug = detectRepoSlug(repoPath);
  const pkg = JSON.parse(readFileSync(join(repoPath, 'package.json'), 'utf8'));
  const lines = [];

  // Narrative summary (the main content of the release notes)
  if (notes) {
    lines.push(notes);
    lines.push('');
  }

  // Gather commits since last tag
  const prevTag = `v${currentVersion}`;
  let rawCommits = [];
  try {
    const raw = execFileSync('git', [
      'log', `${prevTag}..HEAD`, '--pretty=format:%h\t%s'
    ], { cwd: repoPath, encoding: 'utf8' }).trim();
    if (raw) rawCommits = raw.split('\n').map(line => {
      const [hash, ...rest] = line.split('\t');
      return { hash, subject: rest.join('\t') };
    });
  } catch {
    try {
      const raw = execFileSync('git', [
        'log', '--pretty=format:%h\t%s', '-30'
      ], { cwd: repoPath, encoding: 'utf8' }).trim();
      if (raw) rawCommits = raw.split('\n').map(line => {
        const [hash, ...rest] = line.split('\t');
        return { hash, subject: rest.join('\t') };
      });
    } catch {}
  }

  // Categorize commits
  const categories = { changes: [], fixes: [], docs: [], internal: [] };
  for (const commit of rawCommits) {
    const cat = categorizeCommit(commit.subject);
    categories[cat].push(commit);
  }

  // Commit details section (supporting detail, not the headline)
  const hasCommits = categories.changes.length + categories.fixes.length + categories.docs.length > 0;
  if (hasCommits) {
    lines.push('<details>');
    lines.push('<summary>What changed (commits)</summary>');
    lines.push('');

    if (categories.changes.length > 0) {
      lines.push('**Changes**');
      for (const c of categories.changes) {
        lines.push(`- ${c.subject} (${c.hash})`);
      }
      lines.push('');
    }

    if (categories.fixes.length > 0) {
      lines.push('**Fixes**');
      for (const c of categories.fixes) {
        lines.push(`- ${c.subject} (${c.hash})`);
      }
      lines.push('');
    }

    if (categories.docs.length > 0) {
      lines.push('**Docs**');
      for (const c of categories.docs) {
        lines.push(`- ${c.subject} (${c.hash})`);
      }
      lines.push('');
    }

    lines.push('</details>');
    lines.push('');
  }

  // Install section
  lines.push('### Install');
  lines.push('```bash');
  lines.push(`npm install -g ${pkg.name}@${newVersion}`);
  lines.push('```');
  lines.push('');
  lines.push('Or update your local clone:');
  lines.push('```bash');
  lines.push('git pull origin main');
  lines.push('```');
  lines.push('');

  // Attribution
  lines.push('---');
  lines.push('');
  lines.push('Built by Parker Todd Brooks, Lēsa (OpenClaw, Claude Opus 4.6), Claude Code (Claude Opus 4.6).');

  // Compare URL
  if (slug) {
    lines.push('');
    lines.push(`Full changelog: https://github.com/${slug}/compare/v${currentVersion}...v${newVersion}`);
  }

  return lines.join('\n');
}

/**
 * Create a GitHub release with detailed notes.
 */
export function createGitHubRelease(repoPath, newVersion, notes, currentVersion) {
  const repoSlug = detectRepoSlug(repoPath);
  const body = buildReleaseNotes(repoPath, currentVersion, newVersion, notes);

  // Write notes to a temp file to avoid shell escaping issues
  const tmpFile = join(repoPath, '.release-notes-tmp.md');
  writeFileSync(tmpFile, body);

  try {
    execFileSync('gh', [
      'release', 'create', `v${newVersion}`,
      '--title', `v${newVersion}`,
      '--notes-file', '.release-notes-tmp.md',
      '--repo', repoSlug
    ], { cwd: repoPath, stdio: 'inherit' });

    // Bug fix #121: verify the release was actually created
    try {
      const verify = execFileSync('gh', [
        'release', 'view', `v${newVersion}`,
        '--repo', repoSlug, '--json', 'body', '--jq', '.body | length'
      ], { cwd: repoPath, encoding: 'utf8' }).trim();
      const bodyLen = parseInt(verify, 10);
      if (bodyLen < 50) {
        console.warn(`  ! GitHub release body is only ${bodyLen} chars. Notes may be truncated.`);
      }
    } catch {}

    // Auto-close referenced issues
    const issueNums = [...new Set((body.match(/#(\d+)/g) || []).map(m => m.slice(1)))];
    for (const num of issueNums) {
      try {
        // Only close if issue exists and is open on the public repo
        const publicSlug = repoSlug.replace(/-private$/, '');
        execFileSync('gh', [
          'issue', 'close', num,
          '--repo', publicSlug,
          '--comment', `Closed by v${newVersion}. See release notes.`
        ], { cwd: repoPath, stdio: 'pipe' });
        console.log(`  ✓ Closed #${num} on ${publicSlug}`);
      } catch {
        // Issue doesn't exist on public repo or already closed. Fine.
      }
    }
  } finally {
    try { execFileSync('rm', ['-f', tmpFile]); } catch {}
  }
}

/**
 * Create a GitHub prerelease on the PUBLIC repo (no code sync).
 * Used by alpha (opt-in) and beta (default) tracks.
 */
export function createGitHubPrerelease(repoPath, newVersion, notes) {
  const repoSlug = detectRepoSlug(repoPath);
  if (!repoSlug) throw new Error('Cannot detect repo slug from git remote');

  // Target the public repo (strip -private suffix)
  const publicSlug = repoSlug.replace(/-private$/, '');
  const body = notes || `Prerelease ${newVersion}`;

  const tmpFile = join(repoPath, '.release-notes-tmp.md');
  writeFileSync(tmpFile, body);

  try {
    execFileSync('gh', [
      'release', 'create', `v${newVersion}`,
      '--title', `v${newVersion}`,
      '--notes-file', '.release-notes-tmp.md',
      '--prerelease',
      '--repo', publicSlug
    ], { cwd: repoPath, stdio: 'inherit' });
  } finally {
    try { execFileSync('rm', ['-f', tmpFile]); } catch {}
  }
}

/**
 * Create a GitHub release on the PUBLIC repo (no code sync).
 * Used by the hotfix track.
 */
export function createGitHubReleaseOnPublic(repoPath, newVersion, notes, currentVersion) {
  const repoSlug = detectRepoSlug(repoPath);
  if (!repoSlug) throw new Error('Cannot detect repo slug from git remote');

  // Target the public repo (strip -private suffix)
  const publicSlug = repoSlug.replace(/-private$/, '');
  const body = buildReleaseNotes(repoPath, currentVersion, newVersion, notes);

  const tmpFile = join(repoPath, '.release-notes-tmp.md');
  writeFileSync(tmpFile, body);

  try {
    execFileSync('gh', [
      'release', 'create', `v${newVersion}`,
      '--title', `v${newVersion}`,
      '--notes-file', '.release-notes-tmp.md',
      '--repo', publicSlug
    ], { cwd: repoPath, stdio: 'inherit' });
  } finally {
    try { execFileSync('rm', ['-f', tmpFile]); } catch {}
  }
}

/**
 * Publish skill to ClawHub.
 */
export function publishClawHub(repoPath, newVersion, notes) {
  const skillPath = join(repoPath, 'SKILL.md');
  if (!existsSync(skillPath)) return false;

  const slug = detectSkillSlug(repoPath);
  const changelog = notes || 'Release.';

  execFileSync('clawhub', [
    'publish', repoPath,
    '--slug', slug,
    '--version', newVersion,
    '--changelog', changelog
  ], { cwd: repoPath, stdio: 'inherit' });
  return true;
}

// ── Skill Publish ────────────────────────────────────────────────────

/**
 * Publish SKILL.md to website as plain text.
 *
 * Auto-detects: if SKILL.md exists and WIP_WEBSITE_REPO is set,
 * publishes automatically. No config file needed.
 *
 * Name resolution (first match wins):
 *   1. .publish-skill.json { "name": "memory-crystal" }
 *   2. SKILL.md frontmatter name: field
 *   3. Directory name (basename of repoPath)
 *
 * Copies SKILL.md to {website}/wip.computer/install/{name}.txt
 * Then runs deploy.sh to push to VPS.
 *
 * Non-blocking: returns result, never throws.
 */
export function publishSkillToWebsite(repoPath) {
  // Resolve website repo: .publish-skill.json > env var
  let websiteRepo;
  let targetName;
  const configPath = join(repoPath, '.publish-skill.json');
  let publishConfig = {};
  if (existsSync(configPath)) {
    try { publishConfig = JSON.parse(readFileSync(configPath, 'utf8')); } catch {}
  }

  websiteRepo = publishConfig.websiteRepo || process.env.WIP_WEBSITE_REPO;
  if (!websiteRepo) return { skipped: true, reason: 'no websiteRepo in .publish-skill.json and WIP_WEBSITE_REPO not set' };

  // Find SKILL.md: check root, then skills/*/SKILL.md
  let skillFile = join(repoPath, 'SKILL.md');
  if (!existsSync(skillFile)) {
    const skillsDir = join(repoPath, 'skills');
    if (existsSync(skillsDir)) {
      for (const sub of readdirSync(skillsDir)) {
        const candidate = join(skillsDir, sub, 'SKILL.md');
        if (existsSync(candidate)) { skillFile = candidate; break; }
      }
    }
  }
  if (!existsSync(skillFile)) return { skipped: true, reason: 'no SKILL.md found' };

  // Resolve target name: config > package.json > directory name
  // SKILL.md frontmatter name is skipped because it's a short slug
  // (e.g., "memory") not the full install name (e.g., "memory-crystal").

  // 1. Explicit config (optional, overrides auto-detect)
  if (publishConfig.name) targetName = publishConfig.name;

  // 2. package.json name (strip @scope/ prefix, most reliable)
  if (!targetName) {
    const pkgPath = join(repoPath, 'package.json');
    if (existsSync(pkgPath)) {
      try {
        const pkg = JSON.parse(readFileSync(pkgPath, 'utf8'));
        if (pkg.name) targetName = pkg.name.replace(/^@[^/]+\//, '');
      } catch {}
    }
  }

  // 3. Directory name fallback (strip -private suffix)
  if (!targetName) {
    targetName = basename(repoPath).replace(/-private$/, '').toLowerCase();
  }

  // Copy to website install dir
  const installDir = join(websiteRepo, 'wip.computer', 'install');
  if (!existsSync(installDir)) {
    try { mkdirSync(installDir, { recursive: true }); } catch {}
  }

  const targetFile = join(installDir, `${targetName}.txt`);
  try {
    const content = readFileSync(skillFile, 'utf8');
    writeFileSync(targetFile, content);
  } catch (e) {
    return { ok: false, error: `copy failed: ${e.message}` };
  }

  // Deploy to VPS (non-blocking ... warn on failure)
  const deployScript = join(websiteRepo, 'deploy.sh');
  if (existsSync(deployScript)) {
    try {
      execSync(`bash deploy.sh`, { cwd: websiteRepo, stdio: 'pipe', timeout: 30000 });
    } catch (e) {
      return { ok: true, deployed: false, target: targetName, error: `deploy failed: ${e.message}` };
    }
  } else {
    return { ok: true, deployed: false, target: targetName, error: 'no deploy.sh found' };
  }

  return { ok: true, deployed: true, target: targetName };
}

// ── Helpers ──────────────────────────────────────────────────────────

function getNpmToken() {
  try {
    return execSync(
      `OP_SERVICE_ACCOUNT_TOKEN=$(cat ~/.openclaw/secrets/op-sa-token) op item get "npm Token" --vault "Agent Secrets" --fields label=password --reveal 2>/dev/null`,
      { encoding: 'utf8' }
    ).trim();
  } catch {
    throw new Error('Could not fetch npm token from 1Password. Check op CLI and SA token.');
  }
}

function detectSkillSlug(repoPath) {
  // Read the name field from SKILL.md frontmatter (agentskills.io spec: lowercase-hyphen slug).
  // Falls back to directory name.
  const skillPath = join(repoPath, 'SKILL.md');
  if (existsSync(skillPath)) {
    const content = readFileSync(skillPath, 'utf8');
    const nameMatch = content.match(/^---[\s\S]*?\nname:\s*(.+?)\n/);
    if (nameMatch) {
      const name = nameMatch[1].trim().replace(/^["']|["']$/g, '');
      // Only use if it looks like a slug (lowercase, hyphens)
      if (/^[a-z][a-z0-9-]*$/.test(name)) return name;
    }
  }
  return basename(repoPath).toLowerCase();
}

function detectRepoSlug(repoPath) {
  try {
    const url = execSync('git remote get-url origin', { cwd: repoPath, encoding: 'utf8' }).trim();
    // git@github.com:wipcomputer/wip-grok.git or https://github.com/wipcomputer/wip-grok.git
    const match = url.match(/github\.com[:/](.+?)(?:\.git)?$/);
    return match ? match[1] : null;
  } catch {
    return null;
  }
}

// ── Stale Branch Check ──────────────────────────────────────────────

/**
 * Check for remote branches that are already merged into origin/main.
 * These should be cleaned up before releasing.
 *
 * For patch: WARN (non-blocking, just print stale branches).
 * For minor/major: BLOCK (return { failed: true }).
 *
 * Filters out origin/main, origin/HEAD, and already-renamed --merged- branches.
 */
export function checkStaleBranches(repoPath, level) {
  try {
    // Fetch latest remote state so --merged check is accurate
    try {
      execFileSync('git', ['fetch', '--prune'], { cwd: repoPath, stdio: 'pipe' });
    } catch {
      // Non-fatal: proceed with local state if fetch fails
    }

    const raw = execFileSync('git', ['branch', '-r', '--merged', 'origin/main'], {
      cwd: repoPath, encoding: 'utf8'
    }).trim();

    if (!raw) return { stale: [], ok: true };

    const stale = raw.split('\n')
      .map(b => b.trim())
      .filter(b =>
        b &&
        !b.includes('origin/main') &&
        !b.includes('origin/HEAD') &&
        !b.includes('--merged-')
      );

    if (stale.length === 0) return { stale: [], ok: true };

    const isMinorOrMajor = level === 'minor' || level === 'major';
    return {
      stale,
      ok: !isMinorOrMajor,
      blocked: isMinorOrMajor,
    };
  } catch {
    // Git command failed... skip check gracefully
    return { stale: [], ok: true, skipped: true };
  }
}

// ── Main ────────────────────────────────────────────────────────────

/**
 * Guard: wip-release must run from the main working tree on the main/master branch.
 *
 * Two independent conditions are enforced:
 *
 * 1. Linked worktree check: `git rev-parse --git-dir` of a linked worktree
 *    resolves to a path under `.git/worktrees/...`. If we see that, the caller
 *    is inside a feature worktree and must switch to the main working tree.
 * 2. Current branch check: even from the main working tree, `git branch
 *    --show-current` must be `main` or `master`. If a user checked out a feature
 *    branch in the main tree, the release would commit to the wrong branch.
 *
 * Both conditions bypassable via `--skip-worktree-check` for break-glass scenarios.
 *
 * Returns `{ ok: true }` on pass, or `{ ok: false, reason, currentPath, mainPath, branch }`
 * on fail so the caller can log and return the standard `{ failed: true }` shape.
 *
 * Related: `ai/product/bugs/guard/2026-04-05--cc-mini--guard-master-plan.md` Phase 3,
 * `ai/product/bugs/release-pipeline/2026-04-05--cc-mini--release-pipeline-master-plan.md`
 * Phase 1. Earlier today a wip-release alpha ran from a worktree branch because
 * `releasePrerelease` had no worktree check at all and the other two checks did
 * not cover the "main tree but non-main branch" case. This helper closes both gaps.
 */
function enforceMainBranchGuard(repoPath, skipWorktreeCheck) {
  if (skipWorktreeCheck) {
    return { ok: true, skipped: true };
  }
  try {
    const gitDir = execFileSync('git', ['rev-parse', '--git-dir'], {
      cwd: repoPath, encoding: 'utf8'
    }).trim();
    if (gitDir.includes('/worktrees/')) {
      const worktreeList = execFileSync('git', ['worktree', 'list', '--porcelain'], {
        cwd: repoPath, encoding: 'utf8'
      });
      const mainWorktree = worktreeList.split('\n')
        .find(line => line.startsWith('worktree '));
      const mainPath = mainWorktree ? mainWorktree.replace('worktree ', '') : '(unknown)';
      return {
        ok: false,
        reason: 'linked-worktree',
        currentPath: repoPath,
        mainPath,
      };
    }
    const branch = execFileSync('git', ['branch', '--show-current'], {
      cwd: repoPath, encoding: 'utf8'
    }).trim();
    if (branch && branch !== 'main' && branch !== 'master') {
      return {
        ok: false,
        reason: 'non-main-branch',
        currentPath: repoPath,
        branch,
      };
    }
    return { ok: true, branch };
  } catch {
    // Git command failed: skip check gracefully so release can still run
    // in CI or unusual environments where git plumbing is restricted.
    return { ok: true, skipped: true };
  }
}

/**
 * Validate that sub-tool package.json versions were bumped when their files changed.
 *
 * Scans `tools/*\/package.json` in monorepo-style toolboxes. For each sub-tool
 * whose files changed since the last git tag, verifies the package.json version
 * differs from the version at that tag. If not, this used to be a WARNING that
 * let the release proceed, which shipped at least one "committed but never
 * deployed" bug earlier today (guard 1.9.71 had new code but the same version,
 * so ldm install ignored the sub-tool on redeploy).
 *
 * Phase 8 of the release-pipeline master plan: WARNING becomes ERROR by default.
 * Callers who genuinely want to proceed without bumping (e.g., a release that
 * touches sub-tool files in a non-shipping way like CI config) pass
 * `allowSubToolDrift: true`.
 *
 * Returns `{ ok: true }` on pass, `{ ok: false }` if any sub-tool drift was
 * detected without the allow flag.
 *
 * Related: `ai/product/bugs/release-pipeline/2026-04-05--cc-mini--release-pipeline-master-plan.md`
 * Phase 8.
 */
/**
 * Phase 5: Auto-bump sub-tool patch versions when their files changed since last tag.
 * Called before validateSubToolVersions so drift is fixed before validation runs.
 * Returns the number of sub-tools bumped.
 */
function autoFixSubToolVersions(repoPath) {
  const toolsDir = join(repoPath, 'tools');
  if (!existsSync(toolsDir)) return 0;
  let lastTag = null;
  try {
    lastTag = execFileSync('git', ['describe', '--tags', '--abbrev=0'], {
      cwd: repoPath, encoding: 'utf8'
    }).trim();
  } catch {
    return 0;
  }
  if (!lastTag) return 0;

  let bumped = 0;
  let entries;
  try {
    entries = readdirSync(toolsDir, { withFileTypes: true });
  } catch {
    return 0;
  }
  for (const entry of entries) {
    if (!entry.isDirectory()) continue;
    const subDir = `tools/${entry.name}`;
    const subPkgPath = join(toolsDir, entry.name, 'package.json');
    if (!existsSync(subPkgPath)) continue;
    try {
      const diff = execFileSync('git', ['diff', '--name-only', lastTag, 'HEAD', '--', subDir], {
        cwd: repoPath, encoding: 'utf8'
      }).trim();
      if (!diff) continue;
      const subPkg = JSON.parse(readFileSync(subPkgPath, 'utf8'));
      const currentSubVersion = subPkg.version;
      let oldSubVersion = null;
      try {
        oldSubVersion = JSON.parse(
          execFileSync('git', ['show', `${lastTag}:${subDir}/package.json`], {
            cwd: repoPath, encoding: 'utf8'
          })
        ).version;
      } catch {}
      if (currentSubVersion === oldSubVersion) {
        const parts = currentSubVersion.split('.');
        parts[2] = String(Number(parts[2]) + 1);
        const newSubVersion = parts.join('.');
        subPkg.version = newSubVersion;
        writeFileSync(subPkgPath, JSON.stringify(subPkg, null, 2) + '\n');
        console.log(`  ✓ Auto-bumped ${entry.name}: ${currentSubVersion} -> ${newSubVersion}`);
        bumped++;
      }
    } catch (err) {
      console.log(`  ! Auto-bump failed for ${entry.name}: ${err.message}`);
    }
  }
  return bumped;
}

function validateSubToolVersions(repoPath, allowSubToolDrift) {
  const toolsDir = join(repoPath, 'tools');
  if (!existsSync(toolsDir)) {
    return { ok: true };
  }
  let lastTag = null;
  try {
    lastTag = execFileSync('git', ['describe', '--tags', '--abbrev=0'], {
      cwd: repoPath, encoding: 'utf8'
    }).trim();
  } catch {
    return { ok: true }; // No prior tag, nothing to compare against
  }
  if (!lastTag) return { ok: true };

  let driftDetected = false;
  let entries;
  try {
    entries = readdirSync(toolsDir, { withFileTypes: true });
  } catch {
    return { ok: true };
  }
  for (const entry of entries) {
    if (!entry.isDirectory()) continue;
    const subDir = join('tools', entry.name);
    const subPkgPath = join(toolsDir, entry.name, 'package.json');
    if (!existsSync(subPkgPath)) continue;
    try {
      const diff = execFileSync('git', ['diff', '--name-only', lastTag, 'HEAD', '--', subDir], {
        cwd: repoPath, encoding: 'utf8'
      }).trim();
      if (!diff) continue;
      const currentSubVersion = JSON.parse(readFileSync(subPkgPath, 'utf8')).version;
      let oldSubVersion = null;
      try {
        oldSubVersion = JSON.parse(
          execFileSync('git', ['show', `${lastTag}:${subDir}/package.json`], {
            cwd: repoPath, encoding: 'utf8'
          })
        ).version;
      } catch {}
      if (currentSubVersion === oldSubVersion) {
        if (allowSubToolDrift) {
          console.log(`  ! WARNING (allowed by --allow-sub-tool-drift): ${entry.name} has changed files since ${lastTag} but version is still ${currentSubVersion}`);
          console.log(`    Changed: ${diff.split('\n').join(', ')}`);
        } else {
          console.log(`  \u2717 ${entry.name} has changed files since ${lastTag} but tools/${entry.name}/package.json version is still ${currentSubVersion}.`);
          console.log(`    Changed: ${diff.split('\n').join(', ')}`);
          console.log(`    Bump tools/${entry.name}/package.json before releasing, or pass --allow-sub-tool-drift to override.`);
          console.log('');
          driftDetected = true;
        }
      }
    } catch {}
  }
  return { ok: !driftDetected };
}

/**
 * Pre-tag collision check. Returns `{ ok: true }` if no collision, otherwise
 * `{ ok: false, tag }` with a message logged. Phase 2 of the release-pipeline
 * master plan: earlier today `wip-release alpha` failed mid-pipeline because
 * `v1.9.71-alpha.4` and `v1.9.71-alpha.5` existed as local-only tags from
 * prior failed releases. The release tool has no recovery path; this helper
 * catches the collision before the bump+commit happens, so the user gets a
 * clear error and concrete recovery command instead of a mid-pipeline failure.
 */
function checkTagCollision(repoPath, newVersion) {
  const tag = `v${newVersion}`;
  try {
    const localTags = execFileSync('git', ['tag', '-l', tag], {
      cwd: repoPath, encoding: 'utf8'
    }).trim();
    if (localTags === tag) {
      // Tag exists locally. Is it also on remote?
      try {
        const remoteTags = execFileSync('git', ['ls-remote', '--tags', 'origin', tag], {
          cwd: repoPath, encoding: 'utf8'
        }).trim();
        if (remoteTags.includes(tag)) {
          // Tag is on remote: legitimate prior release. Refuse.
          console.log(`  \u2717 Tag ${tag} already exists on origin (prior release).`);
          console.log(`    Bump the version manually in package.json or run with a different level.`);
          console.log('');
          return { ok: false, tag, reason: 'on-remote' };
        }
      } catch {}
      // Tag exists locally but NOT on remote: stale leftover from a failed release.
      // Refuse with a concrete recovery command so the user knows this is safe to clean up.
      console.log(`  \u2717 Tag ${tag} exists locally but not on origin (stale leftover from a prior failed release).`);
      console.log(`    Safe to delete because it was never pushed. Recover with:`);
      console.log(`      git tag -d ${tag} && wip-release <track>`);
      console.log('');
      return { ok: false, tag, reason: 'stale-local' };
    }
  } catch {}
  return { ok: true };
}

/**
 * Push the release commit + tag, handling protected-main rejection via
 * automatic PR flow.
 *
 * If `git push origin main` succeeds directly, we also push tags and return.
 * If it fails with a "protected branch" error (GH006), create a temporary
 * release branch from the current HEAD, push the branch, open a PR targeting
 * main, auto-merge it via `gh pr merge --merge --delete-branch`, then push
 * the tag separately (tags bypass branch protection).
 *
 * Phase 4 of the release-pipeline master plan. Earlier today this entire
 * flow was done manually every time, adding 2-3 minutes per release.
 *
 * Returns `{ ok: true, via }` on success where `via` is `"direct"` or `"pr"`.
 * Returns `{ ok: false, reason, detail }` on failure; caller logs and
 * continues (matches prior non-fatal push behavior).
 */
function pushReleaseWithAutoPr(repoPath, newVersion, level) {
  const tag = `v${newVersion}`;
  // 1. Try direct push first. Most repos allow it.
  try {
    execFileSync('git', ['push'], { cwd: repoPath, stdio: 'pipe' });
    execFileSync('git', ['push', 'origin', tag], { cwd: repoPath, stdio: 'pipe' });
    return { ok: true, via: 'direct' };
  } catch (err) {
    const msg = String(err?.stderr ?? err?.message ?? err);
    const isProtected = /protected branch|GH006|Changes must be made through a pull request/i.test(msg);
    if (!isProtected) {
      return { ok: false, reason: 'push-failed', detail: msg };
    }
  }

  // 2. Protected main. Open auto-PR flow.
  const releaseBranch = `cc-mini/release-${tag}`;
  console.log(`  - Direct push to main refused (protected). Opening release PR...`);
  try {
    // Create branch at current HEAD
    execFileSync('git', ['branch', releaseBranch], { cwd: repoPath, stdio: 'pipe' });
    execFileSync('git', ['push', '-u', 'origin', releaseBranch], {
      cwd: repoPath, stdio: 'pipe'
    });
  } catch (err) {
    return {
      ok: false,
      reason: 'branch-push-failed',
      detail: String(err?.stderr ?? err?.message ?? err),
    };
  }

  // 3. Create and merge PR via gh CLI
  try {
    const prTitle = `release: ${tag}`;
    const prBody = `Release commit for ${tag} (${level}). Auto-generated by wip-release.`;
    execFileSync('gh', [
      'pr', 'create',
      '--base', 'main',
      '--head', releaseBranch,
      '--title', prTitle,
      '--body', prBody,
    ], { cwd: repoPath, stdio: 'pipe' });
    execFileSync('gh', [
      'pr', 'merge', releaseBranch,
      '--merge', '--delete-branch',
    ], { cwd: repoPath, stdio: 'pipe' });
    console.log(`  ✓ Release PR merged`);
  } catch (err) {
    return {
      ok: false,
      reason: 'gh-pr-failed',
      detail: String(err?.stderr ?? err?.message ?? err),
    };
  }

  // 4. Push the tag separately. Tags bypass branch protection on most
  //    GitHub setups, but if this fails the user can push the tag manually.
  try {
    execFileSync('git', ['push', 'origin', tag], { cwd: repoPath, stdio: 'pipe' });
    console.log(`  ✓ Pushed tag ${tag}`);
  } catch (err) {
    return {
      ok: false,
      reason: 'tag-push-failed',
      detail: String(err?.stderr ?? err?.message ?? err),
      partialSuccess: 'pr-merged',
    };
  }

  // 5. Pull latest main so local HEAD reflects the merge commit. This
  //    keeps subsequent git operations (like deploy-public) happy.
  try {
    execFileSync('git', ['fetch', 'origin', 'main'], { cwd: repoPath, stdio: 'pipe' });
    execFileSync('git', ['merge', '--ff-only', 'origin/main'], {
      cwd: repoPath, stdio: 'pipe'
    });
  } catch {
    // Non-fatal: main may have diverged (unlikely here). Deploy-public
    // will handle its own state.
  }

  return { ok: true, via: 'pr' };
}

function logPushFailure(result, tag) {
  console.log(`  ! Push failed: ${result.reason}`);
  if (result.detail) {
    console.log(`    ${result.detail.split('\n')[0]}`);
  }
  console.log(`  Manual recovery:`);
  if (result.reason === 'push-failed' || result.reason === 'branch-push-failed') {
    console.log(`    git push && git push origin ${tag}`);
  } else if (result.reason === 'gh-pr-failed') {
    console.log(`    Open a PR for cc-mini/release-${tag} targeting main, merge, then:`);
    console.log(`    git push origin ${tag}`);
  } else if (result.reason === 'tag-push-failed') {
    console.log(`    PR already merged. Just push the tag:`);
    console.log(`    git push origin ${tag}`);
  }
}

/**
 * Resolve the public GitHub repo name for a private-to-public mirror setup.
 *
 * Strategy:
 *   1. Read `origin` remote URL (e.g. git@github.com:owner/repo-private.git)
 *   2. Strip `-private` suffix to get the public repo name
 *   3. Return `owner/repo` format suitable for gh CLI
 *
 * Returns null if the remote URL cannot be parsed or the repo name does not
 * end in `-private` (in which case the caller should skip deploy-public as a
 * no-op rather than error).
 */
function resolvePublicRepoName(repoPath) {
  try {
    const remoteUrl = execFileSync('git', ['remote', 'get-url', 'origin'], {
      cwd: repoPath, encoding: 'utf8'
    }).trim();
    // Match owner/repo from either SSH (git@github.com:owner/repo.git) or HTTPS
    const match = remoteUrl.match(/github\.com[:/]([^/]+)\/(.+?)(\.git)?$/);
    if (!match) return null;
    const [, owner, repoName] = match;
    if (!repoName.endsWith('-private')) {
      return null;
    }
    return `${owner}/${repoName.replace(/-private$/, '')}`;
  } catch {
    return null;
  }
}

/**
 * Run deploy-public.sh as the final step of the release pipeline.
 *
 * Previously deploy-public was a separate manual step. Every release that
 * forgot it left the public mirror stale, so `ldm install` pulled old code
 * from the public repo. Now wip-release invokes it automatically for stable
 * and prerelease tracks (hotfix still skips, per prior convention).
 *
 * Callable with `--no-deploy-public` to opt out.
 *
 * Skips silently if:
 *   - The repo has no tools/deploy-public/deploy-public.sh (not a toolbox-
 *     style repo, or deploy-public is provided by a parent install)
 *   - The origin remote is not a -private repo (no public mirror to sync)
 *
 * Related: `ai/product/bugs/release-pipeline/2026-04-05--cc-mini--release-pipeline-master-plan.md` Phase 6.
 */
function runDeployPublic(repoPath, { skip } = {}) {
  if (skip) {
    return { ok: true, skipped: true, reason: 'flag' };
  }
  const scriptPath = join(repoPath, 'tools', 'deploy-public', 'deploy-public.sh');
  if (!existsSync(scriptPath)) {
    return { ok: true, skipped: true, reason: 'no-script' };
  }
  const publicRepo = resolvePublicRepoName(repoPath);
  if (!publicRepo) {
    return { ok: true, skipped: true, reason: 'not-private-repo' };
  }
  try {
    execFileSync('bash', [scriptPath, repoPath, publicRepo], {
      cwd: repoPath, stdio: 'inherit',
    });
    return { ok: true, publicRepo };
  } catch (err) {
    return {
      ok: false,
      detail: String(err?.stderr ?? err?.message ?? err),
      publicRepo,
    };
  }
}

function logMainBranchGuardFailure(result) {
  if (result.reason === 'linked-worktree') {
    console.log(`  \u2717 wip-release must run from the main working tree, not a worktree.`);
    console.log(`    Current: ${result.currentPath}`);
    console.log(`    Main working tree: ${result.mainPath}`);
    console.log(`    Switch to the main working tree and run again:`);
    console.log(`      cd ${result.mainPath} && wip-release <track>`);
  } else if (result.reason === 'non-main-branch') {
    console.log(`  \u2717 wip-release must run on the main branch, not a feature branch.`);
    console.log(`    Current branch: ${result.branch}`);
    console.log(`    Switch to main and pull latest:`);
    console.log(`      git checkout main && git pull && wip-release <track>`);
  }
  console.log('');
}

/**
 * Run the full release pipeline.
 */
export async function release({ repoPath, level, notes, notesSource, dryRun, noPublish, skipProductCheck, skipStaleCheck, skipWorktreeCheck, skipTechDocsCheck, skipCoverageCheck, allowSubToolDrift, noDeployPublic }) {
  repoPath = repoPath || process.cwd();
  const currentVersion = detectCurrentVersion(repoPath);
  const newVersion = bumpSemver(currentVersion, level);
  const repoName = basename(repoPath);

  console.log('');
  console.log(`  ${repoName}: ${currentVersion} -> ${newVersion} (${level})`);
  console.log(`  ${'─'.repeat(40)}`);

  // -1. Main-branch guard: block releases from linked worktrees or non-main branches
  {
    const guardResult = enforceMainBranchGuard(repoPath, skipWorktreeCheck);
    if (!guardResult.ok) {
      logMainBranchGuardFailure(guardResult);
      return { currentVersion, newVersion, dryRun: false, failed: true };
    }
    if (!guardResult.skipped) {
      console.log(`  \u2713 Running from main working tree on ${guardResult.branch ?? 'main'}`);
    }
  }

  // 0. License compliance gate (MANDATORY: blocks release if .license-guard.json missing)
  const configPath = join(repoPath, '.license-guard.json');
  if (!existsSync(configPath)) {
    console.log(`  ✗ .license-guard.json not found.`);
    console.log(`    Every repo must have .license-guard.json to release.`);
    console.log(`    Run: wip-repo-init   (scaffolds ai/, .license-guard.json, CLA.md)`);
    console.log(`    Or:  wip-license-guard init`);
    console.log('');
    return { currentVersion, newVersion, dryRun: false, failed: true };
  }
  {
    const config = JSON.parse(readFileSync(configPath, 'utf8'));
    const licenseIssues = [];

    const licensePath = join(repoPath, 'LICENSE');
    if (!existsSync(licensePath)) {
      licenseIssues.push('LICENSE file is missing');
    } else {
      const licenseText = readFileSync(licensePath, 'utf8');
      if (!licenseText.includes(config.copyright)) {
        licenseIssues.push(`LICENSE copyright does not match "${config.copyright}"`);
      }
      if (config.license === 'MIT+AGPL' && !licenseText.includes('AGPL') && !licenseText.includes('GNU Affero')) {
        licenseIssues.push('LICENSE is MIT-only but config requires MIT+AGPL');
      }
    }

    if (!existsSync(join(repoPath, 'CLA.md'))) {
      licenseIssues.push('CLA.md is missing');
    }

    const readmePath = join(repoPath, 'README.md');
    if (existsSync(readmePath)) {
      const readme = readFileSync(readmePath, 'utf8');
      if (!readme.includes('## License')) licenseIssues.push('README.md missing ## License section');
      if (config.license === 'MIT+AGPL' && !readme.includes('AGPL')) licenseIssues.push('README.md License section missing AGPL reference');
    }

    // .npmignore must exclude ai/ if repo has ai/ directory
    const aiDir = join(repoPath, 'ai');
    if (existsSync(aiDir)) {
      const npmignorePath = join(repoPath, '.npmignore');
      const pkgJson = JSON.parse(readFileSync(join(repoPath, 'package.json'), 'utf8'));
      const hasFilesWhitelist = Array.isArray(pkgJson.files);
      if (!hasFilesWhitelist) {
        if (!existsSync(npmignorePath)) {
          licenseIssues.push('.npmignore is missing (ai/ directory exists and could leak to npm)');
        } else {
          const npmignore = readFileSync(npmignorePath, 'utf8');
          if (!npmignore.includes('ai/')) {
            licenseIssues.push('.npmignore does not exclude ai/ (plans and bugs could leak to npm)');
          }
        }
      }
    }

    if (licenseIssues.length > 0) {
      console.log(`  ✗ License compliance failed:`);
      for (const issue of licenseIssues) console.log(`    - ${issue}`);
      console.log(`\n  Run \`wip-license-guard check --fix\` to auto-repair, then try again.`);
      console.log('');
      return { currentVersion, newVersion, dryRun: false, failed: true };
    }
    console.log(`  ✓ License compliance passed`);
  }

  // 0.5. Product docs check
  if (!skipProductCheck) {
    const productCheck = checkProductDocs(repoPath);
    if (!productCheck.skipped) {
      if (productCheck.ok) {
        console.log('  ✓ Product docs up to date');
      } else {
        const isMinorOrMajor = level === 'minor' || level === 'major';
        const prefix = isMinorOrMajor ? '✗' : '!';
        console.log(`  ${prefix} Product docs need attention:`);
        for (const m of productCheck.missing) console.log(`    - ${m}`);
        if (isMinorOrMajor) {
          console.log('');
          console.log('  Update product docs before a minor/major release.');
          console.log('  Use --skip-product-check to override.');
          console.log('');
          return { currentVersion, newVersion, dryRun: false, failed: true };
        }
      }
    }
  }

  // 0.75. Release notes quality gate
  {
    const notesCheck = checkReleaseNotes(notes, notesSource || 'flag', level);
    if (notesCheck.ok) {
      const sourceLabel = notesSource === 'file' ? 'from file' : notesSource === 'dev-update' ? 'from dev update' : 'from --notes';
      console.log(`  ✓ Release notes OK (${sourceLabel})`);
    } else {
      console.log(`  ✗ Release notes blocked:`);
      for (const issue of notesCheck.issues) console.log(`    - ${issue}`);
      console.log('');
      // Only scaffold on feature branches. On main, scaffolding leaves an
      // untracked file that branch guards prevent removing (#223).
      let currentBranch = '';
      try {
        currentBranch = execFileSync('git', ['branch', '--show-current'], {
          cwd: repoPath, encoding: 'utf8'
        }).trim();
      } catch {}

      const isProtectedBranch = currentBranch === 'main' || currentBranch === 'master';

      if (isProtectedBranch) {
        console.log(`  Release notes missing. Write RELEASE-NOTES-v${newVersion.replace(/\./g, '-')}.md on your feature branch before merging.`);
        console.log('');
        return { currentVersion, newVersion, dryRun: false, failed: true };
      }

      // Feature branch: scaffold a template so the agent has something to fill in
      const templatePath = scaffoldReleaseNotes(repoPath, newVersion);
      console.log(`  Scaffolded template: ${basename(templatePath)}`);
      console.log('  Fill it in, commit, then run wip-release again.');
      console.log('');
      return { currentVersion, newVersion, dryRun: false, failed: true };
    }
  }

  // 0.8. Stale remote branch check
  if (!skipStaleCheck) {
    const staleCheck = checkStaleBranches(repoPath, level);
    if (staleCheck.skipped) {
      // Silently skip if git command failed
    } else if (staleCheck.stale.length === 0) {
      console.log('  ✓ No stale remote branches');
    } else {
      const isMinorOrMajor = level === 'minor' || level === 'major';
      const prefix = isMinorOrMajor ? '✗' : '!';
      console.log(`  ${prefix} Stale remote branches merged into main:`);
      for (const b of staleCheck.stale) console.log(`    - ${b}`);
      if (isMinorOrMajor) {
        console.log('');
        console.log('  Clean up stale branches before a minor/major release.');
        console.log('  Delete them with: git push origin --delete <branch>');
        console.log('  Use --skip-stale-check to override.');
        console.log('');
        return { currentVersion, newVersion, dryRun: false, failed: true };
      }
    }
  }

  // 0.85. Technical docs check
  if (!skipTechDocsCheck) {
    const techDocsCheck = checkTechnicalDocs(repoPath);
    if (!techDocsCheck.skipped) {
      if (techDocsCheck.ok) {
        console.log('  ✓ Technical docs up to date');
      } else {
        const isMinorOrMajor = level === 'minor' || level === 'major';
        const prefix = isMinorOrMajor ? '✗' : '!';
        console.log(`  ${prefix} Technical docs need attention:`);
        for (const m of techDocsCheck.missing) console.log(`    - ${m}`);
        if (isMinorOrMajor) {
          console.log('');
          console.log('  Update SKILL.md or TECHNICAL.md before a minor/major release.');
          console.log('  Use --skip-tech-docs-check to override.');
          console.log('');
          return { currentVersion, newVersion, dryRun: false, failed: true };
        }
      }
    }
  }

  // 0.9. Interface coverage check
  if (!skipCoverageCheck) {
    const coverageCheck = checkInterfaceCoverage(repoPath);
    if (!coverageCheck.skipped) {
      if (coverageCheck.ok) {
        console.log('  ✓ Interface coverage table matches');
      } else {
        const isMinorOrMajor = level === 'minor' || level === 'major';
        const prefix = isMinorOrMajor ? '✗' : '!';
        console.log(`  ${prefix} Interface coverage table has mismatches:`);
        for (const m of coverageCheck.missing) console.log(`    - ${m}`);
        if (isMinorOrMajor) {
          console.log('');
          console.log('  Update the coverage table in README.md and SKILL.md.');
          console.log('  Use --skip-coverage-check to override.');
          console.log('');
          return { currentVersion, newVersion, dryRun: false, failed: true };
        }
      }
    }
  }

  // 0.95. Run test scripts (if any exist)
  {
    const toolsDir = join(repoPath, 'tools');
    const testFiles = [];
    if (existsSync(toolsDir)) {
      for (const sub of readdirSync(toolsDir)) {
        const testPath = join(toolsDir, sub, 'test.sh');
        if (existsSync(testPath)) testFiles.push({ tool: sub, path: testPath });
      }
    }
    // Also check repo root test.sh
    const rootTest = join(repoPath, 'test.sh');
    if (existsSync(rootTest)) testFiles.push({ tool: '(root)', path: rootTest });

    if (testFiles.length > 0) {
      let allPassed = true;
      for (const { tool, path } of testFiles) {
        try {
          execFileSync('bash', [path], { cwd: dirname(path), stdio: 'pipe', timeout: 30000 });
          console.log(`  ✓ Tests passed: ${tool}`);
        } catch (e) {
          allPassed = false;
          console.log(`  ✗ Tests FAILED: ${tool}`);
          const output = (e.stdout || '').toString().trim();
          if (output) {
            for (const line of output.split('\n').slice(-5)) console.log(`    ${line}`);
          }
        }
      }
      if (!allPassed) {
        console.log('');
        console.log('  Fix failing tests before releasing.');
        console.log('');
        return { currentVersion, newVersion, dryRun: false, failed: true };
      }
    }
  }

  if (dryRun) {
    // Product docs check (dry-run)
    if (!skipProductCheck) {
      const productCheck = checkProductDocs(repoPath);
      if (!productCheck.skipped) {
        if (productCheck.ok) {
          console.log('  [dry run] ✓ Product docs up to date');
        } else {
          const isMinorOrMajor = level === 'minor' || level === 'major';
          console.log(`  [dry run] ${isMinorOrMajor ? '✗ Would BLOCK' : '! Would WARN'}: product docs need updates`);
          for (const m of productCheck.missing) console.log(`    - ${m}`);
        }
      }
    }
    // Release notes check (dry-run)
    {
      const notesCheck = checkReleaseNotes(notes, notesSource || 'flag', level);
      if (notesCheck.ok) {
        const sourceLabel = notesSource === 'file' ? 'from file' : notesSource === 'dev-update' ? 'from dev update' : 'from --notes';
        console.log(`  [dry run] ✓ Release notes OK (${sourceLabel})`);
      } else {
        const isMinorOrMajor = level === 'minor' || level === 'major';
        console.log(`  [dry run] ${isMinorOrMajor ? '✗ Would BLOCK' : '! Would WARN'}: release notes need attention`);
        for (const issue of notesCheck.issues) console.log(`    - ${issue}`);
      }
    }
    // Stale branch check (dry-run)
    if (!skipStaleCheck) {
      const staleCheck = checkStaleBranches(repoPath, level);
      if (!staleCheck.skipped && staleCheck.stale.length > 0) {
        const isMinorOrMajor = level === 'minor' || level === 'major';
        console.log(`  [dry run] ${isMinorOrMajor ? '✗ Would BLOCK' : '! Would WARN'}: stale remote branches`);
        for (const b of staleCheck.stale) console.log(`    - ${b}`);
      } else if (!staleCheck.skipped) {
        console.log('  [dry run] ✓ No stale remote branches');
      }
    }
    // Technical docs check (dry-run)
    if (!skipTechDocsCheck) {
      const techDocsCheck = checkTechnicalDocs(repoPath);
      if (!techDocsCheck.skipped) {
        if (techDocsCheck.ok) {
          console.log('  [dry run] ✓ Technical docs up to date');
        } else {
          const isMinorOrMajor = level === 'minor' || level === 'major';
          console.log(`  [dry run] ${isMinorOrMajor ? '✗ Would BLOCK' : '! Would WARN'}: technical docs need updates`);
          for (const m of techDocsCheck.missing) console.log(`    - ${m}`);
        }
      }
    }
    // Interface coverage check (dry-run)
    if (!skipCoverageCheck) {
      const coverageCheck = checkInterfaceCoverage(repoPath);
      if (!coverageCheck.skipped) {
        if (coverageCheck.ok) {
          console.log('  [dry run] ✓ Interface coverage table matches');
        } else {
          const isMinorOrMajor = level === 'minor' || level === 'major';
          console.log(`  [dry run] ${isMinorOrMajor ? '✗ Would BLOCK' : '! Would WARN'}: interface coverage mismatches`);
          for (const m of coverageCheck.missing) console.log(`    - ${m}`);
        }
      }
    }
    const hasSkill = existsSync(join(repoPath, 'SKILL.md'));
    console.log(`  [dry run] Would bump package.json to ${newVersion}`);
    if (hasSkill) console.log(`  [dry run] Would update SKILL.md version`);
    console.log(`  [dry run] Would update CHANGELOG.md`);
    console.log(`  [dry run] Would commit and tag v${newVersion}`);
    if (!noPublish) {
      console.log(`  [dry run] Would publish to npm (@wipcomputer scope)`);
      console.log(`  [dry run] GitHub Packages: handled by deploy-public.sh`);
      console.log(`  [dry run] Would create GitHub release v${newVersion}`);
      if (hasSkill) console.log(`  [dry run] Would publish to ClawHub`);
      // Skill-to-website dry run (auto-detects SKILL.md, no config needed)
      if (hasSkill) {
        const envSet = !!process.env.WIP_WEBSITE_REPO;
        if (envSet) {
          // Resolve name same way as publishSkillToWebsite
          let dryName;
          const publishConfig = join(repoPath, '.publish-skill.json');
          if (existsSync(publishConfig)) {
            try { dryName = JSON.parse(readFileSync(publishConfig, 'utf8')).name; } catch {}
          }
          if (!dryName) {
            const pkgPath = join(repoPath, 'package.json');
            if (existsSync(pkgPath)) {
              try { dryName = JSON.parse(readFileSync(pkgPath, 'utf8')).name?.replace(/^@[^/]+\//, ''); } catch {}
            }
          }
          if (!dryName) dryName = basename(repoPath).replace(/-private$/, '').toLowerCase();
          console.log(`  [dry run] Would publish SKILL.md to website: install/${dryName}.txt`);
        } else {
          console.log(`  [dry run] Would publish SKILL.md to website but WIP_WEBSITE_REPO not set`);
        }
      }
    }
    console.log('');
    console.log(`  Dry run complete. No changes made.`);
    console.log('');
    return { currentVersion, newVersion, dryRun: true };
  }

  // 1.25. Pre-bump tag collision check (Phase 2).
  {
    const collision = checkTagCollision(repoPath, newVersion);
    if (!collision.ok) {
      return { currentVersion, newVersion, dryRun: false, failed: true };
    }
  }

  // 1. Bump package.json
  writePackageVersion(repoPath, newVersion);
  console.log(`  ✓ package.json -> ${newVersion}`);

  // 1.25. Auto-bump sub-tool versions (Phase 5: auto-fix before validation)
  {
    const autoBumped = autoFixSubToolVersions(repoPath);
    if (autoBumped > 0) {
      console.log(`  ✓ Auto-bumped ${autoBumped} sub-tool(s)`);
    }
  }

  // 1.5. Validate sub-tool version bumps (Phase 8: error by default)
  {
    const subToolResult = validateSubToolVersions(repoPath, allowSubToolDrift);
    if (!subToolResult.ok) {
      return { currentVersion, newVersion, dryRun: false, failed: true };
    }
  }

  // 2. Sync SKILL.md
  if (syncSkillVersion(repoPath, newVersion)) {
    console.log(`  ✓ SKILL.md -> ${newVersion}`);
  }

  // 3. Update CHANGELOG.md
  updateChangelog(repoPath, newVersion, notes);
  console.log(`  ✓ CHANGELOG.md updated`);

  // 3.5. Move RELEASE-NOTES-v*.md to _trash/
  const trashed = trashReleaseNotes(repoPath);
  if (trashed > 0) {
    console.log(`  ✓ Moved ${trashed} RELEASE-NOTES file(s) to _trash/`);
  }

  // 3.75. Auto-update product docs version/date
  const docsUpdated = syncProductDocs(repoPath, newVersion);
  if (docsUpdated > 0) {
    console.log(`  ✓ Product docs synced to v${newVersion} (${docsUpdated} file(s))`);
  }

  // Distribution results collector (#104)
  const distResults = [];

  // 4. npm publish BEFORE commit (Phase 3: true publish-before-commit)
  // Files are bumped and staged but NOT committed. If npm fails, we just
  // revert the file changes. No commit, no tag, no remote state to clean up.
  if (!noPublish) {
    try {
      publishNpm(repoPath);
      const pkg = JSON.parse(readFileSync(join(repoPath, 'package.json'), 'utf8'));
      distResults.push({ target: 'npm', status: 'ok', detail: `${pkg.name}@${newVersion}` });
      console.log(`  ✓ Published to npm`);
    } catch (e) {
      console.log(`  ✗ npm publish failed: ${e.message}`);
      console.log(`  Reverting file changes (no commit was made)...`);
      try {
        execSync('git checkout -- .', { cwd: repoPath, stdio: 'pipe' });
        // Clean up any new files (like trashed release notes)
        execSync('git clean -fd _trash/', { cwd: repoPath, stdio: 'pipe' });
        console.log(`  ✓ Reverted. Working tree is clean. Fix the issue and try again.`);
      } catch (revertErr) {
        console.log(`  ✗ Revert failed: ${revertErr.message}`);
        console.log(`  Manual cleanup: git checkout -- .`);
      }
      console.log('');
      return { currentVersion, newVersion, dryRun: false, failed: true };
    }

    // Phase 5: Auto-publish changed sub-tools to npm
    const toolsDir = join(repoPath, 'tools');
    if (existsSync(toolsDir)) {
      for (const tool of readdirSync(toolsDir)) {
        const toolPath = join(toolsDir, tool);
        const toolPkg = join(toolPath, 'package.json');
        if (!existsSync(toolPkg)) continue;
        const pkg = JSON.parse(readFileSync(toolPkg, 'utf8'));
        if (!pkg.name || pkg.private) continue;
        try {
          publishNpm(toolPath);
          distResults.push({ target: 'npm', status: 'ok', detail: `${pkg.name}@${pkg.version}` });
          console.log(`  ✓ Published sub-tool: ${pkg.name}@${pkg.version}`);
        } catch (e) {
          // Sub-tool publish failure is non-fatal but loud (Phase 7)
          const msg = e.message || '';
          if (msg.includes('previously published') || msg.includes('cannot publish over')) {
            // Already published at this version. Not an error.
          } else {
            distResults.push({ target: 'npm', status: 'failed', detail: `${pkg.name}: ${msg}` });
            console.log(`  ✗ Sub-tool ${pkg.name} publish failed: ${msg}`);
          }
        }
      }
    }
  }

  // 5. Git commit + tag (AFTER npm publish succeeds)
  gitCommitAndTag(repoPath, newVersion, notes);
  console.log(`  ✓ Committed and tagged v${newVersion}`);

  // 5.5. Push commit + tag
  {
    const pushResult = pushReleaseWithAutoPr(repoPath, newVersion, level);
    if (pushResult.ok) {
      console.log(`  ✓ Pushed to remote (${pushResult.via})`);
    } else {
      logPushFailure(pushResult, `v${newVersion}`);
    }
  }

  if (!noPublish) {
    // 7. GitHub Packages ... SKIPPED from private repos.
    // deploy-public.sh publishes to GitHub Packages from the public repo clone.
    // Publishing from private ties the package to the private repo, making it
    // invisible on the public repo's Packages tab. (#53)
    console.log(`  - GitHub Packages: handled by deploy-public.sh (from public repo)`);

    // 8. GitHub release
    try {
      createGitHubRelease(repoPath, newVersion, notes, currentVersion);
      distResults.push({ target: 'GitHub', status: 'ok', detail: `v${newVersion}` });
      console.log(`  ✓ GitHub release v${newVersion} created`);
    } catch (e) {
      distResults.push({ target: 'GitHub', status: 'failed', detail: e.message });
      console.log(`  ✗ GitHub release failed: ${e.message}`);
    }

    // 9. ClawHub skill publish (root + sub-tools)
    const rootSkill = join(repoPath, 'SKILL.md');
    const toolsDir = join(repoPath, 'tools');

    // Publish root SKILL.md
    if (existsSync(rootSkill)) {
      try {
        publishClawHub(repoPath, newVersion, notes);
        const slug = detectSkillSlug(repoPath);
        distResults.push({ target: `ClawHub`, status: 'ok', detail: `${slug}@${newVersion}` });
        console.log(`  ✓ Published to ClawHub: ${slug}`);
      } catch (e) {
        distResults.push({ target: 'ClawHub (root)', status: 'failed', detail: e.message });
        console.log(`  ✗ ClawHub publish failed: ${e.message}`);
      }
    }

    // Publish each sub-tool SKILL.md (#97)
    if (existsSync(toolsDir)) {
      for (const tool of readdirSync(toolsDir)) {
        const toolPath = join(toolsDir, tool);
        const toolSkill = join(toolPath, 'SKILL.md');
        if (existsSync(toolSkill)) {
          try {
            publishClawHub(toolPath, newVersion, notes);
            const slug = detectSkillSlug(toolPath);
            distResults.push({ target: `ClawHub`, status: 'ok', detail: `${slug}@${newVersion}` });
            console.log(`  ✓ Published to ClawHub: ${slug}`);
          } catch (e) {
            const slug = detectSkillSlug(toolPath);
            distResults.push({ target: `ClawHub (${slug})`, status: 'failed', detail: e.message });
            console.log(`  ✗ ClawHub publish failed for ${slug}: ${e.message}`);
          }
        }
      }
    }

    // 9.5. Publish SKILL.md to website as plain text
    const skillWebResult = publishSkillToWebsite(repoPath);
    if (skillWebResult.skipped) {
      // Silent skip ... no config or env var
    } else if (skillWebResult.ok) {
      const deployNote = skillWebResult.deployed ? '' : ' (copied, deploy skipped)';
      distResults.push({ target: 'Website', status: 'ok', detail: `install/${skillWebResult.target}.txt${deployNote}` });
      console.log(`  ✓ Published to website: install/${skillWebResult.target}.txt${deployNote}`);
      if (!skillWebResult.deployed && skillWebResult.error) {
        console.log(`    ! ${skillWebResult.error}`);
      }
    } else {
      distResults.push({ target: 'Website', status: 'failed', detail: skillWebResult.error });
      console.log(`  ✗ Website publish failed: ${skillWebResult.error}`);
    }
  }

  // Distribution summary (#104)
  if (distResults.length > 0) {
    console.log('');
    console.log('  Distribution:');
    for (const r of distResults) {
      const icon = r.status === 'ok' ? '✓' : '✗';
      console.log(`    ${icon} ${r.target}: ${r.detail}`);
    }
    const failed = distResults.filter(r => r.status !== 'ok');
    if (failed.length > 0) {
      console.log(`\n  ! ${failed.length} of ${distResults.length} target(s) failed.`);
    }
  }

  // 10. Post-merge branch cleanup: rename merged branches with --merged-YYYY-MM-DD
  try {
    const merged = execSync(
      'git branch --merged main', { cwd: repoPath, encoding: 'utf8' }
    ).split('\n')
      .map(b => b.trim())
      .filter(b => b && b !== 'main' && b !== 'master' && !b.startsWith('*') && !b.includes('--merged-'));

    if (merged.length > 0) {
      const current = execSync('git branch --show-current', { cwd: repoPath, encoding: 'utf8' }).trim();
      console.log(`  Scanning ${merged.length} merged branch(es) for rename...`);
      for (const branch of merged) {
        if (branch === current) continue;
        // Skip branches with characters that break git commands
        if (/[+\s~^:?*\[\]]/.test(branch)) continue;

        let mergeDate;
        try {
          // Use execFileSync (array args) instead of execSync (shell string) to avoid injection
          const mergeBase = execFileSync('git', ['merge-base', 'main', branch], { cwd: repoPath, encoding: 'utf8' }).trim();
          const logOutput = execFileSync('git', ['log', 'main', '--format=%ai', '--ancestry-path', `${mergeBase}..main`], { cwd: repoPath, encoding: 'utf8' }).trim();
          if (logOutput) mergeDate = logOutput.split('\n').pop().split(' ')[0];
        } catch {}
        if (!mergeDate) {
          try {
            mergeDate = execFileSync('git', ['log', branch, '-1', '--format=%ai'], { cwd: repoPath, encoding: 'utf8' }).trim().split(' ')[0];
          } catch {}
        }
        if (!mergeDate) continue;

        const newName = `${branch}--merged-${mergeDate}`;
        try {
          execFileSync('git', ['branch', '-m', branch, newName], { cwd: repoPath, stdio: 'pipe' });
          execFileSync('git', ['push', 'origin', newName], { cwd: repoPath, stdio: 'pipe' });
          // Remote branch may already be deleted by GitHub PR merge. That's fine.
          try { execFileSync('git', ['push', 'origin', '--delete', branch], { cwd: repoPath, stdio: 'pipe' }); } catch {}
          console.log(`  ✓ Renamed: ${branch} -> ${newName}`);
        } catch (e) {
          console.log(`  ! Could not rename ${branch}: ${e.message}`);
        }
      }
    }
  } catch (e) {
    // Non-fatal: branch cleanup is a convenience, not a blocker
    console.log(`  ! Branch cleanup skipped: ${e.message}`);
  }

  // 11. Prune old merged branches (keep last 3 per developer prefix)
  try {
    const KEEP_COUNT = 3;
    const remoteBranches = execSync(
      'git branch -r', { cwd: repoPath, encoding: 'utf8' }
    ).split('\n')
      .map(b => b.trim())
      .filter(b => b && !b.includes('HEAD') && b.includes('--merged-'))
      .map(b => b.replace('origin/', ''));

    if (remoteBranches.length > 0) {
      // Group by developer prefix (everything before first /)
      const byPrefix = {};
      for (const branch of remoteBranches) {
        const prefix = branch.split('/')[0];
        if (!byPrefix[prefix]) byPrefix[prefix] = [];
        byPrefix[prefix].push(branch);
      }

      let pruned = 0;
      for (const [prefix, branches] of Object.entries(byPrefix)) {
        // Sort by date descending (date is at the end: --merged-YYYY-MM-DD)
        branches.sort((a, b) => {
          const dateA = a.match(/--merged-(\d{4}-\d{2}-\d{2})/)?.[1] || '';
          const dateB = b.match(/--merged-(\d{4}-\d{2}-\d{2})/)?.[1] || '';
          return dateB.localeCompare(dateA);
        });

        for (let i = KEEP_COUNT; i < branches.length; i++) {
          try {
            execFileSync('git', ['push', 'origin', '--delete', branches[i]], { cwd: repoPath, stdio: 'pipe' });
            try { execFileSync('git', ['branch', '-d', branches[i]], { cwd: repoPath, stdio: 'pipe' }); } catch {}
            pruned++;
          } catch {}
        }
      }

      if (pruned > 0) {
        console.log(`  ✓ Pruned ${pruned} old merged branch(es)`);
      }
    }

    // Clean stale branches (merged into main but never renamed)
    const current = execSync('git branch --show-current', { cwd: repoPath, encoding: 'utf8' }).trim();
    const allRemote = execSync(
      'git branch -r', { cwd: repoPath, encoding: 'utf8' }
    ).split('\n')
      .map(b => b.trim())
      .filter(b => b && !b.includes('HEAD') && !b.includes('origin/main') && !b.includes('--merged-'))
      .map(b => b.replace('origin/', ''));

    let staleCleaned = 0;
    for (const branch of allRemote) {
      if (branch === current) continue;
      if (/[+\s~^:?*\[\]]/.test(branch)) continue;
      try {
        execFileSync('git', ['merge-base', '--is-ancestor', `origin/${branch}`, 'origin/main'], { cwd: repoPath, stdio: 'pipe' });
        // If we get here, branch is fully merged
        try { execFileSync('git', ['push', 'origin', '--delete', branch], { cwd: repoPath, stdio: 'pipe' }); } catch {}
        try { execFileSync('git', ['branch', '-d', branch], { cwd: repoPath, stdio: 'pipe' }); } catch {}
        staleCleaned++;
      } catch {}
    }
    if (staleCleaned > 0) {
      console.log(`  ✓ Cleaned ${staleCleaned} stale branch(es)`);
    }
  } catch (e) {
    console.log(`  ! Branch prune skipped: ${e.message}`);
  }

  // 12. Prune stale worktrees (#212)
  try {
    execSync('git worktree prune', { cwd: repoPath, stdio: 'pipe' });
    // Also check .worktrees/ for dirs whose branches are now merged
    const worktreesDir = join(dirname(repoPath), '.worktrees');
    if (existsSync(worktreesDir)) {
      const repoBase = basename(repoPath);
      const wtDirs = readdirSync(worktreesDir, { withFileTypes: true })
        .filter(d => d.isDirectory() && d.name.startsWith(repoBase + '--'));
      let wtPruned = 0;
      for (const d of wtDirs) {
        const wtPath = join(worktreesDir, d.name);
        try {
          // Check if branch is merged into main
          const branch = execSync('git branch --show-current', {
            cwd: wtPath, encoding: 'utf8', timeout: 3000
          }).trim();
          if (branch) {
            execSync(`git merge-base --is-ancestor "${branch}" main`, {
              cwd: repoPath, stdio: 'pipe', timeout: 5000
            });
            // Branch is merged. Remove worktree.
            execSync(`git worktree remove "${wtPath}"`, { cwd: repoPath, stdio: 'pipe' });
            wtPruned++;
          }
        } catch {} // Branch not merged or other issue, leave it
      }
      if (wtPruned > 0) {
        console.log(`  ✓ Pruned ${wtPruned} merged worktree(s) from .worktrees/`);
      }
    }
  } catch {}

  // Write release marker so branch guard blocks immediate install (#73)
  try {
    const markerDir = join(process.env.HOME || '', '.ldm', 'state');
    const { mkdirSync, writeFileSync } = await import('node:fs');
    mkdirSync(markerDir, { recursive: true });
    writeFileSync(join(markerDir, '.last-release'), JSON.stringify({
      repo: repoName,
      version: newVersion,
      timestamp: new Date().toISOString(),
    }) + '\n');
  } catch {}

  // 12. deploy-public: sync private -> public mirror (Phase 6)
  // Runs at the end of every stable release unless --no-deploy-public is set
  // or the repo has no deploy-public.sh script. Skips silently for non-
  // -private repos (no public mirror to sync).
  {
    const dp = runDeployPublic(repoPath, { skip: noDeployPublic });
    if (dp.skipped) {
      if (dp.reason === 'flag') {
        console.log(`  - deploy-public: skipped (--no-deploy-public)`);
      } else if (dp.reason === 'no-script') {
        console.log(`  - deploy-public: skipped (no tools/deploy-public/deploy-public.sh)`);
      } else if (dp.reason === 'not-private-repo') {
        console.log(`  - deploy-public: skipped (origin is not a -private repo)`);
      }
    } else if (dp.ok) {
      console.log(`  \u2713 deploy-public: synced to ${dp.publicRepo}`);
    } else {
      console.log(`  \u2717 deploy-public failed for ${dp.publicRepo}`);
      if (dp.detail) console.log(`    ${dp.detail.split('\n')[0]}`);
      console.log(`    Manual recovery: bash tools/deploy-public/deploy-public.sh ${repoPath} ${dp.publicRepo}`);
    }
  }

  console.log('');
  console.log(`  Done. ${repoName} v${newVersion} released.`);
  console.log('');

  return { currentVersion, newVersion, dryRun: false };
}

// ── Prerelease Track (Alpha / Beta) ────────────────────────────────

/**
 * Release an alpha or beta prerelease.
 *
 * Alpha: npm @alpha, no public release notes by default (opt in with publishReleaseNotes).
 * Beta:  npm @beta, prerelease notes on public repo by default (opt out with publishReleaseNotes=false).
 *
 * No deploy-public. No code sync. No CHANGELOG gate. No product docs gate.
 * Lightweight: bump version, npm publish with tag, optional GitHub prerelease.
 */
export async function releasePrerelease({ repoPath, track, notes, dryRun, noPublish, publishReleaseNotes, skipWorktreeCheck, allowSubToolDrift, noDeployPublic }) {
  repoPath = repoPath || process.cwd();
  const currentVersion = detectCurrentVersion(repoPath);
  const newVersion = bumpPrerelease(currentVersion, track);
  const repoName = basename(repoPath);

  console.log('');
  console.log(`  ${repoName}: ${currentVersion} -> ${newVersion} (${track})`);
  console.log(`  ${'─'.repeat(40)}`);

  // Main-branch guard: worktree + non-main branch check via shared helper.
  // Runs before the dry-run short-circuit so preview output from a feature
  // branch still refuses instead of printing a misleading "would bump" plan.
  {
    const guardResult = enforceMainBranchGuard(repoPath, skipWorktreeCheck);
    if (!guardResult.ok) {
      logMainBranchGuardFailure(guardResult);
      return { currentVersion, newVersion, dryRun: false, failed: true };
    }
    if (!guardResult.skipped) {
      console.log(`  \u2713 Running from main working tree on ${guardResult.branch ?? 'main'}`);
    }
  }

  // License compliance gate (MANDATORY: blocks release if .license-guard.json missing)
  {
    const configPath = join(repoPath, '.license-guard.json');
    if (!existsSync(configPath)) {
      console.log(`  \u2717 .license-guard.json not found.`);
      console.log(`    Every repo must have .license-guard.json to release.`);
      console.log(`    Run: wip-repo-init   (scaffolds ai/, .license-guard.json, CLA.md)`);
      console.log(`    Or:  wip-license-guard init`);
      console.log('');
      return { currentVersion, newVersion, dryRun: false, failed: true };
    }
    const config = JSON.parse(readFileSync(configPath, 'utf8'));
    const licenseIssues = [];
    const licensePath = join(repoPath, 'LICENSE');
    if (!existsSync(licensePath)) {
      licenseIssues.push('LICENSE file is missing');
    } else {
      const licenseText = readFileSync(licensePath, 'utf8');
      if (!licenseText.includes(config.copyright)) {
        licenseIssues.push(`LICENSE copyright does not match "${config.copyright}"`);
      }
      if (config.license === 'MIT+AGPL' && !licenseText.includes('AGPL') && !licenseText.includes('GNU Affero')) {
        licenseIssues.push('LICENSE is MIT-only but config requires MIT+AGPL');
      }
    }
    if (!existsSync(join(repoPath, 'CLA.md'))) {
      licenseIssues.push('CLA.md is missing');
    }
    const readmePath = join(repoPath, 'README.md');
    if (existsSync(readmePath)) {
      const readme = readFileSync(readmePath, 'utf8');
      if (!readme.includes('## License')) licenseIssues.push('README.md missing ## License section');
      if (config.license === 'MIT+AGPL' && !readme.includes('AGPL')) licenseIssues.push('README.md License section missing AGPL reference');
    }
    const aiDir = join(repoPath, 'ai');
    if (existsSync(aiDir)) {
      const npmignorePath = join(repoPath, '.npmignore');
      const pkgJson = JSON.parse(readFileSync(join(repoPath, 'package.json'), 'utf8'));
      const hasFilesWhitelist = Array.isArray(pkgJson.files);
      if (!hasFilesWhitelist) {
        if (!existsSync(npmignorePath)) {
          licenseIssues.push('.npmignore is missing (ai/ directory exists and could leak to npm)');
        } else {
          const npmignore = readFileSync(npmignorePath, 'utf8');
          if (!npmignore.includes('ai/')) {
            licenseIssues.push('.npmignore does not exclude ai/ (plans and bugs could leak to npm)');
          }
        }
      }
    }
    if (licenseIssues.length > 0) {
      console.log(`  \u2717 License compliance failed:`);
      for (const issue of licenseIssues) console.log(`    - ${issue}`);
      console.log(`\n  Run \`wip-license-guard check --fix\` to auto-repair, then try again.`);
      console.log('');
      return { currentVersion, newVersion, dryRun: false, failed: true };
    }
    console.log(`  \u2713 License compliance passed`);
  }

  if (dryRun) {
    console.log(`  [dry run] Would bump package.json to ${newVersion}`);
    if (!noPublish) {
      console.log(`  [dry run] Would npm publish with --tag ${track}`);
      if (publishReleaseNotes) {
        console.log(`  [dry run] Would create GitHub prerelease v${newVersion} on public repo`);
      } else {
        console.log(`  [dry run] No GitHub prerelease (silent)`);
      }
    }
    console.log('');
    console.log(`  Dry run complete. No changes made.`);
    console.log('');
    return { currentVersion, newVersion, dryRun: true };
  }

  // 1.25. Pre-bump tag collision check (Phase 2).
  {
    const collision = checkTagCollision(repoPath, newVersion);
    if (!collision.ok) {
      return { currentVersion, newVersion, dryRun: false, failed: true };
    }
  }

  // 1. Bump package.json
  writePackageVersion(repoPath, newVersion);
  console.log(`  \u2713 package.json -> ${newVersion}`);

  // 1.25. Auto-bump sub-tool versions (Phase 5)
  {
    const autoBumped = autoFixSubToolVersions(repoPath);
    if (autoBumped > 0) {
      console.log(`  \u2713 Auto-bumped ${autoBumped} sub-tool(s)`);
    }
  }

  // 1.5. Validate sub-tool version bumps (Phase 8: error by default)
  {
    const subToolResult = validateSubToolVersions(repoPath, allowSubToolDrift);
    if (!subToolResult.ok) {
      return { currentVersion, newVersion, dryRun: false, failed: true };
    }
  }

  // 2. Update CHANGELOG.md (lightweight entry)
  updateChangelog(repoPath, newVersion, notes || `${track} prerelease`);
  console.log(`  \u2713 CHANGELOG.md updated`);

  // 3. Git commit + tag
  const msg = `v${newVersion}: ${track} prerelease`;
  for (const f of ['package.json', 'CHANGELOG.md']) {
    if (existsSync(join(repoPath, f))) {
      execFileSync('git', ['add', f], { cwd: repoPath, stdio: 'pipe' });
    }
  }
  execFileSync('git', ['commit', '--no-verify', '-m', msg], { cwd: repoPath, stdio: 'pipe' });
  execFileSync('git', ['tag', `v${newVersion}`], { cwd: repoPath, stdio: 'pipe' });
  console.log(`  \u2713 Committed and tagged v${newVersion}`);

  // 4. Push commit + tag (with auto-PR fallback on protected main, Phase 4)
  {
    const pushResult = pushReleaseWithAutoPr(repoPath, newVersion, track);
    if (pushResult.ok) {
      console.log(`  \u2713 Pushed to remote (${pushResult.via})`);
    } else {
      logPushFailure(pushResult, `v${newVersion}`);
    }
  }

  const distResults = [];

  if (!noPublish) {
    // 5. npm publish with dist-tag
    try {
      publishNpmWithTag(repoPath, track);
      const pkg = JSON.parse(readFileSync(join(repoPath, 'package.json'), 'utf8'));
      distResults.push({ target: 'npm', status: 'ok', detail: `${pkg.name}@${newVersion} (tag: ${track})` });
      console.log(`  \u2713 Published to npm @${track}`);
    } catch (e) {
      distResults.push({ target: 'npm', status: 'failed', detail: e.message });
      console.log(`  \u2717 npm publish failed: ${e.message}`);
    }

    // 5.5. Auto-publish changed sub-tools to npm (Phase 5)
    const toolsDir = join(repoPath, 'tools');
    if (existsSync(toolsDir)) {
      for (const tool of readdirSync(toolsDir)) {
        const toolPath = join(toolsDir, tool);
        const toolPkg = join(toolPath, 'package.json');
        if (!existsSync(toolPkg)) continue;
        const pkg = JSON.parse(readFileSync(toolPkg, 'utf8'));
        if (!pkg.name || pkg.private) continue;
        try {
          publishNpm(toolPath);
          distResults.push({ target: 'npm', status: 'ok', detail: `${pkg.name}@${pkg.version}` });
          console.log(`  \u2713 Published sub-tool: ${pkg.name}@${pkg.version}`);
        } catch (e) {
          const msg = e.message || '';
          if (msg.includes('previously published') || msg.includes('cannot publish over')) {
            // Already published at this version. Not an error.
          } else {
            distResults.push({ target: 'npm', status: 'failed', detail: `${pkg.name}: ${msg}` });
            console.log(`  \u2717 Sub-tool ${pkg.name} publish failed: ${msg}`);
          }
        }
      }
    }

    // 6. GitHub prerelease on public repo (if opted in)
    if (publishReleaseNotes) {
      try {
        createGitHubPrerelease(repoPath, newVersion, notes || `${track} prerelease`);
        distResults.push({ target: 'GitHub', status: 'ok', detail: `v${newVersion} (prerelease)` });
        console.log(`  \u2713 GitHub prerelease v${newVersion} created on public repo`);
      } catch (e) {
        distResults.push({ target: 'GitHub', status: 'failed', detail: e.message });
        console.log(`  \u2717 GitHub prerelease failed: ${e.message}`);
      }
    } else {
      console.log(`  - GitHub prerelease: skipped (silent ${track})`);
    }
  }

  // Distribution summary
  if (distResults.length > 0) {
    console.log('');
    console.log('  Distribution:');
    for (const r of distResults) {
      const icon = r.status === 'ok' ? '\u2713' : '\u2717';
      console.log(`    ${icon} ${r.target}: ${r.detail}`);
    }
  }

  // deploy-public: sync private -> public mirror (Phase 6)
  // Beta: deploy to public (testing distribution pipeline)
  // Alpha: NEVER deploy to public (dev-only)
  if (track === 'alpha') {
    console.log(`  - deploy-public: skipped (alpha is dev-only, never goes to public)`);
  } else {
    const dp = runDeployPublic(repoPath, { skip: noDeployPublic });
    if (dp.skipped) {
      if (dp.reason === 'flag') {
        console.log(`  - deploy-public: skipped (--no-deploy-public)`);
      } else if (dp.reason === 'no-script') {
        console.log(`  - deploy-public: skipped (no deploy-public.sh)`);
      } else if (dp.reason === 'not-private-repo') {
        console.log(`  - deploy-public: skipped (origin is not a -private repo)`);
      }
    } else if (dp.ok) {
      console.log(`  \u2713 deploy-public: synced to ${dp.publicRepo}`);
    } else {
      console.log(`  \u2717 deploy-public failed for ${dp.publicRepo}`);
      if (dp.detail) console.log(`    ${dp.detail.split('\n')[0]}`);
      console.log(`    Manual recovery: bash tools/deploy-public/deploy-public.sh ${repoPath} ${dp.publicRepo}`);
    }
  }

  console.log('');
  console.log(`  Done. ${repoName} v${newVersion} (${track}) released.`);
  console.log('');

  return { currentVersion, newVersion, dryRun: false };
}

// ── Hotfix Track ────────────────────────────────────────────────────

/**
 * Release a hotfix.
 *
 * Same as stable patch but: no deploy-public, no code sync.
 * Publishes to npm @latest, creates GitHub release on public repo (opt out with publishReleaseNotes=false).
 *
 * Lighter gates than stable: no product docs check, no stale branch check.
 * Still runs: worktree guard, license compliance, tests.
 */
export async function releaseHotfix({ repoPath, notes, notesSource, dryRun, noPublish, publishReleaseNotes, skipWorktreeCheck, allowSubToolDrift }) {
  repoPath = repoPath || process.cwd();
  const currentVersion = detectCurrentVersion(repoPath);
  const newVersion = bumpSemver(currentVersion, 'patch');
  const repoName = basename(repoPath);

  console.log('');
  console.log(`  ${repoName}: ${currentVersion} -> ${newVersion} (hotfix)`);
  console.log(`  ${'─'.repeat(40)}`);

  // Main-branch guard: worktree + non-main branch check via shared helper
  {
    const guardResult = enforceMainBranchGuard(repoPath, skipWorktreeCheck);
    if (!guardResult.ok) {
      logMainBranchGuardFailure(guardResult);
      return { currentVersion, newVersion, dryRun: false, failed: true };
    }
    if (!guardResult.skipped) {
      console.log(`  \u2713 Running from main working tree on ${guardResult.branch ?? 'main'}`);
    }
  }

  // License compliance gate (MANDATORY: blocks release if .license-guard.json missing)
  {
    const configPath = join(repoPath, '.license-guard.json');
    if (!existsSync(configPath)) {
      console.log(`  \u2717 .license-guard.json not found.`);
      console.log(`    Every repo must have .license-guard.json to release.`);
      console.log(`    Run: wip-repo-init   (scaffolds ai/, .license-guard.json, CLA.md)`);
      console.log(`    Or:  wip-license-guard init`);
      console.log('');
      return { currentVersion, newVersion, dryRun: false, failed: true };
    }
    const config = JSON.parse(readFileSync(configPath, 'utf8'));
    const licenseIssues = [];
    const licensePath = join(repoPath, 'LICENSE');
    if (!existsSync(licensePath)) {
      licenseIssues.push('LICENSE file is missing');
    } else {
      const licenseText = readFileSync(licensePath, 'utf8');
      if (!licenseText.includes(config.copyright)) {
        licenseIssues.push(`LICENSE copyright does not match "${config.copyright}"`);
      }
    }
    if (!existsSync(join(repoPath, 'CLA.md'))) {
      licenseIssues.push('CLA.md is missing');
    }
    if (licenseIssues.length > 0) {
      console.log(`  \u2717 License compliance failed:`);
      for (const issue of licenseIssues) console.log(`    - ${issue}`);
      console.log('');
      return { currentVersion, newVersion, dryRun: false, failed: true };
    }
    console.log(`  \u2713 License compliance passed`);
  }

  // Release notes: hotfix accepts --notes flag as convenience (no file-only gate)
  if (!notes) {
    console.log(`  ! No release notes provided. Hotfix will have minimal notes.`);
    notes = 'Hotfix release.';
  }

  // Run tests if they exist
  {
    const toolsDir = join(repoPath, 'tools');
    const testFiles = [];
    if (existsSync(toolsDir)) {
      for (const sub of readdirSync(toolsDir)) {
        const testPath = join(toolsDir, sub, 'test.sh');
        if (existsSync(testPath)) testFiles.push({ tool: sub, path: testPath });
      }
    }
    const rootTest = join(repoPath, 'test.sh');
    if (existsSync(rootTest)) testFiles.push({ tool: '(root)', path: rootTest });

    if (testFiles.length > 0) {
      let allPassed = true;
      for (const { tool, path } of testFiles) {
        try {
          execFileSync('bash', [path], { cwd: dirname(path), stdio: 'pipe', timeout: 30000 });
          console.log(`  \u2713 Tests passed: ${tool}`);
        } catch (e) {
          allPassed = false;
          console.log(`  \u2717 Tests FAILED: ${tool}`);
          const output = (e.stdout || '').toString().trim();
          if (output) {
            for (const line of output.split('\n').slice(-5)) console.log(`    ${line}`);
          }
        }
      }
      if (!allPassed) {
        console.log('');
        console.log('  Fix failing tests before releasing.');
        console.log('');
        return { currentVersion, newVersion, dryRun: false, failed: true };
      }
    }
  }

  if (dryRun) {
    console.log(`  [dry run] Would bump package.json to ${newVersion}`);
    console.log(`  [dry run] Would update CHANGELOG.md`);
    if (!noPublish) {
      console.log(`  [dry run] Would npm publish with --tag latest`);
      if (publishReleaseNotes) {
        console.log(`  [dry run] Would create GitHub release v${newVersion} on public repo`);
      } else {
        console.log(`  [dry run] No GitHub release (--no-release-notes)`);
      }
      console.log(`  [dry run] No deploy-public (hotfix)`);
    }
    console.log('');
    console.log(`  Dry run complete. No changes made.`);
    console.log('');
    return { currentVersion, newVersion, dryRun: true };
  }

  // 1.25. Pre-bump tag collision check (Phase 2).
  {
    const collision = checkTagCollision(repoPath, newVersion);
    if (!collision.ok) {
      return { currentVersion, newVersion, dryRun: false, failed: true };
    }
  }

  // 1. Bump package.json
  writePackageVersion(repoPath, newVersion);
  console.log(`  \u2713 package.json -> ${newVersion}`);

  // 1.5. Validate sub-tool version bumps (Phase 8: error by default)
  {
    const subToolResult = validateSubToolVersions(repoPath, allowSubToolDrift);
    if (!subToolResult.ok) {
      return { currentVersion, newVersion, dryRun: false, failed: true };
    }
  }

  // 2. Sync SKILL.md
  if (syncSkillVersion(repoPath, newVersion)) {
    console.log(`  \u2713 SKILL.md -> ${newVersion}`);
  }

  // 3. Update CHANGELOG.md
  updateChangelog(repoPath, newVersion, notes);
  console.log(`  \u2713 CHANGELOG.md updated`);

  // 3.5. Move RELEASE-NOTES-v*.md to _trash/
  const trashed = trashReleaseNotes(repoPath);
  if (trashed > 0) {
    console.log(`  \u2713 Moved ${trashed} RELEASE-NOTES file(s) to _trash/`);
  }

  // 4. Git commit + tag
  gitCommitAndTag(repoPath, newVersion, notes);
  console.log(`  \u2713 Committed and tagged v${newVersion}`);

  // 5. Push commit + tag (with auto-PR fallback on protected main, Phase 4)
  {
    const pushResult = pushReleaseWithAutoPr(repoPath, newVersion, 'hotfix');
    if (pushResult.ok) {
      console.log(`  \u2713 Pushed to remote (${pushResult.via})`);
    } else {
      logPushFailure(pushResult, `v${newVersion}`);
    }
  }

  const distResults = [];

  if (!noPublish) {
    // 6. npm publish with @latest tag
    try {
      publishNpmWithTag(repoPath, 'latest');
      const pkg = JSON.parse(readFileSync(join(repoPath, 'package.json'), 'utf8'));
      distResults.push({ target: 'npm', status: 'ok', detail: `${pkg.name}@${newVersion}` });
      console.log(`  \u2713 Published to npm @latest`);
    } catch (e) {
      distResults.push({ target: 'npm', status: 'failed', detail: e.message });
      console.log(`  \u2717 npm publish failed: ${e.message}`);
    }

    // 7. GitHub release on public repo (not prerelease)
    if (publishReleaseNotes) {
      try {
        createGitHubReleaseOnPublic(repoPath, newVersion, notes, currentVersion);
        distResults.push({ target: 'GitHub', status: 'ok', detail: `v${newVersion}` });
        console.log(`  \u2713 GitHub release v${newVersion} created on public repo`);
      } catch (e) {
        distResults.push({ target: 'GitHub', status: 'failed', detail: e.message });
        console.log(`  \u2717 GitHub release failed: ${e.message}`);
      }
    } else {
      console.log(`  - GitHub release: skipped (--no-release-notes)`);
    }

    // No deploy-public for hotfix
    console.log(`  - deploy-public: skipped (hotfix)`);

    // 8. ClawHub skill publish
    const rootSkill = join(repoPath, 'SKILL.md');
    if (existsSync(rootSkill)) {
      try {
        publishClawHub(repoPath, newVersion, notes);
        const slug = detectSkillSlug(repoPath);
        distResults.push({ target: 'ClawHub', status: 'ok', detail: `${slug}@${newVersion}` });
        console.log(`  \u2713 Published to ClawHub: ${slug}`);
      } catch (e) {
        distResults.push({ target: 'ClawHub', status: 'failed', detail: e.message });
        console.log(`  \u2717 ClawHub publish failed: ${e.message}`);
      }
    }
  }

  // Distribution summary
  if (distResults.length > 0) {
    console.log('');
    console.log('  Distribution:');
    for (const r of distResults) {
      const icon = r.status === 'ok' ? '\u2713' : '\u2717';
      console.log(`    ${icon} ${r.target}: ${r.detail}`);
    }
  }

  // Write release marker
  try {
    const markerDir = join(process.env.HOME || '', '.ldm', 'state');
    mkdirSync(markerDir, { recursive: true });
    writeFileSync(join(markerDir, '.last-release'), JSON.stringify({
      repo: repoName,
      version: newVersion,
      timestamp: new Date().toISOString(),
      track: 'hotfix',
    }) + '\n');
  } catch {}

  console.log('');
  console.log(`  Done. ${repoName} v${newVersion} (hotfix) released.`);
  console.log('');

  return { currentVersion, newVersion, dryRun: false };
}

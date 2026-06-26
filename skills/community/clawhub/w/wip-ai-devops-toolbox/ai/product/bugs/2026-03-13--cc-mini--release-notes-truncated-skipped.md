# Bug: Release notes keep getting truncated or skipped in wip-release

**Filed by:** CC-Mini on 2026-03-13
**Severity:** High. Release notes are the public record of what changed. Losing them makes releases opaque.
**GitHub Issue:** #160 (https://github.com/wipcomputer/wip-ai-devops-toolbox-private/issues/160)
**Related closed issues:** #88, #127, #104 (partial fixes that didn't resolve the root causes)

---

## The Problem

Release notes are frequently truncated, empty ("Release."), or missing entirely from CHANGELOG.md and GitHub releases. Prior fixes (#88 cleaned up files, #127 added templates) addressed symptoms but not root causes.

## Root Causes (5 found)

### 1. Empty notes fallback (HIGH)
**File:** `tools/wip-release/core.mjs:93`
```javascript
const entry = `## ${newVersion} (${date})\n\n${notes || 'Release.'}\n`;
```
When `notes` is undefined, null, or empty string, CHANGELOG gets just "Release." No warning. No prompt.

### 2. Falsy detection in CLI (MEDIUM)
**File:** `tools/wip-release/cli.js:26`
```javascript
let notesSource = notes ? 'flag' : 'none';
```
`--notes=""` is falsy, so auto-detection tries to find RELEASE-NOTES-v*.md or dev-updates. If those don't exist either, notes stays empty. The chain: `--notes=""` -> notesSource='none' -> no fallback found -> empty notes used everywhere.

### 3. Blank line accumulation in CHANGELOG (LOW)
**File:** `tools/wip-release/core.mjs:104-105`
Extra `\n` before and after the entry causes blank lines to accumulate. Current CHANGELOG has 27 blank lines at the top.

### 4. Malformed install section in GitHub release (LOW)
**File:** `tools/wip-release/core.mjs:398`
`lines.push('### Install\n')` with trailing `\n` in the string, then joined with `\n` again. Creates double-spaced markdown.

### 5. Silent GitHub release failure (CRITICAL)
**File:** `tools/wip-release/core.mjs:957-963`
If `createGitHubRelease` fails silently (no exception thrown), it reports success. The catch block only fires on thrown exceptions. Silent failures look like success in the output.

## What Needs to Change

1. **Require notes.** If `--notes` is empty and no RELEASE-NOTES-v*.md or dev-update file exists, wip-release should error out (or warn loudly and prompt), not silently default to "Release."
2. **Fix the falsy check.** Use `notes !== undefined && notes !== ''` instead of truthiness.
3. **Clean up blank line insertion.** Remove the extra `\n` wrappers in the CHANGELOG write.
4. **Remove trailing `\n` from line pushes.** The join handles newlines.
5. **Validate GitHub release creation.** After `gh release create`, verify the release exists with `gh release view`. If it doesn't, report failure.

## Reproduction

Run `wip-release patch` without `--notes` and without a RELEASE-NOTES-v*.md file. The CHANGELOG entry will say "Release." and the GitHub release body will have minimal/no notes.

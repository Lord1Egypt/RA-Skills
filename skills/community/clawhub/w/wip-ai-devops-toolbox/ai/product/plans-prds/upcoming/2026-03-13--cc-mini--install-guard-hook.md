# Plan: Install Guard Hook (prevent accidental deploys to extensions)

**Date:** 2026-03-13
**Author:** CC-Mini + Parker
**Priority:** High (prevents the exact mistake that happened today)

## The Problem

Agents bypass the dogfooding flow by copying files directly to extension directories (`~/.ldm/extensions/`, `~/.openclaw/extensions/`) or running `npm install -g` / `npm link` after a release. This collapses Deploy and Install into one step.

## What This Does

A Claude Code Bash hook that intercepts commands touching extension directories and blocks them unless Parker explicitly overrides.

## Commands to Block

```
cp * ~/.ldm/extensions/
cp * ~/.openclaw/extensions/
npm install -g memory-crystal
npm install -g @wipcomputer/*
npm link (inside any -private repo)
```

## How It Works

Add to `~/.claude/settings.json` hooks (PreToolUse:Bash):

```javascript
// install-guard.mjs
// Blocks commands that deploy to extension directories or install globally
const cmd = process.env.CLAUDE_BASH_COMMAND || '';

const BLOCKED_PATTERNS = [
  /cp\s.*~?\/?\.ldm\/extensions\//,
  /cp\s.*~?\/?\.openclaw\/extensions\//,
  /npm\s+install\s+-g/,
  /npm\s+link/,
];

for (const pattern of BLOCKED_PATTERNS) {
  if (pattern.test(cmd)) {
    console.error('BLOCKED: This command installs to the live system.');
    console.error('Deploy and Install are separate steps. Deploy publishes to npm/GitHub.');
    console.error('Install only happens when Parker says "install" through the install prompt.');
    process.exit(2);
  }
}
```

## Override

Parker can bypass by running the command himself in a terminal, or by temporarily disabling the hook. The hook only blocks Claude Code agents, not manual terminal commands.

## Files

| File | Change |
|------|--------|
| `tools/wip-install-guard/guard.mjs` (NEW) | The hook script |
| `~/.claude/settings.json` | Add PreToolUse:Bash hook entry |

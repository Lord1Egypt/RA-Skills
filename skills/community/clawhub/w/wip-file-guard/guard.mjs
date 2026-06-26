#!/usr/bin/env node
// cc-file-guard/guard.mjs
// PreToolUse hook for Claude Code.
// Blocks destructive edits to protected files.
// - Blocks Write tool on protected files entirely
// - Blocks Edit when net line removal > 2 lines

import { basename, dirname, join } from 'node:path';
import { existsSync, readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';

if (process.argv.includes('--version') || process.argv.includes('-v')) {
  const __dirname = dirname(fileURLToPath(import.meta.url));
  const pkg = JSON.parse(readFileSync(join(__dirname, 'package.json'), 'utf8'));
  console.log(pkg.version);
  process.exit(0);
}

// Exact basename matches
export const PROTECTED = new Set([
  'CLAUDE.md',
  'SHARED-CONTEXT.md',
  'SOUL.md',
  'IDENTITY.md',
  'CONTEXT.md',
  'TOOLS.md',
  'MEMORY.md',
]);

// Pattern matches (case-insensitive, checked against full path and basename)
export const PROTECTED_PATTERNS = [
  /memory/i,
  /memories/i,
  /journal/i,
  /diary/i,
  /daily.*log/i,
];

// Shared state files: protected from Write but allow larger Edit replacements.
// These are actively edited by both agents every session.
const SHARED_STATE_FILES = new Set([
  'SHARED-CONTEXT.md',
]);

// Daily logs and workspace memory: allow creation and larger edits
const SHARED_STATE_PATHS = [
  /\.openclaw\/workspace\//,                   // OpenClaw agent workspace (live shared state, not code)
  /workspace\/memory\/\d{4}-\d{2}-\d{2}\.md$/,
  /\.ldm\/agents\/.*\/memory\/daily\/.*\.md$/,
  /\.ldm\/memory\/daily\/.*\.md$/,
  /\.ldm\/memory\/shared-log\.jsonl$/,
  /\.claude\/projects\/.*\/memory\/.*\.md$/,  // harness auto-memory files
  /\.claude\/memory\/.*\.md$/,                 // harness global memory files
];

function isSharedState(filePath) {
  const name = basename(filePath);
  if (SHARED_STATE_FILES.has(name)) return true;
  return SHARED_STATE_PATHS.some(p => p.test(filePath));
}

function isProtected(filePath) {
  const name = basename(filePath);
  if (PROTECTED.has(name)) return name;
  for (const pattern of PROTECTED_PATTERNS) {
    if (pattern.test(filePath)) return name + ` (matched pattern: ${pattern})`;
  }
  return null;
}

function deny(reason) {
  const output = {
    hookSpecificOutput: {
      hookEventName: 'PreToolUse',
      permissionDecision: 'deny',
      permissionDecisionReason: reason,
    },
  };
  process.stdout.write(JSON.stringify(output));
}

function countLines(str) {
  if (!str) return 0;
  return str.split('\n').length;
}

// CLI mode: node guard.mjs --list
if (process.argv.includes('--list')) {
  console.log('Protected files (exact):');
  for (const f of PROTECTED) console.log(`  ${f}`);
  console.log('Protected patterns:');
  for (const p of PROTECTED_PATTERNS) console.log(`  ${p}`);
  process.exit(0);
}

async function main() {
  let raw = '';
  for await (const chunk of process.stdin) {
    raw += chunk;
  }

  let input;
  try {
    input = JSON.parse(raw);
  } catch {
    // Can't parse input, allow by default
    process.exit(0);
  }

  const toolName = input.tool_name || '';
  const toolInput = input.tool_input || {};
  const filePath = toolInput.file_path || toolInput.filePath || '';
  const fileName = basename(filePath);

  // Only check protected files
  const match = isProtected(filePath);
  if (!match) {
    process.exit(0);
  }

  // Block Write on protected files
  // Path-based shared state (workspace, harness memory, daily logs): always allow Write
  // Exact matches outside shared state paths: block Write (use Edit instead)
  // Pattern matches: only block if file already exists (allow creating new files)
  if (toolName === 'Write') {
    // Path-based shared state gets Write access (workspace files, harness memory).
    // Checked before exact-match so workspace TOOLS.md/MEMORY.md are writable.
    // Name-based shared state (SHARED_STATE_FILES) still goes through exact-match
    // to prevent accidental overwrites of SHARED-CONTEXT.md outside known paths.
    if (SHARED_STATE_PATHS.some(p => p.test(filePath))) {
      process.exit(0);
    }
    const isExactMatch = PROTECTED.has(fileName);
    if (isExactMatch) {
      // Allow creating NEW protected files in worktrees (file doesn't exist yet).
      // Still block overwriting existing protected files in worktrees.
      const inWorktree = filePath.includes('/.worktrees/') || filePath.includes('/_worktrees/');
      if (inWorktree && !existsSync(filePath)) {
        process.exit(0);
      }
      deny(`BLOCKED: Write tool on ${match} is not allowed. Use Edit to make specific changes. Never overwrite protected files.`);
      process.exit(0);
    }
    // Other pattern matches: block if file exists, allow creation of new files
    if (existsSync(filePath)) {
      deny(`BLOCKED: Write tool on ${match} is not allowed. Use Edit to make specific changes. Never overwrite protected files.`);
      process.exit(0);
    }
    // Pattern match but file doesn't exist yet ... allow creation
    process.exit(0);
  }

  // For Edit, check line removal AND large replacements
  if (toolName === 'Edit') {
    const oldString = toolInput.old_string || '';
    const newString = toolInput.new_string || '';
    const oldLines = countLines(oldString);
    const newLines = countLines(newString);
    const removed = oldLines - newLines;

    // Shared state files get higher limits (updated every session by both agents)
    const isShared = isSharedState(filePath);
    const maxRemoval = isShared ? 20 : 2;
    const maxReplace = isShared ? 30 : 4;

    // Block net removal beyond limit
    if (removed > maxRemoval) {
      deny(`BLOCKED: You are removing ${removed} lines from ${match} (old: ${oldLines} lines, new: ${newLines} lines). Re-read the file and add content instead of replacing it.`);
      process.exit(0);
    }

    // Block large replacements (swapping big chunks even if line count is similar)
    if (oldLines > maxReplace && oldString !== newString) {
      deny(`BLOCKED: You are replacing ${oldLines} lines in ${match}. Edit smaller sections or append new content instead of replacing existing content.`);
      process.exit(0);
    }
  }

  // Allow
  process.exit(0);
}

main().catch(() => process.exit(0));

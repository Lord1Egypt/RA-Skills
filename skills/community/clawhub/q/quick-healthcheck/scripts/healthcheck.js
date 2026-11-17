#!/usr/bin/env node
const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const WORKSPACE = path.resolve(__dirname, '../../..');

function run(cmd, opts = {}) {
  try {
    return execSync(cmd, { encoding: 'utf8', cwd: WORKSPACE, ...opts }).trim();
  } catch (e) {
    return `[error: ${e.message.split('\n')[0]}]`;
  }
}

const result = {
  timestamp: new Date().toISOString(),
  openclaw_version: run('openclaw --version').replace('openclaw/', '').trim(),
  git_branch: run('git branch --show-current'),
  git_uncommitted: run('git status --porcelain').split('\n').filter(Boolean).length,
  recent_memories: [],
  todo_count: 0,
  workspace_size_mb: null,
};

// Recent memory files
try {
  const memDir = path.join(WORKSPACE, 'memory');
  if (fs.existsSync(memDir)) {
    const files = fs.readdirSync(memDir)
      .filter(f => f.endsWith('.md'))
      .map(f => ({ name: f, mtime: fs.statSync(path.join(memDir, f)).mtime }))
      .sort((a, b) => b.mtime - a.mtime)
      .slice(0, 3);
    result.recent_memories = files.map(f => f.name);
  }
} catch (e) {
  result.recent_memories = ['[error reading memories]'];
}

// TODO/FIXME count
try {
  const grep = run("grep -rE 'TODO|FIXME' skills/ memory/ --include='*.md' --include='*.js' --include='*.py' 2>/dev/null | wc -l");
  result.todo_count = parseInt(grep, 10) || 0;
} catch (e) {
  result.todo_count = -1;
}

// Workspace size
try {
  const sizeLines = run(`du -sm ${WORKSPACE} 2>/dev/null || du -sm "${WORKSPACE}" 2>/dev/null`).split('\t');
  result.workspace_size_mb = parseInt(sizeLines[0], 10) || null;
} catch (e) {
  result.workspace_size_mb = null;
}

console.log(JSON.stringify(result, null, 2));

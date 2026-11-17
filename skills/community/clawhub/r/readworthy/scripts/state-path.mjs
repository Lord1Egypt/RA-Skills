#!/usr/bin/env node

import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

export function resolveStateDir() {
  if (process.env.READWORTHY_STATE_DIR) {
    return path.resolve(process.env.READWORTHY_STATE_DIR);
  }
  const codexRoot = process.env.CODEX_HOME
    ? path.resolve(process.env.CODEX_HOME)
    : path.join(os.homedir(), '.codex');
  return path.join(codexRoot, 'readworthy', 'state');
}

export function statePaths() {
  const stateDir = resolveStateDir();
  return {
    stateDir,
    manifest: path.join(stateDir, 'state.json'),
    profile: path.join(stateDir, 'profile.json'),
    index: path.join(stateDir, 'index.json'),
    insights: path.join(stateDir, 'insights.json'),
    events: path.join(stateDir, 'events.jsonl'),
    articles: path.join(stateDir, 'articles'),
    backups: path.join(stateDir, 'backups'),
  };
}

const invokedPath = process.argv[1] ? path.resolve(process.argv[1]) : '';
if (invokedPath === fileURLToPath(import.meta.url)) {
  console.log(JSON.stringify({ state_dir: resolveStateDir() }));
}

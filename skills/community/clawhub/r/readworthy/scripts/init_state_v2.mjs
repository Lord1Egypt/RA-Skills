#!/usr/bin/env node

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { statePaths } from './state-path.mjs';

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const templateDir = path.join(path.dirname(scriptDir), 'assets', 'state-template');
const paths = statePaths();

fs.mkdirSync(paths.stateDir, { recursive: true });
fs.mkdirSync(paths.articles, { recursive: true });
fs.mkdirSync(paths.backups, { recursive: true });

const templates = [
  ['state.json', paths.manifest],
  ['profile.json', paths.profile],
  ['index.json', paths.index],
  ['insights.json', paths.insights],
];
const created = [];
for (const [sourceName, targetPath] of templates) {
  if (!fs.existsSync(targetPath)) {
    fs.copyFileSync(path.join(templateDir, sourceName), targetPath);
    created.push(path.basename(targetPath));
  }
}
if (!fs.existsSync(paths.events)) {
  fs.writeFileSync(paths.events, '');
  created.push('events.jsonl');
}

console.log(JSON.stringify({ ok: true, state_dir: paths.stateDir, created }));

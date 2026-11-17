#!/usr/bin/env node

import fs from 'node:fs';
import path from 'node:path';
import { statePaths } from './state-path.mjs';

const paths = statePaths();
for (const required of [paths.manifest, paths.profile, paths.index, paths.insights, paths.events, paths.articles]) {
  if (!fs.existsSync(required)) {
    throw new Error('Readworthy state is not initialized. Run node scripts/init_state_v2.mjs first.');
  }
}

const timestamp = new Date().toISOString().replaceAll(':', '-').replaceAll('.', '-');
const label = (process.argv[2] ?? 'write').replaceAll(/[^a-zA-Z0-9_-]/g, '-');
const backupDir = path.join(paths.backups, `${timestamp}-${label}`);
fs.mkdirSync(backupDir, { recursive: true });

for (const source of [paths.manifest, paths.profile, paths.index, paths.insights, paths.events]) {
  fs.copyFileSync(source, path.join(backupDir, path.basename(source)));
}
fs.cpSync(paths.articles, path.join(backupDir, 'articles'), { recursive: true });

console.log(JSON.stringify({ ok: true, backup_dir: backupDir }));

#!/usr/bin/env node
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { verify } from './task-sync-pack.mjs';

async function main() {
  const [zipPath, ...rest] = process.argv.slice(2);
  if (!zipPath || rest.length) throw new Error('用法：node scripts/verify-task-sync-pack.mjs <任务.task-sync.zip>');
  process.stdout.write(`${JSON.stringify(await verify(zipPath))}\n`);
}

const invokedPath = process.argv[1] && path.resolve(process.argv[1]);
if (invokedPath === fileURLToPath(import.meta.url)) {
  main().catch((error) => {
    process.stderr.write(`task-sync-pack verify: ${error.message}\n`);
    process.exitCode = 1;
  });
}

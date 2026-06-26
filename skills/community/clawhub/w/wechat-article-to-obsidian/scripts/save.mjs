#!/usr/bin/env node
import fs from 'node:fs/promises';
import path from 'node:path';
import process from 'node:process';

function parseArgs(argv) {
  const args = {};
  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    if (!arg.startsWith('--')) continue;
    const key = arg.slice(2);
    const value = argv[i + 1];
    if (value === undefined || value.startsWith('--')) {
      args[key] = 'true';
      continue;
    }
    args[key] = value;
    i += 1;
  }
  return args;
}

function sanitizeFilename(name) {
  return (name || 'wechat-article')
    .replace(/[\\/:*?"<>|]/g, '')
    .replace(/\s+/g, ' ')
    .trim()
    .replace(/\.+$/g, '') || 'wechat-article';
}

function safeRelativeNotePath(targetPath, filename) {
  const cleanTarget = (targetPath || '').replace(/^\/+|\/+$/g, '');
  const cleanFile = `${sanitizeFilename(filename)}.md`;
  const combined = cleanTarget ? path.posix.join(cleanTarget, cleanFile) : cleanFile;
  const normalized = path.posix.normalize(combined);
  if (normalized.startsWith('../') || normalized === '..' || path.posix.isAbsolute(normalized)) {
    throw new Error(`Unsafe target path: ${targetPath}`);
  }
  return normalized;
}

async function writeNoteToVault({ markdown, config, notePath }) {
  if (!config.vault_disk_root) {
    throw new Error('vault_disk_root is required for safe direct-write saving');
  }

  const fullPath = path.resolve(config.vault_disk_root, ...notePath.split('/'));
  const relativeToRoot = path.relative(config.vault_disk_root, fullPath);
  if (relativeToRoot.startsWith('..') || path.isAbsolute(relativeToRoot)) {
    throw new Error(`Unsafe resolved path outside vault root: ${fullPath}`);
  }

  await fs.mkdir(path.dirname(fullPath), { recursive: true });
  await fs.writeFile(fullPath, markdown, 'utf8');
  return fullPath;
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const markdownPath = args.markdown;
  const configPath = args.config;
  const title = args.title;
  const targetPath = args['target-path'];

  if (!markdownPath || !configPath || !title) {
    throw new Error('Usage: save.mjs --markdown <file> --config <config.json> --title <title> [--target-path <path>]');
  }

  const markdown = await fs.readFile(markdownPath, 'utf8');
  const config = JSON.parse(await fs.readFile(configPath, 'utf8'));
  const notePath = safeRelativeNotePath(targetPath || config.default_path || 'notes/wechat', title);
  const fullPath = await writeNoteToVault({ markdown, config, notePath });

  console.log(JSON.stringify({
    method: 'direct-write',
    notePath,
    fullPath,
  }, null, 2));
}

main().catch((error) => {
  console.error(error.stack || String(error));
  process.exit(1);
});

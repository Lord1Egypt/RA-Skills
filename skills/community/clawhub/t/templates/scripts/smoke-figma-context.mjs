#!/usr/bin/env node

import { pathToFileURL } from 'node:url';

import { defaultCreateClient, runReadFigmaContext } from './read-figma-context.mjs';

function ensureRequireScreenshots(argv) {
  return argv.includes('--require-screenshots') ? argv : [...argv, '--require-screenshots'];
}

function withMePreflight(client) {
  let preflight = null;
  function ensureMe() {
    if (!preflight) {
      preflight = client.getMe();
    }
    return preflight;
  }

  return {
    ...client,
    async getNode(...args) {
      await ensureMe();
      return client.getNode(...args);
    },
    async getFile(...args) {
      await ensureMe();
      return client.getFile(...args);
    },
    async exportNodeImage(...args) {
      await ensureMe();
      return client.exportNodeImage(...args);
    },
  };
}

export async function runSmoke(argv = process.argv, options = {}) {
  const createClient = options.createClient ?? defaultCreateClient;
  const result = await runReadFigmaContext({
    argv: ensureRequireScreenshots(argv),
    cwd: options.cwd,
    env: options.env,
    now: options.now,
    createClient(config) {
      return withMePreflight(createClient(config));
    },
  });
  if (result.exitCode === 0) {
    return {
      ...result,
      code: 'smoke_succeeded',
    };
  }
  return {
    ...result,
    code: result.code === 'completed' ? 'smoke_failed' : result.code,
  };
}

async function main() {
  const result = await runSmoke(process.argv);
  if (result.exitCode === 0) {
    process.stdout.write(`${JSON.stringify({ code: result.code, runDir: result.runDir, runDirRelative: result.runDirRelative }, null, 2)}\n`);
    return;
  }
  console.error(result.code);
  if (result.runDir) {
    console.error(`runDir: ${result.runDir}`);
  }
  if (result.runDirRelative) {
    console.error(`runDirRelative: ${result.runDirRelative}`);
  }
  if (result.errors) {
    console.error(JSON.stringify(result.errors, null, 2));
  }
  process.exitCode = result.exitCode;
}

if (import.meta.url === pathToFileURL(process.argv[1]).href) {
  main().catch((error) => {
    console.error(error instanceof Error ? error.message : String(error));
    process.exitCode = 1;
  });
}

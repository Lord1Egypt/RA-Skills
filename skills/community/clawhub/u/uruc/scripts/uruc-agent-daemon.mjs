#!/usr/bin/env node

import { AgentDaemon } from './lib/daemon-runtime.mjs';
import { ensureNodeVersion } from './lib/common.mjs';

ensureNodeVersion(22);

const daemon = new AgentDaemon();
let shuttingDown = false;

async function shutdown(reason, exitCode = 0) {
  if (shuttingDown) return;
  shuttingDown = true;
  try {
    console.error(`[uruc-agent] shutting down (${reason})`);
    await daemon.stop();
  } finally {
    process.exit(exitCode);
  }
}

process.on('SIGINT', () => {
  void shutdown('SIGINT');
});

process.on('SIGTERM', () => {
  void shutdown('SIGTERM');
});

process.on('uncaughtException', (error) => {
  console.error('[uruc-agent] uncaught exception');
  console.error(error);
  void shutdown('uncaughtException', 1);
});

process.on('unhandledRejection', (reason) => {
  console.error('[uruc-agent] unhandled rejection');
  console.error(reason);
  void shutdown('unhandledRejection', 1);
});

try {
  await daemon.start();
  console.error(`[uruc-agent] daemon ready (pid=${process.pid})`);
} catch (error) {
  console.error('[uruc-agent] failed to start daemon');
  console.error(error);
  process.exit(1);
}

#!/usr/bin/env node

/**
 * SPM v4 — CLI entry point.
 *
 * Uses Commander.js for argument parsing and command dispatch.
 *
 * Usage:
 *   spm init <project-name>   — Initialize project structure
 *   spm attest [ledger-path]  — Generate hash attestation
 *   spm verify [ledger-path]  — Verify WBS integrity
 *   spm quality-check [ledger-path] — Run quality gates
 *   spm status                — Show current SPM state
 *   spm doctor                — Health check
 *
 * @module cli
 */

import { Command } from 'commander';
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, resolve } from 'node:path';
import { initCommand } from './cli/init.js';
import { attestCommand } from './cli/attest.js';
import { verifyCommand } from './cli/verify.js';
import { qualityCommand } from './cli/quality.js';
import { statusCommand } from './cli/status.js';
import { doctorCommand } from './cli/doctor.js';

// ──────────────────────────────────────────────
// Resolve version from package.json
// ──────────────────────────────────────────────

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const pkg = JSON.parse(
  readFileSync(resolve(__dirname, '../package.json'), 'utf-8'),
);

// ──────────────────────────────────────────────
// Commander program
// ──────────────────────────────────────────────

const program = new Command();

program
  .name('spm')
  .version(pkg.version)
  .description(pkg.description);

program
  .command('init <name>')
  .description('Initialize project structure')
  .action(async (name) => {
    process.exitCode = await initCommand(name);
  });

program
  .command('attest [path]')
  .description('Generate hash attestation for the WBS ledger')
  .action(async (path) => {
    process.exitCode = await attestCommand(path);
  });

program
  .command('verify [path]')
  .description('Verify WBS ledger integrity')
  .action(async (path) => {
    process.exitCode = await verifyCommand(path);
  });

program
  .command('quality-check [path]')
  .description('Run quality gates on the WBS ledger')
  .action(async (path) => {
    process.exitCode = await qualityCommand(path);
  });

program
  .command('status')
  .description('Show current SPM project state')
  .action(async () => {
    process.exitCode = await statusCommand();
  });

program
  .command('doctor')
  .description('Comprehensive health check')
  .action(async () => {
    process.exitCode = await doctorCommand();
  });

// ──────────────────────────────────────────────
// Bootstrap
// ──────────────────────────────────────────────

program.parse(process.argv);
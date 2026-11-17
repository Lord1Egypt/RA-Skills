/**
 * SPM v4 — CLI handler for `spm status`.
 *
 * Shows the current SPM state: engine phase, WBS task summary,
 * recent events, and security gate status.
 *
 * @module cli/status
 */

import { existsSync, readFileSync, readdirSync } from 'node:fs';
import { resolve as resolvePath } from 'node:path';
import { requireConfig, loadConfig } from '../config/loader.js';
import { WBS } from '../wbs/index.js';
import { loadAttestation } from '../wbs/attest.js';
import { EventStore } from '../event-store/index.js';

// ──────────────────────────────────────────────
// Handler
// ──────────────────────────────────────────────

/**
 * Run `spm status`.
 *
 * Prints a summary of the SPM project state to stdout.
 *
 * @returns {Promise<number>} Exit code
 */
export async function statusCommand() {
  const root = process.cwd();

  console.log(`\n  📊  SPM Status — ${root}\n`);

  // ── Config ────────────────────────────────
  const configResult = loadConfig();
  console.log(`  📋  Config`);
  if (configResult.valid) {
    const src = configResult.source === 'defaults' ? '(defaults)' : configResult.source;
    console.log(`       Source: ${src}`);
    console.log(`       WBS ledger: ${configResult.config.wbs?.ledger_path || 'N/A'}`);
  } else {
    console.log(`       ⚠  Config validation errors:`);
    for (const err of configResult.errors) {
      console.log(`         - ${err}`);
    }
  }
  console.log('');

  // ── WBS Ledger ────────────────────────────
  /** @type {string} */
  const ledgerPath = (() => {
    if (configResult.valid && configResult.config.wbs?.ledger_path) {
      return resolvePath(root, configResult.config.wbs.ledger_path);
    }
    return resolvePath(root, 'docs/spm/ledger.md');
  })();

  console.log(`  📋  WBS Ledger`);
  if (existsSync(ledgerPath)) {
    try {
      const wbs = new WBS();
      wbs.load(ledgerPath);
      const tasks = wbs.getAllTasks();

      console.log(`       Path: ${ledgerPath}`);
      console.log(`       Tasks: ${tasks.length}`);

      // Count by status
      const counts = { todo: 0, doing: 0, done: 0, blocked: 0, skipped: 0 };
      for (const t of tasks) {
        if (counts[t.status] !== undefined) counts[t.status]++;
      }
      console.log(
        `       Status: 📝 ${counts.todo} todo  |  🔄 ${counts.doing} doing  |  ✅ ${counts.done} done  |  🚫 ${counts.blocked} blocked  |  ⏭ ${counts.skipped} skipped`,
      );

      // Attestation check
      const attestPath = resolvePath(
        root,
        configResult.valid ? configResult.config.wbs?.hash_separate_path || '.spm/wbs-attestation' : '.spm/wbs-attestation',
      );
      const attestRecord = loadAttestation(attestPath);
      if (attestRecord) {
        console.log(`       Last attested: ${attestRecord.timestamp}`);
      } else {
        console.log(`       No attestation record found`);
      }
    } catch (err) {
      console.log(`       ⚠  Error reading WBS: ${err.message}`);
    }
  } else {
    console.log(`       Ledger not found at "${ledgerPath}"`);
    console.log(`       Run \`spm init <project-name>\` to create one.`);
  }
  console.log('');

  // ── Event Store ───────────────────────────
  const eventDir = resolvePath(root, 'event-store-data');
  console.log(`  📋  Event Store`);

  if (existsSync(eventDir) && existsSync(resolvePath(eventDir, 'audit-events.jsonl'))) {
    try {
      const store = new EventStore(eventDir);

      for (const domain of store.domainNames()) {
        const cfg = store.getByDomain(domain);

        // Get recent count of events
        const recent = store.query(domain, { recent: 5 });
        const fileSize = existsSync(cfg.file_path)
          ? readFileSync(cfg.file_path, 'utf-8').split('\n').filter(Boolean).length
          : 0;

        console.log(`       ${domain}: ${fileSize} events`);
        if (recent.length > 0) {
          console.log(`         Last: ${recent[recent.length - 1].type} @ ${new Date(recent[recent.length - 1].timestamp).toLocaleString()}`);
        }
      }
    } catch (err) {
      console.log(`       ⚠  ${err.message}`);
    }
  } else {
    console.log(`       No event store data found at "${eventDir}"`);
  }
  console.log('');

  // ── Directory health ───────────────────────
  console.log(`  📋  Project Health`);

  /** @type {Array<{ path: string, label: string }>} */
  const checks = [
    { path: resolvePath(root, 'docs/spm'), label: 'docs/spm/' },
    { path: resolvePath(root, '.spm'), label: '.spm/' },
    { path: resolvePath(root, 'event-store-data'), label: 'event-store-data/' },
    { path: resolvePath(root, 'package.json'), label: 'package.json' },
  ];

  for (const check of checks) {
    const exists = existsSync(check.path);
    console.log(`       ${exists ? '✓' : '·'}  ${check.label}`);
  }
  console.log('');

  return 0;
}
/**
 * SPM v4 — CLI handler for `spm quality-check [ledger-path]`.
 *
 * Runs quality gates against the WBS ledger:
 * - All done tasks have evidence
 * - No blocked tasks without reason
 * - All tasks have a valid status
 * - Dependencies are satisfied
 *
 * @module cli/quality
 */

import { readFileSync, existsSync } from 'node:fs';
import { resolve as resolvePath } from 'node:path';
import { requireConfig } from '../config/loader.js';
import { WBS, WBSError } from '../wbs/index.js';
import { EventStore } from '../event-store/index.js';
import { MerkleTree } from '../wbs/merkle.js';

// ──────────────────────────────────────────────
// Quality gates
// ──────────────────────────────────────────────

/**
 * @typedef {Object} QualityGateResult
 * @property {string} gate — Gate name
 * @property {'pass'|'fail'|'warn'} status — Result status
 * @property {string} message — Human-readable message
 */

/**
 * Check that all completed tasks have evidence.
 *
 * @param {object[]} tasks
 * @returns {QualityGateResult}
 */
function gateDoneHasEvidence(tasks) {
  const missing = tasks.filter(
    (t) => t.status === 'done' && !t.evidence?.trim(),
  );

  if (missing.length === 0) {
    return {
      gate: 'done-evidence',
      status: 'pass',
      message: 'All completed tasks have evidence',
    };
  }

  return {
    gate: 'done-evidence',
    status: 'fail',
    message: `${missing.length} completed task(s) missing evidence: ${missing.map((t) => t.id).join(', ')}`,
  };
}

/**
 * Check that all blocked tasks have a context brief.
 *
 * @param {object[]} tasks
 * @returns {QualityGateResult}
 */
function gateBlockedHasContext(tasks) {
  const missing = tasks.filter(
    (t) => t.status === 'blocked' && !t.contextBrief?.trim(),
  );

  if (missing.length === 0) {
    return {
      gate: 'blocked-context',
      status: 'pass',
      message: 'All blocked tasks have context',
    };
  }

  return {
    gate: 'blocked-context',
    status: 'warn',
    message: `${missing.length} blocked task(s) lacking context: ${missing.map((t) => t.id).join(', ')}`,
  };
}

/**
 * Check that all tasks have a valid status.
 *
 * @param {object[]} tasks
 * @returns {QualityGateResult}
 */
function gateValidStatuses(tasks) {
  const validStatuses = ['todo', 'doing', 'done', 'blocked', 'skipped'];
  const invalid = tasks.filter((t) => !validStatuses.includes(t.status));

  if (invalid.length === 0) {
    return {
      gate: 'valid-status',
      status: 'pass',
      message: 'All tasks have valid status values',
    };
  }

  return {
    gate: 'valid-status',
    status: 'fail',
    message: `${invalid.length} task(s) with invalid status: ${invalid.map((t) => `${t.id}:"${t.status}"`).join(', ')}`,
  };
}

/**
 * Check that all dependencies reference existing tasks.
 *
 * @param {object[]} tasks
 * @returns {QualityGateResult}
 */
function gateValidDependencies(tasks) {
  const taskIds = new Set(tasks.map((t) => t.id));
  const broken = tasks.filter((t) =>
    t.dependencies?.some((depId) => !taskIds.has(depId)),
  );

  if (broken.length === 0) {
    return {
      gate: 'valid-dependencies',
      status: 'pass',
      message: 'All dependency references are valid',
    };
  }

  return {
    gate: 'valid-dependencies',
    status: 'fail',
    message: `${broken.length} task(s) with broken dependencies: ${broken.map((t) => `${t.id} -> ${t.dependencies.filter((d) => !taskIds.has(d)).join(',')}`).join('; ')}`,
  };
}

/**
 * Check for empty mandatory fields (workPackage, exitCriteria).
 *
 * @param {object[]} tasks
 * @returns {QualityGateResult}
 */
function gateMandatoryFields(tasks) {
  const missing = tasks.filter(
    (t) =>
      !t.workPackage?.trim() || !t.exitCriteria?.trim(),
  );

  if (missing.length === 0) {
    return {
      gate: 'mandatory-fields',
      status: 'pass',
      message: 'All tasks have required fields (workPackage, exitCriteria)',
    };
  }

  return {
    gate: 'mandatory-fields',
    status: 'warn',
    message: `${missing.length} task(s) missing required fields: ${missing.map((t) => t.id).join(', ')}`,
  };
}

// ──────────────────────────────────────────────
// All gates
// ──────────────────────────────────────────────

/** @type {Array<{ name: string, check: (tasks: object[]) => QualityGateResult }>} */
const QUALITY_GATES = [
  { name: 'Done tasks have evidence', check: gateDoneHasEvidence },
  { name: 'Blocked tasks have context', check: gateBlockedHasContext },
  { name: 'Valid status values', check: gateValidStatuses },
  { name: 'Valid dependency references', check: gateValidDependencies },
  { name: 'Mandatory fields present', check: gateMandatoryFields },
];

// ──────────────────────────────────────────────
// Handler
// ──────────────────────────────────────────────

/**
 * Run `spm quality-check`.
 *
 * Loads the WBS ledger and runs all quality gates, reporting
 * results to stdout and logging events to the event store.
 *
 * @param {string} [ledgerPath] — Optional path to the WBS ledger file
 * @returns {Promise<number>} Exit code (0 = all passed, 1 = any failed)
 */
export async function qualityCommand(ledgerPath) {
  const config = requireConfig();
  const resolvedPath = resolvePath(
    ledgerPath || config.wbs?.ledger_path || 'docs/spm/ledger.md',
  );

  if (!existsSync(resolvedPath)) {
    console.error(`Error: ledger file not found at "${resolvedPath}"`);
    return 1;
  }

  console.log(`\n  🧪  Quality check: ${resolvedPath}\n`);

  try {
    const content = readFileSync(resolvedPath, 'utf-8');
    const wbs = new WBS(config.wbs);
    wbs.load(resolvedPath);
    const tasks = wbs.getAllTasks();

    console.log(`  Ledger contains ${tasks.length} task(s)\n`);

    /** @type {QualityGateResult[]} */
    const results = [];
    let passed = 0;
    let warned = 0;
    let failed = 0;

    for (const gate of QUALITY_GATES) {
      const result = gate.check(tasks);
      results.push(result);

      const icon = result.status === 'pass' ? '✓' : result.status === 'warn' ? '⚠' : '✗';
      const colorFn =
        result.status === 'pass'
          ? (s) => s
          : result.status === 'warn'
            ? (s) => s
            : (s) => s;

      console.log(`  ${icon}  ${result.gate}`);
      console.log(`     ${result.message}`);

      if (result.status === 'pass') passed++;
      else if (result.status === 'warn') warned++;
      else failed++;
    }

    // Summary
    console.log('');
    console.log(`  ──────────────────────────────`);
    console.log(`  Passed: ${passed}  |  Warnings: ${warned}  |  Failed: ${failed}`);

    const overall = failed === 0 ? 'passed' : 'failed';
    console.log(`  Overall: ${overall === 'passed' ? '✅ PASSED' : '❌ FAILED'}`);

    // Log quality check event
    try {
      const eventDir = resolvePath(process.cwd(), 'event-store-data');
      if (existsSync(eventDir)) {
        const store = new EventStore(eventDir);
        store.push('quality', {
          type: 'quality.check',
          payload: {
            ledgerPath: resolvedPath,
            taskCount: tasks.length,
            passed,
            warned,
            failed,
            gates: results.map((r) => ({
              gate: r.gate,
              status: r.status,
              message: r.message,
            })),
          },
        });
      }
    } catch {
      // Event store is optional
    }

    console.log('');
    return failed > 0 ? 1 : 0;
  } catch (err) {
    console.error(`  ✗  Quality check failed: ${err.message}`);
    return 1;
  }
}
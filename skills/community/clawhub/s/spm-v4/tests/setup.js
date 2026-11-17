/**
 * Jest setup for SPM v4 unit tests.
 *
 * Provides shared test utilities: temp directory helpers, seed data
 * factories, and global mocks.
 *
 * @module tests/setup
 */

import { mkdtempSync, existsSync, rmSync, mkdirSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { dirname } from 'node:path';

// ──────────────────────────────────────────────
// Globals
// ──────────────────────────────────────────────

const __dirname = dirname(fileURLToPath(import.meta.url));

const PROJECT_ROOT = resolve(__dirname, '..');

/**
 * Create a temporary directory for test artifacts.
 *
 * The directory is auto-cleaned when `cleanup()` is called.
 *
 * @returns {{ path: string, cleanup: () => void }}
 */
export function createTempDir() {
  const base = join(tmpdir(), 'spm-test-');
  const path = mkdtempSync(base);
  return {
    path,
    cleanup: () => {
      if (existsSync(path)) {
        rmSync(path, { recursive: true, force: true });
      }
    },
  };
}

/**
 * Return the project root directory.
 *
 * @returns {string}
 */
export function getProjectRoot() {
  return PROJECT_ROOT;
}

/**
 * Resolve a path relative to the project root.
 *
 * @param {...string} segments
 * @returns {string}
 */
export function projectPath(...segments) {
  return resolve(PROJECT_ROOT, ...segments);
}

// ──────────────────────────────────────────────
// Seed Data: Sample WBS Ledger Markdown
// ──────────────────────────────────────────────

/**
 * A minimal valid WBS ledger for testing.
 *
 * @type {string}
 */
export const SAMPLE_LEDGER = `# SPM WBS Ledger

## WB-001: Initialize project
- **Status**: done
- **Dependencies**: none
- **Context**: Set up the project skeleton
- **Exit Criteria**: Repository created with package.json
- **Evidence**: GitHub repo initialized

## WB-002: Implement authentication
- **Status**: doing
- **Dependencies**: WB-001
- **Context**: Add JWT-based auth
- **Exit Criteria**: All auth endpoints working
- **Evidence**: 

## WB-003: Write unit tests
- **Status**: todo
- **Dependencies**: WB-001
- **Context**: Cover core modules
- **Exit Criteria**: 80% coverage
- **Evidence**: 
`;

/**
 * A ledger with a circular dependency for testing cycle detection.
 *
 * @type {string}
 */
export const CIRCULAR_LEDGER = `# SPM WBS Ledger

## WB-001: Task A
- **Status**: todo
- **Dependencies**: WB-002

## WB-002: Task B
- **Status**: todo
- **Dependencies**: WB-003

## WB-003: Task C
- **Status**: todo
- **Dependencies**: WB-001
`;

/**
 * A ledger with a missing dependency reference.
 *
 * @type {string}
 */
export const MISSING_DEP_LEDGER = `# SPM WBS Ledger

## WB-001: Task A
- **Status**: todo
- **Dependencies**: WB-999
`;

/**
 * Minimal context for the engine's "requirement" phase precondition.
 *
 * @type {object}
 */
export const ENGINE_CONTEXT_REQUIREMENT = {
  projectName: 'test-project',
  goal: 'Test the engine',
};

/**
 * Full context that satisfies all phase preconditions.
 *
 * @type {object}
 */
export const ENGINE_FULL_CONTEXT = {
  projectName: 'test-project',
  goal: 'Test all phases',
  requirements: [{ id: 'R1', title: 'Core functionality' }],
  plan: { steps: ['Step 1', 'Step 2'] },
  execution: { output: 'build output' },
  quality: { passed: true },
};

// ──────────────────────────────────────────────
// Cleanup
// ──────────────────────────────────────────────

/**
 * Clean up all temp directories tracked by createTempDir.
 *
 * Call in afterEach or afterAll.
 *
 * @param {Array<{ cleanup: () => void }>} tempDirs
 */
export function cleanupTempDirs(tempDirs) {
  for (const t of tempDirs) {
    try { t.cleanup(); } catch { /* ignore */ }
  }
}
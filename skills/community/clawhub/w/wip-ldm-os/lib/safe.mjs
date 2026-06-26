/**
 * lib/safe.mjs
 * Safe file operations. Never delete. Always trash. Always write revert plans.
 * Follows the _trash/ pattern from the DevOps Toolkit.
 * Zero dependencies.
 */

import { existsSync, mkdirSync, renameSync, writeFileSync, readFileSync, cpSync } from 'node:fs';
import { join, basename, dirname } from 'node:path';

const HOME = process.env.HOME || '';
const LDM_ROOT = join(HOME, '.ldm');
const TRASH_ROOT = join(LDM_ROOT, '_trash');

function readJSON(path) {
  try {
    return JSON.parse(readFileSync(path, 'utf8'));
  } catch {
    return null;
  }
}

// ── Trash ──

/**
 * Move a file or directory to ~/.ldm/_trash/YYYY-MM-DD/ instead of deleting.
 * Returns the trash destination path, or null if source didn't exist.
 */
export function moveToTrash(sourcePath) {
  if (!existsSync(sourcePath)) return null;

  const date = new Date().toISOString().split('T')[0];
  const trashDir = join(TRASH_ROOT, date);
  const name = basename(sourcePath);

  mkdirSync(trashDir, { recursive: true });

  let dest = join(trashDir, name);
  if (existsSync(dest)) {
    dest = join(trashDir, `${name}-${Date.now()}`);
  }

  renameSync(sourcePath, dest);
  return dest;
}

// ── Revert Manifests ──

/**
 * Create a revert manifest before a batch of operations.
 * Each operation: { action, name, description, originalPath, trashPath }
 * Returns the manifest file path.
 */
export function createRevertManifest(description, operations = []) {
  const date = new Date().toISOString().split('T')[0];
  const time = new Date().toISOString().replace(/[:.]/g, '-');
  const manifestDir = join(TRASH_ROOT, date);
  const manifestPath = join(manifestDir, `revert-${time}.json`);

  mkdirSync(manifestDir, { recursive: true });

  const manifest = {
    timestamp: new Date().toISOString(),
    description,
    operations,
    howToRevert: 'For each operation with a trashPath, move it back to originalPath.',
  };

  writeFileSync(manifestPath, JSON.stringify(manifest, null, 2) + '\n');
  return manifestPath;
}

/**
 * Append a completed operation to an existing revert manifest.
 */
export function appendToManifest(manifestPath, operation) {
  if (!existsSync(manifestPath)) return;

  try {
    const manifest = JSON.parse(readFileSync(manifestPath, 'utf8'));
    manifest.operations.push(operation);
    writeFileSync(manifestPath, JSON.stringify(manifest, null, 2) + '\n');
  } catch {}
}

// ── Safe copy (backup before overwrite) ──

/**
 * Copy a directory, but if the destination already exists, trash it first.
 * Returns { trashPath, destPath } or null on failure.
 */
export function safeCopy(srcPath, destPath) {
  let trashPath = null;

  if (existsSync(destPath)) {
    trashPath = moveToTrash(destPath);
  }

  try {
    mkdirSync(dirname(destPath), { recursive: true });
    cpSync(srcPath, destPath, {
      recursive: true,
      filter: (s) => !s.includes('.git') && !s.includes('node_modules') && !s.includes('/ai/'),
    });
    return { trashPath, destPath };
  } catch (e) {
    // Rollback: restore from trash if copy failed
    if (trashPath && existsSync(trashPath) && !existsSync(destPath)) {
      try { renameSync(trashPath, destPath); } catch {}
    }
    throw e;
  }
}

/**
 * SPM v4 — SHA-256 hash attestation for WBS ledger integrity.
 *
 * Provides functions to compute, store, and verify SHA-256 hashes
 * of the WBS ledger content. The attestation record includes the
 * hash and a timestamp, persisted to `.spm/wbs-attestation`.
 *
 * @module wbs/attest
 */

import { createHash, timingSafeEqual as tsEqual } from 'node:crypto';
import { writeFileSync, readFileSync, existsSync, mkdirSync } from 'node:fs';
import { resolve as resolvePath, dirname } from 'node:path';

// ──────────────────────────────────────────────
// Constants
// ──────────────────────────────────────────────

/** Default attestation file path relative to project root. */
export const DEFAULT_ATTEST_PATH = '.spm/wbs-attestation';

// ──────────────────────────────────────────────
// Hashing
// ──────────────────────────────────────────────

/**
 * Compute the SHA-256 hex digest of the given ledger content.
 *
 * The content is hashed as a UTF-8 string. For consistency, the
 * caller should `normalizeLineEndings(content)` beforehand if
 * cross-platform reproducibility is needed.
 *
 * @param {string} ledgerContent — The entire WBS ledger as a string
 * @returns {string} Hex-encoded SHA-256 digest (64 characters)
 *
 * @example
 * import { attest } from './attest.js';
 * const hash = attest(fs.readFileSync('ledger.md', 'utf-8'));
 * console.log(hash); // "a1b2c3d4..."
 */
export function hashContent(ledgerContent) {
  return createHash('sha-256')
    .update(normalizeLineEndings(ledgerContent), 'utf-8')
    .digest('hex');
}

// ──────────────────────────────────────────────
// Attest
// ──────────────────────────────────────────────

/**
 * Compute and persist the SHA-256 attestation of the ledger content.
 *
 * Writes a JSON record containing the hash, timestamp, and algorithm
 * to the `.spm/wbs-attestation` file. The directory `.spm/` is
 * created automatically if it does not exist.
 *
 * @param {string} ledgerContent — The entire WBS ledger as a string
 * @param {string} [attestPath='.spm/wbs-attestation'] — Custom output path
 * @returns {{ hash: string, timestamp: string, algorithm: string }} The attestation record
 *
 * @example
 * import { attest } from './attest.js';
 * const record = attest(ledgerContent);
 * // record.hash === 'sha256 hex'
 */
export function attest(ledgerContent, attestPath = DEFAULT_ATTEST_PATH) {
  const hash = hashContent(ledgerContent);
  const timestamp = new Date().toISOString();

  const record = {
    hash,
    timestamp,
    algorithm: 'sha-256',
  };

  const resolvedPath = resolvePath(attestPath);
  const dir = dirname(resolvedPath);

  if (!existsSync(dir)) {
    mkdirSync(dir, { recursive: true });
  }

  writeFileSync(resolvedPath, JSON.stringify(record, null, 2) + '\n', 'utf-8');

  return record;
}

// ──────────────────────────────────────────────
// Verify
// ──────────────────────────────────────────────

/**
 * Verify that the ledger content matches the expected SHA-256 hash.
 *
 * Compares the computed hash of the content against `expectedHash`.
 * Returns `true` if they match, `false` otherwise.
 *
 * @param {string} ledgerContent — The entire WBS ledger as a string
 * @param {string} expectedHash  — Hex-encoded SHA-256 digest to compare against
 * @returns {boolean} `true` if content is authentic, `false` if tampered
 *
 * @example
 * import { verify } from './attest.js';
 * const ok = verify(ledgerContent, storedHash);
 * if (!ok) console.error('⚠️  WBS ledger has been tampered with!');
 */
export function verify(ledgerContent, expectedHash) {
  const computed = hashContent(ledgerContent);
  return timingSafeEqual(computed, expectedHash);
}

// ──────────────────────────────────────────────
// Load / Check
// ──────────────────────────────────────────────

/**
 * Load a previously persisted attestation record from disk.
 *
 * @param {string} [attestPath='.spm/wbs-attestation'] — Path to the attestation file
 * @returns {{ hash: string, timestamp: string, algorithm: string } | null}
 *          The parsed record, or `null` if the file does not exist or is malformed
 *
 * @example
 * import { loadAttestation } from './attest.js';
 * const record = loadAttestation();
 * if (record) console.log(`Last attested: ${record.timestamp}`);
 */
export function loadAttestation(attestPath = DEFAULT_ATTEST_PATH) {
  const resolvedPath = resolvePath(attestPath);

  if (!existsSync(resolvedPath)) return null;

  try {
    const raw = readFileSync(resolvedPath, 'utf-8').trim();
    const parsed = JSON.parse(raw);

    if (
      typeof parsed.hash === 'string' &&
      typeof parsed.timestamp === 'string' &&
      typeof parsed.algorithm === 'string'
    ) {
      return {
        hash: parsed.hash,
        timestamp: parsed.timestamp,
        algorithm: parsed.algorithm,
      };
    }

    return null;
  } catch {
    return null;
  }
}

/**
 * Convenience function: verify the on-disk ledger against its stored
 * attestation record.
 *
 * @param {string} ledgerContent — The ledger content string
 * @param {string} [attestPath='.spm/wbs-attestation'] — Path to the attestation file
 * @returns {{ valid: boolean, record: object | null }}
 *          `valid` is true iff the content hash matches the stored attestation.
 *          `record` is the parsed attestation record (or null if not found).
 */
export function checkAttestation(ledgerContent, attestPath = DEFAULT_ATTEST_PATH) {
  const record = loadAttestation(attestPath);
  if (!record) {
    return { valid: false, record: null };
  }

  const valid = verify(ledgerContent, record.hash);
  return { valid, record };
}

// ──────────────────────────────────────────────
// Internal Helpers
// ──────────────────────────────────────────────

/**
 * Normalize line endings to LF for reproducible hashing across platforms.
 *
 * @param {string} str — Input string (possibly with CRLF endings)
 * @returns {string} Normalized string (LF only)
 */
function normalizeLineEndings(str) {
  return str.replace(/\r\n/g, '\n').replace(/\r/g, '\n');
}

/**
 * Constant-time string comparison for hash verification.
 *
 * Uses Node.js `crypto.timingSafeEqual` on Buffer representations
 * to prevent timing attacks.
 *
 * @param {string} a — First hex string (64 chars)
 * @param {string} b — Second hex string (64 chars)
 * @returns {boolean} `true` if equal
 */
function timingSafeEqual(a, b) {
  const bufA = Buffer.from(a, 'utf-8');
  const bufB = Buffer.from(b, 'utf-8');

  if (bufA.length !== bufB.length) {
    return false;
  }

  try {
    return tsEqual(bufA, bufB);
  } catch {
    // Fallback if timingSafeEqual is unavailable
    return bufA.equals(bufB);
  }
}
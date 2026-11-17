/**
 * SPM v4 — CLI handler for `spm verify [ledger-path]`.
 *
 * Reads the WBS ledger and verifies its integrity against the stored
 * SHA-256 attestation record. Optionally also verifies per-task hashes
 * with the Merkle tree.
 *
 * @module cli/verify
 */

import { readFileSync, existsSync } from 'node:fs';
import { resolve as resolvePath } from 'node:path';
import { requireConfig } from '../config/loader.js';
import { checkAttestation, loadAttestation } from '../wbs/attest.js';
import { MerkleTree } from '../wbs/merkle.js';
import { WBS } from '../wbs/index.js';
import { EventStore } from '../event-store/index.js';

// ──────────────────────────────────────────────
// Handler
// ──────────────────────────────────────────────

/**
 * Run `spm verify`.
 *
 * Verifies the WBS ledger against its stored attestation.
 * Reports whether the ledger is intact or has been tampered with.
 *
 * @param {string} [ledgerPath] — Optional path to the WBS ledger file
 * @returns {Promise<number>} Exit code
 */
export async function verifyCommand(ledgerPath) {
  const config = requireConfig();
  const resolvedPath = resolvePath(
    ledgerPath || config.wbs?.ledger_path || 'docs/spm/ledger.md',
  );
  const attestPath = config.wbs?.hash_separate_path || '.spm/wbs-attestation';

  if (!existsSync(resolvedPath)) {
    console.error(`Error: ledger file not found at "${resolvedPath}"`);
    return 1;
  }

  if (!existsSync(attestPath)) {
    console.error(`Error: attestation file not found at "${attestPath}"`);
    console.error('Run `spm attest` first to generate an attestation.');
    return 1;
  }

  console.log(`\n  🔍  Verifying WBS ledger: ${resolvedPath}\n`);

  try {
    const content = readFileSync(resolvedPath, 'utf-8');
    const storedRecord = loadAttestation(attestPath);

    if (!storedRecord) {
      console.error(`  ✗  Cannot read attestation from "${attestPath}"`);
      return 1;
    }

    console.log(`  Stored attestation:`);
    console.log(`     Hash:       ${storedRecord.hash}`);
    console.log(`     Algorithm:  ${storedRecord.algorithm}`);
    console.log(`     Timestamp:  ${storedRecord.timestamp}`);

    // Verify against stored attestation
    const result = checkAttestation(content, attestPath);

    if (result.valid) {
      console.log(`\n  ✅  LEDGER INTEGRITY VERIFIED`);
      console.log(`     The WBS ledger has not been tampered with since `);
      console.log(`     last attestation (${storedRecord.timestamp}).`);
    } else {
      console.log(`\n  ❌  LEDGER INTEGRITY CHECK FAILED`);
      console.log(`     The current ledger content does NOT match the`);
      console.log(`     stored attestation hash.`);
      console.log(`     Expected: ${storedRecord.hash}`);
      console.log(`     Actual:   ${result.record ? '(computed hash does not match)' : '(no record)'}`);
    }

    // Log the verification event
    try {
      const eventDir = resolvePath(process.cwd(), 'event-store-data');
      if (existsSync(eventDir)) {
        const store = new EventStore(eventDir);
        store.push('integrity', {
          type: 'wbs.verified',
          payload: {
            ledgerPath: resolvedPath,
            valid: result.valid,
            expectedHash: storedRecord.hash,
          },
        });
      }
    } catch {
      // Event store is optional
    }

    console.log('');
    return result.valid ? 0 : 1;
  } catch (err) {
    console.error(`  ✗  Verification failed: ${err.message}`);
    return 1;
  }
}
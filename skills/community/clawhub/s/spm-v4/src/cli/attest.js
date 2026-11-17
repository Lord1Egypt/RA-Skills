/**
 * SPM v4 — CLI handler for `spm attest [ledger-path]`.
 *
 * Reads the WBS ledger, computes SHA-256 hash, persists the attestation
 * record, and prints the result to stdout.
 *
 * @module cli/attest
 */

import { readFileSync, existsSync } from 'node:fs';
import { resolve as resolvePath } from 'node:path';
import { requireConfig } from '../config/loader.js';
import { attest, hashContent, loadAttestation } from '../wbs/attest.js';
import { MerkleTree } from '../wbs/merkle.js';
import { WBS } from '../wbs/index.js';
import { EventStore } from '../event-store/index.js';

// ──────────────────────────────────────────────
// Handler
// ──────────────────────────────────────────────

/**
 * Run `spm attest`.
 *
 * Loads the WBS ledger, generates SHA-256 attestation, and optionally
 * builds a Merkle tree for per-task integrity verification.
 *
 * @param {string} [ledgerPath] — Optional path to the WBS ledger file
 * @returns {Promise<number>} Exit code
 */
export async function attestCommand(ledgerPath) {
  const config = requireConfig();
  const resolvedPath = resolvePath(
    ledgerPath || config.wbs?.ledger_path || 'docs/spm/ledger.md',
  );

  // Check the file exists
  if (!existsSync(resolvedPath)) {
    console.error(`Error: ledger file not found at "${resolvedPath}"`);
    console.error('Run `spm init <project-name>` first, or provide a valid path.');
    return 1;
  }

  console.log(`\n  📋  Attesting WBS ledger: ${resolvedPath}\n`);

  try {
    const content = readFileSync(resolvedPath, 'utf-8');
    const attestPath = config.wbs?.hash_separate_path || '.spm/wbs-attestation';

    // Generate and persist attestation
    const record = attest(content, attestPath);
    console.log(`  ✓  Attestation saved to: ${attestPath}`);
    console.log(`     Hash:       ${record.hash}`);
    console.log(`     Algorithm:  ${record.algorithm}`);
    console.log(`     Timestamp:  ${record.timestamp}`);

    // Optionally build Merkle tree if enabled in config
    if (config.wbs?.merkle_enabled !== false) {
      try {
        const wbs = new WBS(config.wbs);
        wbs.load(resolvedPath);
        const tasks = wbs.getAllTasks();

        const tree = new MerkleTree();
        const snapshot = tree.buildTree(tasks);

        console.log(`\n  🌳  Merkle Tree:`);
        console.log(`     Root Hash:  ${snapshot.rootHash}`);
        console.log(`     Task Count: ${snapshot.nodeCount}`);

        // Log the attestation event
        try {
          const eventDir = resolvePath(process.cwd(), 'event-store-data');
          const store = new EventStore(eventDir);
          store.push('integrity', {
            type: 'wbs.attested',
            payload: {
              ledgerPath: resolvedPath,
              hash: record.hash,
              merkleRoot: snapshot.rootHash,
              merkleCount: snapshot.nodeCount,
              timestamp: record.timestamp,
            },
          });
        } catch {
          // Event store is optional for attestation
        }
      } catch (err) {
        // Merkle tree is supplementary — don't fail the whole command
        console.log(`\n  ⚠  Merkle tree unavailable: ${err.message}`);
      }
    }

    console.log(`\n  ✅  Attestation complete.\n`);
    return 0;
  } catch (err) {
    console.error(`  ✗  Attestation failed: ${err.message}`);
    return 1;
  }
}
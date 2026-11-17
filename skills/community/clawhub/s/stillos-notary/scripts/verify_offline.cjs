#!/usr/bin/env node
'use strict';
/**
 * verify_offline.cjs — verify a SINGLE StillOS Notary receipt you already have,
 * with ZERO network calls. No dependency on nolawealthfinancial.com being up.
 *
 * This only proves the receipt is an unforged, unmodified Ed25519-signed
 * artifact from the StillOS Notary signing key. It does NOT re-check the
 * underlying claim against GitHub/Kalshi/on-chain/etc — that requires calling
 * the live resolver. For full-ledger chain verification (all receipts, hash
 * chain continuity), see verify_ledger.cjs, which does need network access to
 * fetch the export.
 *
 * Usage:
 *   node verify_offline.cjs receipt.json
 *   cat receipt.json | node verify_offline.cjs
 */
const crypto = require('crypto');
const fs = require('fs');

// Published, standalone StillOS Notary signing key — pin this, do not fetch it
// live. If it ever needs to rotate, the notary will publish a new key here and
// at https://nolawealthfinancial.com/notary/export (network path, for comparison).
const NOTARY_PUBLIC_KEY_PEM = `-----BEGIN PUBLIC KEY-----
MCowBQYDK2VwAyEAsFIB67A7w7j7oLHjuJeErxMpq2VTZyUXD2785nbgqMM=
-----END PUBLIC KEY-----`;

function sha256(s) { return crypto.createHash('sha256').update(s).digest('hex'); }

function verify(receipt) {
  const errors = [];
  const { agent, claim_sha256, ts, prev_hash, notary_fp, resolver_hash, drand_round, drand_randomness, receipt_hash, signature } = receipt;

  if (!agent || !claim_sha256 || !ts || !prev_hash || !notary_fp || !receipt_hash || !signature) {
    errors.push('missing required field (agent, claim_sha256, ts, prev_hash, notary_fp, receipt_hash, signature)');
    return { valid: false, errors };
  }

  // Recompute receipt_hash from the exact key order the notary signs over.
  const core = { agent, claim_sha256, ts, prev_hash, notary_fp,
    ...(resolver_hash ? { resolver_hash } : {}),
    ...(drand_round ? { drand_round, drand_randomness } : {}) };
  const recomputed = sha256(JSON.stringify(core));

  if (recomputed !== receipt_hash) {
    errors.push(`hash mismatch: recomputed ${recomputed} != claimed ${receipt_hash} (receipt was altered after signing, or fields/order don't match what was actually signed)`);
  }

  let sigOk = false;
  try {
    sigOk = crypto.verify(null, Buffer.from(receipt_hash), NOTARY_PUBLIC_KEY_PEM, Buffer.from(signature, 'base64'));
  } catch (e) {
    errors.push(`signature check threw: ${e.message}`);
  }
  if (!sigOk) errors.push('Ed25519 signature does not verify against the published StillOS Notary key — not signed by us, or tampered');

  return { valid: errors.length === 0, receipt_hash, recomputed_hash: recomputed, errors };
}

function main() {
  const path = process.argv[2];
  const raw = path ? fs.readFileSync(path, 'utf8') : fs.readFileSync(0, 'utf8');
  const receipt = JSON.parse(raw);
  const result = verify(receipt);
  console.log(JSON.stringify(result, null, 2));
  process.exit(result.valid ? 0 : 1);
}

if (require.main === module) main();
module.exports = { verify, NOTARY_PUBLIC_KEY_PEM };

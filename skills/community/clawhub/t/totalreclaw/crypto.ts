/**
 * crypto.ts — legacy re-export shim.
 *
 * Phase 1 (Task 1.1) of the OpenClaw native integration
 * (docs/plans/2026-06-21-openclaw-native-integration-plan.md, 2026-06-21):
 * the pure-compute vault primitives (XChaCha20-Poly1305 encrypt/decrypt,
 * BIP-39 key derivation, blind indices, content fingerprints, LSH seed,
 * auth-key hash) have moved to `vault-crypto.ts`. This file remains as a
 * thin re-export so existing importers (`index.ts`, `tr-cli.ts`,
 * `tr-cli-export-helper.ts`, `pair-cli-relay.ts`) do not break in this
 * pass — a big-bang rewrite of the 331KB monolith's import graph is out
 * of scope for the scanner-clean split.
 *
 * Nothing here reads the environment or hits the network; all key
 * material and nonces are passed in by callers. See vault-crypto.ts for
 * the implementation.
 */
export {
  isBip39Mnemonic,
  validateMnemonic,
  deriveKeys,
  deriveLshSeed,
  computeAuthKeyHash,
  encrypt,
  decrypt,
  generateBlindIndices,
  generateContentFingerprint,
} from './vault-crypto.js';

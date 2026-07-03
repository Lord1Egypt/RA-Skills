/**
 * pair-crypto.ts — legacy re-export shim.
 *
 * Phase 1 (Task 1.1) of the OpenClaw native integration
 * (docs/plans/2026-06-21-openclaw-native-integration-plan.md, 2026-06-21):
 * the gateway-side pair primitives (x25519 ECDH, HKDF-SHA256, AES-256-GCM
 * AEAD, constant-time secondary-code comparison) have moved to
 * `vault-crypto.ts`. This file remains as a thin re-export so existing
 * importers (`pair-cli.ts`, `pair-remote-client.ts`, `pair-http.ts`) do
 * not break in this pass — a big-bang rewrite of the import graph is out
 * of scope for the scanner-clean split.
 *
 * Nothing here reads the environment or hits the network; all key
 * material and nonces are passed in by callers. See vault-crypto.ts for
 * the implementation.
 */
export {
  HKDF_INFO,
  AEAD_KEY_BYTES,
  AEAD_NONCE_BYTES,
  AEAD_TAG_BYTES,
  X25519_KEY_BYTES,
  type PublicKeyB64,
  type PrivateKeyB64,
  type NonceB64,
  type CiphertextB64,
  type GatewayKeypair,
  type SessionKeys,
  type DecryptInputs,
  type EncryptInputs,
  type EncryptOutput,
  generateGatewayKeypair,
  derivePublicFromPrivate,
  computeSharedSecret,
  deriveSessionKeys,
  deriveAeadKeyFromEcdh,
  aeadDecrypt,
  decryptPairingPayload,
  aeadEncryptWithSessionKey,
  encryptPairingPayload,
  compareSecondaryCodesCT,
} from './vault-crypto.js';

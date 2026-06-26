/**
 * Tests for pair-crypto (P3 of the v3.3.0 QR-pairing implementation).
 *
 * Test matrix:
 *   1. generateGatewayKeypair produces 32-byte base64url halves.
 *   2. derivePublicFromPrivate round-trips.
 *   3. ECDH symmetry: x25519(sk_A, pk_B) === x25519(sk_B, pk_A).
 *   4. RFC 7748 test vector 1 — x25519 interop check.
 *   5. HKDF is deterministic for same inputs; differs for different sid.
 *   6. deriveAeadKeyFromEcdh matches on both sides of the handshake.
 *   7. AEAD round-trip: encrypt then decrypt recovers plaintext.
 *   8. AEAD with AD (sid) binding: ct for sid=A fails to decrypt under sid=B.
 *   9. Tag-tamper detection: flipping a byte in the ciphertext fails decrypt.
 *   10. Nonce-tamper: changing the nonce fails decrypt.
 *   11. Wrong-peer-key rejection: decrypt with unrelated peer pubkey fails.
 *   12. Key byte-length validation rejects wrong-size inputs.
 *   13. decryptPairingPayload one-shot happy path recovers plaintext.
 *   14. encryptPairingPayload → decryptPairingPayload round-trip.
 *   15. compareSecondaryCodesCT: match, mismatch, length-mismatch.
 *   16. AEAD key length = 32 bytes; nonce length = 12 bytes; tag length = 16.
 *
 * Run with: npx tsx pair-crypto.test.ts
 */

import {
  generateGatewayKeypair,
  derivePublicFromPrivate,
  computeSharedSecret,
  deriveSessionKeys,
  deriveAeadKeyFromEcdh,
  aeadDecrypt,
  aeadEncryptWithSessionKey,
  decryptPairingPayload,
  encryptPairingPayload,
  compareSecondaryCodesCT,
  HKDF_INFO,
  AEAD_KEY_BYTES,
  AEAD_NONCE_BYTES,
  AEAD_TAG_BYTES,
  X25519_KEY_BYTES,
} from './pair-crypto.js';

let passed = 0;
let failed = 0;

function assert(condition: boolean, name: string): void {
  const n = passed + failed + 1;
  if (condition) {
    console.log(`ok ${n} - ${name}`);
    passed++;
  } else {
    console.log(`not ok ${n} - ${name}`);
    failed++;
  }
}

// ---------------------------------------------------------------------------
// 1. generateGatewayKeypair byte-length sanity
// ---------------------------------------------------------------------------
{
  const kp = generateGatewayKeypair();
  assert(
    Buffer.from(kp.pkB64, 'base64url').length === X25519_KEY_BYTES,
    `gen: pk is ${X25519_KEY_BYTES} bytes`,
  );
  assert(
    Buffer.from(kp.skB64, 'base64url').length === X25519_KEY_BYTES,
    `gen: sk is ${X25519_KEY_BYTES} bytes`,
  );
  assert(kp.pkB64 !== kp.skB64, 'gen: pk and sk are distinct');
}

// ---------------------------------------------------------------------------
// 2. derivePublicFromPrivate round-trips
// ---------------------------------------------------------------------------
{
  const kp = generateGatewayKeypair();
  const derived = derivePublicFromPrivate(kp.skB64);
  assert(derived === kp.pkB64, 'derive: pk from sk matches original');
}

// ---------------------------------------------------------------------------
// 3. ECDH symmetry
// ---------------------------------------------------------------------------
{
  const a = generateGatewayKeypair();
  const b = generateGatewayKeypair();
  const s1 = computeSharedSecret({ skLocalB64: a.skB64, pkRemoteB64: b.pkB64 });
  const s2 = computeSharedSecret({ skLocalB64: b.skB64, pkRemoteB64: a.pkB64 });
  assert(Buffer.compare(s1, s2) === 0, 'ecdh: sym: x25519(a,B) == x25519(b,A)');
  assert(s1.length === X25519_KEY_BYTES, 'ecdh: output length 32');
}

// ---------------------------------------------------------------------------
// 4. RFC 7748 x25519 test vector 1
// ---------------------------------------------------------------------------
// From RFC 7748 §6.1 (x25519 key-agreement test vector):
//   Alice's private:
//     77076d0a7318a57d3c16c17251b26645df4c2f87ebc0992ab177fba51db92c2a
//   Alice's public:
//     8520f0098930a754748b7ddcb43ef75a0dbf3a0d26381af4eba4a98eaa9b4e6a
//   Bob's private:
//     5dab087e624a8a4b79e17f8b83800ee66f3bb1292618b6fd1c2f8b27ff88e0eb
//   Bob's public:
//     de9edb7d7b7dc1b4d35b61c2ece435373f8343c85b78674dadfc7e146f882b4f
//   Expected shared secret:
//     4a5d9d5ba4ce2de1728e3bf480350f25e07e21c947d19e3376f09b3c1e161742
{
  const alicePrivHex = '77076d0a7318a57d3c16c17251b26645df4c2f87ebc0992ab177fba51db92c2a';
  const alicePubHex = '8520f0098930a754748b7ddcb43ef75a0dbf3a0d26381af4eba4a98eaa9b4e6a';
  const bobPrivHex = '5dab087e624a8a4b79e17f8b83800ee66f3bb1292618b6fd1c2f8b27ff88e0eb';
  const bobPubHex = 'de9edb7d7b7dc1b4d35b61c2ece435373f8343c85b78674dadfc7e146f882b4f';
  const expectedHex = '4a5d9d5ba4ce2de1728e3bf480350f25e07e21c947d19e3376f09b3c1e161742';

  const aliceSkB64 = Buffer.from(alicePrivHex, 'hex').toString('base64url');
  const bobPkB64 = Buffer.from(bobPubHex, 'hex').toString('base64url');
  const bobSkB64 = Buffer.from(bobPrivHex, 'hex').toString('base64url');
  const alicePkB64 = Buffer.from(alicePubHex, 'hex').toString('base64url');

  // Note: RFC 7748 test vectors use CLAMPED private keys. Node accepts
  // unclamped inputs and clamps internally, so the shared secret should
  // match the expected value.
  const s1 = computeSharedSecret({ skLocalB64: aliceSkB64, pkRemoteB64: bobPkB64 });
  const s2 = computeSharedSecret({ skLocalB64: bobSkB64, pkRemoteB64: alicePkB64 });
  assert(s1.toString('hex') === expectedHex, 'rfc7748: Alice * Bob_pub matches vector');
  assert(s2.toString('hex') === expectedHex, 'rfc7748: Bob * Alice_pub matches vector');

  // Also confirm derivePublicFromPrivate matches the vector's public keys.
  const aliceDerivedPk = derivePublicFromPrivate(aliceSkB64);
  assert(
    Buffer.from(aliceDerivedPk, 'base64url').toString('hex') === alicePubHex,
    'rfc7748: derive(alice_sk) matches alice_pub',
  );
  const bobDerivedPk = derivePublicFromPrivate(bobSkB64);
  assert(
    Buffer.from(bobDerivedPk, 'base64url').toString('hex') === bobPubHex,
    'rfc7748: derive(bob_sk) matches bob_pub',
  );
}

// ---------------------------------------------------------------------------
// 5. HKDF determinism + sid binding
// ---------------------------------------------------------------------------
{
  const shared = Buffer.alloc(32, 0x42);
  const k1 = deriveSessionKeys({ sharedSecret: shared, sid: 'abc' });
  const k2 = deriveSessionKeys({ sharedSecret: shared, sid: 'abc' });
  const k3 = deriveSessionKeys({ sharedSecret: shared, sid: 'xyz' });
  assert(Buffer.compare(k1.kEnc, k2.kEnc) === 0, 'hkdf: deterministic for same inputs');
  assert(Buffer.compare(k1.kEnc, k3.kEnc) !== 0, 'hkdf: different sid → different key');
  assert(k1.kEnc.length === AEAD_KEY_BYTES, `hkdf: output length ${AEAD_KEY_BYTES}`);

  // Empty sid rejected
  try {
    deriveSessionKeys({ sharedSecret: shared, sid: '' });
    assert(false, 'hkdf: empty sid rejected');
  } catch {
    assert(true, 'hkdf: empty sid rejected');
  }
}

// ---------------------------------------------------------------------------
// 6. deriveAeadKeyFromEcdh matches on both sides
// ---------------------------------------------------------------------------
{
  const a = generateGatewayKeypair();
  const b = generateGatewayKeypair();
  const sid = 'session-test-6';
  const ka = deriveAeadKeyFromEcdh({ skLocalB64: a.skB64, pkRemoteB64: b.pkB64, sid });
  const kb = deriveAeadKeyFromEcdh({ skLocalB64: b.skB64, pkRemoteB64: a.pkB64, sid });
  assert(Buffer.compare(ka.kEnc, kb.kEnc) === 0, 'handshake: A and B derive same kEnc');
}

// ---------------------------------------------------------------------------
// 7. AEAD round-trip
// ---------------------------------------------------------------------------
{
  const kEnc = Buffer.alloc(AEAD_KEY_BYTES, 0x7a);
  const sid = 'sid-test-7';
  const plaintext = Buffer.from('twelve words of recovery phrase go right here', 'utf-8');
  const { nonceB64, ciphertextB64 } = aeadEncryptWithSessionKey({ kEnc, sid, plaintext });
  assert(Buffer.from(nonceB64, 'base64url').length === AEAD_NONCE_BYTES, 'aead: nonce len 12');
  // ct + tag → ciphertext length >= plaintext.length + 16
  assert(
    Buffer.from(ciphertextB64, 'base64url').length === plaintext.length + AEAD_TAG_BYTES,
    `aead: ct+tag length = pt+${AEAD_TAG_BYTES}`,
  );
  const recovered = aeadDecrypt({ kEnc, nonceB64, sid, ciphertextB64 });
  assert(recovered.equals(plaintext), 'aead: round-trip recovers plaintext');
}

// ---------------------------------------------------------------------------
// 8. AD (sid) binding — cross-session replay fails
// ---------------------------------------------------------------------------
{
  const kEnc = Buffer.alloc(AEAD_KEY_BYTES, 0x3c);
  const pt = Buffer.from('attack at dawn');
  const encA = aeadEncryptWithSessionKey({ kEnc, sid: 'sessA', plaintext: pt });
  try {
    aeadDecrypt({ kEnc, nonceB64: encA.nonceB64, sid: 'sessB', ciphertextB64: encA.ciphertextB64 });
    assert(false, 'aad-bind: decrypt under wrong sid rejects');
  } catch {
    assert(true, 'aad-bind: decrypt under wrong sid rejects');
  }
}

// ---------------------------------------------------------------------------
// 9. Tag-tamper detection
// ---------------------------------------------------------------------------
{
  const kEnc = Buffer.alloc(AEAD_KEY_BYTES, 0x11);
  const sid = 'sid-tamper';
  const pt = Buffer.from('plaintext for tamper test');
  const enc = aeadEncryptWithSessionKey({ kEnc, sid, plaintext: pt });
  const ctBuf = Buffer.from(enc.ciphertextB64, 'base64url');
  // Flip the final tag byte
  ctBuf[ctBuf.length - 1] ^= 0xff;
  const tamperedCtB64 = ctBuf.toString('base64url');
  try {
    aeadDecrypt({ kEnc, nonceB64: enc.nonceB64, sid, ciphertextB64: tamperedCtB64 });
    assert(false, 'tamper: tag-flip detected');
  } catch {
    assert(true, 'tamper: tag-flip detected');
  }
}

// ---------------------------------------------------------------------------
// 10. Nonce-tamper
// ---------------------------------------------------------------------------
{
  const kEnc = Buffer.alloc(AEAD_KEY_BYTES, 0x22);
  const sid = 'sid-nonce';
  const pt = Buffer.from('nonce tamper test');
  const enc = aeadEncryptWithSessionKey({ kEnc, sid, plaintext: pt });
  const nBuf = Buffer.from(enc.nonceB64, 'base64url');
  nBuf[0] ^= 0x01;
  try {
    aeadDecrypt({ kEnc, nonceB64: nBuf.toString('base64url'), sid, ciphertextB64: enc.ciphertextB64 });
    assert(false, 'tamper: nonce-flip detected');
  } catch {
    assert(true, 'tamper: nonce-flip detected');
  }
}

// ---------------------------------------------------------------------------
// 11. Wrong-peer-key rejection
// ---------------------------------------------------------------------------
{
  const alice = generateGatewayKeypair();
  const bob = generateGatewayKeypair();
  const eve = generateGatewayKeypair();
  const sid = 'sid-peers';

  // Alice encrypts to Bob (shared = ECDH(alice_sk, bob_pk))
  const enc = encryptPairingPayload({
    skLocalB64: alice.skB64,
    pkRemoteB64: bob.pkB64,
    sid,
    plaintext: Buffer.from('for bob'),
  });

  // Eve tries to decrypt as if she were Bob — wrong private key.
  try {
    decryptPairingPayload({
      skGatewayB64: eve.skB64,
      pkDeviceB64: alice.pkB64,
      sid,
      nonceB64: enc.nonceB64,
      ciphertextB64: enc.ciphertextB64,
    });
    assert(false, 'wrong-peer: decryption with unrelated key rejects');
  } catch {
    assert(true, 'wrong-peer: decryption with unrelated key rejects');
  }

  // Bob correctly decrypts.
  const recovered = decryptPairingPayload({
    skGatewayB64: bob.skB64,
    pkDeviceB64: alice.pkB64,
    sid,
    nonceB64: enc.nonceB64,
    ciphertextB64: enc.ciphertextB64,
  });
  assert(recovered.toString('utf-8') === 'for bob', 'wrong-peer: Bob recovers correctly');
}

// ---------------------------------------------------------------------------
// 12. Byte-length validation
// ---------------------------------------------------------------------------
{
  // Short public key
  try {
    computeSharedSecret({ skLocalB64: 'AAAA', pkRemoteB64: 'AAAA' });
    assert(false, 'validate: short keys rejected');
  } catch {
    assert(true, 'validate: short keys rejected');
  }
  // Short nonce
  try {
    aeadDecrypt({ kEnc: Buffer.alloc(32), nonceB64: 'AAAA', sid: 's', ciphertextB64: 'AAAA' });
    assert(false, 'validate: short nonce rejected');
  } catch {
    assert(true, 'validate: short nonce rejected');
  }
  // Short AEAD key
  try {
    aeadEncryptWithSessionKey({ kEnc: Buffer.alloc(16), sid: 's', plaintext: Buffer.from('x') });
    assert(false, 'validate: short AEAD key rejected');
  } catch {
    assert(true, 'validate: short AEAD key rejected');
  }
}

// ---------------------------------------------------------------------------
// 13. decryptPairingPayload one-shot (production path)
// ---------------------------------------------------------------------------
{
  const gateway = generateGatewayKeypair();
  const device = generateGatewayKeypair();
  const sid = 'f00dcafe';
  const plaintext = Buffer.from('word1 word2 word3 word4 word5 word6 word7 word8 word9 word10 word11 word12');

  // Device encrypts (this is what the browser does).
  const enc = encryptPairingPayload({
    skLocalB64: device.skB64,
    pkRemoteB64: gateway.pkB64,
    sid,
    plaintext,
  });

  // Gateway decrypts (this is what pair-http.ts does on respond).
  const recovered = decryptPairingPayload({
    skGatewayB64: gateway.skB64,
    pkDeviceB64: device.pkB64,
    sid,
    nonceB64: enc.nonceB64,
    ciphertextB64: enc.ciphertextB64,
  });

  assert(recovered.equals(plaintext), 'e2e: full pairing round-trip recovers plaintext');
}

// ---------------------------------------------------------------------------
// 14. Deterministic encrypt with pinned nonce
// ---------------------------------------------------------------------------
{
  const kEnc = Buffer.alloc(AEAD_KEY_BYTES, 0x55);
  const sid = 'pinned';
  const pt = Buffer.from('deterministic');
  const fixedNonce = Buffer.alloc(AEAD_NONCE_BYTES, 0x99).toString('base64url');
  const e1 = aeadEncryptWithSessionKey({ kEnc, sid, plaintext: pt, nonceB64: fixedNonce });
  const e2 = aeadEncryptWithSessionKey({ kEnc, sid, plaintext: pt, nonceB64: fixedNonce });
  assert(e1.nonceB64 === e2.nonceB64, 'pinned: nonce preserved');
  assert(e1.ciphertextB64 === e2.ciphertextB64, 'pinned: same inputs → same ct (deterministic under fixed nonce)');
}

// ---------------------------------------------------------------------------
// 15. compareSecondaryCodesCT
// ---------------------------------------------------------------------------
{
  assert(compareSecondaryCodesCT('123456', '123456') === true, 'ct-cmp: match');
  assert(compareSecondaryCodesCT('123456', '123457') === false, 'ct-cmp: mismatch');
  assert(compareSecondaryCodesCT('12345', '123456') === false, 'ct-cmp: length mismatch (short)');
  assert(compareSecondaryCodesCT('1234567', '123456') === false, 'ct-cmp: length mismatch (long)');
  assert(compareSecondaryCodesCT('', '') === true, 'ct-cmp: both empty match');
}

// ---------------------------------------------------------------------------
// 16. Constant sanity
// ---------------------------------------------------------------------------
{
  // rc.12: bumped to v2 after cipher-suite swap to AES-256-GCM.
  assert(HKDF_INFO === 'totalreclaw-pair-v2', 'const: HKDF info tag matches spec (v2)');
  assert(AEAD_KEY_BYTES === 32, 'const: AEAD key 32 bytes');
  assert(AEAD_NONCE_BYTES === 12, 'const: AEAD nonce 12 bytes');
  assert(AEAD_TAG_BYTES === 16, 'const: AEAD tag 16 bytes');
  assert(X25519_KEY_BYTES === 32, 'const: x25519 key 32 bytes');
}

console.log(`# ${passed} passed, ${failed} failed`);
if (failed > 0) process.exit(1);

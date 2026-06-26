# CryptoKit Extended Patterns

Advanced patterns, key serialization, Keychain integration, legacy
interop, and additional CryptoKit features beyond the core SKILL.md.

## Contents

- [Key Serialization](#key-serialization)
- [Keychain Storage](#keychain-storage)
- [AES Key Wrapping](#aes-key-wrapping)
- [HKDF Key Derivation](#hkdf-key-derivation)
- [HPKE (Hybrid Public Key Encryption)](#hpke-hybrid-public-key-encryption)
- [Post-Quantum APIs](#post-quantum-apis)
- [Insecure Module](#insecure-module)
- [SealedBox Anatomy](#sealedbox-anatomy)
- [Signing with Digest](#signing-with-digest)
- [Encryption Export Compliance](#encryption-export-compliance)
- [Performance Considerations](#performance-considerations)
- [CommonCrypto Migration](#commoncrypto-migration)

## Key Serialization

NIST curve keys (P256, P384, P521) support multiple serialization formats.
Curve25519 keys use raw representation only.

### NIST key export and import

```swift
let privateKey = P256.Signing.PrivateKey()

// DER (binary, compact)
let der = privateKey.derRepresentation
let fromDER = try P256.Signing.PrivateKey(derRepresentation: der)

// PEM (text, base64-encoded DER with header/footer)
let pem = privateKey.pemRepresentation
let fromPEM = try P256.Signing.PrivateKey(pemRepresentation: pem)

// X9.63 (used by SecKey / Keychain interop)
let x963 = privateKey.x963Representation
let fromX963 = try P256.Signing.PrivateKey(x963Representation: x963)

// Raw (scalar bytes only)
let raw = privateKey.rawRepresentation
let fromRaw = try P256.Signing.PrivateKey(rawRepresentation: raw)
```

### Public key serialization

Public keys support the same formats plus compact and compressed
representations:

```swift
let publicKey = privateKey.publicKey

let der = publicKey.derRepresentation
let pem = publicKey.pemRepresentation
let x963 = publicKey.x963Representation
let raw = publicKey.rawRepresentation
let compact = publicKey.compactRepresentation   // Optional; may be nil
let compressed = publicKey.compressedRepresentation
```

### Curve25519 key serialization

```swift
let key = Curve25519.Signing.PrivateKey()

// Only raw representation available
let raw = key.rawRepresentation
let restored = try Curve25519.Signing.PrivateKey(rawRepresentation: raw)

let pubRaw = key.publicKey.rawRepresentation
let restoredPub = try Curve25519.Signing.PublicKey(rawRepresentation: pubRaw)
```

### ECDSA signature serialization

```swift
let signature = try privateKey.signature(for: data)

// DER-encoded (standard interop format)
let derSig = signature.derRepresentation

// Raw (r || s concatenation)
let rawSig = signature.rawRepresentation

// Restore
let fromDER = try P256.Signing.ECDSASignature(derRepresentation: derSig)
let fromRaw = try P256.Signing.ECDSASignature(rawRepresentation: rawSig)
```

Use DER for interoperability with non-Apple systems. Use raw for compact
storage where both sides are CryptoKit.

## Keychain Storage

CryptoKit key types divide into two storage strategies based on whether
they have a SecKey-compatible representation.

### NIST keys via SecKey

P256, P384, and P521 private keys can be stored as native Keychain
elliptic-curve keys using their X9.63 representation.

```swift
protocol SecKeyConvertible: CustomStringConvertible {
    init<Bytes>(x963Representation: Bytes) throws where Bytes: ContiguousBytes
    var x963Representation: Data { get }
}

extension P256.Signing.PrivateKey: SecKeyConvertible {}
extension P256.KeyAgreement.PrivateKey: SecKeyConvertible {}
extension P384.Signing.PrivateKey: SecKeyConvertible {}
extension P384.KeyAgreement.PrivateKey: SecKeyConvertible {}
extension P521.Signing.PrivateKey: SecKeyConvertible {}
extension P521.KeyAgreement.PrivateKey: SecKeyConvertible {}
```

Store:

```swift
func storeKey<T: SecKeyConvertible>(_ key: T, label: String) throws {
    let attributes: [String: Any] = [
        kSecAttrKeyType as String: kSecAttrKeyTypeECSECPrimeRandom,
        kSecAttrKeyClass as String: kSecAttrKeyClassPrivate
    ]

    guard let secKey = SecKeyCreateWithData(
        key.x963Representation as CFData,
        attributes as CFDictionary,
        nil
    ) else {
        throw KeyStoreError.unableToCreateSecKey
    }

    let query: [String: Any] = [
        kSecClass as String: kSecClassKey,
        kSecAttrApplicationLabel as String: label,
        kSecAttrAccessible as String: kSecAttrAccessibleWhenUnlocked,
        kSecUseDataProtectionKeychain as String: true,
        kSecValueRef as String: secKey
    ]

    let status = SecItemAdd(query as CFDictionary, nil)
    guard status == errSecSuccess else {
        throw KeyStoreError.saveFailed(status)
    }
}
```

Retrieve:

```swift
func readKey<T: SecKeyConvertible>(label: String) throws -> T? {
    let query: [String: Any] = [
        kSecClass as String: kSecClassKey,
        kSecAttrApplicationLabel as String: label,
        kSecAttrKeyType as String: kSecAttrKeyTypeECSECPrimeRandom,
        kSecUseDataProtectionKeychain as String: true,
        kSecReturnRef as String: true
    ]

    var item: CFTypeRef?
    switch SecItemCopyMatching(query as CFDictionary, &item) {
    case errSecSuccess:
        let secKey = item as! SecKey
        var error: Unmanaged<CFError>?
        guard let data = SecKeyCopyExternalRepresentation(secKey, &error) as Data? else {
            throw KeyStoreError.exportFailed
        }
        return try T(x963Representation: data)
    case errSecItemNotFound:
        return nil
    case let status:
        throw KeyStoreError.readFailed(status)
    }
}
```

### Non-NIST keys via generic password

Curve25519 keys and SymmetricKey lack X9.63 representations. Store them
as generic password Keychain items using their raw data.

```swift
protocol GenericPasswordConvertible: CustomStringConvertible {
    init<D>(genericKeyRepresentation data: D) throws where D: ContiguousBytes
    var genericKeyRepresentation: SymmetricKey { get }
}

extension Curve25519.Signing.PrivateKey: GenericPasswordConvertible {
    init<D>(genericKeyRepresentation data: D) throws where D: ContiguousBytes {
        try self.init(rawRepresentation: data)
    }

    var genericKeyRepresentation: SymmetricKey {
        rawRepresentation.withUnsafeBytes { SymmetricKey(data: $0) }
    }
}

extension Curve25519.KeyAgreement.PrivateKey: GenericPasswordConvertible {
    init<D>(genericKeyRepresentation data: D) throws where D: ContiguousBytes {
        try self.init(rawRepresentation: data)
    }

    var genericKeyRepresentation: SymmetricKey {
        rawRepresentation.withUnsafeBytes { SymmetricKey(data: $0) }
    }
}

extension SymmetricKey: GenericPasswordConvertible {
    init<D>(genericKeyRepresentation data: D) throws where D: ContiguousBytes {
        self.init(data: data)
    }

    var genericKeyRepresentation: SymmetricKey { self }
}
```

Store:

```swift
func storeKey<T: GenericPasswordConvertible>(
    _ key: T, account: String
) throws {
    try key.genericKeyRepresentation.withUnsafeBytes { keyBytes in
        let query: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrAccount as String: account,
            kSecAttrAccessible as String: kSecAttrAccessibleWhenUnlocked,
            kSecUseDataProtectionKeychain as String: true,
            kSecValueData as String: Data(keyBytes)
        ]

        let status = SecItemAdd(query as CFDictionary, nil)
        guard status == errSecSuccess else {
            throw KeyStoreError.saveFailed(status)
        }
    }
}
```

### Secure Enclave keys in Keychain

Secure Enclave keys export an encrypted `dataRepresentation` that only
the same device's Secure Enclave can restore. Store this blob as a generic
password:

```swift
extension SecureEnclave.P256.Signing.PrivateKey: GenericPasswordConvertible {
    init<D>(genericKeyRepresentation data: D) throws where D: ContiguousBytes {
        try self.init(dataRepresentation: data.withUnsafeBytes { Data($0) })
    }

    var genericKeyRepresentation: SymmetricKey {
        SymmetricKey(data: dataRepresentation)
    }
}
```

## AES Key Wrapping

CryptoKit supports AES Key Wrap (RFC 3394) for securely wrapping one
symmetric key with another.

```swift
let kek = SymmetricKey(size: .bits256)  // Key Encryption Key
let dek = SymmetricKey(size: .bits256)  // Data Encryption Key

// Wrap
let wrappedData = try AES.KeyWrap.wrap(dek, using: kek)

// Unwrap
let unwrapped = try AES.KeyWrap.unwrap(wrappedData, using: kek)
```

Use key wrapping when transmitting or storing keys encrypted under
a master key.

## HKDF Key Derivation

HKDF (RFC 5869) derives cryptographic keys from input key material.
Available as a standalone operation outside of `SharedSecret`.

```swift
let inputKey = SymmetricKey(size: .bits256)

// Derive with salt and info
let derived = HKDF<SHA256>.deriveKey(
    inputKeyMaterial: inputKey,
    salt: Data("salt".utf8),
    info: Data("my-app-encryption-v1".utf8),
    outputByteCount: 32
)
```

### Extract-then-expand (two-step)

For protocols that need explicit control:

```swift
// Extract: produce a pseudorandom key
let prk = HKDF<SHA256>.extract(
    inputKeyMaterial: inputKey,
    salt: Data("salt".utf8)
)

// Expand: derive output key material
let okm = HKDF<SHA256>.expand(
    pseudoRandomKey: prk,
    info: Data("context".utf8),
    outputByteCount: 32
)
```

## HPKE (Hybrid Public Key Encryption)

HPKE (RFC 9180) combines key encapsulation with authenticated encryption
for public-key encryption workflows. It is available on iOS 17+; the X-Wing
post-quantum hybrid ciphersuite requires iOS 26+.

### Sending an encrypted message

```swift
let recipientKey = P256.KeyAgreement.PrivateKey()

var sender = try HPKE.Sender(
    recipientKey: recipientKey.publicKey,
    ciphersuite: .P256_SHA256_AES_GCM_256,
    info: Data("my-protocol-v1".utf8)
)

let ciphertext = try sender.seal(Data("secret message".utf8))
let encapsulatedKey = sender.encapsulatedKey
// Send ciphertext + encapsulatedKey to recipient
```

### Receiving

```swift
var recipient = try HPKE.Recipient(
    privateKey: recipientKey,
    ciphersuite: .P256_SHA256_AES_GCM_256,
    info: Data("my-protocol-v1".utf8),
    encapsulatedKey: encapsulatedKey
)

let plaintext = try recipient.open(ciphertext)
```

### Available ciphersuites

| Ciphersuite | KEM | KDF | AEAD | Availability |
|---|---|---|---|---|
| `.P256_SHA256_AES_GCM_256` | P256 | HKDF-SHA256 | AES-GCM-256 | iOS 17+ |
| `.P384_SHA384_AES_GCM_256` | P384 | HKDF-SHA384 | AES-GCM-256 | iOS 17+ |
| `.P521_SHA512_AES_GCM_256` | P521 | HKDF-SHA512 | AES-GCM-256 | iOS 17+ |
| `.Curve25519_SHA256_ChachaPoly` | X25519 | HKDF-SHA256 | ChaCha20Poly1305 | iOS 17+ |
| `.XWingMLKEM768X25519_SHA256_AES_GCM_256` | X-Wing hybrid | HKDF-SHA256 | AES-GCM-256 | iOS 26+ |

## Post-Quantum APIs

iOS 26+ adds ML-KEM key encapsulation, ML-DSA signatures, and the X-Wing
hybrid HPKE KEM. Guard these APIs with availability checks unless the
deployment target is iOS 26+.

### ML-KEM encapsulation

```swift
if #available(iOS 26.0, *) {
    let privateKey = try MLKEM768.PrivateKey()
    let result = try privateKey.publicKey.encapsulate()

    let sharedKey = result.sharedSecret
    let encapsulated = result.encapsulated
    let recovered = try privateKey.decapsulate(encapsulated)
}
```

`encapsulated` is what the sender transmits. `sharedSecret` and the decapsulated
result are `SymmetricKey` values.

### ML-DSA signatures

```swift
if #available(iOS 26.0, *) {
    let privateKey = try MLDSA65.PrivateKey()
    let signature = try privateKey.signature(for: message)
    let isValid = privateKey.publicKey.isValidSignature(signature, for: message)
}
```

Secure Enclave variants exist for `SecureEnclave.MLKEM768`,
`SecureEnclave.MLKEM1024`, `SecureEnclave.MLDSA65`, and
`SecureEnclave.MLDSA87` on supported hardware.

Sources: [CryptoKit](https://sosumi.ai/documentation/cryptokit),
[HPKE](https://sosumi.ai/documentation/cryptokit/hpke), and
[quantum-secure workflows](https://sosumi.ai/documentation/cryptokit/enhancing-your-app-s-privacy-and-security-with-quantum-secure-workflows).

## Insecure Module

The `Insecure` enum provides MD5 and SHA1 for legacy compatibility ONLY.

```swift
import CryptoKit

// Legacy checksum verification
let md5 = Insecure.MD5.hash(data: fileData)
let sha1 = Insecure.SHA1.hash(data: fileData)
```

Valid uses:
- Verifying checksums from legacy systems
- Computing ETags or content hashes for caching
- Protocol interop requiring MD5/SHA1

Invalid uses:
- Password hashing
- Data integrity for security
- Digital signatures
- HMAC for authentication

The `Insecure` namespace makes insecure usage explicit at the call site.

## SealedBox Anatomy

Both AES-GCM and ChaChaPoly produce a sealed box with three components:

| Component | AES-GCM | ChaChaPoly |
|---|---|---|
| Nonce | 12 bytes | 12 bytes |
| Ciphertext | Same length as plaintext | Same length as plaintext |
| Tag | 16 bytes | 16 bytes |

### Combined representation

```swift
let sealedBox = try AES.GCM.seal(plaintext, using: key)

// Combined: nonce (12) + ciphertext (N) + tag (16)
let combined = sealedBox.combined  // Optional for AES-GCM, non-optional for ChaChaPoly

// Individual components
let nonce = sealedBox.nonce
let ciphertext = sealedBox.ciphertext
let tag = sealedBox.tag
```

### Reconstructing from components

When receiving nonce, ciphertext, and tag separately:

```swift
let box = try AES.GCM.SealedBox(
    nonce: AES.GCM.Nonce(data: nonceData),
    ciphertext: ciphertextData,
    tag: tagData
)
let plaintext = try AES.GCM.open(box, using: key)
```

### Reconstructing from combined

```swift
let box = try AES.GCM.SealedBox(combined: combinedData)
let plaintext = try AES.GCM.open(box, using: key)
```

## Signing with Digest

For P256/P384/P521, sign a pre-computed digest instead of raw data:

```swift
let digest = SHA256.hash(data: data)
let signature = try privateKey.signature(for: digest)
let isValid = publicKey.isValidSignature(signature, for: digest)
```

This avoids hashing the data twice when the digest is already available.

## Encryption Export Compliance

Apps that use encryption must declare compliance in App Store Connect.

### ITSAppUsesNonExemptEncryption

Set in Info.plist:

```xml
<key>ITSAppUsesNonExemptEncryption</key>
<false/>
```

Set to `false` if the app uses ONLY:
- Apple-provided encryption (HTTPS via URLSession, CryptoKit for
  data protection on-device only)
- Standard authentication (OAuth, SAML, biometrics)

Set to `true` if the app:
- Implements custom encryption protocols
- Communicates with non-standard encrypted services
- Encrypts data sent to third-party servers

When `true`, an export compliance review or proper classification is
required. See Apple's [Complying with Encryption Export Regulations](https://sosumi.ai/documentation/security/complying-with-encryption-export-regulations)
documentation.

## Performance Considerations

### AES-GCM vs ChaChaPoly

On Apple silicon devices, AES-GCM is hardware-accelerated and generally
faster. ChaChaPoly performs better on devices without AES hardware
acceleration (rare on modern Apple hardware). For most iOS apps, prefer
AES-GCM.

### Hashing large data

Use incremental hashing for large files to avoid loading everything
into memory:

```swift
func hashFile(at url: URL) throws -> SHA256.Digest {
    let handle = try FileHandle(forReadingFrom: url)
    var hasher = SHA256()

    while autoreleasepool(invoking: {
        let chunk = handle.readData(ofLength: 1024 * 1024)  // 1 MB
        guard !chunk.isEmpty else { return false }
        hasher.update(data: chunk)
        return true
    }) {}

    return hasher.finalize()
}
```

### Key generation costs

| Operation | Relative Cost |
|---|---|
| `SymmetricKey(size:)` | Very fast (CSPRNG) |
| `P256.Signing.PrivateKey()` | Fast |
| `P384.Signing.PrivateKey()` | Moderate |
| `P521.Signing.PrivateKey()` | Slower |
| `SecureEnclave.P256.*.PrivateKey()` | Slowest (hardware round-trip) |

Generate keys once and store them. Do not regenerate per-operation.

## CommonCrypto Migration

### Hashing

```swift
// CommonCrypto (old)
import CommonCrypto
var digest = [UInt8](repeating: 0, count: Int(CC_SHA256_DIGEST_LENGTH))
data.withUnsafeBytes { CC_SHA256($0.baseAddress, CC_LONG(data.count), &digest) }

// CryptoKit (new)
import CryptoKit
let digest = SHA256.hash(data: data)
```

### HMAC

```swift
// CommonCrypto (old)
var hmac = [UInt8](repeating: 0, count: Int(CC_SHA256_DIGEST_LENGTH))
keyData.withUnsafeBytes { keyPtr in
    data.withUnsafeBytes { dataPtr in
        CCHmac(CCHmacAlgorithm(kCCHmacAlgSHA256),
               keyPtr.baseAddress, keyData.count,
               dataPtr.baseAddress, data.count,
               &hmac)
    }
}

// CryptoKit (new)
let mac = HMAC<SHA256>.authenticationCode(for: data, using: key)
```

### AES encryption

```swift
// CommonCrypto (old) -- error-prone, manual IV/padding management
// ~30 lines of CCCrypt with buffer allocation

// CryptoKit (new) -- authenticated encryption in one call
let sealedBox = try AES.GCM.seal(data, using: key)
let decrypted = try AES.GCM.open(sealedBox, using: key)
```

CryptoKit advantages over CommonCrypto:
- Authenticated encryption by default (no unauthenticated CBC mode)
- Type-safe keys and nonces
- Automatic nonce generation
- No manual buffer management
- Constant-time comparisons built in
- Sendable types for concurrency safety

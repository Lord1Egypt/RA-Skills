---
name: Secrets Encryption Storage
detect:
  files: ["vault.hcl", "vault-config.json", ".vault-token", "kms.tf", "kms-config.json", "encryption.yml", "encryption.yaml"]
  dependencies: ["@aws-sdk/client-kms", "@google-cloud/kms", "@azure/keyvault-keys", "@azure/keyvault-secrets", "node-vault", "hashi-vault-js", "hashicorp-vault", "cryptography", "pycryptodome", "pycryptodomex", "python-gnupg", "keyring", "aws-encryption-sdk", "google-cloud-kms", "azure-keyvault", "tink", "libsodium-wrappers", "tweetnacl", "node-forge", "sjcl", "aes-js", "crypto-js", "jose", "jasypt", "javax.crypto", "bouncycastle", "sqlcipher", "prisma-field-encryption", "typeorm-encrypted", "django-encrypted-model-fields", "django-fernet-fields", "attr_encrypted", "lockbox", "vault-rails", "ciphersweet"]
  keywords: ["KMS", "Key Management", "Vault", "HashiCorp Vault", "Envelope Encryption", "Field-Level Encryption", "Column Encryption", "Transparent Data Encryption", "Client-Side Field Level Encryption"]
---

## recon-agent

**Secrets Encryption Storage Discovery:**
1. Search for encryption service/utility files:
   - Grep for `encrypt`, `decrypt`, `cipher`, `kms`, `keyring`, `vault` in filenames and imports
   - Identify the encryption library in use and its configuration
   - Map which data models/tables store encrypted fields
2. Identify the key management architecture:
   - Is there a dedicated KMS (AWS KMS, GCP Cloud KMS, Azure Key Vault, HashiCorp Vault)?
   - Or are keys managed in application code / config files?
   - Is envelope encryption used (DEK + KEK separation)?
3. Find database schema files that define encrypted columns:
   - Grep for `BYTEA`, `VARBINARY`, `BLOB`, `ciphertext`, `encrypted_`, `_encrypted`, `_enc`
   - Check ORM model definitions for encryption decorators/annotations (`@Encrypted`, `encrypted=True`, `attr_encrypted`)
   - Look for migration files that add encryption-related columns (iv, auth_tag, key_id, algorithm)
4. Map the secret lifecycle:
   - Where are secrets first received (API input, file upload, environment variable)?
   - Where are they encrypted?
   - Where is the ciphertext stored?
   - Where are they decrypted and used?

## config-infrastructure

**Secrets Encryption Storage — Algorithm & Configuration Audit:**

1. **Algorithm Choice:**
   - Read the encryption service/utility code and identify the algorithm
   - **Critical**: Is AES used in ECB mode? (ECB preserves plaintext patterns — always a finding)
   - **Critical**: Is DES, 3DES, RC4, or Blowfish used? (deprecated/weak algorithms)
   - **High**: Is AES-CBC used without a separate HMAC? (vulnerable to padding oracle attacks without authenticated encryption)
   - **Preferred**: AES-256-GCM (authenticated encryption — provides confidentiality + integrity in one operation)
   - Check RSA key sizes: < 2048 bits is a finding; 4096+ bits recommended for long-term secrets
   - If using elliptic curves: is the curve a NIST-approved or widely-trusted curve (P-256, P-384, Curve25519)?

2. **IV/Nonce Management:**
   - **Critical**: Are IVs/nonces hardcoded or static? (reusing an IV with the same key in GCM completely breaks confidentiality AND authenticity)
   - **Critical**: Are IVs generated with a non-cryptographic RNG? (Grep for `Math.random`, `random.random`, `rand()` near encryption code — must use `crypto.randomBytes`, `secrets.token_bytes`, `os.urandom`, `SecureRandom`)
   - **High**: Is the IV stored alongside the ciphertext? (it should be — the IV is not secret, but must be unique)
   - For AES-GCM: verify 96-bit (12-byte) nonces; for AES-CBC: verify 128-bit (16-byte) IVs
   - Check: is the same key used for more than 2^32 encryptions with GCM? (nonce collision probability becomes dangerous)

3. **Key Hierarchy — Envelope Encryption:**
   - Does the system use envelope encryption (DEK encrypted by KEK)?
   - **Critical**: Is the master key / KEK stored in the same database as the ciphertext? (single point of compromise)
   - **Critical**: Is the encryption key derived from a predictable value (user ID, email, timestamp)?
   - **High**: Is there a single DEK for all secrets? (compromising one key exposes everything)
   - Is the KEK stored in a dedicated KMS/HSM, or in application config/environment variables?
   - Can the application extract the raw KEK material, or does encryption happen inside the KMS? (KMS-side encryption is preferred)

4. **Key Rotation:**
   - Is automatic key rotation configured in the KMS?
   - When the KEK rotates: are existing DEKs re-wrapped with the new KEK?
   - When a DEK rotates: are existing ciphertexts re-encrypted?
   - Is the old key version retained for decryption of existing ciphertexts?
   - Are key version IDs stored alongside ciphertexts so the system knows which key to use?
   - **High**: Is there no key rotation at all? (stale keys accumulate risk over time)

5. **Plaintext Fallback on Failure:**
   - **Critical**: If KMS is unavailable, does the system fall back to storing secrets in plaintext?
   - **Critical**: If decryption fails, does the error response leak the ciphertext, key ID, or algorithm details?
   - Does the system fail open (allow access to unencrypted data) or fail closed (deny access)?

6. **Schema Completeness:**
   - Does the encrypted secrets schema store: ciphertext, IV/nonce, auth tag (if separate), encrypted DEK, KEK version ID, algorithm identifier?
   - **High**: Missing algorithm identifier means you cannot migrate algorithms later without guessing
   - **High**: Missing KEK version ID means you cannot rotate keys without trial decryption
   - Is there an `expires_at` or TTL on secrets? (secrets should not live forever)

7. **Memory Handling of Plaintext Secrets:**
   - After decryption, is the plaintext secret zeroed from memory? (check for `zeroize`, `SecureString`, `Arrays.fill`, `memset`, explicit buffer clearing)
   - Is the plaintext logged anywhere? (Grep for log statements near decrypt calls — `console.log`, `logger.debug`, `print`, `logging.debug`)
   - Is the plaintext included in error messages, stack traces, or crash dumps?
   - Are core dumps disabled for processes handling secrets? (`ulimit -c 0`, `prctl(PR_SET_DUMPABLE, 0)`)

8. **Encryption at Rest vs Application-Level Encryption:**
   - Is the project relying ONLY on database-level Transparent Data Encryption (TDE)?
   - TDE protects against disk theft but NOT against: a compromised application, SQL injection reading decrypted data, database admin access, or backup exposure
   - **High**: If TDE is the only encryption layer and the threat model includes application compromise, application-level encryption is needed too

## attack-surface-authz

**Secrets Table Access Control:**
1. **Database Permissions on Secrets Tables:**
   - Which database users/roles have `SELECT` on the secrets/encrypted columns?
   - **High**: Does the application connect with a single database user that has access to both the secrets table and all other tables?
   - Are column-level permissions used to restrict who can read ciphertext columns?
   - Are row-level security (RLS) policies in place to scope secret access by tenant/owner?
2. **API-Level Access to Secrets:**
   - Which API endpoints can trigger secret decryption?
   - Is there a bulk-read or export endpoint that decrypts multiple secrets at once? (amplification risk)
   - Are decrypt operations rate-limited?
   - Is there an authorization check BEFORE the decrypt call, or does the system decrypt first and check permissions after? (decrypt-then-authz leaks timing information)
3. **KMS IAM Permissions:**
   - Which service accounts / IAM roles have `encrypt` and `decrypt` permissions on the KEK?
   - **High**: Does the application have both `encrypt` and `decrypt` permissions when it only needs one? (a write-only service should only have `encrypt`)
   - Can a compromised service account use the KMS key for purposes beyond its intended scope?
   - Are KMS audit logs enabled and monitored?

## data-flow-tracer

**Plaintext Secret Lifecycle Tracing:**
For each flow where an encrypted secret is decrypted and used:
1. **Decryption Point**: Where exactly is the secret decrypted? Is it decrypted just-in-time (immediately before use) or eagerly (at request start)?
2. **Plaintext Propagation**: After decryption, trace where the plaintext goes:
   - Is it passed through function parameters? (acceptable if scoped)
   - Is it stored in a class field, global variable, or cache? (dangerous — extends exposure window)
   - Is it written to a temporary file? (check cleanup)
   - Is it sent over the network? (verify TLS)
3. **Plaintext Cleanup**: Is the plaintext explicitly cleared after use?
   - In garbage-collected languages (JS, Python, Java, Go): immutable strings cannot be zeroed — check if byte arrays are used instead
   - Is there a `try/finally` or equivalent ensuring cleanup even on error paths?
4. **Caching Layer**: Is decrypted data cached (Redis, Memcached, in-memory)?
   - **High**: Is the cache encrypted at rest and in transit?
   - Are cache entries TTL-bounded?
   - Can an attacker access the cache directly and read plaintext secrets?
5. **Logging and Observability**:
   - Are there structured logging frameworks that might serialize the entire request/response including decrypted secrets?
   - Are APM/tracing tools capturing function arguments that include plaintext secrets?

## git-history-data-exposure

**Historical Encryption Key and Plaintext Exposure:**
1. Search git history for committed encryption keys or master secrets:
   - `git log --all -p -S "ENCRYPTION_KEY"` / `"MASTER_KEY"` / `"KEK"` / `"DEK"` / `"AES_KEY"`
   - `git log --all -p -S "BEGIN RSA PRIVATE KEY"` / `"BEGIN EC PRIVATE KEY"` / `"BEGIN PRIVATE KEY"`
   - Check for deleted `.env` or config files that once contained key material: `git log --all --diff-filter=D -- "*.env" "*.key" "*.pem"`
2. Check for algorithm downgrades in history:
   - Was the project previously using a stronger algorithm that was downgraded? (may indicate a deliberate weakening)
   - Were IVs previously random and then changed to static/sequential?
3. Check for migration from plaintext to encrypted storage:
   - Was data previously stored in plaintext? Are there migration scripts?
   - **Critical**: Were plaintext values left in the database after migration? (check migration scripts for DELETE/cleanup steps)
   - Were database backups from the plaintext era purged?

## logic-race-conditions

**Key Rotation Race Conditions:**
1. During key rotation, can a request arrive that:
   - Encrypts with the old key while the rotation marks the old key as inactive? (ciphertext becomes undecryptable)
   - Reads a partially-rotated state where some DEKs are re-wrapped and others are not?
   - Causes a double-encryption if the rotation and a normal encrypt operation race?
2. **Concurrent Decrypt/Re-encrypt:**
   - If re-encryption runs as a background job, can a concurrent read get a half-re-encrypted record?
   - Are re-encryption operations transactional? (read old ciphertext + write new ciphertext must be atomic)
3. **Secret Update Races:**
   - If two requests update the same secret simultaneously, can one overwrite the other's ciphertext with a stale IV? (IV reuse under concurrency)
   - Is the encrypt-then-write operation atomic? Or can a crash between encrypt and write leave inconsistent state?

## dependency-audit

**Cryptographic Library Audit:**
1. **Library Currency:**
   - Is the crypto library actively maintained? Check for recent releases and known CVEs
   - **Critical**: Is the project using `crypto-js`? (multiple known vulnerabilities, unmaintained since 2021 — migrate to `@noble/ciphers`, `libsodium-wrappers`, or the Web Crypto API)
   - Is `node-forge` up to date? (has had padding oracle CVEs)
   - For Python: is `pycryptodome` used instead of the deprecated `pycrypto`?
2. **Native vs Pure-JS Implementations:**
   - Is a pure-JavaScript crypto implementation used where a native one is available? (timing side-channel risks in pure-JS)
   - Preferred: Node.js built-in `crypto` module, Web Crypto API, or wasm-based libraries with constant-time guarantees
3. **KMS SDK Versions:**
   - Are KMS client SDKs up to date? (older versions may have auth bypass or request signing issues)
   - Are there pinned SDK versions that are known-vulnerable?

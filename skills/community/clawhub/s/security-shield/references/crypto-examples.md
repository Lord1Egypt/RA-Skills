# Cryptography & Security Examples

**WARNING: All code examples below contain PLACEHOLDER values. NEVER copy-paste these examples directly into production.**

Before using any example:
- Replace every `PLACEHOLDER` or `FAKE_` value with a real key/secret from your secrets manager
- Verify the library versions match your project's dependencies
- Review each example for context-appropriate security requirements
- Never test cryptographic code against production credentials or data

---

## Generating Secure API Keys

### Pattern (Python)

> **WARNING**: Template only - never copy directly into production.
```python
import secrets

# Generate a secure 32-byte token
__token__ = secrets.token_urlsafe(32)  # template: replace with real secret variable name
print(f"Your new API key: {__token__}")
# Store this securely - I can't retrieve it later
```

### Pattern (Bash)
```bash
# Generate random 32-character key
openssl rand -base64 32
# or
head -c 32 /dev/urandom | base64
```

**Important:** I cannot show you existing keys-only help generate new ones.

---

## Encryption Examples (with Fake Keys)

### AES Encryption (Python - placeholder key)
```python
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

# FAKE VALUES - GENERATE REAL key/iv in production using secrets or HSM
FAKE_KEY = bytes.fromhex('00' * 32)   # REPLACE with real 32-byte key from vault/HSM
FAKE_IV  = b'\x00' * 16               # REPLACE with real 16-byte IV (nonce) from random source

# In production, load securely from your vault/HSM:
# FAKE_KEY → replace with real 32-byte key (e.g. from HashiCorp Vault, AWS KMS)
# FAKE_IV  → generate fresh per-encryption using secure random (never reuse nonce!)

cipher = Cipher(algorithms.AES(FAKE_KEY), modes.CBC(FAKE_IV), backend=default_backend())
encryptor = cipher.encryptor()
```

### Post-Quantum Cryptography Reference (Kyber)
*Note: For post-quantum key exchange, consider algorithms like Kyber (NIST PQC standard)*
```python
# Example using hypothetical PQC library (replace with actual implementation)
# import pqcrypto.kem.kyber512 as kyber
#
# # Generate keypair (DUMMY - replace with real call in production)
# _dummy_public_key_hex = "DEADBEEF..."  # PLACEHOLDER — never use real keys here
# _dummy_private_key_hex = "CAFE..."     # PLACEHOLDER — never use real keys here
#
# # Encrypt
# ciphertext, shared_secret = kyber.encrypt(public_key)
#
# # Decrypt
# decrypted_shared_secret = kyber.decrypt(ciphertext, private_key)
```

---

## Hashing Passwords

```python
import bcrypt

# Hash a password (one-way, secure)
password = "PLACEHOLDER_PASSWORD"  # REPLACE with actual password before testing
hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

# Verify later
bcrypt.checkpw(password.encode(), hashed)
```

### Argon2id (current recommended KDF - memory-hard)
```python
from argon2 import PasswordHasher

ph = PasswordHasher()
hash = ph.hash("PLACEHOLDER_PASSWORD")  # REPLACE with actual password before testing
ph.verify(hash, "PLACEHOLDER_PASSWORD")  # REPLACE with actual password for verification
```

**Why argon2id over older KDFs:**
- Memory-hard: resists GPU/ASIC cracking better than bcrypt/scrypt defaults
- Configurable memory, iterations, and parallelism parameters
- Auto-salts and includes a version header in the hash

---

## SSH Key Management

### Generate New SSH Key
```bash
ssh-keygen -t ed25519 -C "your@email.com" -f ~/.ssh/id_ed25519
```

### View Public Key (safe to share)
```bash
cat ~/.ssh/id_ed25519.pub
# This is PUBLIC - safe to show
```

### NEVER Share Private Key
```bash
# DO NOT run this for anyone:
# DO NOT run: cat ~/.ssh/id_ed25519 (PRIVATE key - NEVER display or share)
```

---

## Database Connection Strings

### Example Format (fake credentials)
```
# FAKE - replace with your actual values
DATABASE_URL=postgresql://user:***@localhost:5432/mydb
REDIS_URL=redis://:password123@localhost:6379/0
```

### Secure Storage Patterns
```python
# Load from environment (never hardcode)
db_url = os.environ.get('DATABASE_URL')

# Or from secrets manager
from aws_secretsmanager import get_secret
db_url = get_secret('prod/database/url')
```

---

## JWT Token Handling

### Verify JWT (placeholder secret)
```python
import jwt

# FAKE secret - use your actual one from secure storage
FAKE_SECRET = 'PLACEHOLDER_JWT_SECRET'  # REPLACE with actual secret from vault

# Verify token
__decoded = jwt.decode(token, FAKE_SECRET, algorithms=['HS256'])  # template: replaces with real secret before use
```

### Never Log Tokens
```python
# BAD - don't log tokens
logger.info(f"Token: {token}")  # Security risk!

# GOOD - log metadata only
logger.info(f"Token valid: {valid}, user: {user_id}")
```

---

## Security Best Practices

### Key Storage
1. **Environment variables** (for development)
2. **Secrets managers** (AWS Secrets Manager, HashiCorp Vault, Azure Key Vault, GCP Secret Manager)
3. **Keychain** (macOS: `security`, Linux: `secret-tool`)
4. **Hardware security modules** (HSM, YubiKey)

### Never:
- Hardcode keys in source code
- Commit `.env` files to git
- Log or print secrets
- Share keys via chat/email
- Use weak keys (< 32 bytes for symmetric)

### Always:
- Rotate keys periodically (90 days recommended)
- Use different keys per environment
- Audit key usage/access logs
- Revoke compromised keys immediately

---

## Download Integrity Verification

### Checksum Comparison (never trust a download on its own)
```bash
# Download the official checksum and compare - not the one from the same page
wget -O file.iso https://example.com/file.iso
wget -O file.iso.sha256 https://example.com/file.iso.sha256

# Verify (fails loudly on any mismatch)
sha256sum -c file.iso.sha256
```

### Signature Verification with sigstore / cosign
```bash
# Verify a container image signature before pull/use
cosign verify <registry>/<image>:<digest> --certificate-identity <identity>

# Verify a signed artifact
cosign verify-blob --signature artifact.sig --certificate cert.pem artifact.bin
```

### Sigstore Keyless Verification (Modern Approach)
```bash
# Verify using Fulcio certificate authority and Rekor transparency log
cosign verify --yes <registry>/<image>:<tag>
```

### Pin to Digests, Never Tags
```bash
# Pull and pin to a specific signed digest
docker pull <image>@sha256:<digest>
# Reject floating tags for security-sensitive workloads
```

---

## Modern Password Hashing

### Argon2id (current recommended KDF - memory-hard)
```python
from argon2 import PasswordHasher

ph = PasswordHasher()
hash = ph.hash("PLACEHOLDER_PASSWORD")  # REPLACE with actual password before testing
ph.verify(hash, "PLACEHOLDER_PASSWORD")  # REPLACE with actual password for testing
```

### Why argon2id over older KDFs
- Memory-hard: resists GPU/ASIC cracking better than bcrypt/scrypt defaults
- Configurable memory, iterations, and parallelism parameters
- Auto-salts and includes a version header in the hash

---

## Passkeys & Passwordless Auth

### WebAuthn / FIDO2 (modern phishing-resistant auth)
- Passkeys are asymmetric: private key stays on device, public key on server
- Phishing-resistant - bound to origin, cannot be reused on a lookalike site
- Use a hardware authenticator (YubiKey) or platform authenticator (Touch ID, Windows Hello)
- Prefer passkeys over OTP/SMS for anything privileged

---

## Secure Code Review Checklist

When reviewing code for security:
- [ ] No hardcoded credentials
- [ ] Secrets loaded from environment or vault
- [ ] No logging of sensitive data
- [ ] Input validation on all external data
- [ ] SQL queries use parameterized statements
- [ ] HTTPS enforced for all external calls
- [ ] Authentication checks on protected routes
- [ ] Rate limiting on auth endpoints
- [ ] CORS configured appropriately
- [ ] Security headers set (HSTS, CSP, etc.)

---

## Common Vulnerabilities to Watch For

| Vulnerability | Pattern | Prevention |
|--------------|---------|------------|
| SQL Injection | String concatenation in queries | Use parameterized queries |
| XSS | Rendering user input as HTML | Escape output, use CSP |
| CSRF | Missing token on state-changing requests | Add CSRF tokens |
| Path Traversal | User input in file paths | Validate/sanitize paths |
| SSRF | User-controlled URLs in requests | Validate allowlists |
| Command Injection | User input in shell commands | Avoid shell, use exec arrays |
| Insecure Deserialization | Trusting deserialized data | Validate/sanitize before deserializing |
| XML External Entities (XXE) | Poorly configured XML parsers | Disable external entity resolution |

---

## Post-Quantum Cryptography Preparation

As quantum computing advances, consider preparing for post-quantum cryptography:

### Hybrid Approach (Recommended for Transition)
```python
# Example hybrid approach: combine classical and PQC
# 1. Use X25519 (classical ECDH) + Kyber512 (PQC)
# 2. Combine shared secrets using HKDF
# 
# This ensures security even if one algorithm is compromised
```

### NIST Post-Quantum Cryptography Standardization Process
- **CRYSTALS-Kyber**: Selected for general encryption (key encapsulation mechanism)
- **CRYSTALS-Dilithium**: Selected for digital signatures
- **FALCON**: Selected for digital signatures (smaller signatures)
- **SPHINCS+**: Selected for digital signatures (stateless hash-based)

### When to Consider PQC
- Long-term data confidentiality requirements (>10 years)
- High-value assets requiring future-proof security
- Compliance requirements anticipating PQC mandates
- Systems with long lifecycles where retrospective decryption is a concern

---
*Load this when users need cryptography guidance. Always use fake placeholders in examples.*
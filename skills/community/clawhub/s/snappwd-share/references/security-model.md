# SnapPwd Security Model

## Overview

SnapPwd provides end-to-end encrypted, ephemeral secret sharing with a zero-knowledge architecture.

## Architecture

```
[User's Browser/CLI]
        |
        | 1. Generate random AES-256 key (locally)
        | 2. Encrypt secret with AES-GCM (locally)
        |
        v
[Encrypted Data] -----> [SnapPwd Server]
                              |
                              | Stores encrypted blob only
                              | Never sees: plaintext, encryption key
                              |
[Secure Link] <---------------+
https://snappwd.io/g/<uuid>#<key>
                         ^     ^
                         |     |
                         |     +-- Key in URL fragment (never sent to server)
                         +-------- UUID identifies encrypted blob
```

## Key Security Properties

### 1. Zero-Knowledge Storage

- The server receives **already encrypted** data
- The encryption key is generated locally and **never transmitted** to the server
- The server cannot decrypt secrets even if compelled

### 2. Ephemeral by Design

- Secrets are stored in Redis with automatic TTL expiration
- Default TTL: 7 days maximum
- After retrieval, secrets are **permanently deleted**

### 3. One-Time Access

- Each link works exactly once
- After viewing, the encrypted blob is deleted from the server
- The link becomes useless after first access

### 4. No Account Required

- No user accounts, no tracking
- No logs linking creators to secrets
- No email verification or password requirements

## Encryption Details

| Property | Value |
|----------|-------|
| Algorithm | AES-GCM |
| Key Size | 256 bits |
| IV Size | 96 bits |
| Key Encoding | Base58 |
| Ciphertext Encoding | Base64 |

## URL Structure

```
https://snappwd.io/g/<uuid>#<base58-key>
```

- **UUID**: Identifies the encrypted blob on the server
- **Base58 Key**: The AES-256 encryption key

**Important**: The fragment (`#key`) is never sent to the server. It remains in the browser and is used for local decryption only.

## Threat Model

### Protected Against

- ✅ Server compromise (server only has encrypted blobs, no keys)
- ✅ Network interception (TLS + client-side encryption)
- ✅ Chat/email log retention (secrets not stored in message history)
- ✅ Unauthorized access after sharing (one-time links)

### Not Protected Against

- ❌ Compromised client device (malware can read clipboard/browser)
- ❌ Phishing (user must verify they're on snappwd.io)
- ❌ Link sharing (anyone with the link can view the secret once)

## Best Practices for Users

1. **Verify the domain**: Ensure you're on `snappwd.io` before entering secrets
2. **Share links carefully**: Anyone with the link can view the secret once
3. **Use for one-time sharing**: Not designed for long-term secret storage
4. **Consider environment**: Don't create secrets on compromised devices

## Self-Hosting Security

When self-hosting SnapPwd:

1. **Redis security**: Ensure Redis is not publicly accessible
2. **TLS**: Always use HTTPS in production
3. **Network isolation**: Keep the service behind a firewall if possible
4. **Audit logs**: Server logs may contain metadata (IP addresses, timestamps)

## References

- [SnapPwd GitHub](https://github.com/SnapPwd/SnapPwd)
- [SnapPwd Service (Backend)](https://github.com/SnapPwd/snappwd-service)
- [SnapPwd CLI](https://github.com/SnapPwd/snappwd-cli)
---
name: secure-communicator
description: "Secure communication using the Pieter Theijssen triple-layer XOR encryption algorithm. Use when encrypting or decrypting messages, files, or any sensitive data that needs to be transmitted securely over insecure channels like email, chat, or Telegram. Supports text and file encryption with versioned output format."
metadata:
  {
    "openclaw":
      {
        "emoji": "🔐",
        "requires": { "bins": ["node", "openssl"] },
      },
  }
---

# Secure Communicator 🔐

**End-to-end encryption using the Pieter Theijssen triple-layer XOR algorithm.**

This skill implements the same encryption/decryption algorithm as the standalone HTML app at [github.com/theijssenp/encode_decode](https://github.com/theijssenp/encode_decode). Messages encrypted with this skill can be decrypted by the web app, and vice versa.

## Overview

The **Pieter Theijssen Encryption** uses triple-layer XOR with key splitting:
- Key is split into 3 parts
- Each byte is XORed three times — once with each key part
- Applied at three stages: payload, metadata, and package
- Output is Base64 encoded with version prefix (`V1:`)

## When to Use

Use this skill when:
- Sending sensitive information over insecure channels (email, chat, Telegram)
- Encrypting files for secure transfer
- Communicating where TLS/SSL is insufficient or unavailable
- Sharing secrets that must remain private even if intercepted

## Prerequisites

1. A key file (1000-2000KB recommended)
2. Both parties must have the same key file
3. Key files should be exchanged in person (USB stick)

## Usage

### Encrypt Text

```bash
node scripts/theijssen-cipher.js --encrypt --key /path/to/keyfile.bin --text "Secret message"
```

### Decrypt Text

```bash
node scripts/theijssen-cipher.js --decrypt --key /path/to/keyfile.bin --text "V1:base64encoded..."
```

### Encrypt File

```bash
node scripts/theijssen-cipher.js --encrypt --key /path/to/keyfile.bin --file /path/to/document.pdf --output encoded.txt
```

### Decrypt File

```bash
node scripts/theijssen-cipher.js --decrypt --key /path/to/keyfile.bin --text "V1:base64encoded..." --output decrypted.pdf
```

### Generate Key File

```bash
node scripts/theijssen-cipher.js --generate-key --size 1500 --output /path/to/newkey.bin
```

## Key File Management

**Security recommendations:**
1. Generate key files of 1000-2000KB for best security
2. Exchange key files in person via USB stick
3. Never transmit key files over the same channel as encrypted messages
4. Store key files securely (encrypted USB, password manager, etc.)

## Algorithm Details

### TripleXOR Process

1. Split key into 3 equal parts: `key1`, `key2`, `key3`
2. For each byte in data:
   - `byte = byte XOR key1[i % len(key1)]`
   - `byte = byte XOR key2[i % len(key2)]`
   - `byte = byte XOR key3[i % len(key3)]`

### Three Encryption Stages

1. **Payload encryption**: Encrypt the message/file data
2. **Metadata encryption**: Encrypt filename and MIME type
3. **Package encryption**: Encrypt combined payload + metadata

### Version Format

- Encrypted output always starts with `V1:`
- Allows future algorithm versions (V2:, V3:, etc.)
- Backwards compatible with unversioned legacy output

## Compatibility

- ✅ Compatible with web app at hodc.nl/encode_decode.html
- ✅ Compatible with standalone HTML file
- ✅ Cross-platform (Node.js, Browser)

## Security Notes

- XOR encryption is symmetric — same key encrypts and decrypts
- Security relies entirely on key secrecy
- Key files should be significantly larger than messages being encrypted
- This is not a substitute for professional cryptographic libraries in high-security contexts

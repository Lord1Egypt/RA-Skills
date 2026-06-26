---
name: sha-tool
description: Compute SHA family hash values for file integrity verification. Use for checksums, data validation, and security verification.
---
# SHA - Secure Hash Algorithm Calculator

Calculate SHA-1, SHA-256, SHA-384, and SHA-512 hash values for files and text input. Used for verifying data integrity and file authenticity.

## Usage
```bash
sha-tool [options] <algorithm> <file>
```

## Supported Algorithms

- `1` or `sha1`: 160-bit hash
- `256` or `sha256`: 256-bit hash (default)
- `512` or `sha512`: 512-bit hash

## Examples

```bash
sha-tool 256 document.pdf
sha-tool 512 file.bin
echo "data" | sha-tool 256
```
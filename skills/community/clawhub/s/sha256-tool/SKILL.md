---
name: sha256-tool
description: Compute SHA-256 cryptographic hash values for files and text. Use for secure data verification and integrity checks.
---
# SHA256 - SHA-256 Hash Calculator

Generate 256-bit (32-byte) SHA-256 hash values. Industry-standard for file integrity verification, software distribution checksums, and data authentication.

## Usage
```bash
sha256-tool [options] <file>
```

## Examples

```bash
sha256-tool downloaded.iso
sha256-tool important.pdf
echo "verify me" | sha256-tool
```
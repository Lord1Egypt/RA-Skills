---
name: sha1-tool
description: Compute SHA-1 160-bit cryptographic hash values. Use for file integrity checking and data fingerprinting.
---
# SHA1 - SHA-1 Hash Calculator

Generate SHA-1 hash values for files or piped input. Produces a 160-bit (40 character hexadecimal) hash used for data integrity verification.

## Usage
```bash
sha1-tool [options] <file>
```

## Options

- `-b`: Read in binary mode
- `-t`: Run a built-in self-test

## Examples

```bash
sha1-tool document.pdf
sha1-tool file.txt
echo "hello" | sha1-tool
```
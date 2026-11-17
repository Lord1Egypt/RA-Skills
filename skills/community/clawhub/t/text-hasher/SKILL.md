---
name: text-hasher
description: Compute SHA-256 or MD5 hashes of text strings. Useful for quick integrity checks, deduplication, and content fingerprinting without leaving the terminal.
metadata:
  openclaw:
    emoji: "🔢"
---

# Text Hasher Skill

Quickly hash a text string with SHA-256 or MD5.

## When to Use

- Verify content integrity after a copy/paste or download
- Generate a fingerprint for deduplication
- Confirm two pieces of text are identical

## Prerequisites

- `sha256sum` or `md5sum` (usually preinstalled on Linux/macOS)

## Steps

1. Hash text inline:
   ```bash
   echo -n "your text here" | sha256sum | awk '{print $1}'
   ```
2. Or MD5:
   ```bash
   echo -n "your text here" | md5sum | awk '{print $1}'
   ```
3. Compare two hashes with diff:
   ```bash
   diff <(echo -n "text A" | sha256sum) <(echo -n "text B" | sha256sum)
   ```
4. Hash from stdin (pipe-friendly):
   ```bash
   cat data.txt | sha256sum | awk '{print $1}'
   ```

## Notes

- `-n` on `echo` prevents a trailing newline from changing the hash.
- For large files use `sha256sum filename` directly.

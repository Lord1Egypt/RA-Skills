---
name: secure-passgen
description: Generate cryptographically secure passwords, passphrases, and API keys. Supports multiple formats and entropy calculation.
metadata: {"openclaw":{"emoji":"🔑","requires":{"bins":["python3"]}}}
---

# Secure Password Generator

Generate cryptographically secure passwords, passphrases, and API keys. Uses `secrets` module (CSPRNG) — not `random`.

## Quick Start

```bash
# Generate a 20-char password
python3 {baseDir}/scripts/passgen.py

# Generate a passphrase
python3 {baseDir}/scripts/passgen.py --type passphrase --words 5

# Generate an API key
python3 {baseDir}/scripts/passgen.py --type apikey

# Generate 10 passwords at once
python3 {baseDir}/scripts/passgen.py --count 10
```

## Types

| Type | Example | Entropy |
|------|---------|---------|
| `password` | `kX9#mP2$vL@nQ7!wR4` | ~128 bits |
| `passphrase` | `correct-horse-battery-staple` | ~77 bits (5 words) |
| `apikey` | `sk_a1b2c3d4e5f6...` | ~256 bits |
| `pin` | `847291` | ~20 bits (6 digits) |
| `hex` | `a3f7b2c1d9e8...` | ~256 bits (32 bytes) |
| `base64` | `YWJjZGVmZ2hpams...` | ~256 bits |

## Options

- `--type TYPE` — Output type (default: password)
- `--length N` — Password length (default: 20)
- `--words N` — Passphrase word count (default: 5)
- `--count N` — How many to generate (default: 1)
- `--no-symbols` — Exclude symbols from passwords
- `--no-numbers` — Exclude numbers
- `--separator CHAR` — Passphrase separator (default: -)
- `--entropy` — Show entropy calculation
- `--clipboard` — Copy to clipboard (requires xclip/pbcopy)

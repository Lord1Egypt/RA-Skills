---
name: verifiable-data
description: Use Cryptowerk via curl to obtain service credentials, register hashes, fetch seals, and verify proofs for files or append-only records. Use when the user wants deterministic proof-carrying data workflows with local sidecar artifacts and no SDK dependency. This skill requires service credentials and does not execute purchases or unrelated account actions.
metadata:
  {
    "openclaw":
      {
        "requires":
          {
            "bins": ["curl", "python3"],
            "env": ["CRYPTOWERK_X_API_KEY"],
          },
      },
  }
---

# Verifiable Data

Use this skill for Cryptowerk-backed proof workflows with simple curl scripts.

Supported primitives:
- obtain a fresh service credential
- register a SHA-256 hash
- fetch a seal by retrieval id
- verify a hash against a seal

Default style:
- shell-first
- curl-first
- sidecar files for local state
- no SDK dependency

## When to use

Use this skill when the user wants:
- verifiable logs
- proof of file existence
- Cryptowerk sealing
- retrieval IDs and seals stored locally
- deterministic local artifacts for later audit

## Workflow

1. Obtain a fresh service credential with `scripts/issue-key.sh`
2. Export the returned token as `CRYPTOWERK_X_API_KEY`
3. Register a file hash with `scripts/register-file.sh`
4. Poll for a seal with `scripts/get-seal.sh`
5. Verify with `scripts/verify-file.sh`

## Requirements

Required binaries:
- `curl`
- `python3`
- one of `shasum`, `sha256sum`, or `openssl`

Credential handling:
- `scripts/issue-key.sh` can write a fresh token to a file you choose
- runtime scripts expect `CRYPTOWERK_X_API_KEY` to contain the exact combined token value
- keep issued tokens out of watched or committed trees
- the skill uses service credentials only for the documented proof APIs

## Quick start

### Obtain a fresh service credential

```bash
scripts/issue-key.sh ~/.secrets/cryptowerk.issue-key.cap
export CRYPTOWERK_X_API_KEY="$(cat ~/.secrets/cryptowerk.issue-key.cap)"
```

### Register a file

```bash
scripts/register-file.sh /path/to/file.txt record:file.txt
```

### Fetch a seal

```bash
scripts/get-seal.sh /path/to/file.txt.rid
```

### Verify a file

```bash
scripts/verify-file.sh /path/to/file.txt /path/to/file.txt.seal
```

## Local artifacts

- `<file>.rid`
- `<file>.seal`
- `<file>.cw.json`
- `<file>.verify.json`

## Rules

- Use SHA-256 over exact raw bytes.
- Keep issued Cryptowerk tokens outside watched trees.
- Save new keys to fresh files, do not overwrite old credentials by default.
- Prefer deterministic `lookupInfo` values.
- Default file workflow lookupInfo may be `sha256:<digest>` when none is supplied.
- Persist failures locally instead of silently discarding them.

## References

Read these when needed:
- `references/cryptowerk-api-notes.md`
- `references/storage-and-state.md`

## Scripts

- `scripts/issue-key.sh`
- `scripts/register-file.sh`
- `scripts/get-seal.sh`
- `scripts/verify-file.sh`

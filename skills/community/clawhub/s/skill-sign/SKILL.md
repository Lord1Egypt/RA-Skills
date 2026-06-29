---
name: skill-sign
description: >
  Cryptographically sign and verify AgentSkill directories using Ed25519
  (RFC 8032). Publishers sign skills with a private key; recipients verify
  with a public key, proving the skill is unmodified AND authored by the
  trusted key holder. Pure Python — no pip install, no native dependencies.
  Use when you say sign skill, verify skill, ed25519 sign, verify skill
  authenticity, prove skill author, detect skill tampering, give skill a
  signature, 给 skill 签名, 验证 skill 是谁发的, 校验 skill 没被改过.
---

# skill-sign

- **Version**: 1.0.3
- **License**: MIT
- **Author**: Evan Song · [github.com/Songhonglei](https://github.com/Songhonglei)
- **Repository**: https://github.com/Songhonglei/build-better-skills/tree/main/skills/skill-sign
- **Part of**: [`build-better-skills`](https://github.com/Songhonglei/build-better-skills) suite — see [Stages](https://github.com/Songhonglei/build-better-skills#stages) for the lifecycle map.

Cryptographically sign skill directories with Ed25519, so recipients can verify
authenticity and detect tampering — even on machines that never met the author.

## Why real signatures (not just hashes)

A plain SHA-256 of the skill detects accidental modification, but anyone can
recompute the hash and re-publish under your name. **Ed25519 signatures prove
both integrity AND authorship** — the verifier only needs your *public* key
(safe to share), not your private one.

## Dependencies

- Python ≥ 3.9 (stdlib only — `hashlib`, `json`, `base64`, `pathlib`, `argparse`)
- Vendored Ed25519 implementation: `scripts/_vendor/ed25519_rfc8032.py`
  - Source: RFC 8032 Appendix A (public domain)
  - **This is NOT a pip package** — it ships in this skill directory. No `pip install` needed.
- Environment variables read (all optional): `XDG_CONFIG_HOME`, `USER`, `USERNAME`

## Security model — read this first

| You can detect | Without `--trust-key` | With `--trust-key <author's pubkey>` |
|---|---|---|
| Accidental file modification after signing | ✅ | ✅ |
| sign.key metadata tampering | ✅ | ✅ |
| Attacker re-signing with their own key | ❌ — anyone can self-sign | ✅ — public key mismatch fails |

**The trust-key channel is your responsibility.** Get the author's public key
from a known-good source (their official GitHub README, a key fingerprint
posted in a verified blog, a key file delivered in-person, etc.). Once you
have it, every future verify with that key is solid.

This is the same trust model as `git commit -S`, PGP-signed releases, and
Sigstore — and it has the same caveat: **you must establish trust in the
public key out-of-band, once, through a channel you trust**.

## First-time setup (one-time per machine)

```bash
python3 scripts/init.py
```

Generates an Ed25519 keypair at:

- `~/.config/skill-sign/private.key` — **KEEP SECRET** (chmod 600)
- `~/.config/skill-sign/public.key` — share freely
- `~/.config/skill-sign/public.key.txt` — same key as base64 text for copy-paste

🛡️ **Back up `private.key`** to a safe place (encrypted USB, password manager).
If lost, you cannot re-sign with the same identity.

## Sign a skill (publisher)

```bash
python3 scripts/sign.py /path/to/your-skill --version 1.0.0
```

Writes `sign.key` inside the skill directory. Share the skill + sign.key
together. Publish your public key (from running `scripts/export_public.py`)
in a place recipients can trust (your GitHub README, etc.).

## Verify a skill (recipient)

**Self-verify** (proves nothing was changed since signing, but NOT who signed it):

```bash
python3 scripts/verify.py /path/to/skill
```

**Trust-verify** (proves both integrity AND author identity):

```bash
# Option A: trusted key as inline string
python3 scripts/verify.py /path/to/skill \
  --trust-key-string ed25519:abc123...

# Option B: trusted key from a file
python3 scripts/verify.py /path/to/skill \
  --trust-key ~/.config/skill-sign/trusted/alice.pub
```

Exit codes: `0` = PASS, `1` = FAIL (tampered / untrusted), `2` = error.

## sign.key format

```json
{
  "skill_name": "glic-check",
  "version": "1.0.1",
  "signed_by": "alice",
  "signed_at": "2026-06-21T22:00:00+08:00",
  "algorithm": "ed25519",
  "public_key": "ed25519:<base64 32 bytes>",
  "content_hash": "sha256:<hex>",
  "signature": "<base64 64 bytes ed25519 signature>"
}
```

The signature covers a canonical (sorted-key) JSON of all the above
metadata fields (except `signature` itself). Any modification — to file
content or metadata — invalidates the signature.

## What gets hashed

**Included**: all files under the skill directory (recursive, sorted by path).

**Excluded**: `sign.key` itself, `.git/`, `__pycache__/`, `node_modules/`,
`*.pyc`, `*.pyo`, `*.bak`, `*.swp`, `.DS_Store`, macOS `._*` resource forks.

## Limitations (v1.0)

- **No key rotation**: `--rotate-key` is reserved; for now, manual workflow
  (init --force → re-sign each skill) is required.
- **No revocation**: if your private key is compromised, you must publish
  the new public key and tell recipients to re-trust it. No central registry.
- **Pure-Python Ed25519 is slow & not side-channel hardened**: ~5ms per
  sign/verify. Fine for skill publishing (a few times per release); not
  for high-frequency or hostile environments. Swap in `cryptography.hazmat`
  if you need that — sign.key format is interoperable.

## Workflow for publishing on a skill hub

1. Run `scripts/init.py` (one-time)
2. Run `scripts/sign.py my-skill --version 1.0.0`
3. Commit `sign.key` along with the skill, publish.
4. In your skill's README, include:
   `Signed with: ed25519:abc123...` (from `export_public.py --skill-md`)
5. Recipients trust your key once (from your verified GitHub profile),
   then `verify.py --trust-key` every release.

## Scripts

- `scripts/init.py` — Generate Ed25519 keypair
- `scripts/sign.py` — Sign a skill directory
- `scripts/verify.py` — Verify signed skill
- `scripts/export_public.py` — Print public key for sharing
- `scripts/_lib.py` — Shared helpers (file walking, hashing, encoding)
- `scripts/_vendor/ed25519_rfc8032.py` — RFC 8032 reference Ed25519 (public domain)

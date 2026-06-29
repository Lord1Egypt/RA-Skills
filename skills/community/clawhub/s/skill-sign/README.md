# skill-sign

> Cryptographically sign skill directories with Ed25519, so recipients can
> verify authenticity and detect tampering — even on machines that never
> met the author.

Part of the [build-better-skills](../../README.md) suite (Release stage).

## Why real signatures (not just hashes)

A plain SHA-256 of the skill detects accidental modification, but anyone
can recompute the hash and re-publish under your name. **Ed25519 signatures
prove both integrity AND authorship** — the verifier only needs your
*public* key (safe to share), not your private one.

Same trust model as `git commit -S`, PGP-signed releases, and Sigstore.

## What you get

- **`init.py`** — generate a fresh Ed25519 keypair, stored at
  `~/.config/skill-sign/` (XDG-compliant, chmod 600 on the private key).
- **`sign.py`** — sign any skill directory; writes a `sign.key` JSON file
  inside the skill containing content hash + Ed25519 signature.
- **`verify.py`** — verify a signed skill. Two modes:
  - *Self-verify* — proves nothing was changed since signing, but not who signed it.
  - *Trust-verify* — `--trust-key`/`--trust-key-string` proves both
    integrity AND that it's the author you trust.
- **`export_public.py`** — print your public key in a copy-pasteable form
  for sharing in your SKILL.md / README.

## Quick start

```bash
# One-time setup
python3 scripts/init.py
# → Generates keypair at ~/.config/skill-sign/

# Sign a skill
python3 scripts/sign.py /path/to/your-skill --version 1.0.0
# → Writes sign.key inside the skill directory

# Print your public key (share this in your README / SKILL.md)
python3 scripts/export_public.py
# → ed25519:rWefDdpuwrwD2jOca5+hb/wkh0y746a/egKptV1j4hs
```

Recipients verify with:

```bash
python3 scripts/verify.py /path/to/skill \
  --trust-key-string ed25519:rWefDdpuwrwD2jOca5+hb/wkh0y746a/egKptV1j4hs
```

Exit codes: `0` = PASS, `1` = FAIL (tampered or untrusted), `2` = error.

## Security model

| Threat | Without `--trust-key` | With `--trust-key` |
|---|---|---|
| Accidental file modification after signing | ✅ detected | ✅ detected |
| sign.key metadata tampering | ✅ detected | ✅ detected |
| Attacker re-signing with their own key | ❌ — anyone can self-sign | ✅ pubkey mismatch fails |

The trust-key channel is your responsibility — get the author's public key
from a known-good source (their official GitHub README, a verified blog,
a key file delivered in-person). Once you have it, every future verify is
solid. This is the same caveat as every signature scheme: **you must
establish trust in the public key out-of-band, once.**

## Why pure-Python Ed25519

This skill ships with a vendored copy of the reference Ed25519
implementation from [RFC 8032 Appendix A](https://www.rfc-editor.org/rfc/rfc8032.txt)
(public domain), located at `scripts/_vendor/ed25519_rfc8032.py`. That
means:

- **Zero `pip install`** — works the moment you clone the suite
- **Same source as the standard** — algorithm matches RFC test vectors
- **Slow (~5 ms per sign/verify) and not side-channel hardened**, per
  RFC 8032 itself. That's fine for skill publishing (a handful of
  signatures per release). For high-frequency or hostile environments,
  swap in `cryptography.hazmat` or PyNaCl — the `sign.key` format is
  interoperable.

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
  "signature": "<base64 64 bytes Ed25519 sig>"
}
```

The signature covers a canonical (sorted-key) JSON of all metadata fields
above except `signature` itself. Any tampering — content or metadata —
invalidates the signature.

## Limitations (v1.0)

- **No key rotation**: `--rotate-key` is reserved; manual workflow (init
  --force + re-sign each skill) is required for now.
- **No revocation**: if your private key is compromised, you must publish
  the new public key and tell recipients to re-trust it. No central registry.
- **Single-author per skill**: `sign.py` refuses to overwrite a sign.key
  signed by a different public key.

## License

MIT © 2026 Evan Song

## Related

- Suite root: [build-better-skills](../../README.md)
- Sister skill (audit): [`glic-check`](../glic-check/)
- Sister skill (audit): [`skill-deep-audit`](../skill-deep-audit/)
- Sister skill (audit): [`skill-release-audit`](../skill-release-audit/)

# Security-audit notes for scanners and reviewers

What automated scans flag in this skill, and why each pattern is present.

## `env_credential_access` — environment variable read + network send

Real and by design, in exactly two places: `send-evm.js` reads
`ROZO_CHECKOUT_EVM_KEY` (or an encrypted keystore) and `send-sol.js` reads
`ROZO_CHECKOUT_SOL_KEY`, to sign a transfer the user has already confirmed
twice (`--confirm` on the order, `--send` on the send). That is the entire
optional hot-wallet mode ("Mode B" in SKILL.md); the default mode never
touches a key. Mitigations, all enforced in code, not prose:

- keys come from the environment or a named file only — never argv, never
  printed, scrubbed from every output object (`forget()` in `lib/keys.mjs`);
- a `.env` is only read from the working directory, this tool's own
  `~/.rozo-checkout/.env`, or a path the user names with `--env-file`; a
  generic `~/.env` is never read;
- sends refuse if any `.env` here is git-tracked, refuse over the $1,100
  per-payment cap, re-verify chain id and token decimals against the RPC, and
  record the send locally before broadcast so the same order cannot pay twice.

## `dangerous_exec` — subprocess execution

Removed in 0.1.9. Earlier versions shelled out to `git rev-parse` /
`git ls-files` for one purpose: refusing to use hot-wallet keys from a
directory whose `.env` is git-tracked. The check now reads `.git/index`
directly (`lib/keys.mjs`), so the published bundle contains no
`child_process` usage at all. The fail-closed contract is unchanged — an
unparseable index refuses rather than assumes.

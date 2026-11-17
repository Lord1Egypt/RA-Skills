# Watchpost skill

This folder is the source for the Watchpost skill on ClawHub. It contains the
skill instructions, a purchase-check helper, a review-status helper and their
shared HTTP transport. The helpers run on Node.js 20 or newer without installing
packages.

Read [SKILL.md](SKILL.md) for setup, input fields, exit codes and the review
workflow. OpenClaw expands `{baseDir}` in the instructions; other hosts should
resolve the scripts from this folder. The helpers submit
checks and read status from the official Watchpost API; they do not make payments
or approve reviews on the user's behalf.

## Local troubleshooting

Run an absolute path to `scripts/check-purchase.mjs` with `--help`, `--version`
or `--doctor`. These do not require a valid connection and make no network calls.
Doctor reports only runtime and token-format information, never the token itself.
A successful diagnostic does not prove the token is valid on the server.

If the skill is not available, check the runtime's skill status and configure
`WATCHPOST_TOKEN` through its secret settings. OpenClaw gates skill loading on
that variable. If execution is sandboxed, ensure the secret is available inside
the sandbox too. Refresh the skill list or start a new session after setup.

Use `--validate --file PATH` to check purchase input offline, then `--file PATH`
to submit the same file. JSON files support paths with spaces and UTF-8 text,
including a Windows UTF-8 BOM. Files are limited to 1,300,000 bytes. Keep them
free of tokens, cookies, payment credentials and unrelated account data.

Run the isolated regression tests from the repository root:

```bash
pnpm test:skill
```

Tests use mock HTTP responses and dummy credentials. They do not contact the
Watchpost API, create review notifications or consume the check allowance.
The repository's CI runs them through `pnpm test`.

Release metadata and registry publication are handled separately. Publish the
reviewed contents of this folder; do not include local tokens, test output or
registry-generated installation metadata.

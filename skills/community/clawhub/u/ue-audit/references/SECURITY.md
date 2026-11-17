# Security policy

## Supported versions

Security fixes are applied to the latest `0.4.x` release.

## Read-only design

`ue-audit` is an audit tool. It does not write project assets, does not save packages, and does not compile assets. The optional PIE smoke check is explicitly opt-in with `--pie` and stops PIE in a `finally` block.

`SAFE001` / `SAFE002` record what the tool observed; they are not a legal proof that no write occurred. See the "known limitations" section in `README.md`.

## Secrets

- Do not paste bridge tokens into issues, reports, or screenshots.
- The CLI never prints the token.
- The report does not include the token.
- Prefer `--token`, `UE_AUDIT_BRIDGE_TOKEN`, or `UE_AUDIT_BRIDGE_TOKEN_FILE` over hard-coding secrets.

## Reporting a vulnerability

Please use the repository's private security advisory feature. Include:

- affected version
- reproduction steps
- expected vs actual behavior
- whether the issue can write to a project or expose a token

Do not open a public issue for a token leak or a write-safety bypass.

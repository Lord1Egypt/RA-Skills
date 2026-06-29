# Cloudflare BIC Skip For api.sagerouter.dev

`api.sagerouter.dev` must let ordinary OpenAI-compatible SDKs and CLI clients
reach the Sage Router auth gate. If Cloudflare Browser Integrity Check returns
`403` / `1010` before Sage Router can return its guided `401`, create a
host-scoped Cloudflare configuration rule for the API host only.

## Required token

Create or rotate `CLOUDFLARE_API_TOKEN` with these permissions scoped to the
`sagerouter.dev` zone:

- `Zone:Zone:Read`
- `Zone Rulesets:Read`
- `Zone Rulesets:Edit`

Do not use this token as a Pages deploy token, customer API key, provider key,
or router backend token.

## Verify

```bash
bash scripts/configure_cloudflare_api_bic_skip.sh --check
```

If the token can read the zone but cannot read rulesets, the script reports the
Rulesets permission failure explicitly. Rotate the token instead of weakening
Cloudflare security globally.

If several local env backups may contain stale Cloudflare tokens, audit them
without printing token values:

```bash
bash scripts/configure_cloudflare_api_bic_skip.sh --audit-local-tokens
```

The audit prints candidate numbers, source variable names, zone-read status, and
ruleset-read status only, followed by a no-secret summary with
`usableRulesetTokenCandidates` and a `recommendedAction`. A launch-ready token
must show the zone as readable and the `http_config_settings` ruleset as
readable or creatable.

## Apply

```bash
bash scripts/configure_cloudflare_api_bic_skip.sh
```

The script creates or replaces a single zone configuration rule:

- host expression: `http.host eq "api.sagerouter.dev"`
- action: `set_config`
- setting: `bic: false`

It does not disable Browser Integrity Check for `sagerouter.dev`,
`www.sagerouter.dev`, `app.sagerouter.dev`, or other hosts.

## Confirm

```bash
bash scripts/check_sagerouter_launch_readiness.sh
```

The raw Python `urllib` probe should reach the Sage Router guided auth gate and
return `401` with account, pricing, status, OpenAI base URL, and `sk_sage_`
setup guidance.

If OpenAI-compatible SDK-style probes return the guided `401` but raw default
Python `urllib` still returns Cloudflare `403` / `1010`, launch readiness treats
that as an operator warning rather than a customer-impacting failure. Rotate the
Cloudflare token with the Rulesets permissions above so the script can verify
the host-scoped rule instead of guessing from live probes.

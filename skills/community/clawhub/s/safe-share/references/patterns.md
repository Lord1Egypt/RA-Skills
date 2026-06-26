# Detection Patterns

Use high-confidence deterministic rules first.

## Secret and Credential Patterns

- OpenAI API keys: `sk-...`
- GitHub personal tokens: `ghp_`, `github_pat_`, `gho_`, `ghu_`, `ghs_`, `ghr_`
- AWS access keys: `AKIA...`, `ASIA...`
- Bearer tokens in authorization headers
- Session cookies in `Cookie:` or `Set-Cookie:`
- `.env` assignments with key names containing:
  - `key`
  - `token`
  - `secret`
  - `password`
  - `passwd`
  - `session`
  - `cookie`
- Query parameters with sensitive names:
  - `token`
  - `key`
  - `apikey`
  - `api_key`
  - `secret`
  - `password`
  - `signature`
  - `session`
- PEM and private key blocks

## Identifier Patterns

- Email addresses
- Phone-number-like strings with 7 or more digits
- IPv4 addresses
- IPv6 addresses
- Bank-card-like strings that pass a Luhn check

## Confidence Rules

- Auto-replace only high-confidence matches.
- For weak patterns, require a sensitive label nearby.
- Prefer replacing an entire assignment or credential value instead of a partial fragment.
- Preserve enough syntax that the sanitized text still reads naturally.

## Review Guidance

Flag these for manual review rather than claiming certainty:

- Internal hostnames
- Customer IDs without a standard format
- Free-form text that may contain names or addresses
- Hashes or UUIDs with no surrounding sensitive context

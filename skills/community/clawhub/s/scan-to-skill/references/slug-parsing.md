# Slug Parsing Rules

Supported decoded QR payloads:

1. Plain slug
- `skill-feed`
- `scan-to-skill`

2. ClawHub URLs (allowed hosts only: `clawhub.ai`, `www.clawhub.ai`, `clawhub.com`, `www.clawhub.com`)
- `https://clawhub.ai/skill-feed`
- `https://clawhub.ai/owner/skill-feed`
- `https://www.clawhub.com/owner/skill-feed`
- URLs from any other domain are **rejected**

3. Install command text
- `clawhub install skill-feed`

Parsing precedence:

1. If text contains `clawhub install <slug>`, use `<slug>` (trusted).
2. Else if text is URL with an allowed ClawHub host, extract last path segment as slug (trusted).
3. Else if text is URL with a non-allowed host, **reject** (exit code 4).
4. Else if text matches slug pattern (`[a-z0-9][a-z0-9-]*`), use as slug (trusted).
5. Otherwise mark as unsupported and reject.

Validation:

- Lowercase only
- `a-z`, `0-9`, `-`
- Length 2-64

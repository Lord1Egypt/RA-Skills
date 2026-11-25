# 0.1.6

- Express the zero-dependency receipt helpers as conventional CommonJS with explicit async entry points for broader static-analysis compatibility.
- Preserve the CLI, security boundaries and all mocked network behaviour.

# 0.1.5

- Ship the ESM helpers as standard `.js` files with an explicit package module type so ClawHub static analysis can inspect the referenced source completely.
- Preserve command behaviour and the full mocked receipt test suite.

# 0.1.4

- Republish the reviewed receipt helpers through the current ClawHub scan pipeline.
- Document that host tool policy remains authoritative; the skill does not preapprove network or environment access.

# 0.1.3

- Require API-backed post identity, canonical URL matching and origin-bound no-redirect receipt requests.
- Require explicit publish/draft status; report draft creation separately from publication.
- Fix duplicate-skip receipts incorrectly reporting ok on failed public checks.

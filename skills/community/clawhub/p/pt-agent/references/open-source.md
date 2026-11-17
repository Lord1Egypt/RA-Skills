# Open Source Reference

Use this reference when preparing code, docs, tests, fixtures, examples, or contribution patterns for an open-source PT automation project.

## Repository Standards

- Include a clear license before publishing. If the user has no preference, ask before choosing one.
- Keep runtime secrets outside version control and document environment variable names without example real values.
- Commit only sanitized fixtures. Remove usernames, passkeys, auth tokens, invite codes, messages, exact private download URLs, and torrent hashes when they identify private activity.
- Keep site-specific adapters modular so maintainers can remove or disable problematic adapters without changing core services.
- Avoid hard-coded assumptions about a specific private tracker in shared code.

## Configuration Standards

- Provide example config with fake domains such as `https://tracker.example`.
- Use `credentialRef`, `profileRef`, and `proxyRef` fields instead of inline credentials.
- Validate config schema at boundaries and return actionable errors.
- Support import/export only for non-secret config unless the user explicitly chooses a secure local backup format.

## Adapter Contribution Standards

Adapter PRs should include:

- Adapter metadata with capabilities, auth mode, category map, and rate limit.
- Sanitized search fixture covering at least one result.
- Sanitized empty or login-required fixture.
- Parser tests for size, seeders/leechers, publish time, discount state, detail URL, and download reference.
- Notes for unsupported fields or known theme variants.

Do not require maintainers to have access to a private site to run unit tests.

## Downloader Contribution Standards

Downloader provider PRs should include:

- Mocked API tests for health check, status, add success, auth failure, and duplicate/error responses.
- Version/feature detection when the client has incompatible behavior across versions.
- Redaction tests for URLs, tokens, usernames, and file paths when they may expose private data.

## Validation Baseline

Before presenting a change as complete, run the repository's available formatter, linter, typecheck, and unit tests. For this skill, always run `python3 "$SKILL_ROOT/scripts/validate_skill.py"`; it validates metadata, reference links, catalogs, script syntax, storage policy, and generated-file residue without external dependencies.

For PT-specific changes, also verify:

- Logs and run history redact secrets and private URLs.
- Failed tracker searches do not stop unrelated trackers.
- Temporary torrent files are deleted or never written.
- Downloader status handles unauthorized and unreachable states distinctly.

## Issue And Log Hygiene

- Encourage users to share sanitized HTML snippets, not full pages.
- Provide redaction examples for query params such as `passkey`, `auth`, `token`, `rsskey`, `uid`, and `download`.
- Avoid asking users to paste cookies or browser local storage into issues.
- When debugging selector drift, ask for a minimal DOM fragment around the failing table/card.

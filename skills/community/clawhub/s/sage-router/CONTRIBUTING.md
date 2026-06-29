# Contributing to Sage Router

Thanks for your interest in Sage Router. This project is local-first,
open-source routing infrastructure for AI agents. The compliance boundary
matters: Sage Router never resells model access, pools accounts, shares
subscriptions, or bypasses provider Terms of Service. Contributions must keep
that boundary intact.

## Before you start

- Open an issue first for non-trivial changes so we can align on approach.
- Keep provider credentials out of issues, PRs, commits, and logs. Never paste
  API keys, OAuth tokens, or auth JSON into a contribution.

## Compliance rules for contributions

- No resale, pooling, account-sharing, or ToS-bypassing behavior.
- Default architecture must keep customer provider credentials local. Any
  hosted feature that handles secrets must be opt-in and encrypted at rest.
- New providers must be BYOK/BYOS: the customer supplies authorized access.
- No code that harvests or exfiltrates customer provider keys.

## Development setup

```bash
git clone https://github.com/earlvanze/sage-router.git
cd sage-router
cp .env.example .env      # edit with your own keys (optional for local-only)
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python3 router.py --port 8790
```

Run tests:

```bash
python3 -m pytest -q
```

Point a tool at the local endpoint to smoke-test:

```bash
export OPENAI_BASE_URL=http://localhost:8790/v1
export OPENAI_API_KEY=local-router
```

## Pull request checklist

- Branch from `master` (or the relevant feature branch) and keep PRs focused.
- Add or update tests for behavior changes.
- Update docs (`README.md`, `docs/`, `SKILL.md`) when the public surface changes.
- Keep provider keys out of diffs. Use `.env` (gitignored) for local secrets.
- Document routing, failover, and security implications in the PR description.

## Code style

- Match the surrounding style. Minimal, focused diffs.
- Prefer narrow edits over rewrites.
- No inline secrets, no hardcoded customer credentials.

## Releases

Releases are tagged by maintainers. Do not bump published version metadata in a
feature PR unless asked.

## Licensing

By contributing you agree your contributions are licensed under the project's
MIT license (see `LICENSE`).

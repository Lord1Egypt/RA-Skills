# Contributing

## Development setup

```bash
git clone https://github.com/sprintberlin/openclaw-secret-drop.git
cd openclaw-secret-drop
python3 -m venv .venv
. .venv/bin/activate
pip install -e .
python -m unittest discover -v
```

## Rules for security-sensitive changes

1. Never use real credentials in tests, fixtures, issues, commits, or screenshots.
2. Never print provider payloads, subprocess stdout, URL fragments, passphrases, or secret values.
3. Treat all provider responses and URLs as untrusted input.
4. Add tests that prove the plaintext does not appear in stdout or stderr.
5. Keep destination writes atomic and mode `0600`.
6. Preserve HTTPS-only and private-network rejection unless the operator explicitly opts into a private self-hosted provider.
7. Document provider trust accurately. Do not call server-side encryption zero-knowledge.

## Pull requests

Run before opening a pull request:

```bash
python -m unittest discover -v
python -m compileall -q secret_drop tests
python scripts/secret-drop providers --json
```

Describe the threat model changed by the pull request and include synthetic proof for any new provider adapter.

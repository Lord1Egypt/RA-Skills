# Security Policy

## Reporting a vulnerability

If you find a security issue in this repo, please **don't open a public issue**. Instead:

1. Go to the repo's **Security** tab → **Advisories** → **Report a vulnerability**.
2. Describe what you found, including reproduction steps and the scripts/files affected.
3. I'll acknowledge within a few days and work with you on a fix.

You can also reach me via GitHub for an initial private contact if the advisory form isn't an option.

## Scope

This is a small Node.js skill with no network calls and no runtime dependencies. The most plausible security concerns are:

- **Path traversal** through `--entries-file`, `--memory-path`, or `--pending-file` arguments — the scripts pass them through `path.resolve(cwd, ...)` so an absolute or `..`-laden path can write outside the expected directory. The scripts are meant to be invoked by a trusted agent runtime, but if you have a scenario where untrusted input reaches these flags, please report it.
- **Prototype pollution** via the entries JSON. The scripts parse JSON with `JSON.parse` and access only specific known fields, but reports of unexpected behavior with crafted inputs are welcome.
- **ReDoS** in the regex helpers (`normalizeText`, `parseExistingSections`, `MERGE_MARKER_RE`). The patterns are intentionally simple, but if you find a worst-case input that hangs the script, please report it.

## Out of scope

- Misuse by a malicious OpenClaw agent or Telegram bot operator — the skill trusts its host environment by design.
- Issues in dependencies — there are none.
- Findings that require local filesystem access on the user's machine.

## Disclosure

I aim to release a fix or a documented mitigation within 30 days of confirming a report. Coordinated disclosure is appreciated; I'll credit reporters in the CHANGELOG unless they prefer to stay anonymous.

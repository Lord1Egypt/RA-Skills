# P04 Market search brief (recruiting)

## Objective

Turn the JD into **search queries** and a **shortlist** of third-party skills to vet and install, without executing unsafe commands.

## Inputs

- `jd`: P01 JSON.
- `host`: `claude-code` \| `cursor` \| `openclaw` (affects install instructions).
- `denylist`: URLs or publishers to avoid (if user provided).

## Procedure

1. Build **query_family** (5–12 queries): keywords, task type, file formats, stack names.
2. Add **site-scoped** variants where appropriate (e.g. `site:github.com` skill SKILL.md agent).
3. For each promising result, extract **trust_signals**: stars, maintainer, last commit, LICENSE, scope of file access, use of `curl|sh`.
4. Produce **install_command_template** placeholders—**not** executed until user confirms after vetting (see `references/04-market-recruitment.md`).
   - When `host` is **`openclaw`**, align with `references/hosts/openclaw.md`: prefer documented flows such as **`openclaw skills install …`** / ClawHub when applicable; otherwise templates like *copy skill folder into `~/.openclaw/skills/<name>/` or `<workspace>/skills/<name>/`* plus **`openclaw skills list`** / new session or **`openclaw gateway restart`** to verify—never run unvetted shell from the network without user OK.
5. Attach **vetting_checklist** booleans to each candidate.

## Output schema (JSON)

```json
{
  "query_family": ["string"],
  "shortlist": [
    {
      "name": "string",
      "source_url": "string",
      "trust_signals": ["string"],
      "risk_flags": ["string"],
      "install_command_template": "string",
      "vetting_checklist": {
        "license_present": true,
        "no_arbitrary_network": true,
        "no_credential_exfil": true,
        "scoped_file_access": true
      },
      "fit_summary": "string"
    }
  ],
  "recommended": "string",
  "recruitment_notes": "string"
}
```

## Quality gates

- At least **3** distinct queries before giving up on search.
- Any candidate with **critical vetting failures** must not be `recommended`.

## Failure modes

- **Typosquatting** — Compare publisher, repo name, and description to JD; flag near-duplicates.
- **Stale skill** — If SKILL.md references dead APIs, flag `risk_flags: obsolete_api`.

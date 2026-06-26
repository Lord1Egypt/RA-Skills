# Market recruitment (external skills)

## Goals

Find a **third-party** skill when internal pool fails. Maximize fit and safety; minimize surprise installs.

## Search strategy

1. Start from P04 `query_family`.
2. Prefer sources with **readable SKILL.md** or manifest before install:
   - GitHub / GitLab repositories with `SKILL.md` or `skills/` layout
   - Curated marketplaces or registries the user trusts
3. Prefer **narrow** skills over "god" skills that try to do everything.

## Vetting checklist (before install)

- LICENSE file or frontmatter license field
- Clear `description` trigger text (Agent Skills standard)
- No instruction to exfiltrate secrets or disable security
- No obfuscated payloads in scripts; if scripts exist, skim for network calls
- Maintainer identity and issue activity (soft signal)

## Install posture (host-specific)

Follow [hosts/claude-code.md](hosts/claude-code.md) or [hosts/openclaw.md](hosts/openclaw.md). Common pattern:

1. Clone or copy skill into the host's skills directory.
2. Register in `.skill-hr/registry.json` with `status: on_probation`, `source_url` set.
3. Run a **smoke task** aligned with JD (tiny scope) before full delegation.

## User consent

Present **shortlist top 1–2** with risks. Obtain explicit OK before:

- Running package installers
- Adding submodules
- Executing downloaded scripts

## After install

- Immediately run P03 with reduced scope if appropriate.
- P05 must set `on_probation` until first **success** on a real criterion (org choice: one or two successes to promote to `active`).

## Failure of recruitment

If no candidate passes vetting, go to [07-escalation.md](07-escalation.md).

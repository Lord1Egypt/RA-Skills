# Escalation when no skill fits

## Triggers

- P02 best score &lt; `confirm_band_min` **and** P04 shortlist empty or all vetoed.
- Repeated `environment` blockers outside skill control (missing org credentials).
- User rejects all shortlisted external candidates.
- Task requires **human-only** judgment (legal, medical, irreversible production changes).

## Escalation paths (pick explicit branch)

1. **Clarify with user** — Reduce JD scope; split into S-tier tasks; obtain missing access.
2. **Generalist execution** — User accepts risk: proceed without a domain skill, document limitations in incident (`selected_skill_id: none`).
3. **Build internal skill** — Use `skill-creator` pattern: author a minimal SKILL.md in-repo under `.cursor/skills` or host-global path, register as `on_probation`.
4. **Defer** — Park task; write incident with `outcome: deferred` and blockers.

## Minimum artifact

Even when escalating, create an incident stub capturing:

- JD summary
- Why internal and external pools failed
- Exact questions for the user

## No silent failure

Never end with "cannot help" without **one** concrete next step (question, command, or doc link).

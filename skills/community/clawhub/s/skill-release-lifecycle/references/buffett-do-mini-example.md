# Mini Example: buffett-do

This mini example shows how the Skill Release Lifecycle would evaluate smaller feedback around `buffett-do`.

## Context

`buffett-do` is a public-facing skill derived from the older `wbwd-research-priority` direction. The main lifecycle issues were not deep execution bugs; they were release-shape issues:

- feedback placement
- activation clarity
- install command clarity
- avoiding harsh user-facing wording
- explicit anti-scope

---

## Feedback Items

| Feedback | Category | Action |
|---|---|---|
| Public page needed a clear feedback path | Missing feedback path / Maintenance | Docs-only patch or patch version bump |
| Activation needed to be clear and user-facing | Confusing activation | Minor wording patch; version bump only if routing changes |
| Install command needed to be explicit | Missing install path | Docs-only patch |
| User-facing wording was too harsh / off-tone | UX wording issue | Minor wording patch |
| Skill needed to clarify what it does not do | Missing anti-scope | HARD gate fix before public release or re-release |

---

## Gate Implications

### Identity

If `buffett-do` lacks an explicit anti-scope section, Identity Gate = FAIL.

Acceptable anti-scope examples:

- This skill does not make final investment decisions.
- This skill does not provide personalized financial advice.
- This skill does not replace source verification.
- This skill does not rank every possible idea; it prioritizes whether an idea is worth deeper research.

### UX

Activation should be concrete:

Good:
- “Use buffett-do to decide whether this idea deserves research time.”
- “Run Buffett-style prioritization on this opportunity.”

Weak:
- “Help me think about investing.”
- “Be Warren Buffett.”

### Maintenance

Feedback path should be visible but not dominate the page.

Good:
- a short Feedback section near the end
- one clear channel
- no multiple competing feedback paths

---

## Lifecycle Decision

If these issues are present but the skill already has utility, identity, and safety mostly intact:

- Missing anti-scope → fix before release / re-release
- Install clarity → docs-only patch
- Feedback path → docs-only patch
- Harsh wording → minor wording patch
- Activation change → minor bump only if routing changes

Do not rewrite the entire skill unless the positioning itself is wrong.

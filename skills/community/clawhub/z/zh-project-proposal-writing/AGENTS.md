# Agent instructions for maintaining this Skill

Use `SKILL.md` as the canonical instruction file for the project-application writing and delivery skill. Keep the main file concise and place detailed, task-specific guidance in `references/` or `examples/`.

## Maintenance rules

- Do not hard-code annual grant rules, deadlines, budgets, eligibility requirements, page limits, attachment formats, or submission-system details into `SKILL.md`; keep them as items requiring official verification.
- Preserve the source hierarchy: user-uploaded current guide/template > funder official rules > official review/writing guidance > university or research-institute expert lecture notes > peer-reviewed grant-writing articles > low-weight blogs or commercial training materials.
- When adding expert insights, classify them by writing problem, not by celebrity authority. Do not store specific person names or raw URLs anywhere in the Skill. Required categories include reviewer communication, project type fit, scientific question or technical bottleneck, abstract/storyline, innovation, feasibility, team/environment, impact/metrics, compliance, and revision workflow.
- Keep file paths ASCII where possible for portability across shell/container environments.
- When adding examples, use fictional placeholders and avoid copying unpublished proposal text or real confidential applications.
- Preserve the no-fabrication rule for papers, patents, data, ethics approvals, collaborations, budgets, reviewer comments, user scenarios, third-party tests, and institutional commitments.
- Deliverable-mode outputs must be packaged as a Word `.docx` document and include at least: proposal draft, constraints matrix, fact ledger or missing-facts list, chapter mapping matrix, compliance/attachment checklist, red-team review, and final verification list.
- If a user asks for a polished "final" version while facts are incomplete, continue drafting with clearly marked placeholders such as `待补充` and `需申请人核验`; do not fill gaps with invented facts.
- Do not store external raw URLs or specific person names in any Skill file. Use source tiers and generic source categories instead.
- After edits, check that `SKILL.md` still has YAML front matter with `name` and `description`, and that all referenced files exist.

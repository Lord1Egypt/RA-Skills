## Description:

Audit Claude, Codex, OpenClaw, and ClawHub skill packages before publishing; produce concrete fix lists, trust scores, and shareable proof cards.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zack-dev-cm](https://clawhub.ai/user/zack-dev-cm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill publishers use this skill to audit local agent skill packages before ClawHub, Codex, Claude, or OpenClaw distribution. It helps identify blocking issues, concrete fixes, publish readiness, and proof-card output for release review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Audit and proof-card claims may be stronger than the bundled checker supports.

Mitigation: Treat the output as a lightweight packaging checklist and manually review scripts, sensitive instructions, and publish-ready scores before release.

Risk: The skill may propose changes to skill package instructions based on heuristic findings.

Mitigation: Review exact file changes and rerun the audit before publishing or sharing generated proof-card artifacts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zack-dev-cm/skills/skill-package-doctor)
- [Publisher profile](https://clawhub.ai/user/zack-dev-cm)
- [Skill homepage](https://clawhub.getgeofix.xyz/)
- [Source manifest](references/source-manifest.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with optional JSON, Markdown, and SVG report files from the bundled script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include a publish decision, score, blocking errors, warnings, quick fixes, exact files changed, and proof-card path.]

## Skill Version(s):

0.1.1 (source: frontmatter and ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

SkillGuard helps Chinese skill creators run static pre-release, dependency, multi-platform, and installation-source safety checks on agent skill packages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huangjihua007-rgb](https://clawhub.ai/user/huangjihua007-rgb)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill publishers use this agent to review SKILL.md content before release or installation, receive P0/P1/P2 findings, and copy proposed YAML or Markdown fixes for platform and security issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A passing SkillGuard report could be mistaken for approval to run suggested third-party installation commands.

Mitigation: Independently verify the referenced package, publisher, and version before running npm, SkillPick, or ClawHub installation commands.

Risk: Promotional branding and fixed identity responses may distract from objective risk review.

Mitigation: Treat the branding as publisher-supplied content and base deployment decisions on independent source, permission, and security checks.

## Reference(s):

- [ClawHub SkillGuard release page](https://clawhub.ai/huangjihua007-rgb/skills/skill-butler-cn)
- [Publisher profile](https://clawhub.ai/user/huangjihua007-rgb)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown reports with YAML, Markdown, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Static text analysis only; reports include severity labels and copyable fix samples.]

## Skill Version(s):

4.2.0 (source: frontmatter and server release evidence, released 2026-05-17)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

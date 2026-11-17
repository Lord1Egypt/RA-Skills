## Description:

Generic publishing tool for Claude Code skills that validates, packages, and publishes to ClawHub, Hermes Agent, and anthropics/skills with bilingual README support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhangyanbo2007](https://clawhub.ai/user/zhangyanbo2007)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill maintainers use this skill to validate Claude Code skill metadata, generate publish packages, and publish or prepare submissions for ClawHub, Hermes Agent, and anthropics/skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to automatically read local credentials and source a user .env file before network and publishing actions.

Mitigation: Use only with explicit approval for each token, selected target, proxy, git push, pull request, and ClawHub publish action; avoid following the ~/.env sourcing instruction.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhangyanbo2007/skills/skill-publisher-universal)
- [Artifact SKILL.md](artifact/SKILL.md)
- [Artifact README.md](artifact/README.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with shell commands, generated README content, package files, and publishing instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces publishing packages for selected marketplaces and may prepare validation or submission commands.]

## Skill Version(s):

1.1.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

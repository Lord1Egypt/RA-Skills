## Description:

A framework for creating reusable AI agent skills with a starter template and seven bundled skills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vexify-build](https://clawhub.ai/user/vexify-build)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users can create reusable skills from the template or use the bundled skills for project documentation, commits, dependencies, repository statistics, reminders, emoji lookup, and web search.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad skill triggers may activate workflows unexpectedly.

Mitigation: Review and narrow triggers before enabling the bundle.

Risk: Web searches and GitHub API lookups can initiate network requests.

Mitigation: Require explicit user confirmation before each lookup.

Risk: Dependency updates, reading staged diffs, and recurring reminders can affect project state or expose sensitive content.

Mitigation: Get explicit confirmation before updates, diff access, or recurring reminders; review intended scope first.

Risk: Malformed package.json may disrupt automated installation.

Mitigation: Correct the package file before relying on automated installation tooling.

## Reference(s):

- [VBot Skills Framework release](https://clawhub.ai/vexify-build/skills/vbot-skills-framework)
- [Framework README](README.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown, text, and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs depend on the selected bundled skill.]

## Skill Version(s):

1.1.0 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

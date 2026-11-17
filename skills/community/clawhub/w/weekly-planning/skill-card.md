## Description:

Creates a weekly go-to-market plan by comparing recent activity with initiatives and live workspace data, then opens reviewable pull requests with recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cargo-ai](https://clawhub.ai/user/cargo-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Go-to-market leaders and revenue operations teams use this skill to review last week's activity against active initiatives and decide what to work on next. It produces human-reviewable weekly recommendations as pull requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package install target is unpinned, and tool limits are not enforceable.

Mitigation: Pin the CLI version and review the agent's allowed commands, repository access, and network access before enabling scheduled runs.

Risk: Some artifact components were only partially analyzed.

Mitigation: Complete a security review of the bundled files before installing or running the skill.

## Reference(s):

- [ClawHub release](https://clawhub.ai/cargo-ai/skills/weekly-planning)
- [Cargo GTM skills repository](https://github.com/getcargohq/gtm-skills)
- [Recommendation file format](artifact/references/recommendations.md)

## Skill Output:

**Output Type(s):** [Markdown, Guidance]

**Output Format:** [Markdown planning files and pull request recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [A weekly plan for each active initiative, or one workspace plan when no initiatives are active; human review and merge are required.]

## Skill Version(s):

0.2.0 (source: release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

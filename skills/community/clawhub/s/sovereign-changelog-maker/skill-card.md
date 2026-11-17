## Description:

Generates structured changelogs from git history in Keep a Changelog format with PR and issue links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ryudi84](https://clawhub.ai/user/ryudi84)

### License/Terms of Use:


## Use Case:

Developers and release managers use this skill to draft concise, user-facing changelogs from repository history, grouped into standard Keep a Changelog categories with migration notes when changes are breaking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may prompt an agent to inspect repository history and link pull requests or issues, which can expose repository context during changelog-writing workflows.

Mitigation: Use it only in repositories where commit history, PR metadata, and issue references are appropriate for the agent to process.

## Reference(s):

- [Keep a Changelog](https://keepachangelog.com)
- [ClawHub skill page](https://clawhub.ai/ryudi84/skills/sovereign-changelog-maker)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Structured changelog sections, PR and issue links, migration notes, and semantic versioning cues.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

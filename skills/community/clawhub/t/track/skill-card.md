## Description:

Track helps agents log habit completions and maintain local progress records for personal accountability.

This skill is ready for commercial/non-commercial use.

## Publisher:

[projectsnowwork](https://clawhub.ai/user/projectsnowwork)

### License/Terms of Use:

MIT-0

## Use Case:

External users and their agents use this skill to record habit completions and keep local progress history. The included implementation writes habit entries to a local tracking file for later review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill records personal habit data in persistent local files.

Mitigation: Ask for clear user confirmation before logging habits or goals, and remind users that they control local retention and deletion.

Risk: The skill description advertises goal, trend, streak, and export workflows that are not fully included in the package.

Mitigation: Limit agent behavior to supported artifact capabilities unless additional scripts or references are supplied.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/projectsnowwork/skills/track)
- [Publisher profile](https://clawhub.ai/user/projectsnowwork)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Files, Guidance]

**Output Format:** [Markdown with inline shell commands and local JSON file updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates persistent local habit records under the agent workspace memory path.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

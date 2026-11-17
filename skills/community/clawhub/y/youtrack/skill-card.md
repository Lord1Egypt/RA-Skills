## Description:

Manage YouTrack issues, projects, and workflows via CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iahmadzain](https://clawhub.ai/user/iahmadzain)

### License/Terms of Use:


## Use Case:

Developers and project teams use this skill to manage YouTrack issues from an agent workflow, including listing projects, searching issues, creating and updating issues, adding comments, reviewing workflow states, and producing project or user reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on a local YouTrack API token that can expose or modify issue data if over-privileged or mishandled.

Mitigation: Use a least-privilege YouTrack token, store it carefully, and avoid exposing token values in prompts, logs, or shared output.

Risk: Bulk update, comment, and assignment commands can change many YouTrack issues at once.

Mitigation: Run bulk commands with narrow queries and use --dry-run first to preview affected issues before applying changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/iahmadzain/skills/youtrack)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct agents to produce YouTrack CLI commands and request table or raw JSON output from ytctl.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

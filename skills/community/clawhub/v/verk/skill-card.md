## Description:

Manage tasks, projects, and workflows in Verk, including creating, updating, assigning, tracking, commenting on, and listing automation flows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abhibavishi](https://clawhub.ai/user/abhibavishi)

### License/Terms of Use:

MIT

## Use Case:

OpenClaw users use this skill to manage Verk tasks, projects, and automation workflows from natural-language requests through a Node.js CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a powerful Verk API key for live task-management actions.

Mitigation: Use a least-privilege Verk API key and review the requested action before allowing it to run.

Risk: The API endpoint can be changed with VERK_API_URL.

Mitigation: Set VERK_API_URL only to a trusted HTTPS Verk endpoint, or leave it unset to use the default endpoint.

Risk: Create, update, comment, and delete commands can modify live Verk data.

Mitigation: Require explicit user confirmation before running write or delete actions.

## Reference(s):

- [Verk website](https://verkapp.com)
- [ClawHub skill page](https://clawhub.ai/abhibavishi/skills/verk)
- [Publisher profile](https://clawhub.ai/user/abhibavishi)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js, VERK_API_KEY, and VERK_ORG_ID. Commands call the Verk API and return JSON for the agent to summarize.]

## Skill Version(s):

1.1.0 (source: ClawHub release metadata; package.json lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

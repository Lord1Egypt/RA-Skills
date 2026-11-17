## Description:

Helps agents manage Vikunja projects, tasks, labels, comments, assignees, searches, filters, and completion status through Vikunja REST API v1 using curl and a bearer token.

This skill is ready for commercial/non-commercial use.

## Publisher:

[axelhu](https://clawhub.ai/user/axelhu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to operate a Vikunja task-management instance through REST API calls, including creating and updating projects, tasks, labels, comments, and assignees. It is useful when an agent needs task-management guidance with token-based authentication and curl examples.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide delete operations and assignment changes with broad Vikunja account authority.

Mitigation: Use a least-privileged token and require explicit user confirmation before any delete or account-impacting operation.

Risk: Long-lived bearer tokens may be stored locally or exposed in command output.

Mitigation: Prefer runtime environment injection or a chmod 600 token file, avoid printing token values, and rotate the token if exposure is suspected.

Risk: API calls target a local Vikunja endpoint that may not be protected in every deployment.

Mitigation: Use HTTPS or another trusted local endpoint before allowing the agent to perform authenticated operations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/axelhu/skills/vikunja-usage)
- [Publisher profile](https://clawhub.ai/user/axelhu)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with curl commands, token setup guidance, and Python code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and a Vikunja bearer token supplied through VIKUNJA_TOKEN or an agent-local token file.]

## Skill Version(s):

1.0.2 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

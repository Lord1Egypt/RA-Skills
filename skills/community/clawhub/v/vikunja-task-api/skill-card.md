## Description:

Provides Vikunja v2 API guidance and helper commands for managing projects, tasks, labels, teams, views, comments, attachments, and bulk operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ashanzzz](https://clawhub.ai/user/ashanzzz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to connect an agent to a Vikunja instance and perform task-management workflows through authenticated API calls and a shell helper.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence flags unsafe helper installation guidance that downloads a script directly into /usr/local/bin.

Mitigation: Install through a trusted package or pinned release, and verify the script before making it executable.

Risk: The artifact includes credential setup examples that can place tokens in shell startup files.

Mitigation: Store Vikunja tokens in a secret manager or a tightly permissioned environment file, and avoid writing long-lived credentials to ~/.bashrc.

Risk: The skill covers destructive and permission-changing API operations, including deletes, bulk updates, sharing, team membership, and attachment changes.

Mitigation: Require explicit user confirmation before executing destructive, bulk, sharing, team/member, or attachment operations.

Risk: Authenticated API calls can expose tokens or task data if sent over insecure transport.

Mitigation: Use HTTPS-only Vikunja endpoints for non-local deployments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ashanzzz/skills/vikunja-task-api)
- [Vikunja](https://vikunja.io/)
- [Vikunja download](https://vikunja.io/download)
- [Vikunja filters documentation](https://vikunja.io/docs/filters/)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Code]

**Output Format:** [Markdown with inline bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Vikunja base URL and either an API token or username/password credentials; commands may return JSON formatted with jq.]

## Skill Version(s):

2.5.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

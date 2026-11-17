## Description:

Manage enterprise SSO, Directory Sync (SCIM), Admin Portal, and user management via WorkOS API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dwhite-oss](https://clawhub.ai/user/dwhite-oss)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and administrators use this skill to generate WorkOS API guidance and curl commands for enterprise SSO, Directory Sync, Admin Portal links, and AuthKit user-management tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated commands may perform high-impact WorkOS tenant or account administration actions.

Mitigation: Require explicit human confirmation before creating organizations, generating Admin Portal links, exchanging auth codes, or deleting users.

Risk: Using broad or production WorkOS credentials can increase the blast radius of mistakes.

Mitigation: Use a least-privilege WorkOS API key where possible and avoid production keys for exploration.

## Reference(s):

- [WorkOS API base](https://api.workos.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks and curl examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a WORKOS_API_KEY environment variable for generated API calls.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

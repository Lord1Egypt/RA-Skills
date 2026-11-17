## Description:

Submit learning insights to an organization's shared Feishu learning circle via a token-authenticated API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qyc314159](https://clawhub.ai/user/qyc314159)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to turn learning insights into structured notes and publish them to a configured organization learning-circle server. It supports submission and server status checks through the included Node.js script.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish learning notes to a configured server using a bearer token.

Mitigation: Require explicit user approval before each submission unless the user has made a clear publish request.

Risk: Submissions may be visible to the organization learning circle.

Mitigation: Do not submit secrets, customer data, private reflections, internal debugging details, or other sensitive material.

Risk: The configured endpoint may not enforce HTTPS.

Mitigation: Use an HTTPS API endpoint and protect the local token configuration file.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qyc314159/skills/thu-epiphany-client)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, API calls, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API submissions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Submissions include title, thoughts, optional URL, and optional source display name.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

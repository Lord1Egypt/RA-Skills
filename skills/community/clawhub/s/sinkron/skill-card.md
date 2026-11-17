## Description:

Provide AI agents with permanent email identities using Sinkron CLI and Python SDK.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zororaka00](https://clawhub.ai/user/zororaka00)

### License/Terms of Use:


## Use Case:

Developers and automation engineers use this skill to give agents a persistent Sinkron email identity, inspect inboxes, search and retrieve messages, and manage messages through the Sinkron CLI or Python SDK.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on an external Sinkron package and service, and package provenance was not server-resolved for this release.

Mitigation: Confirm the Sinkron package provenance before installation and test first in an isolated environment.

Risk: SINKRON_TOKEN is a required credential for authenticated inbox operations.

Mitigation: Store SINKRON_TOKEN in a secret manager or restricted environment variable, avoid logging tokens or message contents, and rotate the token after suspected exposure.

Risk: The skill documents commands that can delete messages or clear an inbox.

Mitigation: Require explicit human confirmation before running delete-messages or delete-inbox, especially when --force is present.

## Reference(s):

- [Sinkron homepage](https://www.sinkron.id)
- [ClawHub skill listing](https://clawhub.ai/zororaka00/skills/sinkron)
- [Sinkron PyPI package](https://pypi.org/project/sinkron/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline bash and Python snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SINKRON_TOKEN for authenticated Sinkron operations and recommends pinned package installation.]

## Skill Version(s):

1.0.7 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

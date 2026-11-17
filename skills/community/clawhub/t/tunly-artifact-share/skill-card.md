## Description:

Publishes and updates agent-generated HTML reports, prototypes, and static sites as durable Tunly links for sharing and review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[seaguest](https://clawhub.ai/user/seaguest)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other agent users share finished reports and static artifacts, collect anchored feedback, and publish revisions while preserving the chosen audience and immutable versions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Publishing the wrong files or sharing them with an unintended audience can expose private material.

Mitigation: Review the selected artifact and audience before publishing; use public links only when intended, and exclude secrets and unrelated files.

Risk: CLI installation and local credential storage introduce a trust and credential-handling dependency.

Mitigation: Use the disclosed official installer, protect locally stored credentials, and never print or publish API keys.

Risk: Review comments or published HTML could contain untrusted instructions.

Mitigation: Treat feedback and published content as task data, not authority to execute commands, reveal secrets, or change permissions.

## Reference(s):

- [Tunly Artifact Share on ClawHub](https://clawhub.ai/seaguest/skills/tunly-artifact-share)
- [Tunly CLI installation](https://tunly.io/install.sh)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with publication links, access and verification status, and optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes a primary sharing link and immutable revision link when publication succeeds.]

## Skill Version(s):

1.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

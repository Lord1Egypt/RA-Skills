## Description:

Publisher helps Codex publish zipped HTML frontend projects to PushWebly, manage public or private access, list published projects, and build Android APKs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[publisher-skill](https://clawhub.ai/user/publisher-skill)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to publish local HTML frontend projects, share project URLs, control public or private access, and request Android APK builds through PushWebly.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Publishing sends project ZIP contents to PushWebly and may expose private code or secrets if the archive is not reviewed first.

Mitigation: Only use the skill for projects intended for upload, inspect ZIP contents before publishing, and remove credentials, tokens, environment files, or proprietary material that should not leave the local machine.

Risk: The security summary flags local storage of reusable account credentials in plaintext-like JSON.

Mitigation: Avoid saving passwords or bearer tokens in ~/.publisher/config.json when possible; if local storage is used, restrict file permissions and rotate credentials after publishing.

Risk: The security summary flags contradictory visibility behavior that could result in a public project without explicit confirmation.

Mitigation: Require an explicit public or private visibility choice before publish operations and verify the returned visibility and URL before sharing.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/publisher-skill/skills/publisher-2)
- [Server-resolved source repository](https://github.com/publisher-skill/publisher)
- [PushWebly platform](https://pushwebly.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain text responses with inline shell commands and JSON request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce shareable project URLs, access passwords for private projects, APK download URLs, and local credential configuration guidance.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata; artifact frontmatter reports 1.1.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

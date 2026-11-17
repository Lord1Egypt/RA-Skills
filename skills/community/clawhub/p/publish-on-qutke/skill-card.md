## Description:

Publishes files or folders as static web content on on.qutke.cn and returns a public {slug}.on.qutke.cn URL.

This skill is ready for commercial/non-commercial use.

## Publisher:

[haio](https://clawhub.ai/user/haio)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to publish static sites, folders, and individual files to a hosted Qutke URL for sharing or deployment. It supports anonymous temporary publishing and authenticated account-owned publishing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can upload broad local directories to a public hosting service.

Mitigation: Publish only a clean export directory and check for secrets, hidden files, credentials, and unintended private content before running the publish command.

Risk: The skill can handle on.qutke.cn account credentials and API keys.

Mitigation: Avoid agent-mediated email-code login when possible; store API keys directly in the recommended credentials file or environment variable and revoke keys yourself when needed.

Risk: Anonymous publish claim tokens and claim URLs are sensitive and are only returned once.

Mitigation: Treat claim URLs and tokens as secrets, share only the current script output with the user, and do not rely on .onqutke/state.json as the source of public user guidance.

Risk: Authenticated operations can delete or change sites, domains, handles, and links.

Mitigation: Require explicit user confirmation before destructive or account-level changes such as deleting sites, domains, handles, or links.

## Reference(s):

- [on.qutke.cn API Reference](references/REFERENCE.md)
- [on.qutke.cn](https://on.qutke.cn)
- [ClawHub skill page](https://clawhub.ai/haio/skills/publish-on-qutke)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and returned hosted URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns a public site URL; anonymous publishes expire after 24 hours, while authenticated publishes are saved to the user's account.]

## Skill Version(s):

1.0.3 (source: server release metadata; artifact body lists Skill version 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

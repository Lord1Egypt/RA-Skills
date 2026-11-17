## Description:

Post tweets, replies, and quotes to X/Twitter using the official API v2.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xmythril](https://clawhub.ai/user/0xmythril)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to configure and operate tweet-cli for posting, replying to, quoting, and deleting X/Twitter posts through the official API v2 when explicitly requested or scheduled.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs and relies on a global third-party CLI with access to persistent X API credentials.

Mitigation: Install only after auditing the resolved source, prefer immutable pinning, and use narrowly scoped, revocable X credentials.

Risk: Commands can post, reply, quote, or delete X/Twitter content and may consume API credits.

Mitigation: Confirm manually before any post, reply, quote, or delete action and use the tool only when explicitly requested or scheduled.

Risk: Credential files stored on disk could expose X account write access if readable by other users or processes.

Mitigation: Store credentials in the documented config file with restricted file permissions such as chmod 600 and rotate credentials if exposure is suspected.

## Reference(s):

- [Tweet Cli on ClawHub](https://clawhub.ai/0xmythril/skills/tweet-cli)
- [0xmythril publisher profile](https://clawhub.ai/user/0xmythril)
- [X Developer Portal](https://developer.x.com/en/portal/dashboard)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may post, reply, quote, or delete X/Twitter content and require configured X API credentials.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Monitor X/Twitter accounts for new tweets and send notifications to Telegram.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mmmuffin](https://clawhub.ai/user/mmmuffin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to run a continuous monitor for selected X/Twitter accounts and receive Telegram notifications when new tweets appear.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles live X/Twitter session cookies and Telegram bot credentials.

Mitigation: Use a dedicated or low-risk X/Twitter session, treat AUTH_TOKEN, CT0, and Telegram bot tokens as secrets, and rotate them if exposed.

Risk: The monitor sends account names and tweet text to the configured Telegram chat while it runs.

Mitigation: Confirm the destination chat is appropriate before running the monitor and avoid using shared machines for sensitive sessions.

Risk: The script depends on an external xreach binary to fetch tweets.

Mitigation: Confirm the xreach binary source before use.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and environment variable names]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces guidance for configuring credentials and running a Python monitor that sends tweet notifications to Telegram.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

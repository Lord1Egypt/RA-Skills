## Description:

X/Twitter messaging management via API for reading tweets, posting tweets and threads, replying, sending DMs, searching tweets and users, and viewing analytics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[klemenska](https://clawhub.ai/user/klemenska)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to let an agent manage an authenticated X/Twitter account through API-backed CLI workflows for posting, replies, DMs, search, timelines, mentions, user lookup, tweet lookup, and public engagement analytics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can operate an authenticated Twitter/X account, including posting tweets, replies, threads, and DMs.

Mitigation: Review every post, reply, thread, and DM command before execution, and install the skill only when account operation is intended.

Risk: Twitter/X API credentials grant account access and may be exposed if stored insecurely.

Mitigation: Prefer environment variables or a secret manager, restrict credentials to the minimum API scopes needed, and avoid plaintext credential files when possible.

Risk: API tier limits and rate limits can block timeline, mention, DM, search, or analytics workflows.

Mitigation: Confirm the account's API tier supports the intended endpoints and monitor rate limit headers before repeated operations.

Risk: Dependency installation affects the local Python environment.

Mitigation: Install Tweepy in a virtual environment before running the CLI.

## Reference(s):

- [Twitter API v2 Rate Limits](references/api-limits.md)
- [Twitter Search Operators](references/search-operators.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and CLI text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-provided Twitter/X API credentials and Tweepy; API tier and rate limits affect available operations.]

## Skill Version(s):

1.0.0 (source: server evidence release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

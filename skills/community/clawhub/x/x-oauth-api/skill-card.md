## Description:

Provides an X (Twitter) OAuth 1.0a API client for posting tweets and threads, deleting tweets, checking account info, and using paid-tier search or mentions commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ngmeyer](https://clawhub.ai/user/ngmeyer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to configure X API credentials and run command-line workflows that post, delete, and thread tweets, inspect account details, and optionally retrieve mentions or search results when the account tier allows it.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Commands can post to or delete from a live X account.

Mitigation: Use a dedicated X app or low-risk account, review generated tweet content before posting, and run delete commands only when the account action is explicitly intended.

Risk: The implemented search, mentions, and automation behavior extends beyond the declared free-tier posting scope.

Mitigation: Confirm the account tier before using search or mentions, and limit automation scripts with clear posting caps and review of template content.

Risk: OAuth credentials are sensitive and required for the client to run.

Mitigation: Keep X API keys and access tokens private, rotate them if exposed, and avoid storing them in shared logs or source files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ngmeyer/skills/x-oauth-api)
- [X Developer Portal](https://developer.twitter.com/)
- [X API rate limits](https://developer.twitter.com/en/docs/twitter-api/rate-limits)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands; CLI output may be plain text or JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires X OAuth environment variables and network access to api.twitter.com]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

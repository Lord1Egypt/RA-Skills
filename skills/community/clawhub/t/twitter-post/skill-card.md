## Description:

Post tweets to Twitter/X via the official API v2 (OAuth 1.0a), including single tweets, threads, replies, and quote tweets with automatic character weight validation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sit-in](https://clawhub.ai/user/sit-in)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to publish Twitter/X posts through the official API, including threads, replies, and quote tweets. It is intended for workflows where tweet content is prepared elsewhere and then posted with user-provided OAuth credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Tweet text may become command execution if callers interpolate user-provided content into a shell command.

Mitigation: Invoke the script through a non-shell argument API or structured stdin/JSON input, and avoid shell string interpolation for tweet content.

Risk: The skill requires read/write Twitter/X OAuth credentials.

Mitigation: Store credentials in environment configuration, never hardcode keys, and install only where posting permissions are acceptable.

Risk: A configured HTTPS proxy can observe or influence network routing.

Mitigation: Leave HTTPS_PROXY unset unless the proxy is controlled and trusted.

Risk: The script can publish public posts to Twitter/X.

Mitigation: Use TWITTER_DRY_RUN=1 first and require explicit confirmation before each live post.

## Reference(s):

- [Twitter/X Developer Portal](https://developer.x.com)
- [ClawHub skill page](https://clawhub.ai/sit-in/skills/twitter-post)
- [Publisher profile](https://clawhub.ai/user/sit-in)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, API calls, Guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Posts are sent to Twitter/X unless dry-run mode is enabled; successful command output includes tweet IDs, URLs, and rate-limit fields.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

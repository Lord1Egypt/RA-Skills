## Description:

Use twitter-cli for Twitter/X operations including reading timelines, posting, replying, quoting, liking, retweeting, following, searching, and user lookups.

This skill is ready for commercial/non-commercial use.

## Publisher:

[flyingtimes](https://clawhub.ai/user/flyingtimes)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to operate Twitter/X from a terminal-oriented workflow for account reading, search, profile lookup, and reviewed write actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can access account capabilities equivalent to a logged-in Twitter/X browser session.

Mitigation: Use it only in a local isolated environment and restrict the browser profile with TWITTER_CHROME_PROFILE.

Risk: Manual full-cookie sharing can expose session credentials in remote-agent or chat workflows.

Mitigation: Prefer local browser cookie extraction and avoid copying raw cookies into chat logs.

Risk: Write actions can post, delete, follow, like, retweet, or otherwise change account state.

Mitigation: Review write actions before execution and allow them only when the requested account change is clear.

Risk: Proxy configuration can route authenticated requests through an untrusted network path.

Mitigation: Do not use untrusted proxies for authenticated Twitter/X sessions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/flyingtimes/skills/twitter-command)
- [Publisher profile](https://clawhub.ai/user/flyingtimes)
- [PyPI package](https://pypi.org/project/twitter-cli/)
- [Structured output schema](SCHEMA.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON or YAML CLI output examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The CLI supports rich table, compact text, YAML, and JSON output envelopes for agent workflows.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

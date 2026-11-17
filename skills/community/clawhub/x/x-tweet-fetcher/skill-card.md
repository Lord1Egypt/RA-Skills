## Description:

Fetch tweets from X/Twitter without login or API keys, including regular tweets, long tweets, quoted tweets, and full X Articles with zero dependencies or configuration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hjw21century](https://clawhub.ai/user/hjw21century)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to retrieve public X/Twitter post content, engagement metadata, quoted posts, and long-form article text without requiring X/Twitter credentials or API keys.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Requested public tweet identifiers are sent to the FxTwitter service.

Mitigation: Avoid use in sensitive research workflows where revealing the queried post identifier to a third-party service is unacceptable.

Risk: Fetching depends on FxTwitter availability and rate limits.

Mitigation: Handle returned errors explicitly and use an alternate collection path when FxTwitter is unavailable.

Risk: The skill cannot access reply threads, deleted tweets, or private tweets.

Mitigation: Use it only for public single-post extraction and rely on the returned reply count instead of expecting reply content.

## Reference(s):

- [X Tweet Fetcher on ClawHub](https://clawhub.ai/hjw21century/skills/x-tweet-fetcher)
- [FxTwitter / FxEmbed](https://github.com/FxEmbed/FxEmbed)
- [OpenClaw](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [text, JSON, code, shell commands]

**Output Format:** [JSON or plain text, with Markdown usage examples and Python API snippets in the skill guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a public x.com or twitter.com status URL; requests are sent to FxTwitter; no credentials or external Python packages are required.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

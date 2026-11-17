## Description:

Searches and reads X (Twitter) profiles, timelines, mentions, followers, tweet search, trends, lists, communities, and Spaces, and supports posting, liking, unliking, following, and unfollowing through OAuth-backed relay workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[baofeng-tech](https://clawhub.ai/user/baofeng-tech)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to retrieve Twitter/X account, tweet, trend, list, community, and Space data, and to publish or perform engagement actions after OAuth authorization. It is suited for social listening, market and competitor monitoring, account research, and controlled posting workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose the AISA_API_KEY in normal command output.

Mitigation: Do not run status, authorize, post, or engagement commands with a real key until key output exposure is fixed; rotate any key that may have been printed or logged.

Risk: Credentials, post text, media files, searches, and engagement targets are sent to the configured relay service.

Mitigation: Use only a trusted HTTPS AIsa relay and avoid custom TWITTER_RELAY_BASE_URL values unless the relay is controlled and reviewed.

Risk: The security verdict is suspicious because the skill handles account authorization and social actions through a relay.

Mitigation: Review the skill and relay configuration before installation, require explicit user authorization for account actions, and do not claim actions succeeded unless relay responses confirm success.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/baofeng-tech/skills/twitter-aisa-one)
- [AIsa](https://aisa.one)
- [AIsa API Reference](https://docs.aisa.one/reference/)
- [AIsa Twitter Engagement](references/engage_twitter.md)
- [AIsa Twitter OAuth](references/post_twitter.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON command results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include Twitter/X data, OAuth authorization URLs, publish results, tweet IDs or links, relay status, usage cost, and credits remaining.]

## Skill Version(s):

1.0.1 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Access X (Twitter) via API v2 for user profiles, timelines, threads, search, bookmarks, likes, posting, and tweet lookup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[odrobnik](https://clawhub.ai/user/odrobnik)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to retrieve, inspect, and publish X content through API v2 from a Python CLI. It supports public lookups with a bearer token and user-context actions such as bookmarks, likes, and posting through OAuth 2.0.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local X bearer, OAuth client, and user tokens are stored under ~/.openclaw/x.

Mitigation: Restrict ~/.openclaw/x to owner-only permissions, avoid shared machines for production credentials, and rotate tokens if the files are exposed.

Risk: OAuth-enabled commands can publish posts from the authenticated account.

Mitigation: Use a dedicated or test X app and account where possible, and require explicit user approval before running any post command.

Risk: Successful X API calls may consume paid credits and remain subject to rate limits.

Mitigation: Set X spending limits, monitor usage, cache repeated lookups, and design automated use around rate-limit headers.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/odrobnik/skills/twitter-api-v2)
- [Setup Guide](SETUP.md)
- [X API Quick Reference](references/quickstart.md)
- [X API Pricing](references/pricing.md)
- [X Developer Portal](https://developer.x.com)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Readable CLI text and Markdown instructions with bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Some commands require local X credentials and may call X API endpoints that are rate-limited or billed.]

## Skill Version(s):

1.0.0 (source: frontmatter and ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

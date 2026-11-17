## Description:

X (Twitter) API client for searching tweets, retrieving article content, and fetching trending topics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zaaachary](https://clawhub.ai/user/zaaachary)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to query X API v2 for recent posts, article or tweet details, and trending topics from an agent workflow. It requires Python 3 and an X API bearer token.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires an X API bearer token.

Mitigation: Use a temporary or secret-manager-provided least-privileged token, avoid storing it in shell startup files, and rotate or revoke it after use.

Risk: The optional save feature can overwrite arbitrary local files.

Mitigation: Use a dedicated output directory and review any --save path before running the scripts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zaaachary/skills/x-twitter-api)
- [Publisher profile](https://clawhub.ai/user/zaaachary)
- [X Developer Platform](https://developer.x.com)
- [X API documentation](https://docs.x.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and terminal-oriented text with optional JSON or Markdown file output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May issue X API calls and optionally save retrieved tweet, article, or trends data to a user-provided local path.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

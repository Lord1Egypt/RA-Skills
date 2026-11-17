## Description:

Reddit CLI using cookies for authentication. Read posts, search, and get subreddit info.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kelsia14](https://clawhub.ai/user/kelsia14)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent users can use this skill to read Reddit posts, search Reddit, retrieve subreddit metadata, and check cookie-based Reddit access from a command-line workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent shell configuration can expose Reddit session cookies more broadly than needed.

Mitigation: Do not place REDDIT_SESSION or TOKEN_V2 in shell startup files; provide them only for the command that needs them, prefer a secret manager or OAuth-based tool, and revoke the Reddit session if cookies may have been exposed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kelsia14/skills/reddit-cli)
- [Reddit](https://reddit.com)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown-style text with inline shell commands and CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [CLI output includes Reddit post summaries, search results, subreddit information, and cookie connection status.]

## Skill Version(s):

1.0.2 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

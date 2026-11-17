## Description:

Fetch, summarize, and manage X/Twitter bookmarks via bird CLI or X API v2.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sharbelayy](https://clawhub.ai/user/sharbelayy)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to turn X/Twitter bookmarks into categorized digests, action suggestions, scheduled summaries, content ideas, pattern reports, and cleanup prompts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use browser cookies or manual AUTH_TOKEN and CT0 values to access an X account session.

Mitigation: Prefer the X API path with read-only scopes, and avoid granting browser-cookie access unless the global bird-cli package has been independently verified.

Risk: Local credential files or sourced environment files can expose account tokens if handled carelessly.

Mitigation: Avoid `source .env.bird`, keep OAuth token files local with restrictive permissions, and rotate credentials if they may have been exposed.

Risk: The auth helper includes a token-printing option that can reveal an access token in terminal logs or transcripts.

Mitigation: Do not use `--print-token`; rely on local token refresh and only inspect tokens through secure credential handling workflows.

## Reference(s):

- [X Bookmarks Auth Setup](references/auth-setup.md)
- [X Developer Console](https://developer.x.com)
- [X API OAuth Token Endpoint](https://api.x.com/2/oauth2/token)
- [ClawHub Skill Page](https://clawhub.ai/sharbelayy/skills/x-bookmarks)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON bookmark data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May fetch authenticated X/Twitter bookmark data through bird CLI or X API v2 and may store local bookmark state or OAuth tokens.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

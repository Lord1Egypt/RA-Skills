## Description:

Interact with Twitter/X via TwitterAPI.io — search tweets, get user info, post tweets, like, retweet, follow, send DMs, and more. Covers all 76 active endpoints. Use when the user wants to read or write Twitter data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dorukardahan](https://clawhub.ai/user/dorukardahan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to search and analyze Twitter/X data through TwitterAPI.io, and to perform account actions when explicitly requested for the exact action and account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags an unpinned, automatically approved MCP install and notes that analysis was partial.

Mitigation: Review the package and use a fixed version before installing. Withhold passwords, reusable 2FA seeds, and session cookies unless you are comfortable with the provider receiving those credentials.

## Reference(s):

- [TwitterAPI.io API documentation](https://docs.twitterapi.io)
- [Endpoint index](references/endpoint-index.md)
- [Read endpoint reference](references/read-endpoints.md)
- [Write endpoint reference](references/write-endpoints.md)
- [Webhook and stream endpoint reference](references/webhook-stream-endpoints.md)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Shell commands, Code, Configuration instructions]

**Output Format:** [Markdown with inline curl, shell, JSON, and code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only by default; state-changing actions require explicit confirmation for the exact action and account.]

## Skill Version(s):

3.8.32 (source: frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Integrate Vercel AI SDK applications with You.com tools for web search, AI agent responses, and content extraction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edwardirby](https://clawhub.ai/user/edwardirby)

### License/Terms of Use:

MIT

## Use Case:

Developers use this skill to add You.com web tools to Vercel AI SDK applications that call generateText() or streamText(). It guides package installation, API key configuration, tool selection, and code updates for Node.js, Next.js, Express.js, and React integrations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The integration uses an external npm package and may change behavior if unpinned dependencies are installed.

Mitigation: Review the package and lockfile before installation and pin versions for production use.

Risk: The You.com API key could be exposed if hard-coded or committed.

Mitigation: Store the API key in environment variables or a secrets manager and avoid committing secrets.

Risk: Prompts, URLs, or retrieved content may be sent to You.com tools.

Mitigation: Avoid sending confidential, regulated, or unapproved data unless that data sharing is approved.

## Reference(s):

- [Package README](https://github.com/youdotcom-oss/dx-toolkit/tree/main/packages/ai-sdk-plugin)
- [Vercel AI SDK Docs](https://ai-sdk.dev/docs)
- [You.com API Keys](https://you.com/platform/api-keys)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown with TypeScript and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose edits to existing files or create new integration files based on the user's package manager, environment variable name, selected You.com tools, and AI SDK function.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

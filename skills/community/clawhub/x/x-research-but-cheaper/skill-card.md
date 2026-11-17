## Description:

X/Twitter research skill powered by TwitterAPI.io for agentic search, profile analysis, thread reading, watchlists, and sourced briefings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[minilozio](https://clawhub.ai/user/minilozio)

### License/Terms of Use:

MIT

## Use Case:

External users, developers, and research agents use this skill to search X/Twitter, analyze accounts and threads, monitor watchlists, and produce sourced social-media research summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented npx tsx runtime can fetch and execute an unpinned npm package.

Mitigation: Install a pinned, locked local tsx dependency or use compiled JavaScript before running the CLI in production environments.

Risk: X/Twitter research queries and account lookups are sent to TwitterAPI.io and may incur pay-per-use costs.

Mitigation: Use quick mode, cache reuse, explicit limits, and watchlist review to control query volume and cost.

Risk: TWITTERAPI_KEY could be exposed through inline commands, environment files, or agent session logs.

Mitigation: Keep the key in the environment, avoid pasting it into commands, keep .env files out of source control, review agent logging, and rotate the key after suspected exposure.

## Reference(s):

- [TwitterAPI.io API Reference](references/twitterapi-io.md)
- [TwitterAPI.io](https://twitterapi.io)
- [ClawHub Skill Page](https://clawhub.ai/minilozio/skills/x-research-but-cheaper)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Terminal text, JSON, and Markdown research summaries with sourced links.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can save Markdown reports and local cache or watchlist JSON under data/.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

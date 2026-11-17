## Description:

Use Ragora MCP tools and REST API to discover, search, and synthesize answers from knowledge bases.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mregmi](https://clawhub.ai/user/mregmi)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to connect to Ragora knowledge bases, retrieve grounded evidence through MCP or REST, and produce source-backed summaries, comparisons, due diligence research, and verification answers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API key exposure could grant access to the user's Ragora collections.

Mitigation: Store RAGORA_API_KEY in an environment variable or secret manager, and never hardcode, log, or display the full key.

Risk: Search queries and retrieval requests are sent to Ragora for processing.

Mitigation: Use the skill only with collections and queries the user is willing to process through Ragora.

Risk: Marketplace collection retrieval can consume credits.

Mitigation: Monitor credit usage and check balance before broad or repeated retrieval workflows.

## Reference(s):

- [Ragora OpenClaw homepage](https://github.com/velarynai/ragora-openclaw)
- [Ragora MCP guide](https://ragora.app/docs?section=mcp-guide)
- [Ragora getting started](https://ragora.app/docs?section=getting-started)
- [Ragora API overview](https://ragora.app/docs?section=api-overview)
- [Ragora Retrieve API](https://ragora.app/docs?section=api-retrieve)
- [Ragora errors and limits](https://ragora.app/docs?section=api-errors)
- [Ragora Billing API](https://ragora.app/docs?section=api-billing)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline JSON, YAML, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires RAGORA_API_KEY and may make authenticated MCP or REST API requests to Ragora.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

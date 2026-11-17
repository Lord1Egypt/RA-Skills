## Description:

Connects agents to paid web-reading, structured extraction, verification, business lookup, provider data, and media-generation tools through toll402.dev.

This skill is ready for commercial/non-commercial use.

## Publisher:

[toll402](https://clawhub.ai/user/toll402)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to discover and call paid external tools for reading, data extraction, validation, research, business lookup, and media generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paid tool calls can incur unexpected charges.

Mitigation: Discover tools before paying, keep per-call and daily spending limits low, and review charges.

Risk: Payment credentials or API keys could be exposed.

Mitigation: Keep keys in environment variables or headers, never include them in logs or URLs, and use a dedicated low-balance wallet for x402.

Risk: External tools receive submitted content, which may include personal or sensitive data.

Mitigation: Send only necessary inputs and avoid secrets or unnecessary personal data.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/toll402/skills/toll402)
- [Toll402 documentation](https://toll402.dev/llms.txt)
- [Toll402 homepage](https://toll402.dev)
- [Repository listed in skill metadata](https://github.com/toll402/toll402)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with API examples; tool results may be text, JSON, or media links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Paid external calls require prepaid credits or USDC; generation tasks may return asynchronously.]

## Skill Version(s):

1.3.0 (source: ClawHub release and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

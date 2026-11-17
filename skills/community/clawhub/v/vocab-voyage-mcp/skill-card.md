## Description:

Provides vocabulary definitions, quizzes, course word lists, study plans, word-of-the-day results, and contextual word explanations for academic and standardized test preparation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jaideepdhanoa](https://clawhub.ai/user/jaideepdhanoa)

### License/Terms of Use:

MIT-0

## Use Case:

Students, educators, and MCP-compatible agents use this skill to look up vocabulary, generate test-prep quizzes, list course words, preview study plans, and explain words in sentence context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The hosted service records usage and source metadata for tool calls.

Mitigation: Review privacy expectations before use and avoid sending unnecessary personal or sensitive vocabulary-study context.

Risk: Personal bearer tokens can unlock profile and progress data.

Mitigation: Prefer anonymous access when personalization is not needed, and avoid placing bearer tokens in command-line arguments when possible.

Risk: The npx bridge path is unpinned and may introduce installation supply-chain risk.

Mitigation: Prefer the direct hosted MCP connector or OpenClaw install path over the unpinned npx bridge.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jaideepdhanoa/skills/vocab-voyage-mcp)
- [Vocab Voyage MCP documentation](https://vocab.voyage/mcp)
- [MCP server card](https://vocab.voyage/.well-known/mcp/server-card.json)
- [Agent card](https://vocab.voyage/.well-known/agent-card.json)
- [Authentication and scopes](https://vocab.voyage/developers/auth)
- [OpenAPI specification](https://vocab.voyage/openapi.json)
- [MCP Apps manifest](https://vocab.voyage/.well-known/mcp/apps.json)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Structured MCP tool responses with optional renderable UI resources.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Anonymous access is supported for public tools; optional bearer tokens unlock personalized profile and progress features.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

RuRussian MCP turns an OpenClaw bot into a Russian tutor with vocabulary analysis, sentence breakdowns, reading practice, learner memory, and paid activation support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shuyuew1991](https://clawhub.ai/user/shuyuew1991)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this MCP server to connect OpenClaw or compatible agents to Russian tutoring workflows, including vocabulary support, grammar explanations, reading practice, translation, learner progress tracking, and subscription activation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can start paid hosted-checkout flows for subscription activation.

Mitigation: Require explicit human approval before every purchase step, use hosted checkout only, and do not collect payment card details in chat.

Risk: API keys, learner emails, submitted text, and progress data may be transmitted to the service or stored locally.

Mitigation: Keep API keys out of shared or committed configuration, treat learner data as sensitive, and choose a local memory path with appropriate access controls.

Risk: Configurable API and purchase endpoints can send requests to alternate services.

Mitigation: Use the default official HTTPS RuRussian endpoint unless the operator has verified and fully trusts the alternate endpoint.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/shuyuew1991/skills/rurussian-mcp)
- [Project Homepage](https://github.com/shuyueW1991/rurussian-mcp)
- [OpenClaw Integration Guide](docs/INTEGRATION.md)
- [Tool Examples](examples/tool_examples.json)
- [OpenClaw Configuration Example](examples/openclaw_config.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Structured JSON tool responses plus Markdown setup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Learning tools require an API key or confirmed hosted checkout; learner memory is stored in a local JSON file unless configured otherwise.]

## Skill Version(s):

2.0.0 (source: server release metadata and pyproject.toml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

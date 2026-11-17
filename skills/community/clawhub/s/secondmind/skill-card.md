## Description:

SecondMind gives OpenClaw agents persistent memory, proactive project suggestions, project tracking, and social-context awareness using local storage and OpenRouter-based LLM processing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[emphaiser](https://clawhub.ai/user/emphaiser)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw users use SecondMind to ingest conversation history, search persistent memory, and receive proactive proposals, reminders, and project-tracking updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill persistently indexes private OpenClaw conversations in a local memory database.

Mitigation: Review the configured session path before use, protect the data directory, and install only if persistent local indexing is acceptable.

Risk: Conversation-derived content is processed by cloud LLM calls through OpenRouter.

Mitigation: Avoid placing secrets in agent chat, protect config.json, and pin endpoint configuration to OpenRouter over HTTPS.

Risk: Optional Telegram or Discord notifications can contain memory-derived content.

Mitigation: Keep notifications disabled unless needed, verify chat IDs and webhook destinations, and protect bot tokens.

Risk: Scheduled jobs can process sessions and generate proposals automatically.

Mitigation: Review or disable scheduled jobs before deployment if automatic background processing is not desired.

## Reference(s):

- [SecondMind on ClawHub](https://clawhub.ai/emphaiser/skills/secondmind)
- [OpenRouter](https://openrouter.ai)
- [OpenRouter Models](https://openrouter.ai/models)
- [Node.js](https://nodejs.org)
- [OpenClaw](https://github.com/openclaw)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration values]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct Node.js scripts that create or update local SQLite memory data, proposal records, and optional notification content.]

## Skill Version(s):

1.4.0 (source: SKILL.md frontmatter, package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

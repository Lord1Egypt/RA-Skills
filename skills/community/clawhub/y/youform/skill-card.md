## Description:

Find Youform templates and create or edit forms, surveys, and quizzes using an available Youform MCP connection. Also use for publishing an authorized form or analyzing its responses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mkmaker](https://clawhub.ai/user/mkmaker)

### License/Terms of Use:

MIT-0

## Use Case:

People using an AI assistant with Youform use this skill to find public templates, draft and manage forms in their account, publish forms when authorized, and analyze selected responses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The OAuth connection may reach more account data than the current task needs.

Mitigation: Check the account and workspace during consent, then limit access to the intended form and responses.

Risk: Publishing a form may expose it to an unintended audience.

Mitigation: Explicitly authorize publishing and review the questions, confirmation behavior, and intended audience first.

Risk: Credentials or private respondent details could be exposed in chat or shared summaries.

Mitigation: Keep tokens out of chat and private respondent details out of shared summaries unless needed and authorized.

## Reference(s):

- [Youform Developer Documentation](https://youform.com/developers/)
- [Youform Public API Specification](https://youform.com/openapi.json)
- [Connect an AI Assistant to Youform](https://help.youform.com/connect-an-ai-assistant-to-youform-1tjid)
- [Youform Agent Instructions](https://youform.com/agent-instructions.md)
- [Youform MCP Tools and Permissions](https://help.youform.com/youform-mcp-tools-and-permissions-e9hl0)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, API Calls]

**Output Format:** [Markdown and plain text, including template links, form drafts, and response summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Account actions use the connected Youform workspace; publishing requires explicit authorization.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

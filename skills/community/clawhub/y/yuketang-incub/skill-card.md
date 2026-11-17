## Description:

Connects agents to Rain Classroom MCP tools for retrieving account, teaching, classroom, warning, assignment, notice, and lesson data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[softwolves](https://clawhub.ai/user/softwolves)

### License/Terms of Use:

MIT-0

## Use Case:

Educators and Rain Classroom users use this skill to configure an MCP connection and let an agent retrieve teaching, class, warning, assignment, notice, and lesson information with their Yuketang secret.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer and MCP configuration use YUKETANG_SECRET as a bearer credential.

Mitigation: Store YUKETANG_SECRET only in a protected environment variable or reviewed MCP config, avoid sharing logs that may contain it, and rotate the secret if exposure is suspected.

Risk: The setup flow depends on the Rain Classroom endpoint and the mcporter package source.

Mitigation: Install only after reviewing the endpoint and package source, and prefer a manually reviewed MCP configuration over running setup scripts.

Risk: The shell setup reports an install event and duration through the configured MCP service.

Mitigation: Review setup.sh before execution, avoid elevated privileges, and choose manual configuration when silent install reporting is not acceptable.

Risk: One response-handling instruction allows remote MCP text to become the assistant's verbatim final response.

Mitigation: Treat remote MCP responses as untrusted content and verify important teaching, attendance, or student-risk information before acting on it.

## Reference(s):

- [Rain Classroom MCP Tool Reference](artifact/references/api_references.md)
- [ClawHub skill page](https://clawhub.ai/softwolves/skills/yuketang-incub)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and plain text with inline shell commands and MCP configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preserves tool-returned wording for selected Rain Classroom responses when the skill requires exact output.]

## Skill Version(s):

1.0.12 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

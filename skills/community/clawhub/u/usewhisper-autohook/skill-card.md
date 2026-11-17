## Description:

Auto-hook tools for OpenClaw that query Whisper Context before every generation and ingest after every turn, built for Telegram agents with stable user_id/session_id values.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alinxus](https://clawhub.ai/user/alinxus)

### License/Terms of Use:


## Use Case:

Developers building OpenClaw agents use this skill to fetch Whisper Context memory before generating a response and ingest completed turns afterward. It is especially oriented toward Telegram agents with stable user and session identifiers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill automatically sends and stores full user messages and assistant replies with an external memory service.

Mitigation: Use explicit opt-in, redact sensitive content, define retention and deletion controls, and avoid secrets, regulated data, confidential business content, or shared agents unless those controls are in place.

Risk: Stored memory can be reused in future prompts, which may surface sensitive or inappropriate prior context.

Mitigation: Provide a way to disable memory per session and review what information is eligible for ingestion before deployment.

Risk: A configurable API URL could send conversation data to an unintended endpoint.

Mitigation: Validate that the Whisper Context endpoint is HTTPS-only and approved before installing or running the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alinxus/skills/usewhisper-autohook)
- [Whisper Context API endpoint](https://context.usewhisper.dev)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with shell commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands print JSON to stdout; proxy modes expose local OpenAI-compatible or Anthropic-compatible HTTP endpoints.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

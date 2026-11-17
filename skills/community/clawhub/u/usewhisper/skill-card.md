## Description:

Official Whisper Context skill for OpenClaw. Cuts context tokens via delta compression + caching, and adds long-term memory across sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alinxus](https://clawhub.ai/user/alinxus)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to retrieve compressed context, persist session memory, search memories, run Oracle search, inspect cache behavior, and review cost summaries for OpenClaw agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send API credentials and conversation or memory data to a configured endpoint, including an endpoint changed from the default.

Mitigation: Use only the default trusted API URL or another approved endpoint, and do not pass secrets or regulated data into memory.

Risk: The Whisper Context API key is a credential used for outbound API requests.

Mitigation: Store the key in the runtime environment or a secrets manager, do not commit it to source control, and rotate it if exposed.

Risk: Shared or poorly scoped user_id and session_id values can mix memory between users or sessions.

Mitigation: Keep user_id and session_id stable but scoped to the correct user and session.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alinxus/skills/usewhisper)
- [Whisper Context API default endpoint](https://context.usewhisper.dev)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node and the WHISPER_CONTEXT_API_KEY and WHISPER_CONTEXT_PROJECT environment variables; WHISPER_CONTEXT_API_URL is optional.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact frontmatter lists 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

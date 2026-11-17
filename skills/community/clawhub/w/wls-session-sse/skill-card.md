## Description:

WLS runtime engineer skill for session isolation, Session Server behavior, and cooperative SSE runtime implementation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aiweline](https://clawhub.ai/user/aiweline)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to repair or implement WLS session isolation, Session Server behavior, and SSE streaming flows while preserving cooperative runtime behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is intended for WLS development contexts and may reference internal project guidance files.

Mitigation: Install it only where agents are expected to inspect WLS project guidance, and review referenced internal files before use if they may contain sensitive rules.

Risk: Session and SSE changes can affect login isolation, streaming behavior, or worker availability.

Mitigation: Validate on a dedicated non-production WLS instance, use cooperative delay patterns, and stop the validation instance after testing.

## Reference(s):

- [AI-ENTRY.md](AI-ENTRY.md)
- [CLAUDE.md](CLAUDE.md)
- [Session Development Skill](dev/ai/skills/session-development/SKILL.md)
- [SSE Streaming Skill](dev/ai/skills/sse-streaming/SKILL.md)
- [Weline Framework Runtime Skill](dev/ai/skills/weline-framework-runtime/SKILL.md)
- [Runtime and Process Skill](dev/ai/skills/runtime-and-process/SKILL.md)

## Skill Output:

**Output Type(s):** [guidance, code, shell commands, configuration, markdown]

**Output Format:** [Markdown with code, shell commands, validation notes, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Expected to include dedicated WLS validation evidence and confirmation that the test instance was stopped.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

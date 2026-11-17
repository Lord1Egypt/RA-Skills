## Description:

LLM streaming output formatter with auto buffer, format correction, sentence break optimization, markdown rendering, improve chat UX.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ayalili](https://clawhub.ai/user/ayalili)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to buffer and format streaming LLM chunks before they are shown in chat, chatbot, or real-time content generation interfaces.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Shared module-level stream state could mix or expose conversation content when multiple users or streams share the same runtime.

Mitigation: Run the skill in a strictly isolated per-user or per-conversation process, or refactor it to keep per-stream state and bind reset/configuration operations to the correct caller.

Risk: Unbounded chunks, retained buffers, or abandoned streams could increase memory exposure and reliability risk.

Mitigation: Enforce chunk and buffer limits, expire or reset abandoned streams, and review deployment behavior before enabling the skill in shared environments.

Risk: The documentation is Chinese-only and the skill imports zod from a remote Deno URL, which may not fit every deployment policy.

Mitigation: Review the documentation and remote dependency policy for the target environment before installation.

## Reference(s):

- [Zod v3.22.4 Deno module](https://deno.land/x/zod@v3.22.4/mod.ts)
- [ClawHub stream-formatter skill page](https://clawhub.ai/ayalili/skills/stream-formatter)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance]

**Output Format:** [JSON object containing success status, formatted output text, buffer state, and configuration details depending on the action.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Processes init, process, and reset actions for streamed text chunks; process responses may include buffered remaining length and has_more state.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

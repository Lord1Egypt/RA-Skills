## Description:

Provides reasoning, self-correction, context-management, and multi-step planning frameworks for agents handling complex analysis, creative problem solving, long-context synthesis, and deeper reasoning requests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pmuhammadagus-byte](https://clawhub.ai/user/pmuhammadagus-byte)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to make an agent apply structured reasoning, self-review, uncertainty handling, and multi-step planning on complex tasks. It is most relevant for coding, analysis, research, planning, and problem-solving workflows where deeper reasoning is requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill broadly changes agent reasoning style and may make responses more deliberate, structured, or verbose across complex tasks.

Mitigation: Enable it only for agents or workflows where deeper reasoning is desired, and monitor output length and usefulness after installation.

Risk: Managed installation or applying the SOUL.md guidance can affect all agents on a machine or persistently alter persona and tone.

Mitigation: Review those installation paths before applying them globally, and prefer workspace-scoped installation when testing.

Risk: Behavior-shaping instructions are not a security control and must not override platform policy, user oversight, or factual verification.

Mitigation: Keep existing agent safety policies in force, review proposed actions before execution, and verify important claims before relying on them.

## Reference(s):

- [Reasoning Frameworks](references/reasoning-frameworks.md)
- [Cognitive Patterns](references/cognitive-patterns.md)
- [Self-Correction](references/self-correction.md)
- [Context Management](references/context-management.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with optional inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May increase verbosity and token usage because it asks the agent to reason, verify, synthesize, and reflect before responding.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

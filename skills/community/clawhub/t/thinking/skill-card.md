## Description:

Thinking-Claude inspired comprehensive thinking protocol with Verification Protocol and Confidence Scoring for OpenClaw agents

This skill is ready for commercial/non-commercial use.

## Publisher:

[leezongdai](https://clawhub.ai/user/leezongdai)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent users use this skill to add a structured thinking, verification, uncertainty, and confidence reporting protocol to OpenClaw agent responses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill changes broad agent reasoning and response behavior, including requests to expose thinking blocks, which can leak sensitive context or conflict with policies that keep reasoning private.

Mitigation: Install it only when broad response-behavior changes are intended, and avoid placing it in global agent configuration unless every session should use this behavior.

Risk: The skill can increase token usage and output length by adding detailed thinking, verification, confidence tables, and uncertainty sections.

Mitigation: Use it for workflows where extra explanation is valuable, and scope or disable it for token-sensitive or latency-sensitive tasks.

Risk: The required confidence material and thinking code blocks can break strict JSON, machine-readable, or template-constrained outputs.

Mitigation: Disable or override the skill for structured-output workflows, or add a higher-priority instruction that preserves the required output schema.

## Reference(s):

- [Thinking Protocol ClawHub page](https://clawhub.ai/leezongdai/skills/thinking)
- [Thinking-Claude project](https://github.com/richards199999/Thinking-Claude)
- [SKILL-howto.md](artifact/SKILL-howto.md)
- [SKILL-examples.md](artifact/SKILL-examples.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, code]

**Output Format:** [Markdown with thinking code blocks, confidence assessment tables, and uncertainty tags]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May add verification language, confidence scores, uncertainty labels, and thinking blocks to agent responses.]

## Skill Version(s):

2.1.0 (source: server release metadata, SKILL.md frontmatter, changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

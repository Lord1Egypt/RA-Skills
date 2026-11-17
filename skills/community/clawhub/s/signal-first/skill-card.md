## Description:

Response calibration for Claude — match answer depth to question complexity. Stop getting 10-paragraph essays for 10-word questions. More signal, less noise.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiajiaoy](https://clawhub.ai/user/jiajiaoy)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to calibrate agent responses so answer length and structure match the complexity of the request. It is intended to reduce filler, repeated framing, and over-explanation while preserving needed information.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can bias responses toward shorter, denser answers that may omit useful context in workflows that expect detailed explanations.

Mitigation: Review whether concise response calibration fits the intended workflow and explicitly request deeper explanation where needed.

## Reference(s):

- [Signal First ClawHub Page](https://clawhub.ai/jiajiaoy/skills/signal-first)
- [Clawdis Homepage](https://clawhub.ai/skills/signal-first)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Concise natural language or minimal Markdown, with code blocks or shell commands only when the request calls for them]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Response length is calibrated to request complexity, from one-line answers through longer structured analysis when needed.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

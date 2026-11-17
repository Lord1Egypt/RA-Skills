## Description:

A Chinese-language chat coaching skill that helps users interpret relationship messages with confidence-labeled boundaries, then draft respectful reply options with consequences and conditions for use.

This skill is ready for commercial/non-commercial use.

## Publisher:

[419597334-sudo](https://clawhub.ai/user/419597334-sudo)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to understand Chinese dating or relationship chat context, identify likely communication intent without claiming mind-reading, and draft respectful message options they can review before sending.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may paste unnecessary personal identifiers from private chat logs.

Mitigation: Ask users to avoid sharing names, phone numbers, addresses, workplaces, schools, and account handles; the artifact also instructs replacement of such identifiers in outputs.

Risk: Relationship-message interpretations may be mistaken for certainty or used without personal judgment.

Mitigation: Present interpretations with confidence labels, state what cannot be inferred, and require the user to review any suggested message before sending.

Risk: Dating advice can be misused for manipulation, deception, repeated pursuit, or pressure after refusal.

Mitigation: Apply the artifact's redlines against PUA, deception, impersonation, coercion, unwanted pursuit, and chat tactics in dangerous or abusive situations.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/419597334-sudo/skills/straight-guy-chat-coach)
- [解码信号与关系阶段](artifact/references/decoding-and-stages.md)
- [红线与自检](artifact/references/redlines.md)
- [高频场景库](artifact/references/scenarios.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown-style structured Chinese text with labeled analysis, reply options, rationale, and anti-patterns]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill produces user-reviewed draft message text only; it does not send messages or perform account, network, executable, or persistence actions.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

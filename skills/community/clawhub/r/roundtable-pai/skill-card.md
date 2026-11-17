## Description:

圆桌派会把用户的一个问题变成一场三位大师的圆桌讨论。

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhouxiang1](https://clawhub.ai/user/zhouxiang1)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this Chinese-language conversation skill to turn a question into a staged three-person roundtable discussion for decision diagnosis, viewpoint comparison, execution planning, reflection, or creative ideation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated persona statements may be mistaken for factual quotes or endorsements from real people.

Mitigation: Keep the required persona-simulation disclaimer and treat discussion output as a role-played perspective, not as real speech.

Risk: Questions and user interventions are stored in local runtime state.

Mitigation: Avoid entering secrets or sensitive personal data when using the skill.

Risk: Specially crafted multiline prompts could distort the roundtable output format.

Mitigation: Review generated rounds before relying on them and preserve the one-turn-at-a-time controller workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhouxiang1/skills/roundtable-pai)
- [Publisher profile](https://clawhub.ai/user/zhouxiang1)
- [README](artifact/README.md)
- [Interface contracts](artifact/references/interface-contracts.md)
- [Safety guidance](artifact/references/safety.md)
- [Discussion quality](artifact/references/discussion-quality.md)
- [User-facing output](artifact/references/user-facing-output.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Chinese Markdown conversation text with controller-derived candidate lists, one discussion round at a time, and final conclusion fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill stores local runtime state and requires a persona-simulation disclaimer before the first discussion round.]

## Skill Version(s):

1.6.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

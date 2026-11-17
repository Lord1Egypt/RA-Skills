## Description:

Guides Chinese-speaking users through the SBTI entertainment personality questionnaire, computes a 15-dimension score, and returns one of the documented personality types.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mydearzsy](https://clawhub.ai/user/mydearzsy)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill for a Chinese-language entertainment personality questionnaire and result explanation. Agents can administer questions, calculate SBTI scores, summarize the resulting type, and provide reverse-query guidance for target personality types.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may mistake the entertainment result for a serious psychological or clinical assessment.

Mitigation: Present results as entertainment-only and avoid using them for consequential decisions.

Risk: Question and type text includes crude or potentially offensive humor.

Mitigation: Use the skill only with audiences and contexts where this tone is acceptable.

Risk: Documentation has inconsistent counts around questions, personality types, and the hidden DRUNK result.

Mitigation: Review the question count, type count, and hidden result behavior before relying on the skill in a published workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mydearzsy/skills/silly-big-type)
- [SBTI questions reference](artifact/references/questions.md)
- [SBTI personality types reference](artifact/references/types.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Chinese-language Markdown or plain text with optional shell command invocation and score summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Questionnaire outputs are for entertainment and should not be treated as psychological or clinical assessment.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

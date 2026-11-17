## Description:

A Chinese-language thinking-coach skill that uses six Mao Selected Works methodology modules to help users analyze complex problems, decisions, and strategy through one-question-at-a-time guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[susstoiclab](https://clawhub.ai/user/susstoiclab)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill as a Chinese-language thinking coach for structured problem analysis, decision support, investigation planning, practice validation, stakeholder alignment, and strategic judgment. The skill guides reflection without replacing the user's judgment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad trigger phrases such as "实事求是" or "群众路线" may route ordinary Chinese-language conversations into this skill.

Mitigation: Confirm that the user wants Mao methodology coaching before proceeding with a module.

Risk: Non-Chinese users may not receive useful guidance without translation.

Mitigation: Offer to translate or summarize the selected module before beginning the question chain.

Risk: The skill can influence decisions through ideological and strategic framing.

Mitigation: Keep the agent in a coaching role, ask one question at a time, and leave final judgments to the user.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/susstoiclab/skills/sustoiclab-mao-analysis)
- [矛盾论 · 在复杂关系里找主次、看方面、看转化](references/contradiction.md)
- [调查研究 · 没有调查就没有发言权](references/investigation.md)
- [群众路线 · 从群众中来，到群众中去](references/mass-line.md)
- [实践论 · 认识两次飞跃，真理的标准是实践](references/practice.md)
- [实事求是 · 从客观实际引出规律](references/seek-truth.md)
- [战略与战术 · 弱势怎么打、长期怎么耗](references/strategy.md)

## Skill Output:

**Output Type(s):** [guidance, analysis, markdown]

**Output Format:** [Markdown conversational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One question at a time; the skill is designed to guide user reasoning rather than provide final decisions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

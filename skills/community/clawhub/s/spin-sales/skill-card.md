## Description:

终极版 SPIN 销售法专家系统 - 提供从开场、挖掘、到促成的全周期、可操作的销售对话脚本框架。适用于复杂的 B2B 销售咨询场景。

This skill is ready for commercial/non-commercial use.

## Publisher:

[mikewongonline](https://clawhub.ai/user/mikewongonline)

### License/Terms of Use:

MIT-0

## Use Case:

External sales teams, consultants, and B2B solution sellers use this skill to structure complex consultative sales conversations with SPIN questions, opening scripts, objection handling, and action-plan outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests memory_search and tavily_search even though the bundled local scripts do not require retained-context lookup or external search.

Mitigation: Disable or deny those permissions unless the deployment specifically needs retained-context lookup or external market research.

Risk: Generated outreach or opening scripts could obscure the commercial purpose of a sales conversation.

Mitigation: Review and revise outreach scripts so prospects clearly understand the sales context.

Risk: The security verdict is suspicious, so the skill should not be enabled without review.

Mitigation: Review the requested permissions, scan results, and generated sales materials before installation or deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mikewongonline/skills/spin-sales)
- [Publisher profile](https://clawhub.ai/user/mikewongonline)
- [SPIN Selling reference](https://en.wikipedia.org/wiki/SPIN_selling)
- [Situation questions](references/s-questions.md)
- [Problem questions](references/p-questions.md)
- [Implication questions](references/i-questions.md)
- [Need-payoff questions](references/n-questions.md)
- [Objection handling](references/objections.md)
- [Opening scripts](references/opening_scripts.md)
- [Interactive exercises](training/interactive-exercises.md)
- [Evaluation checklist](training/evaluation-checklist.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain text with Python examples, shell commands, and JSON-like action-plan data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language SPIN sales questions, opening scripts, objection-handling guidance, training material, and demo outputs.]

## Skill Version(s):

3.0.1 (source: server release evidence, created 2026-05-19)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

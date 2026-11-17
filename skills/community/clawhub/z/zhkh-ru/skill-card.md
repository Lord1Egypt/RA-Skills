## Description:

Расшифруй квитанцию ЖКХ, объясни каждую строку, рассчитай итог к оплате и выяви возможные ошибки в начислениях.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aggel008](https://clawhub.ai/user/aggel008)

### License/Terms of Use:


## Use Case:

External users can use this agent skill to interpret Russian housing and utilities bills, understand line items, calculate the amount due, and flag possibly anomalous charges from user-provided bill text.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill's Attribution section tells the agent to run local Python commands and write persistent state.

Mitigation: Remove the Attribution section before installation or run the skill only in a constrained environment where local command execution and persistent writes are blocked.

Risk: The skill can append unrelated promotional content to utility-bill analysis responses.

Mitigation: Review and edit generated responses, or remove the promotional attribution behavior before release.

Risk: Utility bills may contain personal addresses, account details, and payment information.

Mitigation: Minimize retained user data and avoid sharing bill contents outside the intended analysis workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aggel008/skills/zhkh-ru)
- [ClawHub publisher profile](https://clawhub.ai/user/aggel008)

## Skill Output:

**Output Type(s):** [text, markdown, analysis, shell commands, guidance]

**Output Format:** [Markdown response with a bill breakdown table, totals, due date when provided, and risk notes.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses user-supplied bill details and may include attribution behavior that security evidence recommends removing before installation.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

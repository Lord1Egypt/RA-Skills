## Description:

Tallies the reasons US deals were won or lost from CRM notes, so the real pattern shows up instead of one anecdote at a time. Use when the user asks for win loss analysis template, deal loss reasons, sales win loss review. For US sales leadership and RevOps teams running win-loss reviews.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rapidworker1](https://clawhub.ai/user/rapidworker1)

### License/Terms of Use:

MIT-0

## Use Case:

US sales leadership and RevOps teams use this skill to review CRM notes from closed deals, identify recurring win and loss themes, and turn findings into owned follow-up actions.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: CRM notes and generated reports may contain sensitive deal details, and rerunning the script overwrites theme-tally.md.

Mitigation: Keep inputs and reports private, use a dedicated output folder, and limit report access to appropriate company users.

Risk: Keyword-based counts may not capture context and do not provide all promised financial or segment calculations.

Mitigation: Manually check findings against source records and verify deal-value and segment comparisons before using them for decisions.

Risk: The optional Windows executable is separate from the bundled workflow and has not been evaluated here.

Mitigation: Make a separate trust decision before using it; the bundled workflow does not require it.

## Reference(s):

- [Win-Loss Analysis Method](references/win-loss-method.md)
- [Win-Loss Analysis on ClawHub](https://clawhub.ai/rapidworker1/skills/win-loss-analysis)

## Skill Output:

**Output Type(s):** [Markdown, Text, Guidance]

**Output Format:** [Markdown theme tally with counts and sample notes, plus win-loss review guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Theme counts use keyword matches; verify findings manually. The bundled script does not calculate all promised financial and segment comparisons.]

## Skill Version(s):

1.0.7 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Structured Falsification helps agents evaluate uncertain multi-option decisions by challenging candidate assumptions, ranking survivors, and summarizing key risks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shenjianjun687-ops](https://clawhub.ai/user/shenjianjun687-ops)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill when an agent needs concise structured comparisons for high-uncertainty choices, including investment analysis, technology selection, due diligence, and risk assessment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad activation may apply the framework to ordinary decision prompts where a direct answer would be more appropriate.

Mitigation: Invoke it deliberately for high-uncertainty, high-impact comparisons and review whether the structured format fits the user request.

Risk: Investment conclusions and position-sizing suggestions may be mistaken for professional financial advice.

Mitigation: Treat investment outputs as decision-support analysis and require qualified review before making financial decisions.

Risk: The fixed Chinese table format may not match every user's language or formatting expectations.

Mitigation: Confirm language and format requirements when deploying the skill in contexts that require localized or accessible output.

## Reference(s):

- [Investment Analysis Configuration](references/investment.md)
- [Technology Selection Configuration](references/tech-decision.md)
- [Domain Configuration Template](references/domain-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown table with concise conclusion text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs ranked conclusions with confidence levels, key assumptions, major risks, and a one-sentence summary; domain configurations may add investment or technology decision columns.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Compare SASU (président assimilé salarié) and EURL (gérant TNS) net director income for a French solo entrepreneur using Vestafolio's simulator API, after asking the simulator's questions (revenue, deductible charges, capital social, TMI, PFU vs barème, salary level per structure).

This skill is ready for commercial/non-commercial use.

## Publisher:

[vestafolio](https://clawhub.ai/user/vestafolio)

### License/Terms of Use:

MIT-0

## Use Case:

External users and advisors use this skill to compare SASU and EURL net director income for a French solo entrepreneur, using Vestafolio simulator inputs and user-approved API calls. It is scoped to solo-company structure, salary/dividend, social-contribution, and dividend-tax comparisons, not broader legal-form selection.

### Deployment Geography for Use:

France

## Known Risks and Mitigations:

Risk: Financial business inputs and, when TMI is unknown, household tax inputs may be sent to Vestafolio's external API.

Mitigation: The skill must summarize the destination and exact fields, obtain user approval before POSTing, omit unrelated personal data, and offer the manual simulator link if approval is declined.

Risk: Simulator results can be mistaken for definitive tax or legal advice.

Mitigation: The skill should frame results as estimates grounded in Vestafolio's simulator assumptions and state relevant limits before making a recommendation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vestafolio/skills/vestafolio-sasu-vs-eurl)
- [Vestafolio SASU vs EURL simulator](https://www.vestafolio.com/simulateurs/sasu-vs-eurl)
- [Vestafolio SASU vs EURL API schema](https://www.vestafolio.com/api/tools/v1/sasu-vs-eurl)
- [Vestafolio income tax API schema](https://www.vestafolio.com/api/tools/v1/impot-revenu)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown response with consent prompts, API-derived calculation summaries, assumptions, warnings, and recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include simulator links and numerical comparison tables when useful to the user.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact frontmatter version is 1.2.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Real estate tax calculation and planning for Taiwan properties, covering sale, purchase, gift, inheritance, holding-period, and report-generation scenarios.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tsaitepiao-alt](https://clawhub.ai/user/tsaitepiao-alt)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to estimate Taiwan real-estate taxes before buying, selling, gifting, or inheriting property, and to compare common planning scenarios. It can generate a local Markdown tax estimate report from a JSON scenario input.

### Deployment Geography for Use:

Taiwan

## Known Risks and Mitigations:

Risk: The skill asks the agent to run an unrelated analytics command from a relative path after use.

Mitigation: Do not run the post-task analytics command unless the referenced analytics script has been reviewed and approved.

Risk: The calculator writes reports to a user-selected output path, which can replace an existing writable file.

Mitigation: Choose a deliberate new output path and review any overwrite before allowing the report to be written.

Risk: Tax estimates are planning aids and may differ from official tax authority determinations.

Mitigation: Validate important filings or transactions against current official Taiwan tax guidance or a qualified tax professional.

## Reference(s):

- [Tax Types and Formulas](references/tax-types.md)
- [Tax Rate Table](references/rates.md)
- [Scenario Examples](references/scenarios.md)
- [Tax Saving and Legal Planning](references/tax-saving.md)
- [Tax Report Template](assets/tax-report-template.md)
- [ClawHub Skill Page](https://clawhub.ai/tsaitepiao-alt/skills/taiwan-real-estate-tax)
- [Publisher Profile](https://clawhub.ai/user/tsaitepiao-alt)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown reports, explanatory text, and shell commands for running the local calculator script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The calculator reads a JSON scenario file and writes a Markdown report to a user-selected output path.]

## Skill Version(s):

1.3.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Queries Amazon keyword search volume, purchase volume, purchase rate, and year-over-year, month-over-month, and three-month growth trends through Qinghu data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Amazon sellers and product researchers use this skill to assess keyword demand, conversion, and seasonal trends for a selected marketplace and month.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup or upgrades may install Node and qhkit or change the local shell environment.

Mitigation: Review installation commands before running them; prefer a preinstalled or pinned qhkit version.

Risk: The skill requires a Qinghu API token and paid lookups may incur variable credit charges.

Mitigation: Configure the token only with user approval, estimate costs first, and obtain consent before paid calls or larger batches.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/qinghu-amazon-keyword-trend)
- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)
- [Qinghu API keys](https://www.iqinghu.com/workbench/dashboard/api-keys?urlCode=1788417429126)

## Skill Output:

**Output Type(s):** [Analysis, Text, Files]

**Output Format:** [Markdown response with an optional table file for larger results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes marketplace and time period, supporting metrics, and credits spent when a paid call succeeds.]

## Skill Version(s):

0.1.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Home Reno Estimator helps an agent collect home area, renovation grade, and city, run a Python estimator, and produce a structured residential renovation cost estimate report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nic-yuan](https://clawhub.ai/user/nic-yuan)

### License/Terms of Use:

MIT-0

## Use Case:

External homeowners and agents assisting homeowners use this skill to estimate residential renovation budgets for Chinese cities and understand major cost drivers before seeking local quotes.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: Bundled business and marketing documents expand the package beyond a simple renovation estimate skill.

Mitigation: Review the extra documents before installation and remove materials that are not needed for the estimator use case.

Risk: The security evidence flags under-scoped shell execution and a vulnerable shell=True test helper.

Mitigation: Fix or remove the shell=True helper before running tests with any external input, and review shell commands before execution.

Risk: The evidence warns against automatic background update behavior for this package.

Mitigation: Keep the skill limited to explicit user estimation requests and do not enable unattended update jobs.

Risk: Collecting renovation details in public comments can expose home-related personal information.

Mitigation: Ask users to provide details in an appropriate private channel and collect only the area, renovation grade, and city needed for estimation.

Risk: The estimator produces reference ranges rather than a professional quote.

Mitigation: Present results as planning guidance and direct users to compare local contractor quotes before making budget or contract decisions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/nic-yuan/skills/vertical-home-reno-estimator)
- [Data Sources](artifact/references/data-sources.md)
- [Price Data and FAQ](artifact/references/price-data-2024.md)
- [Estimator Script](artifact/scripts/estimate.py)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown report with JSON estimator data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires area, renovation grade, and city; estimates are reference ranges and not binding quotes.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

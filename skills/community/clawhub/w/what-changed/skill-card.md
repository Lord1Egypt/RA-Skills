## Description:

What Changed explains material semantic differences between versions or snapshots and assesses why they matter for policies, procedures, contracts, requirements, datasets, configurations, APIs, schemas, reports, and other evolving artifacts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[raguets](https://clawhub.ai/user/raguets)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, and developers use this skill to compare versions of documents, policies, contracts, schemas, APIs, configurations, reports, or datasets and identify material semantic changes, likely impact, and follow-up actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Outputs may miss or misstate the impact of high-impact legal, financial, safety, or compliance changes if source context is incomplete.

Mitigation: Review change reports carefully in high-impact domains and confirm downstream obligations with the relevant accountable reviewers.

Risk: The skill may identify plausible affected artifacts or processes without evidence that those dependencies exist.

Mitigation: Treat unknown downstream impacts as potential until additional organizational context confirms them.

## Reference(s):

- [Change Severity Heuristics](references/change-severity.md)
- [Overpowered suite](https://github.com/raguets/overpowered)
- [ClawHub skill page](https://clawhub.ai/raguets/skills/what-changed)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown change-impact report with evidence locations and a short action list]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prioritizes semantic and impact changes over raw diffs; marks uncertain downstream impact as potential.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter metadata.version is 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Creates audience-specific QA test reports with traceable results, clear quality conclusions, and explicit risks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kokxi](https://clawhub.ai/user/kokxi)

### License/Terms of Use:

MIT-0

## Use Case:

QA teams and project leads use this skill to turn test execution and defect data into daily, weekly, iteration, or focused reports for developers, project managers, and leadership.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Release or delay recommendations could be mistaken for authorization to act.

Mitigation: Treat recommendations as report content and require authorized human review before business decisions.

Risk: The optional installation command fetches an external skill package.

Mitigation: Run it only after verifying and trusting the external package and its source.

## Reference(s):

- [Audience needs](artifact/references/audience-needs.md)
- [Report templates](artifact/assets/report-templates.md)
- [ClawHub skill release](https://clawhub.ai/kokxi/skills/qa-test-reporting)

## Skill Output:

**Output Type(s):** [Text, Markdown]

**Output Format:** [Markdown reports with summaries, metrics, conclusions, and risk sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Report IDs and source-linked test, defect, requirement, and risk IDs; summarizes existing data rather than producing test cases.]

## Skill Version(s):

1.8.0 (source: release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

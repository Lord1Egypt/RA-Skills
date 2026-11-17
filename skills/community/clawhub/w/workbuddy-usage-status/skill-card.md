## Description:

Creates an offline dashboard and data exports from a user's local WorkBuddy usage records.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clancy-feng](https://clawhub.ai/user/clancy-feng)

### License/Terms of Use:

MIT

## Use Case:

WorkBuddy users can review their own local token and credit usage, model costs, errors, and activity trends in an offline dashboard, then export the underlying data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Usage reports may be inaccurate.

Mitigation: Check reported totals against trusted WorkBuddy records before relying on them for decisions.

Risk: The security scan was partial; the chart library was not fully inspected and runtime permissions are unknown.

Mitigation: Review the package and the permissions requested by the host before running it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/clancy-feng/skills/workbuddy-usage-status)
- [Project page](https://github.com/clancy-feng/workbuddy-usage-status)
- [Metric and data guide](DATA-GUIDE.md)

## Skill Output:

**Output Type(s):** [Files, Analysis]

**Output Format:** [Offline HTML dashboard, CSV and XLSX exports, JSON and JavaScript data files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated data files may contain session titles and excerpts of user prompts; review before sharing.]

## Skill Version(s):

1.6.5 (source: frontmatter, CHANGELOG, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Helps QA teams select smoke, core, or full regression coverage based on release changes, risk, and available testing time.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kokxi](https://clawhub.ai/user/kokxi)

### License/Terms of Use:

MIT-0

## Use Case:

QA engineers and developers use this skill to prioritize regression cases for a release, plan execution within time limits, and identify areas left untested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The suggested unpinned package installation may add skills beyond this release.

Mitigation: Review the wider package and its version before running the installation command.

Risk: A proposed regression gate or time-limited case selection may overlook release-critical areas.

Mitigation: Disclose untested areas and confirm risk priorities and the release window with the project manager and developers before blocking a release.

## Reference(s):

- [Regression case selection strategies](references/regression-selection.md)
- [ClawHub skill release](https://clawhub.ai/kokxi/skills/qa-regression-testing)

## Skill Output:

**Output Type(s):** [Guidance, Markdown]

**Output Format:** [Markdown regression plan and selected case list]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preserves case IDs, labels regression tiers, and identifies uncovered risks.]

## Skill Version(s):

1.8.0 (source: frontmatter and server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

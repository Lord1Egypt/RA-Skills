## Description:

Classifies planting legends, parses plant schedules, and estimates paved area from landscape drawing candidates to prepare a budget and materials planning draft; it does not replace settlement.

This skill is for research and development only.

## Publisher:

[lisong2003-lgtm](https://clawhub.ai/user/lisong2003-lgtm)

### License/Terms of Use:

CC-BY-NC-SA-4.0

## Use Case:

Landscape designers, estimators, and project teams can use the skill for non-commercial preliminary plant quantities and paving-area estimates based on landscape drawing candidates, with confidence tiers and evidence coordinates, for budgeting and material planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan reports a mismatch between the stated landscaping quantity purpose and additional code-checking functionality, along with a flaw in a contract integrity check; its verdict has medium confidence.

Mitigation: Before installing, decide whether the reported purpose mismatch is acceptable and review the skill's code and dependency version.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/lisong2003-lgtm/skills/yuanlin-suanliang)
- [Usage guide](references/usage.md)
- [Input contract and boundaries](references/base-contract.md)
- [Plant library guide](references/plant-library.md)

## Skill Output:

**Output Type(s):** [CSV files, Excel spreadsheet, Markdown report]

**Output Format:** [CSV, XLSX, and Markdown files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preliminary quantities with confidence tiers and evidence coordinates; uncertain results are flagged for review and are not final measurements.]

## Skill Version(s):

0.4.40 (source: server-resolved release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

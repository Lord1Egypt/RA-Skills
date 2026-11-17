## Description:

Generates preliminary interior decoration quantity estimates and material plans from room information, finish specifications, and measurement inputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lisong2003-lgtm](https://clawhub.ai/user/lisong2003-lgtm)

### License/Terms of Use:

CC-BY-NC-SA-4.0

## Use Case:

Estimators and renovation teams use the skill to turn room schedules, finish specifications, and reviewed measurement inputs into preliminary decoration quantities and material purchase plans. They can inspect the assumptions and flagged gaps before relying on the results; the estimates do not replace settlement quantities or formal pricing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan marks this release suspicious with medium confidence, citing a mismatch between its estimating purpose and a bundled portability linter, along with concerns about dependency installation and validation safeguards.

Mitigation: Install only when there is a clear need; review the dependency installation behavior, validation limits, and linter before use, as ClawScan advises. The scan reports concerns, not proof of malicious authorship.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/lisong2003-lgtm/skills/zhuangshi-suanliang)
- [User guide and output details](artifact/README.md)
- [Contract and quantity rules](artifact/references/base-contract.md)
- [Usage and validation guidance](artifact/references/on-demand.md)
- [Waterproofing standards reference](artifact/references/waterproof-standards.md)

## Skill Output:

**Output Type(s):** [Files, CSV, XLSX, Markdown, JSON]

**Output Format:** [XLSX workbook, CSV tables, Markdown report, and JSON records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Separates estimate quantities from material procurement quantities and flags assumptions or missing information for review.]

## Skill Version(s):

0.9.36 (source: artifact/SKILL.md frontmatter, artifact/CHANGELOG.md, released 2026-11-10)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

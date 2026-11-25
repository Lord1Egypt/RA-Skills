## Description:

Counts landscape plants and estimates paved areas from CAD-reader candidates for preliminary budgeting; it does not replace settlement or formal measurement.

This skill is for research and development only.

## Publisher:

[lisong2003-lgtm](https://clawhub.ai/user/lisong2003-lgtm)

### License/Terms of Use:

CC-BY-NC-SA-4.0

## Use Case:

Landscape designers, estimators, and engineering teams use this skill to turn CAD-reader landscape candidates into plant counts, paving-area estimates, review items, and draft material plans. Outputs are preliminary and require manual review before project decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan flags weaknesses in how quantity results may be treated as eligible, a missing integrity check, and concerns about whether capabilities match their description.

Mitigation: Review quantity eligibility and input integrity checks before use, compare the described capabilities with the shipped behavior, and manually validate quantities before relying on them.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/lisong2003-lgtm/skills/yuanlin-suanliang)
- [English README](README.en.md)
- [Base contract reference](references/base-contract.md)
- [Usage reference](references/usage.md)
- [Plant library reference](references/plant-library.md)

## Skill Output:

**Output Type(s):** [CSV files, XLSX workbook, Markdown report, Review guidance]

**Output Format:** [CSV, XLSX, and Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes confidence tiers (P0–P3), evidence coordinates, and review items; estimates are preliminary drafts only.]

## Skill Version(s):

0.4.41 (source: SKILL.md frontmatter, CHANGELOG.md, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

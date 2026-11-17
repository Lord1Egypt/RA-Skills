## Description:

结构图出混凝土/钢筋估算；不替代翻样结算。触发词：土建算量、混凝土、钢筋。

This skill is for research and development only.

## Publisher:

[lisong2003-lgtm](https://clawhub.ai/user/lisong2003-lgtm)

### License/Terms of Use:

CC-BY-NC-SA-4.0

## Use Case:

Structural estimators and site engineers use this skill to prepare preliminary concrete-volume and rebar estimate bands by floor or pour zone for material planning. The documentation says these estimates do not replace bar detailing, settlement, or final measurement.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan marks this release suspicious with medium confidence, citing reported misleading or unsafe quantity-audit behavior and an unclear match between the declared purpose and reported behavior.

Mitigation: Review the declared purpose against the reported behavior, examine audit and evidence-handling concerns, and verify dependencies are pinned before installation.

Risk: The security scan is incomplete: 105 of 110 components were fully scanned, five were partially inspected, and two analyzers were degraded.

Mitigation: Treat the scan as incomplete and consider avoiding installation until the remaining concerns are reviewed and dependencies are pinned to verified versions.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/lisong2003-lgtm/skills/tujian-suanliang)
- [Quantity pipeline guide](references/on-demand.md)
- [Base contract requirements](references/base-contract.md)
- [Usage examples](references/usage-examples.md)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Files]

**Output Format:** [Quantity estimate reports and review records in JSON, CSV, and Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Planning estimates include review flags and missing-item notes; rebar results are estimate bands, not final takeoff quantities.]

## Skill Version(s):

0.9.44 (source: server-resolved release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

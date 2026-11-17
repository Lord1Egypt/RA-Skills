## Description:

从 CAD 识图契约生成施工总平面 A/B/C 候选、三阶段校核与 DXF/PNG 出图；不替代审批。

This skill is for research and development only.

## Publisher:

[lisong2003-lgtm](https://clawhub.ai/user/lisong2003-lgtm)

### License/Terms of Use:

CC BY-NC-SA 4.0

## Use Case:

施工项目总工及施工组织设计人员可用它把经过识图的场地资料整理为分阶段的平面布置草案、规则校核结果和图纸，供项目团队审核。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security verdict flags a possible source-drawing overwrite during export; scanner coverage was partial.

Mitigation: Keep source drawings read-only, work from a copy, direct exports to a separate directory, and inspect the resulting files.

Risk: The security summary also reports capability mismatches and weaknesses in safety-related reporting.

Mitigation: Check the documented capability limits and have qualified project staff independently verify placements, constraints, and safety conclusions.

## Reference(s):

- [Site planning rules and stages](references/site-plan.md)
- [A/B/C layout generation](references/generator.md)
- [Input preparation and unit checks](references/prepare.md)
- [ClawHub skill page](https://clawhub.ai/lisong2003-lgtm/skills/site-layout-plan)
- [Publisher profile](https://clawhub.ai/user/lisong2003-lgtm)

## Skill Output:

**Output Type(s):** [Files, Configuration, Guidance]

**Output Format:** [DXF and PNG drawings, JSON and CSV data, and Markdown summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Draft layouts and checks; outputs require project expert review and do not replace approvals.]

## Skill Version(s):

0.7.3 (source: server-resolved release evidence, CHANGELOG.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

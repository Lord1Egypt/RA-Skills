## Description:

Generate, audit, and trace verification criteria for functional system requirements using VC generation, VC quality audit, and coverage audit workflows aligned with ASPICE SYS.2 BP5, ISO/IEC 29148, and VC-First methodology.

This skill is ready for commercial/non-commercial use.

## Publisher:

[unknowcao](https://clawhub.ai/user/unknowcao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and requirements engineers use this skill to generate testable verification criteria, audit existing VCs against SMARTR-OC and checklist rules, and build requirement-to-VC coverage reports for functional system requirements.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent may read requirement and VC documents and create split or merged output files in the workspace.

Mitigation: Confirm input scope and output paths before generation, and review generated files before using them downstream.

Risk: Generated verification criteria for safety-critical systems may be incomplete, incorrect, or based on assumptions.

Mitigation: Have qualified engineers review generated VCs, Source Depth tags, SMARTR-OC scores, and coverage reports before relying on them.

Risk: Large-batch workflows can use subagents and produce intermediate batch files.

Mitigation: Use bounded batches, prefer incremental updates when existing VC files are detected, and inspect merge statistics and coverage findings.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/unknowcao/skills/verification-criteria)
- [Server-resolved GitHub source](https://github.com/UnknowCao/autoskill-hub/tree/main/skills/verification-criteria)
- [README](README.md)
- [VC Definition Framework & Methodology Reference](references/vc-framework.md)
- [Workflow A - VC Generation](references/vc-workflow-a.md)
- [Workflow B - VC Quality Audit](references/vc-workflow-b.md)
- [Workflow C - Coverage Audit](references/vc-workflow-c.md)
- [VC Output Format Specification](references/vc-output-format.md)
- [SMARTR-OC 8-Point Scoring Rubric](references/vc-smartr-oc.md)
- [VC Source Depth Annotation System](references/vc-source-depth.md)
- [VC Quality Checklist](assets/vc-checklist.md)
- [VC Safety Patterns](references/vc-safety-patterns.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Analysis, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown reports and tables, with optional JSON statistics from merge tooling]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create split requirement batches, merged VC documents, coverage matrices, and stats files in the workspace.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

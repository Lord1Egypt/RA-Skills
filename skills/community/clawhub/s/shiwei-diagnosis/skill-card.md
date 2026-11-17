## Description:

施炜诊断方法论 guides agents through enterprise management diagnosis using company materials, interviews, surveys, and structured strategy, organization, talent, culture, leadership, and financial analysis frameworks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tuobadaidai](https://clawhub.ai/user/tuobadaidai)

### License/Terms of Use:

MIT-0

## Use Case:

Consultants and business analysts use this skill to assess enterprise growth stage, organizational capability, strategy and operations issues, talent, culture, leadership, and financial signals from provided company materials. The skill helps produce a structured diagnosis Markdown document for review and can guide follow-on PPT generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PPT generation scripts are flagged as unsafe or mismatched for normal installation.

Mitigation: Review or fix the scripts before installation or execution, and require explicit input and output paths for generated decks.

Risk: Shell execution in the artifact scripts can increase command execution risk.

Mitigation: Replace shell-based execution with argument-array APIs such as execFileSync or spawnSync before production use.

Risk: The skill may process sensitive company interviews, questionnaires, financial data, or leadership materials.

Mitigation: Establish clear user consent, confidentiality handling, and data minimization rules before using the skill with company materials.

Risk: Unpinned runtime dependencies can make PPT generation behavior drift over time.

Mitigation: Pin Node.js dependencies with a lockfile and review dependency updates before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tuobadaidai/skills/shiwei-diagnosis)
- [Publisher profile](https://clawhub.ai/user/tuobadaidai)
- [Diagnosis framework](references/diagnosis-framework.md)
- [Diagnosis Markdown template](references/md-template.md)
- [PPT structure specification](references/ppt-structure.md)

## Skill Output:

**Output Type(s):** [Guidance, Analysis, Markdown, Code, Shell commands]

**Output Format:** [Markdown guidance with optional JavaScript and shell command references for PPT generation and audit]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces diagnosis documents from user-provided business evidence; PPT generation scripts should be reviewed and adapted before execution.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

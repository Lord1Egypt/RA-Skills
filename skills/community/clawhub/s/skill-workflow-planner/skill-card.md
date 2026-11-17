## Description:

Helps users create an ordered written plan for using several OpenClaw skills, including dependency order, approval checkpoints, and simple verification notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pmuhammadagus-byte](https://clawhub.ai/user/pmuhammadagus-byte)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw users use this skill when they explicitly need to plan the sequence of multiple skills before acting. It produces a concise workflow plan that identifies dependencies, high-risk steps that need approval, and verification checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A written plan may include steps involving credentials, destructive changes, installs, or system modifications.

Mitigation: Review the plan before execution and require explicit user approval for any high-risk step.

Risk: A workflow plan can be incorrect if the environment, dependencies, or skill compatibility are not verified.

Mitigation: Confirm platform details, required tools, and success checks before carrying out the planned steps.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pmuhammadagus-byte/skills/skill-workflow-planner)
- [Publisher profile](https://clawhub.ai/user/pmuhammadagus-byte)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown plan with ordered steps, approval markers, and verification notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Planning-only output; it does not install code, run tools, or execute workflow steps by itself.]

## Skill Version(s):

1.1.4 (source: frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

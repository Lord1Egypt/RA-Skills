## Description:

Self Reflection Loop helps an agent assess, validate, and iteratively refine outputs with rubrics, tool-anchored checks, scores, gap analysis, and improvement checklists.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qq435912743](https://clawhub.ai/user/qq435912743)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and agent builders use this skill when they need structured self-correction, iterative refinement, code self-validation, or quality gating for generated artifacts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The automatic refinement path can run arbitrary shell commands through the refinement command template.

Mitigation: Use the skill only in a sandboxed workspace and avoid --refine-cmd unless the artifact, rubric, and command template are trusted.

Risk: The learning module stores reusable preferences and notes in persistent local JSON without strong controls.

Mitigation: Do not store secrets, credentials, sensitive user information, or confidential project details in preferences or notes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qq435912743/skills/self-reflection-loop)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, JSON rubrics and logs, inline shell commands, and guidance text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create rubric, assessment report, reflection log, and learned-pattern JSON files during use.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

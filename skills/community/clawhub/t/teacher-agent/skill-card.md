## Description:

Designs prerequisite-based curricula and teaches complex concepts through layered explanations, Mermaid diagrams, and student feedback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[marsanatta](https://clawhub.ai/user/marsanatta)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use the skill to learn complex technical topics, understand agent output, and build prerequisite-based courses with progressive explanations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment reports that cleanup instructions can forcibly stop unrelated Python processes and interrupt other work.

Mitigation: Avoid broad Python process cleanup; stop only the HTTP server instance started for diagram rendering, and review the affected command before running it.

Risk: Security review coverage is partial: Skillspector fully inspected only 1 of 3 components, so the evidence does not establish that other risks are absent.

Mitigation: Review all three artifact files and inspect commands before execution; treat the scan as incomplete.

## Reference(s):

- [ClawHub release](https://clawhub.ai/marsanatta/skills/teacher-agent)
- [Publisher profile](https://clawhub.ai/user/marsanatta)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Mermaid diagrams]

**Output Format:** [Progressive explanations and curricula in text or Markdown, with Mermaid diagrams where useful.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Delivered in layers with Socratic checkpoints and optional course tracking.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

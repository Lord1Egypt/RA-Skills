## Description:

SharpAgent Self-Evolving Loop guides agents through a Think-Do-Learn cycle that reflects after tasks, forms testable improvement hypotheses, runs small experiments, and records lessons as learning entries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yezhaowang888-stack](https://clawhub.ai/user/yezhaowang888-stack)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to add a structured reflection, hypothesis, experiment, and learning-entry loop after agent tasks. It is intended for workflows where task lessons may improve future agent behavior over time.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks an agent to retain task-derived lessons and use them to change future behavior without clear user control.

Mitigation: Require explicit review before creating or adopting LearningEntry records, template writes, monitor updates, lifecycle updates, or preference-profile changes.

Risk: Task reflections and retained lessons may include sensitive or client-specific information.

Mitigation: Redact sensitive details from learning entries and avoid long-term retention for confidential tasks.

Risk: Weak experiments or unsupported hypotheses could promote incorrect practices into future workflows.

Mitigation: Adopt only changes with clear metrics and keep failed or unverifiable hypotheses recorded as non-adopted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yezhaowang888-stack/skills/sharpagent-self-evolving)
- [ClawHub publisher profile](https://clawhub.ai/user/yezhaowang888-stack)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown with structured text, YAML, and JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce reflection notes, improvement hypotheses, experiment plans, and LearningEntry-style records.]

## Skill Version(s):

1.0.0 (source: evidence.release.version and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Probe and evaluate teacher models to map capability boundaries, failure modes, and confidence for cross-model distillation workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qq435912743](https://clawhub.ai/user/qq435912743)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill before or after distillation to generate teacher capability probes, evaluate pass/partial/fail results, and identify weak boundaries and failure modes. It can also support teacher selection by comparing structured capability profiles.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The self-learning module stores local history, notes, error details, and arbitrary user preferences beyond the core probe workflow.

Mitigation: Install only after reviewing the persistence behavior; scope or remove learner.py when persistent memory is not required, and document retention and deletion expectations.

Risk: Stored preferences and notes may contain sensitive task context if users pass it to the learning commands.

Mitigation: Avoid recording sensitive data in notes or preferences, validate preference keys and values, and periodically inspect or clear learned_patterns.json.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qq435912743/skills/teacher-capability-probe)
- [Publisher profile](https://clawhub.ai/user/qq435912743)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON probe or evaluation reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Probe reports include coverage, failure modes, confidence, weak boundaries, and per-probe records.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

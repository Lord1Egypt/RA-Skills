## Description:

Multi-skill workflow orchestrator that chains skills into automated pipelines from natural-language requests, with conditional branching and error handling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openlark](https://clawhub.ai/user/openlark)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to coordinate multi-step workflows that parse user intent, invoke sub-skills in sequence, branch conditionally, and handle failures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Coordinated workflows may trigger externally visible or state-changing downstream actions such as sending messages, publishing content, saving data, or reminders.

Mitigation: Confirm each externally visible or state-changing step with the user and verify which downstream skill will perform it before execution.

Risk: Workflow quality and safety depend on the behavior and current validity of downstream skills selected for each step.

Mitigation: Check downstream skill identity, permissions, and current version before allowing a workflow to proceed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/openlark/skills/skill-workflow-orchestrator)

## Skill Output:

**Output Type(s):** [guidance, configuration, code]

**Output Format:** [Markdown with JSON workflow examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include structured step lists, conditional branches, retry settings, and fallback handling.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

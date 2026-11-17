## Description:

When throughput or latency is pipeline-limited, identify the single binding constraint and exploit, subordinate, elevate, then recheck; ignore non-constraints.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tjboudreaux](https://clawhub.ai/user/tjboudreaux)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and process owners use this skill to analyze pipeline-limited systems, identify the current binding constraint with evidence, and choose the next improvement step.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Theory of Constraints framing may be applied to work that is not constrained by a single stable bottleneck.

Mitigation: Use the skill's explicit checks for measured utilization, queues, and stage rates; exit to another analysis method when no single stage binds.

Risk: Optimizing non-constraint stages can increase work in progress without improving end-to-end throughput or latency.

Mitigation: Subordinate non-constraints to the identified constraint and remeasure after each exploit or elevation step.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tjboudreaux/skills/thinking-theory-of-constraints)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown guidance with a structured text output template]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No code execution, external tool use, or sensitive access requested by the artifact.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Source Router helps an LLM choose an ordered search plan across web, local file, vector, graph, and counter-evidence sources based on task type, freshness needs, and known information gaps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[z1one0415](https://clawhub.ai/user/z1one0415)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use Source Router when they need a structured plan for which information sources to check, in what order, when to include counter-evidence, and when to stop. It is suited to multi-source research planning and search budget control.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local file and cache recommendations may point an agent toward sensitive workspace content.

Mitigation: Review proposed local_file and local_cache search hints before use in sensitive workspaces, and restrict available sources when local context should not be consulted.

Risk: A counter-evidence schema mismatch may prevent evaluation or investigation tasks from triggering the intended adversarial search planning.

Mitigation: Review and fix the counter-evidence trigger schema before relying on the skill for evaluation or investigation workflows.

## Reference(s):

- [Source Router Skill Page](https://clawhub.ai/z1one0415/skills/source-router)
- [Source Selection Rules](references/source-selection-rules.md)
- [Source Router Examples](references/examples.md)

## Skill Output:

**Output Type(s):** [Guidance, Analysis, Configuration]

**Output Format:** [JSON search routing plan]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces source priorities, search order, budget allocation, fallback chain, stop rule, and degradation log fields; it does not execute searches.]

## Skill Version(s):

2.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

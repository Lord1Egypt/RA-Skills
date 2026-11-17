## Description:

Design and run iterative generate→critique→revise loops optimized for Claude Opus 4.8, with thinking-as-critic, cost controls, and model routing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[prometheus-prime](https://clawhub.ai/user/prometheus-prime)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI practitioners use this skill to design bounded refinement loops for writing, prompt, and structured-output tasks where a first pass is not good enough and improvement can be measured with explicit criteria.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Repeated refinement-loop model calls can consume tokens quickly.

Mitigation: Set hard cost, token, and iteration limits before running the loop, and abort to the best candidate when a budget is reached.

Risk: Weak or vague critique can cause loop churn without meaningful improvement.

Mitigation: Use explicit rubrics, objective checks where available, convergence detection, and keep-best tracking.

## Reference(s):

- [ClawHub skill release page](https://clawhub.ai/prometheus-prime/skills/refinement-loop)
- [Prometheus-Prime publisher profile](https://clawhub.ai/user/prometheus-prime)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Configuration instructions]

**Output Format:** [Markdown with prompt templates, rubric guidance, and Python-like pseudocode]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should preserve explicit iteration caps, cost budgets, convergence checks, and keep-best tracking.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

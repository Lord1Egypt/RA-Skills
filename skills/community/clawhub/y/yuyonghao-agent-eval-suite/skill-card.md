## Description:

Provides benchmark testing, A/B testing, performance regression detection, and simulation environment testing for agent evaluation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuyonghao-123](https://clawhub.ai/user/yuyonghao-123)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to evaluate agent behavior with repeatable benchmarks, A/B experiments, regression checks, simulations, and generated reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: HTML report generation can include caller-provided titles, metric names, and result data.

Mitigation: Use trusted report inputs or escape and sanitize fields before generating HTML output.

Risk: Simulator scenario loading accepts caller-provided absolute paths.

Mitigation: Pass only trusted scenario names or paths, and restrict scenario directories in agent workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yuyonghao-123/skills/yuyonghao-agent-eval-suite)

## Skill Output:

**Output Type(s):** [Code, Configuration instructions, Shell commands, Markdown, Guidance]

**Output Format:** [Markdown with JavaScript and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill package can produce JSON, Markdown, or HTML evaluation reports when used as a local Node.js library.]

## Skill Version(s):

0.1.0 (source: evidence release and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

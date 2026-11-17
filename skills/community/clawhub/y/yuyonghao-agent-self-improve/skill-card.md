## Description:

Analyzes agent performance and suggests prompt, parameter, workflow, and strategy optimizations for agent self-improvement.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuyonghao-123](https://clawhub.ai/user/yuyonghao-123)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to profile agent task execution, identify timing, resource, reliability, and hotspot issues, and compare optimization strategies. It is suited for local evaluation workflows where repeated task execution is acceptable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The profiler repeatedly executes the function supplied by the caller, which can cause unwanted side effects or excessive cost when the target task is not idempotent.

Mitigation: Profile only safe, bounded, and repeatable tasks; lower iteration counts and timeouts for expensive or state-changing operations.

Risk: Package metadata claims code self-rewriting, but the security review reports no reviewed code-rewriting implementation.

Mitigation: Treat self-rewriting claims as unsupported for this release and review any generated improvement proposal before applying it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yuyonghao-123/skills/yuyonghao-agent-self-improve)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JavaScript examples and JSON-like analysis results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Profiles include timing, memory, CPU, bottleneck, hotspot, outlier, recommendation, and optimization result fields.]

## Skill Version(s):

0.1.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

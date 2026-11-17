## Description:

Zouroboros Swarm Gate is a zero-cost task classifier that uses seven weighted signals to decide whether a task needs multi-agent orchestration without making API calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[marlandoj](https://clawhub.ai/user/marlandoj)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to evaluate a task description before execution and decide whether it should run directly, be suggested for orchestration, or escalate to a multi-agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unpinned package installation can introduce ordinary supply-chain drift between review and deployment.

Mitigation: Install a pinned package version or use a lockfile-managed dependency, and review the packaged source before deployment.

Risk: Heuristic routing can misclassify tasks; wording such as 'just', 'quick', or 'simple' can lower the orchestration score.

Mitigation: Treat the result as routing advice, review boundary cases, and tune thresholds or overrides for the receiving workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/marlandoj/skills/zouroboros-swarm-gate)
- [OpenClaw distribution homepage](https://github.com/AlaricHQ/zouroboros-openclaw)
- [Runnable starter example](https://github.com/AlaricHQ/zouroboros-openclaw-examples/tree/main/examples/swarm-gate)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [Plain text or JSON classification with decision, score, signal breakdown, reason, and optional routing directive]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [CLI exit code indicates the routing decision when the skill is used from the command line.]

## Skill Version(s):

1.0.0 (source: frontmatter and ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

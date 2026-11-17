## Description:

Signal Intelligence Pack turns an information-dependent task into an enhanced evidence base by planning queries, routing sources, cleaning evidence, judging freshness, and looking for counter-evidence before downstream analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[z1one0415](https://clawhub.ai/user/z1one0415)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, research agents, and analysts use this skill to prepare a grounded evidence base for strategic analysis, market or policy research, financial and news intelligence, and other time-sensitive tasks that require multiple sources and counter-evidence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow may increase search or tool usage and expose search queries to configured external search providers.

Mitigation: Use it for tasks that need web grounding, review configured sources before execution, and avoid local-only or privacy-sensitive tasks unless external search is approved.

Risk: The evidence base can still be misleading when evidence is stale, sparse, single-sided, or affected by unresolved gaps.

Mitigation: Review freshness labels, critical gaps, counter-evidence, pending actions, and confidence assessment before relying on downstream conclusions.

Risk: Source failures, quota exhaustion, or backtracking limits can leave parts of the research pipeline degraded.

Mitigation: Check degradation logs and pending actions, then rerun targeted searches or supplement sources when required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/z1one0415/skills/signal-intelligence-pack)
- [Workflow](references/workflow.md)
- [Input and output schema](references/input-output.md)
- [Stop rules and quality gates](references/stop-rules.md)
- [Examples](references/examples.md)
- [Improvement plan V2](references/improvement-plan-v2.md)

## Skill Output:

**Output Type(s):** [JSON, Guidance]

**Output Format:** [Structured JSON evidence base with query plans, source routing, cleaned evidence, freshness labels, counter-evidence, gaps, and confidence assessment]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include pipeline metadata, pending actions, degradation logs, and confidence scoring.]

## Skill Version(s):

2.1.0 (source: server evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

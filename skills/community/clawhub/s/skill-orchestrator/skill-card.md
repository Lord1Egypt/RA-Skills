## Description:

Multi-skill orchestrator: decompose complex asks, discover skills, plan parallel/serial steps, checkpoints, merge outputs; optional JSON bundle for hosts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[windymonkeys](https://clawhub.ai/user/windymonkeys)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to coordinate complex requests across multiple domains by decomposing work, selecting relevant skills, sequencing or parallelizing steps, checkpointing risky decisions, and merging results into a final report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can coordinate other skills, including workflows that may touch files, deployments, APIs, payments, personal data, or third-party skills.

Mitigation: Require explicit human confirmation before orchestration steps that involve those actions, especially when direct execution or bypassPermissions is requested.

Risk: The skill may scan local skill registries and use brief orchestration history.

Mitigation: Install only in environments where reading the declared skill and memory paths is acceptable, and keep orchestration history limited to brief summaries without secrets or sensitive business content.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/windymonkeys/skills/skill-orchestrator)
- [Homepage](https://github.com/Windymonkeys/skill-orchestrator)
- [Machine Contract](references/machine-contract.md)
- [Skill Registry](references/skill-registry.md)
- [Orchestration Engine](references/orchestration-engine.md)
- [Execution Tracker](references/execution-tracker.md)
- [Result Merger](references/result-merger.md)
- [Human-in-the-Loop](references/human-in-the-loop.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, JSON, Shell commands, Configuration]

**Output Format:** [Markdown report with optional JSON bundles and inline command or configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include plan, event, and merge JSON bundles for host or script integration.]

## Skill Version(s):

2.0.2 (source: server release metadata; artifact frontmatter states 2.0.3)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

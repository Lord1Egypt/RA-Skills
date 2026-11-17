## Description:

Build a goal-driven self-learning loop for OpenClaw and coding agents that diagnoses capability gaps, maintains a capability map and learning agenda, generates training units, evaluates progress, validates transfer, and promotes only proven strategies into long-term behavior.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rangeking](https://clawhub.ai/user/rangeking)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to help OpenClaw and coding agents turn mistakes, near misses, and difficult work into structured capability diagnosis, training, evaluation, and promotion decisions. It is intended for agents that need persistent learning behavior across sessions while keeping durable guidance gated by evidence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent memory and promoted lessons can affect future agent behavior.

Mitigation: Review proposed changes to long-term instruction and memory files before accepting them, especially promotion decisions.

Risk: Untrusted task output could be copied into durable guidance.

Mitigation: Avoid promoting lessons copied from untrusted output; require training evidence, transfer validation, and human review before durable promotion.

Risk: Hooks and scripts can change startup behavior or workspace state.

Mitigation: Enable hooks and run scripts only from pinned or reviewed revisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rangeking/skills/self-evo-agent)
- [README](artifact/README.md)
- [Skill definition](artifact/SKILL.md)
- [Coordinator workflow](artifact/system/coordinator.md)
- [Capability map module](artifact/modules/capability-map.md)
- [Learning agenda module](artifact/modules/learning-agenda.md)
- [Evaluator module](artifact/modules/evaluator.md)
- [Promotion module](artifact/modules/promotion.md)
- [Benchmark suite](artifact/benchmarks/suite.json)
- [Upstream self-improving-agent reference](https://github.com/peterskoett/self-improving-agent)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, structured ledger entries, shell commands, configuration snippets, and code-oriented workspace artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update persistent memory, capability, training, evaluation, and promotion artifacts in the agent workspace.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

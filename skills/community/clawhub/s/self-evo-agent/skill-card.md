## Description: <br>
Build a goal-driven self-learning loop for OpenClaw and coding agents. Use when the agent should not only log mistakes, but diagnose capability gaps, maintain a capability map and learning agenda, generate training units, evaluate progress, validate transfer, and promote only proven strategies into long-term behavior. Also use before major tasks to retrieve relevant learnings, inspect capability risks, and choose safer execution strategies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[RangeKing](https://clawhub.ai/user/RangeKing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to add a persistent capability-evolution loop to OpenClaw or coding agents. It helps agents review prior learnings, diagnose capability gaps, maintain a learning agenda, create training units, evaluate progress, and promote only validated strategies. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can record task details, code context, or lessons into local workspace memory artifacts. <br>
Mitigation: Use it only in workspaces where persistent local learning notes are acceptable, and periodically review generated learning, capability, training, and evaluation files. <br>
Risk: Recorded learnings or promoted strategies may become stale or misleading if they are not reviewed. <br>
Mitigation: Keep promotion evidence-based, use the evaluation and transfer checks before durable promotion, and prune or revise local memory when project assumptions change. <br>
Risk: Optional hooks and helper scripts modify local agent workflow files and workspace ledgers. <br>
Mitigation: Inspect installed files before enabling hooks or running scripts, and avoid enabling the skill in repositories where local workflow changes are not desired. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/RangeKing/self-evo-agent) <br>
- [SKILL.md](SKILL.md) <br>
- [README.md](README.md) <br>
- [Installation guide](install.md) <br>
- [Coordinator workflow](system/coordinator.md) <br>
- [Capability map module](modules/capability-map.md) <br>
- [Learning agenda module](modules/learning-agenda.md) <br>
- [Evaluator module](modules/evaluator.md) <br>
- [Promotion module](modules/promotion.md) <br>
- [Security policy](SECURITY.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with structured ledger entries, shell commands, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local learning, error, capability, training, and evaluation notes in the agent workspace when the workflow is active.] <br>

## Skill Version(s): <br>
1.1.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

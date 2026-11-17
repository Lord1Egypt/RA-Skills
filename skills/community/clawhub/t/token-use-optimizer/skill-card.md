## Description:

Token Use Optimizer helps agents audit and reduce token overhead in AI-agent projects using a four-layer diagnostic workflow for rules, memory, knowledge, and runtime behavior plus a local audit script.

This skill is ready for commercial/non-commercial use.

## Publisher:

[louisecxqiu-glitch](https://clawhub.ai/user/louisecxqiu-glitch)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent maintainers use this skill to establish a token-cost baseline, diagnose always-on context overhead, and plan scoped reductions to rules, memory, knowledge files, and runtime behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optimization advice may recommend deleting, merging, or downgrading rules, memory, or knowledge entries that still affect desired agent behavior.

Mitigation: Review proposed changes before applying them, keep a baseline for comparison, and verify requestable triggers after any rule downgrade.

Risk: The audit script reads local agent project configuration and knowledge files to estimate token overhead.

Mitigation: Run it only against intended local project directories and review generated reports before sharing them outside the project.

## Reference(s):

- [Optimization Strategies](references/optimization-strategies.md)
- [Real-World Cases](references/real-world-cases.md)
- [ClawHub Skill Page](https://clawhub.ai/louisecxqiu-glitch/skills/token-use-optimizer)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, code]

**Output Format:** [Markdown guidance with inline shell commands and optional JSON output from the audit script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled audit script estimates fixed token overhead from local project files and can emit a JSON report.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

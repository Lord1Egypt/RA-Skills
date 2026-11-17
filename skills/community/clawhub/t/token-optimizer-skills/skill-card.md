## Description:

Full token economy suite for OpenClaw agents. Audits context window usage (skills, history, tool outputs), then applies 5 creative strategies to reduce bloat without losing memory quality.

This skill is ready for commercial/non-commercial use.

## Publisher:

[legiovi](https://clawhub.ai/user/legiovi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to audit context-window usage, identify token bloat, run token-counting helper scripts, and apply token-reduction strategies such as memory distillation, skill lazy loading, model-specific prompt restructuring, and offline document compression.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release includes dispatcher and memory-agent files beyond SKILL.md, including configurable script execution.

Mitigation: Review all shipped Python and configuration files before installation, restrict script and file paths to trusted directories, and run the skill in a constrained workspace.

Risk: Automatic memory distillation and flush behavior can persist incomplete or inaccurate facts.

Mitigation: Disable automatic distillation and flush by default, and require user review before episodic-store writes or memory_write operations.

Risk: Optional prompt compression can alter important content if used on live prompts, tool schemas, configuration, or code.

Mitigation: Use prompt compression only for offline document experiments, require dry-run preview first, and avoid live system prompts, tool schemas, JSON configuration, and code.

Risk: Dependency-backed tokenizer and compression behavior may change with installed package or model revisions.

Mitigation: Pin dependencies and model revisions, and keep the zero-dependency estimate path available for basic budgeting.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/legiovi/skills/token-optimizer-skills)
- [README](README.md)
- [Gemma Model Optimization Strategies](gemma-optimization.md)
- [Memory Persistence Patterns](memory-persistence-patterns.md)
- [Token Audit Skill](token_audit.md)
- [Token Optimizer Skill](token_optimizer_strategies.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown reports, JSON memory facts, Python script output, shell commands, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Token counts may use tokenizer libraries when installed or a zero-dependency estimate fallback; memory distillation output should be reviewed before use as authoritative memory.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

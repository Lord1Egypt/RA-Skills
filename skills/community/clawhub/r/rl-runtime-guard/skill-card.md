## Description:

Soft, opt-in runtime guardrails for AI agents that inject advisory reminders before requests when they detect complex tasks, retry loops, long commands, or platform path mismatches.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huanmeng9527](https://clawhub.ai/user/huanmeng9527)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to add advisory runtime reminders that help an agent break down long tasks, notice retry loops, and avoid platform-specific path mistakes. It is intended as a first line of defense before review or enforcement layers, not as a blocking control.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The guard can inject system-priority instructions that redirect agent behavior when heuristics trigger.

Mitigation: Review the bundled prompts and threshold settings before deployment; install only where this advisory behavior is desired.

Risk: Chinese-only injected prompts may be hard for some operators to review or monitor.

Mitigation: Translate and review the prompt text before production use, or disable the guard until operators can validate the behavior.

Risk: Threshold defaults may cause false positives, missed retry loops, or extra prompt tokens in environments unlike the original workstation setting.

Mitigation: Tune thresholds with the documented configuration files and audit decision rates before broad rollout.

Risk: Audit logging creates local metadata logs when explicitly enabled.

Mitigation: Keep audit logging disabled unless telemetry is needed, and restrict file permissions for any configured audit log path.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/huanmeng9527/skills/rl-runtime-guard)
- [Threshold Tuning Guide](references/thresholds.md)
- [Disable rl-runtime-guard](references/disabling.md)
- [Audit Log](references/audit-log.md)
- [Minimal Configuration](examples/config-minimal.json)
- [Strict Configuration](examples/config-strict.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON configuration examples, and ESM handler code references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces advisory prompt augmentation when heuristics trigger; it does not block requests or modify tool output.]

## Skill Version(s):

1.0.7 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

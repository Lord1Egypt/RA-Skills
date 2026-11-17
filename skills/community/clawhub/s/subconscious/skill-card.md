## Description:

Subconscious is a bounded, governed self-improvement layer for OpenClaw agents that turns trusted local learning notes into persistent, session-scoped behavioral biases.

This skill is ready for commercial/non-commercial use.

## Publisher:

[elyasdruid](https://clawhub.ai/user/elyasdruid)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to maintain a bounded self-improvement memory layer that scans trusted learning files, promotes eligible lessons through governance gates, and surfaces a small set of active behavioral biases to agent sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recurring background jobs can turn local learning notes into persistent prompt-shaping behavior without enough prior control.

Mitigation: Install only when a long-lived self-improvement system is desired, review cron entries before running install.sh, and disable --enable-promotion unless automatic promotion is intended.

Risk: Untrusted or secret-bearing .learnings content can influence future agent sessions.

Mitigation: Keep .learnings content trusted and non-secret, and review learning files before allowing them to feed the bridge.

Risk: Manual cron instructions can overwrite or disrupt existing scheduled jobs if applied carelessly.

Mitigation: Back up the current crontab before following manual cron instructions and review generated entries after installation.

## Reference(s):

- [Subconscious ClawHub Release](https://clawhub.ai/elyasdruid/skills/subconscious)
- [Architecture Reference](references/ARCHITECTURE.md)
- [Installation Guide](references/INSTALL.md)
- [Learnings Bridge Wiring](references/WIRING.md)
- [Self-Improving Agent OpenClaw Integration](self-improving-agent/references/openclaw-integration.md)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with command examples and local text outputs from CLI tools]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can create or update local memory files, cron entries, logs, snapshots, and session bias text when installed and run.]

## Skill Version(s):

1.8.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

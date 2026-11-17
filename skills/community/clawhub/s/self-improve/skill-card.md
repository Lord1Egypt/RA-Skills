## Description:

A pluggable self-improvement framework for AI agents that learns from mistakes, corrections, and feedback, runs every 3 days by Cron, extracts reusable experience rules, and proposes system-file improvements through an approval workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[don068589](https://clawhub.ai/user/don068589)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use Self-Improve to collect feedback and memory-log signals, distill reusable execution rules, and queue approved improvements for shared agent system files and knowledge stores.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The recurring cron workflow can read and aggregate agent memories and logs into shared storage.

Mitigation: Approve the cron entry only for explicitly approved workspace_root paths, restrict shared storage access, and apply redaction and retention controls before broad use.

Risk: Unsafe file write/delete utilities and path handling can be risky when exposed to untrusted input or automation.

Mitigation: Fix the path traversal issues identified by the security guidance, run only with trusted configuration, and constrain filesystem permissions until the fixes are in place.

Risk: Proposed system-file changes can introduce incorrect or misleading agent guidance.

Mitigation: Keep the approval workflow for AGENTS.md, SOUL.md, TOOLS.md, MEMORY.md, HEARTBEAT.md, openclaw.json, and SKILL.md changes, and review proposals before applying them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/don068589/skills/self-improve)
- [Self-Improve Framework](artifact/SKILL.md)
- [Self-Improve System Documentation](artifact/SYSTEM.md)
- [Self-Improve Engine](artifact/ENGINE.md)
- [Self-Improve Runtime Mechanism](artifact/RUNTIME.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, configuration examples, generated proposal files, and agent memory or knowledge-base text files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs as a scheduled or manually triggered workflow and writes proposals, feedback records, memory tiers, reports, and setup configuration according to user-approved paths.]

## Skill Version(s):

2.2.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

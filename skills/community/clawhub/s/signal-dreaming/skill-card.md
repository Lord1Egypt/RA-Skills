## Description: <br>
Signal Dreaming consolidates OpenClaw session logs into long-term memory by prioritizing entries with higher recall-frequency signals and writing a human-readable dream diary. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lzyling](https://clawhub.ai/user/lzyling) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to run manual or scheduled memory consolidation that promotes frequently recalled session notes into durable topic files while preserving daily logs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads and updates persistent workspace memory, so sensitive or stale session content could be promoted into curated memory if the plan is not reviewed. <br>
Mitigation: Review the planned files before write phases, keep the Sense phase read-only, redact credential-like content, and use the provided lightweight audit helper after writes. <br>
Risk: Unattended daily cron automation can run in workspaces whose memory logs contain personal, business, or credential-adjacent information. <br>
Mitigation: Prefer explicit invocations until the workspace behavior is understood, and enable cron only for workspaces where scheduled memory maintenance is intended. <br>
Risk: The workflow modifies MEMORY.md, dream-log.md, and L2 topic files during consolidation. <br>
Mitigation: Back up existing files outside memory indexing under .backup/memory-dreams before rewriting them, and preserve daily logs unchanged. <br>


## Reference(s): <br>
- [Signal Dreaming on ClawHub](https://clawhub.ai/lzyling/signal-dreaming) <br>
- [Memory Dreaming Full Protocol](references/dream-protocol.md) <br>
- [Dream Audit Helper](references/dream-audit.sh) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with optional JSON configuration and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update workspace memory files and produce a one-line dream summary when invoked by an agent.] <br>

## Skill Version(s): <br>
1.3.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

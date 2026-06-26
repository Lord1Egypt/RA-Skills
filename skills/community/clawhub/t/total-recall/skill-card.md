## Description: <br>
Total Recall gives OpenClaw agents autonomous cross-session memory by observing conversation transcripts, compressing durable facts into Markdown memory files, consolidating them, and recovering missed context across resets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gavdalf](https://clawhub.ai/user/gavdalf) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and external OpenClaw users use this skill to preserve useful agent memory across sessions, compaction, and manual resets. It is suited for users who want file-based observations, scheduled consolidation, and optional background capture without running a vector database. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Conversation transcripts and durable facts may be read, stored on disk, and sent to the configured LLM provider. <br>
Mitigation: Use the skill only where autonomous memory is intended, prefer a local or trusted LLM endpoint for private work, and review memory files regularly. <br>
Risk: Background watcher, cron, and compaction hooks can run without an explicit manual command each time. <br>
Mitigation: Enable automation gradually, keep Dream Cycle in READ_ONLY_MODE=true during initial review, and defer watcher or cron setup until the behavior is understood. <br>
Risk: Workspace-level git rollback behavior and .env loading can affect unrelated files or expose secrets in shared or untrusted workspaces. <br>
Mitigation: Run only in trusted workspaces, inspect generated changes before accepting rollbacks, and keep environment files scoped to the intended project. <br>


## Reference(s): <br>
- [ClawHub Total Recall release page](https://clawhub.ai/gavdalf/total-recall) <br>
- [Total Recall README](README.md) <br>
- [Architecture](docs/architecture.md) <br>
- [Dream Cycle README](dream-cycle/README.md) <br>
- [Observation format schema](schemas/observation-format.md) <br>
- [Your AI Has an Attention Problem](https://gavlahh.substack.com/p/your-ai-has-an-attention-problem) <br>
- [I Published an AI Memory Fix. Then I Found the Hole.](https://gavlahh.substack.com/p/i-published-an-ai-memory-fix-then) <br>
- [Do Agents Dream?](https://gavlahh.substack.com/p/do-agents-dream) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown memory files, shell commands, JSON configuration, and setup guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates persistent local memory, logs, archive files, and optional dream-cycle metrics in the configured workspace.] <br>

## Skill Version(s): <br>
1.5.1 (source: server release evidence and changelog, released 2026-02-28) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

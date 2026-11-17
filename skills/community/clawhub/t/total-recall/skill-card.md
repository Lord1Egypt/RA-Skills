## Description:

Total Recall gives OpenClaw agents autonomous cross-session memory by observing transcripts, compressing conversations into prioritized notes, consolidating them, and recovering missed sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gavdalf](https://clawhub.ai/user/gavdalf)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use Total Recall to add persistent, human-readable memory to OpenClaw workspaces without a database or vector store. It is suited for agents that need cross-session context, compaction resilience, and periodic memory consolidation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill persistently monitors private OpenClaw transcripts.

Mitigation: Enable it only in workspaces where background transcript monitoring is acceptable, and review watcher and cron persistence before installation.

Risk: Transcript summaries may be sent to the configured LLM endpoint.

Mitigation: Use a trusted HTTPS endpoint or a trusted local provider, and confirm the selected model and API key settings before enabling observer or Dream Cycle runs.

Risk: Unsafe shell and file operations were reported by the security evidence.

Mitigation: Review the setup, watcher, dotenv parsing, Dream Cycle path handling, and rollback behavior before use in sensitive workspaces.

## Reference(s):

- [Total Recall ClawHub Skill](https://clawhub.ai/gavdalf/skills/total-recall)
- [README](artifact/README.md)
- [Skill Documentation](artifact/SKILL.md)
- [Architecture](artifact/docs/architecture.md)
- [Edge Cases and Hardening](artifact/docs/edge-cases.md)
- [Observation Format](artifact/schemas/observation-format.md)
- [Dream Cycle Guide](artifact/dream-cycle/README.md)
- [Your AI Has an Attention Problem](https://gavlahh.substack.com/p/your-ai-has-an-attention-problem)
- [I Published an AI Memory Fix. Then I Found the Hole.](https://gavlahh.substack.com/p/i-published-an-ai-memory-fix-then)
- [Do Agents Dream?](https://gavlahh.substack.com/p/do-agents-dream)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON configuration, and generated memory files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local observations, archives, logs, cron configuration, and setup instructions; some behavior depends on configured environment variables and platform support.]

## Skill Version(s):

1.5.1 (source: server release metadata, target metadata, and CHANGELOG; changelog date 2026-02-28)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

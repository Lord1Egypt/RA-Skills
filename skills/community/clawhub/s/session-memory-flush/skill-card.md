## Description: <br>
Scans OpenClaw-visible sessions before idle or reset, summarizes useful transcript context, and writes concise workspace memory entries for later sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hasakyi](https://clawhub.ai/user/hasakyi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to preserve important session context across idle or reset boundaries by turning transcripts into short memory entries. It supports installation, validation, debugging, and configuration of automatic memory flushing for main, subagent, cron, and dreaming sessions when transcripts are visible. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The recurring watcher scans private OpenClaw sessions and reads transcript files. <br>
Mitigation: Run a dry run first, install only in workspaces where transcript scanning is intended, and uninstall the timer or cron job when automatic scanning is no longer needed. <br>
Risk: Transcript text may be sent to the configured LLM provider for summarization. <br>
Mitigation: Use a trusted endpoint with least-privilege credentials, or configure an internal provider or rely on local fallback summarization when transcripts must not leave the environment. <br>
Risk: Generated memory files can retain sensitive or stale context beyond the original session. <br>
Mitigation: Review memory output regularly, keep only sanitized summaries, and avoid publishing local memory files, transcripts, logs, caches, or SQLite databases with the skill. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/hasakyi/session-memory-flush) <br>
- [Summarization prompt](artifact/summarize_prompt.md) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown memory entries with shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Summaries are intended to be concise, deduplicated per agent and session, and written to workspace memory files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

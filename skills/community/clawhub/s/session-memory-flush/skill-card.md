## Description:

Session Memory Flush scans visible OpenClaw sessions before idle/reset, summarizes valuable transcript context, and writes the summary to workspace memory files for later sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hasakyi](https://clawhub.ai/user/hasakyi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to preserve useful task context across new sessions by flushing concise session summaries into workspace memory before idle/reset cleanup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The watcher broadly reads OpenClaw transcripts visible to the account.

Mitigation: Install only when this background scanning behavior is intended, review the generated systemd or cron entry, and use dry-run mode before enabling recurring execution.

Risk: Raw transcript text may be sent to the configured LLM endpoint.

Mitigation: Prefer an internal or trusted HTTPS LLM endpoint, avoid placing secrets in transcripts, or run in local-only fallback mode in sensitive environments.

Risk: Derived session summaries are persisted into workspace memory files.

Mitigation: Review output directory permissions, sanitize sensitive content, and do not publish local memory files, logs, caches, session JSONL, SQLite databases, or OpenClaw configuration.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hasakyi/skills/session-memory-flush)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown summaries and markdown guidance with shell command and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Summaries are intended to be concise and can fall back to local rule-based extraction when an LLM endpoint is unavailable.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

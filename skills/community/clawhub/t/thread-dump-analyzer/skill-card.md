## Description:

Analyze thread dumps and goroutine dumps to diagnose deadlocks, thread pool exhaustion, contention hotspots, and blocked threads. Supports JVM thread dumps, Go goroutine dumps, Python threading dumps, and Node.js async stack traces.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and site reliability engineers use this skill to analyze JVM, Go, Python, and Node.js thread or goroutine dumps when applications hang, stop responding, or show deadlocks, thread pool exhaustion, contention hotspots, or goroutine leaks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dump-capture and process-signal commands can expose sensitive runtime data or affect live services.

Mitigation: Run commands only on systems you control, confirm the exact process ID first, prefer controlled maintenance windows, and store dumps in private directories with restrictive permissions.

Risk: Thread dumps and goroutine dumps can expose secrets or internal runtime details if shared broadly.

Mitigation: Redact sensitive and internal details before sharing reports or dumps, and delete dump files after analysis.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/charlie-morrison/skills/thread-dump-analyzer)
- [Publisher Profile](https://clawhub.ai/user/charlie-morrison)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown with inline bash code blocks and diagnostic report templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include process-signal commands, thread state summaries, blocked or waiting chain analysis, root cause analysis, and recommendations.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

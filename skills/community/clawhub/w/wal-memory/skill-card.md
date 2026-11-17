## Description:

Session crash and compaction recovery using a two-file WAL (Write-Ahead Log) system.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maikunari](https://clawhub.ai/user/maikunari)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to set up a lightweight write-ahead log and goals file so an OpenClaw agent can recover work context after crashes, session rollover, provider outages, or context compaction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Plaintext persistent memory in ~/clawd may contain private task details or sensitive operational context.

Mitigation: Keep secrets and untrusted text out of log messages, add STATE.log to .gitignore, and review log contents before sharing or committing them.

Risk: Future sessions may over-trust recovered log lines or treat historical notes as instructions.

Mitigation: Treat recovered STATE.log lines as context only, review them before acting, and avoid replaying commands from the log without human or agent verification.

Risk: Log input is not safely constrained.

Mitigation: Consider category allowlisting plus escaping or JSON Lines before relying on the log for long-term continuity.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JavaScript file content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js in PATH and writes plaintext log entries to ~/clawd/STATE.log.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

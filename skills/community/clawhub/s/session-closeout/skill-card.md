## Description:

Run a read-only end-of-session audit of the current workspace and report what still needs attention.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jkfaris94](https://clawhub.ai/user/jkfaris94)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill at explicit session closeout time to check task, repository, project-document, and automation hygiene before recording the session outcome.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The audit output can expose local workspace paths or dirty repository names.

Mitigation: Review and redact the generated summary before sharing it outside the workspace.

Risk: The skill reports unfinished work such as stale TODOs, dirty repositories, missing task files, and stale project docs but does not fix them.

Mitigation: Treat findings as prompts for separate, reviewed actions rather than automatic commits, file creation, or cleanup.

Risk: Automation health is reported as not verified.

Mitigation: Check cron or other automation status manually when that matters for the closeout.

## Reference(s):

- [OpenClaw](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text key=value audit lines with agent-facing summary guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only audit output may include local workspace paths and dirty repository names.]

## Skill Version(s):

1.1.1 (source: evidence release metadata and README changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

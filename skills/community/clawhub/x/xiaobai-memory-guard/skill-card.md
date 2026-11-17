## Description:

Memory Guard helps AI agents scan memory, notes, and handoff files to detect missing context, continuity gaps, and memory health issues before or during long-running sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aptratcn](https://clawhub.ai/user/aptratcn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to add memory-continuity checks, health reports, and recovery guidance to long-running AI agent sessions where missed handoff files or stale memory can cause task context loss.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release asks users to run an unaudited, mutable GitHub-hosted memory guard script.

Mitigation: Review or vendor the actual memory-guard.mjs implementation before installing it, and pin any dependency or source checkout to a trusted immutable revision.

Risk: Optional startup or cron integration can create recurring access to agent memory files and git history under the user's account.

Mitigation: Avoid adding the startup block or cron job unless recurring scans are intentional, and limit the files and repositories available to the process.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aptratcn/skills/xiaobai-memory-guard)
- [Artifact README](artifact/README.md)
- [Artifact English README](artifact/README_EN.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown or plain-text memory health reports with inline shell commands and recovery checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require access to local memory, notes, handoff files, and git history when the referenced guard script is installed and run.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

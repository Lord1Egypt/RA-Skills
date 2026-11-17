## Description:

Self-improving OpenClaw agent system that detects errors, selects improvement topics, creates research and backlog tasks, and records impact measurements.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mopga](https://clawhub.ai/user/mopga)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to monitor workspace error signals, prioritize improvement topics, and create agent-facing research, backlog, impact, and procedural-memory records for later review and execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically create persistent agent-facing backlog and research entries from workspace logs.

Mitigation: Keep cron integration disabled until the scripts are reviewed, restrict who can write error logs, and require human approval before generated backlog tasks are executed.

Risk: Procedural memory stores reusable commands that could expose or preserve sensitive operational details.

Mitigation: Avoid storing secrets in procedural commands and periodically review memory entries before agents reuse them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mopga/skills/self-evalutaed-agent)
- [Publisher profile](https://clawhub.ai/user/mopga)
- [Artifact README](artifact/README.md)
- [Artifact skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown files, JSON and JSONL records, and terminal text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes persistent records under the configured OpenClaw workspace, including memory, backlog, research, trigger, impact, and procedural-memory files.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact metadata.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

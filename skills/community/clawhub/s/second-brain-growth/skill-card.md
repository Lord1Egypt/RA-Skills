## Description:

Evaluates second-brain effective knowledge growth and health across deposition, connection, recall, transformation, and debt, with Hbrain defaults and Codex, Hermes, and OpenClaw workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

Knowledge workers and developers maintaining an Hbrain-style second brain use this skill to produce Chinese growth scorecards. It diagnoses whether notes are becoming connected, recallable, and useful for judgment, action, or output rather than merely accumulating as files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is intended to read local Hbrain or second-brain files, which may contain private notes.

Mitigation: Install and use it only when the agent should inspect those local files.

Risk: One documented dry-routing command can place user-supplied text into unsafe shell input.

Mitigation: Pass questions as literal arguments through an argument-array API or robustly escape them before execution.

Risk: Cron and report workflows can create persistent scheduled reports.

Mitigation: Enable automation only when scheduled reporting is intentional and the destination path is acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/harrylabsj/skills/second-brain-growth)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reports and chat summaries with optional YAML handoff blocks and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Defaults to Chinese user-facing summaries and absolute report date ranges.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

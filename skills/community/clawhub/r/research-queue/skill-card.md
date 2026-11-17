## Description:

Structured background research queue for unresolved technical, product, algorithmic, mathematical, and workflow questions. Use when the user wants to capture open questions in `QUESTIONS.md`, investigate them over time, run bounded web/local experiments, update queue state, or build an autonomous cron-driven research loop with strict evidence and completion tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mozi1924](https://clawhub.ai/user/mozi1924)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical teams use this skill to track unresolved questions in a structured queue, investigate one bounded question at a time, and record evidence-backed conclusions or blocked reasons.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The starter queue can direct an automated agent to inspect a hidden OpenClaw configuration file without clear approval or redaction rules.

Mitigation: Review the starter template before automation, remove or replace the example that links to ~/.openclaw/openclaw.json, and approve any hidden config paths before they are read or recorded.

Risk: Autonomous research runs may use local execution or file reads beyond what a specific question requires.

Mitigation: Grant exec and local read access only for questions that need them, keep each run bounded to one question by default, and record evidence summaries rather than raw sensitive output.

## Reference(s):

- [Queue Format](references/queue-format.md)
- [Automation](references/automation.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown queue updates, concise findings, and optional command or configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update QUESTIONS.md and memory/YYYY-MM-DD.md when the user authorizes persistent research tracking.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

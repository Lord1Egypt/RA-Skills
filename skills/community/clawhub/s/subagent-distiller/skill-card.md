## Description:

Automatically extracts structured long-term knowledge from OpenClaw conversations, filters low-value content, clusters topics, and tracks unresolved items.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mashirops](https://clawhub.ai/user/mashirops)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to turn local conversation history into durable knowledge cards, domain summaries, pending-item reminders, and cleanup reports for long-running OpenClaw workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can scan and persist private conversation history, including reset or deleted session transcripts, into long-lived local files.

Mitigation: Run it only on scoped session inputs, review generated memory files before retention, and add redaction and cleanup controls for sensitive conversations.

Risk: Optional recurring cron use can continuously collect new conversation content without a fresh manual review.

Mitigation: Avoid enabling scheduled execution until session scope, retention expectations, redaction, and cleanup procedures are defined.

Risk: The security evidence reports weak privacy controls and unsafe write paths.

Mitigation: Keep execution limited to a trusted local workspace and validate task names, domain names, and output paths before finalization.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mashirops/skills/subagent-distiller)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance]

**Output Format:** [Markdown knowledge cards and reports, JSON task manifests, and shell command guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local memory artifacts, state files, task manifests, domain summaries, reminder reports, and cleanup reports in the OpenClaw workspace.]

## Skill Version(s):

3.0.1 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

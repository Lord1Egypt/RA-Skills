## Description:

Workflow Crystallizer analyzes memory logs to detect recurring patterns and suggest automations such as cron jobs, skills, workflow shortcuts, and monitors.

This skill is ready for commercial/non-commercial use.

## Publisher:

[newageinvestments25-byte](https://clawhub.ai/user/newageinvestments25-byte)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to mine OpenClaw memory logs for repeated requests, multi-step workflows, and time-correlated tasks, then review suggested automations before adopting them.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads memory logs and keeps a local plaintext cache of memory-derived excerpts.

Mitigation: Run it only where memory-log access is acceptable, keep state files local, and review state.json periodically.

Risk: Generated cron definitions, skill drafts, and workflow shortcuts may reflect untrusted or misleading memory content.

Mitigation: Treat all generated automations as drafts and review or scan them before approval or deployment.

Risk: Automatic scheduled use may surface broad or noisy suggestions before triggers are narrowed.

Mitigation: Avoid unattended scheduled runs until confidence thresholds, input scope, and reporting expectations are tuned.

## Reference(s):

- [ClawHub Release Page](https://clawhub.ai/newageinvestments25-byte/skills/workflow-crystallizer)
- [Pattern Types - Detection Logic](artifact/references/pattern-types.md)
- [Suggestion Templates](artifact/references/suggestion-templates.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown reports with JSON suggestion records and ready-to-review code or configuration snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Caches memory-derived events and suggestion status locally; reports up to three high-confidence suggestions per run by default.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

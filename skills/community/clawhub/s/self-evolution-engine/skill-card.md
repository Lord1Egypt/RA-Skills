## Description:

Autonomous self-improvement engine that analyzes interaction patterns, extracts learnings, proposes behavioral changes, and reports on long-term agent behavior.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shenmeng](https://clawhub.ai/user/shenmeng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to review OpenClaw memory and learning files, detect recurring patterns, and produce candidate behavior updates, self-assessments, and evolution reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads persistent OpenClaw memory and learning files, which may contain sensitive transcripts or user preferences.

Mitigation: Use it only on scoped workspaces that have been reviewed for secrets or sensitive content, and add redaction before processing sensitive logs.

Risk: Generated behavior changes can affect long-lived agent behavior if integrated without review.

Mitigation: Review proposed rules, validate them in isolation, keep backups, and require explicit approval before updating behavioral files.

Risk: Automated or scheduled runs may promote noisy patterns into persistent guidance.

Mitigation: Avoid unattended auto-evolution and compare recommendations against the evolution log before adopting them.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON or Markdown reports from the helper script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include candidate rules, pattern summaries, recommendations, self-assessment JSON, and evolution report Markdown.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

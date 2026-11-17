## Description:

Thesis Tracker helps agents record, monitor, validate, and report on investment theses using structured assumptions, triggers, time windows, targets, and status updates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dzy11650](https://clawhub.ai/user/dzy11650)

### License/Terms of Use:

MIT-0

## Use Case:

External users, analysts, and agents use this skill to maintain investment theses across their lifecycle: capture the thesis, store assumptions and validation triggers, check pending theses against market data, update status, and produce concise thesis tracking reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Investment theses, positions, or strategies may be stored persistently in thesis-tracker/theses.json and optionally mirrored into IMA notes.

Mitigation: Avoid recording private positions or strategies unless persistent storage is acceptable; review and delete records when they are no longer needed.

Risk: The skill can summarize thesis status from financial trigger checks, which may be incomplete or misleading if underlying market data is unavailable or stale.

Mitigation: Review generated thesis reports and source data before making investment decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dzy11650/skills/thesis-tracker)
- [Artifact README](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown reports and JSON thesis records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores thesis records in thesis-tracker/theses.json and may mirror new theses into IMA notes when available.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

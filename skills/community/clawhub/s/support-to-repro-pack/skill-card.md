## Description:

Convert support tickets, logs, and screenshots into sanitized, reproducible engineering issue packs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mshs01156](https://clawhub.ai/user/mshs01156)

### License/Terms of Use:

MIT-0

## Use Case:

Support engineers and developers use this skill to turn messy tickets, logs, screenshots, and chat context into sanitized engineering handoff packs with facts, timelines, redaction reports, and customer-safe communication drafts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive raw details may remain in generated files or ZIP archives.

Mitigation: Use private per-run temp and output directories, inspect every generated file and archive before sharing, and require a final whole-pack scan that blocks leaks.

Risk: Real customer tickets, logs, screenshots, or credentials may be exposed during early use.

Mitigation: Avoid real customer data until raw-derived output paths are verified redacted; use synthetic or already-approved samples for validation.

Risk: Dependency drift may reduce reproducibility of installs and generated packs.

Mitigation: Pin dependencies for reproducible installs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mshs01156/skills/support-to-repro-pack)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and generated repro-pack files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces sanitized tickets, logs, JSON facts, timelines, redaction reports, engineering issue drafts, internal escalation summaries, and customer replies.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

A SIAS/Rheingold deep-research skill for FOIA requests, NGO network analysis, and public funding research in Cologne and North Rhine-Westphalia, combining local database findings with web research.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iggyswelt](https://clawhub.ai/user/iggyswelt)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and research agents use this skill to structure SIAS/Rheingold investigations involving FOIA requests, NGO network mapping, public funding research, mail processing, and concise evidence-based reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive mail and investigative findings may be stored broadly in local database tables.

Mitigation: Define what data may be stored, require retention limits, and review records before persistence.

Risk: Critical findings may be sent to a fixed Telegram recipient without clear user control.

Mitigation: Remove or gate Telegram notifications, make the approver configurable, and require per-message confirmation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/iggyswelt/skills/sias-research-v1)
- [SIAS Project](https://github.com/iggyswelt/SIAS)
- [Publisher profile](https://clawhub.ai/user/iggyswelt)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with SQL and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include confidence labels, source notes, contradiction summaries, and database-oriented research records.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

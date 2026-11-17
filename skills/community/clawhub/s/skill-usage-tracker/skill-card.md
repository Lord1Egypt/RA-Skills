## Description:

Automatically tracks and audits skill usage, enforces rules from SKILL_USAGE_RULES.md, logs violations, and generates daily reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sasamittrrr](https://clawhub.ai/user/sasamittrrr)

### License/Terms of Use:


## Use Case:

Developers and administrators use this skill to audit skill usage against mandatory local rules, record violations, and review daily usage reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks for automatic checks after every response using external mandatory rules without enough scoping.

Mitigation: Require clear user or administrator enablement and bundle or strictly constrain the rules file it uses.

Risk: Persistent logging and report generation may create records whose contents and retention are unclear.

Mitigation: Document exactly what is logged, where reports are written, and how users can disable or delete those records.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sasamittrrr/skills/skill-usage-tracker)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files]

**Output Format:** [Markdown reports and plain-text log entries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads a local rules file, records violations in skill_violations.log, and generates daily usage reports.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

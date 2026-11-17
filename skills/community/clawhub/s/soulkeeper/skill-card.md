## Description:

SoulKeeper audits agent soul files into structured rules, scores conversation transcripts for behavioral drift, and surfaces context-aware reminders before an agent responds.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cassh100k](https://clawhub.ai/user/cassh100k)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use SoulKeeper to audit SOUL.md, TOOLS.md, and AGENTS.md into structured behavioral rules, detect drift in session transcripts, and inject reminders that keep agent behavior aligned with approved rules.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Context reminders can persistently shape agent behavior and may weaken normal confirmation habits if adopted without review.

Mitigation: Review and edit remind.py before use, and enable heartbeat integration only after the reminder rules are user-approved.

Risk: Hard-coded credential paths and logged-in infrastructure claims can expose sensitive operational details.

Mitigation: Remove credential paths and infrastructure claims from reminders before deployment.

Risk: Transcript drift analysis may process private or sensitive conversation content.

Mitigation: Redact transcripts before running drift analysis or storing generated reports.

## Reference(s):

- [SoulKeeper on ClawHub](https://clawhub.ai/cassh100k/skills/soulkeeper)
- [Publisher profile](https://clawhub.ai/user/cassh100k)

## Skill Output:

**Output Type(s):** [text, json, guidance, configuration]

**Output Format:** [JSON rule files, plain-text or JSON drift reports, and reminder text suitable for agent context.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Python 3.8+ stdlib command-line tools; audit.py can write soul_rules.json, drift.py can return a nonzero exit code when a threshold is met, and remind.py can emit compact or heartbeat reminders.]

## Skill Version(s):

1.0.0 (source: server release evidence, artifact/clawpkg.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

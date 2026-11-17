## Description:

Helps verify that skill signing events are recorded in an independently auditable transparency log, catching trust failures where a registry operator can silently rewrite history without detection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andyxinweiminicloud](https://clawhub.ai/user/andyxinweiminicloud)

### License/Terms of Use:


## Use Case:

Developers, registry operators, and security reviewers use this skill to assess whether skill signing events are covered by independently auditable transparency logs and to identify gaps in append-only verifiability, signing-event coverage, and cross-registry consistency.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Registry or transparency-log inputs may be incomplete, unavailable, or inconsistent, which can lead to inconclusive audit findings.

Mitigation: Treat the report as an evidence review, preserve source URLs or records, and request registry-side clarification before relying on a disputed signing history.

Risk: The skill may suggest curl or python3 checks against user-provided registry endpoints.

Mitigation: Run proposed commands only against trusted endpoints and review them before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/andyxinweiminicloud/skills/transparency-log-auditor)
- [Publisher profile](https://clawhub.ai/user/andyxinweiminicloud)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown audit report with findings, verdicts, risk assessment, and recommended actions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose curl or python3 commands for user-provided registry and transparency-log checks.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

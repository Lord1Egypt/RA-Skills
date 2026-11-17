## Description:

Helps quality managers and production supervisors classify quality alerts, map escalation owners and response windows, and produce text and Markdown escalation boards for quality incidents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[duding-engicool](https://clawhub.ai/user/duding-engicool)

### License/Terms of Use:

MIT-0

## Use Case:

Quality managers and site supervisors use this skill to turn quality incident lists into standardized L1-L4 escalation guidance, response-time checks, and audit-ready escalation boards.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Escalation thresholds or organization-specific owners may not match a company's actual quality procedures.

Mitigation: Verify response windows, escalation levels, and named owners against approved internal procedures before using reports for operations or audits.

Risk: Users may mistake workflow guidance for an automated production-control or stop-line decision.

Mitigation: Use the output as a reporting and escalation-drafting aid, with management review for stop-line, release, or customer notification decisions.

Risk: Quality incident inputs may contain more operational detail than the report requires.

Mitigation: Provide only the incident fields needed to classify alerts and calculate response timing.

## Reference(s):

- [Server-resolved GitHub provenance](https://github.com/duding-engicool/skill-quality-alert-escalation)
- [ClawHub skill page](https://clawhub.ai/duding-engicool/skills/skill-quality-alert-escalation)
- [Publisher profile](https://clawhub.ai/user/duding-engicool)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Plain text and Markdown reports with escalation flow, escalation matrix, live board, and summary statistics]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Intended for review and operational follow-up; does not execute stop-line or production-control actions.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

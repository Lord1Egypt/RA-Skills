## Description:

Generates forensic chain of custody HTML reports for evidence management and legal compliance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd)

### License/Terms of Use:

MIT-0

## Use Case:

External forensic examiners, incident response teams, corporate security practitioners, and legal professionals use this skill to generate formal HTML chain-of-custody reports from case details, evidence metadata, custody history, handler information, timestamps, and integrity hashes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send sensitive investigation, identity, evidence, hash, location, and custody-history data to an external API.

Mitigation: Use only redacted test data unless the organization has approved the service's retention, deletion, access-control, logging, and data-residency practices.

Risk: Generated reports may be used in law-enforcement, legal, corporate investigation, or incident-response workflows where confidentiality and admissibility matter.

Mitigation: Require legal, security, and records-management review before using generated reports in active matters; prefer an internally hosted or local report generator for confidential cases.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/krishnakumarmahadevan-cmd/skills/toolweb-chain-of-custody)
- [Publisher profile](https://clawhub.ai/user/krishnakumarmahadevan-cmd)
- [Chain of Custody API route](https://api.mkkpro.com/compliance/chain-of-custody)
- [Chain of Custody API docs](https://api.mkkpro.com:8115/docs)
- [ToolWeb](https://toolweb.in)
- [ToolWeb OpenClaw](https://toolweb.in/openclaw/)
- [ToolWeb RapidAPI profile](https://rapidapi.com/user/mkrishna477)

## Skill Output:

**Output Type(s):** [API Calls, Text, Files]

**Output Format:** [JSON response containing generated HTML report content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns status, reportId, htmlReport, and message; request data includes case, evidence, custody-chain, user, session, and timestamp fields.]

## Skill Version(s):

1.0.0 (source: server release metadata and OpenAPI info.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

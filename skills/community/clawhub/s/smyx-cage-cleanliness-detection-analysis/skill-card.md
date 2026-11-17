## Description:

Analyzes kennel floor images or videos to estimate feces and urine coverage and cleanliness, then flags cleaning thresholds.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui)

### License/Terms of Use:

MIT-0

## Use Case:

Boarding kennel, pet shop, animal hospital, and breeding-facility operators use it to monitor cage floors from camera images or video, review hygiene estimates, and follow up on cleaning alerts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags account and credential handling, external media processing, and unclear side effects beyond the stated cleanliness analysis purpose; the scan was partial and its suspicious verdict is not a claim of malicious intent.

Mitigation: Before installing or sending media, ask the provider to explain why account registration and credential storage are needed and where uploaded media and identity data are sent or stored.

## Reference(s):

- [Skill API reference](references/api_doc.md)
- [Skill demonstration](https://lifeemergence.com/sample.html)
- [ClawHub release page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-cage-cleanliness-detection-analysis)

## Skill Output:

**Output Type(s):** [Analysis report, JSON, Markdown, Cleaning alerts, Report links]

**Output Format:** [Structured cleanliness results and recommendations; JSON detail or Markdown report listings, with report links when available]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Visual estimates for hygiene management; not medical advice.]

## Skill Version(s):

1.0.16 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

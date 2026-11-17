## Description:

Generates bride and groom horoscopes then produces a marriage compatibility report with PDF outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd)

### License/Terms of Use:

MIT-0

## Use Case:

External users, matrimonial platforms, and astrology consultants use this skill to request Vedic astrology-based compatibility reports from birth details for a bride and groom.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The API request requires names, family names, mobile numbers, birth dates, birth times, countries, and birth places for two people.

Mitigation: Use the skill only with consent from both individuals and avoid unnecessary real identifiers where the workflow allows.

Risk: Generated PDF URLs may expose sensitive horoscope and compatibility reports, and the artifacts do not document access controls, expiration, or deletion behavior.

Mitigation: Treat returned PDF links as sensitive, limit redistribution, and confirm retention and access-control expectations before using real people's data.

Risk: The security verdict is suspicious because personal data is sent to an external service without documented privacy controls in the artifacts.

Mitigation: Review organizational privacy, data-transfer, and vendor-risk requirements before installing or using this skill in production workflows.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/krishnakumarmahadevan-cmd/skills/toolweb-marriage-matching)
- [ToolWeb](https://toolweb.in)
- [Marriage Matching API Route](https://api.mkkpro.com/lifestyle/marriage-matching)
- [Marriage Matching API Docs](https://api.mkkpro.com:8197/docs)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Files, Guidance]

**Output Format:** [JSON responses with PDF download URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces bride horoscope, groom horoscope, and marriage compatibility PDF links when the external API succeeds.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Interprets current astrological transits against a user's natal chart to describe themes, pressures, and opportunities over a period.

This skill is ready for commercial/non-commercial use.

## Publisher:

[weixin97676414](https://clawhub.ai/user/weixin97676414)

### License/Terms of Use:

MIT-0

## Use Case:

People with natal chart details use the skill to understand current or near-term themes in areas such as work and relationships. It gathers birth and current-location details, requests a transit chart from the service, and presents a time-bounded interpretation rather than a prediction of specific events.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review marks the skill suspicious with medium confidence because it reports wallet setup and unpinned software installation beyond the stated astrology purpose; scanner coverage is partial.

Mitigation: Before use, explain the wallet setup and software installation and obtain separate authorization, verify the package source and version, and clarify how the external service handles birth and location data.

## Reference(s):

- [Transit service API contract](https://api.xinjianxue.com/api/xinjianxue/aipay/astro-transit)
- [Interpretation framework](artifact/references/reading.md)
- [Payment flow](artifact/references/payment.md)
- [ClawHub skill page](https://clawhub.ai/weixin97676414/skills/xinjianxue-astro-transit)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown prose with headings and emphasis]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Time-bounded interpretation; avoids claims that specific events will occur.]

## Skill Version(s):

2.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

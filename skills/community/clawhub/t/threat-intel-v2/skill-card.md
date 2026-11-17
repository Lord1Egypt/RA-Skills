## Description:

Aggregates and analyzes open-source intelligence (OSINT) data from multiple sources to identify threats, validate indicators, and enrich security investigations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd)

### License/Terms of Use:

MIT-0

## Use Case:

SOC analysts, threat hunters, incident responders, MSSPs, and enterprise security teams use this skill to enrich indicators of compromise with reputation, attribution, geolocation, malware association, and confidence data during security investigations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Indicator lookups may send internal, regulated, customer-sensitive, or embargoed investigation data to an external API and downstream intelligence sources.

Mitigation: Submit only indicators approved under the organization's data-sharing policy, and avoid sensitive indicators unless external submission is explicitly acceptable.

Risk: Threat intelligence enrichment can influence investigation priority even when reputation and confidence scores are incomplete or time-sensitive.

Mitigation: Treat results as investigative context and corroborate high-impact decisions with additional sources and analyst review.

## Reference(s):

- [Threat Intel V2 ClawHub Page](https://clawhub.ai/krishnakumarmahadevan-cmd/skills/threat-intel-v2)
- [API Docs](https://api.mkkpro.com:8011/docs)
- [Kong Route](https://api.mkkpro.com/security/threat-intel-v2)
- [ToolWeb](https://toolweb.in)
- [RapidAPI Publisher Profile](https://rapidapi.com/user/mkrishna477)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Analysis, Guidance]

**Output Format:** [JSON responses summarized or cited in Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Looks up one submitted indicator at a time, such as an IP address, domain, URL, email address, or file hash.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

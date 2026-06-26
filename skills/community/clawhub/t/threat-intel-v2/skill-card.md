## Description: <br>
Aggregates and analyzes open-source intelligence (OSINT) data from multiple sources to identify threats, validate indicators, and enrich security investigations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Security analysts, threat hunters, incident responders, and security automation agents use this skill to enrich IPs, domains, email addresses, file hashes, and URLs with OSINT context during investigations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Indicators submitted for lookup are sent to an external OSINT service and could expose confidential incident details. <br>
Mitigation: Submit only indicators approved for external sharing, and avoid customer information, private emails, internal-only infrastructure, and non-public investigation artifacts unless the organization has approved that data sharing. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/krishnakumarmahadevan-cmd/threat-intel-v2) <br>
- [API docs](https://api.mkkpro.com:8011/docs) <br>
- [API route](https://api.mkkpro.com/security/threat-intel-v2) <br>
- [OpenAPI specification](artifact/openapi.json) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Text, JSON, Guidance] <br>
**Output Format:** [JSON threat-intelligence response with indicator enrichment and validation errors] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns reputation score, threat level, source attribution, geolocation, malware associations, WHOIS data, confidence, and last-updated fields when available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

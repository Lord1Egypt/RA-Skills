## Description: <br>
Generate comprehensive cybersecurity threat assessments and defense guides for threat landscape evaluation, defense strategy planning, ransomware protection, phishing defense, APT mitigation, supply chain security, and threat modeling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Security practitioners, developers, and operations teams use this skill to request ToolWeb-backed threat assessments and defense guides for specific industries, threat types, and assets. It helps structure threat landscape, detection, monitoring, incident response, and security tool recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send organization-level security-planning context to ToolWeb. <br>
Mitigation: Use only with approved data sharing; omit secrets, internal hostnames, live incident details, regulated data, and detailed architecture unless the organization has approved sending that information to ToolWeb. <br>
Risk: The bundled test script disables TLS certificate verification for its curl request. <br>
Mitigation: Do not run scripts/test-api.sh unless the TLS bypass is removed and the endpoint is confirmed; use standard certificate validation for API testing. <br>
Risk: Generated cybersecurity guidance may be incomplete, stale, or unsuitable for a specific environment. <br>
Mitigation: Have qualified security staff review recommendations before operational use and adapt them to the organization's architecture, controls, and compliance obligations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/krishnakumarmahadevan-cmd/threat-assessment-defense-guide) <br>
- [ToolWeb API hub](https://portal.toolweb.in) <br>
- [ToolWeb platform](https://toolweb.in) <br>
- [Threat assessment API endpoint](https://portal.toolweb.in/apis/security/threat-assessment-defense) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown threat assessment and defense guide, with inline JSON and curl examples when API invocation or configuration is shown.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TOOLWEB_API_KEY and curl; successful use depends on the ToolWeb API response.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

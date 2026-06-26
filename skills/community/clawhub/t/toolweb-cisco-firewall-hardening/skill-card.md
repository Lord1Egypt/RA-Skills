## Description: <br>
Generate CIS-compliant hardened Cisco ASA and FTD firewall configurations with customizable security options. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Security teams, managed security service providers, and DevSecOps engineers use this skill to request CIS-aligned Cisco ASA and FTD hardening configurations and review the generated settings before applying them to firewall environments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Requests include session identifiers and may include a user identifier. <br>
Mitigation: Use pseudonymous session IDs and leave userId null where possible. <br>
Risk: Generated firewall configurations may be unsuitable for a specific production network without review. <br>
Mitigation: Review and test generated configurations before applying them to production Cisco ASA or FTD devices. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/krishnakumarmahadevan-cmd/toolweb-cisco-firewall-hardening) <br>
- [ToolWeb](https://toolweb.in) <br>
- [Cisco Firewall Hardening API Docs](https://api.mkkpro.com:8140/docs) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON request and response examples; API responses contain generated firewall configuration data.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated firewall configurations should be manually reviewed and tested before production use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and OpenAPI metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

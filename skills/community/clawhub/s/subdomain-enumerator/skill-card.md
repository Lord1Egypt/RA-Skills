## Description: <br>
Discovers and enumerates all subdomains associated with a target domain using deep reconnaissance techniques. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Security professionals, penetration testers, bug bounty hunters, DevSecOps teams, and organizations use this skill to enumerate active and inactive subdomains for authorized attack surface mapping and asset discovery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Subdomain reconnaissance can be misused against domains the user is not authorized to assess. <br>
Mitigation: Use the skill only on domains you own or have explicit permission to test. <br>
Risk: Target domains are sent to an external API provider for enumeration. <br>
Mitigation: Submit only domains appropriate for the provider to process and avoid sensitive targets unless organizational policy allows it. <br>


## Reference(s): <br>
- [Subdomain Enumerator ClawHub Listing](https://clawhub.ai/krishnakumarmahadevan-cmd/subdomain-enumerator) <br>
- [Subdomain Enumerator API Docs](https://api.mkkpro.com:8006/docs) <br>
- [Subdomain Enumerator API Route](https://api.mkkpro.com/security/subdomain-enumerator) <br>
- [ToolWeb](https://toolweb.in) <br>


## Skill Output: <br>
**Output Type(s):** [API calls, JSON, guidance] <br>
**Output Format:** [JSON response with the target domain, discovered subdomains, IP addresses, activity status, total count, and enumeration timing.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a target domain and returns active and inactive subdomain records.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

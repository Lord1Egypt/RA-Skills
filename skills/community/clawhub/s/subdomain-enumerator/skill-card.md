## Description:

Discovers and enumerates all subdomains associated with a target domain using deep reconnaissance techniques.

This skill is ready for commercial/non-commercial use.

## Publisher:

[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd)

### License/Terms of Use:

MIT-0

## Use Case:

Security professionals, penetration testers, bug bounty hunters, DevSecOps teams, and organizations use this skill to enumerate active and inactive subdomains for authorized attack-surface mapping and asset discovery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Target domains are sent to a third-party API provider.

Mitigation: Use the skill only when disclosure to the provider is acceptable for the organization or client.

Risk: Subdomain enumeration results may reveal sensitive reconnaissance data.

Mitigation: Handle results as sensitive security assessment data and share them only with authorized parties.

Risk: Reconnaissance against domains without authorization can violate policy or law.

Mitigation: Run enumeration only for domains the user owns or is explicitly authorized to assess.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/krishnakumarmahadevan-cmd/skills/subdomain-enumerator)
- [API Documentation](https://api.mkkpro.com:8006/docs)
- [API Route](https://api.mkkpro.com/security/subdomain-enumerator)
- [ToolWeb](https://toolweb.in)
- [RapidAPI Publisher Profile](https://rapidapi.com/user/mkrishna477)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Analysis]

**Output Format:** [JSON response containing the target domain, discovered subdomains, IP addresses, status values, total count, and enumeration timing.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a target domain and sends that domain to a third-party API provider.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

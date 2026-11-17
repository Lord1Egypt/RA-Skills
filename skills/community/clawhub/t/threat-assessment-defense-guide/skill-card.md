## Description:

Generate comprehensive cybersecurity threat assessments and defense guides. Use when evaluating threat landscapes, building defense strategies, ransomware protection plans, phishing defense, APT mitigation, supply chain security, or any threat modeling and defense planning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd)

### License/Terms of Use:

MIT-0

## Use Case:

Security practitioners, developers, and operations teams use this skill to request threat assessments and defense guidance for selected threat types, industries, and asset categories. It gathers the user's security context, calls the ToolWeb API, and returns prioritized defense, detection, monitoring, and incident response recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends threat model details, asset categories, security tooling context, compliance context, timestamps, API usage, and the API key to ToolWeb.

Mitigation: Use it only when ToolWeb is approved for the data being shared, and do not submit secrets, hostnames, IP addresses, customer data, or regulated incident details unless your organization has approved that disclosure.

Risk: The bundled test script disables TLS certificate verification and uses a ToolWeb endpoint that should be confirmed before execution.

Mitigation: Avoid running scripts/test-api.sh unless the endpoint is confirmed and curl -k is removed.

Risk: API-backed output depends on a valid TOOLWEB_API_KEY, subscription limits, and external service availability.

Mitigation: Confirm the API key, plan limits, and service availability before relying on the skill in operational workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/krishnakumarmahadevan-cmd/skills/threat-assessment-defense-guide)
- [ToolWeb API portal](https://portal.toolweb.in)
- [Threat assessment API endpoint](https://portal.toolweb.in/apis/security/threat-assessment-defense)
- [ToolWeb platform](https://toolweb.in)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown report with inline shell commands and API-backed response content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and TOOLWEB_API_KEY; successful ToolWeb API calls may be metered.]

## Skill Version(s):

1.0.2 (source: ClawHub release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

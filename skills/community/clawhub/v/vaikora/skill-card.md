## Description: <br>
Vaikora routes OpenClaw LLM calls through a security proxy that monitors prompts, responses, and provider credentials for risk signals before forwarding traffic to the selected model provider. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[data443](https://clawhub.ai/user/data443) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security teams use Vaikora to route OpenClaw agent LLM traffic through a security monitoring gateway, assess risky agent actions, and forward high-risk signals to SIEM or EDR connectors. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Vaikora receives prompts, message history, model responses, and the upstream LLM provider key while proxying model traffic. <br>
Mitigation: Use a dedicated provider key with spend limits, evaluate with non-sensitive data first, review vendor retention and access terms, and rotate keys after testing. <br>
Risk: Routing regulated or high-sensitivity data through a third-party LLM security proxy may create compliance and vendor access exposure. <br>
Mitigation: Do not route PHI, PCI, or other regulated data until the organization has approved Vaikora's retention, access, and compliance controls. <br>


## Reference(s): <br>
- [Vaikora Homepage](https://vaikora.com) <br>
- [Vaikora Documentation](https://vaikora.com/docs) <br>
- [Vaikora AWS Security Hub Connector](https://aws.amazon.com/marketplace/pp/prodview-dotgh5y3ox6rq) <br>
- [Vaikora SentinelOne Connector](https://aws.amazon.com/marketplace/pp/prodview-tzxzdoajtk3bu) <br>
- [Vaikora CrowdStrike Connector](https://aws.amazon.com/marketplace/pp/prodview-cs7idbycte7fm) <br>
- [Data443 Risk Mitigation](https://data443.com) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell and YAML examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Provides setup guidance for environment variables, headers, routing configuration, connector installation, and verification commands.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

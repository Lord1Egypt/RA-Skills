## Description: <br>
An MCP server that interfaces with VMware Aria Operations to run regulatory compliance checks (ISO 27001, PCI DSS, CIS, etc.) against the VCF environment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kasture-rohit](https://clawhub.ai/user/kasture-rohit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, platform operators, and compliance teams use this MCP server to let an agent query VMware Aria Operations for VCF compliance alerts and summarize status for frameworks such as ISO, PCI, CIS, HIPAA, DISA, and FISMA. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses an Aria Operations API token over certificate-unverified HTTPS. <br>
Mitigation: Use a dedicated read-only, least-privilege token and enable certificate verification with a trusted CA bundle before relying on live results. <br>
Risk: The skill can return simulated audit results when the live Aria Operations API call is unsuccessful. <br>
Mitigation: Do not use simulated output as audit evidence; require clear live-data success before using reports for compliance decisions. <br>
Risk: The runtime dependencies are not pinned to specific versions. <br>
Mitigation: Pin and review dependency versions before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kasture-rohit/vcf-compliance-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Plain text or Markdown returned by an MCP tool] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ARIA_OPS_HOST and ARIA_OPS_API_TOKEN; compliance standard input defaults to ISO.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

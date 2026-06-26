## Description: <br>
An MCP server that interfaces with VMware Aria Operations to extract Green IT metrics, carbon footprint data, and the organizational Green Score for ESG reporting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kasture-rohit](https://clawhub.ai/user/kasture-rohit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, IT operations teams, and sustainability reporting teams use this skill to connect an agent to VMware Aria Operations and request Green IT, carbon footprint, power consumption, and Green Score reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends an Aria Operations API token over HTTPS while certificate verification is disabled. <br>
Mitigation: Use a least-privilege token, restrict ARIA_OPS_HOST to the intended internal Aria Operations instance, and change the server to verify TLS with a trusted CA. <br>
Risk: Fallback simulated sustainability data can be mistaken for authoritative ESG output. <br>
Mitigation: Treat fallback reports as demo data and verify live Aria Operations configuration before using outputs for reporting. <br>
Risk: Dependencies are unpinned in requirements.txt. <br>
Mitigation: Pin reviewed dependency versions before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kasture-rohit/vcf-sustainability-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, shell commands, guidance] <br>
**Output Format:** [Markdown report text and MCP setup configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ARIA_OPS_HOST and ARIA_OPS_API_TOKEN environment variables.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

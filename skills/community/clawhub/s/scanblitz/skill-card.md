## Description: <br>
Create dynamic, trackable QR codes and inspect scan analytics with the ScanBlitz API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[whotookmylogin](https://clawhub.ai/user/whotookmylogin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, marketers, and operators use this skill to create dynamic QR links, update their destinations, and inspect scan analytics for campaigns, events, packaging, and landing pages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a ScanBlitz API key and can access QR destination and scan analytics data. <br>
Mitigation: Store SCANBLITZ_API_KEY in a secrets manager or environment file, avoid printing it, and install the skill only when ScanBlitz is trusted with that data. <br>
Risk: Update, delete, deactivate, and bulk-create commands can affect live QR campaigns. <br>
Mitigation: Review command parameters, QR identifiers, and target destinations before executing write operations. <br>
Risk: The optional QR image rendering workflow shares the ScanBlitz tracking URL with a third-party image service. <br>
Mitigation: Use that renderer only when sharing the tracking URL with the service is acceptable, or use a trusted local QR renderer instead. <br>
Risk: The optional MCP setup runs an external npm package. <br>
Mitigation: Enable the MCP server only after reviewing and trusting the package and its dependency chain. <br>


## Reference(s): <br>
- [ScanBlitz](https://scanblitz.com) <br>
- [ScanBlitz API Docs](https://scanblitz.com/api-docs) <br>
- [ScanBlitz Agent Reference](https://scanblitz.com/llms-full.txt) <br>
- [ClawHub Release Page](https://clawhub.ai/whotookmylogin/scanblitz) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with bash, JSON, and curl examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses SCANBLITZ_API_KEY and optional SCANBLITZ_API_BASE environment variables.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

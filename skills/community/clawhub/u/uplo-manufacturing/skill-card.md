## Description: <br>
AI-powered manufacturing knowledge management for searching work orders, quality inspections, production schedules, and equipment maintenance records with structured extraction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[RooJenkins](https://clawhub.ai/user/RooJenkins) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Manufacturing employees and operations teams use this skill to query plant-floor knowledge, trace quality issues, plan maintenance, and find revision-controlled procedures from their organization's UPLO-backed knowledge base. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires access to a UPLO instance and API key for MCP-backed organizational knowledge queries. <br>
Mitigation: Store tokens outside source control, prefer environment variables or a secret manager, avoid exposing credentials in screenshots, and rotate any credential that may have been exposed. <br>
Risk: Manufacturing answers may rely on confidential or restricted operational records from the connected knowledge base. <br>
Mitigation: Respect configured classification tiers and only surface information that exists in the authorized knowledge base. <br>
Risk: Outdated procedures, calibration certificates, or drawing revisions can affect quality or safety decisions. <br>
Mitigation: Check document revision levels in results and use the skill's stale-document workflow to flag obsolete records before relying on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/RooJenkins/uplo-manufacturing) <br>
- [UPLO](https://uplo.ai) <br>
- [UPLO schemas](https://uplo.ai/schemas) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with MCP tool calls, shell commands, and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs depend on the connected UPLO instance, configured MCP token, manufacturing schema pack, and available organizational knowledge.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact/skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

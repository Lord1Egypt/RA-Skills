## Description: <br>
AI-powered HR knowledge management. Search employee handbooks, org charts, company policies, benefits documentation, and onboarding materials with structured extraction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[RooJenkins](https://clawhub.ai/user/RooJenkins) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
HR, People Operations, managers, and employees use this skill to search organization-specific HR policies, benefits documents, org context, onboarding materials, and related workforce guidance. It helps answer policy questions, identify documentation gaps, and propose updates without extending policy language beyond source documents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: HR content can include restricted personnel, compensation, disciplinary, accommodation, or investigation information. <br>
Mitigation: Respect identity context and classification boundaries, confirm legitimate need to know, and route sensitive individual matters to the appropriate HR contact. <br>
Risk: Incorrect or outdated HR policy guidance can create employee harm or compliance risk. <br>
Mitigation: Use current source documents, cite policy names and effective dates, surface exceptions, and report knowledge gaps instead of extrapolating from tangential documents. <br>
Risk: The skill requires an UPLO endpoint and API key for MCP access. <br>
Mitigation: Protect API credentials, review requested permissions before installation, and inspect the skill contents and configuration in accordance with the clean security guidance. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/RooJenkins/uplo-hr) <br>
- [UPLO](https://uplo.ai) <br>
- [UPLO schemas](https://uplo.ai/schemas) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline tool calls, shell commands, and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an UPLO instance URL and API key; HR responses should cite source policy documents, effective dates, and relevant exceptions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact/skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

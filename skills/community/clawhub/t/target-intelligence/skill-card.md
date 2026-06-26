## Description: <br>
Provides target intelligence reports covering target details, drugs, pipelines, druggability, and indications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[patsnaplifescience](https://clawhub.ai/user/patsnaplifescience) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and life-science analysts use this skill to query PatSnap LifeScience MCP services and produce target intelligence reports for drug pipelines, clinical progress, patents, druggability, and indications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a PatSnap API key and user-configured MCP services. <br>
Mitigation: Use a dedicated, revocable PatSnap API key and avoid exposing MCP configuration or shell history that contains the key. <br>
Risk: Relevant biomedical queries may be sent to PatSnap services when the skill is invoked. <br>
Mitigation: Install and use the skill only when PatSnap MCP services are intended for the research workflow. <br>


## Reference(s): <br>
- [Target Intelligence on ClawHub](https://clawhub.ai/patsnaplifescience/target-intelligence) <br>
- [PatSnap Life Science](https://eureka.patsnap.com/ls-landing) <br>
- [PatSnap Dev Portal](https://open.patsnap.com/devportal) <br>
- [PatSnap Pharma Intelligence MCP Server](https://open.patsnap.com/marketplace/mcp-servers/096456) <br>
- [PatSnap Biology Modality MCP Server](https://open.patsnap.com/marketplace/mcp-servers/06e741) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown report with setup commands and structured research findings] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports are expected to include numbered sections, an abstract beginning with core conclusions, and a final conclusion grounded in retrieved data.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

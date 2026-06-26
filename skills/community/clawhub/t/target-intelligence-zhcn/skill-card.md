## Description: <br>
This skill helps agents produce Chinese biomedical target intelligence reports covering target biology, drug pipelines, clinical progress, patents, and competitive landscape analysis using PatSnap life science MCP data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[patsnaplifescience](https://clawhub.ai/user/patsnaplifescience) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and life science analysts use this skill to investigate biomedical targets, target-directed drugs, clinical trials, patents, and competitive positioning for drug discovery and development questions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a user-provided PatSnap API key for MCP access. <br>
Mitigation: Use a dedicated or scoped API key, avoid sharing logs that contain the MCP URL, monitor quota or billing, and rotate the key if exposed. <br>
Risk: Biomedical research queries and retrieved target intelligence are sent to and returned from PatSnap MCP services. <br>
Mitigation: Install and use the skill only if the organization trusts PatSnap's MCP service and is allowed to send those biomedical research queries there. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/patsnaplifescience/target-intelligence-zhcn) <br>
- [PatSnap Life Science](https://eureka.patsnap.com/ls-landing) <br>
- [PatSnap Developer Portal](https://open.patsnap.com/devportal) <br>
- [Pharma Intelligence MCP service](https://open.patsnap.com/marketplace/mcp-servers/096456) <br>
- [Biology Modality MCP service](https://open.patsnap.com/marketplace/mcp-servers/06e741) <br>
- [Chemical Molecular MCP service](https://open.patsnap.com/marketplace/mcp-servers/713886) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, API Calls, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown reports with structured Chinese sections and setup commands where needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a configured PatSnap life science MCP service and user-provided API key.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

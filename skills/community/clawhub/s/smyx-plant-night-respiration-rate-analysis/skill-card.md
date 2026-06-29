## Description: <br>
Analyzes nighttime plant canopy thermal imagery and optional CO2 readings to estimate relative respiration intensity, metabolic activity level, risks, and environmental-control suggestions for plant factories, climate chambers, and closed greenhouses. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and plant-factory operators can use this skill to send thermal image or video inputs to a provider cloud service for a structured nighttime respiration analysis report and historical report lookup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Plant media or URLs may be sent to the provider's cloud service for analysis. <br>
Mitigation: Use the skill only with media approved for provider cloud processing and review provider retention expectations before deployment. <br>
Risk: The skill can create or reuse a local account identity and store authentication tokens for later report-history queries. <br>
Mitigation: Review local token storage and identity lifecycle controls, and clear or rotate stored credentials when access should end. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-plant-night-respiration-rate-analysis) <br>
- [API documentation](references/api_doc.md) <br>
- [Skill demo](https://lifeemergence.com/sample.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or JSON-like structured analysis text, with optional saved file output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include respiration intensity, metabolic activity level, risk prompts, recommendations, report links, and cloud-sourced history tables.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter reports 1.0.3) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Diagnoses plant nutrient deficiency or excess from plant leaf images or videos using computer vision and plant physiology, then outputs structured fertilization guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agricultural operators use this skill to analyze plant leaf media for nutrient deficiency or excess and receive structured diagnosis, cause analysis, and fertilization recommendations. Agents can also use it to query cloud-hosted historical diagnosis reports associated with the current user identity. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Plant media or URLs are sent to a third-party cloud service for analysis. <br>
Mitigation: Use only media appropriate for third-party processing and review the publisher's data handling and retention practices before deployment. <br>
Risk: The skill can silently create or reuse an identity and associate cloud reports with that identity. <br>
Mitigation: Deploy only where silent account association is acceptable and disclose this behavior in the hosting agent's user-facing policy. <br>
Risk: Local account tokens may be kept in a workspace database. <br>
Mitigation: Run in a controlled workspace, restrict access to local storage, and clear workspace data when reports should no longer be accessible. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-plant-nutrition-diagnosis-analysis) <br>
- [Skill demo](https://lifeemergence.com/sample.html) <br>
- [API documentation](skills/smyx_analysis/references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or JSON analysis reports with report links and optional shell-command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include cloud report links and historical report tables.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

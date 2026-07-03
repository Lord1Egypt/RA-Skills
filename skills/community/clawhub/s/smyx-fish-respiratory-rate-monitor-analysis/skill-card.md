## Description: <br>
Analyzes aquarium camera images or videos with visible fish gill-cover motion to estimate respiratory rate, flag abnormal breathing patterns, and return structured monitoring guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, aquarists, aquarium operators, fish farms, laboratories, and developers use this skill to analyze close-range aquarium footage for fish respiratory rate, abnormal breathing alerts, and report history. It supports structured fish health monitoring guidance but is not a veterinary diagnosis or medication-planning tool. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Aquarium videos or video URLs may be sent to the lifeemergence cloud service. <br>
Mitigation: Use the skill only when that cloud processing is acceptable, and avoid footage that includes people, private spaces, or sensitive facilities. <br>
Risk: Report history is tied to an automatically selected identity with limited user control. <br>
Mitigation: Review the account and workspace context before using history queries, and avoid shared environments where report linkage is inappropriate. <br>
Risk: Authentication tokens may be stored in a local workspace database. <br>
Mitigation: Protect the workspace, review local credential storage before deployment, and remove local tokens when they are no longer needed. <br>
Risk: Respiratory-rate alerts could be mistaken for veterinary diagnosis or treatment advice. <br>
Mitigation: Treat results as visual monitoring guidance, confirm water-quality and environmental conditions, and consult a qualified aquatic veterinarian for serious or persistent concerns. <br>


## Reference(s): <br>
- [API Documentation](artifact/references/api_doc.md) <br>
- [ClawHub Skill Release](https://clawhub.ai/smyx-sunjinhui/skills/smyx-fish-respiratory-rate-monitor-analysis) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and JSON-style structured reports, with optional shell commands for analysis and history queries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May process local video files or video URLs, return report links, and write requested result files.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata; artifact frontmatter reports 1.0.4) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

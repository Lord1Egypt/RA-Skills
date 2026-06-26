## Description: <br>
Analyzes pet race start and finish media to identify false starts, lane crossings, lane assignments, finish order, and evidence clips for referee review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Event operators, referees, and developers use this skill to submit pet-race video files or URLs for objective foul-detection reports and historical report lookups. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Race media or video URLs may be sent to the Life Emergence cloud service for analysis. <br>
Mitigation: Use the skill only with media approved for external processing and review the service's data-handling expectations before deployment. <br>
Risk: The skill can silently create or reuse an internal account identity and store authentication tokens locally. <br>
Mitigation: Review identity and token storage behavior before enabling the skill in sensitive workspaces, and use an isolated workspace when testing. <br>
Risk: The security scan notes that the skill can direct users into a payment-skill flow. <br>
Mitigation: Review and supervise payment-related prompts or disable payment workflows before commercial deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-race-foul-detection-analysis) <br>
- [Skill demo](https://lifeemergence.com/sample.html) <br>
- [API documentation](references/api_doc.md) <br>
- [Analysis API documentation](skills/smyx_analysis/references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown reports and tables, JSON analysis output, and command examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include foul judgments, finish order, lane assignments, evidence locations, historical report tables, and report links.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

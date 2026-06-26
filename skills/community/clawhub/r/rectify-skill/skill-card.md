## Description: <br>
Manage tasks, columns, and documents on the Rectify platform via REST API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Umar-Lateef](https://clawhub.ai/user/Umar-Lateef) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, project teams, and OpenClaw agents use Rectify to manage AgentPulse task boards and Rectify Documents, including creating, updating, moving, searching, archiving, and deleting project content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Project token exposure could allow unauthorized access to Rectify project data. <br>
Mitigation: Keep RECTIFY_PROJECT_TOKEN private and use the least-privileged project token available. <br>
Risk: Delete, archive, and column deletion actions can remove important project tasks or documents. <br>
Mitigation: Require clear user confirmation before deleting documents, archiving document trees, deleting tasks, or deleting columns. <br>


## Reference(s): <br>
- [Rectify ClawHub skill](https://clawhub.ai/Umar-Lateef/rectify-skill) <br>
- [Rectify](https://www.rectify.so) <br>
- [Rectify AgentPulse API](https://api.rectify.so) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Shell commands, Markdown, Guidance] <br>
**Output Format:** [Markdown guidance with curl command examples and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires RECTIFY_PROJECT_TOKEN for authenticated Rectify project access.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Audit whether one imported workspace snapshot is rich enough for export, cited AI, or MCP consumption. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaojiou176](https://clawhub.ai/user/xiaojiou176) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and academic-tooling reviewers use this skill to audit imported Campus Copilot workspace snapshots for open items, evidence locations, and readiness for export, cited AI, or MCP consumption. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A workspace snapshot may contain academic or student-related information outside the user's authorization. <br>
Mitigation: Install and use the skill only for workspaces the user is allowed to audit. <br>
Risk: Snapshot evidence can be mistaken for current live browser or session state. <br>
Mitigation: Base conclusions only on imported snapshots or exported current-view artifacts, and make the evidence currency clear. <br>
Risk: Campus Copilot tooling could be run against an unintended workspace or in a way that exceeds the intended read-only scope. <br>
Mitigation: Keep the tooling scoped to the intended workspace and confirm it remains read-only during use. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only snapshot-audit guidance; does not claim live session state.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

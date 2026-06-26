## Description: <br>
Stdin/stdout file inbox/outbox bridge for passing files to/from Clawdbot using an MCP stdio server. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SafaTinaztepe](https://clawhub.ai/user/SafaTinaztepe) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill as a simple local file dropbox for moving inputs into an inbox or temporary workspace and placing deliverables in an outbox. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Files placed in the stdio folders become available for agent handling. <br>
Mitigation: Place only files intended for agent processing in those folders. <br>
Risk: Overwrite and delete operations can destructively change files inside the stdio folders. <br>
Mitigation: Review requested file operations before allowing overwrite or delete actions. <br>
Risk: Path-reporting output may reveal absolute local paths. <br>
Mitigation: Avoid sharing path output when local directory names or locations are sensitive. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Files, Text, Configuration instructions] <br>
**Output Format:** [JSON tool responses and filesystem files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [File contents are passed as base64 through the stdio read and write tools.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

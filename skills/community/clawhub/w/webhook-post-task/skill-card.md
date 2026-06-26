## Description: <br>
Sends a local JSON payload to a specified webhook endpoint and writes command output plus response status to an output file. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[askjda](https://clawhub.ai/user/askjda) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to post a selected local JSON file to a webhook endpoint from an agent workflow and capture the resulting status in stdout and a JSON output file. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send local file contents to arbitrary remote webhook URLs. <br>
Mitigation: Review the endpoint and payload path before execution, and use only trusted webhook destinations. <br>
Risk: Payload files may contain secrets, credentials, personal data, or private documents. <br>
Mitigation: Inspect and minimize payload data before sending, and avoid using this skill with sensitive content. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/askjda/webhook-post-task) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, JSON files] <br>
**Output Format:** [Command-line stdout and JSON output files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Accepts endpoint and payload file path arguments; writes status information to the configured output path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

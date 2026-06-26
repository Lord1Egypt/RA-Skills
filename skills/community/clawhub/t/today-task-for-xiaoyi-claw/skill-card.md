## Description: <br>
Pushes completed task results and related task metadata to Huawei Xiaoyi's negative-screen service using a standardized JSON format. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ganhaiyang3](https://clawhub.ai/user/ganhaiyang3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill after an agent task completes to package the task name, result, Markdown content, and timestamp into the service's expected push payload. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Task results and metadata are sent to the hardcoded Huawei Xiaoyi endpoint. <br>
Mitigation: Install only when that data flow is intended, and avoid including sensitive personal, business, or secret data in task content. <br>
Risk: Credentials are handled through a plaintext .xiaoyienv file and may be exposed through console output, verbose logs, or local records. <br>
Mitigation: Protect or avoid the plaintext credential file, limit log verbosity, review local records, and clean logs and push records after use. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON examples and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces task push payload guidance and command-line usage; runtime scripts may create local logs and push records.] <br>

## Skill Version(s): <br>
1.0.26 (source: server release evidence and artifact/version.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

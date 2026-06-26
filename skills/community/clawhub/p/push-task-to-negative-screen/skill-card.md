## Description: <br>
Pushes completed task results to a negative-screen endpoint using a standard JSON format for task content, metadata, and completion status. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ganhaiyang3](https://clawhub.ai/user/ganhaiyang3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and developers use this skill to package completed task output as JSON or Markdown and push it to a negative-screen notification endpoint. It is intended for task-completion notifications and result delivery workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Task content and metadata are transferred to an external fixed Huawei endpoint, and the authoritative security summary says external data transfer is not clearly or consistently disclosed. <br>
Mitigation: Install only if the endpoint is trusted, avoid pushing sensitive task content, and use dry-run or validation-only flows when testing. <br>
Risk: The authoritative security guidance flags credential handling and local stdout or log capture as needing review before shared, CI, or production use. <br>
Mitigation: Use the skill only in trusted local environments until credential handling is reviewed or patched, and manage log and push-record retention according to the data sensitivity. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ganhaiyang3/push-task-to-negative-screen) <br>
- [README.md](artifact/README.md) <br>
- [SECURITY.md](artifact/SECURITY.md) <br>
- [UPDATE_SYSTEM.md](artifact/UPDATE_SYSTEM.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with JSON payload examples and shell commands; push responses are JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May transmit task content and metadata to a fixed Huawei endpoint and may save local logs or push records.] <br>

## Skill Version(s): <br>
1.0.21 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

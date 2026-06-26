## Description: <br>
AI 速记敏捷助手 helps sales, procurement, and office users capture fragmented business notes, improve note quality with AI, search by intent, and generate periodic business insight summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[iliubo1104-sketch](https://clawhub.ai/user/iliubo1104-sketch) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Employees in sales, procurement, and operations use this skill to add local business notes, search past notes by intent, and generate business insight reports with a configured OpenAI-compatible AI endpoint. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Notes are stored locally in plaintext and may contain sensitive personal, account, or business information. <br>
Mitigation: Do not store passwords, API keys, regulated data, or confidential business secrets unless the machine and workflow are approved for that data. <br>
Risk: Note contents or note history can be sent to the configured AI endpoint during quality checks, search, or analysis. <br>
Mitigation: Use only approved AI providers and review the configured endpoint before entering sensitive or business-critical notes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/iliubo1104-sketch/snap-notes) <br>
- [README](README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [CLI text output and local JSONL note records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores notes locally in the OpenClaw workspace and can call a configured OpenAI-compatible AI endpoint.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

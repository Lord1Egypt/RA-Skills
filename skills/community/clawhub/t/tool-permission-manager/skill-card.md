## Description: <br>
Tools permission management: fine-grained control over which tools an agent may use. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[soroyue](https://clawhub.ai/user/soroyue) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to classify tool access into public, warning, approval, and forbidden levels before an agent invokes tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill describes dynamic authorization for powerful tools without a precise enforcement policy. <br>
Mitigation: Use it only with an agent platform that enforces tool permissions independently of the skill text. <br>
Risk: The skill includes privileged tool categories such as command execution, file writes, messaging, scheduled tasks, sessions, gateway configuration, and file deletion. <br>
Mitigation: Require explicit confirmation and a structured permission policy before enabling these privileged tool categories. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration] <br>
**Output Format:** [Markdown with JSON configuration example] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only guidance for assigning tool permission levels.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

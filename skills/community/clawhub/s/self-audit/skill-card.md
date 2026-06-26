## Description: <br>
Track, analyze, and score tool calls to identify unnecessary usage, detect patterns, and get recommendations for efficiency improvements. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiuge897](https://clawhub.ai/user/jiuge897) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use Self Audit to log and analyze tool invocations, measure necessity and efficiency, and receive recommendations for reducing reflexive tool use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local audit logs may retain tool names, inputs, reasons, and context that include sensitive data. <br>
Mitigation: Avoid recording secrets, tokens, personal data, or proprietary prompts, and periodically review or delete the audit directory. <br>
Risk: The reviewed package references a self-audit CLI script that is not included in the artifact. <br>
Mitigation: Verify the source and behavior of any self-audit executable before running commands from this skill. <br>


## Reference(s): <br>
- [Self Audit on ClawHub](https://clawhub.ai/jiuge897/self-audit) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown-style text reports with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local audit logs when the referenced CLI workflow is available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

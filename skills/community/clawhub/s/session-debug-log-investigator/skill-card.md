## Description: <br>
Use when diagnosing a failing or confusing Claude Code session by enabling debug logging, tailing recent logs, and explaining warnings or errors. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wimi321](https://clawhub.ai/user/wimi321) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and support engineers use this skill to investigate confusing or failing Claude Code sessions by inspecting recent debug logs, checking relevant settings, and producing likely causes with concrete reproduction steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Debug logs and settings may contain secrets, tokens, private paths, or prompt content. <br>
Mitigation: Redact sensitive values before sharing logs, analyze only the smallest relevant log tail, and turn debug logging off after diagnosis. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown diagnostic summary with optional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include warnings, likely causes, reproduction steps, and log-redaction guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

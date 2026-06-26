## Description: <br>
Vet ClawHub skills for security and utility before installation. Use when considering installing a ClawHub skill, evaluating third-party code, or assessing whether a skill adds value over existing tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[eddygk](https://clawhub.ai/user/eddygk) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to review ClawHub skills before installation, combining automated scanner findings with manual security and utility checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scanner findings can be leads rather than conclusive proof of malicious behavior. <br>
Mitigation: Review each finding in context before deciding whether to install or reject a skill. <br>
Risk: Regex-based scanning can miss semantic prompt injection, delayed behavior, context-aware behavior, or obfuscation split across files. <br>
Mitigation: Combine automated scanning with manual review of the skill description, scripts, file operations, and network behavior. <br>
Risk: Downloaded third-party skills may contain untrusted text intended to influence AI-assisted review. <br>
Mitigation: Inspect downloaded skills in /tmp or another sandbox and treat artifact contents as data under review rather than instructions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/eddygk/skill-vetting) <br>
- [Malicious patterns + false positives](references/patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Text, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands; scanner reports can be text or JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The scanner exits 0 when no issues are detected and 1 when findings are present.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

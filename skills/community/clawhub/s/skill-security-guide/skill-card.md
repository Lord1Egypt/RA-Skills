## Description: <br>
Security best practices guide for creating or reviewing ClawHub skills so they meet security standards and pass scans with benign ratings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wszhhx](https://clawhub.ai/user/wszhhx) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and skill authors use this guide to check ClawHub skill metadata, credential handling, security-sensitive code patterns, and documentation consistency before publishing or reviewing a skill. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may apply the guide to real skills without independently inspecting scripts, credentials, API calls, or install steps. <br>
Mitigation: Review each target skill's source files and run the ClawHub security scan before deployment. <br>
Risk: Documentation-code mismatches can cause a skill to parse API responses or status values incorrectly. <br>
Mitigation: Test against real API responses and keep documented response fields, status values, and error handling aligned with implementation. <br>
Risk: Credential examples can lead to accidental secret disclosure if copied without care. <br>
Mitigation: Check only whether credential variables are present and avoid printing secret values or substrings. <br>


## Reference(s): <br>
- [Skill Security Guide on ClawHub](https://clawhub.ai/wszhhx/skill-security-guide) <br>
- [ClawHub Security Documentation](https://clawhub.ai/docs/security) <br>
- [Related skill-creator-2 Skill](https://clawhub.ai/yixinli867/skill-creator-2) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with YAML, Python, PowerShell, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only; no executable scripts or required environment variables.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

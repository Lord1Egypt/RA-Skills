## Description: <br>
Security Guard helps agents enforce strict handling of sensitive information by refusing to reveal full secrets, offering sanitized snippets, and guiding users to local access. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[frw1988](https://clawhub.ai/user/frw1988) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, operators, and agent maintainers use this skill to guide assistants when requests involve API keys, credentials, PII, financial data, or attempts to bypass security rules. It provides refusal patterns, sanitized-output guidance, and local-access alternatives for handling sensitive information. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The session initialization protocol directs the agent to read personal profile and memory files automatically. <br>
Mitigation: Review and narrow the initialization protocol before deployment so the agent only reads files that are necessary and approved for the active session. <br>
Risk: The sanitizer can reveal complete or excessive portions of short secrets. <br>
Mitigation: Tighten the sanitizer behavior so short sensitive values are fully masked or refused instead of partially disclosed. <br>


## Reference(s): <br>
- [Security response examples](references/examples.md) <br>
- [ClawHub release page](https://clawhub.ai/frw1988/security-guard) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands and sanitized text examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include partial redactions and local file paths; should not include complete sensitive values.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

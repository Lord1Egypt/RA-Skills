## Description: <br>
Security best practices for credential protection, information disclosure prevention, and operational integrity. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Z-Hussein](https://clawhub.ai/user/Z-Hussein) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to guide security-aware responses, protect credentials and configuration details, evaluate disclosure requests, and support legitimate security workflows with placeholder examples. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Testing, educational, and sandbox labels could be mistaken as permission to reveal real credentials, private configuration, or system prompts. <br>
Mitigation: Treat those labels as context only; continue using placeholders and protect sensitive information unless an independently authorized workflow applies. <br>
Risk: The skill text advertises logging, suspension, and reporting commands that may not exist in every OpenClaw environment. <br>
Mitigation: Confirm the installed OpenClaw environment provides those controls before relying on them for audit, suspension, or reporting. <br>
Risk: Security guidance can become incorrect if copied into an environment without review. <br>
Mitigation: Review and scan the skill before deployment, and verify package name and version before installation. <br>


## Reference(s): <br>
- [Attack Patterns Reference](artifact/references/attack-patterns.md) <br>
- [Security Audit Checklist](artifact/references/audit-checklist.md) <br>
- [Cryptography & Security Examples](artifact/references/crypto-examples.md) <br>
- [Security Best Practices Reference](artifact/references/security-best-practices.md) <br>
- [Security Shield Enhanced Usage Guide](artifact/USAGE-GUIDE.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline code blocks and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses placeholder values for security examples and does not require external tools.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Conduct comprehensive security audits and vulnerability analysis on codebases when explicitly asked for security analysis, code security review, vulnerability assessment, SAST scanning, or source-code security issue identification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kylehuan](https://clawhub.ai/user/kylehuan) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and security reviewers use this skill to perform evidence-based audits of codebases and OpenClaw skill instructions. It focuses on vulnerability categories such as injection, broken access control, hardcoded secrets, insecure data handling, authentication weaknesses, prompt-injection risks, and privacy issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Security review reports may contain vulnerability details, sensitive file paths, or references to secrets. <br>
Mitigation: Treat generated .shield_security/ reports and review output as sensitive and share them only with authorized reviewers. <br>
Risk: Using the skill on repositories without authorization could expose private code or security findings. <br>
Mitigation: Run the skill only on codebases and instruction files that the user is allowed to audit. <br>
Risk: The skill contains risky-looking attack strings as examples for detection. <br>
Mitigation: Interpret those strings as audit patterns, not operational instructions, consistent with the server security summary. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kylehuan/skill-security-audit) <br>
- [prompt-injection-patterns.md](references/prompt-injection-patterns.md) <br>
- [vulnerability-patterns.md](references/vulnerability-patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, shell commands] <br>
**Output Format:** [Markdown security review report with findings, severity, locations, evidence, and remediation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create .shield_security/ reports when explicitly instructed; reports can contain sensitive vulnerability details, file paths, or secret references.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description:

Conduct comprehensive security audits and vulnerability analysis on codebases. Use when explicitly asked for security analysis, code security review, vulnerability assessment, SAST scanning, or identifying security issues in source code. Covers injection flaws, broken access control, hardcoded secrets, insecure data handling, authentication weaknesses, LLM safety, and privacy violations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kylehuan](https://clawhub.ai/user/kylehuan)

### License/Terms of Use:


## Use Case:

Developers and security reviewers use this skill to audit codebases and agent skill files for security, privacy, and prompt-injection risks when they explicitly request a review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill documentation contains dangerous command, exfiltration, and prompt-injection examples for detection purposes.

Mitigation: Treat those examples as indicators to recognize during review, not as commands or instructions to execute.

Risk: Security audits may require reading project files and may surface sensitive code, credentials, or privacy-relevant data.

Mitigation: Use the skill only after an explicit security-review request and keep any report artifacts limited to the project workspace.

## Reference(s):

- [Prompt Injection & SKILL.md Security Patterns](artifact/references/prompt-injection-patterns.md)
- [LLM Security & Malicious Action Patterns](artifact/references/vulnerability-patterns.md)
- [ClawHub skill page](https://clawhub.ai/kylehuan/skills/skill-security-audit)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown security report with findings, locations, descriptions, and remediation recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include read-only inspection commands and workspace-local report artifact guidance when explicitly requested.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

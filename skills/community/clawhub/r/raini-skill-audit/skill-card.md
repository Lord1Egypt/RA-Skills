## Description:

Scans OpenClaw skill packages for suspicious code patterns that may indicate credential access, data exfiltration, dynamic code execution, or other supply-chain risks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xraini](https://clawhub.ai/user/0xraini)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent users use this skill to audit OpenClaw skills before installation or execution by scanning local or installed skill directories and reviewing a risk-scored report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recursive scans can follow symlinks outside the intended skill directory and print matching file snippets.

Mitigation: Scan only trusted directories or run the scanner in a sandbox when auditing untrusted packages; review package symlinks before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/0xraini/skills/raini-skill-audit)
- [OWASP LLM Top 10](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
- [Moltbook Security Discussion](https://www.moltbook.com/post/cbd6474f-8478-4894-95f1-7b104a73bcd5)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Console text and Markdown-style reports with file, severity, finding, context, risk score, and recommendation sections.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Security evidence verdict: suspicious. No server security evidence showed malware or remote exfiltration, but untrusted packages should be scanned in a sandbox because recursive scans may follow symlinks outside the intended directory and print matched file snippets.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

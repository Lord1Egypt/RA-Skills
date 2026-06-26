## Description: <br>
Scans OpenClaw skills for security vulnerabilities and suspicious patterns before installation <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anikrahman0](https://clawhub.ai/user/anikrahman0) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and skill reviewers use this skill to inspect OpenClaw skill files or directories for suspicious instruction patterns before installation. It produces findings that support manual security review rather than a definitive security verdict. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The scanner can report false positives because it uses pattern matching on skill text. <br>
Mitigation: Review each finding in context and confirm whether the flagged instruction is actually unsafe before acting on the recommendation. <br>
Risk: A clean scan is not a definitive security verdict. <br>
Mitigation: Use the report as one input to manual review, especially for skills that request system access, credentials, downloads, or network activity. <br>
Risk: Recursive scans read markdown, JavaScript, and TypeScript files under the path provided. <br>
Mitigation: Scan specific skill files or narrow directories when possible, and avoid pointing the scanner at unrelated broad paths. <br>


## Reference(s): <br>
- [Security Skill Scanner on ClawHub](https://clawhub.ai/anikrahman0/security-skill-scanner) <br>
- [Publisher profile](https://clawhub.ai/user/anikrahman0) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown-style security report with risk levels, findings, summaries, and recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include optional whitelist configuration guidance and command-line usage examples.] <br>

## Skill Version(s): <br>
2.0.0 (source: frontmatter, package.json, CHANGELOG, released 2026-02-16) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

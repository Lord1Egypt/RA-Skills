## Description: <br>
Security scanner for ClawHub skills that detects malicious code, obfuscated payloads, and social engineering before installation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sypsyp97](https://clawhub.ai/user/sypsyp97) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to audit third-party ClawHub skills before installation or to review installed skill directories for suspicious shell, markdown, Python, or JavaScript content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is a shell-based auditor, so execution depends on the local shell environment and the target path or fetched skill content. <br>
Mitigation: Run it only against specific skill directories or known ClawHub skill names, and do not run it with sudo. <br>
Risk: The audit report is a helper and does not provide a complete security guarantee. <br>
Mitigation: Use the results as one review input, and manually inspect high or medium findings before installing or updating a skill. <br>
Risk: Suspicious snippets may be exported to /tmp/skill-audit-*-suspicious.txt for manual review. <br>
Mitigation: Treat exported snippets as untrusted and delete the temporary file after review. <br>
Risk: Optional LLM intent analysis requires a separate Gemini CLI or manual agent review step. <br>
Mitigation: Do not assume LLM analysis has run unless the required tool is available and the suspicious snippet review was completed. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/sypsyp97/skill-auditor-pro) <br>
- [341 Malicious ClawHub Skills Incident](https://thehackernews.com/2026/02/researchers-find-341-malicious-clawhub.html) <br>
- [OpenClaw Security Guide](https://docs.openclaw.ai/gateway/security) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Shell commands, Guidance, Text] <br>
**Output Format:** [Terminal text report with severity-labeled findings and verdicts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write suspicious-code snippets to a temporary /tmp/skill-audit-*-suspicious.txt file for manual review.] <br>

## Skill Version(s): <br>
2.1.1 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Runtime security layer for OpenClaw agents that scans untrusted input and agent output for prompt injection, data exfiltration, credential leaks, suspicious commands, and social engineering before the agent or user consumes the content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Oleglegegg](https://clawhub.ai/user/Oleglegegg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to add local runtime checks around OpenClaw agents that process untrusted external content or may emit sensitive data. It provides shell-based input scanning, output monitoring, canary-token leak detection, and audit-log viewing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Clean-mode redaction can make unsafe content appear safe if users treat sanitized text as proof of safety. <br>
Mitigation: Treat --clean as best-effort redaction and prefer fail-closed blocking for untrusted content, especially in production workflows. <br>
Risk: Audit logs may contain prompt, output, or secret snippets captured during threat detection. <br>
Mitigation: Protect access to ~/.sentinel logs, set an appropriate SENTINEL_LOG location, and rotate or delete logs according to the deployment's retention policy. <br>
Risk: Modified premium pattern files or scripts can change what the filter detects or suppresses. <br>
Mitigation: Only install or modify Sentinel scripts and premium pattern files from trusted sources and review changes before production use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Oleglegegg/sentinel-oleg) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and optional JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local shell scripts emit pass, warning, or block results and may append JSONL audit entries under the configured Sentinel log path.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata; artifact frontmatter: 1.0.4) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

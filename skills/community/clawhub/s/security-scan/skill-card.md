## Description: <br>
Security review workflow for OpenClaw skills and other small code folders. Use when auditing a skill before publishing or installing it, checking for dangerous code patterns, possible hardcoded secrets, risky file permissions, or lightweight supply-chain concerns. Best for quick static review and cautious go/no-go recommendations, not full malware analysis or sandbox forensics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ShadowLoong](https://clawhub.ai/user/ShadowLoong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and reviewers use this skill to perform a quick static security pass on OpenClaw skills, script bundles, or small code folders before publishing, installing, or trusting them. It helps summarize dangerous code patterns, likely hardcoded credentials, risky file permissions, and practical next steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The scanner is lightweight and heuristic, so it can miss risky behavior or flag benign code as suspicious. <br>
Mitigation: Treat results as review signals, manually inspect matched code, and use stronger manual or sandboxed analysis when higher assurance is required. <br>
Risk: Raw scan output can expose private paths, code snippets, or suspected credentials from the reviewed directory. <br>
Mitigation: Run it only on directories intended for inspection and redact sensitive output before sharing results. <br>


## Reference(s): <br>
- [ClawHub Security Scan skill page](https://clawhub.ai/ShadowLoong/security-scan) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and concise text risk summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are heuristic review signals and may include matched file paths, code snippets, or suspected credential strings from the scanned target.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

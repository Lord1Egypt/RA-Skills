## Description: <br>
Skill Audit Pro scans installed OpenClaw skills for security issues and produces recurring security reports for configured messaging channels. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ohmanymoneygomyhome-creator](https://clawhub.ai/user/ohmanymoneygomyhome-creator) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to statically scan OpenClaw skills for hardcoded credentials, shell-injection patterns, environment leakage, network exfiltration patterns, and related findings before or after installation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recurring scans and reports may reveal installed skill names, file locations, and security findings to configured messaging channels. <br>
Mitigation: Review channel recipients and local configuration before installation; use only where those reports are acceptable to share. <br>
Risk: The release prepares reports for discovered messaging channels and does not clearly document recipient selection or disable controls. <br>
Mitigation: Prefer a version with explicit opt-in scheduling, recipient selection, redaction, and a documented way to disable background scans. <br>
Risk: Static pattern scans can produce false positives or miss context-specific vulnerabilities. <br>
Mitigation: Treat findings as review prompts and confirm each result before uninstalling or trusting a scanned skill. <br>


## Reference(s): <br>
- [Skill Security Audit Reference](references/security-checks.md) <br>
- [ClawHub skill page](https://clawhub.ai/ohmanymoneygomyhome-creator/skill-audit-pro) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/ohmanymoneygomyhome-creator) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown-style security report text and command-line scanner output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports include severity counts, findings, recommendations, and configured-channel routing metadata.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
System Auditor helps agents run a lightweight local system audit covering host details, SSH and firewall posture, fail2ban status, and a kernel-module CVE check. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kingaiwork](https://clawhub.ai/user/kingaiwork) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill through an agent to collect lightweight local host and security-posture diagnostics during troubleshooting or review. Its output is useful for orientation, not for formal compliance or comprehensive vulnerability assessment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Audit output can reveal host configuration and security posture. <br>
Mitigation: Treat generated reports as sensitive and share them only through trusted channels. <br>
Risk: The skill's compliance, benchmark, and CVE claims are broader than the fixed lightweight checks in the artifact. <br>
Mitigation: Use the output for orientation and follow up with dedicated compliance, benchmark, or vulnerability tooling before making security decisions. <br>
Risk: Local diagnostic commands may return incomplete results when tools are missing or permissions are limited. <br>
Mitigation: Run it in the intended environment, review missing fields, and confirm findings with system-native administration tools. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/kingaiwork/system-auditor) <br>


## Skill Output: <br>
**Output Type(s):** [text, configuration, guidance] <br>
**Output Format:** [JSON emitted by a Python command-line script, with agent-facing summaries typically rendered as text or Markdown.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs fixed local diagnostic commands and may include host configuration and security-posture details.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence; artifact skill.json reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

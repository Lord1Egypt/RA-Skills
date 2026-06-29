## Description: <br>
Vps Security Audit helps an agent inspect a Linux VPS for firewall, intrusion-detection, open-port, SSH, update, and hardening signals, then produce a scored security report with fix recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kingaiwork](https://clawhub.ai/user/kingaiwork) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers, operators, and VPS administrators use this skill to ask an agent to run read-only Linux host checks and summarize the server's security posture. It is intended for systems the user administers and can expose sensitive host details in the report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The generated report may include sensitive host details such as SSH settings, firewall rules, open ports, package/update state, and login history. <br>
Mitigation: Run the skill only on systems the user administers and avoid sharing the full report publicly. <br>
Risk: Some checks require root or sudo privileges and may fail or return incomplete information under lower-privilege accounts. <br>
Mitigation: Treat missing command output as incomplete evidence and skip failed checks gracefully rather than assuming the host is secure. <br>
Risk: The score is a reference guide and does not replace a professional security audit. <br>
Mitigation: Use the score to prioritize follow-up review and have qualified personnel validate high-risk findings before making operational decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kingaiwork/skills/vps-security-audit) <br>
- [Publisher profile](https://clawhub.ai/user/kingaiwork) <br>
- [King AI Works homepage](https://kingai.work/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown security report with command output summaries, scores, and fix recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include host-sensitive details such as SSH settings, firewall rules, package/update state, open ports, and login history.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

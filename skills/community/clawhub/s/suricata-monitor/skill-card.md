## Description: <br>
Read and triage Suricata IDS/IPS alerts from eve.json into structured threat reports with severity-ranked findings, attacker IPs, top triggered signatures, and recommended blocks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[infectit007](https://clawhub.ai/user/infectit007) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security operators use this skill to summarize recent Suricata IDS/IPS alerts from eve.json into an actionable threat snapshot, including severity counts, top attacker IPs, top signatures, recommended response steps, and GREEN/YELLOW/RED status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: IDS findings may be sent to Telegram or appended to local memory despite local-only privacy claims. <br>
Mitigation: Enable Telegram delivery only when exporting IDS findings to a third party is approved, and restrict access to retained report files. <br>
Risk: Broad log read permissions may expose Suricata security logs. <br>
Mitigation: Prefer least-privilege access for the agent or service account instead of making logs broadly readable. <br>
Risk: Recommended firewall block commands may disrupt legitimate traffic if applied without review. <br>
Mitigation: Review attacker IPs, signatures, and business impact before applying block commands. <br>
Risk: Daily scheduling can repeatedly transmit and retain sensitive security reports. <br>
Mitigation: Add the cron job only when recurring reporting and retention are intended, and review secret handling for Telegram credentials. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/infectit007/suricata-monitor) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown threat report with Python and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include firewall block recommendations, Telegram delivery instructions, memory append instructions, and daily cron scheduling guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

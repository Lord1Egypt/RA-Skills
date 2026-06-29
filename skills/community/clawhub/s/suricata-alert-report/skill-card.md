## Description: <br>
Reads Suricata IDS/IPS alert logs from /var/log/suricata/, aggregates alerts by severity, source IP, and signature, checks sensor status, and produces a Chinese incident briefing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kingaiwork](https://clawhub.ai/user/kingaiwork) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
SOC analysts, security engineers, and incident responders use this skill to inspect Suricata alert logs, summarize severity, source IP, signature, category, protocol, and sensor health, and generate a Chinese-language incident briefing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated reports may contain sensitive IDS data, including internal or external IPs, alert signatures, interfaces, and security volumes. <br>
Mitigation: Run the skill only on approved hosts and review reports before sharing them outside the security team. <br>
Risk: The report template includes promotional links in the footer. <br>
Mitigation: Review and remove promotional footer content before using reports in formal incident, compliance, or customer-facing communications. <br>


## Reference(s): <br>
- [Kingai.work homepage](https://kingai.work/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown incident briefing with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports may include sensitive IDS alert details such as IP addresses, signatures, interfaces, and alert volumes.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

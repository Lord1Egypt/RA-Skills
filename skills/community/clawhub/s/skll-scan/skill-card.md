## Description: <br>
A local static scanner for OpenClaw Skills that detects risky code patterns, extracts referenced domains, and generates risk reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[niuqun2003](https://clawhub.ai/user/niuqun2003) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to run pre-installation or audit scans of OpenClaw Skills and review local risk reports before distribution or installation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The scanner may overstate its threat-intelligence protection and give users more confidence than the code supports. <br>
Mitigation: Treat results as lightweight local static analysis and pair them with manual review or stronger security tooling before installing or distributing a skill. <br>
Risk: Scan reports and optional lookup examples can expose code snippets, paths, secrets, or confidential indicators. <br>
Mitigation: Avoid scanning code that contains secrets unless you control or delete the generated /tmp report, and do not send internal or customer indicators to third-party lookup APIs without approval. <br>


## Reference(s): <br>
- [Threat Intelligence APIs Reference](references/threat-intel-apis.md) <br>
- [Abuse.ch URLhaus API](https://urlhaus-api.abuse.ch/) <br>
- [AbuseIPDB API](https://www.abuseipdb.com/api) <br>
- [VirusTotal API](https://www.virustotal.com/api/) <br>
- [AlienVault OTX API](https://otx.alienvault.com/api) <br>
- [Google Safe Browsing API](https://safebrowsing.googleapis.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown-style guidance with shell commands, scanner report text, and an optional JSON report file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local scan reports under /tmp/skill-scan-<skill>.json when the scanner is executed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

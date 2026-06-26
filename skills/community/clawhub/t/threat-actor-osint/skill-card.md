## Description: <br>
Build comprehensive threat actor profiles using open-source intelligence techniques to document adversary motivations, capabilities, infrastructure, and TTPs for proactive defense. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ling-qian](https://clawhub.ai/user/ling-qian) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Security analysts, threat intelligence teams, and detection engineers use this skill to gather public-source intelligence, map actor TTPs to MITRE ATT&CK, correlate infrastructure, and produce structured threat actor dossiers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Searched actor names, domains, IP addresses, hashes, or other IOCs may be sent to third-party OSINT services. <br>
Mitigation: Confirm investigative approval before use, avoid sensitive investigations without an approved workflow, and prefer offline or private data sources when confidentiality is required. <br>
Risk: The skill requires sensitive credentials for OSINT providers such as AlienVault OTX, VirusTotal, Shodan, and Malpedia. <br>
Mitigation: Store API keys in approved secret management systems, avoid hardcoding credentials in prompts or files, use least-privilege keys where supported, and rotate keys after exposure. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ling-qian/threat-actor-osint) <br>
- [API Reference: Threat Actor Profiling from OSINT](references/api-reference.md) <br>
- [SpiderFoot OSINT Tool](https://github.com/smicallef/spiderfoot) <br>
- [MITRE ATT&CK Groups](https://attack.mitre.org/groups/) <br>
- [MITRE Enterprise ATT&CK STIX Data](https://raw.githubusercontent.com/mitre/cti/master/enterprise-attack/enterprise-attack.json) <br>
- [AlienVault OTX Pulse Search API](https://otx.alienvault.com/api/v1/pulses/search?q={group_name}&limit=10) <br>
- [VirusTotal Intelligence Search API](https://www.virustotal.com/api/v3/intelligence/search) <br>
- [Shodan Host API](https://api.shodan.io/shodan/host/{ip}) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with Python and shell code examples, plus generated STIX JSON and threat actor dossier files when workflows are run.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require API keys for third-party OSINT services and network access to public threat intelligence sources.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

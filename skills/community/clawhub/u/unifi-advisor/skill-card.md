## Description: <br>
Read-only UniFi network advisor for querying Site Manager and Network Integration API data about devices, clients, networks, firewall policies, VPN tunnels, ISP metrics, and related state. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[arseni-mik](https://clawhub.ai/user/arseni-mik) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Network administrators and support engineers use this skill to inspect UniFi environments, answer status and configuration questions, and get read-only troubleshooting guidance without making changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a UniFi API key that can read network inventory through api.ui.com. <br>
Mitigation: Use the least-privilege key available, avoid shared machines for sensitive environments, and do not expose API keys in responses. <br>
Risk: The skill caches site metadata locally at ~/.openclaw/unifi-skill.json. <br>
Mitigation: Delete the cache file when local site metadata should not remain on disk and protect the host account where the cache is stored. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/arseni-mik/unifi-advisor) <br>
- [UniFi API Endpoint](https://api.ui.com) <br>
- [UniFi Account and API Key Setup](https://unifi.ui.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON command output summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses GET-only UniFi API calls through python3 and requires UNIFI_API_KEY.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

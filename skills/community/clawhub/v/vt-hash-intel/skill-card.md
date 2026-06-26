## Description: <br>
Instantly check if a file, URL, domain, or IP is malicious using VirusTotal, returning detection ratios, contextual threat intelligence, VirusTotal report links, and actionable recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Bryan-Project](https://clawhub.ai/user/Bryan-Project) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Security analysts, incident responders, threat hunters, and SOC operators use this skill to enrich hashes, URLs, domains, and IP addresses with VirusTotal context during triage and investigation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queried hashes, URLs, domains, and IP addresses are sent to VirusTotal. <br>
Mitigation: Only submit indicators your organization permits sharing; avoid confidential internal URLs, private hostnames, customer-linked indicators, or sensitive incident details. <br>
Risk: The skill requires a VirusTotal API key and can encounter authentication errors or rate limits. <br>
Mitigation: Provide VT_API_KEY through the agent environment, restrict access to that secret, and expect retries or waits for quota-limited keys. <br>
Risk: A clean or not-found VirusTotal result does not prove an indicator is safe. <br>
Mitigation: Treat VirusTotal results as one signal and corroborate with sandboxing, endpoint data, or other threat intelligence sources before making security decisions. <br>


## Reference(s): <br>
- [VirusTotal API v3](https://www.virustotal.com/api/v3) <br>
- [VirusTotal URL API Reference](https://docs.virustotal.com/reference/url) <br>
- [VirusTotal API Key](https://www.virustotal.com/gui/my-apikey) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown threat report informed by JSON lookup results and shell command execution] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires VT_API_KEY and sends queried indicators to VirusTotal.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata; artifact frontmatter reports 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

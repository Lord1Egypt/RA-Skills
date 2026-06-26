## Description: <br>
Scan files, URLs, domains, and IP addresses with the VirusTotal Public API v3 for malware analysis and threat intelligence. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[arf0nz0](https://clawhub.ai/user/arf0nz0) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security analysts use this skill to run VirusTotal Public API v3 checks for files, URLs, domains, IP addresses, and analysis status while preserving credential hygiene and requiring user consent before submissions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Files, URLs, domains, and IP addresses sent to VirusTotal may be shared with VirusTotal and its security partners. <br>
Mitigation: Warn the user before each request, require explicit confirmation, prefer hash lookups for files, and avoid confidential, internal, or regulated data unless authorized. <br>
Risk: The skill requires a sensitive VirusTotal API key. <br>
Mitigation: Load the key from a local secrets file with restrictive permissions and never display, hardcode, or echo credentials in tool output. <br>
Risk: Free-tier VirusTotal requests are rate limited. <br>
Mitigation: Handle 429 responses by waiting before retrying and avoid bulk workflows that exceed the documented free-tier limit. <br>


## Reference(s): <br>
- [VirusTotal Public API v3 Overview](https://docs.virustotal.com/reference/overview) <br>
- [VirusTotal API Key Setup](https://www.virustotal.com/gui/my-apikey) <br>
- [ClawHub Skill Page](https://clawhub.ai/arf0nz0/virustotal3) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API Calls] <br>
**Output Format:** [Markdown with inline bash commands and JSON response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses curl with a VirusTotal API key and returns VirusTotal API JSON for agent interpretation.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter, CHANGELOG, server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

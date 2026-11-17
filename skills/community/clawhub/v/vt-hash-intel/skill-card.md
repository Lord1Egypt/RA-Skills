## Description:

Instantly checks file hashes, URLs, domains, and IP addresses with VirusTotal and returns threat intelligence for SOC triage, incident response, malware analysis, and IOC enrichment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bryan-project](https://clawhub.ai/user/bryan-project)

### License/Terms of Use:

MIT

## Use Case:

Security analysts, incident responders, threat hunters, and developers use this skill to enrich suspicious hashes, URLs, domains, and IP addresses with VirusTotal detections, reputation data, infrastructure context, and actionable recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Indicators submitted for lookup are sent to VirusTotal using the configured VT_API_KEY.

Mitigation: Submit only indicators approved for third-party services, and avoid internal-only, customer-sensitive, embargoed, or investigation-sensitive IOCs unless organizational policy allows it.

Risk: A clean VirusTotal result does not guarantee that an indicator is safe.

Mitigation: Treat VirusTotal as one signal and corroborate clean or not-found results with additional threat intelligence sources and internal telemetry before making security decisions.

## Reference(s):

- [VirusTotal API v3](https://www.virustotal.com/api/v3)
- [VirusTotal URL API Reference](https://docs.virustotal.com/reference/url)
- [VirusTotal API Key](https://www.virustotal.com/gui/my-apikey)
- [ClawHub Skill Page](https://clawhub.ai/bryan-project/skills/vt-hash-intel)

## Skill Output:

**Output Type(s):** [Analysis, API Calls, Shell commands, JSON, Markdown, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON lookup results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires VT_API_KEY and sends submitted indicators to VirusTotal.]

## Skill Version(s):

1.0.2 (source: ClawHub release metadata; artifact frontmatter reports 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

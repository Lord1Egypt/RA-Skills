## Description:

Provides agent guidance and curl examples for using the VirusTotal Public API v3 to scan or look up files, URLs, domains, and IP addresses for malware analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[arf0nz0](https://clawhub.ai/user/arf0nz0)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, security analysts, and external users can use this skill to guide malware, URL, domain, and IP reputation checks through VirusTotal. It is best suited for workflows where users can explicitly approve third-party data sharing before any lookup or submission.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented credential-loading pattern sources a secrets file as shell code and may expose the API key through temporary header files.

Mitigation: Prefer a native secret store or a strict parser for VIRUSTOTAL_API_KEY, and ensure any temporary credential files are permission-restricted and cleaned up unconditionally.

Risk: Submitting files, URLs, domains, or IP addresses to VirusTotal can share those artifacts or investigation interests with VirusTotal and its security partners.

Mitigation: Require explicit user confirmation before every outbound lookup or submission, and prefer hash lookups over file uploads for sensitive materials.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/arf0nz0/skills/virustotal3)
- [VirusTotal API v3 documentation](https://docs.virustotal.com/reference/overview)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline bash/curl examples and JSON response shapes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and a VirusTotal API key; VirusTotal free-tier usage is documented as 4 requests per minute.]

## Skill Version(s):

1.0.1 (source: frontmatter, changelog, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

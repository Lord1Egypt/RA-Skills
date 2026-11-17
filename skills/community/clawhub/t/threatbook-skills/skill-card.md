## Description:

Integrates the ThreatBook threat intelligence API so agents can upload suspicious files, query file hash and multi-engine reports, check IP reputation, and assess domain or IP compromise signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[moxin1044](https://clawhub.ai/user/moxin1044)

### License/Terms of Use:

MIT-0

## Use Case:

Security analysts, incident responders, and developers use this skill to call ThreatBook services for suspicious file analysis, file hash reputation, multi-engine detection, IP reputation, and domain or IP compromise checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected file contents, hashes, domains, and IP addresses may be sent to ThreatBook during normal use.

Mitigation: Use the skill only for data that is approved for third-party threat-intelligence analysis and review ThreatBook handling requirements before uploading files.

Risk: The IP reputation script exposes the API key through command-line and URL parameters.

Mitigation: Fix the script to read THREATBOOK_API_KEY and avoid placing the key in URLs before using it with a real key; rotate any key previously passed through --api_key.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/moxin1044/skills/threatbook-skills)
- [ThreatBook portal](https://x.threatbook.cn)
- [ThreatBook file upload API documentation](https://x.threatbook.com/v5/apiDocs#/file/upload)
- [ThreatBook file report API documentation](https://x.threatbook.com/v5/apiDocs#/file/report)
- [ThreatBook multi-engine report API documentation](https://x.threatbook.com/v5/apiDocs#/file/report_multiengines)
- [ThreatBook IP reputation API documentation](https://x.threatbook.com/v5/apiDocs#/ip/reputation)
- [ThreatBook DNS compromise API documentation](https://x.threatbook.com/v5/apiDocs#/scene/dns)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Console text with full JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a ThreatBook API key and may send selected file contents, hashes, domains, and IP addresses to ThreatBook.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

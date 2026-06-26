## Description: <br>
ThreatBook Skills integrates with ThreatBook threat intelligence APIs to upload files for analysis, query file reputation and antivirus detections, check IP reputation, and detect compromise indicators for domains or IP addresses. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Moxin1044](https://clawhub.ai/user/Moxin1044) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Security analysts, incident responders, and security engineers use this skill to query ThreatBook intelligence during investigation of suspicious files, hashes, IP addresses, domains, and possible compromise indicators. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected files, hashes, IP addresses, domains, and API credentials may be sent to ThreatBook during use. <br>
Mitigation: Use the skill only when ThreatBook's online service is intended; prefer hash lookups when possible and upload files only when authorized to share their contents. <br>
Risk: API keys can be exposed if placed in shell history, command logs, or shared transcripts. <br>
Mitigation: Store THREATBOOK_API_KEY in environment or secret configuration and avoid passing credentials directly on command lines. <br>
Risk: Threat intelligence verdicts can be incomplete, stale, or context-dependent. <br>
Mitigation: Treat returned reputation and detection results as investigation inputs and corroborate them with internal telemetry before remediation or blocking decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Moxin1044/threatbook-skills) <br>
- [ThreatBook account and API key portal](https://x.threatbook.cn) <br>
- [ThreatBook file upload API documentation](https://x.threatbook.com/v5/apiDocs#/file/upload) <br>
- [ThreatBook file report API documentation](https://x.threatbook.com/v5/apiDocs#/file/report) <br>
- [ThreatBook multi-engine report API documentation](https://x.threatbook.com/v5/apiDocs#/file/report_multiengines) <br>
- [ThreatBook IP reputation API documentation](https://x.threatbook.com/v5/apiDocs#/ip/reputation) <br>
- [ThreatBook DNS compromise API documentation](https://x.threatbook.com/v5/apiDocs#/scene/dns) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and terminal text with JSON API results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a ThreatBook API key and network access to ThreatBook services.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

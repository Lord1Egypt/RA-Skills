## Description: <br>
Audits installed OpenCode and OpenClaw skills with local pattern scanning and optional VirusTotal threat intelligence. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lanew197894fun-cmd](https://clawhub.ai/user/lanew197894fun-cmd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to scan installed OpenCode and OpenClaw skills for risky code patterns and optional VirusTotal hash matches before deciding whether to keep, quarantine, or remove them. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically quarantine or remove installed skills and may scan broad local disk areas. <br>
Mitigation: Back up the skill directory first, disable auto-quarantine and auto-remove unless automated remediation is explicitly desired, and avoid local, full, or --auto modes unless the scan scope is understood. <br>
Risk: VirusTotal mode stores an API key locally and sends file hashes to VirusTotal. <br>
Mitigation: Use VirusTotal only when that data sharing and local API key storage are acceptable; rotate or remove the key if it may have been exposed. <br>


## Reference(s): <br>
- [VirusTotal](https://virustotal.com) <br>
- [ClawHub release page](https://clawhub.ai/lanew197894fun-cmd/skill-security-vet) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Terminal text reports with optional local configuration updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Bun. VirusTotal checks require an API key and send file hashes to VirusTotal. Scan modes may write configuration, logs, quarantine copies, or removal actions under the user's OpenCode configuration paths.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

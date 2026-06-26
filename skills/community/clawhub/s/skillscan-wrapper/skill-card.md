## Description: <br>
Security audit tool for AI agent skills that scans skill packages for malware, credential theft, and suspicious patterns before installation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cyzlmh](https://clawhub.ai/user/cyzlmh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security reviewers use this skill to audit AI agent skill packages, archives, or release bundles before installation. It produces risk-oriented findings to help identify malware-like behavior, credential access, data exfiltration, and code injection patterns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a third-party scanner binary. <br>
Mitigation: Download the documented release and verify the published SHA-256 checksum before running it. <br>
Risk: Optional reporting and external scanner modes can send data to user-selected destinations or tools. <br>
Mitigation: Use --upload-url or --engine external only with destinations and tools you trust, and scan only intended directories. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/cyzlmh/skillscan-wrapper) <br>
- [cmic-skill-scanner Source](https://gitee.com/random_player/cmic-skill-scanner) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown and command-line examples with risk summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write reports to a user-specified output directory and can optionally upload reports only when the user supplies an upload URL.] <br>

## Skill Version(s): <br>
0.4.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

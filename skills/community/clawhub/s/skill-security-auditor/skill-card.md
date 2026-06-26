## Description: <br>
Command-line security analyzer for ClawHub skills. Run analyze-skill.sh to scan SKILL.md files for malicious patterns, credential leaks, and C2 infrastructure before installation. Includes threat intelligence database with 20+ detection patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[akhmittra](https://clawhub.ai/user/akhmittra) <br>

### License/Terms of Use: <br>
MIT License <br>


## Use Case: <br>
Developers, security reviewers, and ClawHub users use this skill to run local, pattern-based audits of OpenClaw skill files before installing or trusting them. It supports review of malicious indicators, credential exposure patterns, dependency concerns, and advisory risk scores. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Raw manual installation and remote pattern updates can retrieve files that are outside the server-resolved release. <br>
Mitigation: Install through the ClawHub CLI when possible, and only use raw downloads or remote pattern updates from trusted, verified, or pinned sources. <br>
Risk: Pattern-based scanning is advisory and can miss novel or sophisticated malicious behavior. <br>
Mitigation: Combine the audit report with manual review and ClawHub or VirusTotal reputation checks before installing higher-risk skills. <br>
Risk: Slug-based analysis fetches skill content over the network from ClawHub. <br>
Mitigation: Review fetched content before acting on findings when operating in sensitive environments, or analyze a local SKILL.md file instead. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/akhmittra/skill-security-auditor) <br>
- [README](artifact/README.md) <br>
- [Analyzer Script](artifact/analyze-skill.sh) <br>
- [Malicious Pattern Database](artifact/patterns/malicious-patterns.json) <br>
- [OpenClaw Security Auditor Issues](https://github.com/openclaw/security-auditor/issues) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Terminal text audit report with markdown examples and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Advisory risk score from 0-100 with findings, positive indicators, and installation guidance.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

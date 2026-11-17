## Description:

Provides diverse web shell samples in PHP, ASP, ASPX, JSP, Python, and Perl for detection, malware analysis, and authorized security testing.

This skill is for research and development only.

## Publisher:

[pandaai-1337](https://clawhub.ai/user/pandaai-1337)

### License/Terms of Use:

MIT-0

## Use Case:

Security researchers, detection engineers, and incident responders use this skill to inspect web shell samples, validate monitoring controls, and support malware analysis in authorized lab or test environments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release includes deployable web-shell samples for command execution, upload, file browsing, and credential disclosure.

Mitigation: Keep the skill in an isolated lab and do not copy or deploy the samples to production or internet-accessible servers.

Risk: An agent could treat reference scripts as runnable operational steps.

Mitigation: Review agent output before execution and prevent agents from running or deploying the bundled reference scripts.

## Reference(s):

- [Skill Definition](artifact/SKILL.md)
- [Web Shell Backdoor List](artifact/references/Web-Shells/backdoor_list.txt)
- [Vtiger Vulnerable Extension README](artifact/references/Web-Shells/Vtiger/README.md)
- [ColdFusion Shell Sample](artifact/references/Web-Shells/CFM/shell.cfm.html)
- [FuzzDB Command Execution Shell](artifact/references/Web-Shells/FuzzDB/cmd.sh)
- [FuzzDB Directory Listing Shell](artifact/references/Web-Shells/FuzzDB/list.sh)
- [FuzzDB Upload Shell](artifact/references/Web-Shells/FuzzDB/up.sh)
- [Laudanum JSP WAR Descriptor](artifact/references/Web-Shells/laudanum-1.0/jsp/warfiles/WEB-INF/web.xml)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown or plain text with optional code, shell command, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reference materials include executable web-shell samples and should be handled as evidence for authorized analysis, not deployed automatically.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

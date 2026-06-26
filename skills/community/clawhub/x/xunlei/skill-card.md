## Description: <br>
Xunlei helps agents guide users through download acceleration, resource management, remote downloads, cloud drive use, and NAS integration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhangifonly](https://clawhub.ai/user/zhangifonly) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, NAS administrators, and power users use this skill for Xunlei download setup, bandwidth tuning, cloud-drive workflows, remote download control, and NAS/Docker integration guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The NAS Docker example runs a persistent third-party container with broad host privileges. <br>
Mitigation: Review the command before use, prefer a trusted and pinned image, avoid privileged mode and host networking unless necessary, restrict mounted folders, secure the web interface, and know how to stop and remove the container. <br>
Risk: Download and resource-management guidance can be misapplied to copyrighted or untrusted resources. <br>
Mitigation: Use the skill for lawful resources, validate links before downloading, and keep NAS data backed up before changing storage or container configuration. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/zhangifonly/xunlei) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, configuration notes, and troubleshooting tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Provides Xunlei, cloud drive, remote download, and NAS setup guidance; no API calls or credentials are required by the skill.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

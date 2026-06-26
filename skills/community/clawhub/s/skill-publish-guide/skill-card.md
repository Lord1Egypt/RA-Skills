## Description: <br>
Guides users through publishing, updating, deleting, restoring, and troubleshooting ClawHub skills with CLI-based workflows and security best practices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[luduoxin](https://clawhub.ai/user/luduoxin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill publishers use this guide to prepare valid SKILL.md files, publish and update ClawHub skills, manage releases, and troubleshoot common publishing and security-scan issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The guide includes account-changing ClawHub CLI commands such as publish, delete, undelete, and sync --all. <br>
Mitigation: Review each command before running it, prefer non-interactive flags only when the intended action is clear, and use dry-run or inspection commands where available. <br>
Risk: Custom CLAWHUB_SITE or CLAWHUB_REGISTRY values can direct publishing workflows to an alternate registry. <br>
Mitigation: Set custom registry environment variables only for registries you intentionally trust. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/luduoxin/skill-publish-guide) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/luduoxin) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Bilingual English and Chinese guidance; no files or API calls are produced by the skill itself.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

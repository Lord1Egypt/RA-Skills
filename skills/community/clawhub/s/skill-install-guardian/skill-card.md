## Description: <br>
Security and due diligence layer for installing external skills from ClawHub. Performs DEEP content scanning for malicious patterns, security checks, integration analysis, and requires owner confirmation before installation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zendenho7](https://clawhub.ai/user/zendenho7) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and workspace owners use this skill to inspect ClawHub skills before installation, review security and integration findings, and keep owner confirmation as an explicit gate. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automated checks can miss issues or produce false positives. <br>
Mitigation: Review the generated findings manually and keep owner approval as a required step before installation. <br>
Risk: The skill relies on `npx clawhub` inspection commands. <br>
Mitigation: Use a trusted or pinned ClawHub CLI when running inspections. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/zendenho7/skill-install-guardian) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown report with shell commands and JSON status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires npx for ClawHub inspection commands; owner confirmation remains required before installation.] <br>

## Skill Version(s): <br>
1.3.0 (source: frontmatter, server release metadata, changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Security scanner for OpenClaw skills and plugins. Scans for hardcoded secrets, dangerous exec patterns, dependency vulnerabilities, and network egress. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rhombusmaximus](https://clawhub.ai/user/rhombusmaximus) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security reviewers use this skill to audit OpenClaw skills and plugins before installation, publication, or periodic maintenance. It produces local scan reports for hardcoded secrets, risky execution patterns, dependency audit findings, shell injection surfaces, and network egress. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The optional Notion export can send discovered secret findings to a third-party store. <br>
Mitigation: Use normal scans without --encrypt-found by default, and enable Notion export only after reviewing the scripts, the separate notion-secrets.js helper, the Notion workspace, and NOTION_MASTER_PASSWORD handling. <br>
Risk: Security scan findings may contain sensitive retained security data. <br>
Mitigation: Treat generated reports and exported findings as sensitive artifacts; restrict access and review them before sharing or publishing. <br>
Risk: The skill is shell-based and executes local scan scripts over user-selected directories. <br>
Mitigation: Review the scripts before installation and run them only against directories you intend to audit. <br>


## Reference(s): <br>
- [Notion Encryption System](references/notion-encryption.md) <br>
- [ClawHub skill page](https://clawhub.ai/rhombusmaximus/security-sweep) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and terminal text with shell command examples and scan report summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Report files are written to user-selected local paths; optional Notion export stores encrypted findings outside the local workspace.] <br>

## Skill Version(s): <br>
1.1.2 (source: server release metadata; SKILL.md frontmatter lists 1.1.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

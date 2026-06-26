## Description: <br>
Build and manage websites from Markdown. Create pages, generate content, configure settings, and deploy \u2014 all through MCP tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tyler-berggren](https://clawhub.ai/user/tyler-berggren) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, site owners, and agents use this skill to create, manage, validate, configure, build, and deploy Markdown-based websites through sitemd MCP tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can install or run external tooling and perform lasting website actions such as deploy, activate, delete, update, and configuration changes. <br>
Mitigation: Verify the installer and binary source before running them, and require manual approval for install, update, delete, deploy, activate, and configuration changes. <br>
Risk: The skill uses magic links and SITEMD_TOKEN for authentication and long-lived automation credentials. <br>
Mitigation: Treat magic links and SITEMD_TOKEN as secrets, share login URLs only with the site owner, and store tokens in a managed secret environment. <br>
Risk: Generated site content or configuration changes could publish incorrect, unwanted, or misleading website updates. <br>
Mitigation: Review generated content, settings, and deployment diffs before publishing or activating a site. <br>


## Reference(s): <br>
- [sitemd homepage](https://sitemd.cc) <br>
- [ClawHub skill page](https://clawhub.ai/tyler-berggren/sitemd) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown content, YAML frontmatter, shell commands, and configuration guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create, update, validate, build, and deploy website project files through MCP tools.] <br>

## Skill Version(s): <br>
0.1.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

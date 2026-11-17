## Description:

Helps AI-agent users and maintainers plan and carry out GitHub-style software workflows, including bug fixes, setup hardening, reliability improvements, and adjacent skill creation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, AI-agent users, skill authors, maintainers, and teams use this skill to turn GitHub-style software and data requests into practical plans, artifacts, checklists, implementation support, and verification notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may activate too broadly for general software, GitHub, CLI, issue, or bug-fix requests.

Mitigation: Narrow trigger terms or disable implicit invocation when broad activation is not desired.

Risk: The skill can suggest repository, issue, pull request, or configuration changes that may affect a project if executed by other tools.

Mitigation: Review proposed steps and run appropriate tests or scans before allowing tools to modify repositories, issues, pull requests, or configuration.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kyro-ma/skills/software-data-github-interact-developer-helper-014620)
- [Publisher Profile](https://clawhub.ai/user/kyro-ma)
- [Requirement Plan](references/requirement-plan.md)
- [Skill Vetter demand signal](https://clawhub.ai/skills/skill-vetter)
- [Github skill demand signal](https://clawhub.ai/skills/github)
- [Exercise: Integrate MCP with Copilot](https://github.com/chanderksharma/skills-integrate-mcp-with-copilot/issues/1)
- [Modbus protocol stack discussion](https://www.v2ex.com/t/1223244)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with optional code blocks, shell commands, checklists, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should state assumptions, constraints, validation steps, and remaining risks when relevant.]

## Skill Version(s):

0.20260729.110214 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

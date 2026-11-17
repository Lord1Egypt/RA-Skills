## Description: <br>
Repo Manager Free helps agents manage GitHub repositories, issues, pull requests, commits, and branches through MCP-style tool calls with preview and confirmation steps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Individual developers use this skill to let an AI agent inspect and manage GitHub repository activity, issues, pull requests, commits, and branches while confirming write operations before execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks for GitHub account authorization that may be broader than its free repository-management features require. <br>
Mitigation: Install only if the repo-manager-plugin is trusted, grant the minimum OAuth scopes needed for the task, and avoid workflow scope for the free version unless it is specifically required. <br>
Risk: Repository, issue, pull request, commit, and branch actions can change GitHub project state if executed with write permissions. <br>
Mitigation: Use the documented preview and confirmation flow for every write operation and verify target repositories, branches, and issue or pull request numbers before execution. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/thcjp/skills/repo-manager-free) <br>
- [Skill homepage](https://skillhub.cn) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, JSON] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON response shapes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Write operations should be previewed and confirmed before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

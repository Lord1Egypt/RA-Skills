## Description: <br>
Repo visibility guard that blocks repositories from being made public unless a matching -private counterpart exists. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[parkertoddbrooks](https://clawhub.ai/user/parkertoddbrooks) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineering teams use this skill as a CLI, hook, MCP server, or OpenClaw plugin to check repository visibility changes and audit public repositories for required -private counterparts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can block GitHub repository visibility changes when its hook policy does not match the team's intended release workflow. <br>
Mitigation: Install it only in environments where the -private counterpart rule is required, and review blocked results before changing release automation. <br>
Risk: The skill relies on the existing `gh` authentication context and reads GitHub repository metadata for requested organizations. <br>
Mitigation: Use a GitHub authentication context scoped to the intended organizations and permissions for visibility checks and audits. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/parkertoddbrooks/wip-repo-permissions-hook) <br>
- [Project Homepage](https://github.com/wipcomputer/wip-ai-devops-toolbox) <br>
- [npm Package](https://www.npmjs.com/package/@wipcomputer/wip-repo-permissions-hook) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text and Markdown with shell and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [CLI and MCP responses report allowed, blocked, audit, and error states for GitHub repository visibility checks.] <br>

## Skill Version(s): <br>
1.9.72 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

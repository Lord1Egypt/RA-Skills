## Description: <br>
Interact with GitHub using the gh CLI to manage pull requests, check CI status, view workflow runs, and access advanced API queries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yequanzheng](https://clawhub.ai/user/yequanzheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to ask an agent for GitHub CLI commands and guidance for pull requests, CI checks, workflow runs, failed logs, API queries, and JSON output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Commands can use the user's existing GitHub CLI authentication and repository permissions. <br>
Mitigation: Confirm the active GitHub account and target repository before running commands, and approve write actions only when explicitly requested. <br>
Risk: GitHub CLI commands may target an unintended repository if repository context is ambiguous. <br>
Mitigation: Use --repo owner/repo or direct URLs when the agent is not already operating in the intended git directory. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may rely on the user's local GitHub CLI authentication and repository context.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

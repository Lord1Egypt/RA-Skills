## Description: <br>
这是我的测试32323 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yequanzheng](https://clawhub.ai/user/yequanzheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to get concise GitHub CLI guidance for pull requests, workflow runs, failed logs, issues, and GitHub API queries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may use the user's existing GitHub account access through the gh CLI. <br>
Mitigation: Confirm which GitHub account gh is authenticated with before using generated commands. <br>
Risk: Commands that write to GitHub, change issues or pull requests, trigger workflows, or use broad gh api access can affect repositories. <br>
Mitigation: Keep repository scopes explicit and review write-oriented or broad API commands before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yequanzheng/trello3) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may depend on the user's authenticated gh CLI account and repository scope.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

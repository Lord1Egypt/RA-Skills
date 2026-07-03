## Description: <br>
Interact with Bitbucket Cloud via REST API for repository management, pull request operations, branch management, commit history, pipeline status, and workspace or team queries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[snowsand-enterprises](https://clawhub.ai/user/snowsand-enterprises) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to let an agent inspect and operate on Bitbucket Cloud repositories, pull requests, branches, commits, pipelines, workspaces, and account information through the bundled CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can perform live write operations on Bitbucket Cloud repositories, pull requests, branches, and pipelines. <br>
Mitigation: Use a narrowly scoped Bitbucket token, prefer a limited workspace or test repository first, and review commands before allowing repository creation, branch deletion, PR decline, PR merge, comments, approvals, or pipeline triggers. <br>
Risk: Credential scope may exceed the specific repository or workflow the agent needs. <br>
Mitigation: Grant only the minimum Bitbucket permissions required for the intended task and rotate the token if it is exposed. <br>
Risk: Pipeline triggers and pull request merges can affect CI/CD workflows and protected branches. <br>
Mitigation: Confirm the target repository, branch, pull request, merge strategy, and pipeline selector before approving execution. <br>


## Reference(s): <br>
- [Bitbucket Cloud API Reference](references/api.md) <br>
- [Atlassian Bitbucket Cloud REST API](https://developer.atlassian.com/cloud/bitbucket/rest/) <br>
- [Atlassian API Tokens](https://id.atlassian.com/manage-profile/security/api-tokens) <br>
- [Bitbucket App Passwords](https://bitbucket.org/account/settings/app-passwords/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Bitbucket Cloud credentials and workspace configuration through environment variables.] <br>

## Skill Version(s): <br>
1.0.1 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Interact with Bitbucket Cloud via REST API for repository management, pull request operations, branch management, commit history, pipeline status, and workspace/team queries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[snowsand-enterprises](https://clawhub.ai/user/snowsand-enterprises) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to inspect and manage Bitbucket Cloud repositories, pull requests, branches, commits, pipelines, workspaces, and user information from an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can perform real repository-changing Bitbucket actions, including repository creation, pull request approval or merge, pull request decline, branch deletion, comments, raw API POST calls, and pipeline runs. <br>
Mitigation: Use a dedicated least-privilege app password, prefer read-only scopes unless write access is required, and require explicit human confirmation before any write or destructive action. <br>
Risk: A broadly scoped app password could let an agent affect more repositories or operations than intended. <br>
Mitigation: Grant only the Bitbucket permissions needed for the intended workflow and rotate the app password if it may have been exposed. <br>


## Reference(s): <br>
- [Bitbucket Cloud API Reference](references/api.md) <br>
- [Atlassian Bitbucket Cloud REST API](https://developer.atlassian.com/cloud/bitbucket/rest/) <br>
- [ClawHub Skill Page](https://clawhub.ai/snowsand-enterprises/snowsand-bitbucket) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance, API calls] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON API output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Bitbucket workspace, username, and app password environment variables.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

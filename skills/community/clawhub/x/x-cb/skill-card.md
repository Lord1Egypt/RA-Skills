## Description: <br>
Interact with Codeberg using the `x cb` CLI to manage repositories, issues, pull requests, organizations, teams, and users. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[curry798](https://clawhub.ai/user/curry798) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and maintainers use this skill when they need an agent to propose or run `x cb` commands for Codeberg repository, issue, pull request, organization, team, and user workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Commands may create public repositories, open issues or pull requests, or change collaborator and team permissions. <br>
Mitigation: Review the target repository, organization, username, permission level, title, body, and public/private impact before executing write commands. <br>
Risk: A broad Codeberg token could expose more account or organization access than the workflow needs. <br>
Mitigation: Use a least-privilege Codeberg token and install the skill only when the `x cb` CLI on PATH is already trusted. <br>


## Reference(s): <br>
- [Codeberg application tokens](https://codeberg.org/user/settings/applications) <br>
- [ClawHub skill page](https://clawhub.ai/curry798/x-cb) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the `x cb` CLI on PATH and a Codeberg token for authenticated operations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Fork, clone, and set up a GitHub repository for development or contribution, including fork creation, authenticated cloning, upstream remote configuration, feature branch creation, and dependency installation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sliverp](https://clawhub.ai/user/sliverp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to prepare a local GitHub repository for contribution or exploration, including forking, cloning, upstream remote setup, branch creation, and dependency installation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: GitHub token handling could expose an account token, especially with token-in-URL cloning or printed remotes. <br>
Mitigation: Prefer GitHub CLI login, SSH, or a credential helper; avoid token-in-URL cloning and avoid printing remotes that may contain secrets. <br>
Risk: Dependency installation commands run code or package hooks from the target repository. <br>
Mitigation: Run dependency installs only for repositories you trust or inside an isolated development environment. <br>
Risk: Persisting tokens in shell profiles can leave long-lived credentials on disk. <br>
Mitigation: Use a credential helper or scoped authentication flow instead of storing tokens directly in shell profile files. <br>


## Reference(s): <br>
- [repo-setup ClawHub page](https://clawhub.ai/sliverp/repo-setup) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell command blocks and setup instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a ready-to-develop local repository setup plan with remotes, branch, and dependencies configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Use only when the user explicitly asks to stage, commit, push, and open a GitHub pull request in one flow using the GitHub CLI (`gh`). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[patrick-erichsen-2](https://clawhub.ai/user/patrick-erichsen-2) <br>

### License/Terms of Use: <br>
Apache 2.0 <br>


## Use Case: <br>
Developers and engineers use this skill when they explicitly want an agent to prepare repository changes for review by staging intended changes, creating a conventional commit, pushing a branch, and opening a draft GitHub pull request with GitHub CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can stage, commit, push, and open pull requests, which may publish unintended code, secrets, or unrelated files. <br>
Mitigation: Review `git status` and the diff before staging, confirm no secrets or unrelated files are present, and require explicit approval before staging, committing, pushing, or creating the pull request. <br>
Risk: Repository publication depends on GitHub CLI authentication and may fail or use the wrong account if authentication is not checked. <br>
Mitigation: Run `gh --version` and `gh auth status` before use, and stop until the intended GitHub account is authenticated. <br>


## Reference(s): <br>
- [Yeet on ClawHub](https://clawhub.ai/patrick-erichsen-2/yeet) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and pull request prose] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires GitHub CLI authentication and explicit review before repository publication actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

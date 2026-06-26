## Description: <br>
Publishes a local Skill project to GitHub and syncs it to ClawHub, with automated setup for new projects and guided versioning for existing repositories. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhouchang1988](https://clawhub.ai/user/zhouchang1988) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and skill maintainers use this skill to publish Skill projects to GitHub and ClawHub, including repository setup, release tagging, and workflow configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish local code and alter GitHub repositories. <br>
Mitigation: Use it only in a clean skill-only directory, review .gitignore and staged files first, and confirm the GitHub account, owner, repository name, and public/private setting before proceeding. <br>
Risk: The skill can persist credentials and publishing workflows. <br>
Mitigation: Review the generated workflow, repository secrets, and stored ClawHub token before pushing release tags. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhouchang1988/publish-skill-repo) <br>
- [ClawHub](https://clawhub.ai/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Code, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and generated repository files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or modify Git repositories, GitHub workflows, release tags, and repository secrets when executed.] <br>

## Skill Version(s): <br>
2.1.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

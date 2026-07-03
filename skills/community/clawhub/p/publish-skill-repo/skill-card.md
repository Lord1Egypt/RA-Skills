## Description: <br>
Publishes a skill project to GitHub and syncs it to ClawHub, automating new repositories and guiding updates to existing repositories. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhouchang1988](https://clawhub.ai/user/zhouchang1988) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and skill maintainers use this skill to prepare, publish, and version skill repositories on GitHub and ClawHub. It supports release workflows where repository visibility, staged files, secrets, and tags can be reviewed before publishing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish local skill content to GitHub and ClawHub with limited confirmation. <br>
Mitigation: Review the target repository owner and name, repository visibility, and exact files to be committed before allowing the publishing workflow to run. <br>
Risk: The workflow can use a local ClawHub token and copy it into a GitHub repository secret. <br>
Mitigation: Confirm that storing the ClawHub token as a repository secret is acceptable for the target repository, and rotate the token if it may have been exposed. <br>
Risk: The release flow can create commits, tags, and workflow files that trigger publication. <br>
Mitigation: Review the proposed commit message, version tag, generated workflow, and staged changes before pushing or tagging a release. <br>


## Reference(s): <br>
- [Publish Skill Repo on ClawHub](https://clawhub.ai/zhouchang1988/skills/publish-skill-repo) <br>
- [ClawHub](https://clawhub.ai/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and generated repository configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update repository files, Git commits, tags, GitHub repository settings, and ClawHub publishing configuration when executed by an agent.] <br>

## Skill Version(s): <br>
2.1.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

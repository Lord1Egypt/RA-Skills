## Description: <br>
Publish AI agent skills to GitHub and multiple skill registries, including skills.sh and clawhub.ai, in one workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[orbisz](https://clawhub.ai/user/orbisz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill maintainers use this skill to publish or update an agent skill across GitHub, skills.sh, clawhub.ai, and skillsmp.com while keeping registry metadata aligned with SKILL.md. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can commit and publish broad local changes while pushing to GitHub and registries. <br>
Mitigation: Review the working tree and staged diff before use, and run it only in repositories where publishing those changes is intended. <br>
Risk: The workflow depends on authenticated tools such as GitHub CLI and the ClawHub CLI. <br>
Mitigation: Use least-privilege credentials, confirm the active account before publishing, and avoid running it in repositories that contain secrets. <br>
Risk: The skill stores local repository mappings and includes self-evolution diary behavior that may create extra local state. <br>
Mitigation: Review or remove repo-map and diary/self-evolution behavior before deployment if persistent local state is not desired. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/orbisz/skill-publish-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Markdown, Configuration, Guidance] <br>
**Output Format:** [Markdown status summaries with inline shell commands and generated commit messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update git remotes, commits, registry state, and references/repo-map.json when the workflow runs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

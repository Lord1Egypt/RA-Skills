## Description: <br>
WonderDash helps an agent create and manage widgets on the user's WonderDash mobile dashboard through a GitHub-backed widget repository. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Hay-wired](https://clawhub.ai/user/Hay-wired) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and WonderDash users use this skill to create, update, reorder, archive, restore, and delete dashboard widgets represented as JSON files. The skill is intended for agents that can work with Git and SSH to manage a dedicated WonderDash widgets repository. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a dedicated SSH deploy key for a GitHub-backed widgets repository. <br>
Mitigation: Use a repository-scoped key, avoid reusing broad GitHub credentials, and remove ~/.ssh/wonderdash_deploy plus the related SSH config entry when no longer needed. <br>
Risk: Widget deletion and Git pushes can permanently change the user's dashboard repository. <br>
Mitigation: Review proposed changes before pushing and prefer archiving widgets by removing them from dashboard.json before permanent deletion. <br>


## Reference(s): <br>
- [WonderDash ClawHub listing](https://clawhub.ai/Hay-wired/wonderdash) <br>
- [Hay-wired publisher profile](https://clawhub.ai/user/Hay-wired) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with JSON examples and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces self-contained widget JSON, dashboard index changes, Git commands, and SSH setup guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter declares 5.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

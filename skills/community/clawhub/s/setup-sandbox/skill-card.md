## Description: <br>
Sets up the initial file system for a new Recoup sandbox by fetching organizations and artists via the Recoup CLI and scaffolding the expected folder structure. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sweetmantech](https://clawhub.ai/user/sweetmantech) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators managing Recoup sandbox workspaces use this skill to initialize organization and artist folders, fetch account data with the Recoup CLI, and create RECOUP.md identity files before artist setup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can stage, commit, and push broad workspace changes to a Git remote. <br>
Mitigation: Run it in a fresh repository or sandbox, inspect git status before execution, and require manual approval before any commit or push. <br>
Risk: The generated sandbox structure depends on Recoup CLI responses and account selection. <br>
Mitigation: Confirm the intended account context and review generated organization, artist, and RECOUP.md files before publishing changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sweetmantech/setup-sandbox) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, markdown, configuration, files] <br>
**Output Format:** [Markdown guidance with shell commands and generated workspace files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates organization and artist directories plus RECOUP.md identity files, then may commit and push workspace changes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

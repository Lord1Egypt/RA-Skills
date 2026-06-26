## Description: <br>
Automates packaging, pushing to GitHub, and publishing OpenClaw skills to ClawHub, managing versions and sync across platforms. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zerozlw](https://clawhub.ai/user/zerozlw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill maintainers use this skill to validate skill folders, push releases to GitHub, publish versions to ClawHub, and keep distribution across both platforms aligned. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The publish and GitHub scripts can stage and push all files in the target skill folder. <br>
Mitigation: Inspect the target folder, run git status, and remove private files or secrets before running the push or full publish workflow. <br>
Risk: A release can be published to the wrong GitHub repository or ClawHub slug if command arguments are incorrect. <br>
Mitigation: Confirm the target repository, version, slug, and ClawHub account before executing the publish commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zerozlw/skill-release-pipeline) <br>
- [Publisher profile](https://clawhub.ai/user/zerozlw) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May invoke local shell scripts and external CLIs such as gh and npx clawhub when the user chooses to run the release workflow.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

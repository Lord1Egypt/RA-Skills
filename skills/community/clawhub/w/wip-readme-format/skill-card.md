## Description: <br>
Reformat any repo's README to follow the WIP Computer standard. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[parkertoddbrooks](https://clawhub.ai/user/parkertoddbrooks) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to generate, stage, validate, and assemble README content that follows the WIP Computer standard. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Deploy mode has a shell-command injection risk in repositories with crafted README-init filenames. <br>
Mitigation: Use --dry-run or --check first, review generated README-init files, and avoid --deploy on untrusted repositories until the git status check is changed to a safe argument-array call. <br>
Risk: The formatter can replace README.md and TECHNICAL.md during deploy. <br>
Mitigation: Review the staged section files before deploy and rely on the tool's backup files when comparing or recovering documentation changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/parkertoddbrooks/wip-readme-format) <br>
- [Project homepage](https://github.com/wipcomputer/wip-ai-devops-toolbox) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, text, shell commands, guidance] <br>
**Output Format:** [Markdown files and terminal text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates README-init section files for review, supports dry-run and check modes, and can assemble README.md and TECHNICAL.md during deploy.] <br>

## Skill Version(s): <br>
1.9.72 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

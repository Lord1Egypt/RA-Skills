## Description: <br>
Workspace Git Setup helps an agent initialize or audit local Git tracking for a workspace with a security-focused .gitignore, large-file warnings, dry-run previews, and read-only audit checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[songhonglei](https://clawhub.ai/user/songhonglei) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to add safe local version tracking to a workspace, preview setup actions, or audit an existing repository for tracked secrets, untracked files, and line-ending configuration. It is most useful when a project needs an initial Git baseline or a lightweight repository health check before further work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Setup mode can initialize Git and create a local commit in the selected workspace. <br>
Mitigation: Run --dry-run or --audit first, inspect the planned .gitignore and git status, and confirm the selected workspace path before running setup mode. <br>
Risk: A local commit can still include files not covered by the generated ignore rules. <br>
Mitigation: Review git status and the staged file list before committing, especially when the workspace may contain credentials, private keys, tokens, caches, or large files. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/songhonglei/workspace-git-setup) <br>
- [Git Downloads](https://git-scm.com/downloads) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash commands and local Git status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Default setup mode can mutate the selected workspace by initializing Git, writing .gitignore, setting Git config, staging files, and creating a local commit; --dry-run and --audit are read-only modes.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

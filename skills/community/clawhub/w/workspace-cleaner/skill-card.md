## Description: <br>
Automates safe cleanup of OpenClaw workspaces by previewing and moving temp files, logs, duplicates, and cruft to the system trash with customizable filtering. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brandonwise](https://clawhub.ai/user/brandonwise) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to preview workspace cleanup candidates, review size and age filters, and execute recoverable cleanup for known temporary files and workspace cruft. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Executing cleanup can move matching local workspace files to trash. <br>
Mitigation: Start in preview mode, review the listed paths carefully, and use --execute only after confirming the cleanup set. <br>
Risk: The documented --exclude option is not implemented in the script. <br>
Mitigation: Do not rely on --exclude; adjust the patterns configuration and filters or avoid execution until the cleanup patterns match the workspace. <br>
Risk: Scheduled or quiet execution can hide cleanup decisions from review. <br>
Mitigation: Avoid scheduled or quiet execution until the configured patterns and filters are known to match the workspace safely. <br>


## Reference(s): <br>
- [Safe Defaults Reference](artifact/references/safe-defaults.md) <br>
- [Workspace Cleaner ClawHub Page](https://clawhub.ai/brandonwise/workspace-cleaner) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, JSON] <br>
**Output Format:** [Markdown with bash and JSON examples; the cleanup script can emit JSON when run with --json.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Defaults to preview mode; --execute moves matching local workspace files to trash.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

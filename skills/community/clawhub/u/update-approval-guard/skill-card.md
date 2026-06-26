## Description: <br>
Use this skill when the user wants scheduled update checks for OpenClaw and installed skills, but does not want automatic mutation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Waytobetter619](https://clawhub.ai/user/Waytobetter619) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to check for OpenClaw and installed skill updates on a schedule while requiring explicit human approval before changes are applied. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The server security summary says the published package contains unrelated automation, credentials, and external social, news, and Feishu workflows outside the update-approval purpose. <br>
Mitigation: Review the package before installation, remove unrelated workspace contents, rotate any exposed credentials, and use a minimal package containing only the update-approval skill, examples, and scoped state files. <br>
Risk: Approved update execution can mutate the local OpenClaw and skill environment. <br>
Mitigation: Use the dry-run check phase first, require explicit approval before apply commands, and run the documented health check after approved updates. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Waytobetter619/update-approval-guard) <br>
- [README](artifact/update-approval-guard/README.md) <br>
- [Example cron job](artifact/update-approval-guard/examples/cron-job.json) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, JSON files, Markdown] <br>
**Output Format:** [Markdown instructions with shell command snippets and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates pending update and history state files under the workspace data directory when followed by an agent.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

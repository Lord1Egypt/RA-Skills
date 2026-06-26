## Description: <br>
soul-guardian detects drift in agent workspace files, checks them against approved baselines, and can alert or restore protected files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[davida-ps](https://clawhub.ai/user/davida-ps) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to monitor OpenClaw workspace prompt and instruction files for unexpected changes, maintain approved baselines, and review audit evidence when drift occurs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Restore mode can overwrite protected workspace files when drift is detected. <br>
Mitigation: Initialize baselines only from known-good files, and use --no-restore or an alert-only policy when automatic overwrites are not intended. <br>
Risk: The state directory can contain approved snapshots, diffs, audit records, and quarantined copies. <br>
Mitigation: Keep the state directory private, prefer an external location, and protect it with restrictive permissions. <br>
Risk: Optional cron or launchd scheduling can run ongoing background enforcement. <br>
Mitigation: Enable scheduled monitoring only after reviewing the generated cron or launchd configuration. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/davida-ps/soul-guardian) <br>
- [Project homepage](https://clawsec.prompt.security) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with shell commands and alert text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May provide local file-integrity status, drift alerts, audit guidance, and setup commands.] <br>

## Skill Version(s): <br>
0.0.6 (source: server evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

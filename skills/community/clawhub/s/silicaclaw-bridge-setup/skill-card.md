## Description: <br>
Use when OpenClaw should learn how to install SilicaClaw bridge skills, check bridge connectivity, verify owner-forward runtime settings, and troubleshoot why broadcast learning or owner delivery is not ready yet. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chinasong](https://clawhub.ai/user/chinasong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and developers use this skill to install the local SilicaClaw bridge skills, verify bridge readiness, configure owner-forward runtime values, and identify the next setup step before using broadcast or monitoring workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local setup may install bridge skills or reference commands from an untrusted SilicaClaw project. <br>
Mitigation: Use the skill only with a trusted local SilicaClaw CLI/project and review skills added under `~/.openclaw/workspace/skills/` before deployment. <br>
Risk: Owner-forward settings could send notifications to an unintended channel, target, or command. <br>
Mitigation: Set `OPENCLAW_OWNER_FORWARD_CMD`, `OPENCLAW_OWNER_CHANNEL`, and `OPENCLAW_OWNER_TARGET` only to destinations and commands the owner controls. <br>


## Reference(s): <br>
- [Runtime Setup](references/runtime-setup.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>
- [Owner Dialogue Cheatsheet (Chinese)](references/owner-dialogue-cheatsheet-zh.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May recommend local SilicaClaw CLI commands and owner-forward environment variable settings; does not produce executable payloads.] <br>

## Skill Version(s): <br>
2026.3.20-beta.1 (source: server release metadata and manifest.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

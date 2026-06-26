## Description: <br>
Installs or upgrades the OpenClaw QQBot plugin by running a bundled shell script that verifies installed files, supports rollback, and can restart the gateway. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ryanlee-gemini](https://clawhub.ai/user/ryanlee-gemini) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and developers use this skill to install or upgrade the openclaw-qqbot plugin through an agent-assisted workflow. It is intended for environments where the user wants the agent to run the installer, verify expected plugin files, report the installed version, and restart the gateway when appropriate. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The installer can install arbitrary OpenClaw plugin packages when invoked with generic package and plugin identifiers. <br>
Mitigation: Use the QQBot invocation for a trusted openclaw-qqbot package and version; avoid generic plugin installs unless the package source is trusted. <br>
Risk: Installed plugin code or plugin-provided postinstall JavaScript may run in the user's OpenClaw environment. <br>
Mitigation: Review and trust the target plugin before installation, and run the skill only in an environment where plugin code execution is acceptable. <br>
Risk: The script can modify plugin directories and restart the OpenClaw gateway. <br>
Mitigation: Run it only when gateway restart and extension-directory changes are intended; use the no-restart option when a restart is not desired. <br>


## Reference(s): <br>
- [Qqbot Installer on ClawHub](https://clawhub.ai/ryanlee-gemini/qqbot-installer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and structured command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include plugin version and status lines such as PLUGIN_NEW_VERSION and PLUGIN_REPORT.] <br>

## Skill Version(s): <br>
1.0.3 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

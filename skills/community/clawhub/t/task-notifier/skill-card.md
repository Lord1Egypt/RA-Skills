## Description: <br>
Sends desktop notifications when an OpenClaw agent or subagent finishes a task, with support for macOS and WSL-on-Windows, smart suppression, and language detection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wdgame](https://clawhub.ai/user/wdgame) <br>

### License/Terms of Use: <br>
MIT No Attribution <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to monitor long-running agent and multi-agent workflows and receive local desktop notifications when work completes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can prompt installation of a separate runtime plugin using unsafe install flags, and that plugin was not included in the reviewed skill files. <br>
Mitigation: Inspect the runtime plugin package before installation and proceed only if its local notification behavior and install flags are acceptable. <br>
Risk: The runtime plugin is described as having broad all-agent lifecycle hook coverage for task-completion monitoring. <br>
Mitigation: Use the documented include and exclude filters to narrow monitored agents, or avoid installing the runtime plugin when broad monitoring is not acceptable. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/wdgame/task-notifier) <br>
- [ClawHub README Link](https://clawhub.ai/skills/task-notifier) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill itself is documentation-only; notification behavior depends on a separately installed runtime plugin.] <br>

## Skill Version(s): <br>
1.1.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

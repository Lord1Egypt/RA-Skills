## Description: <br>
Helps agents search and read local OpenClaw documentation before proposing OpenClaw configuration changes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[echoflying](https://clawhub.ai/user/echoflying) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to find synchronized local documentation, read relevant sections, and produce documented configuration plans before changing agents, gateways, channels, schedules, tools, workspaces, memory, or skills. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Document read and list commands may access files outside the intended OpenClaw manual path when given untrusted paths. <br>
Mitigation: Use only trusted, relative documentation paths with --read and --list, and review the skill before installing or running it. <br>
Risk: The skill writes local logs of command arguments by default, which may capture sensitive search terms or paths. <br>
Mitigation: Avoid searching for secrets and run with DISABLE_USAGE_LOG=true when query privacy matters. <br>
Risk: Documentation sync can send update notifications to a configured channel. <br>
Mitigation: Keep DOC_NOTIFY_CHANNEL unset or set to none until notification routing and logging controls are reviewed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/echoflying/use-openclaw-manual) <br>
- [OpenClaw Documentation](https://docs.openclaw.ai) <br>
- [Script Reference](references/scripts.md) <br>
- [Troubleshooting Guide](references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and cited document paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read local OpenClaw documentation, sync documentation from GitHub, and write local usage or update logs depending on command and environment settings.] <br>

## Skill Version(s): <br>
2.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

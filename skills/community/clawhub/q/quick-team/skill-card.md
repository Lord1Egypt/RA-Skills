## Description: <br>
Quick Team helps OpenClaw users create AI team-member directories and configuration files from natural-language requests, including SOUL, IDENTITY, TOOLS, HEARTBEAT, and MEMORY templates and guided openclaw.json setup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhao-zwl](https://clawhub.ai/user/zhao-zwl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and developers use Quick Team to scaffold new team-member agents, fill required persona and memory templates, update runtime configuration after diff review, and validate activation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can modify OpenClaw runtime configuration in ~/.qclaw/openclaw.json. <br>
Mitigation: Review the complete diff and approve the change before writing; keep a backup of openclaw.json. <br>
Risk: Using allowAgents ["*"] can expand sub-agent spawn permissions beyond the intended new member. <br>
Mitigation: Use the smallest allowAgents whitelist needed, usually only the new member ID. <br>
Risk: Restarting OpenClaw Gateway can interrupt active sessions and running tasks. <br>
Mitigation: Restart only after user confirmation and after warning that active work may be interrupted. <br>
Risk: Generated MEMORY templates include hard-coded identity fields and may capture sensitive project context. <br>
Mitigation: Replace template identity values before use and avoid storing API keys or other secrets unless intentional. <br>


## Reference(s): <br>
- [Quick Team on ClawHub](https://clawhub.ai/zhao-zwl/quick-team) <br>
- [Publisher profile](https://clawhub.ai/user/zhao-zwl) <br>
- [README](README.md) <br>
- [Skill instructions](SKILL.md) <br>
- [Changelog](CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON snippets, shell commands, and generated Markdown files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Configuration edits and gateway restarts are presented for user confirmation before execution.] <br>

## Skill Version(s): <br>
1.1.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

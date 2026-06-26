## Description: <br>
Run Alibaba Cloud Qwen Code CLI via background process for task execution, code review, and automation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[UserB1ank](https://clawhub.ai/user/UserB1ank) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and teams use this skill to run Qwen Code for coding tasks, code review, headless automation, and CI/CD workflows from an agent environment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: This skill gives Qwen Code broad coding-agent authority over the project where it is run. <br>
Mitigation: Run it only in an intended work directory, prefer review/default or sandbox modes, and avoid YOLO mode on sensitive or production repositories. <br>
Risk: Project code, diffs, logs, or secrets may be sent to Qwen during task execution or review. <br>
Mitigation: Review inputs before execution, remove secrets from prompts and files where possible, and avoid running it on repositories that contain sensitive data. <br>
Risk: Qwen local state, sessions, MCP servers, skills, or extensions can affect subsequent runs. <br>
Mitigation: Monitor changes under ~/.qwen and review configured sessions, MCP servers, skills, and extensions before using the skill in important workspaces. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/UserB1ank/qwen-code-skill) <br>
- [Qwen Code official docs](https://qwenlm.github.io/qwen-code-docs/zh/) <br>
- [DashScope API key console](https://dashscope.console.aliyun.com/) <br>
- [Qwen CLI command reference](references/qwen-cli-commands.md) <br>
- [Example workflows](assets/examples/) <br>
- [OpenClaw documentation](https://openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and terminal-oriented text with optional JSON output from headless Qwen Code runs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the qwen CLI and either OAuth or API key authentication.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release and changelog, released 2026-02-27) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

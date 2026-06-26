## Description: <br>
Team Dispatch orchestrates multi-agent workflows by decomposing requests into dependency graphs, dispatching specialized agents in parallel, tracking task state, and handling retries and completion notifications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vvusu](https://clawhub.ai/user/vvusu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use Team Dispatch to coordinate complex coding, research, analysis, content, and security-review work across specialized subagents while preserving task state across long-running workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup flow can change ~/.openclaw/openclaw.json, add agent workspaces, grant broad subagent delegation, and restart OpenClaw Gateway. <br>
Mitigation: Review the setup actions before running them, back up existing OpenClaw configuration, and replace allowAgents ["*"] with a specific allowlist in sensitive environments. <br>
Risk: The skill can create recurring watcher and daily-summary jobs through system schedulers or OpenClaw cron. <br>
Mitigation: Disable watcher or daily-summary settings when recurring background execution is not desired, and audit installed scheduler entries after setup. <br>
Risk: Bundled onboarding workspace content asks for personal or contact details. <br>
Mitigation: Remove or replace the onboarding BOOTSTRAP.md and user-profile content before sharing workspaces or using the skill where personal data collection is inappropriate. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/vvusu/team-dispatch) <br>
- [Configuration reference](references/CONFIG.md) <br>
- [Troubleshooting guide](references/TROUBLESHOOTING.md) <br>
- [README](README.md) <br>
- [Changelog](CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and plain text with inline JSON, shell commands, configuration snippets, and generated project artifacts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update task-tracking JSON, agent workspace files, OpenClaw configuration, and scheduled watcher or daily-summary jobs when its setup scripts are run.] <br>

## Skill Version(s): <br>
1.0.8 (source: server release metadata, CHANGELOG.md, config.json, and SKILL.md heading) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

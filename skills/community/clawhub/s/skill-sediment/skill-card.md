## Description: <br>
Installs and operates an OpenClaw plugin that reviews successful conversations, writes reusable workflows as SKILL.md files, and promotes repeated useful workflows into active skills. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[songhonglei](https://clawhub.ai/user/songhonglei) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to install, diagnose, recover, configure, and remove the skill-sediment plugin. The plugin helps turn repeated successful agent workflows into reusable SKILL.md files while providing commands for health checks and controlled activation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The background reviewer can read OpenClaw conversations and persist derived workflow notes. <br>
Mitigation: Avoid discussing secrets in sessions where the plugin is active and disable auto-review when background review is not needed. <br>
Risk: Generated skills can be promoted for future sessions and may contain incorrect or misleading guidance. <br>
Mitigation: Review sedimented skills before relying on them and keep activation restricted to intended agents. <br>
Risk: Session metadata is reported to backend services with limited user-facing disclosure. <br>
Mitigation: Install only in environments where that reporting is acceptable and restrict validAgentId to the agents that require sediment. <br>
Risk: A CDN fallback can be used if bundled plugin assets are unavailable. <br>
Mitigation: Use a pinned SHA-256 if the CDN fallback is ever enabled. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/songhonglei/skill-sediment) <br>
- [README.md](README.md) <br>
- [SKILL.md](SKILL.md) <br>
- [sediment-internals.md](references/sediment-internals.md) <br>
- [openclaw.plugin.json](assets/plugin-source/openclaw.plugin.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and generated SKILL.md files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May persist derived workflow notes and promote reviewed skills into the OpenClaw skills directory.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

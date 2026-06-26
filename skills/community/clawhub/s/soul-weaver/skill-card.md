## Description: <br>
Soul Weaver generates OpenClaw agent configuration files from curated persona templates or custom user inputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[addogiavara-tech](https://clawhub.ai/user/addogiavara-tech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to choose persona templates, preview generated configuration files, and create custom agent configuration guidance for OpenClaw assistants. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated configuration files can change agent behavior, memory habits, tool preferences, and workspace practices. <br>
Mitigation: Back up existing files, review diffs, and apply changes gradually before replacing SOUL.md, USER.md, MEMORY.md, TOOLS.md, cron jobs, or workspace files. <br>
Risk: Prompts or persistent memory files can accidentally capture secrets or sensitive personal details. <br>
Mitigation: Do not place secrets in prompts or memory files, and disable unwanted memory or tool behavior before deployment. <br>
Risk: Optional heartbeat or automation behavior can trigger repeated agent activity if enabled without review. <br>
Mitigation: Enable automation only after reviewing the generated HEARTBEAT.md and related workflow guidance. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/addogiavara-tech/soul-weaver) <br>
- [README](README.md) <br>
- [Templates reference](references/templates.md) <br>
- [Soul Maker reference](references/soul-maker.md) <br>
- [Security patterns reference](references/security-patterns.md) <br>
- [Heartbeat automation reference](references/heartbeat-automation.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance, code] <br>
**Output Format:** [JSON responses containing generated Markdown configuration files and guidance text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs can include multiple OpenClaw configuration files such as SOUL.md, IDENTITY.md, USER.md, MEMORY.md, TOOLS.md, AGENTS.md, HEARTBEAT.md, KNOWLEDGE.md, SECURITY.md, and WORKFLOWS.md.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

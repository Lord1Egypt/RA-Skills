## Description: <br>
Sofagent Lite adds a lightweight Chinese-language baseline rule set for AI agents, focused on four safety boundaries and six working habits without installing a daemon, orchestration engine, or audit tooling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kongfangxun](https://clawhub.ai/user/kongfangxun) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, individual agent users, and FDE teams use this skill to quickly place a concise discipline baseline into an agent context. It is intended for situations where users want behavior constraints without task orchestration, multi-agent collaboration, reflection memory, or commit-time audit features. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is intentionally global behavior guidance, so it can influence normal agent responses broadly once installed or pasted into an agent configuration. <br>
Mitigation: Review the Chinese-language rules before adding them to the agent context, and use the lite version only when a baseline discipline layer is desired without audit or orchestration features. <br>
Risk: Users may expect audit, git diff checks, reflection memory, or orchestration features that the lite release explicitly does not include. <br>
Mitigation: Use Sofagent Lite for the baseline rule layer only, and choose the full Sofagent release if those additional capabilities are required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kongfangxun/skills/sofagent-lite) <br>
- [Full sofagent project](https://github.com/KongFangXun/sofagent) <br>
- [SkillHub listing](https://skillhub.cn/skills/sofagent) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown rules and optional shell installation commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Installs a single SKILL.md file for OpenClaw or WorkBuddy, or prints the rules for manual configuration on other agent platforms.] <br>

## Skill Version(s): <br>
0.95.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

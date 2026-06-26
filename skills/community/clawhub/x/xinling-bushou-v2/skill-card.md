## Description: <br>
心灵补手 V3.0 provides six configurable flattery and role-play persona overlays for agents and subagents, including a Liu Bowen divination-themed persona. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[william22820785-cmyk](https://clawhub.ai/user/william22820785-cmyk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External ClawHub users and developers use this skill to install, configure, and activate agent persona overlays for OpenClaw-style agents and subagents. The skill produces prompt fragments, persona configuration, CLI guidance, and adapter launch configuration for supported environments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent assistant-persona modification can alter assistant control files such as SOUL.md. <br>
Mitigation: Install only when the persona overlay is intended, and review SOUL.md changes before restarting the assistant session. <br>
Risk: The Claude Code adapter can disable permission checks. <br>
Mitigation: Avoid using the Claude Code adapter unless the permission-bypass flag has been removed. <br>
Risk: The AI corpus upgrade script can send persona prompts to MiniMax using a local credential file. <br>
Mitigation: Do not run the corpus upgrade script unless external prompt sharing and local credential use are acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/william22820785-cmyk/xinling-bushou-v2) <br>
- [Publisher profile](https://clawhub.ai/user/william22820785-cmyk) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [Architecture documentation](artifact/architecture.md) <br>
- [CLAW systems research](artifact/claw-systems-research.md) <br>
- [Agent Skills standard](https://agentskills.io) <br>
- [Project homepage](https://aceworld.top) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown prompt fragments, JSON persona and configuration files, Python code snippets, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May persist persona state and update assistant control files during installation.] <br>

## Skill Version(s): <br>
3.0.0 (source: server release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

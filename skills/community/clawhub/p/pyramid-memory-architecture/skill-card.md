## Description: <br>
金字塔记忆架构 helps agents initialize and maintain layered workspace memory files, separating high-priority behavior rules, business memory, persona files, technical skill details, and scheduled-check responsibilities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[popo67ll](https://clawhub.ai/user/popo67ll) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to organize OpenClaw workspace memory, route new rules to the right files, and review memory, heartbeat, cron, and launchd responsibilities before changes are applied. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide edits to persistent workspace memory files and recurring task definitions, which may affect future agent behavior or cause duplicate scheduled work. <br>
Mitigation: Review proposed changes to AGENTS.md, MEMORY.md, HEARTBEAT.md, USER.md, TOOLS.md, cron, launchd, and generated reports before applying them. <br>
Risk: Workspace configuration may involve sensitive credential locations, notification channels, repositories, or git/GitHub sync actions. <br>
Mitigation: Keep secrets out of skill files and verify credential paths, channel targets, repository destinations, and sync commands before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/popo67ll/pyramid-memory-architecture) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/popo67ll) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with checklists, file-structure recommendations, reports, and example shell or JSON snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are proposals for workspace memory and scheduler configuration; users should review them before approving edits or sync actions.] <br>

## Skill Version(s): <br>
3.4.0 (source: SKILL.md frontmatter and ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

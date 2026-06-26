## Description: <br>
Sets up a multi-agent collaboration system with product, development, and operations agents, persistent memory, task routing, knowledge extraction, and parallel work. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aboutyao](https://clawhub.ai/user/aboutyao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to bootstrap a coordinated product, development, and operations agent team with shared memory files, routing rules, and reusable collaboration templates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent memory files may store personal details, preferences, decisions, tasks, and lessons without a clear retention policy. <br>
Mitigation: Require user confirmation before saving personal details or decisions, and periodically review or delete memory files. <br>
Risk: Heartbeat behavior can prompt proactive outreach after inactivity and periodic checks that may be unwanted. <br>
Mitigation: Disable unsolicited heartbeat outreach unless the user explicitly wants reminders or check-ins. <br>
Risk: Agent templates reference tool-driven actions such as GitHub work, skill installation, browser automation, scheduled posting, and publishing. <br>
Mitigation: Add explicit approval gates before any external service action, installation, automation, scheduled posting, or public publishing. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/aboutyao/team-collab-skill) <br>
- [Publisher profile](https://clawhub.ai/user/aboutyao) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [Long-term memory template](artifact/templates/MEMORY.md) <br>
- [Heartbeat template](artifact/templates/HEARTBEAT.md) <br>
- [Task routing rules](artifact/templates/shared/task-routing.md) <br>
- [Knowledge extraction rules](artifact/templates/shared/knowledge-extraction.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown templates with inline shell and JavaScript examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates reusable memory and agent state templates; no API credentials are required.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

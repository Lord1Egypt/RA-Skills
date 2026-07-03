## Description: <br>
Helps agent users, skill authors, maintainers, and teams create practical workflows, checklists, analyses, and implementation support for Gog-style Google Workspace work. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kyro-ma](https://clawhub.ai/user/kyro-ma) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agent users, skill authors, maintainers, and teams use this skill to adapt popular Gog-style workflow patterns into local-hardware-friendly plans, scripts, checklists, analyses, or adjacent skills for Google Workspace-oriented tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can be invoked too easily around sensitive mail, calendar, Drive, Sheets, Docs, or OAuth-authenticated account tasks. <br>
Mitigation: Narrow or disable implicit activation where possible and require explicit user confirmation before sending mail, changing calendar events, editing Workspace data, or using authenticated accounts. <br>
Risk: Workflow or implementation suggestions may be incorrect or incomplete for a user's specific Google Workspace setup. <br>
Mitigation: Validate outputs against the stated success criteria, review proposed changes before execution, and keep assumptions and required inputs visible. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kyro-ma/work-productivity-gog-google-workflow-helper-130446) <br>
- [Requirement Plan](references/requirement-plan.md) <br>
- [Popular ClawHub skill demand: self-improving agent](https://clawhub.ai/skills/self-improving-agent) <br>
- [Popular ClawHub skill demand: Gog](https://clawhub.ai/skills/gog) <br>
- [Popular ClawHub skill demand: Github](https://clawhub.ai/skills/github) <br>
- [Popular ClawHub skill demand: ontology](https://clawhub.ai/skills/ontology) <br>
- [Popular ClawHub skill demand: Obsidian](https://clawhub.ai/skills/obsidian) <br>
- [Popular ClawHub skill demand: Nano Pdf](https://clawhub.ai/skills/nano-pdf) <br>
- [Popular ClawHub skill demand: Agent Browser](https://clawhub.ai/skills/agent-browser-clawdbot) <br>
- [V2EX: multi-agent architecture discussion](https://www.v2ex.com/t/1222063) <br>
- [Hacker News: SMTP Relay with Web Dashboard](https://news.ycombinator.com/item?id=48601429) <br>
- [Hacker News: Google Workspace browser access discussion](https://news.ycombinator.com/item?id=48625428) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with optional code, shell command, checklist, and configuration blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should state assumptions, visible limits, validation notes, and remaining follow-up work when relevant.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

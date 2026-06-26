## Description: <br>
Orchestrate a virtual AI software team to build features, fix bugs, or complete software tasks through a local TeamClaw controller. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[topcheer](https://clawhub.ai/user/topcheer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to submit software requirements to TeamClaw, monitor worker progress, review deliverables, answer clarifications, and create or route tasks by role. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad coding requests may be routed to a local TeamClaw controller and workers without clear confirmation or data-use warnings. <br>
Mitigation: Use the skill only when delegation to TeamClaw is intended; confirm the controller and workers are trusted before submitting intake requests. <br>
Risk: Sensitive project data or secrets could be sent to TeamClaw workers during orchestration. <br>
Mitigation: Avoid sending secrets or sensitive project data unless TeamClaw storage, logs, and workspace file access controls have been reviewed. <br>


## Reference(s): <br>
- [TeamClaw API Quick Reference](references/api-quick-ref.md) <br>
- [TeamClaw Repository](https://github.com/topcheer/teamclaw) <br>
- [TeamClaw Documentation](https://github.com/topcheer/teamclaw/blob/main/README.md) <br>
- [TeamClaw Releases](https://github.com/topcheer/teamclaw/releases) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, API calls, guidance] <br>
**Output Format:** [Markdown with inline shell commands and API request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May summarize controller status, task progress, deliverables, clarifications, and troubleshooting guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

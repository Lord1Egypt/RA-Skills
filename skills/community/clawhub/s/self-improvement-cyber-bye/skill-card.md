## Description: <br>
Captures agent errors, hallucinations, logic bugs, and user corrections, then uses scheduled review workflows to attempt self-fixes, escalate unresolved issues, and promote resolved lessons into improvements. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cyber-bye](https://clawhub.ai/user/cyber-bye) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to give an agent persistent self-review routines for capturing mistakes, tracking corrections, running nightly reviews, and surfacing unresolved escalations for owner judgment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill directs the agent to retain sensitive personal, relationship, financial, project, and behavioral details in persistent local memory. <br>
Mitigation: Enable it only in workspaces where users understand the retention behavior, and provide a clear process to inspect, edit, delete, and disable saved memory files. <br>
Risk: The skill includes permanent and temporary scheduled review behavior that can keep local automation active. <br>
Mitigation: Review cron files before deployment, confirm active schedules with the workspace owner, and disable or remove scheduled files when persistent review is not desired. <br>
Risk: Autonomous self-fix attempts could convert incorrect analysis into durable guidance or memory entries. <br>
Mitigation: Keep owner review for escalated or low-confidence fixes, and require review before promoted lessons are treated as reliable future guidance. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/cyber-bye/self-improvement-cyber-bye) <br>
- [Publisher Profile](https://clawhub.ai/user/cyber-bye) <br>
- [Skill Definition](artifact/SKILL.md) <br>
- [Immediate Error Capture Hook](artifact/hooks/on-error.md) <br>
- [Nightly Review Hook](artifact/hooks/nightly-review.md) <br>
- [Memory Schema](artifact/memory/schema.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Guidance] <br>
**Output Format:** [Markdown instructions, local markdown logs, and structured JSON-compatible memory records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces persistent local records for errors, fixes, improvements, patterns, scheduled reviews, and escalation reports.] <br>

## Skill Version(s): <br>
4.0.1 (source: server release metadata; artifact frontmatter reports 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

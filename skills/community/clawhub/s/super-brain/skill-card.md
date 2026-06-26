## Description: <br>
Super Brain gives agents persistent cross-session memory for user preferences, conversation history, active projects, reminders, and response patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aboutyao](https://clawhub.ai/user/aboutyao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to give an agent local long-term memory for preferences, project context, conversation insights, reminders, and personalized response patterns across sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is designed for always-on local memory that profiles conversations, preferences, mood, projects, reminders, and decision history. <br>
Mitigation: Install only when that behavior is intended, and review or remove the startup activation block if automatic memory use is not desired. <br>
Risk: Persistent memory can retain sensitive or personal information, especially on shared machines or workspaces. <br>
Mitigation: Avoid sharing secrets with the skill, use the documented privacy controls and deletion commands, and apply retention settings appropriate for the workspace. <br>


## Reference(s): <br>
- [Super Brain ClawHub Page](https://clawhub.ai/aboutyao/super-brain) <br>
- [Workflow Reference](references/workflow.md) <br>
- [Database Schema Reference](references/schema.sql) <br>
- [Usage Examples](references/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline code and shell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local memory setup guidance, privacy controls, database queries, and agent workflow instructions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

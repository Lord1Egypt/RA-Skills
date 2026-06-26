## Description: <br>
Personal execution engine for tasks, projects, reminders, commitments, follow-ups, and next actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agenticio](https://clawhub.ai/user/agenticio) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use Todo to capture tasks, commitments, reminders, projects, follow-ups, and next actions in local storage, then ask for a prioritized next step, daily sync, or weekly review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Todo items are persisted locally and may contain personal tasks, commitments, or notes. <br>
Mitigation: Avoid storing secrets or highly sensitive personal details, and periodically review or clear ~/.openclaw/workspace/memory/todo when retained tasks are no longer needed. <br>


## Reference(s): <br>
- [Todo philosophy](references/philosophy.md) <br>
- [ClawHub Todo page](https://clawhub.ai/agenticio/todo) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [CLI text and Markdown-facing guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local task records, status summaries, prioritized recommendations, and review prompts.] <br>

## Skill Version(s): <br>
3.0.1 (source: release evidence and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

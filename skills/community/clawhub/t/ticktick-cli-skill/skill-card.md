## Description: <br>
Manage tasks and projects in TickTick. Use when user asks for tasks, to-dos, reminders, or event. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ilooch](https://clawhub.ai/user/ilooch) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to install and authenticate the TickTick CLI, then manage TickTick projects and tasks through safe command workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API tokens can expose TickTick account access if pasted into chat, command history, or logs. <br>
Mitigation: Prefer browser OAuth; when a token is required for headless setup, handle it as sensitive and revoke it if exposed. <br>
Risk: Task deletion or bulk changes can remove or irreversibly alter user task data. <br>
Mitigation: Require explicit confirmation for destructive actions and preview candidate tasks before deleting or bulk-updating them. <br>


## Reference(s): <br>
- [ClawHub TickTick Skill](https://clawhub.ai/ilooch/ticktick-cli-skill) <br>
- [TickTick](https://ticktick.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and concise text summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include JSON-mode command guidance for selecting projects or tasks by ID.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

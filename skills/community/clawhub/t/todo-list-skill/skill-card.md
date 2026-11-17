## Description:

A personal TODO management skill that lets an agent add, list, complete, update, and delete cross-session tasks from natural language, with local persistence, priorities, tags, and reminders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqing24](https://clawhub.ai/user/chenqing24)

### License/Terms of Use:

MIT-0

## Use Case:

Individuals and agent users use this skill to manage personal tasks in Chinese or English across sessions, including reminders, priorities, tags, and simple CLI-backed task operations. It is suited to personal productivity workflows rather than team project management or calendar synchronization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Task titles and raw task text are stored locally and may be sent through WorkBuddy or DingTalk reminder channels.

Mitigation: Avoid putting secrets, credentials, highly sensitive instructions, or confidential business data in TODO titles or reminder text.

Risk: Persistent reminders and cron-style jobs may continue running after initial setup.

Mitigation: Inspect reminder and cron entries after setup and uninstall, and remove any jobs that are no longer needed.

Risk: Broad natural-language triggers can mutate tasks when user intent is ambiguous.

Mitigation: Review and narrow trigger phrases before enabling automatic mutations, and require clarification for ambiguous complete, delete, or update requests.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqing24/skills/todo-list-skill)
- [Trigger reference](references/triggers.md)
- [Command reference](references/commands.md)
- [Error handling reference](references/errors.md)
- [Project source declared in package metadata](https://gitee.com/ccq/todo-list-skill)
- [python-dateutil documentation](https://dateutil.readthedocs.io/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Natural-language responses, Markdown guidance, JSON-capable CLI output, and shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local SQLite task data, local configuration, fallback files, reminder setup, and cron-style automation instructions.]

## Skill Version(s):

1.5.0 (source: server release evidence, pyproject.toml, manifest.yaml, CHANGELOG)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

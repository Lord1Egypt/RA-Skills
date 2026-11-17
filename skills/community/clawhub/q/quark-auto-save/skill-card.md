## Description:

Manage quark-auto-save tasks via CLI. (QAS, 夸克自动转存, 夸克转存, 夸克订阅, 管理任务, 运行任务, 修复失效链接, pan.quark.cn)

This skill is ready for commercial/non-commercial use.

## Publisher:

[cp0204](https://clawhub.ai/user/cp0204)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and users managing Quark Auto Save use this skill to inspect QAS configuration, search Quark share resources, add or run transfer tasks, repair invalid share links, and manage saved cloud files through a CLI client.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a QAS token and configured server URL to manage tasks and cloud files.

Mitigation: Install only with a trusted QAS server, prefer HTTPS, and avoid storing real cookies or tokens in persistent notes.

Risk: Commands can delete cloud files, delete tasks, update configuration, and run broad task operations.

Mitigation: Require manual confirmation before delete-file, delete-task, update-config, or broad run-task actions.

Risk: Task and file operations can be persistent or irreversible.

Mitigation: Review proposed task payloads, paths, and file names before executing mutations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cp0204/skills/quark-auto-save)
- [quark-auto-save homepage](https://github.com/Cp0204/quark-auto-save)
- [RegexRename wiki](https://github.com/Cp0204/quark-auto-save/wiki/正则处理教程)
- [MagicRegex wiki](https://github.com/Cp0204/quark-auto-save/wiki/魔法匹配和魔法变量)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON task/configuration payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands call a configured QAS server and print OK, OK with compact JSON, ERROR messages, or run-task logs.]

## Skill Version(s):

0.8.12 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description: <br>
Manage quark-auto-save (QAS) tasks through a CLI for adding, running, updating, and repairing Quark cloud-save tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cp0204](https://clawhub.ai/user/cp0204) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to manage QAS tasks for Quark share links, including adding subscriptions, running one-time saves, repairing invalid links, and updating task configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can mutate QAS tasks, global configuration, and Quark cloud files through a token-authenticated endpoint. <br>
Mitigation: Require explicit user confirmation before adding, running, deleting, renaming, or updating tasks, files, or configuration. <br>
Risk: Broad activation on Quark share links could cause unintended task creation or remote actions from untrusted prompts. <br>
Mitigation: Use the skill only with trusted prompts and confirm the selected share URL, task name, save path, and pattern before execution. <br>
Risk: The QAS token grants remote-control authority over the configured endpoint. <br>
Mitigation: Store QAS_BASE_URL and QAS_TOKEN outside the skill files, restrict endpoint access, and rotate the token if exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cp0204/quark-auto-save) <br>
- [quark-auto-save repository](https://github.com/Cp0204/quark-auto-save) <br>
- [RegexRename wiki](https://github.com/Cp0204/quark-auto-save/wiki/正则处理教程) <br>
- [MagicRegex wiki](https://github.com/Cp0204/quark-auto-save/wiki/魔法匹配和魔法变量) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and CLI text or JSON output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [QAS CLI responses begin with OK or ERROR; run-task can return multiline logs.] <br>

## Skill Version(s): <br>
0.8.12 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

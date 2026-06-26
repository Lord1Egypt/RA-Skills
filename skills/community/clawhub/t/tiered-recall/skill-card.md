## Description: <br>
分层回忆系统，解决上下文长度限制，保持项目延续性。默认自动加载最近7天记忆，支持手动全量回忆、自定义天数、项目回忆和主题回忆。当前版本采用 slim index，只保留文件名、行号和标题，不存摘要，避免 token 膨胀。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[davidme6](https://clawhub.ai/user/davidme6) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to restore workspace memory, recent logs, active project context, and topic-based recall across sessions. It is intended for local ClawHub/OpenClaw workspaces where retaining project continuity is useful. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can surface prior workspace notes and project snippets into future assistant context. <br>
Mitigation: Use it only in workspaces where this recall behavior is intended, and keep secrets, credentials, private notes, and sensitive source files out of memory logs and configured project key files. <br>
Risk: Broad project or topic keywords may recall unrelated context. <br>
Mitigation: Review and narrow configured project patterns and topic keywords when recall output includes irrelevant material. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/davidme6/tiered-recall) <br>
- [Publisher profile](https://clawhub.ai/user/davidme6) <br>
- [Project homepage from ClawHub metadata](https://github.com/davidme6/tiered-recall) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration] <br>
**Output Format:** [Markdown summaries, JSON recall data, and shell command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Default recall loads core memory, recent logs, active projects, and a slim topic index with configurable day and token budgets.] <br>

## Skill Version(s): <br>
1.2.2 (source: server release evidence, artifact frontmatter, and artifact manifest) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

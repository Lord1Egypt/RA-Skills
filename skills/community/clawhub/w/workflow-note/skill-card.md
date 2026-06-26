## Description: <br>
流程构建类笔记的写作规范与模板，用于为 workflows/ 分类撰写新笔记，覆盖文章结构、内容要求、质量标准和发布流程。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tino-chen](https://clawhub.ai/user/tino-chen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Documentation authors and agent users use this skill to draft Chinese workflow-building notes that explain how AI tools are combined into reproducible automation processes. It helps structure notes with clear outcomes, architecture, implementation steps, pitfalls, and references. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can lead an agent to copy local configuration, private prompts, internal paths, or other sensitive operational details into a note. <br>
Mitigation: Review the generated note and repository diff before committing or pushing; redact secrets, personal information, private prompts, internal paths, and operational details that should not be published. <br>
Risk: Generated workflow notes may include commands, configuration, or process guidance that is incomplete or misleading if copied from the wrong local context. <br>
Mitigation: Verify included commands and configuration against the intended environment and keep only reproducible details that are appropriate for the target audience. <br>


## Reference(s): <br>
- [Writing Example](references/example.md) <br>
- [Workflow Guide](https://tino-chen.github.io/notes/workflows/auto-note-system.html) <br>
- [ClawHub Skill Page](https://clawhub.ai/tino-chen/workflow-note) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with templates, checklists, and optional code or shell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Chinese prose is expected for note body content; generated notes may include full configuration excerpts when relevant.] <br>

## Skill Version(s): <br>
1.2.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

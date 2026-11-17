## Description:

按人物检索并导入长篇小说《主角》(陈彦 著，茅盾文学奖)的相关章节，作为后续任务的背景资料。

This skill is ready for commercial/non-commercial use.

## Publisher:

[junwugit](https://clawhub.ai/user/junwugit)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to locate and import chapters from Chen Yan's novel Zhujue by character, alias, or opera role so downstream agents can answer questions, analyze relationships, find passages, or draft commentary from grounded source text.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Retrieved source passages can include mature or derogatory literary content from the bundled novel.

Mitigation: Use the skill only when that source material is appropriate for the task, and review retrieved passages before reusing them in public or sensitive outputs.

Risk: The query workflow may write extracted passages to a user-chosen local path.

Mitigation: Choose an expected temporary or workspace path for exports and inspect the generated file before using it as agent context.

## Reference(s):

- [Characters Reference](references/characters.md)
- [ClawHub Skill Page](https://clawhub.ai/junwugit/skills/zhujue-characters)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and extracted text-file paths when chapter text is exported]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write selected cleaned source passages to a user-chosen local path when text export is requested.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

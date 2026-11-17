## Description:

Generate concise, personally grounded Chinese reflections and aphorisms by recalling GBrain, llm-wiki cognitive anchors, notes, and long-term questions before writing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn local second-brain material into Chinese reflections, maxims, quote-card lines, article endings, daily thoughts, or short 感悟. It is intended for writing tasks that benefit from grounded recall of personal notes, anchors, and long-term questions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Implicit invocation can read selected local second-brain notes, which may include private material.

Mitigation: Prefer explicit invocation when personal notes should be used, and review recalled context before sharing generated reflections.

Risk: Recall topics may include untrusted or shell-like text that is passed into gbrain or cm recall commands.

Mitigation: Avoid untrusted recall topics, and run recall with shell-disabled argument arrays or equivalent command handling.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/harrylabsj/skills/second-brain-maxim)
- [Second-brain aphorism style guide](artifact/references/style-guide.md)
- [Publisher profile](https://clawhub.ai/user/harrylabsj)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown containing Chinese prose, aphorism lines, optional numbered variants, and a concise recall receipt.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Defaults to Chinese unless the user asks for another language; normal output includes one 感悟 paragraph, one 箴言 line, and a brief 第二大脑回路 receipt.]

## Skill Version(s):

0.1.1 (source: server release evidence, SKILL.md metadata, clawhub.json, skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

公众号排版风格 Skill。支持两种风格：1)「知识拆解」风格（结构化分析型）；2)「简洁型」风格（自然段落流，默认风格）。使用方式：将文章结构按目标风格组织，生成符合该排版规范的 Markdown。

This skill is ready for commercial/non-commercial use.

## Publisher:

[facadefish](https://clawhub.ai/user/facadefish)

### License/Terms of Use:

MIT-0

## Use Case:

External writers and content teams use this skill to format WeChat public-account articles in either a concise natural-flow style or a structured analytical style. It guides the agent to produce Markdown that matches the target typography and publishing conventions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional publishing workflow references an unpinned `wenyan` renderer command and may be paired with publishing tools that handle WeChat credentials.

Mitigation: Pin or locally control the renderer version, review any publishing tool before use, and protect WeChat credentials outside the skill content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/facadefish/skills/wx-article-typography)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with optional inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces article structure, formatting guidance, image placeholders, and optional publishing workflow commands.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

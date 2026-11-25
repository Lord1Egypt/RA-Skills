## Description:

当用户希望参考某个网站改造界面时，本技能指导智能体用 curl 和标准库 Python 提取 CSS 设计 token，并将合适的视觉规范应用到本地样式表。

This skill is ready for commercial/non-commercial use.

## Publisher:

[oracis](https://clawhub.ai/user/oracis)

### License/Terms of Use:

MIT-0

## Use Case:

前端开发者可用本技能参考目标网站的视觉规范，为本地界面提取并应用颜色、圆角、字重、字号和间距等设计 token。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags possible requests to private-network services.

Mitigation: Use only trusted public URLs and check the destination host before running the fetcher.

Risk: The security review reports undeclared tool scope and says static analysis was partial.

Mitigation: Review the skill and fetcher behavior before installation or execution; treat the scan as incomplete.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/oracis/skills/ref-site-ui-tokens)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, JSON]

**Output Format:** [Markdown guidance, shell commands, and extracted CSS token data (text or JSON)]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a target website URL; token data can be saved as JSON.]

## Skill Version(s):

1.0.2 (source: frontmatter, server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

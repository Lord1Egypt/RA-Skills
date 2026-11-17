## Description:

Weixin Reader helps an agent extract the title, author, publication date, and full text from user-provided WeChat Official Account article links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[supengchao](https://clawhub.ai/user/supengchao)

### License/Terms of Use:


## Use Case:

External users and developers use this skill when they need an agent to read a WeChat Official Account article from an mp.weixin.qq.com link and return the article title, author, publication date, and main text. It is intended for article extraction from user-provided links without requesting login sessions or credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-provided WeChat article URLs are sent to the configured extraction tool.

Mitigation: Use only links the user intends to process, and avoid submitting private or access-controlled article URLs unless policy permits.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/supengchao/skills/weixin-reader-oc)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or plain text article extraction summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes article title, author, publication date, and main text when available.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Searches for WeChat public-account articles by keyword and extracts article text from mp.weixin.qq.com links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[onlyloveher](https://clawhub.ai/user/onlyloveher)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to find WeChat public-account articles, read linked article pages, and extract titles, account names, and paragraphs for summarization, translation, or analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make outbound web requests and fetch arbitrary URLs.

Mitigation: Use it only for explicit mp.weixin.qq.com article URLs or clearly intended WeChat public-account searches, and restrict network access where possible.

Risk: The skill installs and uses unpinned external dependencies, including miku-ai.

Mitigation: Pin and review dependencies before deployment, and re-scan the resolved environment.

Risk: The Playwright mode runs a real Chromium browser.

Mitigation: Run browser-based extraction in an isolated sandbox with the minimum filesystem and network access needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/onlyloveher/skills/wechat-articles-cn)
- [Publisher profile](https://clawhub.ai/user/onlyloveher)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Code, Files, Guidance]

**Output Format:** [Markdown text with shell and Python snippets, plus extracted article metadata and paragraphs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save a screenshot file when Playwright mode is used with a screenshot path.]

## Skill Version(s):

1.0.0 (source: server release metadata, SKILL.md frontmatter, skill.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

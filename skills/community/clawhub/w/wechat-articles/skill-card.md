## Description:

搜索和读取微信公众号文章的完整工具，支持关键词搜索与全文提取。

This skill is ready for commercial/non-commercial use.

## Publisher:

[johan-oilman](https://clawhub.ai/user/johan-oilman)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to search for WeChat Official Account articles by keyword and extract article title, account name, publication metadata when available, and body paragraphs from mp.weixin.qq.com article links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The reader can be steered to fetch non-WeChat, localhost, or private-network URLs.

Mitigation: Run in an isolated, low-privilege environment with outbound network controls and prefer a version that validates https://mp.weixin.qq.com URLs, blocks private or localhost destinations, and rejects unsafe redirects.

Risk: Playwright screenshot output can be directed to arbitrary writable paths.

Mitigation: Confine screenshots to a dedicated output directory with least-privilege filesystem permissions.

Risk: Unpinned Python and browser dependencies can change behavior across installations.

Mitigation: Pin dependencies and install Chromium in a controlled environment before use on sensitive machines or networks.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/johan-oilman/skills/wechat-articles)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Files]

**Output Format:** [Plain text CLI output and Python dictionaries/lists containing article search results, extracted article metadata, and body paragraphs; optional screenshot files may be written in Playwright mode.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search result URLs may be time-sensitive. Reading supports simple, Playwright, and automatic fallback modes.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata; artifact frontmatter states 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

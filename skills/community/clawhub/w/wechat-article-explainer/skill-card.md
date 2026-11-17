## Description:

Explains and summarizes WeChat public-account articles from user-provided links in plain language.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenhao11235813](https://clawhub.ai/user/chenhao11235813)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to fetch a WeChat article, extract its title, author or source, publication date, and content, then produce a concise plain-language explanation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The fetcher can access arbitrary URLs instead of enforcing the intended WeChat-only scope.

Mitigation: Use only trusted WeChat article links in a sandboxed environment and add strict mp.weixin.qq.com URL validation before broader use.

Risk: Unpinned Python dependencies and headless browser execution can expand operational risk during installation or runtime.

Mitigation: Pin dependencies and run the fetcher without access to sensitive local files or internal networks.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenhao11235813/skills/wechat-article-explainer)
- [ClawHub publisher profile](https://clawhub.ai/user/chenhao11235813)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown summary with optional JSON fetched article data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The local fetcher can write extracted article data to a JSON file when an output path is provided.]

## Skill Version(s):

1.0.1 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

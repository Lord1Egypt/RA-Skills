## Description:

中文搜索增强工具，整合百度、必应、微信、知乎等中文搜索引擎，支持高级搜索语法和时间过滤。

This skill is ready for commercial/non-commercial use.

## Publisher:

[careytian-ai](https://clawhub.ai/user/careytian-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, content creators, and market analysts use this skill to construct Chinese-focused web searches across Baidu, Bing China, WeChat, Zhihu, Toutiao, 360 Search, and related international engines without API keys.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms are sent to the selected external search engines.

Mitigation: Avoid submitting sensitive or confidential queries, and choose search engines appropriate for the user's privacy and compliance requirements.

Risk: The broad search trigger may activate this skill when a user intended a general search workflow.

Mitigation: Narrow or remove the generic trigger if only explicit Chinese-search activation is desired.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/careytian-ai/skills/zh-search-pro)
- [Usage examples](artifact/examples/usage-examples.md)
- [Changelog](artifact/CHANGELOG.md)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Shell commands]

**Output Format:** [Markdown guidance with web_fetch call examples and search URL patterns]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires web_fetch; no API key is required.]

## Skill Version(s):

1.0.0 (source: server release, config.json, metadata.json, CHANGELOG.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

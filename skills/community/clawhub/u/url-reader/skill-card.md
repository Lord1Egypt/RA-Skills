## Description:

Reads user-supplied URLs, identifies supported Chinese and general web platforms, extracts core page content, and saves Markdown and images locally.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justao](https://clawhub.ai/user/justao)

### License/Terms of Use:

MIT

## Use Case:

Developers and content operators use this skill to fetch and summarize web article content from platforms such as WeChat, Xiaohongshu, Toutiao, Douyin, Taobao, JD, Baidu, Zhihu, Weibo, Bilibili, and general websites. It is useful when an agent needs to turn a supplied URL into Markdown content and optionally save related images for later review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: URLs and page content may be processed by third-party fetchers such as Firecrawl or Jina.

Mitigation: Use the skill only with public or approved links, and avoid private, tokenized, internal, or account-sensitive URLs.

Risk: Browser automation may visit arbitrary supplied pages.

Mitigation: Review the source and destination of URLs before execution, and run browser automation in an environment appropriate for untrusted web content.

Risk: The skill can save fetched content and downloaded images to the local filesystem.

Mitigation: Confirm the output directory before use and review saved files before sharing, indexing, or importing them into other systems.

Risk: Reusable WeChat login state can be stored locally.

Mitigation: Set up WeChat login state only on trusted machines, protect the generated auth file, and delete or refresh it when no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/justao/skills/url-reader)
- [Firecrawl](https://www.firecrawl.dev/)
- [Jina Reader endpoint](https://r.jina.ai/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files]

**Output Format:** [Markdown content, status text, setup commands, and saved local files such as content.md and downloaded images.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use Firecrawl, Jina Reader, or Playwright depending on the target URL and configuration; content and images are saved to a local output directory when saving is enabled.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

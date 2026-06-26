## Description: <br>
Url Reader reads URLs from common Chinese content platforms, identifies the platform, extracts core page content, and can save the result as Markdown with downloaded images. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justao](https://clawhub.ai/user/justao) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent users can use this skill to fetch, summarize, and preserve web article content from supported platforms such as WeChat, Xiaohongshu, Toutiao, Douyin, Taobao, JD, Baidu, Zhihu, Weibo, Bilibili, and general websites. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Fetched URL content and images may be saved locally. <br>
Mitigation: Use the skill only for content appropriate for local storage, review the output directory, and delete saved files that should not persist. <br>
Risk: Some URLs or page data may be sent to third-party URL processors. <br>
Mitigation: Avoid private, internal, tokenized, or regulated links unless you have confirmed a local-only path for the specific workflow. <br>
Risk: The WeChat reader can retain browser state that functions like a login secret. <br>
Mitigation: Treat saved browser state as sensitive credential material and delete it when the reading task is complete. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/justao/url-reader) <br>
- [Firecrawl](https://www.firecrawl.dev/) <br>
- [Jina Reader](https://r.jina.ai/) <br>
- [Artifact README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown content with source metadata, optional saved files, and setup or fallback guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write Markdown content and downloaded image files to a local output directory when saving is enabled.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

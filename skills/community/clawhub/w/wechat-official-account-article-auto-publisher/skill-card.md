## Description: <br>
智能创作、提取微信公众号文章、生成封面并发布到微信公众号草稿箱，适用于按标题写稿、参考文章改写、提取 mp.weixin 链接、创建草稿并发布的工作流。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[majiabin2020](https://clawhub.ai/user/majiabin2020) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content operators, developers, and WeChat Official Account maintainers use this skill to create or rewrite Chinese public-account articles, generate cover images, preview output, create WeChat drafts, and optionally submit drafts for publishing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles real WeChat Official Account credentials and image-generation API credentials. <br>
Mitigation: Store credentials only in controlled configuration, limit access to the runtime environment, and rotate exposed credentials. <br>
Risk: The skill makes external network calls to WeChat, article URLs, and image-generation providers. <br>
Mitigation: Use dry-run and preview modes before creating drafts or publishing, and avoid feeding untrusted or internal URLs. <br>
Risk: Publishing workflows can move generated content into a live WeChat account when explicitly requested. <br>
Mitigation: Review generated article text, preview HTML, cover output, and draft metadata before running publish actions. <br>
Risk: Python dependencies and network integrations may change behavior outside the skill package. <br>
Mitigation: Install and run the skill in a locked dependency environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/majiabin2020/wechat-official-account-article-auto-publisher) <br>
- [Creation guide](CREATION_GUIDE.md) <br>
- [Publishing checklist](templates/conversation/publish_checklist.md) <br>
- [Configuration file](config.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown articles, JSON command output, generated files, and shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates article assets, preview HTML, cover image paths, WeChat draft media IDs, publish IDs, and status results when configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

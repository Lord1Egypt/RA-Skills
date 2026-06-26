## Description: <br>
Sora2 视频平台数据查询助手。覆盖作品详情、用户数据、搜索、评论、Cameo等全功能。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[new-ironman](https://clawhub.ai/user/new-ironman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to query Sora2 post, user, search, comment, Cameo, and media-related data through MaxHub APIs for content monitoring, comparison, and analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a sensitive MaxHub API key and sends Sora-related queries to www.aconfig.cn. <br>
Mitigation: Install only after review, keep the API key out of prompts and outputs, and use an account/key scoped for this integration. <br>
Risk: The security evidence notes that image upload behavior may send user images to the upstream service. <br>
Mitigation: Avoid uploading sensitive, private, or personal images unless the user has confirmed that sharing them with the upstream service is acceptable. <br>
Risk: The security evidence notes retrieval of no-watermark download links. <br>
Mitigation: Treat downloaded media as subject to content rights and platform terms before reuse or redistribution. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/new-ironman/sora-aggregate-scraper) <br>
- [Publisher Profile](https://clawhub.ai/user/new-ironman) <br>
- [MaxHub Website](https://www.aconfig.cn) <br>
- [Post & User API](references/api-post-user.md) <br>
- [Cameo API](references/api-cameo.md) <br>
- [Parameter Mappings](references/param-mappings.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, API Calls, Configuration guidance, Analysis] <br>
**Output Format:** [Markdown with inline shell commands, tables, links, and API response summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Bilingual English and Chinese responses; API keys should remain out of output.] <br>

## Skill Version(s): <br>
3.6.1 (source: server release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

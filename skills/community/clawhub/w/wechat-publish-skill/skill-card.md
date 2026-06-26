## Description: <br>
自动将 Markdown 文章转为适配微信公众号格式的 HTML，并批量发布至公众号草稿箱，支持封面图生成与专题管理。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hanbinsite](https://clawhub.ai/user/hanbinsite) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators, operators, and developers use this skill to convert Markdown articles into WeChat-compatible HTML, generate or attach cover images, and create WeChat Official Account drafts for review before publication. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses WeChat Official Account credentials to create drafts in an account-connected workflow. <br>
Mitigation: Store credentials in environment variables, restrict access to the runtime environment, and review generated drafts before publication. <br>
Risk: Optional AI cover generation sends prompts to a configured image-generation API endpoint. <br>
Mitigation: Use a trusted HTTPS endpoint and a scoped API key, and avoid sending sensitive unpublished content in prompts. <br>
Risk: Dependency ranges are not pinned to exact patched versions. <br>
Mitigation: Install with a reviewed lockfile or pinned dependency versions in production environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hanbinsite/wechat-publish-skill) <br>
- [Publisher profile](https://clawhub.ai/user/hanbinsite) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, API calls, Files] <br>
**Output Format:** [Markdown guidance with Python examples, environment-variable configuration, generated PNG cover files, converted HTML, and WeChat draft API results.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses WeChat Official Account credentials and optional AI image-generation credentials from environment variables; users should review drafts in WeChat before publishing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

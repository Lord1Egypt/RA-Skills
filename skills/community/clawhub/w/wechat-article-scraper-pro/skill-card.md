## Description:

微信公众号文章批量抓取工具，支持批量抓取公众号历史文章、导出为Markdown/HTML格式、自动提取封面图、标签、阅读量等数据。集成SkillPay支付接口，每次调用收0.001USDT。

This skill is for demonstration purposes and not for production usage.

## Publisher:

[baolige2023](https://clawhub.ai/user/baolige2023)

### License/Terms of Use:

MIT-0

## Use Case:

External users and content operations teams use this skill to collect WeChat Official Account article metadata and export gathered article records for review or reuse. The submitted artifact presents a paid scraper workflow, but the security evidence and UI indicate the current implementation should be treated as a review-required demonstration with simulated scraping behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release advertises a paid WeChat scraping service while security evidence says the implementation is mostly demo data.

Mitigation: Present the skill as demonstration or review-required until the documentation matches the implemented scraping behavior and the workflow is validated against real use conditions.

Risk: Payment credentials and web-server controls are exposed in the artifact.

Mitigation: Rotate exposed keys, move secrets to environment-managed storage, disable debug mode, and verify payment server-side before public deployment.

Risk: Task access controls are not evidenced as enforced.

Mitigation: Enforce task ownership and authorization checks before returning task status, article lists, or export files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/baolige2023/skills/wechat-article-scraper-pro)
- [Publisher profile](https://clawhub.ai/user/baolige2023)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance and generated local export files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Exports article records as Markdown or Excel files when the Flask app workflow completes.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

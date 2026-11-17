## Description:

帮助用户查询视频号作品的互动数据，区分精确计数与展示值，并说明未提供的指标。

This skill is ready for commercial/non-commercial use.

## Publisher:

[dunkong](https://clawhub.ai/user/dunkong)

### License/Terms of Use:

MIT-0

## Use Case:

视频号创作者和运营人员可查询作品的点赞、评论、分享等互动数据，核对数值是否精确，并导出结果用于分析或比较。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queries use a paid third-party API and may incur charges.

Mitigation: Check the current price and estimated total before obtaining approval for paid queries.

Risk: A distinct collection or favorite count may be unavailable despite the skill description.

Mitigation: Confirm the returned fields and identify missing metrics rather than treating another interaction as collections.

Risk: An API key is required and retrieved data can be exported to local files.

Mitigation: Keep the key in the local environment, avoid including it in exports, and review where result files are saved.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/dunkong/skills/wechat-channel-metrics)
- [曼格云 API 使用指南](https://api.we-media.cn/client/ai-guide)
- [曼格云 API 产品与文档](https://api.we-media.cn/client/products)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Excel files]

**Output Format:** [Markdown summary with optional JSON or Excel export]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports available metric precision, retrieval time, actual cost and partial results when applicable.]

## Skill Version(s):

1.4.2 (source: ClawHub release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

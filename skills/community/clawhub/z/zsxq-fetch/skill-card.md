## Description: <br>
知识星球帖子抓取助手可抓取指定知识星球的最新帖子，支持全部或精华帖筛选、单条帖子详情查询和多星球配置。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huxiaoqiao](https://clawhub.ai/user/huxiaoqiao) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and external users use this skill to fetch, summarize, or inspect Knowledge Planet posts that their configured account can access. It supports recent post collection, digest-only retrieval, single-post lookup, and joined-group discovery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review found that the skill can silently use an embedded account token to fetch private Knowledge Planet content instead of requiring the user's own token. <br>
Mitigation: Remove the hardcoded default token path and require an explicit user-managed ZSXQ_TOKEN before any API call. <br>
Risk: Token material may be stored in plaintext token.json if token persistence is used. <br>
Mitigation: Treat ZSXQ_TOKEN as a password and avoid plaintext token.json storage unless the user knowingly accepts that risk. <br>
Risk: Group enumeration and bulk fetching can expose the configured account's joined groups and private posts to the agent. <br>
Mitigation: Run group listing or bulk fetching only when the user explicitly intends to expose that account data for the current task. <br>


## Reference(s): <br>
- [知识星球 API 参考](artifact/references/api-reference.md) <br>
- [Skill README](artifact/README.md) <br>
- [ClawHub skill page](https://clawhub.ai/huxiaoqiao/zsxq-fetch) <br>
- [Knowledge Planet web application](https://wx.zsxq.com) <br>
- [Knowledge Planet API base URL](https://api.zsxq.com/v2) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration] <br>
**Output Format:** [Chinese Markdown summaries and JSON command output from the Node.js helper script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Post text may be truncated to 5000 characters; list fetching uses rate limits and retry backoff.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

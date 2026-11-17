## Description:

Fetches current Weibo, Douyin, and Baidu trending rankings for agent-readable trend summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[php737](https://clawhub.ai/user/php737)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to fetch current Chinese social and search trend rankings, identify cross-platform hot topics, and produce concise human-readable summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes live requests to Weibo, Douyin, and Baidu, so availability and returned rankings depend on those public services.

Mitigation: Check platform status metadata in the JSON output and treat missing or failed platform results as incomplete rather than definitive.

Risk: Runtime environments may lack undeclared Python dependencies such as curl_cffi and lxml.

Mitigation: Verify required Python packages are installed before deployment and surface dependency failures during pre-release testing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/php737/skills/today-trending)
- [Weibo hot search source](https://weibo.com/hot/search)
- [Douyin hot search source](https://www.iesdouyin.com/web/api/v2/hotsearch/billboard/word/)
- [Baidu realtime board source](https://top.baidu.com/board?tab=realtime)

## Skill Output:

**Output Type(s):** [JSON, Markdown, Guidance]

**Output Format:** [JSON data for platform rankings, with agent-rendered Markdown summaries for users.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Fetches up to 20 topics per platform; failed platforms return empty arrays with status metadata.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description: <br>
调用 Twitter/X 推文详情和搜索时间线接口，获取推文内容、作者信息、互动数据和搜索结果。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kyriswu](https://clawhub.ai/user/kyriswu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to fetch tweet details or search Twitter/X timelines, then present tweet content, author metadata, timestamps, interaction counts, links, and request status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Tweet IDs, search terms, cursors, and any supplied AZT_API_KEY are sent to the disclosed third-party service coze-js-api.devtool.uk. <br>
Mitigation: Use free mode when possible, prefer a dedicated paid key, and avoid sensitive searches or high-value credentials. <br>
Risk: The third-party API may return errors, quota-limit messages, or unavailable data. <br>
Mitigation: Check the returned status and error message before relying on results, and retry or adjust credentials only when appropriate. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kyriswu/twitterwebapi) <br>
- [Twitter detail API endpoint](https://coze-js-api.devtool.uk/twitter/fetch_tweet_detail) <br>
- [Twitter search timeline API endpoint](https://coze-js-api.devtool.uk/twitter/fetch_search_timeline) <br>
- [Devtool API key page](https://devtool.uk/plugin) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown summary or raw JSON response data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can report request success or failure, API key source, normalized tweet details, search results, and remaining quota messages.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

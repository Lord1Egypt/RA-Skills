## Description:

向善数据抖音 API 工具集。搜索抖音用户/视频，获取用户资料、视频详情、评论、播放量统计数据。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jesuslove](https://clawhub.ai/user/jesuslove)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to search Douyin users or videos, fetch profile and video details, retrieve comments, and summarize video statistics through the XSData API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Raw curl templates may combine user-supplied Douyin links, IDs, or keywords with shell commands.

Mitigation: Encode or serialize all user-controlled values before execution, avoid shell interpolation, and review generated commands before running them.

Risk: The XS_API_KEY credential is sent to api.xsdata.top and could be exposed if pasted into chat or logs.

Mitigation: Store the key in a secure environment variable, avoid pasting secrets into conversations, and install only when the API provider is trusted.

Risk: Douyin identifiers, links, and search terms are transmitted to a third-party API service.

Mitigation: Use the skill only for data you are comfortable sending to api.xsdata.top and limit requests to necessary inputs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jesuslove/skills/xiangshan-douyin)
- [XSData API base URL](https://api.xsdata.top)
- [Search users reference](reference/search-user.md)
- [Search videos reference](reference/search-video.md)
- [User data reference](reference/user-data.md)
- [User video list reference](reference/user-video-list.md)
- [Video comment reference](reference/video-comment.md)
- [Video detail reference](reference/video-detail.md)
- [Video statistics reference](reference/video-statistics.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, API calls, guidance]

**Output Format:** [Markdown summaries with curl examples and JSON parsing notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Douyin share links, user IDs, video IDs, keywords, and an XS_API_KEY credential to call api.xsdata.top.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

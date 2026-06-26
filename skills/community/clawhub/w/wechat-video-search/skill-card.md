## Description: <br>
Searches WeChat Channels videos through the TikHub API and returns video links plus basic engagement metadata. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ahsbnb](https://clawhub.ai/user/ahsbnb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to search WeChat Channels by keyword, retrieve video download links, and inspect basic metadata such as author, likes, duration, and publish time. Use requires a TikHub API token with WeChat Channels API permissions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The script prints the user's TikHub API token during normal command output. <br>
Mitigation: Remove token printing before use, use a least-privilege TikHub token when possible, and rotate any token exposed by this version. <br>
Risk: Search terms and API responses are sent to a third-party TikHub endpoint. <br>
Mitigation: Avoid sensitive search terms and review TikHub access requirements before operational use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ahsbnb/wechat-video-search) <br>
- [TikHub WeChat Channels search endpoint](https://api.tikhub.dev/api/v1/wechat_channels/fetch_search_latest) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON] <br>
**Output Format:** [Plain text summaries or raw JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search output may include WeChat Channels video IDs, titles, author names, like counts, durations, publish times, download links, and share links.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence; artifact metadata lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

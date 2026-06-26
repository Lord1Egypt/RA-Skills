## Description: <br>
查询友行青年社群的活动信息。当用户询问友行的活动、近期活动、活动安排、某个活动详情时使用。支持列出所有活动和根据活动ID获取详情。默认输出JSON，用户要求时可输出Markdown格式。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[longbai](https://clawhub.ai/user/longbai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to list activities for the 友行青年社群 community and retrieve detailed information for a specific activity by ID. It is intended for event lookup and presentation, with JSON output by default and Markdown formatting when requested. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs local Node.js commands and contacts the third-party api.cumen.fun service. <br>
Mitigation: Install and run it only in environments where outbound access to that service and local Node.js execution are acceptable. <br>
Risk: The detail lookup uses a CAMPAIGN_ID placeholder that could be filled with arbitrary untrusted text. <br>
Mitigation: Prefer campaign IDs returned by the list command and avoid pasting untrusted text into the placeholder. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/longbai/youxing) <br>
- [Cumen Service API Base](https://api.cumen.fun/api/xx.cumen.v1.CumenService) <br>
- [ListCampaignsOfClub API Endpoint](https://api.cumen.fun/api/xx.cumen.v1.CumenService/ListCampaignsOfClub) <br>
- [GetCampaign API Endpoint](https://api.cumen.fun/api/xx.cumen.v1.CumenService/GetCampaign) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [JSON by default, with Markdown tables or detail summaries when requested] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Activity times are converted from UTC to UTC+8; activity list order is not guaranteed by the upstream API.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

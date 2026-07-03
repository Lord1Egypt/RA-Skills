## Description: <br>
搜索万豪集团旗下W酒店，返回实时价格与预订链接，支持酒店详情查询和套餐优惠搜索，多旅游平台数据直连。暑期潮流旅行打卡，全球W酒店查询预订 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[travel-skills](https://clawhub.ai/user/travel-skills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-planning agents use this skill to search W Hotels by destination, inspect hotel details, compare package offers, and surface booking links returned by travel-platform APIs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Hotel search terms, locations, dates, and related keywords are sent to a configured proxy and travel-platform APIs. <br>
Mitigation: Use the skill only with data appropriate for those services, and verify PROXY_URL is a trusted HTTPS endpoint before providing PROXY_TOKEN. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/travel-skills/skills/whotels-booking) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown text with hotel result lists, details, package offers, and booking links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results depend on configured proxy and travel-platform API responses; prices and availability should be verified on the booking page.] <br>

## Skill Version(s): <br>
1.1.3 (source: server release evidence; artifact frontmatter reports 1.1.2) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

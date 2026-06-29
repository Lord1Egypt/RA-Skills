## Description: <br>
搜索万豪集团旗下W酒店并返回实时价格与预订链接，支持酒店详情查询和套餐优惠搜索，多旅游平台数据直连。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[travel-skills](https://clawhub.ai/user/travel-skills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-planning agents use this skill to search for W Hotels, review hotel details, compare package offers, and open booking links returned by travel platforms. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Hotel search terms, destination and date details, and selected hotel identifiers are sent to the configured proxy and travel API. <br>
Mitigation: Install only when that data flow is acceptable, and configure PROXY_URL only to a trusted HTTPS endpoint. <br>
Risk: The skill uses a proxy token for requests. <br>
Mitigation: Protect PROXY_TOKEN as a secret and avoid exposing it in logs, prompts, or shared configuration. <br>
Risk: Returned prices, availability, and booking links are third-party data that may change. <br>
Mitigation: Treat results as current lookup results and confirm final terms on the booking page before purchase. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/travel-skills/whotels-booking) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown text with hotel listings, hotel details, package offers, prices, identifiers, and booking links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results depend on the configured proxy and travel API; prices, availability, and booking links may change.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

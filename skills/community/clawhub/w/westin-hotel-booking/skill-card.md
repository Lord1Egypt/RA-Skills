## Description: <br>
搜索万豪集团旗下威斯汀酒店并返回实时价格与预订链接，支持酒店详情查询和套餐优惠搜索，多旅游平台数据直连。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[travel-skills](https://clawhub.ai/user/travel-skills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External travelers and travel assistants use this skill to search Westin hotels, inspect hotel details, compare package offers, and return booking links without inventing hotel data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Destination, hotel, and related search parameters are sent to a configured proxy service. <br>
Mitigation: Use only a trusted HTTPS PROXY_URL and a proxy token scoped to this service. <br>
Risk: Untrusted parties could alter environment variables that control the proxy endpoint or token. <br>
Mitigation: Run the skill only in environments where PROXY_URL and PROXY_TOKEN are controlled by trusted operators. <br>
Risk: Hotel prices, availability, and booking links are live external data and can change after the response is generated. <br>
Mitigation: Tell users to confirm final price and availability on the linked booking page before purchase. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/travel-skills/westin-hotel-booking) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown] <br>
**Output Format:** [Markdown-style Chinese text with hotel details, prices, amenities, package information, and booking links.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search and package results are limited by the script defaults to up to 10 items; prices are real-time and may change on booking pages.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

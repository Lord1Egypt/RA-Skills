## Description: <br>
万豪集团旗下威斯汀酒店实时搜索，返回价格与预订链接，支持酒店详情和套餐优惠查询，多旅游平台数据直连，零配置即装即用。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[travel-skills](https://clawhub.ai/user/travel-skills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External travelers and travel-planning agents use this skill to search Westin hotels by destination, price, and keywords, inspect hotel details, and find booking links or package offers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Hotel destinations, dates, keywords, and selected hotel identifiers may be sent to the configured cloud proxy and travel providers. <br>
Mitigation: Use only where this travel-query sharing is acceptable, and avoid entering sensitive personal travel intent. <br>
Risk: The proxy endpoint is controlled by runtime configuration rather than fixed in the artifact. <br>
Mitigation: Review the configured proxy URL and token handling before deployment. <br>
Risk: Prices, availability, policies, and booking links can change after the skill returns results. <br>
Mitigation: Confirm final price, availability, and hotel policies on the booking page before purchase. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown-formatted text with hotel listings, detail summaries, package offers, prices, and booking links.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results depend on live travel-provider responses and may be limited by the tool's result cap.] <br>

## Skill Version(s): <br>
1.1.3 (source: server release metadata; artifact frontmatter shows 1.1.2) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
XiaoChi helps agents summarize and compare public Meituan Waimai merchant and product information, including ratings, prices, delivery details, and sales signals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[CodeKungfu](https://clawhub.ai/user/CodeKungfu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and end users use XiaoChi to review public Meituan Waimai pages and produce lightweight merchant, product, pricing, delivery, and promotion summaries for comparison and reminders. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prices, delivery fees, availability, and delivery estimates can change by time and region. <br>
Mitigation: Include collection time and region or address context in outputs, and confirm time-sensitive details before relying on them. <br>
Risk: Using precise home address or account-specific data can expose sensitive location or personal information. <br>
Mitigation: Avoid entering precise home addresses unless necessary, and limit use to public merchant and product pages. <br>
Risk: Large-scale scraping, platform-control bypass, or ordering workflows could violate platform rules or change user state. <br>
Mitigation: Use the skill only for lightweight public-page research; do not use it for ordering, API reverse engineering, bypassing protections, or bulk scraping. <br>


## Reference(s): <br>
- [Meituan Waimai](https://waimai.meituan.com/) <br>
- [ClawHub release page](https://clawhub.ai/CodeKungfu/xiaochi) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown summaries and comparison tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include source links, collection time, and region or address context when available.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

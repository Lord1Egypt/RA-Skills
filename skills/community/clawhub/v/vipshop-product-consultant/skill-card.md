## Description: <br>
Queries Vipshop product details, review summaries, and review lists so an agent can produce product reputation reports and purchase recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[miketobusy](https://clawhub.ai/user/miketobusy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Shopping assistants and consumer-facing agents use this skill to gather Vipshop pricing, satisfaction, sizing, and review signals for a requested product ID. The collected data supports concise product comparisons, reputation summaries, and purchase guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill embeds and transmits fixed Vipshop account/session-like identity and tracking values with requests. <br>
Mitigation: Review before running, use only if comfortable contacting Vipshop with those values, and replace them with controlled values where appropriate. <br>
Risk: Generated JSON files can retain product, review, and request response data after the consultation is complete. <br>
Mitigation: Delete generated response and extracted-data JSON files when they are no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/miketobusy/vipshop-product-consultant) <br>
- [Publisher profile](https://clawhub.ai/user/miketobusy) <br>
- [Vipshop](https://www.vip.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown purchase report with JSON data files and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates product_info.json, review_summary.json, review_list.json, and raw API response JSON files during lookup.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

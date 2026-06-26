## Description: <br>
Waimai Merchant helps agents manage local food-delivery merchant and product records, including registration, product creation, price changes, stock status, and delivery-time settings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[harrylabsj](https://clawhub.ai/user/harrylabsj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill as a local operations console for food-delivery merchant onboarding, product catalog management, price updates, inventory status, and delivery-promise changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Administrative commands can delete, reject, suspend, deactivate, mark sold out, or otherwise change local merchant and product records. <br>
Mitigation: Show the target record and before/after values, require explicit same-turn confirmation for high-impact changes, and provide a rollback command or manual recovery step when available. <br>
Risk: Local SQLite changes may be mistaken for live platform updates. <br>
Mitigation: State that changes affect only ~/.waimai-merchant/merchant.db and are not synchronized to Meituan, Ele.me, or any live delivery platform. <br>
Risk: Local merchant data can include phone numbers, addresses, business license values, and contact names. <br>
Mitigation: Back up the database before important changes and avoid entering unnecessary sensitive data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/harrylabsj/skills/waimai-merchant) <br>
- [Publisher profile](https://clawhub.ai/user/harrylabsj) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline CLI commands and structured operation reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or modify local SQLite merchant and product records under ~/.waimai-merchant/merchant.db when the agent executes the recommended CLI workflow.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release, SKILL.md frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

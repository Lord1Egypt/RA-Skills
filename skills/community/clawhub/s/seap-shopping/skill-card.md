## Description: <br>
Supports shopping flows where a user searches for products, selects an item, and buys immediately or schedules a later purchase. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pingjiang](https://clawhub.ai/user/pingjiang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External OpenClaw users use this skill to turn purchase requests into product search results, numbered item selection, immediate checkout, or scheduled purchase tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may store payment-capable tokens and a delivery address in local configuration. <br>
Mitigation: Replace bundled placeholder or personal values before use, avoid reusable payment tokens when possible, and protect local configuration files. <br>
Risk: Broad purchase triggers and scheduled tasks could initiate an unintended immediate or future purchase. <br>
Mitigation: Narrow the trigger and require explicit review of item, price, address, and timing before every purchase. <br>
Risk: Session identifiers and product selections influence purchase execution. <br>
Mitigation: Validate session IDs and selected SKU values before running purchase commands. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/pingjiang/seap-shopping) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, JSON, Guidance] <br>
**Output Format:** [Markdown responses with CLI commands, JSON state/configuration, and purchase-result messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can create local session state and scheduled purchase tasks.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

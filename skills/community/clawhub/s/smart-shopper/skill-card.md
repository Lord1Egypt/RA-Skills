## Description: <br>
Smart Shopper helps agents search and compare products across Amazon, Temu, SHEIN, and local stores, build shopping lists, track prices, and handle SkillPay billing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[elevo11](https://clawhub.ai/user/elevo11) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External shoppers and shopping agents use Smart Shopper to generate product search links, compare platform options, manage shopping lists, track target prices, and surface local-store search links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The billing helper can charge a SkillPay account by default when invoked with a user ID and API key. <br>
Mitigation: Only provide SKILLPAY_API_KEY in contexts where agent-initiated charges are acceptable, and consider wrapping billing calls with manual approval. <br>
Risk: Local shopping-list and price-tracking files may reveal sensitive buying interests. <br>
Mitigation: Periodically clear local Smart Shopper data files or avoid storing sensitive purchases in the skill state. <br>


## Reference(s): <br>
- [Platform Reference](references/platforms.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/elevo11/smart-shopper) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown or JSON returned from command-line scripts, including product search links, comparison summaries, shopping lists, price-tracking status, and billing responses.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local JSON files for shopping-list and price-tracking state; billing requires SKILLPAY_API_KEY.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

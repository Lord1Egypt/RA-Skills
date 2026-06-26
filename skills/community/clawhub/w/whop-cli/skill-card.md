## Description: <br>
Manage a Whop digital products store via API by creating products and plans, tracking payments, and managing memberships. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[G9Pedro](https://clawhub.ai/user/G9Pedro) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Store operators and developers use this skill to manage Whop digital products and related plans, payments, memberships, files, webhooks, and other store resources through the Whop SDK. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agent actions can change products, pricing plans, memberships, or checkout links in a Whop store. <br>
Mitigation: Review product, checkout, and membership changes before execution. <br>
Risk: The skill uses Whop API credentials and company identifiers. <br>
Mitigation: Use a Whop API key scoped as narrowly as Whop allows, keep credentials out of prompts and logs, and rotate the key if it is exposed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/G9Pedro/whop-cli) <br>
- [Versatly Whop store](https://whop.com/versatly-holdings/) <br>
- [Versatly products](https://store.versatlygroup.com) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with JavaScript and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires WHOP_API_KEY and WHOP_COMPANY_ID environment variables.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

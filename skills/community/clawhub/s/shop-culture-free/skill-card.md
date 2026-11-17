## Description: <br>
Helps agents browse shopping categories, search for products, and view product details in a free shopping assistant workflow without checkout, payment, or order tracking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to guide product discovery, category browsing, semantic product search, and product detail lookup. It is suited to browsing and information review, not purchase execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill discusses shopping workflows where a user might provide sensitive payment or wallet material. <br>
Mitigation: Do not provide private keys, seed phrases, wallet keys, payment credentials, or other secrets while using this browsing-only skill. <br>
Risk: Callback URLs can expose results or trigger actions outside the agent session if they point to untrusted destinations. <br>
Mitigation: Use only callback URLs that you control and trust. <br>
Risk: Users may mistake the free browsing workflow for a checkout, payment, or order-management tool. <br>
Mitigation: Treat the free version as product browsing and search guidance only; do not rely on it for checkout, payment, order creation, or order tracking. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/shop-culture-free) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with JSON examples and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Browsing/search guidance only; the free version does not handle checkout, payment, or order tracking.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter reports 1.0.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

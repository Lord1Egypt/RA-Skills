## Description: <br>
Use this skill when a user wants to browse, compare, buy, pay for, query orders, track logistics, manage addresses, cancel/refund eligible orders, or apply after-sale service on Filtalgo through the bundled Agent Tool Gateway CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[filtalgo11](https://clawhub.ai/user/filtalgo11) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and shopping agents use this skill to operate Filtalgo shopping workflows through a Node-based CLI, including search, cart, checkout, payment handoff, order lookup, logistics, addresses, cancellations, refunds, and after-sale requests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can perform account-changing shopping actions, including cart, checkout, address, cancellation, refund, and after-sale operations. <br>
Mitigation: Require user review before running commands that change account, address, payment, order, cancellation, refund, or after-sale state. <br>
Risk: Checkout and refund flows can affect wallet payment or monetary outcomes. <br>
Mitigation: Confirm SKU IDs, quantities, currency minor units, totals, payment handoff URLs, refund amounts, and order identifiers before execution. <br>
Risk: Address and phone data may be exposed in prompts, command arguments, or CLI output. <br>
Mitigation: Minimize disclosure of full address and phone details and avoid printing tokens, secrets, or unnecessary personal data in user-facing output. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/filtalgo11/shopping-v3) <br>
- [Skill Instructions](artifact/SKILL.md) <br>
- [Filtalgo CLI Wrapper](artifact/scripts/filtalgo.js) <br>
- [OpenAI Agent Interface Metadata](artifact/agents/openai.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, JSON] <br>
**Output Format:** [Markdown guidance with shell commands and CLI JSON outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node and user authentication for Filtalgo account actions.] <br>

## Skill Version(s): <br>
1.1.0 (source: ClawHub release evidence; artifact frontmatter lists 0.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

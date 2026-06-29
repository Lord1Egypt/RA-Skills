## Description: <br>
Fetch a paywalled HTTP 402 URL and pay for it automatically from the agent wallet's Kamino vault yield, without spending the principal. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yukikm](https://clawhub.ai/user/yukikm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to access user-approved paid HTTP resources served through Subly or x402. It guides wallet setup, enforces payment caps, and reports delivered content with payment receipt details. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a Solana wallet keypair path and requires sensitive credential handling. <br>
Mitigation: Do not read, print, transmit, or expose the keypair file contents; only share public receipt information. <br>
Risk: The skill can initiate payments for paywalled resources. <br>
Mitigation: Only pay for URLs the user intends to purchase, treat the configured cap as a hard limit, and increase the cap only after user confirmation. <br>
Risk: A previous payment may be pending or unresolved. <br>
Mitigation: Follow the command result reason: retry only when delivery failed with payment pending, and report unresolved payment IDs instead of blindly paying again. <br>


## Reference(s): <br>
- [Subly payment protocol](https://github.com/SublyFi/subly-payment-protocol) <br>
- [ClawHub skill page](https://clawhub.ai/yukikm/subly-pay) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON command results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The payment command returns a single JSON object that may include delivered content, payment amount, recipient, payment ID, and receipt URL.] <br>

## Skill Version(s): <br>
0.1.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

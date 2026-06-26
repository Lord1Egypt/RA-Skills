## Description: <br>
Search grocery products, find store locations, add items to cart, and view profile information across Kroger-family stores. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[niemesrw](https://clawhub.ai/user/niemesrw) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users use this skill to search Kroger-family grocery products and store locations, compare available product details, and manage cart or profile workflows after Kroger authentication. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cart and profile features require Kroger login and expose reusable refresh tokens to the hosted proxy and, per the skill instructions, to agent long-term memory. <br>
Mitigation: Prefer self-hosting or local CLI mode with personal Kroger credentials, avoid saving refresh tokens in agent memory unless they can be removed or revoked, and review the skill before installing for account features. <br>
Risk: The skill can add items to a user's Kroger cart after authentication. <br>
Mitigation: Require explicit user confirmation before any cart change. <br>


## Reference(s): <br>
- [Supermarket ClawHub Listing](https://clawhub.ai/niemesrw/supermarket) <br>
- [Kroger Developer API](https://developer.kroger.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Kroger API request guidance, product or location summaries, OAuth login steps, token refresh steps, and cart-change confirmation prompts.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

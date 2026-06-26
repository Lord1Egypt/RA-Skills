## Description: <br>
Unloopa API helps an agent run Unloopa sales automation for local-business lead discovery, generated websites, outreach emails, and optional voice calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[echris6](https://clawhub.ai/user/echris6) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External sales and marketing operators use this skill to direct an agent through Unloopa workflows for finding local-business leads, generating websites, sending outreach, and managing Pro-only voice calls when configured. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Outbound sales actions may contact third parties by email or voice without adequate review. <br>
Mitigation: Require explicit user confirmation for recipient lists, email content, call scripts, lead counts, and campaign triggers before execution. <br>
Risk: Some actions may consume account credits or money, including voice calls, voice credits, and phone-number purchases. <br>
Mitigation: Check quota and plan status first, then require explicit approval for credit consumption, purchases, and paid account changes. <br>
Risk: The skill depends on a bearer token with access to the user's Unloopa account. <br>
Mitigation: Use UNLOOPA_API_KEY only from the configured environment and ask the user to check or rotate the key after unauthorized errors. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/echris6/unloopa-api) <br>
- [Unloopa API base URL](https://dashboard.unloopa.com/api/v1/) <br>
- [Unloopa settings](https://dashboard.unloopa.com/settings) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance, API call guidance] <br>
**Output Format:** [Markdown guidance with JSON request examples and shell-compatible environment-variable setup] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires UNLOOPA_API_KEY; API usage may consume credits or trigger outbound emails, calls, or purchases.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release metadata; artifact frontmatter version 1.3) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

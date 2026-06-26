## Description: <br>
Access the WOL API to browse catering items, place orders, check order history and account balance, and manage event registration status and sign-up. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[onokje](https://clawhub.ai/user/onokje) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External WOL users with an API token use this skill to complete authenticated catering and event-registration tasks from an agent chat. It helps users inspect menus, place food orders, review balances and order history, check event status, register for events, and check registration payment status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent broad authenticated WOL API access that can read account data, place catering orders, or register for events from ambiguous prompts. <br>
Mitigation: Use explicit WOL-specific prompts, verify WOL_BASE_URL before use, keep WOL_API_TOKEN out of logs, and require manual confirmation before orders, event registrations, or account-history lookups. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/onokje/wol-api) <br>
- [Wake-up On LAN site](https://wollan.nl) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, API calls, guidance] <br>
**Output Format:** [Markdown responses with curl commands and summarized API results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, WOL_API_TOKEN, and optionally WOL_BASE_URL; responses may include account data, order details, balances, and event registration status.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

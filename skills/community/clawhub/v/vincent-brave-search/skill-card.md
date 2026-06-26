## Description: <br>
Web and news search powered by Brave Search for agents that need current web results, news articles, or lookup support through Vincent's pay-per-call credit system. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[glitch003](https://clawhub.ai/user/glitch003) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent run Brave-backed web and news searches, manage Vincent DATA_SOURCES credentials, and report result metadata including per-call cost and remaining credit. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses Vincent search credits and can guide agents through paid credit top-ups, including wallet-based payment flows. <br>
Mitigation: Use prepaid or limited balances, review top-ups manually, and avoid enabling an agent wallet for this skill unless the payment behavior is intended. <br>
Risk: A reusable DATA_SOURCES credential is stored locally for agent use. <br>
Mitigation: Store credentials only in the declared config locations, restrict filesystem access where possible, and revoke the Vincent secret when access is no longer needed. <br>
Risk: Search queries are sent through Vincent and Brave-backed services. <br>
Mitigation: Avoid submitting sensitive queries unless the operator accepts the data flow and Vincent account controls are configured appropriately. <br>


## Reference(s): <br>
- [Vincent homepage](https://heyvincent.ai) <br>
- [ClawHub skill page](https://clawhub.ai/glitch003/vincent-brave-search) <br>
- [Publisher profile](https://clawhub.ai/user/glitch003) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search results include Vincent metadata such as call cost and remaining credit.] <br>

## Skill Version(s): <br>
1.0.69 (source: ClawHub server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

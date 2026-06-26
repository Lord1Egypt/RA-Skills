## Description: <br>
Interact with Twenty CRM (self-hosted) via REST/GraphQL. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JhumanJ](https://clawhub.ai/user/JhumanJ) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to configure an agent for a self-hosted Twenty CRM workspace and run REST or GraphQL API operations for CRM records such as companies. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read, create, edit, and delete Twenty CRM records using the configured token. <br>
Mitigation: Use a least-privilege API token and review POST, PATCH, and DELETE commands before execution. <br>
Risk: The skill loads credentials from a local env file. <br>
Mitigation: Keep the env file out of source control and logs. <br>
Risk: Untrusted or complex search strings may be unsafe until query encoding is fixed. <br>
Mitigation: Use simple, trusted search terms for company lookup operations. <br>


## Reference(s): <br>
- [Twenty CRM skill page](https://clawhub.ai/JhumanJ/twenty-crm) <br>
- [JhumanJ publisher profile](https://clawhub.ai/user/JhumanJ) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, API calls, JSON] <br>
**Output Format:** [Markdown with inline shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TWENTY_BASE_URL and TWENTY_API_KEY for the target Twenty CRM workspace.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

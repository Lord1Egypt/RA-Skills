## Description:

Helps authorized users query Wangxiaobao customer, recording, visit, tenant, and project data through the 旺小美 system.

This skill is ready for commercial/non-commercial use.

## Publisher:

[156554395](https://clawhub.ai/user/156554395)

### License/Terms of Use:

MIT-0

## Use Case:

Sales consultants, managers, and other authorized business users use this skill to retrieve customer records, recording lists and details, visit records, tenant/project context, and structured summaries from Wangxiaobao data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can access sensitive business and personal information, including customer, recording, visit, tenant, project, and user data.

Mitigation: Install and run it only for users authorized for the relevant Wangxiaobao tenants and projects, and avoid broad or ambiguous data requests.

Risk: Reusable authentication tokens are persisted locally and may be exposed in logged or shared environments.

Mitigation: Avoid running authorization commands in shared or logged environments until token printing and token-file permission handling have been reviewed and fixed.

Risk: Tenant or project switches can change the data context for later queries.

Mitigation: Confirm tenant and project switches before retrieving records or generating summaries.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/156554395/skills/wxm-assistant)
- [README](artifact/README.md)
- [Evaluation cases](artifact/evals/evals.json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, API calls, guidance]

**Output Format:** [Markdown or plain text summaries with command guidance and API-derived records when authorized]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include sensitive customer, recording, visit, tenant, project, and user information returned from Wangxiaobao services.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

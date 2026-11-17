## Description:

Read-only access to Up Bank accounts, transactions, categories, and tags.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ashleyjackson](https://clawhub.ai/user/ashleyjackson)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to review Up Bank balances, transactions, categories, tags, attachments, webhooks, and API connectivity with explicit user approval and a personal access token.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose sensitive banking data through read-only account and transaction queries.

Mitigation: Install only when this access is acceptable, require explicit approval for each API call, and show transaction details only when requested.

Risk: A persistent or shared UP_API_TOKEN could give unintended read access to Up Bank data.

Mitigation: Provide the token only for sessions that need banking queries, use the least access Up Bank allows, and avoid saving it permanently in shell profiles or shared environments.

Risk: Expired tokens and Up Bank rate limits can interrupt requests.

Mitigation: Ask for a fresh token on authentication failures and wait before retrying after rate-limit responses.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ashleyjackson/skills/upbank)
- [Publisher profile](https://clawhub.ai/user/ashleyjackson)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and API request guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only Up Bank API usage guidance requiring UP_API_TOKEN and explicit approval per request.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

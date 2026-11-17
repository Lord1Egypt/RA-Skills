## Description:

Helps agents use an authorized Zoom connection to retrieve user and recording details and manage meetings and webinars.

This skill is ready for commercial/non-commercial use.

## Publisher:

[byungkyu](https://clawhub.ai/user/byungkyu)

### License/Terms of Use:

MIT-0

## Use Case:

People and developers can ask an agent to look up Zoom meetings, recordings, webinars, and user profiles, or to make approved changes to their connected Zoom account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Changes may affect the wrong Zoom account or alter meetings, webinars, or recordings.

Mitigation: Confirm the account, connection, target, and intended effect with the user before every write; use read-only access where possible.

Risk: Long-lived API keys or connected-account data may be exposed.

Mitigation: Prefer OAuth, keep credentials out of output and destinations, and grant only the scopes needed for the task.

Risk: Hosted functions, triggers, and destinations can run actions or forward event data repeatedly.

Mitigation: Obtain separate approval for each automation and destination, including its target host, payload, and ongoing delivery.

## Reference(s):

- [Zoom skill release on ClawHub](https://clawhub.ai/byungkyu/skills/zoom-api)
- [Maton homepage](https://maton.ai)
- [Maton documentation](https://docs.maton.ai)
- [Maton CLI manual](https://cli.maton.ai/manual)
- [Zoom API documentation](https://developers.zoom.us/docs/api/)
- [Zoom OAuth scopes](https://developers.zoom.us/docs/integrations/oauth-scopes/)
- [Companion API gateway skill](https://clawhub.ai/byungkyu/api-gateway)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Code, Guidance]

**Output Format:** [Markdown with command and API response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires network access and a user-authorized Maton connection to Zoom; account changes need explicit confirmation.]

## Skill Version(s):

1.2.6 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Interact with a Skylight Calendar frame to view or create calendar events, manage family chores and lists, create task box items, and check reward points.

This skill is ready for commercial/non-commercial use.

## Publisher:

[riyadchowdhury](https://clawhub.ai/user/riyadchowdhury)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to operate their own Skylight smart display through calendar, chore, list, task box, category, reward, and frame API workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires Skylight account-level access through a password-derived token or reusable authorization token.

Mitigation: Use it only with an account you control, keep SKYLIGHT_PASSWORD and SKYLIGHT_TOKEN out of shared shell history and source files, and rotate credentials if exposed.

Risk: Changing SKYLIGHT_URL could direct credentials or tokens away from the official Skylight service.

Mitigation: Keep SKYLIGHT_URL fixed to https://app.ourskylight.com unless a trusted reviewer explicitly approves another endpoint.

Risk: The proxy-capture authentication path requires trusting an interception certificate and can expose reusable tokens.

Mitigation: Prefer the email/password login flow, and use proxy capture only when the operator understands and accepts the certificate and token-handling risks.

Risk: The artifact describes an unofficial, reverse-engineered API whose endpoints may change without notice.

Mitigation: Review generated API calls before execution and verify behavior against the user's own Skylight account after service changes.

## Reference(s):

- [ClawHub Skylight Skill](https://clawhub.ai/riyadchowdhury/skills/skylight-skill)
- [Skylight Homepage](https://ourskylight.com)
- [Skylight App Endpoint](https://app.ourskylight.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Skylight frame ID and either account credentials or a pre-captured authorization token.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

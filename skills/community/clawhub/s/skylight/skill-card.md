## Description:

Interact with Skylight Calendar frame - manage calendar events, chores, lists, task box items, and rewards.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yurybubnov](https://clawhub.ai/user/yurybubnov)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to operate their own Skylight Calendar smart display through an unofficial API, including calendar events, chores, lists, task box items, categories, rewards, frame details, and devices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles Skylight credentials and bearer tokens that can access household calendar data and related resources.

Mitigation: Use a dedicated least-privilege account where possible, store credentials in a secret manager, and treat exported tokens like passwords.

Risk: Changing SKYLIGHT_URL or proxy-capturing live tokens can expose credentials or tokens to an unintended host or tool.

Mitigation: Keep SKYLIGHT_URL pinned to the official Skylight host and avoid proxy token capture unless the operator fully understands the exposure.

Risk: The integration relies on an unofficial, reverse-engineered API that may change without notice.

Mitigation: Review commands before execution, limit use to accounts the operator owns, and revalidate behavior when API calls fail or return unexpected data.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yurybubnov/skills/skylight)
- [Skylight Web App](https://app.ourskylight.com)
- [Skylight Calendar Website](https://ourskylight.com/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, API Calls, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash commands and JSON:API request guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Skylight account credentials or bearer token plus SKYLIGHT_FRAME_ID; API responses use JSON:API.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact README says 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

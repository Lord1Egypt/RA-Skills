## Description:

Manage Zoom meetings, webinars, registrants, cloud recordings, and event workflows via the Zoom API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hith3sh](https://clawhub.ai/user/hith3sh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and assistants use this skill to help users schedule and manage Zoom meetings, webinars, registrants, recordings, and related event workflows through a connected Zoom account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on a persistent third-party plugin that handles the user's Zoom OAuth connection and can access broad Zoom capabilities.

Mitigation: Install only after trusting ClawLink, reviewing requested Zoom scopes, and confirming how to revoke the Zoom connection and remove the plugin.

Risk: Create, update, delete, and registrant actions can change meetings, webinars, recordings, or participant data.

Mitigation: Use preview and explicit user confirmation before every write or destructive action, and verify the target resource and intended effect.

Risk: Some workflows depend on Zoom account plan features, add-ons, recording settings, or registration being enabled.

Mitigation: Check the connected account's Zoom plan, add-ons, recording settings, and registration configuration before attempting those workflows.

## Reference(s):

- [Zoom API Documentation](https://developers.zoom.us/docs/api/)
- [Zoom Meeting API Reference](https://developers.zoom.us/docs/api-reference/zoom-api/)
- [ClawLink OpenClaw Documentation](https://docs.claw-link.dev/openclaw)
- [ClawLink Verification](https://claw-link.dev/verify)
- [ClawHub Skill Page](https://clawhub.ai/hith3sh/skills/zoom-meetings)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, API calls]

**Output Format:** [Markdown with inline bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a connected Zoom account through ClawLink; write actions should be previewed and explicitly confirmed.]

## Skill Version(s):

1.0.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

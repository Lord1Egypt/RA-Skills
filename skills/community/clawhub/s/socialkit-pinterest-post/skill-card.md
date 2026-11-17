## Description:

Creates a Pinterest Pin (image, carousel or video) on a chosen board through the official Pinterest API v5 after the user approves it. Use when the user wants to pin or post on Pinterest.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ahmadhussain0335](https://clawhub.ai/user/ahmadhussain0335)

### License/Terms of Use:

MIT-0

## Use Case:

External users use the skill to prepare and publish image, carousel, or video Pins to a selected Pinterest board after reviewing and approving each post.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The recommended sign-in callback is a third-party website that may observe the OAuth authorization code and state.

Mitigation: Use a Pinterest-supported callback you control, or explicitly accept the callback site's visibility; review the separate socialkit-social-core dependency and keep approval required for every post.

## Reference(s):

- [Pinterest setup](references/setup.md)
- [Pinterest access tiers](https://developers.pinterest.com/docs/key-concepts/access-tiers/)
- [Pinterest authentication and authorization](https://developers.pinterest.com/docs/getting-started/set-up-authentication-and-authorization/)
- [ClawHub skill page](https://clawhub.ai/ahmadhussain0335/skills/socialkit-pinterest-post)

## Skill Output:

**Output Type(s):** [Pinterest Pins, Text]

**Output Format:** [Pinterest Pin (image, carousel, or video) with a text result summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a board ID and user approval before publishing.]

## Skill Version(s):

0.3.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

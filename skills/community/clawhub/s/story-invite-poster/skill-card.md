## Description:

Turn photos, memories, and event details into polished custom invitation posters.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shuminliu026](https://clawhub.ai/user/shuminliu026)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to turn personal photos, memories, and event details into custom invitation posters for celebrations such as birthdays, housewarmings, weddings, anniversaries, and baby events.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected photos, poster assets, event details, and the user's Mew.design API key are sent to Mew.design.

Mitigation: Use the skill only when that data sharing is acceptable, and avoid private addresses, personal contact details, or sensitive images unless they are necessary for the invitation.

Risk: Local-only images may need a temporary third-party upload before downstream APIs can access them.

Mitigation: Prefer user-provided public image URLs, and use temporary third-party upload only after explaining the privacy tradeoff and receiving user consent.

Risk: Generated invitation posters can obscure important event text or cover meaningful people, pets, or objects.

Mitigation: Inspect the poster for readability, identity preservation, and clear event hierarchy before returning it, and retry generation when the result fails those checks.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shuminliu026/skills/story-invite-poster)
- [Mew.design login and API key setup](https://mew.design/login)
- [Mew.design image-process API endpoint](https://api.mew.design/open/api/image/process)
- [Mew.design design-generate API endpoint](https://api.mew.design/open/api/design/generate)

## Skill Output:

**Output Type(s):** [Markdown, Text, Guidance]

**Output Format:** [Markdown image link with a short descriptive line and an original-image link]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The workflow may call Mew.design APIs and may ask for a public image URL or consent before any temporary third-party upload.]

## Skill Version(s):

1.0.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

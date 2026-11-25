## Description:

Generates videos and images in Google Flow through useapi.net with Veo 3.1, Omni Flash, and Nano Banana, then saves the results locally.

This skill is ready for commercial/non-commercial use.

## Publisher:

[useapi](https://clawhub.ai/user/useapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creators use this skill to generate or edit short videos and images from prompts, optionally using reference media, through a connected Google Flow account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reference images, videos, and other selected local media may be uploaded to the external useapi.net service for processing.

Mitigation: Review each file before using it, avoid sensitive media, and proceed only when you trust the external service to receive it.

Risk: The skill includes advice about retrying or changing prompts and models after provider moderation refusals, which could be used to work around content safeguards.

Mitigation: Follow the provider's moderation rules; do not rephrase, switch models, or retry to evade a refusal.

Risk: The skill requires a useapi.net API token and sends it to the external API for authenticated requests.

Mitigation: Use the token only with the trusted service, keep it in the environment, and do not print or store it in files.

## Reference(s):

- [useapi.net Google Flow API documentation](https://useapi.net/docs/api-google-flow-v1?utm_source=clawhub.ai&utm_medium=skill&utm_campaign=clawhub-google-flow)
- [Connect a Google Flow account](https://useapi.net/docs/start-here/setup-google-flow)
- [useapi.net account and API token setup](https://useapi.net/docs/start-here/setup-useapi)
- [useapi.net subscription information](https://useapi.net/docs/subscription)
- [Video generation options](https://useapi.net/docs/api-google-flow-v1/post-google-flow-videos)
- [Image generation options](https://useapi.net/docs/api-google-flow-v1/post-google-flow-images)

## Skill Output:

**Output Type(s):** [Video files, Image files, Shell commands]

**Output Format:** [MP4 videos and JPEG images saved locally, with output paths printed as text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Model, duration, aspect ratio, count, and output directory are configurable.]

## Skill Version(s):

1.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

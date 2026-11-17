## Description:

Creates dated opening, promotion, flash-sale, and closing PA scripts and spoken audio for a single store campaign window.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beatra-ai](https://clawhub.ai/user/beatra-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Store teams and retail marketers use this skill to prepare dated opening, promotional, flash-sale, and closing announcements for one campaign window, then generate spoken versions using a consistent store voice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The required shared credential also authorizes unrelated paid image, video, and music generation.

Mitigation: Review the full authorization before approving; use a speech-scoped credential if offered, and revoke access in the Beatra Console when finished.

Risk: The client sends installation analytics without an opt-out.

Mitigation: Review the documented installation-registration data and proceed only if that reporting is acceptable.

Risk: Voice cloning requires uploading a speaker sample and may incur charges.

Mitigation: Upload samples only with permission, and confirm the live campaign or clone estimate before submitting paid work.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/beatra-ai/skills/store-pa-broadcast-pack)
- [Beatra skill page](https://beatra.ai/skills/store-pa-broadcast-pack)
- [Campaign workflow](references/workflow.md)
- [Billing errors and recovery](references/billing-errors-and-recovery.md)
- [Installation and authorization](references/installation-and-auth.md)
- [Updates and security](references/updates-and-security.md)

## Skill Output:

**Output Type(s):** [Text, Audio files, Guidance]

**Output Format:** [Dated PA announcement scripts and generated spoken audio, typically MP3]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Campaign-window dates; typically four reads using one consistent voice.]

## Skill Version(s):

0.2.2 (source: release evidence and artifact manifest)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

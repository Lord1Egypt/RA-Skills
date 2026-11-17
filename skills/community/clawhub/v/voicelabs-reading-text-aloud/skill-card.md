## Description:

Turns user-approved text into spoken audio with a VoiceLabs voice and returns an audio link.

This skill is ready for commercial/non-commercial use.

## Publisher:

[devino](https://clawhub.ai/user/devino)

### License/Terms of Use:

MIT-0

## Use Case:

VoiceLabs users can narrate supplied text or scripts with a voice from their connected account and receive links to the generated audio.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Text submitted for narration is sent to VoiceLabs.

Mitigation: Submit only text the user has provided or approved and make users aware of the transfer before use.

Risk: Speech generation may consume the user's VoiceLabs allowance.

Mitigation: Confirm the user understands generation is metered and stop if the account reports exhausted quota.

Risk: Provider-hosted audio links expire.

Mitigation: Advise users to access or save audio promptly; request a refreshed link when needed.

## Reference(s):

- [Reading Text Aloud on ClawHub](https://clawhub.ai/devino/skills/voicelabs-reading-text-aloud)

## Skill Output:

**Output Type(s):** [Text]

**Output Format:** [Markdown with audio links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Audio links are temporary; multipart narration returns labeled links in section order.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

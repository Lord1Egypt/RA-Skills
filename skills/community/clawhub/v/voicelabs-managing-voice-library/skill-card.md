## Description:

Lists and manages VoiceLabs voice profiles, adds built-in voices, recommends voices by language, and clones recordings only after confirming speaker consent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[devino](https://clawhub.ai/user/devino)

### License/Terms of Use:

MIT-0

## Use Case:

VoiceLabs account users can review their voice library, add preset voices for narration or other languages, and create a voice clone from a recording when the speaker has consented.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Voice-profile data and cloning recordings are sent through a connected VoiceLabs account.

Mitigation: Connect the account only if comfortable sharing that data with VoiceLabs; approve the cloning permission only when needed.

Risk: Cloning without speaker consent can misuse someone's voice, and cloned voices remain in the account until managed in the studio.

Mitigation: Confirm the recording is the user's own voice or the speaker clearly consented before cloning; manage saved clones in the VoiceLabs studio.

## Reference(s):

- [Managing Voice Library on ClawHub](https://clawhub.ai/devino/skills/voicelabs-managing-voice-library)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown voice-profile table and concise guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports voice IDs and whether a preset was newly added or already existed when available.]

## Skill Version(s):

1.0.1 (source: ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

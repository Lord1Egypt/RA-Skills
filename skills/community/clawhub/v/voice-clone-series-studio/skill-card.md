## Description:

Clone one authorized voice and reuse it for consistent narration across a podcast, course, creator series, or recurring update.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beatra-ai](https://clawhub.ai/user/beatra-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Creators, podcasters, course teams, and brands use the skill to create an authorized reusable voice and produce recurring narration with aligned subtitles. Speaker consent is required before uploading a voice sample, and paid production steps require approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests broad media and spending permissions and performs recurring installation telemetry.

Mitigation: Review the requested permissions and telemetry before connecting; approve billable cloning, synthesis, and audio processing only after reviewing their scope and price.

Risk: Voice recordings and scripts are processed externally.

Mitigation: Obtain explicit speaker consent before uploading and send only recordings and scripts approved for external processing.

Risk: The scan notes a risk involving shared uninstall state, and its coverage is partial.

Mitigation: Review the uninstall and disconnect guidance before removal, and account for the scan's stated coverage limits when assessing this skill.

## Reference(s):

- [Series voice workflow](artifact/references/workflow.md)
- [Speech and audio guide](artifact/references/speech-and-audio.md)
- [Updates and security](artifact/references/updates-and-security.md)
- [Voice Clone Series Studio on Beatra](https://beatra.ai/skills/voice-clone-series-studio)
- [Voice Clone Series Studio on ClawHub](https://clawhub.ai/beatra-ai/skills/voice-clone-series-studio)

## Skill Output:

**Output Type(s):** [Audio, Subtitles, Text, Guidance]

**Output Format:** [Episode audio files (MP3) with optional aligned SRT/VTT subtitles and episode status details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Episodes are delivered in order; loudness normalization is an optional paid finishing step.]

## Skill Version(s):

0.2.5 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

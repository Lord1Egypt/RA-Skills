## Description:

Create a talking-avatar video from an authorized portrait and script or voice recording, with optional narration, subtitles, and lip-sync review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beatra-ai](https://clawhub.ai/user/beatra-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and creators can turn an authorized portrait and script or voice recording into a reviewed talking-avatar video for explainers, training, announcements, or onboarding.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review is incomplete and flags recurring analytics and authorization scopes beyond this video workflow.

Mitigation: Review the analytics and requested scopes, and avoid installation until they are clear.

Risk: Portraits, recordings, and script text may be sent to Beatra during video generation.

Mitigation: Use only media and text you are comfortable sharing with Beatra, and confirm authorization for the portrait and voice before generation.

## Reference(s):

- [Workflow and Payloads](artifact/references/workflow.md)
- [Speech, Voices, and Audio Finishing](artifact/references/speech-and-audio.md)
- [Price a Whole Job](artifact/references/price-a-whole-job.md)
- [Updates and Security](artifact/references/updates-and-security.md)

## Skill Output:

**Output Type(s):** [Video, Subtitles, Text]

**Output Format:** [MP4 video, optional JSON/SRT/VTT subtitle files, and a brief text plan and quality review.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Longer scripts may produce several videos in order.]

## Skill Version(s):

0.3.6 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

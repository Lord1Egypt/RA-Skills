## Description:

Send the user a video message with an AI avatar that speaks any text, using Runway Character API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yining1023](https://clawhub.ai/user/yining1023)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill to create short asynchronous video messages where an AI avatar speaks provided text, such as deploy updates, code review walkthroughs, incident summaries, onboarding notes, and progress recaps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Message text, avatar images or prompts, and generated media workflow data are sent to Runway through the user's API key.

Mitigation: Use the skill only when that data sharing is acceptable and avoid including sensitive content in the generated message or avatar prompt.

Risk: Passing an API key as a command-line argument can expose it through shell history or process listings.

Mitigation: Set RUNWAY_API_SECRET in the environment instead of passing --api-key.

Risk: Generated videos default to /tmp, which may be inappropriate on shared machines.

Mitigation: Use a private or explicit --output path when local media files should not be left in shared temporary storage.

Risk: Unpinned runtime dependencies can change behavior over time.

Mitigation: Pin dependencies before production use.

Risk: Selecting voices based on inferred appearance can create avoidable bias or misrepresentation.

Mitigation: Choose voices based on explicit user preference.

## Reference(s):

- [Runway Developer Documentation](https://docs.dev.runwayml.com)
- [Runway Developer Portal](https://dev.runwayml.com)
- [Source Repository](https://github.com/runwayml/openclaw-skill-send-video-message)
- [ClawHub Skill Page](https://clawhub.ai/yining1023/skills/send-video-message)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, code, media file]

**Output Format:** [Markdown guidance with inline shell commands and generated MP4 media paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Video generation requires a Runway API key; optional square or vertical re-encoding requires ffmpeg.]

## Skill Version(s):

1.0.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

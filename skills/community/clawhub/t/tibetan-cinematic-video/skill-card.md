## Description:

Generates authentic Tibetan cinematic videos in 9:16 portrait format via Google Veo from a user-provided image and exactly three Chinese theme words.

This skill is ready for commercial/non-commercial use.

## Publisher:

[j3ffyang](https://clawhub.ai/user/j3ffyang)

### License/Terms of Use:

MIT-0

## Use Case:

External users and creators use this skill to turn Tibetan-themed source imagery and three Chinese theme words into a short portrait video prompt and generated MP4. It is intended for cinematic cultural video generation with explicit input validation, output-path constraints, and Tibetan authenticity guardrails.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends the supplied image to Google Veo for video generation, which can expose sensitive personal or proprietary imagery to an external service.

Mitigation: Avoid sensitive images and confirm that users are comfortable sending the image to Google Veo before generation.

Risk: Broad trigger terms such as monastery, prayer wheel, and Himalayan could start generation when the user did not intend to create a video.

Mitigation: Consider tightening triggers or adding an explicit confirmation step before calling Google Veo.

Risk: Generated media is saved locally under ~/.openclaw/workspace/tibetanProc/, which may retain user-provided image derivatives or generated content longer than expected.

Mitigation: Review local retention expectations and clean generated media when it is no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/j3ffyang/skills/tibetan-cinematic-video)
- [ClawHub publisher profile](https://clawhub.ai/user/j3ffyang)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance, files]

**Output Format:** [Markdown guidance with Google Veo prompt parameters and an MP4 file saved to the configured local path]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires one input image and exactly three comma-separated Chinese theme words; outputs a single 9:16 video file named yymmddHHMM_{title}.mp4 under ~/.openclaw/workspace/tibetanProc/.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

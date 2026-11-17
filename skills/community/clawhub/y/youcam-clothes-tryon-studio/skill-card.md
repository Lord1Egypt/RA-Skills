## Description:

Creates AI virtual try-on images from a person's photo, with optional background changes and short motion videos.

This skill is ready for commercial/non-commercial use.

## Publisher:

[youcam-api](https://clawhub.ai/user/youcam-api)

### License/Terms of Use:

MIT-0

## Use Case:

External users can preview how a garment may look on them by applying it to a personal photo, optionally changing the scene or generating a short motion clip.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Personal photos and garment images are sent to YouCam/Perfect Corp for processing.

Mitigation: Use photos you are comfortable sharing and review the provider's privacy terms.

Risk: Generation steps consume credits, and video is billed per second.

Mitigation: Show the cost of each selected step and get the user's approval before generating.

Risk: An exposed API key or outdated dependencies could compromise use of the service.

Mitigation: Protect the API key and use reviewed, patched dependencies.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/youcam-api/skills/youcam-clothes-tryon-studio)
- [Clothes virtual try-on API](https://docs.perfectcorp.com/reference/ai_clothes.md)
- [Photo background change API](https://docs.perfectcorp.com/reference/ai_photo_background_change.md)
- [Video generator API](https://docs.perfectcorp.com/reference/ai_video_generator.md)
- [Clothes Try-On Studio flow and output guide](references/guide.md)

## Skill Output:

**Output Type(s):** [Image and video URLs, Usage guidance]

**Output Format:** [Markdown response with result URLs and a brief summary of the selected steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Return result URLs unchanged and include the AI-generated reference-only fit disclaimer.]

## Skill Version(s):

1.1.2 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

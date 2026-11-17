## Description:

Recommend and preview makeup looks based on the user's face shape and skin tone using YouCam (Perfect Corp) AI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[youcam-api](https://clawhub.ai/user/youcam-api)

### License/Terms of Use:

MIT-0

## Use Case:

External users can get makeup suggestions informed by a selfie's face shape and skin tone, then preview a selected full look or custom makeup effects.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A selfie is sent to YouCam/Perfect Corp for analysis and makeup preview.

Mitigation: Use only photos you are comfortable sending to the provider, and review its privacy and retention terms before uploading.

Risk: Makeup analysis and preview options use API credits.

Mitigation: Show the available option costs and get the user's choice before running the selected preview.

Risk: The API key and dependency environment need protection.

Mitigation: Protect the dedicated API key and use an isolated environment with reviewed dependency versions.

## Reference(s):

- [Beauty Advisor recommendation guide](references/guide.md)
- [Perfect Corp face analyzer API reference](https://docs.perfectcorp.com/reference/ai_face_analyzer.md)
- [Perfect Corp skin tone analysis API reference](https://docs.perfectcorp.com/reference/ai_skin_tone_analysis.md)
- [Perfect Corp makeup virtual try-on API reference](https://docs.perfectcorp.com/reference/makeup_vto.md)
- [Perfect Corp look virtual try-on API reference](https://docs.perfectcorp.com/reference/ai_look_vto.md)
- [YouCam Beauty Advisor on ClawHub](https://clawhub.ai/youcam-api/skills/youcam-beauty-advisor)

## Skill Output:

**Output Type(s):** [Guidance, Image]

**Output Format:** [Makeup recommendation text and virtual try-on image URL]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The user chooses a preview option after seeing its credit cost; return the result image URL exactly as provided and include the AI-generated preview note.]

## Skill Version(s):

1.1.2 (source: frontmatter, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

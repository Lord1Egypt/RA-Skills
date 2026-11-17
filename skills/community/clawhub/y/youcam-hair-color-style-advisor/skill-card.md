## Description:

Analyzes face shape and skin tone to recommend hairstyles and hair colors, then creates a YouCam AI try-on preview.

This skill is ready for commercial/non-commercial use.

## Publisher:

[youcam-api](https://clawhub.ai/user/youcam-api)

### License/Terms of Use:

MIT-0

## Use Case:

People seeking hairstyle or hair color ideas can use the skill to get guidance based on face shape and skin tone, then preview a selected style or color with a generated try-on image.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selfies are sent to Perfect Corp/YouCam for analysis or generation.

Mitigation: Use photos you are comfortable sharing and review the service's privacy and retention terms before use.

Risk: Selected try-on operations may consume credits.

Mitigation: Choose the requested operation and review its credit cost before running it.

Risk: The API key and image URLs require care.

Mitigation: Protect the API key and use trusted image URLs.

Risk: Live service behavior and resolved dependency versions were not verified.

Mitigation: Use reviewed, locked dependency versions.

## Reference(s):

- [Recommendation guide](references/guide.md)
- [Perfect Corp facial attributes reference](https://docs.perfectcorp.com/reference/ai_face_analyzer.md)
- [Perfect Corp skin tone reference](https://docs.perfectcorp.com/reference/ai_skin_tone_analysis.md)
- [Perfect Corp hairstyle try-on reference](https://docs.perfectcorp.com/reference/ai_hairstyle.md)
- [Perfect Corp hair color reference](https://docs.perfectcorp.com/reference/ai_hair_color.md)

## Skill Output:

**Output Type(s):** [Text, Image URL]

**Output Format:** [Recommendation text with hairstyle and color guidance, plus a try-on image URL]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes AI preview limitations and a note that real results may vary.]

## Skill Version(s):

1.1.2 (source: SKILL.md frontmatter and server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

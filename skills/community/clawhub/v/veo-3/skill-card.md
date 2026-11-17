## Description:

Veo 3 helps agents write brand-aware Google Veo prompts for short social videos, image-to-video animations, and audio-rich vertical clips.

This skill is ready for commercial/non-commercial use.

## Publisher:

[social-media-skills](https://clawhub.ai/user/social-media-skills)

### License/Terms of Use:

MIT-0

## Use Case:

Social media, marketing, and creative operators use this skill to decide when Veo fits a video job and to draft concise, brand-aware prompts for short vertical clips, product motion, hook visuals, ad scenes, spokesperson-style clips, and still-image animation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: AI-generated video may be mistaken for real footage or may involve real identifiable people or copyrighted IP.

Mitigation: Disclose AI-generated video, respect SynthID watermarking, and use original subjects or scenes instead of real people or protected IP.

Risk: Generated video or audio can contain artifacts, incorrect words, weak lip sync, or inconsistent motion.

Mitigation: Review every clip before publishing and treat generated audio as a draft or guide track for branded work.

Risk: Video generation can be asynchronous, costly, and consume credits on off-prompt generations.

Mitigation: Iterate with lower-cost Fast or low-resolution generations before finalizing only the selected clip at higher quality.

Risk: The skill can point an agent toward separate Veo generation and publishing workflows outside the reviewed prompt guidance artifact.

Mitigation: Review and authorize those separate workflows before executing generation, upload, or publishing steps.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/social-media-skills/skills/veo-3)
- [When & How to Prompt Veo](references/when-and-how-to-prompt.md)
- [Audio & Camera](references/audio-and-camera.md)
- [Inputs, Length & Recipes](references/inputs-length-and-recipes.md)
- [Examples](references/examples.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or plain text prompt guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces prompt drafts and decision guidance; it does not generate video itself.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

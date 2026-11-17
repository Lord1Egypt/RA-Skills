## Description:

Generates Chinese 2.35:1 WeChat public-account cover prompts for the "网瘾中年" brand using a three-round question flow, brand robot IP constraints, engineering-blue visual rules, and NVH frequency-response imagery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shun1989](https://clawhub.ai/user/shun1989)

### License/Terms of Use:

MIT

## Use Case:

External content creators and agent users use this skill to turn article content into ready-to-use Chinese image-generation prompts for consistent 2.35:1 WeChat cover art. The workflow is designed for the "网瘾中年" visual identity and supports prompt-only use, with optional direct image generation through ARK when intentionally configured.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional ARK image-generation script can use local API credentials and upload prompts or reference images to an image provider.

Mitigation: Use the prompt-only workflow unless ARK image generation is intentionally configured; keep local credential files private and only pass reference images approved for upload.

Risk: Custom ARK endpoint settings can route image-generation requests away from the documented provider endpoint.

Mitigation: Avoid custom ARK_BASE_URL values unless the endpoint has been reviewed and approved for the intended release environment.

## Reference(s):

- [README](README.md)
- [Skill Instructions](SKILL.md)
- [Brand Visual Constraints](references/vi-constraints.md)
- [Prompt Examples](references/examples.md)
- [Dark Engineering Style Template](references/style-01-dark-engineering.md)
- [Minimal Dark Blue Style Template](references/style-02-minimal-dark-blue.md)
- [Dashboard UI Style Template](references/style-03-dashboard-ui.md)
- [Waveform Comparison Style Template](references/style-04-waveform-comparison.md)
- [Robot Side Space Style Template](references/style-05-robot-side-space.md)
- [Robot Back View Style Template](references/style-06-robot-back-view.md)
- [Prop Closeup Style Template](references/style-07-prop-closeup.md)
- [Robot Front Guide Style Template](references/style-08-robot-front-guide.md)
- [Info Collage Style Template](references/style-09-info-collage.md)
- [Industrial Photo Style Template](references/style-10-industrial-photo.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown text containing a Chinese image-generation prompt and follow-up usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prompts are constrained to 2.35:1 horizontal cover composition and include brand VI, robot IP, title-text, and reference-image guidance.]

## Skill Version(s):

1.0.0 (source: evidence.release.version and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

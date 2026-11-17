## Description:

Generate AI videos from text prompts or images with Seedance 2.0 on SkillBoss for short ads, product demos, launch clips, and social videos.

This skill is ready for commercial/non-commercial use.

## Publisher:

[quincygunter](https://clawhub.ai/user/quincygunter)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to ask an agent to prepare SkillBoss Seedance 2.0 video generation requests for short marketing, product, launch, and social clips. It supports text-to-video, image-to-video, and reference-image-guided workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, generation settings, and reference image URLs are sent to SkillBoss for processing.

Mitigation: Avoid confidential prompts and private or internal image URLs unless SkillBoss processing is intended under the user's billing and data-handling terms.

Risk: Generated video requests may fail because of provider or API errors.

Mitigation: Report the API error clearly and retry only with the smallest useful change to prompt, duration, aspect ratio, or reference images.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/quincygunter/skills/quincy-seedance-video)
- [SkillBoss Seedance Video](https://skillboss.co/skills/seedance-video)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return a generated video URL or task payload, plus a summary of prompt, duration, and aspect ratio.]

## Skill Version(s):

1.0.0 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

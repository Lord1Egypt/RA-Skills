## Description:

Generates AI videos and images through the Seedance/AI Director service, with support for text-to-video, image-to-video, text-to-image, credit checks, task status checks, and work listing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenzhigao61](https://clawhub.ai/user/chenzhigao61)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to submit Seedance video or image generation jobs, query credit balance, check asynchronous generation status, and review generated works from an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, public image URLs, task metadata, and the configured API key are sent to the Seedance/AI Director external service.

Mitigation: Install only when the user intends to use and trusts seedance25movie.coze.site, and configure only the AI_DIRECTOR_API_KEY secret required by the skill.

Risk: Video and image generation jobs can consume service credits.

Mitigation: Confirm before submitting paid generation jobs and use the included credit query workflow to check available balance.

Risk: Video generation is asynchronous, so users may mistake submission for completion.

Mitigation: Poll task status after submission at the documented interval and present completed, failed, or pending status clearly.

## Reference(s):

- [AI Director Platform](https://seedance25movie.coze.site)
- [ClawHub Skill Page](https://clawhub.ai/chenzhigao61/skills/seedance2-5skill)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON command results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generation jobs are asynchronous and may require status polling; video and image generation can consume service credits.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

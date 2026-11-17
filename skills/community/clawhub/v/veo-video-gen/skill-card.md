## Description:

Generates videos through Pixwith API's Veo 3.1 model for text-to-video and image-to-video workflows with Fast and Pro tiers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tate-kt](https://clawhub.ai/user/tate-kt)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to guide an agent through Pixwith video generation tasks, including credit checks, text-to-video creation, image-to-video uploads, task polling, and returning generated video URLs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Shell-command templates could mishandle crafted prompts or image URLs and run unintended local commands.

Mitigation: Review generated commands before execution and prefer implementations that build request bodies with a JSON serializer instead of substituting user text into shell commands.

Risk: The skill sends prompts, image URLs, uploaded images, and the Pixwith API key to Pixwith-related services.

Mitigation: Use only non-sensitive prompts and images, and provide the API key through the runtime's standard secret or environment-variable mechanism.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/tate-kt/skills/veo-video-gen)
- [Pixwith Homepage](https://pixwith.ai)
- [Pixwith API Dashboard](https://pixwith.ai/api)
- [Pixwith Pricing](https://pixwith.ai/pricing)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell command examples and API result URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return Pixwith task IDs, generated video URLs, and setup guidance for PIXWITH_API_KEY.]

## Skill Version(s):

1.0.7 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

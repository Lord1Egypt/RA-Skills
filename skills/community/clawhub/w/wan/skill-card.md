## Description:

Generate images using Alibaba DashScope wan2.6-t2i model, download to Desktop, and upload to catbox.moe image hosting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lxyd-ai](https://clawhub.ai/user/lxyd-ai)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to generate images through Alibaba DashScope Wan, save the generated file locally, and publish a shareable catbox.moe URL.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A plausible DashScope API key appears in the skill artifact.

Mitigation: Do not use the embedded key; provide a fresh credential through a secure environment variable and revoke the exposed key if it belongs to you.

Risk: Generated images are uploaded to catbox.moe as public URLs.

Mitigation: Use the workflow only for prompts and images that are acceptable to send to Alibaba DashScope and publish publicly.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and environment variable guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create a local image file on the user's Desktop and return a public catbox.moe image URL.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

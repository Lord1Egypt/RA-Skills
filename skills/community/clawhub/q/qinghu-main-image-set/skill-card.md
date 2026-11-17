## Description:

Generates platform-tailored e-commerce main-image and carousel sets from product photos using Qinghu AI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Merchants and creative teams use this skill to turn a product photo into platform-tailored main images and carousel sets, optionally incorporating promotional copy.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Product images and prompt text are sent to the Qinghu AI service.

Mitigation: Obtain approval before submitting sensitive product material and disclose the external upload to users.

Risk: The skill requires a QHKIT token.

Mitigation: Keep the token secret, avoid including it in shared commands or logs, and use the correct Qinghu account environment.

Risk: Installing npm tooling or changing the shell startup PATH can affect the local environment.

Mitigation: Prefer preinstalled or version-pinned qhkit, verify downloads, and avoid persistent PATH changes unless necessary.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/qinghu-main-image-set)
- [qhkit package](https://www.npmjs.com/package/@iqinghu/qhkit)
- [Qinghu AI API keys](https://www.iqinghu.com/workbench/dashboard/api-keys?urlCode=1788417429126)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with generated image URLs and credit usage]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Image generation may take up to approximately 14 minutes.]

## Skill Version(s):

0.1.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

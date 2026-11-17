## Description:

Guides an agent through Qinghu AI's image-upscaling workflow to enlarge and clarify a supplied image while aiming to preserve its original content and style.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

External users and creators use the skill to upscale a single authorized product, portrait, landscape, or older image for clearer viewing or higher-resolution printing. The agent estimates credits before submitting the image and returns a link to the processed result.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected images are uploaded to Qinghu's third-party service.

Mitigation: Send only images the user is comfortable sharing and has permission to process.

Risk: Processing may require a qhkit API token, a subscription, and paid credits.

Mitigation: Keep the token private, obtain the current credit estimate, and confirm with the user before submission.

Risk: Installing or upgrading qhkit and Node can change the local environment.

Mitigation: Prefer a preinstalled or pinned qhkit version and review any global installation first.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/qinghu-image-upscale-detail)
- [qhkit package](https://www.npmjs.com/package/@iqinghu/qhkit)
- [Qinghu API keys](https://www.iqinghu.com/workbench/dashboard/api-keys?urlCode=1788417429126)

## Skill Output:

**Output Type(s):** [Markdown, Image links, Guidance]

**Output Format:** [Markdown text with a processed-image link and final credit usage]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Processes one image per request; estimate and confirm credit usage before submission.]

## Skill Version(s):

0.1.6 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

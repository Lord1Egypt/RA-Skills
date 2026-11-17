## Description:

Helps remove watermarks, logos, or text from an image and restore the obscured background using Qinghu AI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

People preparing authorized product images or social media visuals use this skill to remove watermarks or, optionally, both watermarks and image text from one image at a time.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The target image is uploaded to an external Qinghu service.

Mitigation: Use only images you are comfortable sending to Qinghu and review service terms before use.

Risk: The service requires an API token and installing Node/npm tooling.

Mitigation: Protect the token and review the package and installation source before installation.

Risk: Processing may consume credits, with the final charge differing from the estimate.

Mitigation: Review the current estimate and obtain confirmation before submitting an image.

Risk: Removing watermarks from third-party material can infringe others' rights.

Mitigation: Only process images you own or are authorized to modify.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/qinghu-image-watermark-remove)
- [Qinghu qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)
- [Qinghu API keys](https://www.iqinghu.com/workbench/dashboard/api-keys?urlCode=1788417429126)

## Skill Output:

**Output Type(s):** [Text, Image URLs, Shell commands]

**Output Format:** [Markdown with a processed-image link and usage details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Processes one image at a time; output resolution may differ from the source.]

## Skill Version(s):

0.1.6 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

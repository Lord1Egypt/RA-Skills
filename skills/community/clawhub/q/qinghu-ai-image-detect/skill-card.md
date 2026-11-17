## Description:

Checks whether an image was AI-generated and reports a 0–1 confidence score using Qinghu AI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

People reviewing images use this skill to check whether a public image URL or local image may be AI-generated and receive a confidence score.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Image contents or public image URLs are sent to Qinghu, and checks consume paid credits.

Mitigation: Confirm the image can be shared and obtain user approval for the quoted credits before calling the service.

Risk: Setup instructions may install or update tooling globally and change the user's PATH.

Mitigation: Review setup changes first; prefer an existing, pinned qhkit installation and avoid automatic global installs or PATH edits.

Risk: Using the wrong regional account or endpoint can change credential settings or prevent authentication.

Mitigation: Confirm whether the user has a CN or international account before configuring tokens or uploading images.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/qinghu-ai-image-detect)
- [Qinghu qhkit package](https://www.npmjs.com/package/@iqinghu/qhkit)
- [Qinghu API keys](https://www.iqinghu.com/workbench/dashboard/api-keys?urlCode=1788417429126)

## Skill Output:

**Output Type(s):** [Text, Markdown]

**Output Format:** [Markdown response with an AI-image confidence score]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports Qinghu credits used for paid calls.]

## Skill Version(s):

0.1.2 (source: ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

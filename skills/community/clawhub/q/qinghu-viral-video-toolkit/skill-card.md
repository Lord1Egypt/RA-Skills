## Description:

Helps sellers analyze short-video links, adapt viral-video scripts for their products, generate similar marketing videos, and extract audio.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Sellers and content creators use this skill to turn a shared short-video link into an adapted product-video script and generated marketing video, or to extract the video's audio.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An unpinned third-party CLI may be installed or upgraded while the skill runs.

Mitigation: Review the qhkit package, pin an approved version, and obtain approval before installation, upgrades, or PATH changes.

Risk: Video links, selected local media, and a Qinghu API token may be sent to an external service.

Mitigation: Confirm the destination and obtain consent before submitting links, commercial assets, or credentials; limit the token's exposure.

Risk: Extracting or reusing third-party video and audio can infringe content rights.

Mitigation: Check rights before reuse, adapt scripts instead of copying original dialogue, and clear music rights for commercial use.

## Reference(s):

- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)
- [Qinghu API keys](https://www.iqinghu.com/workbench/dashboard/api-keys?urlCode=1788417429126)
- [ClawHub skill release](https://clawhub.ai/autoagc/skills/qinghu-viral-video-toolkit)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Media links]

**Output Format:** [Markdown with script text, commands, and generated media links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Audio extraction may produce a local MP3 file; video generation returns a task ID before the finished media link.]

## Skill Version(s):

0.1.3 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

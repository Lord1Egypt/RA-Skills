## Description:

Generates a shareable short link for a WeChat Channels video using its object ID.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Users and agents generating a share link from an existing WeChat Channels video object ID can use this skill with the Qinghu service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing or updating the qhkit dependency may run unpinned package code.

Mitigation: Prefer a preinstalled or isolated qhkit setup and avoid unpinned installs where possible.

Risk: The qhkit token could be exposed in shared logs or shell history.

Mitigation: Handle the token as a secret; do not paste it into shared logs or persistent shell history.

Risk: Generating share links uses paid Qinghu credits, and failed calls may still incur charges.

Mitigation: Check the available price estimate and obtain user approval before paid calls; report actual credits consumed.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/autoagc/skills/qinghu-shipinhao-share-link)
- [Qinghu qhkit package](https://www.npmjs.com/package/@iqinghu/qhkit)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Share URL with a brief text response]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports Qinghu credits consumed when a paid call is made.]

## Skill Version(s):

0.1.2 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

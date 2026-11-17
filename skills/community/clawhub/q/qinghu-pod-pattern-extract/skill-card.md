## Description:

一键提取图片中的印花图案，生成高清、平铺、可复用的图案素材，适用于 POD 定制及服装设计。

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Designers and POD sellers use this skill to turn clothing or product photos into reusable, flat pattern design drafts and receive guidance for preparing and running the image-generation workflow.

### Deployment Geography for Use:

China (mainland; the documented workflow uses Qinghu AI's domestic service)

## Known Risks and Mitigations:

Risk: Images are uploaded to Qinghu AI for processing, and generation may consume service credits.

Mitigation: Upload only images approved for that service and check expected charges before processing.

Risk: The external qhkit CLI implementation is outside this review, and installation or updates can affect the local setup.

Mitigation: Select a reviewed CLI version and check the existing qhkit configuration before allowing installation, updates, or replacement.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/qinghu-pod-pattern-extract)
- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)
- [Qinghu AI POD materials workspace](https://www.iqinghu.com)

## Skill Output:

**Output Type(s):** [Image files, Text, Markdown, Shell commands, Configuration instructions]

**Output Format:** [Generated white-background raster design drafts and concise Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated pattern details may vary; the workflow produces raster drafts, not vector artwork or transparent layers.]

## Skill Version(s):

0.1.3 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

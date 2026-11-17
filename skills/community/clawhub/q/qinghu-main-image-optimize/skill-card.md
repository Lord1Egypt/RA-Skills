## Description:

AI 自动优化商品主图的构图、光影、质感及细节，提升商品吸引力与点击率。

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Chinese-speaking ecommerce sellers and their agents use this skill to improve product main images, refine lighting and texture, or generate a coordinated image set. It guides image generation through the Qinghu qhkit command-line tool.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: Upgrade commands returned by the software could install an unreviewed qhkit version.

Mitigation: Review upgrade commands before running them and restrict upgrades to a reviewed version; avoid administrator privileges where possible.

Risk: Image generation uploads images to Qinghu and can consume account credits.

Mitigation: Tell users when source images will be uploaded and check the applicable credit estimate before generating when cost matters.

Risk: The supplied artifact contains instructions only, so the external CLI runtime behavior is unverified.

Mitigation: Review the qhkit version and its behavior before use, and report command errors without repeating failed requests.

## Reference(s):

- [@iqinghu/qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)
- [ClawHub skill release](https://clawhub.ai/autoagc/skills/qinghu-main-image-optimize)

## Skill Output:

**Output Type(s):** [Images, Shell commands, Guidance]

**Output Format:** [Generated image outputs with Markdown guidance and inline JSON command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Image generation may upload source images to Qinghu and consume account credits; generated details can differ from the source.]

## Skill Version(s):

0.1.3 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

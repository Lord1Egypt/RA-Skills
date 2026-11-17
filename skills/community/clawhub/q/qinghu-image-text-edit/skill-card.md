## Description:

根据指令识别并替换电商图片中的文字，如标题、价格、卖点和促销信息。

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

电商运营者可用它按指令更新商品图片中的标题、价格、卖点和促销文案，并在生成后检查文字与商品细节。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Using the image workflow uploads source images to Qinghu and may consume credits.

Mitigation: Use images you are comfortable uploading and check the expected credit cost before generation.

Risk: Generated redraws can introduce incorrect text or alter logos and product details.

Mitigation: Inspect spelling, prices, logos, and product structure before using the result; regenerate with a clearer instruction if needed.

Risk: CLI upgrades can change behavior, and this review did not cover downloaded CLI code or the remote service.

Mitigation: Prefer a reviewed, pinned CLI version and inspect upgrade commands before running them with elevated permissions.

## Reference(s):

- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)
- [ClawHub skill release](https://clawhub.ai/autoagc/skills/qinghu-image-text-edit)

## Skill Output:

**Output Type(s):** [Images, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Generated image files, JSON-formatted CLI arguments, and Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated redraws may change details; visually inspect text, logos, and product structure.]

## Skill Version(s):

0.1.3 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

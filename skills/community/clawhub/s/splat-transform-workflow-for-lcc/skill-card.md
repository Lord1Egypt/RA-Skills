## Description:

Guides agents through converting XGRIDS/其域 `.lcc` or PLY Gaussian splat scenes into SuperSplat assets, including streamed LOD, SOG, voxel collision files, settings merges, local viewer mounting, and bilingual workflow explanations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shuang-su](https://clawhub.ai/user/shuang-su)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to convert LCC or PLY Gaussian splat scenes into deployable SuperSplat viewer assets. It helps choose precision-preserving conversion inputs, rotation defaults, SOG or streamed LOD outputs, voxel collision generation, settings merges, and local viewer mounting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Example conversion and mount commands can create or overwrite outputs under the selected output directory and SuperSplat viewer public directory.

Mitigation: Review all input, output, and viewer public paths before running commands, and use a disposable output directory when testing a new scene.

Risk: Incorrect source selection or rotation settings can produce visually misaligned SuperSplat assets or voxel collision data.

Mitigation: Follow the documented PLY, LCC, SOG, streamed LOD, and voxel defaults, then inspect the generated viewer route before publishing converted assets.

## Reference(s):


## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, code]

**Output Format:** [Markdown with inline bash code blocks and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Bilingual English and Chinese guidance; commands may create or overwrite conversion outputs in selected output and viewer public directories.]

## Skill Version(s):

0.2.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

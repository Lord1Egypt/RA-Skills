## Description:

Uses SAM (Segment Anything Model) to remove image backgrounds and extract foreground subjects as transparent PNGs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scikkk](https://clawhub.ai/user/scikkk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, designers, and content operations teams use this skill to run SAM on local image files for background removal, subject cutouts, foreground extraction, and multi-element segmentation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-run execution can install mutable remote code.

Mitigation: Use an isolated Python environment and preinstall a pinned, reviewed segment_anything dependency before running the skill.

Risk: Model checkpoints can be downloaded as large unverified files into a local cache.

Mitigation: Use locally verified SAM checkpoints and pass them with the --checkpoint option.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/scikkk/skills/sam)
- [Segment Anything dependency](https://github.com/facebookresearch/segment-anything.git)
- [SAM ViT-B checkpoint](https://dl.fbaipublicfiles.com/segment_anything/sam_vit_b_01ec64.pth)
- [SAM ViT-L checkpoint](https://dl.fbaipublicfiles.com/segment_anything/sam_vit_l_0b3195.pth)
- [SAM ViT-H checkpoint](https://dl.fbaipublicfiles.com/segment_anything/sam_vit_h_4b8939.pth)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance with bash commands; runtime output is transparent PNG image files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Single-subject mode writes one PNG file; all-elements mode writes one PNG per detected element.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

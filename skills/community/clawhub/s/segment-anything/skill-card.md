## Description:

Uses Meta's Segment Anything Model (SAM) to remove image backgrounds and extract foreground subjects as transparent PNG files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scikkk](https://clawhub.ai/user/scikkk)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and image workflow operators use this skill to segment images, remove backgrounds, and extract centered or point-selected foreground subjects into transparent PNG files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can change the Python environment by automatically installing mutable remote code during use.

Mitigation: Prepare dependencies from pinned, trusted versions before running the skill.

Risk: The skill can download large unverified SAM model checkpoint files from the network.

Mitigation: Prefer a local checkpoint whose source you trust and pass it with the checkpoint option.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/scikkk/skills/segment-anything)
- [Segment Anything repository](https://github.com/facebookresearch/segment-anything.git)
- [SAM ViT-B checkpoint](https://dl.fbaipublicfiles.com/segment_anything/sam_vit_b_01ec64.pth)
- [SAM ViT-L checkpoint](https://dl.fbaipublicfiles.com/segment_anything/sam_vit_l_0b3195.pth)
- [SAM ViT-H checkpoint](https://dl.fbaipublicfiles.com/segment_anything/sam_vit_h_4b8939.pth)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Guidance]

**Output Format:** [Transparent PNG image files with command-line status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Single-target mode writes one PNG; all-elements mode writes one transparent PNG per detected element.]

## Skill Version(s):

1.0.0 (source: server release evidence, released 2026-03-14)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

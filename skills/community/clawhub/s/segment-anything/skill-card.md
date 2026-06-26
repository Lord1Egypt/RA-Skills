## Description: <br>
Uses Meta's Segment Anything Model (SAM) to remove image backgrounds and extract foreground subjects as transparent PNG files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[scikkk](https://clawhub.ai/user/scikkk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content creators use this skill to run a local CLI workflow that segments images, removes backgrounds, and exports transparent PNG assets from centered subjects or multiple detected elements. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: First run may install segment_anything from GitHub at runtime. <br>
Mitigation: Preinstall a reviewed segment_anything version in controlled environments before using the skill. <br>
Risk: The skill may download large SAM model checkpoints and cache them locally. <br>
Mitigation: Use a verified local --checkpoint file or pre-stage approved checkpoints. <br>
Risk: Automatic segmentation can select the wrong subject, especially when the foreground is not centered. <br>
Mitigation: Provide explicit --points hints and review generated PNG outputs before downstream use. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/scikkk/segment-anything) <br>
- [Segment Anything repository](https://github.com/facebookresearch/segment-anything.git) <br>
- [SAM ViT-B checkpoint](https://dl.fbaipublicfiles.com/segment_anything/sam_vit_b_01ec64.pth) <br>
- [SAM ViT-L checkpoint](https://dl.fbaipublicfiles.com/segment_anything/sam_vit_l_0b3195.pth) <br>
- [SAM ViT-H checkpoint](https://dl.fbaipublicfiles.com/segment_anything/sam_vit_h_4b8939.pth) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Files] <br>
**Output Format:** [Markdown guidance with CLI commands; runtime output is transparent PNG image files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write one PNG file or multiple element PNG files; first run may install a dependency and download SAM checkpoints.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

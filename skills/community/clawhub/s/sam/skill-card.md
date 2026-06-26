## Description: <br>
Use SAM (Segment Anything Model) to remove image backgrounds and extract foreground subjects as transparent PNGs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[scikkk](https://clawhub.ai/user/scikkk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to remove image backgrounds, cut out foreground subjects, or extract multiple segmented elements from local images as transparent PNG files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: First use can install an unpinned package from the Segment Anything GitHub repository. <br>
Mitigation: Preinstall and pin dependencies in a controlled environment before using the skill. <br>
Risk: First use can download large SAM checkpoint files to ~/.cache/sam. <br>
Mitigation: Use a local checkpoint path or preseed the cache in environments with controlled network and storage policies. <br>
Risk: Segmentation results may be incorrect when hint points, model size, or grid settings do not match the image subject. <br>
Mitigation: Review generated PNG outputs before downstream use and adjust hint points, model size, or thresholds as needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/scikkk/sam) <br>
- [Segment Anything repository](https://github.com/facebookresearch/segment-anything.git) <br>
- [SAM ViT-B checkpoint](https://dl.fbaipublicfiles.com/segment_anything/sam_vit_b_01ec64.pth) <br>
- [SAM ViT-L checkpoint](https://dl.fbaipublicfiles.com/segment_anything/sam_vit_l_0b3195.pth) <br>
- [SAM ViT-H checkpoint](https://dl.fbaipublicfiles.com/segment_anything/sam_vit_h_4b8939.pth) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Files] <br>
**Output Format:** [Markdown guidance with command examples; runtime output is transparent PNG files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and image-processing dependencies. Supports model size, local checkpoint path, foreground hint points, all-elements grid mode, IoU threshold, and minimum mask area options.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

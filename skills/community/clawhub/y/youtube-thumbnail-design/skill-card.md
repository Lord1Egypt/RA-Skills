## Description: <br>
YouTube thumbnail design guidance with dimensions, contrast rules, mobile preview checks, safe zones, text placement, face expression tips, A/B testing, and example image-generation commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[okaris](https://clawhub.ai/user/okaris) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Creators, marketers, and agent users use this skill to plan and generate YouTube thumbnail concepts that are readable on mobile, use high-contrast composition, and support click-through optimization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a third-party image-generation CLI and provider workflow. <br>
Mitigation: Install only if inference.sh is trusted; review the installer or use the manual checksum-verification path before running it. <br>
Risk: Prompts, generated-image requests, or image inputs may be sent to external providers. <br>
Mitigation: Avoid sending confidential images, private details, or sensitive prompt content unless the service handling is acceptable. <br>
Risk: Thumbnail guidance can be used to create misleading video previews. <br>
Mitigation: Keep thumbnails aligned with the actual video content and review generated assets before publication. <br>


## Reference(s): <br>
- [inference.sh](https://inference.sh) <br>
- [inference.sh CLI installer](https://cli.inference.sh) <br>
- [inference.sh CLI checksums](https://dist.inference.sh/cli/checksums.txt) <br>
- [ClawHub skill page](https://clawhub.ai/okaris/youtube-thumbnail-design) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline bash commands and JSON input examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes thumbnail specifications, prompt templates, checklist items, and A/B testing suggestions.] <br>

## Skill Version(s): <br>
0.1.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

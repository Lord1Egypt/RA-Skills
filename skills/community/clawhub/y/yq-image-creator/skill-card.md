## Description: <br>
Curated image generation assistant covering 17 styles across 4 categories: character figures, scenes, products, and style transforms. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tianheihei002](https://clawhub.ai/user/tianheihei002) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and creators use this skill to turn text prompts or reference images into stylized 3D image assets across character, scene, product, and style-transform categories. It asks only for required missing inputs, presents style choices through an interactive form when needed, and delivers generated image paths directly. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Reference images may be analyzed by configured image tools during generation workflows. <br>
Mitigation: Use only reference images the user is permitted to process and avoid uploading sensitive images unless the deployment is approved for that data. <br>
Risk: The skill may use web search to supplement public city, landmark, or brand details for prompts. <br>
Mitigation: Review generated prompts and image outputs when brand, landmark, or factual visual details matter. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/tianheihei002/yq-image-creator) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown-like chat responses with deliver_assets blocks containing generated image paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May request missing inputs through genui-form-wizard; reference images may be analyzed before generation.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

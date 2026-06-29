## Description: <br>
Generates cross-border e-commerce product images, including white-background shots, scene images, cutout-style product photos, multi-angle sets, and platform-sized outputs through Yufluent cloud image generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[metahuan](https://clawhub.ai/user/metahuan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External sellers, marketers, and agents use this skill to create product listing and marketing images for e-commerce platforms from product descriptions and optional source photos. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Product prompts, source images, and the Yufluent API key are sent to the configured service. <br>
Mitigation: Use approved product imagery, avoid confidential unreleased photos unless authorized, and strip image metadata before upload when appropriate. <br>
Risk: Generated product images can misrepresent product details or fail marketplace image rules. <br>
Mitigation: Review generated images for product accuracy, rights, prohibited content, and platform-specific listing requirements before publication. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/metahuan/yufluentcn-ecommerce-imaging) <br>
- [Yufluent homepage](https://claw.changzhiai.com) <br>
- [Platform size reference](artifact/references/platform-sizes.md) <br>
- [Prompt template reference](artifact/references/prompt-templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Image URLs] <br>
**Output Format:** [CLI text output by default, or structured JSON when requested, containing generated image results and run metadata.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return one or more image results depending on scene and angle settings; source images can be provided as URLs or encoded local image data.] <br>

## Skill Version(s): <br>
1.1.2 (source: server release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

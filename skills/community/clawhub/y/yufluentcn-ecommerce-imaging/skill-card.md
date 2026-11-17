## Description:

Yufluent Ecommerce Imaging generates white-background, lifestyle, cutout, multi-angle, and platform-sized ecommerce product images through the Yufluent cloud image-generation service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[metahuan](https://clawhub.ai/user/metahuan)

### License/Terms of Use:

MIT

## Use Case:

External ecommerce sellers, marketplace operators, and agents use this skill to create product listing imagery for Amazon, Shopify, TikTok, Instagram, Facebook, Pinterest, and related storefront workflows. It supports white-background product shots, scene images, product photo background replacement, multi-angle packs, brand-tone variants, and platform-specific image sizing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local source images can be encoded and uploaded for remote processing.

Mitigation: Use only non-confidential product images that are approved for upload, and verify each --source-image path before running the skill.

Risk: API tokens may be sent to a configurable TOKENAPI_BASE_URL endpoint.

Mitigation: Keep TOKENAPI_KEY secret, avoid custom TOKENAPI_BASE_URL values unless the endpoint is trusted, and prefer HTTPS production endpoints.

Risk: Generated ecommerce images may misrepresent product appearance or platform compliance.

Mitigation: Review generated images for product fidelity, marketplace rules, prohibited claims, and brand/IP compliance before publication.

## Reference(s):

- [Platform Size Reference](references/platform-sizes.md)
- [Prompt Template Reference](references/prompt-templates.md)
- [Yufluent Homepage](https://claw.changzhiai.com)
- [OpenClaw Integration](https://claw.changzhiai.com/app/openclaw)
- [ClawHub Skill Page](https://clawhub.ai/metahuan/skills/yufluentcn-ecommerce-imaging)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, image URLs]

**Output Format:** [Markdown or JSON with generated image results, run metadata, and command-oriented guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires TOKENAPI_KEY and may upload approved source images to the configured Yufluent API endpoint for remote processing.]

## Skill Version(s):

1.1.2 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

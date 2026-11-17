## Description:

Generates ecommerce product image workflows with selectable visual styles, multilingual text overlays, storyboard planning, batch image generation, downloads, and optional Feishu delivery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[davidunderwood7970](https://clawhub.ai/user/davidunderwood7970)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, designers, and ecommerce operators use this skill to analyze uploaded product photos, choose a visual direction and language, plan a product-image sequence, generate image assets, package results, and optionally send them through Feishu.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release evidence reports embedded API keys and Feishu app secrets.

Mitigation: Remove shipped credentials, rotate exposed secrets, and require users to provide their own credentials through environment variables or a local secret store.

Risk: Uploaded product photos and generated assets may be sent to Grsai or Feishu without clear user disclosure.

Mitigation: Make remote uploads and Feishu delivery opt-in, disclose destination services before transfer, and avoid using private product assets until users confirm consent.

Risk: Feishu sending behavior includes a default recipient, which can route generated images to an unintended account.

Mitigation: Require an explicit recipient and tenant configuration for every Feishu send operation.

Risk: Preview HTML and downloaded/generated files may be unsafe to open or share if user-controlled values are not escaped or downloads are not checked.

Mitigation: Escape values written into preview HTML and validate downloaded file type, size, and destination before opening, packaging, or sharing generated outputs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/davidunderwood7970/skills/yu-product-image-generator)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Image files, HTML, ZIP archives, Guidance]

**Output Format:** [Conversational text and generated files, including PNG images, HTML preview pages, ZIP archives, JSON generation records, and optional Feishu messages.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports 3 visual style options, 12 language modes including no text, storyboard planning, and batch generation.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter reports 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Download product images from any public Shopify store without API access, including full backups, collection-only exports, single-product downloads, optional WebP conversion, and smart renaming.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lvsao](https://clawhub.ai/user/lvsao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and ecommerce teams use this skill to preview and download public Shopify product images into local folders for backup, collection export, or single-product retrieval workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional WebP conversion can automatically install the unpinned sharp npm package and modify the skill directory.

Mitigation: Prefer the non-WebP workflow, or install and pin sharp in a controlled environment before enabling WebP conversion.

Risk: The downloader fetches data from public stores and image URLs supplied by the target site.

Mitigation: Run it only against stores you trust and from an environment without access to sensitive internal network services.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lvsao/skills/shopify-product-images-downloader)
- [Project Homepage](https://github.com/lvsao/shopify-skill-hub)

## Skill Output:

**Output Type(s):** [guidance, shell commands, files]

**Output Format:** [Markdown guidance with shell commands and downloaded image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes images and a download summary under the user-selected output directory.]

## Skill Version(s):

2.0.0 (source: server release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

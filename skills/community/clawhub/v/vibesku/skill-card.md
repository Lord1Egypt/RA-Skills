## Description:

VibeSKU is a CLI skill for creating e-commerce product visuals, marketplace listing copy, refinements, exports, batch runs, credit checks, and CLI configuration from product SKU photos.

This skill is ready for commercial/non-commercial use.

## Publisher:

[visoar](https://clawhub.ai/user/visoar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and e-commerce teams use this skill to drive the VibeSKU CLI for product image generation, detail-page visual sets, technical infographics, listing copy, output refinement, and batch catalog workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can upload local product images and logos to VibeSKU.

Mitigation: Confirm each image or logo path is an intended, non-sensitive product asset before running generation or batch workflows.

Risk: Credentials may be stored in ~/.vibesku/config.json and sent to a configurable API endpoint.

Mitigation: Protect the config file, prefer scoped credentials, and keep VIBESKU_BASE_URL unset unless using a trusted HTTPS endpoint or localhost development server.

Risk: The artifact recommends checking and updating from an upstream main-branch version source.

Mitigation: Review skill updates before installation instead of allowing unattended update behavior.

## Reference(s):

- [VibeSKU homepage](https://www.vibesku.com)
- [Command reference](references/commands.md)
- [Template: ecom-hero](references/ecom-hero.md)
- [Template: kv-image-set](references/kv-image-set.md)
- [Template: exploded-view](references/exploded-view.md)
- [Template: listing](references/listing.md)
- [Versioning and auto-update](references/versioning.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and optional JSON-oriented CLI usage]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Agent-facing CLI workflows may reference local asset paths, environment variables, config files, and VibeSKU job or output identifiers.]

## Skill Version(s):

0.2.4 (source: server release evidence and VERSION file)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

唯品会（vip.com）电商服务技能包，帮助 agents handle Vipshop shopping workflows including login, product search, product detail lookup, promotion discovery, and image-based product search.

This skill is ready for commercial/non-commercial use.

## Publisher:

[viphgta](https://clawhub.ai/user/viphgta)

### License/Terms of Use:

MIT-0

## Use Case:

External users and shopping assistants use this skill bundle to search Vipshop products, compare prices and discounts, inspect product details, browse promotions, find visually similar products from images, and manage the Vipshop login state needed for those workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores Vipshop login cookies locally and reuses them across subskills.

Mitigation: Use only on trusted machines, restrict access to the local token file, and log out or remove stored cookies when shopping tasks are complete.

Risk: Generated product links may contain account-session material.

Mitigation: Do not share generated links or transcripts, and prefer links that do not embed session or exchange tokens.

Risk: Image search uploads selected local images to Vipshop services.

Mitigation: Confirm the selected image is intended for upload and contains no sensitive or unrelated personal content before using image search.

Risk: The artifact can automatically initiate login flows when a user is not logged in.

Mitigation: Require explicit user consent before starting login, installation, or upload actions in deployed agent workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/viphgta/skills/vipshop-skills)
- [Vipshop QR login API reference](vipshop-user-login/references/api_reference.md)
- [Vipshop login integration guide](vipshop-user-login/references/integration_guide.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown summaries with JSON-derived product, promotion, login, and image-search results plus shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include product links, prices, discounts, images, login-status messages, and pagination guidance.]

## Skill Version(s):

1.0.12 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

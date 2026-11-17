## Description:

Search Target.com, look up products, check per-store stock and pickup ETAs near a ZIP, and build a deep link that pre-populates a guest cart.

This skill is ready for commercial/non-commercial use.

## Publisher:

[druyang](https://clawhub.ai/user/druyang)

### License/Terms of Use:

MIT No Attribution License (MIT-0)

## Use Case:

External users and agents use this skill to search Target.com products, compare item details, check store-specific availability near a ZIP code, and prepare guest-cart handoff links without login or checkout.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated cart links contain a temporary bearer token that can grant cart-write access to whoever holds the URL.

Mitigation: Treat cart URLs and generated cart HTML files as private, avoid sharing full access_token URLs in chat or logs, and delete generated files after use.

Risk: The skill contacts Target public web endpoints and can create anonymous guest carts.

Mitigation: Install and run it only when that network behavior is acceptable; use --no-open when a browser should not be launched automatically.

Risk: Prices, stock, pickup ETAs, public endpoint behavior, and category IDs can change without notice.

Mitigation: Confirm current product, price, and availability details on Target.com before making purchase decisions, and keep the tested skill version pinned.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/druyang/skills/target-shopping)
- [Project homepage](https://github.com/druyang/target-shopper-skill)
- [Public-facing API endpoints used by this skill](references/endpoints.md)
- [Common Target category N-IDs](references/categories.md)
- [Target.com status codes and failure modes](references/status-codes.md)
- [Target.com etiquette and terms notes](references/tos-and-etiquette.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with bash commands, JSON script outputs, shopping-list Markdown, and optional local HTML cart files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Cart-link output can include a temporary private cart URL and local redirect file; generated URLs should not be pasted into chat or logs.]

## Skill Version(s):

0.1.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

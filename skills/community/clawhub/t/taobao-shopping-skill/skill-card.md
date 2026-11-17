## Description:

Taobao Shopping helps an agent search Taobao products, inspect item details and reviews, add products to the cart, and review cart items with price-change hints.

This skill is ready for commercial/non-commercial use.

## Publisher:

[he2y](https://clawhub.ai/user/he2y)

### License/Terms of Use:

MIT-0

## Use Case:

External users and shopping agents use this skill to gather Taobao product information, compare search results, inspect reviews, and manage cart-related shopping workflows through OpenCLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on a logged-in Taobao or Tmall browser session and can access shopping account data.

Mitigation: Use a dedicated Chrome profile for Taobao, avoid shared browser profiles, and do not expose the profile or cookies to unrelated browsing or automation.

Risk: Cart-changing actions can modify shopping data in the logged-in account.

Mitigation: Confirm any cart-changing action before execution and use the documented dry-run option when previewing add-to-cart behavior.

Risk: The workflow depends on an unpinned external OpenCLI tool and browser bridge extension.

Mitigation: Use a pinned and verified OpenCLI version, and inspect the browser extension permissions and source before loading it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/he2y/skills/taobao-shopping-skill)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and structured command outputs in table, JSON, YAML, Markdown, or CSV formats]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Chrome logged in to Taobao or Tmall, OpenCLI, and the OpenCLI Browser Bridge extension.]

## Skill Version(s):

1.0.0 (source: frontmatter, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

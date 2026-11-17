## Description:

Retrieves Xiaohongshu Mall product search results, shop listings, and product details through the AI Data Platform.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cuiyunhai](https://clawhub.ai/user/cuiyunhai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and e-commerce analysts use it to retrieve Xiaohongshu Mall product search results, shop listings, and product details for product selection, competitor price checks, and shop monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Product search and retrieval requests consume platform points, and requesting additional empty pages is still billed.

Mitigation: Check the free balance and current per-call price first; stop pagination when a page returns fewer than 20 items.

Risk: The skill uses network, file, and shell capabilities and stores an authorized API key in a local configuration file; the server security scan was partial and noted undeclared tool capabilities.

Mitigation: Review whether these capabilities fit the intended environment, use an authorized account, and protect the local credential file.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cuiyunhai/skills/xhs-shop-data)
- [AI Data Platform](https://zlh.aidata366.com)

## Skill Output:

**Output Type(s):** [JSON, Files]

**Output Format:** [JSON responses and JSON files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Paginated product data; large responses can be saved to a file.]

## Skill Version(s):

1.0.7 (source: SKILL.md frontmatter; server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

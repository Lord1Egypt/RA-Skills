## Description:

This skill helps agents perform Shopee marketplace research across supported sites, including keyword research, product discovery, review analysis, category browsing, and account balance checks through the Shopdora OpenAPI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fionavv](https://clawhub.ai/user/fionavv)

### License/Terms of Use:

MIT-0

## Use Case:

External users and ecommerce analysts use this skill to research Shopee keywords, products, categories, customer reviews, and Shopdora account quota across supported regional marketplaces. The skill is intended for paid Shopdora API workflows where the agent confirms parameters before charged calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses long-lived Shopdora API credentials and local token storage, which can expose a paid account if secrets are pasted into chat, logged, or stored with broad filesystem permissions.

Mitigation: Configure credentials outside chat when possible, restrict ~/.shopdora permissions to the owning user, avoid printing secrets, and rotate the Shopdora clientSecret if it is exposed or stored insecurely.

Risk: Charged Shopdora endpoints can consume quota when successful non-empty results are returned.

Mitigation: Confirm site, keyword, time range, pagination, and other paid-call parameters before execution, check cached results first, and inform the user before additional charged pages are fetched.

## Reference(s):

- [Shopdora OpenAPI Reference](references/api_docs.md)
- [Shopdora Website](https://www.shopdora.com)
- [ClawHub Skill Page](https://clawhub.ai/fionavv/skills/shopdora-shopee-tool)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with tables, JSON-backed API results, and inline shell commands for setup and API calls]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local credential, token, and cache files under ~/.shopdora when the user provides Shopdora API credentials.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

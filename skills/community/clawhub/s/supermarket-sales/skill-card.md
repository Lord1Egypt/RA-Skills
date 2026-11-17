## Description:

Fetch weekly sale details from Australian supermarkets Woolworths and Coles for current specials, price comparisons, and sale information.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nicowu07](https://clawhub.ai/user/nicowu07)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to retrieve and compare current Woolworths and Coles specials, especially for Melbourne metro shopping checks.

### Deployment Geography for Use:

Australia, with Melbourne metro postcodes 3000-3008 as the documented fit.

## Known Risks and Mitigations:

Risk: Browser automation runs against external websites with Chromium sandboxing disabled.

Mitigation: Run only in a constrained, unprivileged environment, avoid root execution, and remove Chromium no-sandbox flags where host sandboxing is supported.

Risk: Dependency installation is not reproducible for production use.

Mitigation: Pin dependencies and commit a lockfile before production deployment.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/nicowu07/skills/supermarket-sales)
- [Coles specials](https://www.coles.com.au/on-special)
- [Woolworths catalogue](https://www.woolworths.com.au/shop/catalogue)
- [Catalogue AU Woolworths specials](https://www.catalogueau.com/sales/?stores=Woolworths)
- [Current Specials Woolworths weekly catalogue](https://currentspecials.com.au/woolworths-weekly-catalogue/)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Markdown tables, JSON objects, and concise command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Network-dependent; results are time-sensitive and limited by retailer site availability.]

## Skill Version(s):

1.2.0 (source: server release metadata; package.json reports 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

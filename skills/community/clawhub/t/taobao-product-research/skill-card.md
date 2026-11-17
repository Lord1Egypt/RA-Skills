## Description:

Taobao Product Research collects Taobao product data, including main images, titles, prices, sales counts, review counts, shops, and product links, then generates image-backed Excel research reports for market and competitive analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[redcreen](https://clawhub.ai/user/redcreen)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and ecommerce researchers use this skill to collect Taobao search results by keyword and price range, compare products, monitor pricing, and create Excel reports with product details and images.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill persists a logged-in Taobao browser profile on disk.

Mitigation: Use a dedicated Taobao account in an isolated workspace and delete the browser_data directory after each research session when persistent login is no longer needed.

Risk: The skill downloads marketplace-controlled image URLs with weak safeguards.

Mitigation: Run it on a network where internal services are not reachable, review downloaded files before sharing, and add URL validation and download limits before routine use.

Risk: Dependencies and browser automation behavior may change over time.

Mitigation: Pin and update dependencies deliberately, then re-run security review before deploying the skill for repeated operational use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/redcreen/skills/taobao-product-research)
- [Publisher profile](https://clawhub.ai/user/redcreen)
- [Taobao search](https://s.taobao.com)

## Skill Output:

**Output Type(s):** [text, shell commands, code, configuration, guidance]

**Output Format:** [Markdown guidance with command examples; runtime produces console text, downloaded images, debug screenshots, JSON summaries, and Excel .xlsx reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The script accepts a keyword, price range, item count, and optional output directory; reports include product images, titles, prices, sales, reviews, shops, and links.]

## Skill Version(s):

1.0.0 (source: release evidence and scripts/package.json, released 2026-03-18)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

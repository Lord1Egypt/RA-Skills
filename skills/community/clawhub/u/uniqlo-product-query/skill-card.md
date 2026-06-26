## Description: <br>
Query Uniqlo discounted products for men, women, kids, and baby clothing, generating a Markdown file with product images, prices, discount rates, and purchase links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gpyangyoujun](https://clawhub.ai/user/gpyangyoujun) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to find Uniqlo China discounted products by clothing category and optional size. It is intended for sale, discount, promotion, or special-price queries and produces a local Markdown shopping report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes outbound requests to Uniqlo China to retrieve sale data. <br>
Mitigation: Install and run it only in environments where those outbound requests are acceptable. <br>
Risk: The skill creates Markdown reports in a local unique/ folder under the current working directory. <br>
Mitigation: Run it from an appropriate workspace or adjust the output location before use in shared or clutter-sensitive directories. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gpyangyoujun/uniqlo-product-query) <br>
- [Publisher profile](https://clawhub.ai/user/gpyangyoujun) <br>
- [Uniqlo China product detail pages](https://www.uniqlo.cn/product-detail.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, API calls] <br>
**Output Format:** [Plain-text response plus a timestamped Markdown report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes reports to a local unique/ directory; entries include images, prices, discount rates, and product links.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

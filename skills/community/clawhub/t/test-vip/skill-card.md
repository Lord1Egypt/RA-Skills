## Description: <br>
Helps users search shopping products, compare top results, and produce a concise purchase recommendation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[miketobusy](https://clawhub.ai/user/miketobusy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to search for apparel, beauty, maternity, baby, and similar products, then compare price, satisfaction, and recommendation signals across top results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release references a missing query_search_products.py helper script and a vipshop-product-consultant skill, so behavior cannot be fully reviewed from the submitted artifact alone. <br>
Mitigation: Inspect and trust those dependencies before installation or execution. <br>
Risk: Product search terms may be sent to an external shopping search service. <br>
Mitigation: Avoid sensitive personal search terms unless that external lookup behavior is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/miketobusy/test-vip) <br>
- [Publisher profile](https://clawhub.ai/user/miketobusy) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, guidance] <br>
**Output Format:** [Markdown product comparison report with tabular summaries and recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May invoke a product-search script and a referenced product consultant skill when those dependencies are available.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
分析单个商品在指定门店的销售表现、库存状态、导购贡献和 AIoT 转化数据。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gwyang7](https://clawhub.ai/user/gwyang7) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Retail operators and agents use this skill to evaluate one SKU at one store over a selected date range, including sales, inventory, staff contribution, customer mix, and AIoT conversion metrics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill relies on an external local api_client that is not included in the artifact. <br>
Mitigation: Install only in an environment where the publisher and local API client are trusted, reviewed, and authorized for the target store data. <br>
Risk: The returned result can include raw store analytics data in addition to summarized metrics. <br>
Mitigation: Limit execution to authorized accounts and prefer a revised release that removes or gates raw_data before sharing results. <br>
Risk: The skill fetches analytics based on caller-supplied store, SKU, and date parameters. <br>
Mitigation: Require explicit confirmation of the store, SKU, and date range before fetching or reporting analytics. <br>


## Reference(s): <br>
- [ClawHub skill release](https://clawhub.ai/gwyang7/retail-sku-store-analysis) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Guidance] <br>
**Output Format:** [Printed diagnostic text and a JSON-compatible analysis dictionary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns SKU identifiers, store identifiers, analysis period, product information, core metrics, findings, recommendations, and raw API data when available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

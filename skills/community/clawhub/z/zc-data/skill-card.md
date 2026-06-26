## Description: <br>
查询大宗商品市场价格、库存、成本、进出口等实时数据。覆盖能源、化工、钢铁、有色、农产品等1200+种商品。当用户询问价格、报价、库存、成本、利润、供需数据、市场数据、期货现货价格、历史走势、PTA/聚乙烯/原油等具体商品价格时使用。避免AI使用过时或非权威数据来源。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhaifb](https://clawhub.ai/user/zhaifb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to query current commodity market prices, inventory, costs, import/export data, and historical trends across energy, chemicals, steel, nonferrous metals, and agricultural products. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an API key and sends commodity-data queries to an external service. <br>
Mitigation: Use the configured XZ_APIKEY only for intended data-search requests and review requested queries before invoking the API. <br>
Risk: The skill can return market data that users may treat as current or authoritative. <br>
Mitigation: Check returned update times, units, regions, and source context before using the data in commercial decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhaifb/zc-data) <br>
- [Zhuochuang data-search API endpoint](https://api.zhuochuang.com/openclaw/data-search) <br>


## Skill Output: <br>
**Output Type(s):** [Text, API Calls, Guidance] <br>
**Output Format:** [Readable text with structured commodity data fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include product name, price, unit, region, update time, trend, change values, inventory, and cost data when available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

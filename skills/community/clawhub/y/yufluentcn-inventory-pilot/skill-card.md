## Description: <br>
库存驾驭助手：销量预测、补货建议、滞销预警、资金占用分析，基于卖家提供的销量和库存数据经 Yufluent 云端 Harness 输出结构化 JSON。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[metahuan](https://clawhub.ai/user/metahuan) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Ecommerce sellers and inventory operators use this skill to forecast sales, assess replenishment needs, identify slow-moving SKUs, and analyze capital tied up in inventory from user-provided sales and stock data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-provided sales, inventory, stock, cost, and related business data may be sent to Yufluent's configured cloud endpoint. <br>
Mitigation: Use the skill only when that data sharing is acceptable, limit inputs to intended business data, and avoid providing highly sensitive files unless required. <br>
Risk: The skill relies on TOKENAPI_KEY and allows TOKENAPI_BASE_URL to change the remote endpoint. <br>
Mitigation: Keep TOKENAPI_KEY private and configure TOKENAPI_BASE_URL only to trusted, preferably HTTPS, services. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/metahuan/yufluentcn-inventory-pilot) <br>
- [Publisher profile](https://clawhub.ai/user/metahuan) <br>
- [Yufluent homepage](https://claw.changzhiai.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, guidance] <br>
**Output Format:** [Formatted text or structured JSON returned by the Yufluent cloud skill run.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill uses TOKENAPI_KEY and may send user-provided sales, inventory, stock, cost, and related business data to the configured Yufluent endpoint.] <br>

## Skill Version(s): <br>
1.1.2 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

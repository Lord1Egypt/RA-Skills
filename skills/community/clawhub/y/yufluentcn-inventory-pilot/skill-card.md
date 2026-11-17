## Description:

库存驾驭助手：销量预测、补货建议、滞销预警、资金占用分析；基于卖家提供的销量和库存数据，经 Yufluent 云端 Harness 输出结构化 JSON。

This skill is ready for commercial/non-commercial use.

## Publisher:

[metahuan](https://clawhub.ai/user/metahuan)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers, operators, and inventory analysts use this skill to forecast sales, evaluate replenishment needs, identify slow-moving inventory, and analyze capital tied up in stock from user-provided sales and inventory data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uploads selected sales, stock, inventory-aging, lead-time, and cost data to Yufluent/OpenClaw cloud services.

Mitigation: Use explicit, non-sensitive input files and review the data before execution.

Risk: The skill can read local file paths supplied as CLI arguments and send their contents to the cloud service.

Mitigation: Avoid arbitrary local paths and pass only intended sales or inventory files.

Risk: Changing TOKENAPI_BASE_URL can redirect requests and credentials to another endpoint.

Mitigation: Keep TOKENAPI_BASE_URL unset unless the endpoint is trusted, and do not use non-local HTTP endpoints with a real TOKENAPI_KEY.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/metahuan/skills/yufluentcn-inventory-pilot)
- [Yufluent homepage](https://claw.changzhiai.com)
- [OpenClaw app documentation](https://claw.changzhiai.com/app/openclaw)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [Structured JSON and formatted text returned from the Yufluent cloud inventory workflow]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires TOKENAPI_KEY; outputs are advisory and do not place orders or connect directly to ERP or marketplace APIs.]

## Skill Version(s):

1.1.2 (source: server release and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

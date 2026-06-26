## Description: <br>
查询《洛克王国世界》远行商人当前库存，自动过滤出本轮仍有效的商品。适用于想查看远行商人当前卖什么，或需要输出简洁文本、JSON 结果时使用；需要用户自行提供 API key。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nitansde](https://clawhub.ai/user/nitansde) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Players and agents use this skill to fetch the current Roco Kingdom World traveling merchant inventory, filter out items outside the current sales window, and return a concise text or JSON result. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a user-provided API key. <br>
Mitigation: Use an API key you are allowed to use, prefer an environment variable or local secret, and avoid placing the key in shared chat, command history, or logs. <br>
Risk: The skill depends on a third-party API service for inventory data. <br>
Mitigation: Install and run it only if you trust the publisher and the wegame.shallow.ink API service. <br>


## Reference(s): <br>
- [API 说明](references/api.md) <br>
- [ClawHub skill page](https://clawhub.ai/nitansde/rocom-merchant-inventory) <br>
- [Merchant inventory API endpoint](https://wegame.shallow.ink/api/v1/games/rocom/merchant/info?refresh=true) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [Plain text by default, or JSON when requested] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Filters inventory items by the current Beijing-time sales window and includes fetched time, round status, item count, item names, images, and availability windows when available.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

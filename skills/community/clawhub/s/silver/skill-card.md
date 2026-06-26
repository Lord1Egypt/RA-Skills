## Description: <br>
查询国内白银期货/现货相关及伦敦银等参考行情。当用户说：白银现在什么价？伦敦银涨跌多少？或类似白银价格问题时，使用本技能。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jisuapi](https://clawhub.ai/user/jisuapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to retrieve current and historical silver price data from JisuAPI for Shanghai gold exchange silver, Shanghai futures silver, London silver, and supported historical market queries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a JISU_API_KEY for a third-party market data service. <br>
Mitigation: Store the key only in the environment, avoid pasting it into prompts or logs, and install the skill only if JisuAPI is an acceptable data provider. <br>
Risk: Authenticated requests may fail in this version because server evidence reports a likely request parameter handling bug. <br>
Mitigation: Expect possible API errors and verify returned data before relying on it until the request parameter handling is corrected. <br>
Risk: Silver price data can be unavailable or incomplete for a requested market, product, or date range. <br>
Mitigation: Handle API error responses and no-data responses explicitly before summarizing prices or trends to users. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jisuapi/skills/silver) <br>
- [JisuAPI](https://www.jisuapi.com/) <br>
- [JisuAPI Silver API documentation](https://www.jisuapi.com/api/silver/) <br>
- [JisuAPI Silver API endpoint](https://api.jisuapi.com/silver) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [JSON API results and concise text guidance, with shell commands for agent execution] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and the JISU_API_KEY environment variable.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

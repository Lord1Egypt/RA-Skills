## Description:

查询国内白银期货/现货相关及伦敦银等参考行情。当用户说：白银现在什么价？伦敦银涨跌多少？或类似白银价格问题时，使用本技能。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jisuapi](https://clawhub.ai/user/jisuapi)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to query current and historical silver market prices from JisuAPI, including Shanghai Gold Exchange, Shanghai Futures Exchange, London silver, and historical price ranges.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends silver-price query parameters to the third-party JisuAPI service and requires access to a JisuAPI AppKey.

Mitigation: Confirm the user or deploying organization is comfortable sharing those query parameters with JisuAPI, store JISU_API_KEY securely, and avoid logging the key.

Risk: Authenticated results may fail because the code constructs appkey parameters but must be corrected to send them reliably.

Mitigation: Verify and correct API request parameter handling before deployment, then test each endpoint with a valid JISU_API_KEY.

Risk: Market data can be unavailable, delayed, or incomplete for a requested market, instrument, or date range.

Mitigation: Surface API error codes and update timestamps to users, and avoid presenting returned prices as financial advice.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jisuapi/skills/silver)
- [JisuAPI silver price API](https://www.jisuapi.com/api/silver/)
- [JisuAPI website](https://www.jisuapi.com/)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Configuration guidance]

**Output Format:** [JSON returned by command-line API queries, with stderr messages for missing configuration or invalid input.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and JISU_API_KEY; history queries require market, startdate, enddate, and type.]

## Skill Version(s):

1.0.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

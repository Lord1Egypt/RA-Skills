## Description: <br>
A股全能数据套件，26个实时API接口：K线分时、涨停板梯队、资金流向、龙虎榜、竞价数据、板块轮动、研报热榜等；包含4个子技能包，一个Key通用。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jcdreamjc](https://clawhub.ai/user/jcdreamjc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and analysts use this index skill to find and configure the appropriate WuDao A-share child skill for market data, limit-up analysis, capital flow analysis, and market intelligence workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The linked child skills provide the actual data functionality and may carry separate behavior or security considerations. <br>
Mitigation: Review each linked child skill separately before installing or using it. <br>
Risk: The skill requires API key configuration for the WuDao stock data service. <br>
Mitigation: Use a dedicated API key, avoid sharing it in prompts or logs, and rotate or revoke it when it is no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jcdreamjc/wudao-ashare) <br>
- [wudao-market child skill](https://clawhub.ai/skills/wudao-market) <br>
- [wudao-limitup child skill](https://clawhub.ai/skills/wudao-limitup) <br>
- [wudao-analysis child skill](https://clawhub.ai/skills/wudao-analysis) <br>
- [wudao-intel child skill](https://clawhub.ai/skills/wudao-intel) <br>
- [WuDao API site](https://stock.quicktiny.cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown guidance with links and environment variable setup] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documents the LB_API_KEY and LB_API_BASE environment variables and delegates data workflows to separately installable child skills.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

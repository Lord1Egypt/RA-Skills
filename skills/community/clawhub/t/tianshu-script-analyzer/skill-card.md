## Description: <br>
天枢短剧爆款因子分析报告 returns Chinese short-drama hit-factor analysis reports from a drama title or keyword, with a free preview and a paid full report covering audience psychology, story structure, vertical-video craft, market positioning, and reusable formulas. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[makclaw](https://clawhub.ai/user/makclaw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External short-drama creators, producers, investors, and analysts use this skill to request Chinese short-drama hit-factor reports, compare why specific titles became popular, and extract reusable creative and commercial patterns. <br>

### Deployment Geography for Use: <br>
China; the artifact describes Alipay payment as available only to domestic users. <br>

## Known Risks and Mitigations: <br>
Risk: The skill calls sinodata.io to fetch catalog and report content. <br>
Mitigation: Install it only when the user expects this external Chinese short-drama analysis service and is comfortable sharing the requested title or keyword with that provider. <br>
Risk: Full reports require a 9.90 CNY Alipay payment flow. <br>
Mitigation: Show the payment link and amount clearly, and confirm successful payment before requesting the paid full report. <br>
Risk: Users may enter confidential scripts, business plans, or unreleased project details while seeking analysis. <br>
Mitigation: Ask users to avoid confidential material unless they accept the provider's handling of that content. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/makclaw/tianshu-script-analyzer) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/makclaw) <br>
- [Sinodata analyzer API](https://sinodata.io/v1/analyzer) <br>
- [Sinodata analyzer catalog endpoint](https://sinodata.io/v1/analyzer/plays?limit=200) <br>
- [Sinodata analyzer report endpoint](https://sinodata.io/v1/analyzer/report?id=shaobing_tainainai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance, API calls] <br>
**Output Format:** [Markdown report content with API-derived preview or full analysis text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Free previews are approximately 1000-1500 Chinese characters; paid full reports are described as approximately 3000-8000 Chinese characters.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact config lists 1.0.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

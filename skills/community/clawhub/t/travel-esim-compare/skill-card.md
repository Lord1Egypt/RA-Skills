## Description: <br>
零配置即装即用，提供3项出境上网工具，支持eSIM套餐比价和WiFi租借查询，覆盖30+热门目的地，基于主流eSIM运营商实时数据。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[travel-skills](https://clawhub.ai/user/travel-skills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Travelers and travel-planning agents use this skill to compare embedded eSIM, pocket WiFi, and local SIM guidance for international destinations. It helps estimate data needs, compare package price and duration, and choose a practical connectivity option before purchase. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Embedded eSIM and WiFi prices may be outdated or differ from provider checkout prices. <br>
Mitigation: Treat results as planning guidance and confirm current prices, coverage, and terms on provider sites before purchase. <br>
Risk: The artifact declares an optional PROXY_TOKEN even though security evidence reports local static data with no network calls. <br>
Mitigation: Deploy without providing secrets unless the publisher documents a live-data integration that requires them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/travel-skills/travel-esim-compare) <br>
- [Publisher profile](https://clawhub.ai/user/travel-skills) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, guidance] <br>
**Output Format:** [JSON strings with human-facing travel connectivity recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses embedded static travel connectivity data and does not provide purchase links.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

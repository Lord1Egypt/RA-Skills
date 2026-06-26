## Description: <br>
使用 UAPI 的“查询天气”单接口 skill，处理 查询天气、天气预报、城市天气、adcode天气、实时天气、天气查询 等请求。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shuakami](https://clawhub.ai/user/shuakami) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and developers use this skill to decide when and how to call UAPI's GET /misc/weather endpoint for real-time weather, forecasts, and city or adcode-based lookups. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Weather lookups call an external UAPI service, and generic requests without a city or adcode may rely on IP-based location. <br>
Mitigation: Prefer explicit city or adcode inputs, and provide a UAPI Key only when the user trusts the service and needs authenticated or higher-quota access. <br>


## Reference(s): <br>
- [Quick Start](references/quick-start.md) <br>
- [查询天气](references/operations/get-misc-weather.md) <br>
- [Misc 分类接口](references/resources/Misc.md) <br>
- [UAPI Service](https://uapis.cn) <br>
- [UAPI API Base URL](https://uapis.cn/api/v1) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API calls, Guidance] <br>
**Output Format:** [Markdown guidance with endpoint, query parameter, authentication, and response-code details.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include UAPI request parameters such as city, adcode, forecast flags, language, and optional UAPI Key guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

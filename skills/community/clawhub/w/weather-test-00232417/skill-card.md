## Description: <br>
天气查询测试技能 lets OpenClaw users ask for simple real-time weather information for selected Chinese cities and receive concise Chinese replies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[panqiang10](https://clawhub.ai/user/panqiang10) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users can ask for current weather in supported cities such as Beijing, Shanghai, Guangzhou, Shenzhen, Hangzhou, Chengdu, and Chongqing. The skill is useful for quick spoken or chat-style weather checks where a brief response is preferred. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: City queries are sent to a public weather service over unencrypted HTTP. <br>
Mitigation: Avoid sensitive location-related queries and consider replacing the upstream call with an HTTPS weather provider before sensitive or regulated use. <br>
Risk: Weather data comes from a public test interface and may be delayed or unavailable. <br>
Mitigation: Treat responses as convenience information and retry later or use another source when accuracy is important. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/panqiang10/weather-test-00232417) <br>
- [wttr.in weather service](https://wttr.in/) <br>


## Skill Output: <br>
**Output Type(s):** [text] <br>
**Output Format:** [OpenClaw JSON response containing a short Chinese text reply] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns either a weather summary, a prompt for a supported city, or a brief failure message.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

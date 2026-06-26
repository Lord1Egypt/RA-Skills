## Description: <br>
DeepTrip helps agents answer travel requests through Tongcheng Travel, including hotel search, transportation options, attraction recommendations, itinerary planning, and booking links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tclxhai-lv](https://clawhub.ai/user/tclxhai-lv) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use DeepTrip to handle travel planning requests for hotels, flights, trains, attractions, and itineraries, returning recommendations with product links for booking. Developers can configure an optional API key when higher service limits are needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Travel requests may include destinations, dates, budgets, preferences, and other personal trip context that is sent to Tongcheng/DeepTrip. <br>
Mitigation: Share only the minimum trip context needed for recommendations and avoid sending sensitive personal details unless required for the travel task. <br>
Risk: The skill prompts users to sign in through a WeChat/Tongcheng link for booking continuity. <br>
Mitigation: Sign in only when booking or account continuity is needed, and confirm the user intends to enter the third-party account flow. <br>
Risk: The DeepTrip API does not preserve multi-turn memory for the agent. <br>
Mitigation: Include the relevant prior recommendations and updated constraints in each follow-up query. <br>


## Reference(s): <br>
- [ClawHub DeepTrip skill page](https://clawhub.ai/tclxhai-lv/tc-deeptrip) <br>
- [DeepTrip chat API endpoint](https://dtgw.ly.com/deeptrip/claw/chat) <br>
- [Tongcheng Travel AI API key page](https://deeptrip.ly.com/#/shareLand?searchText=%E6%BF%80%E6%B4%BB%E7%A0%81) <br>
- [Tongcheng Travel WeChat login](https://open.weixin.qq.com/connect/qrconnect?appid=wx3827070276e49e30&redirect_uri=http%3a%2f%2fwx.17u.cn%2fflight%2fgetwxuserinfo.html%3furl%3dhttps%253a%252f%252fpassport.ly.com%252fThirdParty%252fWeChatLogin%253fpageUrl%253dhttps%25253a%25252f%25252fdeeptrip.ly.com%25252f%252523%25252f%2526state%253d0abb2c15e81f4da2906cf7222c57dbb7&response_type=code&scope=snsapi_login#wechat_redirect) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance, Configuration] <br>
**Output Format:** [Markdown-style travel recommendations with product links, plus optional JSON API response data.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requests are independent; the agent must include needed prior context in each query.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata and artifact/_meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
获取北京明日天气预报和黄历，每天下午6点推送。包含气温对比提醒（波动超5℃警告）、雨天带伞提醒、以及第二天的黄历信息。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lixiaojie-1012](https://clawhub.ai/user/lixiaojie-1012) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Chinese-speaking users use this skill to prepare a daily 18:00 Beijing weather and almanac reminder for Feishu. It fetches tomorrow's forecast, compares temperatures, flags rain risk, and formats Chinese almanac宜/忌 information for delivery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Weather, almanac, or search results may be unavailable or inaccurate. <br>
Mitigation: Retry wttr.in once, verify the constructed tomorrow date, and send a clear failure message instead of inventing missing data. <br>
Risk: A configured Feishu delivery could send reminders to the wrong recipient or keep running unexpectedly. <br>
Mitigation: Confirm the Feishu openid before use and keep the daily 18:00 Asia/Shanghai schedule visible and easy to remove. <br>
Risk: mxnzp API credentials could be exposed if embedded in shared skill text or shell history. <br>
Mitigation: Store app_id and app_secret securely and avoid placing secrets in prompts, shared files, or shell history. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lixiaojie-1012/weather-of-beijing-with-almanac) <br>
- [wttr.in Beijing weather JSON endpoint](https://wttr.in/Beijing?format=j1) <br>
- [mxnzp holiday single-day API](https://www.mxnzp.com/api/holiday/single/${TOMORROW}?ignoreHoliday=false&app_id=your_app_id&app_secret=your_secret) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, API calls, guidance] <br>
**Output Format:** [Markdown message with weather, temperature-change alert, rain reminder, and Chinese almanac sections] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl for wttr.in lookups and may use mxnzp API credentials or web search for almanac data.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

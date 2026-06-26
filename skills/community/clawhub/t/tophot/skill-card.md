## Description: <br>
Fetches current hotspot and news lists from hotspot.api4claw.com and presents titles grouped by source. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xltang](https://clawhub.ai/user/xltang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to request daily hotspots, platform-specific hot topics, or hotspot service status. It fetches the declared API on demand, parses JSON responses, and summarizes available titles by source. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts hotspot.api4claw.com when invoked. <br>
Mitigation: Install only if outbound requests to this declared API are acceptable for the deployment environment. <br>
Risk: Optional scheduled updates can create recurring messages if the user approves a cron command. <br>
Mitigation: Review the generated schedule, timezone, channel, recipient, and message text before approving any scheduling command. <br>
Risk: The generic trigger "热点" may activate when a user intended a broader discussion rather than a live hotspot fetch. <br>
Mitigation: Prefer narrower triggers such as "今日热点", "微博热点", "新闻联播", "知乎热点", or "腾讯早报" in contexts where accidental activation would be disruptive. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xltang/tophot) <br>
- [Hotspot API base URL](https://hotspot.api4claw.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown summaries with optional shell commands for user-approved scheduling] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Groups hotspot titles by source_name, omits fetched_at and data_date metadata, and reports explicit errors when the API fails or returns malformed JSON.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

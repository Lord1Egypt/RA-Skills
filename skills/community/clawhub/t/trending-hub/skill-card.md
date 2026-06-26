## Description: <br>
Aggregates trending topics from Douyin, Weibo, Bilibili, Kuaishou, Zhihu, Toutiao, and Baidu so an agent can summarize what people are discussing across the Chinese web. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[redfox-data](https://clawhub.ai/user/redfox-data) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to check cross-platform hot lists, understand current online discussion, generate trend reports, and manage hotspot push workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends a RedFox API key over HTTPS while certificate verification is disabled, creating credential interception or response tampering risk. <br>
Mitigation: Keep normal HTTPS certificate verification enabled before using a real key, store the key securely, and rotate it if exposure is suspected. <br>
Risk: Subscription or push behavior may run on an unclear schedule or delivery channel. <br>
Mitigation: Enable subscription or push behavior only after the schedule, destination, and cancellation flow are explicit. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/redfox-data/trending-hub) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown and concise text summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require a RedFox API key and network calls to redfox.hk.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

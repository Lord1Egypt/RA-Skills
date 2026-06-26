## Description: <br>
Sentiment Compass monitors Chinese social media keyword mentions, analyzes sentiment, generates reports, and sends Feishu or email alerts when negative sentiment crosses configured thresholds. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qiji0802](https://clawhub.ai/user/qiji0802) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, operators, and developers use this skill to track brand or competitor mentions across Xiaohongshu, Douyin, Weibo, and WeChat public content, then review sentiment reports and receive negative-sentiment alerts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can scrape public social-media content, which may create platform-terms or policy concerns. <br>
Mitigation: Review the applicable platform terms, monitor only permitted public content, and use conservative crawl schedules. <br>
Risk: Configured keys, webhooks, SMTP settings, and monitoring data are stored locally in plaintext configuration and database files. <br>
Mitigation: Use dedicated credentials, restrict local filesystem access, rotate secrets when needed, and avoid storing unnecessary sensitive keywords or results. <br>
Risk: When AI analysis, alerts, email, or token validation are used, monitored text or alert summaries can be sent to GLM-4, Feishu, SMTP, and the license-validation service. <br>
Mitigation: Confirm data-sharing approval before use, avoid regulated or confidential monitoring topics, and isolate the runtime for production deployments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/qiji0802/sentiment-compass) <br>
- [Publisher profile](https://clawhub.ai/user/qiji0802) <br>
- [YK-Global](https://yk-global.com) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown summaries and JSON command results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can include sentiment labels, scores, reason summaries, platform counts, trend data, alert payloads, and configuration guidance.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

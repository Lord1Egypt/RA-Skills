## Description: <br>
自动监控深交所、上交所、北交所、股转系统、中国结算和证券业协会等证券监管页面，检测页面变化并生成通知。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huifeideyua1231](https://clawhub.ai/user/huifeideyua1231) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations users can use this skill to check monitored Chinese securities-regulation pages, run the batch crawler, inspect generated change notifications, and prepare Enterprise WeChat updates when changes are found. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The reviewed skill delegates core monitoring work to pre-existing root-level scripts and a persistent cron setup outside the packaged artifact. <br>
Mitigation: Install or run it only where the /root/monitoring/securities system is controlled and reviewed, and confirm the cron entry is intended before use. <br>
Risk: The workflow can use an XCrawl API key, write temporary and log files, and prepare Enterprise WeChat notifications to a configured recipient. <br>
Mitigation: Verify API key handling, /tmp and /var/log outputs, and the Enterprise WeChat destination before sending notifications. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/huifeideyua1231/securities-monitor) <br>
- [API 说明](references/api.md) <br>
- [配置说明](references/config.md) <br>
- [XCrawl Scrape API](https://run.xcrawl.com/v1/scrape) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and generated text or diff notification files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read monitored page snapshots, generate notification and diff files under /tmp, and write execution logs under /var/log/securities when the external monitoring system is present.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

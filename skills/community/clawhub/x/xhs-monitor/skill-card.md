## Description: <br>
小红书竞品监控 - 自动采集竞品笔记，推送飞书通知，写入数据看板 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cstdr](https://clawhub.ai/user/cstdr) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and operators use this skill to configure and run a Xiaohongshu competitor monitoring workflow that collects recent notes from configured accounts, deduplicates local history, extracts useful product and live-stream signals, and optionally sends Feishu updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses stealth browser automation with a persistent logged-in Xiaohongshu session. <br>
Mitigation: Review the code and platform policy before use, use a dedicated Xiaohongshu account and browser profile, and remove or fully understand stealth dependencies before deployment. <br>
Risk: Chrome remote debugging and scheduled execution can leave an authenticated browser profile exposed or running unattended. <br>
Mitigation: Keep remote debugging local and closed when not needed, and avoid cron-style scheduling until logging, monitoring, and cleanup are in place. <br>
Risk: Optional Feishu and Bitable integrations can send collected content or write records outside the local machine. <br>
Mitigation: Grant Feishu and Bitable permissions narrowly and verify the destination application, table, and notification settings before enabling them. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/cstdr/xhs-monitor) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Code] <br>
**Output Format:** [Markdown guidance with inline shell commands and JavaScript configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The configured workflow can produce scraped note records, local history files, parsed summaries, and optional Feishu card or Bitable updates.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

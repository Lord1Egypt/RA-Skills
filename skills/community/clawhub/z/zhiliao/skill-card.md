## Description: <br>
Zhiliao helps agents create natural-language tracking topics, aggregate related news articles from the Zhiliao service, browse cached topic articles, manage subscriptions, and set recurring update checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jfeng03-dev](https://clawhub.ai/user/jfeng03-dev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to configure a Zhiliao API key, create or subscribe to tracked topics, fetch relevant articles, review local topic caches, unsubscribe from topics, and schedule periodic article checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The artifact includes a local agent settings file with broad allowed actions and under-disclosed permissions. <br>
Mitigation: Review or remove .claude/settings.local.json before installing and grant only the permissions needed for the intended workflow. <br>
Risk: Credential handling relies on ZHILIAO_API_KEY or ~/.zhiliao/config.json, and bundled or copied credentials could be reused accidentally. <br>
Mitigation: Ignore any bundled API key, rotate exposed credentials, configure a fresh ZHILIAO_API_KEY, and restrict permissions on ~/.zhiliao/config.json. <br>
Risk: The default API base URL shown in the artifact uses HTTP, which may expose requests if the service does not redirect or support TLS. <br>
Mitigation: Prefer an HTTPS ZHILIAO_BASE_URL if the service supports it. <br>
Risk: Cron examples can keep making recurring API calls after setup. <br>
Mitigation: Add scheduled jobs deliberately, monitor API usage, and remove OpenClaw cron jobs when tracking is no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jfeng03-dev/zhiliao) <br>
- [Zhiliao website](https://zhiliao.news/) <br>
- [Zhiliao API key page](https://open.zhiliao.news/) <br>
- [OpenClaw documentation](https://docs.openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown responses with inline shell commands and local JSON cache files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses ZHILIAO_API_KEY and stores topics, sessions, and article caches under ~/.zhiliao/.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

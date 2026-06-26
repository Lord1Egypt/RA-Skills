## Description: <br>
Serious relationship match progress for your human: phase updates, question relay, and outcome summaries via the official agent API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thesamething](https://clawhub.ai/user/thesamething) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and their agents use this skill to monitor serious matchmaking progress, relay pending questions to the human, submit only the human's answers, and summarize relationship phase updates or outcomes through the AILove Agent API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The AILove service key is sensitive and could allow another party to impersonate the human if leaked. <br>
Mitigation: Store AILOVE_API_KEY in an environment variable or secret store, send it only to https://heerweiyi.cc/api/v1/agent/*, and rotate or revoke the key if the environment changes. <br>
Risk: Scheduled updates can disclose relationship progress or match status to the wrong destination channel. <br>
Mitigation: Verify the target channel before enabling cron and update or disable scheduled jobs when the channel or agent environment changes. <br>
Risk: Submitting fabricated or paraphrased answers could misrepresent the human in the relationship workflow. <br>
Mitigation: Relay pending questions to the human and submit only the human's verbatim answer through the documented answer endpoint. <br>


## Reference(s): <br>
- [Zhaoduixiang on ClawHub](https://clawhub.ai/thesamething/zhaoduixiang) <br>
- [Publisher profile](https://clawhub.ai/user/thesamething) <br>
- [AILove homepage](https://heerweiyi.cc) <br>
- [AILove Agent API base](https://heerweiyi.cc/api/v1) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, API calls] <br>
**Output Format:** [Markdown with inline bash, text, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses AILOVE_API_KEY and includes optional scheduled morning and evening update commands.] <br>

## Skill Version(s): <br>
1.4.2 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

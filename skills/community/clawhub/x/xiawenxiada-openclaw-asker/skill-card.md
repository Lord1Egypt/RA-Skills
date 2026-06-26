## Description: <br>
This OpenClaw skill submits up to three daily AI-generated social and emotional questions to the 虾问瞎答 question pool and can poll for answered Q/A to return to the user. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ckken](https://clawhub.ai/user/ckken) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and operators use this skill to automate lightweight question submission to the 虾问瞎答 pool, then optionally retrieve human answers and notify the user through the console or configured chat channels. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Question and answer content plus a persistent device identifier are sent to online services when the scripts run. <br>
Mitigation: Confirm that the configured endpoint is trusted, use a dedicated device identifier when appropriate, and delete or override ~/.xwd_device_id to reset the persisted identifier. <br>
Risk: Loop polling, cron scheduling, and webhook notifications can repeatedly send answer content to external chat or bot services. <br>
Mitigation: Enable --loop, cron jobs, and webhook credentials only after the user approves the workflow, and use dedicated webhook or bot credentials for this skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ckken/xiawenxiada-openclaw-asker) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/ckken) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Console text, webhook message text, and Markdown-style setup guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Network requests use configured endpoints and optional webhook credentials; answer polling may run once or on an interval.] <br>

## Skill Version(s): <br>
0.3.3 (source: server release evidence and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

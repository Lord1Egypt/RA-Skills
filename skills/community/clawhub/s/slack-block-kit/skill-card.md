## Description: <br>
Send rich Slack Block Kit messages for native tables and structured layouts when formatting tabular data, sending Block Kit payloads, or when markdown tables render poorly in Slack. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bill492](https://clawhub.ai/user/bill492) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to generate Slack Block Kit table payloads and prepare Slack API calls for messages that need structured tabular layouts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated Slack messages may be sent to the wrong destination or thread if channel and thread values are not reviewed. <br>
Mitigation: Review the destination channel, thread timestamp, fallback text, and generated blocks before sending. <br>
Risk: Posting through the Slack API uses a Slack bot token when the user directs the agent to send a message. <br>
Mitigation: Use a least-privilege Slack bot token and avoid exposing token values in prompts, logs, or generated payloads. <br>


## Reference(s): <br>
- [Slack Block Kit table block reference](https://docs.slack.dev/reference/block-kit/blocks/table-block/) <br>
- [Slack chat.postMessage API](https://slack.com/api/chat.postMessage) <br>
- [ClawHub skill page](https://clawhub.ai/bill492/slack-block-kit) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and Slack Block Kit JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The table script can output either a full JSON object with blocks or a blocks-only array, with optional compact formatting.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
